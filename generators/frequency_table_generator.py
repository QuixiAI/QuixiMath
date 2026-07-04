import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid

# Categorical contexts: (intro noun phrase, category labels).
CATEGORICAL = [
    ("favorite color", ["Red", "Blue", "Green", "Yellow", "Purple"]),
    ("favorite pet", ["Dog", "Cat", "Fish", "Bird", "Rabbit"]),
    ("favorite sport", ["Soccer", "Tennis", "Golf", "Track"]),
    ("favorite fruit", ["Apple", "Banana", "Cherry", "Grape", "Melon"]),
]


class FrequencyTableGenerator(ProblemGenerator):
    """
    Reading frequency tables and histograms: total the counts, find
    the mode, compute an exact relative frequency, read a cumulative
    count, and count values above a histogram threshold. Every table
    is embedded in the problem text so the answer is recomputable
    from it alone.

    Variants:
    - total:     sum all the frequencies
    - mode:      the category with the (unique) highest frequency
    - relative:  relative frequency of one category as an exact
                 reduced fraction
    - cumulative: running total of histogram bins up to a bin
    - above:     count of values in histogram bins at or above a cut

    Op-codes used:
    - FREQ_SETUP: the table and the question
    - A (established): running sums
    - MODE (established, simple_stats): highest frequency -> category
    - REWRITE / FRAC_REDUCE (established): the relative-frequency ratio
    - Z: the count, category, or exact fraction
    """

    VARIANTS = ["total", "mode", "relative", "cumulative", "above"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _running_sum_steps(values):
        """A-step running total; returns (steps, total)."""
        steps = []
        run = values[0]
        for v in values[1:]:
            steps.append(step("A", run, v, run + v))
            run += v
        return steps, run

    def _categorical(self, unique_mode=False):
        topic, pool = random.choice(CATEGORICAL)
        n = random.randint(4, min(5, len(pool)))
        cats = pool[:n]
        while True:
            freqs = [random.randint(1, 12) for _ in cats]
            if not unique_mode:
                break
            top = max(freqs)
            if freqs.count(top) == 1:
                break
        table = ", ".join(f"{c}: {f}" for c, f in zip(cats, freqs))
        return topic, cats, freqs, table

    def _histogram(self):
        base = random.choice([0, 50, 60, 70])
        width = 10
        n = random.randint(4, 5)
        bins = [f"{base + i * width}-{base + i * width + width - 1}"
                for i in range(n)]
        freqs = [random.randint(1, 15) for _ in bins]
        table = ", ".join(f"{b}: {f}" for b, f in zip(bins, freqs))
        return bins, freqs, table

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "total":
            topic, cats, freqs, table = self._categorical()
            steps = [step("FREQ_SETUP", f"table — {table}",
                          "total count")]
            sum_steps, total = self._running_sum_steps(freqs)
            steps += sum_steps
            answer = str(total)
            problem = (f"A survey records each person's {topic}. The "
                       f"frequencies are — {table}. How many people "
                       f"were surveyed in total?")
        elif variant == "mode":
            topic, cats, freqs, table = self._categorical(unique_mode=True)
            top = max(freqs)
            winner = cats[freqs.index(top)]
            steps = [
                step("FREQ_SETUP", f"table — {table}",
                     "most frequent category"),
                step("MODE", top, winner),
            ]
            answer = winner
            problem = (f"A survey records each person's {topic}. The "
                       f"frequencies are — {table}. Which category is "
                       f"the mode?")
        elif variant == "relative":
            topic, cats, freqs, table = self._categorical()
            idx = random.randrange(len(cats))
            cat, f = cats[idx], freqs[idx]
            sum_steps, total = self._running_sum_steps(freqs)
            frac = Fraction(f, total)
            steps = [step("FREQ_SETUP", f"table — {table}",
                          f"relative frequency of {cat}")]
            steps += sum_steps
            steps.append(step("REWRITE", f"{cat}: {f}/{total}"))
            if str(frac) != f"{f}/{total}":
                steps.append(step("FRAC_REDUCE", f"{f}/{total}",
                                  str(frac)))
            answer = str(frac)
            problem = (f"A survey records each person's {topic}. The "
                       f"frequencies are — {table}. What is the "
                       f"relative frequency of {cat}? Give an exact "
                       f"fraction.")
        elif variant == "cumulative":
            bins, freqs, table = self._histogram()
            cut = random.randint(1, len(bins) - 1)
            steps = [step("FREQ_SETUP", f"histogram — {table}",
                          f"cumulative count up to {bins[cut]}")]
            sum_steps, total = self._running_sum_steps(freqs[:cut + 1])
            steps += sum_steps
            answer = str(total)
            problem = (f"A histogram of scores has these bin counts — "
                       f"{table}. What is the cumulative count of "
                       f"scores through the {bins[cut]} bin?")
        else:
            bins, freqs, table = self._histogram()
            cut = random.randint(1, len(bins) - 1)
            lo = bins[cut].split("-")[0]
            tail = freqs[cut:]
            steps = [step("FREQ_SETUP", f"histogram — {table}",
                          f"count at or above {lo}")]
            if len(tail) == 1:
                total = tail[0]
                steps.append(step("REWRITE", f"only bin {bins[cut]}: "
                                  f"{total}"))
            else:
                sum_steps, total = self._running_sum_steps(tail)
                steps += sum_steps
            answer = str(total)
            problem = (f"A histogram of scores has these bin counts — "
                       f"{table}. How many scores are at least {lo}?")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"frequency_table_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

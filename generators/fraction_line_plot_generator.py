"""Read measurements from evenly spaced fraction line plots.

Variants: ``count_at_least``, ``longest_minus_shortest``, ``total_length``,
and ``equal_share``. Op-codes: ``STAT_SETUP``, ``PLOT_READ``, ``M``, ``A``,
``S``, ``D``, ``CHECK``, and ``Z``. Plot units are 1/2, 1/4, or 1/8;
rows include every intervening multiple and use reduced mixed-number labels.
Random multiplicities, shifts, contexts, and four phrasings give unbounded
capacity; equal shares are constrained to hand-friendly denominators.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt
from stats_common import MARK, frac_label, render_line_plot, running_sum_steps


STATISTICS = True
UNITS = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8))
CONTEXTS = (
    ("pencil lengths", "inch", "inches", "pencil"),
    ("ribbon lengths", "foot", "feet", "ribbon"),
    ("rainfall amounts", "inch", "inches", "day"),
    ("board lengths", "foot", "feet", "board"),
    ("wire lengths", "meter", "meters", "wire"),
    ("fabric lengths", "yard", "yards", "piece"),
)
SETTINGS = ("art room", "classroom", "community workshop", "design lab",
            "field station", "library project", "maker space", "math club",
            "science lab", "school fair", "survey office", "training center")
QUERIES = {
    "count_at_least": (
        "How many measurements are at least {threshold} {plural}?",
        "Count all plotted items with length at least {threshold} {plural}.",
        "Use the rows from {threshold} {plural} upward to find the count.",
        "Find the total frequency at or above {threshold} {plural}.",
    ),
    "longest_minus_shortest": (
        "What is the difference between the longest and shortest measurements?",
        "Subtract the shortest plotted length from the longest.",
        "Use the two end rows to find the measurement range.",
        "Find longest minus shortest and include the unit.",
    ),
    "total_length": (
        "Find the total of all plotted measurements and include the unit.",
        "Multiply each length by its frequency, then add the products.",
        "What combined length do all of the plotted items have?",
        "Compute the exact weighted sum of the line-plot values.",
    ),
    "equal_share": (
        "If the total is shared equally among all items, what is each share?",
        "Divide the combined length by the number of plotted items.",
        "Find the exact equal-share length, including the unit.",
        "Compute the mean measurement from the fraction line plot.",
    ),
}


def _counts(equal_share=False):
    while True:
        unit = random.choice(UNITS)
        start_index = random.randint(1, 8)
        width = random.randint(3, 7)
        values = [unit * (start_index + index) for index in range(width + 1)]
        counts = {value: random.randint(0, 5) for value in values}
        counts[values[0]] = random.randint(1, 5)
        counts[values[-1]] = random.randint(1, 5)
        n = sum(counts.values())
        total = sum((value * count for value, count in counts.items()), Fraction())
        share = total / n
        if 6 <= n <= 24 and (not equal_share
                             or share.denominator in (1, 2, 4, 8, 16)):
            return unit, counts


def _answer_measure(value, singular, plural):
    return f"{frac_label(value)} {singular if value == 1 else plural}"


def _read_step(value, count):
    return step("PLOT_READ", f"row {frac_label(value)}",
                MARK * count if count else "none", count)


class FractionLinePlotGenerator(ProblemGenerator):
    """Generate exact fraction-line-plot measurement exercises."""

    VARIANTS = ("count_at_least", "longest_minus_shortest", "total_length",
                "equal_share")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _build(variant):
        unit, counts = _counts(equal_share=variant == "equal_share")
        topic, singular, plural, noun = random.choice(CONTEXTS)
        title = (f"Fraction line plot of {topic} in {plural} "
                 f"(each {MARK} is one {noun}; row unit = {frac_label(unit)}):")
        plot = render_line_plot(counts, unit, title)
        prefix = (f"At the {random.choice(SETTINGS)}, read the display below.\n"
                  f"{plot}")
        n = sum(counts.values())
        steps = [step("STAT_SETUP", f"fraction line plot of {topic}",
                      f"unit={prob_txt(unit)}, n={n}")]
        fields = {"plural": plural}
        if variant == "count_at_least":
            threshold = random.choice(list(counts)[1:-1])
            selected = [(value, count) for value, count in counts.items()
                        if value >= threshold]
            for value, count in selected:
                steps.append(_read_step(value, count))
            additions, answer_value = running_sum_steps(
                [count for _, count in selected if count])
            steps.extend(additions)
            steps.append(step("CHECK", f"at least {frac_label(threshold)}",
                              answer_value))
            answer = str(answer_value)
            fields["threshold"] = frac_label(threshold)
        elif variant == "longest_minus_shortest":
            shortest, longest = min(counts), max(counts)
            difference = longest - shortest
            steps.extend([
                _read_step(shortest, counts[shortest]),
                _read_step(longest, counts[longest]),
                step("S", prob_txt(longest), prob_txt(shortest),
                     prob_txt(difference)),
                step("CHECK", "end rows contain measurements", "yes"),
            ])
            answer = _answer_measure(difference, singular, plural)
        else:
            products = []
            for value, count in counts.items():
                product = value * count
                steps.extend([
                    _read_step(value, count),
                    step("M", prob_txt(value), count, prob_txt(product)),
                ])
                if product:
                    products.append(product)
            additions, total = running_sum_steps(products)
            steps.extend(additions)
            if variant == "total_length":
                steps.append(step("CHECK", "weighted measurement total",
                                  prob_txt(total)))
                answer = _answer_measure(total, singular, plural)
            else:
                share = total / n
                steps.extend([
                    step("D", prob_txt(total), n, prob_txt(share)),
                    step("CHECK", "share times item count",
                         f"{prob_txt(share)} × {n} = {prob_txt(total)}"),
                ])
                answer = _answer_measure(share, singular, plural)
        return prefix, steps, answer, fields

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        prefix, steps, answer, fields = self._build(variant)
        query = random.choice(QUERIES[variant]).format(**fields)
        problem = f"{prefix}\n{query}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_fraction_line_plot_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

"""Read and estimate statistics from inclusive grouped-frequency classes.

Variants: ``mean_from_midpoints``, ``modal_class``, ``median_class``,
``estimated_median``, and ``total_and_percent_in_class``. Op-codes:
``FREQ_SETUP``, ``RULE``, ``BIN_COUNT``, ``MID_ROW``, ``CUM_ROW``, ``MODE``,
``STAT_COUNT``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``. Class
widths are 5, 10, or 20 and totals use only factors 2 and 5; midpoint means
therefore terminate, while estimated medians are rejection-sampled until
the stated interpolation formula terminates exactly. Random starts, widths,
frequencies, settings, contexts, and four phrasings give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import pct, terminates
from stats_common import bin_label, num_txt, render_bins, running_sum_steps


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
TOPICS = (
    "age ranges", "battery-life measurements", "commute times",
    "daily sales", "delivery times", "exercise minutes", "package weights",
    "plant heights", "quiz scores", "rainfall readings", "reading times",
    "travel distances",
)
QUERIES = {
    "mean_from_midpoints": (
        "Estimate the mean using each class midpoint.",
        "Multiply every midpoint by its frequency and find the grouped mean.",
        "What exact mean estimate comes from the class midpoints?",
        "Use the midpoint approximation to calculate the average.",
    ),
    "modal_class": (
        "Identify the unique modal class and report its frequency.",
        "Which interval has the greatest count?",
        "Find the single most frequent class in the table.",
        "Report the tallest grouped-frequency class with its count.",
    ),
    "median_class": (
        "Apply the stated cumulative rule to identify the median class.",
        "Which first class reaches half of the total frequency?",
        "Use cumulative counts to report the median interval and witness.",
        "Find the class containing the grouped-data median position.",
    ),
    "estimated_median": (
        "Use the stated interpolation formula to estimate the median.",
        "Substitute the median-class quantities into the supplied rule.",
        "Find the exact interpolated grouped median.",
        "Calculate the median estimate from L, cumulative frequency, f, and w.",
    ),
    "total_and_percent_in_class": (
        "Report the total frequency and the percent in the target class.",
        "Find both n and the target interval's percentage of all observations.",
        "Add all counts, then convert the named class frequency to a percent.",
        "Give a composite total-and-relative-frequency answer for the target.",
    ),
}


def _composition(total, parts):
    cuts = sorted(random.sample(range(1, total), parts - 1))
    points = [0, *cuts, total]
    return [right - left for left, right in zip(points, points[1:])]


def _table(unique_mode=False, even_total=False):
    width = random.choice((5, 10, 20))
    start = width * random.randint(0, 10)
    classes = random.randint(3, 6)
    totals = (20, 40, 50) if even_total else (20, 25, 40, 50)
    while True:
        total = random.choice(totals)
        frequencies = _composition(total, classes)
        top = max(frequencies)
        if not unique_mode or frequencies.count(top) == 1:
            break
    labels = [bin_label(start + index * width, width)
              for index in range(classes)]
    return labels, frequencies, width, start


def _prefix(labels, frequencies, topic, extra=None):
    text = (f"At the {random.choice(SETTINGS)}, grouped {topic} use inclusive "
            f"integer classes.\nGrouped frequencies: "
            f"{render_bins(list(zip(labels, frequencies)))}")
    return f"{text}\n{extra}" if extra else text


def _setup_steps(labels, frequencies, topic):
    steps = [step("FREQ_SETUP", f"grouped {topic}",
                  f"n={sum(frequencies)}")]
    steps.extend(step("BIN_COUNT", label, frequency)
                 for label, frequency in zip(labels, frequencies))
    return steps


class GroupedDataGenerator(ProblemGenerator):
    """Generate exact grouped-frequency reading and estimation exercises."""

    VARIANTS = ("mean_from_midpoints", "modal_class", "median_class",
                "estimated_median", "total_and_percent_in_class")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _mean():
        labels, frequencies, _, _ = _table()
        topic = random.choice(TOPICS)
        prefix = _prefix(labels, frequencies, topic)
        steps = _setup_steps(labels, frequencies, topic)
        products = []
        for label, frequency in zip(labels, frequencies):
            low, high = map(int, label.split("-"))
            midpoint = Fraction(low + high, 2)
            product = midpoint * frequency
            products.append(product)
            steps.append(step("MID_ROW", label, num_txt(midpoint),
                              num_txt(product)))
        additions, weighted_total = running_sum_steps(products)
        steps.extend(additions)
        total = sum(frequencies)
        mean = weighted_total / total
        steps.extend([step("STAT_COUNT", total),
                      step("D", num_txt(weighted_total), total, num_txt(mean)),
                      step("CHECK", "midpoint estimate",
                           f"{num_txt(weighted_total)}/{total}", num_txt(mean))])
        return prefix, steps, num_txt(mean)

    @staticmethod
    def _modal():
        labels, frequencies, _, _ = _table(unique_mode=True)
        topic = random.choice(TOPICS)
        prefix = _prefix(labels, frequencies, topic)
        steps = _setup_steps(labels, frequencies, topic)
        index = frequencies.index(max(frequencies))
        answer = f"{labels[index]}; frequency {frequencies[index]}"
        steps.extend([step("MODE", labels[index], frequencies[index]),
                      step("CHECK", "unique greatest frequency", answer)])
        return prefix, steps, answer

    @staticmethod
    def _median_class(estimate=False):
        while True:
            labels, frequencies, width, start = _table(even_total=True)
            total = sum(frequencies)
            halfway = Fraction(total, 2)
            cumulative = 0
            median_index = None
            for index, frequency in enumerate(frequencies):
                before = cumulative
                cumulative += frequency
                if median_index is None and cumulative >= halfway:
                    median_index = index
                    median_before = before
                    median_cumulative = cumulative
            low = start + median_index * width
            offset = (halfway - median_before) / frequencies[median_index] * width
            median = Fraction(low) + offset
            if not estimate or terminates(median):
                break
        topic = random.choice(TOPICS)
        if estimate:
            rule = ("L + ((n/2 - CF before)/f)·w, where L is the lower "
                    "endpoint of the first class whose cumulative frequency "
                    "reaches n/2")
            prefix = _prefix(labels, frequencies, topic,
                             f"Estimated-median rule: {rule}.")
        else:
            rule = "the first class whose cumulative frequency reaches n/2"
            prefix = _prefix(labels, frequencies, topic,
                             f"Median-class rule: {rule}.")
        steps = _setup_steps(labels, frequencies, topic)
        steps.append(step("RULE", "estimated median" if estimate else
                          "median class", rule))
        running = 0
        for label, frequency in zip(labels[:median_index + 1],
                                    frequencies[:median_index + 1]):
            running += frequency
            steps.append(step("CUM_ROW", label, running))
        if not estimate:
            answer = (f"{labels[median_index]}; cumulative "
                      f"{median_cumulative} ≥ {num_txt(halfway)}")
            steps.append(step("CHECK", "first cumulative at least n/2",
                              answer))
            return prefix, steps, answer
        remaining = halfway - median_before
        fraction = remaining / frequencies[median_index]
        steps.extend([
            step("D", total, 2, num_txt(halfway)),
            step("S", num_txt(halfway), median_before, num_txt(remaining)),
            step("D", num_txt(remaining), frequencies[median_index],
                 num_txt(fraction)),
            step("M", num_txt(fraction), width, num_txt(offset)),
            step("A", low, num_txt(offset), num_txt(median)),
            step("CHECK", "interpolation", f"L={low}, w={width}",
                 num_txt(median)),
        ])
        return prefix, steps, num_txt(median)

    @staticmethod
    def _total_percent():
        labels, frequencies, _, _ = _table()
        topic = random.choice(TOPICS)
        target = random.randrange(len(labels))
        prefix = _prefix(labels, frequencies, topic,
                         f"Target class: {labels[target]}.")
        steps = _setup_steps(labels, frequencies, topic)
        additions, total = running_sum_steps(frequencies)
        steps.extend(additions)
        fraction = Fraction(frequencies[target], total)
        percent = pct(fraction)
        steps.extend([
            step("D", frequencies[target], total, num_txt(fraction)),
            step("M", num_txt(fraction), 100,
                 percent.removesuffix("%")),
            step("CHECK", "target share", labels[target], percent),
        ])
        answer = f"total {total}; {labels[target]}: {percent}"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "mean_from_midpoints":
            prefix, steps, answer = self._mean()
        elif variant == "modal_class":
            prefix, steps, answer = self._modal()
        elif variant == "median_class":
            prefix, steps, answer = self._median_class()
        elif variant == "estimated_median":
            prefix, steps, answer = self._median_class(estimate=True)
        else:
            prefix, steps, answer = self._total_percent()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_grouped_data_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

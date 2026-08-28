"""Construct and read contiguous-row integer dot plots.

Variants: ``construct``, ``read_count``, ``count_above_below``,
``most_common``, ``range_from_plot``, ``total_from_plot``, and
``median_from_plot``. Op-codes: ``STAT_SETUP``, ``SORT``, ``DOT_ROW``,
``PLOT_READ``, ``MEDIAN_PICK``, ``MEDIAN_PAIR``, ``MEAN_DIV``, ``A``, ``S``,
``M``, ``CHECK``, and ``Z``. End rows always contain data and every internal
integer row, including gaps, is rendered. Random count patterns, shifts,
contexts, raw-data shuffles, and four phrasings give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import MARK, num_txt, render_dot_plot, running_sum_steps, text_list


STATISTICS = True
CONTEXTS = (
    ("quiz scores", "student"), ("plant heights", "plant"),
    ("commute minutes", "traveler"), ("daily sales", "day"),
    ("rainfall measurements", "day"), ("shoe sizes", "person"),
    ("points per game", "game"), ("books read", "reader"),
)
SETTINGS = ("amber study", "birch survey", "cedar trial", "delta project",
            "ember lab", "forest audit", "granite program", "harbor test",
            "indigo review", "jade pilot", "kestrel study", "lunar trial")
QUERIES = {
    "construct": (
        "Construct the complete dot-plot frequency list.",
        "Count the raw values and report every row, including gaps.",
        "Build the dot plot as a value-to-count text list.",
        "Turn the observations into consecutive dot-plot rows.",
    ),
    "read_count": (
        "How many observations are shown at value {target}?",
        "Read the row for {target} and give its count.",
        "What frequency does the dot plot show at {target}?",
        "Count the marks on the {target} row.",
    ),
    "count_above_below": (
        "How many observations are strictly {relation} {threshold}?",
        "Add the dot counts for values {relation} {threshold}.",
        "Use the rows to count observations {relation} {threshold}.",
        "Find the total frequency strictly {relation} {threshold}.",
    ),
    "most_common": (
        "Identify the unique most common value and its frequency.",
        "Which row is uniquely tallest, and how many observations does it have?",
        "Find the mode from the dot plot and report its count.",
        "Read the unique modal value and frequency.",
    ),
    "range_from_plot": (
        "Find the range represented by the dot plot.",
        "Subtract the smallest plotted value from the largest.",
        "Use the two end rows to compute the data range.",
        "What is the exact maximum-minus-minimum spread?",
    ),
    "total_from_plot": (
        "Find the sum of all data values represented by the dot plot.",
        "Multiply each value by its count, then find the data total.",
        "Compute the weighted sum of every plotted observation.",
        "What do all of the data values add to?",
    ),
    "median_from_plot": (
        "Find the median of the data represented by the dot plot.",
        "Expand the row counts in order and determine the median.",
        "Use the plotted multiplicities to locate the middle value.",
        "Read the exact median from the ordered dot-plot data.",
    ),
}


def _counts(unique_mode=False):
    while True:
        low = random.randint(1, 25)
        width = random.randint(3, 7)
        values = list(range(low, low + width + 1))
        counts = {value: random.randint(0, 6) for value in values}
        counts[values[0]] = random.randint(1, 6)
        counts[values[-1]] = random.randint(1, 6)
        total = sum(counts.values())
        top = max(counts.values())
        if 7 <= total <= 28 and (not unique_mode
                                or list(counts.values()).count(top) == 1):
            return counts


def _data(counts):
    return [value for value in sorted(counts) for _ in range(counts[value])]


def _plot_prompt(counts, topic, noun):
    title = f"Dot plot of {topic} (each {MARK} is one {noun}):"
    return render_dot_plot(counts, title)


def _read_step(value, count):
    marks = MARK * count if count else "none"
    return step("PLOT_READ", f"row {value}", marks, count)


class DotPlotGenerator(ProblemGenerator):
    """Generate exact integer dot-plot construction and reading exercises."""

    VARIANTS = ("construct", "read_count", "count_above_below",
                "most_common", "range_from_plot", "total_from_plot",
                "median_from_plot")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _construct():
        counts = _counts()
        values = _data(counts)
        random.shuffle(values)
        topic, _ = random.choice(CONTEXTS)
        prefix = (f"At the {random.choice(SETTINGS)}, raw {topic} are: "
                  + ", ".join(map(str, values)) + ".")
        steps = [
            step("STAT_SETUP", f"raw {topic}", f"n={len(values)}"),
            step("SORT", ",".join(map(str, sorted(values)))),
        ]
        for value, count in counts.items():
            steps.append(step("DOT_ROW", value, count))
        steps.append(step("CHECK", "row counts sum",
                          " + ".join(str(count) for count in counts.values()
                                     if count), len(values)))
        answer = text_list(counts)
        return prefix, steps, answer, {}

    @staticmethod
    def _read(variant):
        counts = _counts(unique_mode=variant == "most_common")
        topic, noun = random.choice(CONTEXTS)
        prefix = (f"At the {random.choice(SETTINGS)}, read the display below.\n"
                  + _plot_prompt(counts, topic, noun))
        steps = [step("STAT_SETUP", f"dot plot of {topic}",
                      f"n={sum(counts.values())}")]
        fields = {}
        if variant == "read_count":
            target = random.choice(list(counts))
            answer = str(counts[target])
            steps.extend([_read_step(target, counts[target]),
                          step("CHECK", f"row {target}", counts[target])])
            fields = {"target": target}
        elif variant == "count_above_below":
            threshold = random.choice(list(counts)[1:-1])
            relation = random.choice(("above", "below"))
            selected = [value for value in counts
                        if value > threshold] if relation == "above" else [
                            value for value in counts if value < threshold]
            row_counts = [counts[value] for value in selected]
            for value in selected:
                steps.append(_read_step(value, counts[value]))
            additions, total = running_sum_steps(row_counts)
            steps.extend(additions)
            steps.append(step("CHECK", f"strictly {relation} {threshold}", total))
            answer = str(total)
            fields = {"relation": relation, "threshold": threshold}
        elif variant == "most_common":
            mode = max(counts, key=counts.get)
            count = counts[mode]
            steps.extend([_read_step(mode, count),
                          step("CHECK", "unique tallest row", f"{mode}: {count}")])
            answer = f"{mode} ({count} observations)"
        elif variant == "range_from_plot":
            low, high = min(counts), max(counts)
            value = high - low
            steps.extend([_read_step(low, counts[low]),
                          _read_step(high, counts[high]),
                          step("S", high, low, value),
                          step("CHECK", "end rows contain data", "yes")])
            answer = str(value)
        elif variant == "total_from_plot":
            products = []
            for value, count in counts.items():
                product = value * count
                steps.extend([_read_step(value, count),
                              step("M", value, count, product)])
                products.append(product)
            additions, total = running_sum_steps(
                [product for product in products if product])
            steps.extend(additions)
            steps.append(step("CHECK", "weighted data total", total))
            answer = str(total)
        else:
            values = _data(counts)
            for value, count in counts.items():
                steps.append(_read_step(value, count))
            steps.append(step("SORT", ",".join(map(str, values))))
            middle = len(values) // 2
            if len(values) % 2:
                median = Fraction(values[middle])
                steps.append(step("MEDIAN_PICK", f"position {middle + 1}",
                                  values[middle]))
            else:
                left, right = values[middle - 1], values[middle]
                median = Fraction(left + right, 2)
                steps.extend([
                    step("MEDIAN_PAIR", left, right),
                    step("A", left, right, left + right),
                    step("MEAN_DIV", left + right, 2, num_txt(median)),
                ])
            steps.append(step("CHECK", "ordered middle", num_txt(median)))
            answer = num_txt(median)
        return prefix, steps, answer, fields

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "construct":
            prefix, steps, answer, fields = self._construct()
        else:
            prefix, steps, answer, fields = self._read(variant)
        query = random.choice(QUERIES[variant]).format(**fields)
        problem = f"{prefix}\n{query}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_dot_plot_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

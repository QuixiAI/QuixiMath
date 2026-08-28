"""Construct and read integer and decimal stem-and-leaf plots.

Variants: ``construct``, ``list_values``, ``count_in_stem``,
``median_from_plot``, ``range_from_plot``, ``decimal_key``, and
``count_between``. Op-codes: ``STAT_SETUP``, ``LEAF_KEY``, ``STEM_ROW``,
``PLOT_READ``, ``SORT``, ``MEDIAN_PICK``, ``MEDIAN_PAIR``, ``MEAN_DIV``,
``S``, ``CHECK``, and ``Z``. Leaves ascend, empty intervening stems remain,
and every display supplies its key. Random values, shifts, contexts, and four
phrasings per variant give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import (BAR, num_txt, render_stem_leaf, stem_leaf_list,
                          stem_leaf_value)


STATISTICS = True
CONTEXTS = ("ages", "battery hours", "commute times", "daily sales",
            "package weights", "plant heights", "points per game",
            "quiz scores", "rainfall readings", "shoe sizes")
SETTINGS = ("amber study", "birch survey", "cedar trial", "delta project",
            "ember lab", "forest audit", "granite program", "harbor test",
            "indigo review", "jade pilot", "kestrel study", "lunar trial")
QUERIES = {
    "construct": (
        "Construct the complete stem-and-leaf text list.",
        "Sort the raw data and report every stem with its leaves.",
        "Build the stem-and-leaf plot, retaining any empty stem.",
        "Turn the observations into the required stem summary.",
    ),
    "list_values": (
        "List every represented data value in ascending order.",
        "Use the key to reconstruct the complete sorted data set.",
        "Read all stems and leaves back into numerical values.",
        "Decode the plot and give its ordered observation list.",
    ),
    "count_in_stem": (
        "How many observations appear in stem {stem}?",
        "Count the leaves in the row with stem {stem}.",
        "What frequency does stem {stem} represent?",
        "Read the stem {stem} row and report its count.",
    ),
    "median_from_plot": (
        "Find the median of the represented data.",
        "Use the ordered leaves to locate the exact median.",
        "Decode the observations and determine their middle value.",
        "Read the exact median from the stem-and-leaf plot.",
    ),
    "range_from_plot": (
        "Find the range of the represented data.",
        "Subtract the smallest decoded value from the largest.",
        "Use the first and last leaves to compute the range.",
        "Determine the exact maximum-minus-minimum spread.",
    ),
    "decimal_key": (
        "Use the decimal key to list every value in ascending order.",
        "Decode all one-decimal observations from the plot.",
        "Read the decimal stem-and-leaf display back into a sorted list.",
        "Interpret the key and report every represented decimal value.",
    ),
    "count_between": (
        "How many values lie from {lower} through {upper}, inclusive?",
        "Count observations between {lower} and {upper}, including both endpoints.",
        "Use the leaves to find the frequency in [{lower}, {upper}].",
        "Find the number of represented values at least {lower} and at most {upper}.",
    ),
}


def _values(decimal=False):
    while True:
        first_stem = random.randint(0 if decimal else 1, 7)
        stem_count = random.randint(2, 4)
        stems = list(range(first_stem, first_stem + stem_count))
        n = random.randint(7, 15)
        pairs = [(random.choice(stems), random.randint(0, 9)) for _ in range(n - 2)]
        pairs.extend([(stems[0], random.randint(0, 9)),
                      (stems[-1], random.randint(0, 9))])
        values = [stem_leaf_value(stem, leaf, decimal) for stem, leaf in pairs]
        if len(set(values)) >= 4:
            return values


def _rows(values, decimal=False):
    scaled = [(int(Fraction(value) * (10 if decimal else 1))) for value in values]
    pairs = [divmod(value, 10) for value in sorted(scaled)]
    rows = {stem: [] for stem in range(pairs[0][0], pairs[-1][0] + 1)}
    for stem, leaf in pairs:
        rows[stem].append(leaf)
    return rows


def _value_list(values):
    return ", ".join(num_txt(value) for value in sorted(values))


def _trace_rows(values, decimal=False):
    rows = _rows(values, decimal)
    steps = []
    for stem, leaves in rows.items():
        leaf_text = " ".join(map(str, leaves)) or "none"
        decoded = [stem_leaf_value(stem, leaf, decimal) for leaf in leaves]
        steps.append(step("STEM_ROW", stem, leaf_text,
                          ",".join(num_txt(value) for value in decoded) or "none"))
    return steps, rows


class StemAndLeafGenerator(ProblemGenerator):
    """Generate exact keyed stem-and-leaf construction and reading tasks."""

    VARIANTS = ("construct", "list_values", "count_in_stem",
                "median_from_plot", "range_from_plot", "decimal_key",
                "count_between")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _construct():
        values = _values()
        raw = list(values)
        random.shuffle(raw)
        topic = random.choice(CONTEXTS)
        prefix = (f"At the {random.choice(SETTINGS)}, raw {topic} are: "
                  + ", ".join(num_txt(value) for value in raw) + ". "
                  f"Use tens as stems and ones as leaves; for example, "
                  f"stem 2 with leaf 3 means 23.")
        steps = [step("STAT_SETUP", f"raw {topic}", f"n={len(values)}"),
                 step("SORT", ",".join(num_txt(value)
                                          for value in sorted(values)))]
        row_steps, _ = _trace_rows(values)
        steps.extend(row_steps)
        steps.append(step("CHECK", "all leaves counted", len(values)))
        return prefix, steps, stem_leaf_list(values), {}

    @staticmethod
    def _display(variant):
        decimal = variant == "decimal_key"
        values = _values(decimal)
        topic = random.choice(CONTEXTS)
        title = f"Stem-and-leaf plot of {topic}"
        plot = render_stem_leaf(values, decimal=decimal, title=title)
        prefix = (f"At the {random.choice(SETTINGS)}, read the display below.\n"
                  f"{plot}")
        rows = _rows(values, decimal)
        first_stem = next(stem for stem, leaves in rows.items() if leaves)
        first_leaf = rows[first_stem][0]
        key_value = stem_leaf_value(first_stem, first_leaf, decimal)
        steps = [
            step("STAT_SETUP", f"stem-and-leaf plot of {topic}",
                 f"n={len(values)}"),
            step("LEAF_KEY", f"{first_stem} {BAR} {first_leaf}",
                 num_txt(key_value)),
        ]
        row_steps, rows = _trace_rows(values, decimal)
        steps.extend(row_steps)
        fields = {}
        ordered = sorted(values)
        if variant in ("list_values", "decimal_key"):
            answer = _value_list(ordered)
            steps.extend([
                step("SORT", ",".join(num_txt(value) for value in ordered)),
                step("CHECK", "decoded count", len(ordered)),
            ])
        elif variant == "count_in_stem":
            stem = random.choice(list(rows))
            count = len(rows[stem])
            steps.extend([
                step("PLOT_READ", f"stem {stem}",
                     " ".join(map(str, rows[stem])) or "none", count),
                step("CHECK", f"leaf count in stem {stem}", count),
            ])
            answer = str(count)
            fields = {"stem": stem}
        elif variant == "median_from_plot":
            steps.append(step("SORT", ",".join(num_txt(value)
                                                   for value in ordered)))
            middle = len(ordered) // 2
            if len(ordered) % 2:
                median = ordered[middle]
                steps.append(step("MEDIAN_PICK", f"position {middle + 1}",
                                  num_txt(median)))
            else:
                left, right = ordered[middle - 1], ordered[middle]
                median = (left + right) / 2
                steps.extend([
                    step("MEDIAN_PAIR", num_txt(left), num_txt(right)),
                    step("MEAN_DIV", num_txt(left + right), 2, num_txt(median)),
                ])
            steps.append(step("CHECK", "ordered middle", num_txt(median)))
            answer = num_txt(median)
        elif variant == "range_from_plot":
            low, high = ordered[0], ordered[-1]
            difference = high - low
            steps.extend([
                step("PLOT_READ", "smallest", num_txt(low)),
                step("PLOT_READ", "largest", num_txt(high)),
                step("S", num_txt(high), num_txt(low), num_txt(difference)),
                step("CHECK", "max minus min", num_txt(difference)),
            ])
            answer = num_txt(difference)
        else:
            indices = sorted(random.sample(range(len(ordered)), 2))
            lower, upper = ordered[indices[0]], ordered[indices[1]]
            count = sum(lower <= value <= upper for value in ordered)
            steps.extend([
                step("PLOT_READ", f"interval {num_txt(lower)} to {num_txt(upper)}",
                     count),
                step("CHECK", "inclusive endpoints", count),
            ])
            answer = str(count)
            fields = {"lower": num_txt(lower), "upper": num_txt(upper)}
        return prefix, steps, answer, fields

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "construct":
            prefix, steps, answer, fields = self._construct()
        else:
            prefix, steps, answer, fields = self._display(variant)
        query = random.choice(QUERIES[variant]).format(**fields)
        problem = f"{prefix}\n{query}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_stem_and_leaf_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

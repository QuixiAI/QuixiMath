"""Construct and read inclusive-bin text histograms.

Variants: ``bin_counts``, ``bin_of_value``, ``count_between``, ``shape``,
and ``relative_bin``. Op-codes: ``STAT_SETUP``, ``RULE``, ``SORT``,
``BIN_ASSIGN``, ``BIN_COUNT``, ``A``, ``D``, ``CHECK``, and ``Z``. Bin
widths are 5, 10, or 20; all displayed ranges are contiguous inclusive
integer intervals. Shape uses the comparison rule supplied in its prompt,
and relative frequencies remain exact reduced fractions. Random bin counts,
values, widths, starts, contexts, settings, and four phrasings give
unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt
from stats_common import bin_counts, render_bins, running_sum_steps


STATISTICS = True
CONTEXTS = (
    "arrival times", "battery lifetimes", "commute times", "daily sales",
    "delivery times", "exercise minutes", "package weights", "plant heights",
    "quiz scores", "rainfall readings", "reading times", "travel distances",
)
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
QUERIES = {
    "bin_counts": (
        "Give the count in every histogram bin.",
        "Sort and assign the observations, then report all bin frequencies.",
        "Construct the complete histogram frequency list.",
        "Group the raw values into the stated bins and list each count.",
    ),
    "bin_of_value": (
        "Which inclusive bin contains {value}?",
        "Locate {value} in the histogram's bin intervals.",
        "Give the exact bin label to which {value} belongs.",
        "Under the stated inclusive-bin rule, where is {value} assigned?",
    ),
    "count_between": (
        "How many observations lie in bins {first} through {last}, inclusive?",
        "Add the frequencies from {first} to {last}, including both endpoints.",
        "Find the total count across the consecutive bins {first} through {last}.",
        "How many data values fall anywhere from bin {first} to bin {last}?",
    ),
    "shape": (
        "Apply the stated modal-bin rule to classify the histogram's shape.",
        "Compare the counts on the two sides of the peak and describe the shape.",
        "Report the skew label together with the peak bin and tail endpoint.",
        "Use the supplied side-count rule to interpret the histogram.",
    ),
    "relative_bin": (
        "What fraction of all observations lies in bin {target}?",
        "Give the relative frequency of {target} as a reduced fraction.",
        "Divide the count in {target} by the total count.",
        "Find the exact fractional share represented by bin {target}.",
    ),
}


def _random_counts():
    """Positive counts for 8--16 observations across 3--5 bins."""
    while True:
        counts = [random.randint(1, 5) for _ in range(random.randint(3, 5))]
        if 8 <= sum(counts) <= 16:
            return counts


def _shape_counts():
    """A unique mode with a requested left/right/tied side-count outcome."""
    wanted = random.choice(("left-skewed", "right-skewed", "symmetric"))
    while True:
        counts = _random_counts()
        top = max(counts)
        if counts.count(top) != 1:
            continue
        peak = counts.index(top)
        left = sum(counts[:peak])
        right = sum(counts[peak + 1:])
        actual = ("right-skewed" if right > left else
                  "left-skewed" if left > right else "symmetric")
        if actual == wanted:
            return counts


def _dataset(for_shape=False):
    width = random.choice((5, 10, 20))
    start = width * random.randint(0, 8)
    counts = _shape_counts() if for_shape else _random_counts()
    values = []
    for index, count in enumerate(counts):
        low = start + index * width
        high = low + width - 1
        values.extend(random.randint(low, high) for _ in range(count))
    random.shuffle(values)
    bins = bin_counts(values, width, start)
    return values, bins, width, start


def _read_steps(bins, topic):
    steps = [step("STAT_SETUP", f"histogram of {topic}",
                  f"n={sum(count for _, count in bins)}")]
    for label, count in bins:
        steps.append(step("BIN_COUNT", label, count))
    counts = [count for _, count in bins]
    steps.append(step("CHECK", "split", " + ".join(map(str, counts)),
                      sum(counts)))
    return steps


def _label_for(value, width, start):
    index = (value - start) // width
    low = start + index * width
    return f"{low}-{low + width - 1}"


class HistogramConstructGenerator(ProblemGenerator):
    """Generate exact histogram construction and interpretation exercises."""

    VARIANTS = ("bin_counts", "bin_of_value", "count_between", "shape",
                "relative_bin")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _construct(topic):
        values, bins, width, start = _dataset()
        prefix = (f"At the {random.choice(SETTINGS)}, raw {topic}: "
                  f"{', '.join(map(str, values))}.\n"
                  f"Bin rule: use inclusive integer bins of width {width} "
                  f"starting at {start}.")
        steps = [
            step("STAT_SETUP", f"raw {topic}", f"n={len(values)}"),
            step("RULE", "inclusive bins",
                 f"width {width}, start {start}, both endpoints included"),
            step("SORT", ",".join(map(str, sorted(values)))),
        ]
        for value in sorted(values):
            steps.append(step("BIN_ASSIGN", value,
                              _label_for(value, width, start)))
        for label, count in bins:
            steps.append(step("BIN_COUNT", label, count))
        steps.append(step("CHECK", "split",
                          " + ".join(str(count) for _, count in bins),
                          len(values)))
        return prefix, steps, render_bins(bins), {}

    @staticmethod
    def _read(variant, topic):
        _, bins, width, start = _dataset(for_shape=variant == "shape")
        prefix = (f"At the {random.choice(SETTINGS)}, a histogram of {topic} "
                  "uses contiguous inclusive integer bins.\n"
                  f"Histogram bins: {render_bins(bins)}")
        steps = [step("RULE", "inclusive bins",
                      f"width {width}, start {start}, both endpoints included")]
        steps.extend(_read_steps(bins, topic))
        labels = [label for label, _ in bins]
        counts = [count for _, count in bins]
        fields = {}

        if variant == "bin_of_value":
            index = random.randrange(len(bins))
            low, high = map(int, labels[index].split("-"))
            value = random.randint(low, high)
            answer = labels[index]
            steps.extend([step("BIN_ASSIGN", value, answer),
                          step("CHECK", f"{low} ≤ {value} ≤ {high}", answer)])
            fields = {"value": value}
        elif variant == "count_between":
            first_index = random.randrange(len(bins) - 1)
            last_index = random.randrange(first_index + 1, len(bins))
            selected = counts[first_index:last_index + 1]
            additions, total = running_sum_steps(selected)
            steps.extend(additions)
            answer = str(total)
            steps.append(step("CHECK", "inclusive selected bins", answer))
            fields = {"first": labels[first_index], "last": labels[last_index]}
        elif variant == "relative_bin":
            index = random.randrange(len(bins))
            total = sum(counts)
            fraction = Fraction(counts[index], total)
            answer = prob_txt(fraction)
            steps.extend([step("D", counts[index], total, answer),
                          step("CHECK", f"relative frequency {labels[index]}",
                               answer)])
            fields = {"target": labels[index]}
        else:
            peak = counts.index(max(counts))
            left, right = sum(counts[:peak]), sum(counts[peak + 1:])
            rule = ("find the unique modal bin; compare total counts strictly "
                    "left and strictly right of it; larger right means "
                    "right-skewed, larger left means left-skewed, and a tie "
                    "means symmetric")
            prefix += f"\nShape rule: {rule}."
            steps.append(step("RULE", "histogram shape", rule))
            left_steps, _ = running_sum_steps(counts[:peak])
            right_steps, _ = running_sum_steps(counts[peak + 1:])
            steps.extend(left_steps + right_steps)
            if right > left:
                label = "right-skewed"
                tail = labels[-1]
                witness = f"right count {right} > left count {left}"
                answer = f"{label}; peak in {labels[peak]}, tail to {tail}"
            elif left > right:
                label = "left-skewed"
                tail = labels[0]
                witness = f"left count {left} > right count {right}"
                answer = f"{label}; peak in {labels[peak]}, tail to {tail}"
            else:
                label = "symmetric"
                witness = f"left count {left} = right count {right}"
                answer = (f"{label}; peak in {labels[peak]}, equal side "
                          f"counts {left} = {right}")
            steps.append(step("CHECK", "shape comparison", witness, label))
        return prefix, steps, answer, fields

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        topic = random.choice(CONTEXTS)
        if variant == "bin_counts":
            prefix, steps, answer, fields = self._construct(topic)
        else:
            prefix, steps, answer, fields = self._read(variant, topic)
        query = random.choice(QUERIES[variant]).format(**fields)
        problem = f"{prefix}\n{query}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_histogram_construct_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

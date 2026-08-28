"""Compute percentile ranks and nearest-rank percentile values exactly.

Variants: ``percentile_rank``, ``value_at_percentile``,
``quartiles_by_rank``, ``between_percentiles``, and ``interpret``. Op-codes:
``STAT_SETUP``, ``SORT``, ``RULE``, ``COUNT``, ``M``, ``D``, ``S``, ``A``,
``CEIL``, ``PCT_RANK``, ``RANK_POS``, ``CHECK``, and ``Z``. Data values are
distinct, sample sizes come from 10, 20, 25, 40, and 50, and rank targets are
selected so percentile-rank answers are whole percents. Random samples,
shifts, contexts, settings, targets, and four phrasings give unbounded
capacity.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import pct
from stats_common import CONTEXTS, num_txt


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
SIZES = (10, 20, 25, 40, 50)
PERCENTILES = (10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90)
QUERIES = {
    "percentile_rank": (
        "Find the target value's percentile rank.",
        "What percent of observations are strictly below the target?",
        "Use the stated rank rule to calculate a percentile for the target.",
        "Count values below the target and report its percentile rank.",
    ),
    "value_at_percentile": (
        "Find the value at the requested percentile by nearest rank.",
        "Compute the rank position and read the corresponding ordered value.",
        "Which observation occupies the requested percentile position?",
        "Apply the supplied nearest-rank rule to locate the percentile value.",
    ),
    "quartiles_by_rank": (
        "Find Q1 and Q3 using nearest ranks 25% and 75%.",
        "Report both quartiles under the stated nearest-rank rule.",
        "Locate the 25th- and 75th-percentile observations.",
        "Use ordered rank positions to compute the two quartiles.",
    ),
    "between_percentiles": (
        "How many ordered observations lie between the two percentile values, inclusive?",
        "Count rank positions from the lower percentile value through the upper one.",
        "Find the inclusive number of observations between the requested percentiles.",
        "Use the two nearest ranks to determine the inclusive count between them.",
    ),
    "interpret": (
        "Interpret the target's percentile rank and give its ordered rank.",
        "State how much of the group is below the target and where it ranks.",
        "Give a composite percentile interpretation for the target value.",
        "Report both the percent below and the target's 1-indexed position.",
    ),
}


def _data():
    size = random.choice(SIZES)
    contexts = [ctx for ctx in CONTEXTS if ctx.hi - ctx.lo + 1 >= size]
    ctx = random.choice(contexts)
    values = random.sample(range(ctx.lo, ctx.hi + 1), size)
    random.shuffle(values)
    return values, ctx


def _valid_target_index(size):
    indexes = [index for index in range(1, size)
               if (100 * index) % size == 0]
    return random.choice(indexes)


def _nearest_position(size, percentile):
    return math.ceil(Fraction(percentile * size, 100))


def _prefix(values, ctx, extra):
    return (f"At the {random.choice(SETTINGS)}, distinct {ctx.label} are: "
            f"{', '.join(map(str, values))}.\n{extra}")


class PercentileGenerator(ProblemGenerator):
    """Generate exact percentile-rank and nearest-rank exercises."""

    VARIANTS = ("percentile_rank", "value_at_percentile",
                "quartiles_by_rank", "between_percentiles", "interpret")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _rank(interpret=False):
        values, ctx = _data()
        ordered = sorted(values)
        index = _valid_target_index(len(values))
        target = ordered[index]
        percent = pct(Fraction(index, len(values)))
        rule = "percent of values strictly below the target"
        prefix = _prefix(values, ctx,
                         f"Target value: {target}. Percentile-rank rule: {rule}.")
        numerator = 100 * index
        steps = [
            step("STAT_SETUP", "distinct percentile data", f"n={len(values)}"),
            step("SORT", ",".join(map(str, ordered))),
            step("RULE", "percentile rank", rule),
            step("COUNT", f"below {target}", index),
            step("M", 100, index, numerator),
            step("D", numerator, len(values), percent.removesuffix("%")),
            step("PCT_RANK", index, len(values), percent),
        ]
        if interpret:
            rank = index + 1
            steps.extend([step("A", index, 1, rank),
                          step("RANK_POS", rank, f"value {target}"),
                          step("CHECK", "interpretation", percent,
                               f"rank {rank} of {len(values)}")])
            answer = (f"above {percent} of the group; rank {rank} of "
                      f"{len(values)}")
        else:
            steps.append(step("CHECK", "strictly below", index, percent))
            answer = percent
        return prefix, steps, answer

    @staticmethod
    def _value():
        values, ctx = _data()
        ordered = sorted(values)
        percentile = random.choice(PERCENTILES)
        raw = Fraction(percentile * len(values), 100)
        position = _nearest_position(len(values), percentile)
        answer = str(ordered[position - 1])
        rule = "position = ⌈k·n/100⌉ in the sorted list"
        prefix = _prefix(values, ctx,
                         f"Requested percentile: {percentile}%. Nearest-rank "
                         f"rule: {rule}.")
        steps = [
            step("STAT_SETUP", "nearest-rank percentile", f"n={len(values)}"),
            step("SORT", ",".join(map(str, ordered))),
            step("RULE", "nearest rank", rule),
            step("M", Fraction(percentile, 100), len(values), num_txt(raw)),
            step("CEIL", num_txt(raw), position),
            step("RANK_POS", position, f"value {answer}"),
            step("CHECK", f"{percentile}th percentile", answer),
        ]
        return prefix, steps, answer

    @staticmethod
    def _quartiles():
        values, ctx = _data()
        ordered = sorted(values)
        rule = "position = ⌈k·n/100⌉ in the sorted list"
        prefix = _prefix(values, ctx,
                         f"Nearest-rank rule: {rule}.")
        steps = [step("STAT_SETUP", "nearest-rank quartiles",
                      f"n={len(values)}"),
                 step("SORT", ",".join(map(str, ordered))),
                 step("RULE", "nearest rank", rule)]
        answers = []
        for name, percentile in (("Q1", 25), ("Q3", 75)):
            raw = Fraction(percentile * len(values), 100)
            position = _nearest_position(len(values), percentile)
            value = ordered[position - 1]
            steps.extend([step("M", Fraction(percentile, 100), len(values),
                               num_txt(raw)),
                          step("CEIL", num_txt(raw), position),
                          step("RANK_POS", position, f"{name} value {value}")])
            answers.append((name, value))
        answer = f"Q1 = {answers[0][1]}; Q3 = {answers[1][1]}"
        steps.append(step("CHECK", "quartile order", answer))
        return prefix, steps, answer

    @staticmethod
    def _between():
        values, ctx = _data()
        ordered = sorted(values)
        lower, upper = random.choice(((10, 90), (20, 80), (25, 75),
                                      (30, 70), (40, 60)))
        first = _nearest_position(len(values), lower)
        last = _nearest_position(len(values), upper)
        count = last - first + 1
        rule = "position = ⌈k·n/100⌉ in the sorted list"
        prefix = _prefix(
            values, ctx,
            f"Lower percentile: {lower}%. Upper percentile: {upper}%. "
            f"Nearest-rank rule: {rule}.")
        steps = [step("STAT_SETUP", "between percentile values",
                      f"n={len(values)}"),
                 step("SORT", ",".join(map(str, ordered))),
                 step("RULE", "nearest rank", rule)]
        for percentile, position in ((lower, first), (upper, last)):
            raw = Fraction(percentile * len(values), 100)
            steps.extend([step("M", Fraction(percentile, 100), len(values),
                               num_txt(raw)),
                          step("CEIL", num_txt(raw), position),
                          step("RANK_POS", position,
                               f"value {ordered[position - 1]}")])
        difference = last - first
        steps.extend([step("S", last, first, difference),
                      step("A", difference, 1, count),
                      step("CHECK", "inclusive rank count",
                           f"{first} through {last}", count)])
        return prefix, steps, str(count)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "percentile_rank":
            prefix, steps, answer = self._rank()
        elif variant == "interpret":
            prefix, steps, answer = self._rank(interpret=True)
        elif variant == "value_at_percentile":
            prefix, steps, answer = self._value()
        elif variant == "quartiles_by_rank":
            prefix, steps, answer = self._quartiles()
        else:
            prefix, steps, answer = self._between()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_percentile_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

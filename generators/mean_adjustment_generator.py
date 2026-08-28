"""Update means exactly when data or group membership changes.

Variants: ``needed_score``, ``add_value``, ``remove_value``,
``combined_groups``, ``correction``, and ``outlier_effect``. Op-codes:
``STAT_SETUP``, ``SORT``, ``MEDIAN_PICK``, ``MEDIAN_PAIR``, ``M``, ``A``,
``S``, ``D``, ``CHECK``, and ``Z``. Totals are reconstructed from a stated
mean and count; target-score, removal, and combined-group cases are built
backward for exact answers; correction denominators terminate; outlier data
are symmetric and use an offset divisible by six. Random counts, means,
contexts, settings, values, directions, and four phrasings give unbounded
capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import CONTEXTS, num_txt, running_sum_steps


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
QUERIES = {
    "needed_score": (
        "What value is needed next to reach the target mean?",
        "Find the next observation required for the stated new average.",
        "How large must the additional value be to obtain the target mean?",
        "Use total points to solve for the needed next value.",
    ),
    "add_value": (
        "Find the new mean after the value is added.",
        "Update the total and count to compute the resulting average.",
        "What mean results from including the additional observation?",
        "Recalculate the exact mean with the new value included.",
    ),
    "remove_value": (
        "Find the new mean after the value is removed.",
        "Subtract the observation and update the count before averaging.",
        "What exact average remains after deleting the stated value?",
        "Recalculate the mean without the removed observation.",
    ),
    "combined_groups": (
        "Find the combined mean of the two groups.",
        "Use both group totals and counts to compute the overall average.",
        "What mean do the groups have when pooled?",
        "Calculate the exact weighted average across both groups.",
    ),
    "correction": (
        "Find the corrected mean.",
        "Replace the misrecorded value and recompute the exact average.",
        "How does correcting the data entry change the reported mean?",
        "Recover the old total, fix it, and calculate the true mean.",
    ),
    "outlier_effect": (
        "Report the mean and median before and after adding the outlier.",
        "Compare both centers before and after the extreme value is included.",
        "How do the exact mean and median change when the outlier is added?",
        "Compute the before-and-after mean and median as a composite answer.",
    ),
}


def _context():
    return random.choice(CONTEXTS)


class MeanAdjustmentGenerator(ProblemGenerator):
    """Generate exact mean-update and outlier-effect exercises."""

    VARIANTS = ("needed_score", "add_value", "remove_value",
                "combined_groups", "correction", "outlier_effect")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _needed_score():
        while True:
            count = random.randint(3, 8)
            old_mean = random.randint(35, 85)
            target = old_mean + random.randint(-5, 7)
            needed = target * (count + 1) - old_mean * count
            if 1 <= needed <= 100 and target != old_mean:
                break
        prefix = (f"At the {random.choice(SETTINGS)}, {count} test scores "
                  f"have mean {old_mean}. The target mean after one more "
                  f"value is {target}.")
        target_total, old_total = target * (count + 1), old_mean * count
        steps = [
            step("STAT_SETUP", "test-score mean update", f"n={count}"),
            step("M", target, count + 1, target_total),
            step("M", old_mean, count, old_total),
            step("S", target_total, old_total, needed),
            step("CHECK", "substitute",
                 f"({old_total} + {needed})/{count + 1}", target),
        ]
        return prefix, steps, str(needed)

    @staticmethod
    def _add_value():
        ctx = _context()
        count = random.choice((3, 4, 7, 9))
        old_mean = random.randint(ctx.lo, ctx.hi)
        added = random.randint(ctx.lo, ctx.hi)
        old_total = old_mean * count
        new_total, new_count = old_total + added, count + 1
        mean = Fraction(new_total, new_count)
        prefix = (f"At the {random.choice(SETTINGS)}, {count} {ctx.label} "
                  f"have mean {old_mean}. Add the value {added}.")
        steps = [
            step("STAT_SETUP", f"add to {ctx.label}", f"n={count}"),
            step("M", old_mean, count, old_total),
            step("A", old_total, added, new_total),
            step("A", count, 1, new_count),
            step("D", new_total, new_count, num_txt(mean)),
            step("CHECK", "updated total and count",
                 f"{new_total}/{new_count}", num_txt(mean)),
        ]
        return prefix, steps, num_txt(mean)

    @staticmethod
    def _remove_value():
        ctx = _context()
        while True:
            count = random.choice((5, 6, 9, 11))
            old_mean = random.randint(ctx.lo, ctx.hi)
            new_mean = random.randint(ctx.lo, ctx.hi)
            removed = old_mean * count - new_mean * (count - 1)
            if ctx.lo <= removed <= ctx.hi and new_mean != old_mean:
                break
        old_total, new_total = old_mean * count, new_mean * (count - 1)
        prefix = (f"At the {random.choice(SETTINGS)}, {count} {ctx.label} "
                  f"have mean {old_mean}. Remove the value {removed}.")
        steps = [
            step("STAT_SETUP", f"remove from {ctx.label}", f"n={count}"),
            step("M", old_mean, count, old_total),
            step("S", old_total, removed, new_total),
            step("S", count, 1, count - 1),
            step("D", new_total, count - 1, new_mean),
            step("CHECK", "remaining mean",
                 f"{new_total}/{count - 1}", new_mean),
        ]
        return prefix, steps, str(new_mean)

    @staticmethod
    def _combined_groups():
        ctx = _context()
        counts = random.choice(((10, 10), (20, 20), (25, 25), (30, 30),
                                (10, 30), (15, 45), (20, 40), (25, 50)))
        while True:
            target = random.randint(ctx.lo, ctx.hi)
            first_mean = random.randint(ctx.lo, ctx.hi)
            numerator = target * sum(counts) - counts[0] * first_mean
            if numerator % counts[1]:
                continue
            second_mean = numerator // counts[1]
            if ctx.lo <= second_mean <= ctx.hi and second_mean != first_mean:
                break
        prefix = (f"Two groups of {ctx.label}: Group A has {counts[0]} values "
                  f"with mean {first_mean}; Group B has {counts[1]} values "
                  f"with mean {second_mean}.")
        totals = [counts[0] * first_mean, counts[1] * second_mean]
        grand_total, grand_count = sum(totals), sum(counts)
        steps = [
            step("STAT_SETUP", f"combine {ctx.label}", "groups A and B"),
            step("M", counts[0], first_mean, totals[0]),
            step("M", counts[1], second_mean, totals[1]),
            step("A", totals[0], totals[1], grand_total),
            step("A", counts[0], counts[1], grand_count),
            step("D", grand_total, grand_count, target),
            step("CHECK", "combined mean", f"{grand_total}/{grand_count}",
                 target),
        ]
        return prefix, steps, str(target)

    @staticmethod
    def _correction():
        ctx = _context()
        while True:
            count = random.choice((4, 5, 8, 10))
            reported_mean = random.randint(ctx.lo, ctx.hi)
            wrong = random.randint(ctx.lo, ctx.hi)
            correct = random.randint(ctx.lo, ctx.hi)
            reported_total = reported_mean * count
            corrected_total = reported_total - wrong + correct
            mean = Fraction(corrected_total, count)
            if correct != wrong and ctx.lo <= mean <= ctx.hi:
                break
        prefix = (f"The reported mean of {count} {ctx.label} was "
                  f"{reported_mean}, but {wrong} was recorded instead of "
                  f"{correct}.")
        steps = [
            step("STAT_SETUP", f"correct {ctx.label}", f"n={count}"),
            step("M", reported_mean, count, reported_total),
            step("S", reported_total, wrong, reported_total - wrong),
            step("A", reported_total - wrong, correct, corrected_total),
            step("D", corrected_total, count, num_txt(mean)),
            step("CHECK", "corrected total",
                 f"{reported_total} - {wrong} + {correct}", corrected_total),
        ]
        return prefix, steps, num_txt(mean)

    @staticmethod
    def _outlier_effect():
        direction = random.choice(("low", "high"))
        while True:
            center = random.randint(25, 75)
            gap = random.choice((2, 4, 6))
            multiple = random.choice((6, 9, 12))
            outlier = center + (multiple * gap if direction == "high"
                                else -multiple * gap)
            if 1 <= outlier <= 120:
                break
        data = [center - 2 * gap, center - gap, center,
                center + gap, center + 2 * gap]
        shuffled = list(data)
        random.shuffle(shuffled)
        expanded = sorted(data + [outlier])
        old_mean = Fraction(sum(data), len(data))
        new_mean = Fraction(sum(data) + outlier, len(data) + 1)
        old_median = Fraction(center)
        new_median = Fraction(expanded[2] + expanded[3], 2)
        prefix = (f"Data values: {', '.join(map(str, shuffled))}. Add the "
                  f"{direction} outlier {outlier}.")
        steps = [step("STAT_SETUP", "outlier effect", direction),
                 step("SORT", ",".join(map(str, sorted(data))))]
        additions, old_total = running_sum_steps(data)
        steps.extend(additions)
        steps.extend([step("D", old_total, len(data), num_txt(old_mean)),
                      step("MEDIAN_PICK", "position 3", old_median),
                      step("SORT", ",".join(map(str, expanded)))])
        steps.append(step("A", old_total, outlier, old_total + outlier))
        steps.append(step("D", old_total + outlier, len(expanded),
                          num_txt(new_mean)))
        steps.extend([
            step("MEDIAN_PAIR", expanded[2], expanded[3]),
            step("A", expanded[2], expanded[3], expanded[2] + expanded[3]),
            step("D", expanded[2] + expanded[3], 2, num_txt(new_median)),
            step("CHECK", "centers before and after",
                 f"mean {num_txt(old_mean)} to {num_txt(new_mean)}",
                 f"median {num_txt(old_median)} to {num_txt(new_median)}"),
        ])
        answer = (f"mean {num_txt(old_mean)} → {num_txt(new_mean)}; median "
                  f"{num_txt(old_median)} → {num_txt(new_median)}")
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {
            "needed_score": self._needed_score,
            "add_value": self._add_value,
            "remove_value": self._remove_value,
            "combined_groups": self._combined_groups,
            "correction": self._correction,
            "outlier_effect": self._outlier_effect,
        }
        prefix, steps, answer = methods[variant]()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_mean_adjustment_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

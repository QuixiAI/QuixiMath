"""Apply the 68-95-99.7 empirical rule with exact arithmetic.

Variants: ``percent_within``, ``percent_tail``, ``interval_for_percent``,
``count_of_n``, and ``percent_between_asymmetric``. Every problem supplies
the three empirical-rule constants. Cutoffs are exactly ``μ ± kσ`` for
``k`` in 1, 2, 3, and population sizes are filtered so requested counts are
integers. Random models, contexts, sites, regions, sizes, and four phrasings
give unbounded capacity. Op-codes: ``NORM_SETUP``, ``RULE_68_95``,
``ZSCORE``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import num_txt


STATISTICS = True
WITHIN = {1: Fraction(68), 2: Fraction(95), 3: Fraction(997, 10)}
HALF_FROM_MEAN = {k: (value / 2) for k, value in WITHIN.items()}
SIZES = (200, 400, 1000, 2000, 4000)
CONTEXTS = (
    "quiz scores", "plant heights", "commute minutes", "battery hours",
    "package weights", "daily sales", "rainfall measurements", "ages",
    "reading times", "points per game",
)
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
QUERIES = {
    "percent_within": (
        "Find the percent in the target region.",
        "Use the empirical rule to report the requested central percentage.",
        "What percent of observations lie within these symmetric cutoffs?",
        "Identify the supplied within-k-sigma percentage.",
    ),
    "percent_tail": (
        "Find the percent in the target tail.",
        "Use symmetry and the empirical rule to calculate this one-sided percent.",
        "What percentage lies beyond the stated cutoff?",
        "Subtract the central percentage and split the two tails.",
    ),
    "interval_for_percent": (
        "Find the interval containing the target percent.",
        "Use μ ± kσ to report the requested central interval.",
        "What symmetric numeric interval corresponds to this percentage?",
        "Calculate both empirical-rule cutoffs for the target coverage.",
    ),
    "count_of_n": (
        "Find the number of observations in the target region.",
        "Convert the empirical-rule percent to an exact count.",
        "How many members of the stated population fall in this region?",
        "Multiply the region's proportion by N and report the count.",
    ),
    "percent_between_asymmetric": (
        "Find the percent between the two asymmetric cutoffs.",
        "Add the empirical-rule portions on the two sides of the mean.",
        "What percentage lies in this unequal interval around μ?",
        "Use the supplied constants to calculate the asymmetric coverage.",
    ),
}


def _site():
    return f"{random.choice(LOCATIONS)} during the {random.choice(SETTINGS)}"


def _model():
    sigma = random.randint(2, 20)
    mean = random.randint(4 * sigma, 10 * sigma)
    context = random.choice(CONTEXTS)
    prefix = (f"At the {_site()}, {context} follow model X ~ N({mean}, "
              f"{sigma}), where the second number is the standard deviation. "
              f"Use empirical-rule constants: 68% within 1σ, 95% within "
              f"2σ, and 99.7% within 3σ.")
    return mean, sigma, context, prefix


def _percent_text(value):
    return f"{num_txt(value)}%"


def _tail_percent(k):
    return (Fraction(100) - WITHIN[k]) / 2


class EmpiricalRuleGenerator(ProblemGenerator):
    """Generate exact empirical-rule percentages, intervals, and counts."""

    VARIANTS = ("percent_within", "percent_tail", "interval_for_percent",
                "count_of_n", "percent_between_asymmetric")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _within(mean, sigma):
        k = random.randint(1, 3)
        offset = k * sigma
        low, high = mean - offset, mean + offset
        percent = WITHIN[k]
        extra = (f"Target region: from {low} to {high}, inclusive under the "
                 f"continuous model; these are μ − {k}σ and μ + {k}σ.")
        steps = [step("NORM_SETUP", f"X ~ N({mean}, {sigma})",
                      f"within {k}σ"),
                 step("ZSCORE", f"({low} - {mean})/{sigma}", -k),
                 step("ZSCORE", f"({high} - {mean})/{sigma}", k),
                 step("RULE_68_95", f"within {k}σ", _percent_text(percent)),
                 step("CHECK", "symmetric empirical region",
                      f"({low}, {high})", _percent_text(percent))]
        return extra, steps, _percent_text(percent)

    @staticmethod
    def _tail(mean, sigma):
        k = random.randint(1, 3)
        side = random.choice(("above", "below"))
        cutoff = mean + k * sigma if side == "above" else mean - k * sigma
        within = WITHIN[k]
        outside = Fraction(100) - within
        tail = outside / 2
        extra = f"Target region: {side} {cutoff}, which is {side} μ {'+' if side == 'above' else '−'} {k}σ."
        steps = [step("NORM_SETUP", f"X ~ N({mean}, {sigma})",
                      f"{side} {cutoff}"),
                 step("ZSCORE", f"({cutoff} - {mean})/{sigma}",
                      k if side == "above" else -k),
                 step("RULE_68_95", f"within {k}σ", _percent_text(within)),
                 step("S", 100, num_txt(within), num_txt(outside)),
                 step("D", num_txt(outside), 2, num_txt(tail)),
                 step("CHECK", "one symmetric tail", side,
                      _percent_text(tail))]
        return extra, steps, _percent_text(tail)

    @staticmethod
    def _interval(mean, sigma):
        k = random.randint(1, 3)
        percent = WITHIN[k]
        offset = k * sigma
        low, high = mean - offset, mean + offset
        extra = f"Target central percent: {_percent_text(percent)}."
        steps = [step("NORM_SETUP", f"X ~ N({mean}, {sigma})",
                      f"central {_percent_text(percent)}"),
                 step("RULE_68_95", _percent_text(percent), f"within {k}σ"),
                 step("M", k, sigma, offset),
                 step("S", mean, offset, low),
                 step("A", mean, offset, high),
                 step("CHECK", "central interval", f"μ ± {k}σ",
                      f"({low}, {high})")]
        return extra, steps, f"({low}, {high})"

    @staticmethod
    def _count(mean, sigma):
        while True:
            k = random.randint(1, 3)
            region = random.choice(("within", "above", "below"))
            percent = WITHIN[k] if region == "within" else _tail_percent(k)
            valid_sizes = [size for size in SIZES
                           if (Fraction(size) * percent / 100).denominator == 1]
            if valid_sizes:
                break
        size = random.choice(valid_sizes)
        count = int(Fraction(size) * percent / 100)
        if region == "within":
            low, high = mean - k * sigma, mean + k * sigma
            description = f"from {low} to {high} (within {k}σ)"
            z_steps = [step("ZSCORE", f"({low} - {mean})/{sigma}", -k),
                       step("ZSCORE", f"({high} - {mean})/{sigma}", k)]
        else:
            cutoff = mean + k * sigma if region == "above" else mean - k * sigma
            description = f"{region} {cutoff} ({region} μ {'+' if region == 'above' else '−'} {k}σ)"
            z_steps = [step("ZSCORE", f"({cutoff} - {mean})/{sigma}",
                            k if region == "above" else -k)]
        extra = f"Population size N = {size}. Target region: {description}."
        steps = [step("NORM_SETUP", f"X ~ N({mean}, {sigma})", description),
                 *z_steps]
        if region == "within":
            steps.append(step("RULE_68_95", f"within {k}σ",
                              _percent_text(percent)))
        else:
            within = WITHIN[k]
            outside = 100 - within
            steps.extend([step("RULE_68_95", f"within {k}σ",
                               _percent_text(within)),
                          step("S", 100, num_txt(within), num_txt(outside)),
                          step("D", num_txt(outside), 2, num_txt(percent))])
        proportion = percent / 100
        steps.extend([step("M", num_txt(proportion), size, count),
                      step("CHECK", "empirical-rule count",
                           _percent_text(percent), count)])
        return extra, steps, str(count)

    @staticmethod
    def _asymmetric(mean, sigma):
        left_k, right_k = random.choice(
            [(a, b) for a in (1, 2, 3) for b in (1, 2, 3) if a != b])
        low, high = mean - left_k * sigma, mean + right_k * sigma
        left = HALF_FROM_MEAN[left_k]
        right = HALF_FROM_MEAN[right_k]
        percent = left + right
        extra = (f"Target region: from {low} = μ − {left_k}σ to {high} = "
                 f"μ + {right_k}σ.")
        steps = [step("NORM_SETUP", f"X ~ N({mean}, {sigma})",
                      f"{low} to {high}"),
                 step("ZSCORE", f"({low} - {mean})/{sigma}", -left_k),
                 step("ZSCORE", f"({high} - {mean})/{sigma}", right_k),
                 step("RULE_68_95", f"within {left_k}σ",
                      _percent_text(WITHIN[left_k])),
                 step("D", num_txt(WITHIN[left_k]), 2, num_txt(left)),
                 step("RULE_68_95", f"within {right_k}σ",
                      _percent_text(WITHIN[right_k])),
                 step("D", num_txt(WITHIN[right_k]), 2, num_txt(right)),
                 step("A", num_txt(left), num_txt(right), num_txt(percent)),
                 step("CHECK", "asymmetric central pieces",
                      f"{_percent_text(left)} + {_percent_text(right)}",
                      _percent_text(percent))]
        return extra, steps, _percent_text(percent)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        mean, sigma, _, prefix = _model()
        if variant == "percent_within":
            extra, steps, answer = self._within(mean, sigma)
        elif variant == "percent_tail":
            extra, steps, answer = self._tail(mean, sigma)
        elif variant == "interval_for_percent":
            extra, steps, answer = self._interval(mean, sigma)
        elif variant == "count_of_n":
            extra, steps, answer = self._count(mean, sigma)
        else:
            extra, steps, answer = self._asymmetric(mean, sigma)
        problem = f"{prefix}\n{extra}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_empirical_rule_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

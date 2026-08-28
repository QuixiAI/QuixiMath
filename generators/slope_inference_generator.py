"""Exact simple-regression slope inference with supplied t critical values.

Variants: ``se_slope``, ``t_stat``, ``ci_slope``, ``decision``,
``from_output``, and ``sxx_from_data``. Sxx is a perfect square, so
``SE_b = s/√Sxx`` is exact; raw-x cases use zero-sum patterns with square
Sxx. Op-codes: ``REG_SETUP``, ``SE_FORMULA``, ``TEST_STAT_FORMULA``,
``LOOKUP_SUPPLIED``, ``ROOT``, ``SUM``, ``MEAN_DIV``, ``DEV_ROW``, ``M``,
``D``, ``S``, ``A``, ``REWRITE``, ``CHECK``, and ``Z``.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact


STATISTICS = True
SXX_BANK = (16, 25, 36, 64, 100, 144)
RESIDUAL_SD_BANK = (1, 2, 4, 5, 8, 10, 12, 20)
T_CRITICAL = {
    4: "2.776", 6: "2.447", 8: "2.306",
    10: "2.228", 14: "2.145", 18: "2.101",
}
RAW_X_PATTERNS = (
    ((-2, -2, 2, 2), 16),
    ((-3, -3, 0, 3, 3), 36),
    ((-4, -1, -1, 1, 1, 4), 36),
    ((-8, -2, -2, 2, 2, 8), 144),
)
VENUES = (
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
    "se_slope": (
        "Find the standard error of the slope.",
        "Compute SE_b from s and Sxx.",
        "Use the residual SD to obtain the slope uncertainty.",
        "Report s divided by the square root of Sxx.",
    ),
    "t_stat": (
        "Find the t statistic for H0: β = 0.",
        "Standardize the estimated slope under the zero-slope null.",
        "Compute b/SE_b.",
        "Report the exact slope test statistic.",
    ),
    "ci_slope": (
        "Find the 95% confidence interval for the population slope.",
        "Use the supplied t* to construct the slope interval.",
        "Compute b ± t*·SE_b.",
        "Report the exact confidence interval for β.",
    ),
    "decision": (
        "Test H0: β = 0 against Ha: β ≠ 0.",
        "Compare abs(t) with the supplied critical value.",
        "State the checkable two-sided slope-test conclusion.",
        "Decide whether the linear slope is statistically nonzero.",
    ),
    "from_output": (
        "Read the slope row and compute its t statistic.",
        "Use Coef divided by SE Coef.",
        "Standardize the slope shown in the computer output.",
        "Find t for the predictor coefficient.",
    ),
    "sxx_from_data": (
        "Compute Sxx = Σ(x − x̄)^2 from the raw x-values.",
        "Find the centered sum of squares for x.",
        "Use the x deviations to obtain Sxx.",
        "Report the predictor sum of squares.",
    ),
}


def _site():
    code = f"sample {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _slope():
    return Fraction(random.choice([value for value in range(-32, 33)
                                   if value]), 4)


def _summary_case():
    n = random.choice(tuple(df + 2 for df in T_CRITICAL))
    sxx = random.choice(SXX_BANK)
    residual_sd = random.choice(RESIDUAL_SD_BANK)
    se = Fraction(residual_sd, math.isqrt(sxx))
    slope = _slope()
    df = n - 2
    return n, slope, residual_sd, sxx, se, df, T_CRITICAL[df]


def _summary_steps(slope, residual_sd, sxx, se):
    root = math.isqrt(sxx)
    return [
        step("REG_SETUP", f"b = {exact(slope)}, s = {residual_sd}, Sxx = {sxx}",
             "inference for β"),
        step("SE_FORMULA", "SE_b = s/√Sxx"),
        step("ROOT", sxx, 2, root),
        step("D", residual_sd, root, exact(se)),
    ]


class SlopeInferenceGenerator(ProblemGenerator):
    """Generate exact slope SE, t, CI, decision, output, and Sxx cases.

    Perfect-square Sxx values make every slope SE exact. Variants are
    ``se_slope``, ``t_stat``, ``ci_slope``, ``decision``, ``from_output``,
    and ``sxx_from_data``. Op-codes are ``REG_SETUP``, ``SE_FORMULA``,
    ``TEST_STAT_FORMULA``, ``LOOKUP_SUPPLIED``, ``ROOT``, ``SUM``,
    ``MEAN_DIV``, ``DEV_ROW``, ``M``, ``D``, ``S``, ``A``, ``REWRITE``,
    ``CHECK``, and ``Z``.
    """

    VARIANTS = tuple(QUERIES)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _result(variant, problem, steps, answer):
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_slope_inference_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _summary_variant(self, variant):
        n, slope, residual_sd, sxx, se, df, critical_text = _summary_case()
        steps = _summary_steps(slope, residual_sd, sxx, se)
        critical_clause = ""
        if variant == "se_slope":
            answer = exact(se)
        else:
            statistic = slope / se
            steps.extend([
                step("TEST_STAT_FORMULA", "t = (b − 0)/SE_b"),
                step("S", exact(slope), 0, exact(slope)),
                step("D", exact(slope), exact(se), exact(statistic)),
            ])
            if variant == "t_stat":
                answer = exact(statistic)
            elif variant == "ci_slope":
                critical = Fraction(critical_text)
                margin = critical * se
                lower, upper = slope - margin, slope + margin
                critical_clause = (f" Use t* = {critical_text} "
                                   f"(df = {df}).")
                steps.extend([
                    step("LOOKUP_SUPPLIED", f"t* (df = {df})", critical_text),
                    step("M", critical_text, exact(se), exact(margin)),
                    step("S", exact(slope), exact(margin), exact(lower)),
                    step("A", exact(slope), exact(margin), exact(upper)),
                    step("REWRITE", f"({exact(lower)}, {exact(upper)})"),
                ])
                answer = f"({exact(lower)}, {exact(upper)})"
            else:
                critical = Fraction(critical_text)
                reject = abs(statistic) > critical
                relation = ">" if reject else "≤"
                label = "reject H0" if reject else "fail to reject H0"
                critical_clause = (f" Use two-sided t critical value = "
                                   f"{critical_text} (df = {df}).")
                steps.extend([
                    step("LOOKUP_SUPPLIED", f"two-sided t critical (df = {df})",
                         critical_text),
                    step("CHECK", "abs(t) vs critical",
                         f"{exact(abs(statistic))} {relation} {critical_text}",
                         label),
                ])
                answer = (f"{label} ({exact(abs(statistic))} {relation} "
                          f"{critical_text})")
        problem = (f"At the {_site()}, a simple regression on n = {n} points "
                   f"gives slope b = {exact(slope)}, residual sd s = "
                   f"{residual_sd}, and Sxx = {sxx}.{critical_clause}\n"
                   f"{random.choice(QUERIES[variant])}")
        return self._result(variant, problem, steps, answer)

    def _from_output(self):
        _, slope, _, _, se, _, _ = _summary_case()
        statistic = slope / se
        output = ("Computer output:\n"
                  "Predictor  Coef  SE Coef\n"
                  f"x          {exact(slope)}     {exact(se)}")
        problem = (f"At the {_site()}, a regression program prints:\n{output}\n"
                   f"{random.choice(QUERIES['from_output'])}")
        steps = [
            step("REG_SETUP", "read predictor x row",
                 f"b = {exact(slope)}, SE_b = {exact(se)}"),
            step("TEST_STAT_FORMULA", "t = b/SE_b"),
            step("D", exact(slope), exact(se), exact(statistic)),
        ]
        return self._result("from_output", problem, steps, exact(statistic))

    def _sxx_from_data(self):
        deviations, sxx = random.choice(RAW_X_PATTERNS)
        mean = random.randint(10, 100)
        values = [mean + deviation for deviation in deviations]
        random.shuffle(values)
        total = sum(values)
        problem = (f"At the {_site()}, predictor values are x = "
                   f"{', '.join(map(str, values))}.\n"
                   f"{random.choice(QUERIES['sxx_from_data'])}")
        steps = [
            step("REG_SETUP", f"x = {', '.join(map(str, values))}", "find Sxx"),
            step("SUM", " + ".join(map(str, values)), total),
            step("MEAN_DIV", total, len(values), mean),
        ]
        for value in values:
            deviation = value - mean
            steps.append(step("DEV_ROW", value, deviation, deviation * deviation))
        squares = [(value - mean) ** 2 for value in values]
        steps.append(step("SUM", " + ".join(
            str(square) for square in squares if square), sxx))
        return self._result("sxx_from_data", problem, steps, str(sxx))

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("se_slope", "t_stat", "ci_slope", "decision"):
            return self._summary_variant(variant)
        if variant == "from_output":
            return self._from_output()
        return self._sxx_from_data()

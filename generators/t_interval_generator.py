"""One-sample, paired, and pooled t procedures with exact arithmetic.

Variants: ``mean_t_ci``, ``mean_t_margin``, ``paired_from_data``,
``paired_from_summary``, ``paired_t_stat``, ``pooled_t_stat``, and
``pooled_t_ci``. Square sample sizes make every standard error rational;
raw paired differences use sample-square deviation patterns, and pooled
cases use ``POOLED_S_PAIRS``. Every t* used is printed with its df. Op-codes:
``CI_SETUP``, ``HT_SETUP``, ``PAIR_DIFF``, ``DEV_ROW``, ``SE_FORMULA``,
``MOE_FORMULA``, ``CI_FORMULA``, ``TEST_STAT_FORMULA``,
``LOOKUP_SUPPLIED``, ``ROOT``, ``A``, ``S``, ``M``, ``D``, ``E``,
``REWRITE``, ``CHECK``, and ``Z``.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import POOLED_S_PAIRS, num_txt, patterns


STATISTICS = True
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
T_STARS = {
    3: {90: Fraction("2.353"), 95: Fraction("3.182"), 99: Fraction("5.841")},
    8: {90: Fraction("1.860"), 95: Fraction("2.306"), 99: Fraction("3.355")},
    14: {90: Fraction("1.761"), 95: Fraction("2.145"), 99: Fraction("2.977")},
    15: {90: Fraction("1.753"), 95: Fraction("2.131"), 99: Fraction("2.947")},
    24: {90: Fraction("1.711"), 95: Fraction("2.064"), 99: Fraction("2.797")},
    99: {90: Fraction("1.660"), 95: Fraction("1.984"), 99: Fraction("2.626")},
}
SQUARE_N = (4, 9, 16, 25, 100)
QUERIES = {
    "mean_t_ci": (
        "Find the confidence interval for μ.",
        "Compute x̄ ± t*·s/√n.",
        "Use the supplied t* to report the mean interval.",
        "Give the exact one-sample t confidence interval.",
    ),
    "mean_t_margin": (
        "Find the margin of error.",
        "Compute t*·s/√n.",
        "What is the exact one-sample t margin?",
        "Use the supplied t* to report E.",
    ),
    "paired_from_data": (
        "Use the paired data to find the confidence interval for μd.",
        "Compute every after-minus-before difference, then form the t interval.",
        "Find the paired t confidence interval from the raw observations.",
        "Reduce the pairs to differences and report d̄ ± t*·sd/√n.",
    ),
    "paired_from_summary": (
        "Find the paired-difference confidence interval for μd.",
        "Compute d̄ ± t*·sd/√n from the summary.",
        "Use the supplied paired summary to report the t interval.",
        "Give the exact confidence interval for the mean difference.",
    ),
    "paired_t_stat": (
        "Find the paired t statistic.",
        "Standardize d̄ under H0: μd = 0.",
        "Compute t = d̄/(sd/√n).",
        "Report the exact test statistic from the paired summary.",
    ),
    "pooled_t_stat": (
        "Compute the pooled t statistic and make the supplied-critical-value decision.",
        "Find sp, standardize x̄1 − x̄2, and decide the two-sided test.",
        "Use equal variances to give a composite pooled-test verdict.",
        "Compare abs(t) with the printed t critical value.",
    ),
    "pooled_t_ci": (
        "Find the pooled confidence interval for μ1 − μ2.",
        "Compute (x̄1 − x̄2) ± t*·sp√(1/n1 + 1/n2).",
        "Use equal variances and the supplied t* to report the interval.",
        "Find the exact pooled two-sample t confidence interval.",
    ),
}


def _site():
    code = f"trial {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _critical(df):
    confidence = random.choice(tuple(T_STARS[df]))
    return confidence, T_STARS[df][confidence]


def _t_text(value):
    return f"{float(value):.3f}"


def _one_sample_summary():
    n = random.choice(SQUARE_N)
    root_n = math.isqrt(n)
    assert root_n * root_n == n
    se = random.randint(1, 6)
    sample_sd = se * root_n
    mean = random.randint(3 * sample_sd, 3 * sample_sd + 300)
    return n, root_n, mean, sample_sd, Fraction(se)


def _se_steps(sample_sd, n, root_n, se, symbol="s"):
    return [step("SE_FORMULA", f"SE = {symbol}/√n"),
            step("ROOT", n, 2, root_n),
            step("D", num_txt(sample_sd), root_n, num_txt(se))]


def _interval_steps(center, se, t_star):
    margin = t_star * se
    lower, upper = center - margin, center + margin
    return ([step("LOOKUP_SUPPLIED", "t*", _t_text(t_star)),
             step("MOE_FORMULA", "E = t*·SE"),
             step("M", num_txt(t_star), num_txt(se), num_txt(margin)),
             step("CI_FORMULA", "estimate ± E"),
             step("S", num_txt(center), num_txt(margin), num_txt(lower)),
             step("A", num_txt(center), num_txt(margin), num_txt(upper)),
             step("REWRITE", f"({num_txt(lower)}, {num_txt(upper)})")],
            margin, lower, upper)


def _paired_summary():
    n = random.choice(SQUARE_N)
    root_n = math.isqrt(n)
    se = random.randint(1, 5)
    sample_sd = se * root_n
    mean_difference = random.choice([value for value in range(-20, 21)
                                     if value])
    return n, root_n, Fraction(mean_difference), Fraction(sample_sd), Fraction(se)


def _pooled_base():
    n = 8
    s1, s2, pooled_sd = random.choice(POOLED_S_PAIRS)
    mean1 = random.randint(40, 180)
    difference = random.choice([value for value in range(-24, 25) if value])
    mean2 = mean1 - difference
    return n, Fraction(mean1), Fraction(mean2), s1, s2, Fraction(pooled_sd)


def _pooled_steps(n, mean1, mean2, s1, s2, pooled_sd):
    df_each = n - 1
    weighted1 = df_each * s1 * s1
    weighted2 = df_each * s2 * s2
    pooled_ss = weighted1 + weighted2
    df = 2 * n - 2
    pooled_variance = Fraction(pooled_ss, df)
    reciprocal_sum = Fraction(1, n) + Fraction(1, n)
    reciprocal_root = Fraction(1, 2)
    se = pooled_sd * reciprocal_root
    difference = mean1 - mean2
    steps = [
        step("E", s1, 2, s1 * s1),
        step("M", df_each, s1 * s1, weighted1),
        step("E", s2, 2, s2 * s2),
        step("M", df_each, s2 * s2, weighted2),
        step("A", weighted1, weighted2, pooled_ss),
        step("A", df_each, df_each, df),
        step("D", pooled_ss, df, num_txt(pooled_variance)),
        step("ROOT", num_txt(pooled_variance), 2, num_txt(pooled_sd)),
        step("D", 1, n, num_txt(Fraction(1, n))),
        step("A", num_txt(Fraction(1, n)), num_txt(Fraction(1, n)),
             num_txt(reciprocal_sum)),
        step("ROOT", num_txt(reciprocal_sum), 2, num_txt(reciprocal_root)),
        step("M", num_txt(pooled_sd), num_txt(reciprocal_root), num_txt(se)),
        step("S", num_txt(mean1), num_txt(mean2), num_txt(difference)),
    ]
    return steps, df, se, difference


class TIntervalGenerator(ProblemGenerator):
    """Generate exact t intervals and paired/pooled t procedures."""

    VARIANTS = ("mean_t_ci", "mean_t_margin", "paired_from_data",
                "paired_from_summary", "paired_t_stat", "pooled_t_stat",
                "pooled_t_ci")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _mean(variant):
        n, root_n, mean, sample_sd, se = _one_sample_summary()
        confidence, t_star = _critical(n - 1)
        prefix = (f"At the {_site()}, a random sample has n = {n}, x̄ = {mean}, "
                  f"and sample s = {sample_sd}. For a {confidence}% procedure, "
                  f"use t* = {_t_text(t_star)} (df = {n - 1}).")
        steps = [step("CI_SETUP", f"x̄ = {mean}, s = {sample_sd}, n = {n}",
                      f"t* = {_t_text(t_star)} (df = {n - 1})")]
        steps.extend(_se_steps(sample_sd, n, root_n, se))
        if variant == "mean_t_margin":
            margin = t_star * se
            steps.extend([step("LOOKUP_SUPPLIED", f"t* (df = {n - 1})",
                               _t_text(t_star)),
                          step("MOE_FORMULA", "E = t*·s/√n"),
                          step("M", num_txt(t_star), num_txt(se), num_txt(margin))])
            answer = num_txt(margin)
        else:
            extra, _, lower, upper = _interval_steps(Fraction(mean), se, t_star)
            extra[0] = step("LOOKUP_SUPPLIED", f"t* (df = {n - 1})",
                            _t_text(t_star))
            steps.extend(extra)
            answer = f"({num_txt(lower)}, {num_txt(upper)})"
        return prefix, steps, answer

    @staticmethod
    def _paired_raw():
        n = random.choice((4, 16))
        if n == 4:
            pattern = random.choice(patterns(n, sample_square=True, max_abs=8))
        else:
            scale = random.choice((1, 2))
            pattern = tuple([-15 * scale] + [scale] * 15)
        mean_difference = random.randint(-12, 12)
        differences = [mean_difference + value for value in pattern]
        random.shuffle(differences)
        before = [random.randint(60, 140) for _ in range(n)]
        after = [base + difference for base, difference in zip(before, differences)]
        ss = sum((value - mean_difference) ** 2 for value in differences)
        variance = Fraction(ss, n - 1)
        root_sd = math.isqrt(variance.numerator)
        root_den = math.isqrt(variance.denominator)
        assert root_sd * root_sd == variance.numerator
        assert root_den * root_den == variance.denominator
        sample_sd = Fraction(root_sd, root_den)
        root_n = math.isqrt(n)
        se = sample_sd / root_n
        confidence, t_star = _critical(n - 1)
        prefix = (f"At the {_site()}, paired observations use d = after − before. "
                  f"before: {', '.join(map(str, before))}. after: "
                  f"{', '.join(map(str, after))}. For a {confidence}% interval, "
                  f"use t* = {_t_text(t_star)} (df = {n - 1}).")
        steps = [step("CI_SETUP", f"paired n = {n}, d = after − before",
                      f"t* = {_t_text(t_star)} (df = {n - 1})")]
        for after_value, before_value, difference in zip(after, before, differences):
            steps.append(step("PAIR_DIFF", after_value, before_value, difference))
        steps.append(step("SUM", ",".join(map(str, differences)), sum(differences)))
        steps.append(step("D", sum(differences), n, mean_difference))
        for difference in differences:
            deviation = difference - mean_difference
            steps.append(step("DEV_ROW", difference, deviation, deviation * deviation))
        steps.extend([step("SUM", "squared deviations", ss),
                      step("D", ss, n - 1, num_txt(variance)),
                      step("ROOT", num_txt(variance), 2, num_txt(sample_sd))])
        steps.extend(_se_steps(sample_sd, n, root_n, se, symbol="sd"))
        extra, _, lower, upper = _interval_steps(
            Fraction(mean_difference), se, t_star)
        extra[0] = step("LOOKUP_SUPPLIED", f"t* (df = {n - 1})", _t_text(t_star))
        steps.extend(extra)
        answer = f"({num_txt(lower)}, {num_txt(upper)})"
        return prefix, steps, answer

    @staticmethod
    def _paired_summary_variant(variant):
        n, root_n, mean_difference, sample_sd, se = _paired_summary()
        confidence, t_star = _critical(n - 1)
        prefix = (f"At the {_site()}, paired differences use d = after − before "
                  f"and have n = {n}, d̄ = {num_txt(mean_difference)}, and "
                  f"sample sd = {num_txt(sample_sd)}. For a {confidence}% "
                  f"procedure, use t* = {_t_text(t_star)} (df = {n - 1}).")
        setup_op = "HT_SETUP" if variant == "paired_t_stat" else "CI_SETUP"
        steps = [step(setup_op,
                      f"d̄ = {num_txt(mean_difference)}, sd = {num_txt(sample_sd)}, n = {n}",
                      ("H0: μd = 0" if variant == "paired_t_stat" else
                       f"t* = {_t_text(t_star)} (df = {n - 1})"))]
        steps.extend(_se_steps(sample_sd, n, root_n, se, symbol="sd"))
        if variant == "paired_t_stat":
            steps.extend([step("TEST_STAT_FORMULA", "t = (d̄ − 0)/(sd/√n)"),
                          step("S", num_txt(mean_difference), 0,
                               num_txt(mean_difference)),
                          step("D", num_txt(mean_difference), num_txt(se),
                               num_txt(mean_difference / se))])
            answer = num_txt(mean_difference / se)
        else:
            extra, _, lower, upper = _interval_steps(mean_difference, se, t_star)
            extra[0] = step("LOOKUP_SUPPLIED", f"t* (df = {n - 1})",
                            _t_text(t_star))
            steps.extend(extra)
            answer = f"({num_txt(lower)}, {num_txt(upper)})"
        return prefix, steps, answer

    @staticmethod
    def _pooled(variant):
        n, mean1, mean2, s1, s2, pooled_sd = _pooled_base()
        base_steps, df, se, difference = _pooled_steps(
            n, mean1, mean2, s1, s2, pooled_sd)
        confidence, t_star = _critical(df)
        prefix = (f"At the {_site()}, independent sample 1 has n1 = {n}, "
                  f"x̄1 = {num_txt(mean1)}, s1 = {s1}; sample 2 has n2 = {n}, "
                  f"x̄2 = {num_txt(mean2)}, s2 = {s2}. Assume equal variances. "
                  f"For the two-sided {confidence}% procedure, use t* = "
                  f"{_t_text(t_star)} (df = {df}).")
        setup_op = "HT_SETUP" if variant == "pooled_t_stat" else "CI_SETUP"
        steps = [step(setup_op,
                      f"n1 = n2 = {n}, x̄1 = {num_txt(mean1)}, x̄2 = {num_txt(mean2)}",
                      f"s1 = {s1}, s2 = {s2}, df = {df}")]
        steps.extend(base_steps)
        steps.append(step("LOOKUP_SUPPLIED", f"t* (df = {df})", _t_text(t_star)))
        if variant == "pooled_t_stat":
            statistic = difference / se
            steps.extend([step("TEST_STAT_FORMULA",
                               "t = (x̄1 − x̄2)/(sp√(1/n1 + 1/n2))"),
                          step("D", num_txt(difference), num_txt(se),
                               num_txt(statistic))])
            reject = abs(statistic) > t_star
            relation = ">" if reject else "≤"
            label = "reject H0" if reject else "fail to reject H0"
            comparison = (f"{num_txt(abs(statistic))} {relation} "
                          f"{_t_text(t_star)}")
            steps.append(step("CHECK", "abs(t) vs t*", comparison, label))
            answer = f"{label} ({comparison})"
        else:
            margin = t_star * se
            lower, upper = difference - margin, difference + margin
            steps.extend([step("MOE_FORMULA", "E = t*·pooled SE"),
                          step("M", num_txt(t_star), num_txt(se), num_txt(margin)),
                          step("CI_FORMULA", "(x̄1 − x̄2) ± E"),
                          step("S", num_txt(difference), num_txt(margin), num_txt(lower)),
                          step("A", num_txt(difference), num_txt(margin), num_txt(upper)),
                          step("REWRITE", f"({num_txt(lower)}, {num_txt(upper)})")])
            answer = f"({num_txt(lower)}, {num_txt(upper)})"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("mean_t_ci", "mean_t_margin"):
            prefix, steps, answer = self._mean(variant)
        elif variant == "paired_from_data":
            prefix, steps, answer = self._paired_raw()
        elif variant in ("paired_from_summary", "paired_t_stat"):
            prefix, steps, answer = self._paired_summary_variant(variant)
        else:
            prefix, steps, answer = self._pooled(variant)
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_t_interval_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

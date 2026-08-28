"""Exact one-way ANOVA from raw equal-size groups.

Variants: ``group_means``, ``ss_between``, ``ss_within``, ``anova_table``,
``f_stat``, ``f_decision``, and ``df_only``. Each group is an integer mean
plus a zero-sum deviation pattern, so group means and sums of squares are
exact. The F-statistic variants filter for integer MSW. Op-codes:
``ANOVA_SETUP``, ``ANOVA_ROW``, ``DEV_ROW``, ``SS_BETWEEN``, ``SS_WITHIN``,
``F_FORMULA``, ``SUM``, ``MEAN_DIV``, ``EVAL``, ``D``, ``CHECK``,
``LOOKUP_SUPPLIED``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact
from stats_common import text_list


STATISTICS = True
DEVIATION_PATTERNS = {
    3: ((-1, 0, 1), (-2, 0, 2), (-1, -1, 2), (-2, 1, 1)),
    4: ((-1, -1, 1, 1), (-2, 0, 0, 2),
        (-2, -1, 1, 2), (-3, -1, 1, 3)),
    5: ((-1, -1, 0, 1, 1), (-2, -1, 0, 1, 2),
        (-2, -2, 0, 2, 2), (-3, -1, 0, 1, 3)),
}
MEAN_OFFSETS = {
    3: ((-1, 0, 1), (-2, 0, 2), (-3, 0, 3),
        (-4, 1, 3), (-3, -1, 4)),
    4: ((-1, 0, 0, 1), (-3, -1, 1, 3),
        (-4, -2, 2, 4), (-3, -2, 2, 3), (-4, -1, 1, 4)),
}
F_CRITICAL = {
    (2, 6): "5.14", (2, 9): "4.26", (2, 12): "3.89",
    (3, 8): "4.07", (3, 12): "3.49", (3, 16): "3.24",
}
GROUP_LABELS = ("A", "B", "C", "D")
STUDIES = (
    "fertilizer-yield trial", "teaching-method study", "machine-output audit",
    "therapy-score experiment", "seed-growth trial", "training-time study",
    "battery-life experiment", "reaction-yield study", "crop-height trial",
    "service-time comparison", "material-strength test", "memory-score study",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
QUERIES = {
    "group_means": (
        "Find every group mean.", "Compute the mean for each treatment group.",
        "Report the group-means text list.", "Average each raw-data row.",
    ),
    "ss_between": (
        "Find the between-groups sum of squares SSB.",
        "Compute variation due to the group means.",
        "Use the grand mean to obtain SSB.",
        "Report the treatment sum of squares.",
    ),
    "ss_within": (
        "Find the within-groups sum of squares SSW.",
        "Add the squared deviations inside the groups.",
        "Compute the error sum of squares.",
        "Report the within-treatment variation.",
    ),
    "anova_table": (
        "Complete the one-way ANOVA summary.",
        "Report SSB, SSW, both df, both mean squares, and F.",
        "Build the exact ANOVA table as a text list.",
        "Compute every requested ANOVA-table entry.",
    ),
    "f_stat": (
        "Find the one-way ANOVA F statistic.",
        "Compute MSB/MSW.", "Report the exact F ratio.",
        "Use the sums of squares and df to obtain F.",
    ),
    "f_decision": (
        "Compute F and state the test conclusion.",
        "Compare F with the supplied critical value.",
        "Decide whether to reject equal population means.",
        "Give the checkable ANOVA verdict.",
    ),
    "df_only": (
        "Find the between- and within-groups degrees of freedom.",
        "Report df for treatments and error.",
        "Compute the two ANOVA degrees of freedom.",
        "Use k and N to obtain df.",
    ),
}


def _site():
    code = f"batch {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during a "
            f"{random.choice(STUDIES)} ({code})")


def _sum_expression(values):
    return " + ".join(map(str, values))


def _case(require_integer_msw=False):
    while True:
        k = random.choice((3, 4))
        n = random.choice((3, 4, 5))
        grand = random.randint(20, 100)
        scale = random.randint(1, 4)
        offsets = random.choice(MEAN_OFFSETS[k])
        means = [grand + scale * offset for offset in offsets]
        patterns = [random.choice(DEVIATION_PATTERNS[n]) for _ in range(k)]
        groups = [[mean + deviation for deviation in pattern]
                  for mean, pattern in zip(means, patterns)]
        if min(map(min, groups)) <= 0:
            continue
        within_ss = [sum(value * value for value in pattern)
                     for pattern in patterns]
        ssb = n * sum((mean - grand) ** 2 for mean in means)
        ssw = sum(within_ss)
        df_b, df_w = k - 1, k * n - k
        if require_integer_msw and ssw % df_w:
            continue
        msb, msw = Fraction(ssb, df_b), Fraction(ssw, df_w)
        f_value = msb / msw
        return {"k": k, "n": n, "grand": grand, "means": means,
                "patterns": patterns, "groups": groups,
                "within_ss": within_ss, "ssb": ssb, "ssw": ssw,
                "df_b": df_b, "df_w": df_w, "msb": msb,
                "msw": msw, "f": f_value}


class ANOVAGenerator(ProblemGenerator):
    """Generate exact one-way ANOVA summaries and critical-value decisions.

    Variants are ``group_means``, ``ss_between``, ``ss_within``,
    ``anova_table``, ``f_stat``, ``f_decision``, and ``df_only``. Equal-size
    raw groups use zero-sum deviation patterns. Op-codes are ``ANOVA_SETUP``,
    ``ANOVA_ROW``, ``DEV_ROW``, ``SS_BETWEEN``, ``SS_WITHIN``,
    ``F_FORMULA``, ``SUM``, ``MEAN_DIV``, ``EVAL``, ``D``, ``CHECK``,
    ``LOOKUP_SUPPLIED``, and ``Z``.
    """

    VARIANTS = tuple(QUERIES)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _steps(case):
        labels = GROUP_LABELS[:case["k"]]
        steps = [step("ANOVA_SETUP", f"k = {case['k']}, n = {case['n']}",
                      "one-way ANOVA; equal group sizes")]
        for label, group, mean, ss in zip(
                labels, case["groups"], case["means"], case["within_ss"]):
            total = sum(group)
            steps.append(step("SUM", _sum_expression(group), total))
            steps.append(step("MEAN_DIV", total, case["n"], mean))
            for value in group:
                deviation = value - mean
                steps.append(step("DEV_ROW", value, deviation,
                                  deviation * deviation))
            steps.append(step("ANOVA_ROW", label, f"mean {mean}", f"SS {ss}"))
        mean_total = sum(case["means"])
        steps.extend([
            step("SUM", _sum_expression(case["means"]), mean_total),
            step("MEAN_DIV", mean_total, case["k"], case["grand"]),
        ])
        between_expr = " + ".join(
            f"({mean} − {case['grand']})^2" for mean in case["means"])
        steps.append(step("SS_BETWEEN",
                          f"{case['n']}·({between_expr})", case["ssb"]))
        steps.append(step("SS_WITHIN", _sum_expression(case["within_ss"]),
                          case["ssw"]))
        sst = sum((value - case["grand"]) ** 2
                  for group in case["groups"] for value in group)
        steps.extend([
            step("CHECK", "SST",
                 f"SSB + SSW = {case['ssb'] + case['ssw']}",
                 f"Σ(y − ȳ)^2 = {sst}"),
            step("EVAL", "df", f"{case['df_b']}, {case['df_w']}"),
            step("D", case["ssb"], case["df_b"], exact(case["msb"])),
            step("D", case["ssw"], case["df_w"], exact(case["msw"])),
            step("F_FORMULA", "F = MSB/MSW"),
            step("D", exact(case["msb"]), exact(case["msw"]),
                 exact(case["f"])),
        ])
        return steps

    @staticmethod
    def _answer(variant, case, critical_text):
        labels = GROUP_LABELS[:case["k"]]
        if variant == "group_means":
            return text_list(zip(labels, case["means"]))
        if variant == "ss_between":
            return exact(case["ssb"])
        if variant == "ss_within":
            return exact(case["ssw"])
        if variant == "anova_table":
            return (f"SSB = {exact(case['ssb'])}; SSW = {exact(case['ssw'])}; "
                    f"df = {case['df_b']}, {case['df_w']}; "
                    f"MSB = {exact(case['msb'])}; MSW = {exact(case['msw'])}; "
                    f"F = {exact(case['f'])}")
        if variant == "f_stat":
            return exact(case["f"])
        if variant == "df_only":
            return f"df = {case['df_b']}, {case['df_w']}"
        critical = Fraction(critical_text)
        reject = case["f"] > critical
        relation = ">" if reject else "≤"
        label = "reject H0" if reject else "fail to reject H0"
        return (f"{label} ({exact(case['f'])} {relation} "
                f"{critical_text})")

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        case = _case(require_integer_msw=variant in ("f_stat", "f_decision"))
        critical_text = F_CRITICAL[(case["df_b"], case["df_w"])]
        labels = GROUP_LABELS[:case["k"]]
        group_text = "; ".join(
            f"{label}: {', '.join(map(str, group))}"
            for label, group in zip(labels, case["groups"])
        )
        problem = (f"At the {_site()}, equal-size groups give raw data "
                   f"[{group_text}]. Use α = 0.05 and F critical value = "
                   f"{critical_text} (df {case['df_b']}, {case['df_w']}).\n"
                   f"{random.choice(QUERIES[variant])}")
        steps = self._steps(case)
        if variant == "f_decision":
            steps.append(step("LOOKUP_SUPPLIED",
                              f"F critical (df {case['df_b']}, {case['df_w']})",
                              critical_text))
            answer = self._answer(variant, case, critical_text)
            label = answer.split(" (")[0]
            comparison = answer.split("(", 1)[1][:-1]
            steps.append(step("CHECK", "F vs critical", comparison, label))
        else:
            answer = self._answer(variant, case, critical_text)
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_anova_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

"""Compute z-test p-values from supplied standard-normal table excerpts.

Variants: ``right_tail``, ``left_tail``, ``two_sided``, ``decision_alpha``,
``from_prop_data``, ``from_mean_data``, and ``compare_alphas``. They accept a
test statistic directly, derive z from proportion or known-sigma mean data,
and make one- or two-alpha decisions. All arithmetic after the printed Φ
lookup is exact four-decimal table arithmetic; every excerpt contains the
needed row and exactly two decoys. Op-codes: ``HT_SETUP``,
``TEST_STAT_FORMULA``, ``PVALUE_RULE``, ``TABLE_LOOKUP``, ``REWRITE``,
``ROOT``, ``M``, ``D``, ``S``, ``CHECK``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import p4, phi, phi_table, prob_txt
from stats_common import num_txt


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
QUERIES = {
    "right_tail": (
        "Find the right-tail p-value.",
        "Use the supplied Φ row to compute the p-value.",
        "What upper-tail probability corresponds to the test statistic?",
        "Apply the right-tailed p-value rule.",
    ),
    "left_tail": (
        "Find the left-tail p-value.",
        "Use symmetry and the supplied Φ row to compute the p-value.",
        "What lower-tail probability corresponds to the test statistic?",
        "Apply the left-tailed p-value rule.",
    ),
    "two_sided": (
        "Find the two-sided p-value.",
        "Double the tail beyond abs(z) using the supplied Φ row.",
        "What two-tail probability corresponds to the test statistic?",
        "Apply the two-sided p-value rule.",
    ),
    "decision_alpha": (
        "Find the p-value and make the decision at the stated α.",
        "Compare the supplied-table p-value with α.",
        "Should H0 be rejected? Include the p-value comparison.",
        "Compute p, then give a composite test decision.",
    ),
    "from_prop_data": (
        "Compute z from the proportion data, then find the p-value.",
        "Standardize p̂ under H0 and apply the stated tail rule.",
        "Find the one-proportion z statistic's p-value.",
        "Use the sample count to obtain z and then p.",
    ),
    "from_mean_data": (
        "Compute z from the mean data, then find the p-value.",
        "Use the known population SD to standardize x̄ and find p.",
        "Find the known-σ mean z statistic's p-value.",
        "Obtain z from the sample summary and then apply the tail rule.",
    ),
    "compare_alphas": (
        "Compare the decisions at α = 0.05 and α = 0.01.",
        "State which of the two significance levels rejects H0.",
        "Use the p-value to decide separately at 0.05 and 0.01.",
        "Give the two-alpha composite verdict with p.",
    ),
}
ALPHAS = (Fraction(1, 10), Fraction(1, 20), Fraction(1, 50), Fraction(1, 100))


def _site():
    code = f"batch {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _z_text(z):
    return f"{float(z):.2f}"


def _phi_excerpt(magnitude):
    """Use the shared renderer with a needed row and two noncolliding decoys."""
    magnitude = round(float(abs(magnitude)), 1)
    candidates = [round(magnitude + offset, 1)
                  for offset in (0.2, 0.3, -0.2, -0.3, 0.5, -0.5)]
    decoys = []
    for candidate in candidates:
        if 0 < candidate <= 3.4 and candidate != magnitude and candidate not in decoys:
            decoys.append(candidate)
        if len(decoys) == 2:
            break
    assert len(decoys) == 2
    return phi_table([magnitude, *decoys], decoys=0)


def _tail_and_z(tail=None, magnitudes=None):
    tail = tail or random.choice(("right", "left", "two"))
    magnitudes = magnitudes or tuple(Fraction(k, 10) for k in range(5, 35))
    magnitude = random.choice(magnitudes)
    if tail == "left":
        z = -magnitude
    elif tail == "two" and random.choice((True, False)):
        z = -magnitude
    else:
        z = magnitude
    return tail, z


def _hypotheses(parameter, null, tail):
    relation = {"right": ">", "left": "<", "two": "≠"}[tail]
    return f"H0: {parameter} = {null}; Ha: {parameter} {relation} {null}"


def _pvalue_steps(tail, z):
    magnitude = abs(z)
    lookup = Fraction(p4(phi(float(magnitude))))
    upper = 1 - lookup
    steps = []
    if tail == "right":
        steps.extend([
            step("PVALUE_RULE", "right tail", "p = 1 − Φ(z)"),
            step("TABLE_LOOKUP", f"Φ({_z_text(magnitude)})", p4(lookup)),
            step("S", "1.0000", p4(lookup), p4(upper)),
        ])
        value = upper
    elif tail == "left":
        steps.extend([
            step("PVALUE_RULE", "left tail", "p = Φ(z)"),
            step("TABLE_LOOKUP", f"Φ({_z_text(magnitude)})", p4(lookup)),
            step("REWRITE", f"Φ({_z_text(z)}) = 1 − Φ({_z_text(magnitude)})"),
            step("S", "1.0000", p4(lookup), p4(upper)),
        ])
        value = upper
    else:
        value = 2 * upper
        steps.extend([
            step("PVALUE_RULE", "two-sided", "p = 2P(Z ≥ abs(z))"),
            step("TABLE_LOOKUP", f"Φ({_z_text(magnitude)})", p4(lookup)),
            step("S", "1.0000", p4(lookup), p4(upper)),
            step("M", 2, p4(upper), p4(value)),
        ])
    return steps, value


def _decision(value, alpha):
    reject = value < alpha
    relation = "<" if reject else "≥"
    label = "reject H0" if reject else "fail to reject H0"
    comparison = f"p = {p4(value)} {relation} {num_txt(alpha)}"
    return (step("CHECK", "p vs α", comparison, label),
            f"{label} ({comparison})")


class PValueGenerator(ProblemGenerator):
    """Generate supplied-table p-values and p-value decisions."""

    VARIANTS = ("right_tail", "left_tail", "two_sided", "decision_alpha",
                "from_prop_data", "from_mean_data", "compare_alphas")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _direct(variant):
        if variant == "right_tail":
            tail, z = _tail_and_z("right")
        elif variant == "left_tail":
            tail, z = _tail_and_z("left")
        elif variant == "two_sided":
            tail, z = _tail_and_z("two")
        elif variant == "compare_alphas":
            tail = random.choice(("right", "left", "two"))
            eligible = []
            for k in range(5, 35):
                magnitude = Fraction(k, 10)
                upper = 1 - Fraction(p4(phi(float(magnitude))))
                value = 2 * upper if tail == "two" else upper
                if Fraction(1, 100) <= value < Fraction(1, 20):
                    eligible.append(magnitude)
            tail, z = _tail_and_z(tail, tuple(eligible))
        else:
            tail, z = _tail_and_z()
        hypotheses = _hypotheses("p", "1/2", tail)
        alpha = random.choice(ALPHAS) if variant == "decision_alpha" else None
        if variant == "decision_alpha":
            target = f"find the p-value and decide at α = {num_txt(alpha)}"
        elif variant == "compare_alphas":
            target = "compare decisions at α = 0.05 and α = 0.01"
        else:
            target = "find the p-value"
        prefix = (f"At the {_site()}, a z-test uses {hypotheses} "
                  f"({tail}-tailed). Data: z = {_z_text(z)}. Target: {target}.")
        setup_data = f"z = {_z_text(z)}"
        if alpha is not None:
            setup_data += f", α = {num_txt(alpha)}"
        steps = [step("HT_SETUP", hypotheses, setup_data)]
        extra, value = _pvalue_steps(tail, z)
        steps.extend(extra)
        if variant == "decision_alpha":
            check, answer = _decision(value, alpha)
            steps.append(check)
        elif variant == "compare_alphas":
            check_05, _ = _decision(value, Fraction(1, 20))
            check_01, _ = _decision(value, Fraction(1, 100))
            steps.extend([check_05, check_01])
            answer = (f"reject at 0.05, fail at 0.01; p = {p4(value)}")
        else:
            answer = p4(value)
        return prefix, steps, answer, z

    @staticmethod
    def _from_prop_data():
        tail, z = _tail_and_z()
        root_n = random.choice((20, 40, 60))
        n = root_n * root_n
        null = Fraction(1, 2)
        se = Fraction(1, 2 * root_n)
        phat = null + z * se
        successes = phat * n
        assert successes.denominator == 1 and 0 < successes < n
        successes = int(successes)
        hypotheses = _hypotheses("p", "1/2", tail)
        target = "compute z from the data and find the p-value"
        prefix = (f"At the {_site()}, a one-proportion z-test uses {hypotheses} "
                  f"({tail}-tailed). Data: n = {n}, successes = {successes}. "
                  f"Target: {target}.")
        variance = null * (1 - null) / n
        steps = [step("HT_SETUP", hypotheses,
                      f"n = {n}, successes = {successes}"),
                 step("D", successes, n, num_txt(phat)),
                 step("TEST_STAT_FORMULA", "z = (p̂ − p0)/√(p0(1 − p0)/n)"),
                 step("S", 1, prob_txt(null), prob_txt(1 - null)),
                 step("M", prob_txt(null), prob_txt(1 - null), prob_txt(null * (1 - null))),
                 step("D", prob_txt(null * (1 - null)), n, prob_txt(variance)),
                 step("ROOT", prob_txt(variance), 2, num_txt(se)),
                 step("S", num_txt(phat), prob_txt(null), num_txt(phat - null)),
                 step("D", num_txt(phat - null), num_txt(se), _z_text(z))]
        extra, value = _pvalue_steps(tail, z)
        steps.extend(extra)
        return prefix, steps, p4(value), z

    @staticmethod
    def _from_mean_data():
        tail, z = _tail_and_z()
        root_n = random.choice((10, 20, 30))
        n = root_n * root_n
        se = random.randint(1, 5)
        sigma = se * root_n
        null = random.randint(4 * sigma, 4 * sigma + 180)
        xbar = Fraction(null) + z * se
        hypotheses = _hypotheses("μ", str(null), tail)
        target = "compute z from the data and find the p-value"
        prefix = (f"At the {_site()}, a known-σ mean z-test uses {hypotheses} "
                  f"({tail}-tailed). Data: n = {n}, x̄ = {num_txt(xbar)}, "
                  f"population σ = {sigma}. Target: {target}.")
        steps = [step("HT_SETUP", hypotheses,
                      f"n = {n}, x̄ = {num_txt(xbar)}, σ = {sigma}"),
                 step("TEST_STAT_FORMULA", "z = (x̄ − μ0)/(σ/√n)"),
                 step("ROOT", n, 2, root_n),
                 step("D", sigma, root_n, se),
                 step("S", num_txt(xbar), null, num_txt(xbar - null)),
                 step("D", num_txt(xbar - null), se, _z_text(z))]
        extra, value = _pvalue_steps(tail, z)
        steps.extend(extra)
        return prefix, steps, p4(value), z

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "from_prop_data":
            prefix, steps, answer, z = self._from_prop_data()
        elif variant == "from_mean_data":
            prefix, steps, answer, z = self._from_mean_data()
        else:
            prefix, steps, answer, z = self._direct(variant)
        problem = "\n".join((prefix, _phi_excerpt(abs(z)),
                             random.choice(QUERIES[variant])))
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_p_value_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

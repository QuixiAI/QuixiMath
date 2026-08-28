"""Exact Neyman-Pearson and supplied-critical-value likelihood-ratio tests.

Variants: ``np_ratio_bernoulli``, ``np_region``, ``np_power``,
``wilks_normal``, and ``wilks_df``. Bernoulli likelihoods and binomial tails
use exact ``Fraction`` arithmetic with n at most 10 (the direct likelihood
ratio uses n at most 6). The Wilks normal case uses the exact known-variance
closed form and prints its chi-square(1) critical value; no Bernoulli or
Poisson logarithm is approximated. Op-codes: ``LR_FORMULA``, ``TAIL_ROW``,
``NCR``, ``LOOKUP_SUPPLIED``, ``CHECK``, ``SUM``, ``S``, ``A``, ``M``,
``D``, ``E``, and ``Z``.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, prob_txt


STATISTICS = True

PARAMETER_PAIRS = (
    (Fraction(1, 5), Fraction(2, 5)),
    (Fraction(1, 4), Fraction(1, 2)),
    (Fraction(1, 3), Fraction(2, 3)),
    (Fraction(2, 5), Fraction(3, 5)),
    (Fraction(1, 2), Fraction(3, 4)),
    (Fraction(1, 2), Fraction(4, 5)),
)
ALTERNATIVES = (Fraction(3, 5), Fraction(2, 3), Fraction(3, 4),
                Fraction(4, 5))
LOCATIONS = (
    "north lab", "south lab", "river office", "lake office",
    "maple center", "oak center", "pine archive", "cedar archive",
    "amber campus", "birch campus", "granite clinic", "harbor clinic",
)
STUDIES = (
    "likelihood study", "testing review", "power audit", "model trial",
    "sampling review", "method study", "decision audit",
    "asymptotic review", "quality study", "pilot analysis",
    "calibration review", "reliability study",
)

QUERIES = {
    "np_ratio_bernoulli": (
        "Compute the exact simple-null to simple-alternative likelihood ratio Λ.",
        "Find L(p0)/L(p1) from the observed success count.",
        "Evaluate the Neyman-Pearson likelihood ratio as a reduced fraction.",
        "Report the exact Bernoulli likelihood ratio.",
    ),
    "np_region": (
        "Find the smallest cutoff c meeting the target and report its achieved α.",
        "Enumerate the upper binomial tail and choose the rejection boundary.",
        "Determine c for a rejection region S ≥ c under H0.",
        "Report the exact critical count and Type-I error probability.",
    ),
    "np_power": (
        "Compute the exact power P(S ≥ c) at the stated alternative.",
        "Enumerate the alternative upper tail of the rejection region.",
        "Find the Neyman-Pearson test's power at p1.",
        "Report the reduced-fraction rejection probability under Ha.",
    ),
    "wilks_normal": (
        "Compute -2 ln Λ and make the likelihood-ratio decision.",
        "Apply the known-variance normal Wilks statistic.",
        "Compare the exact LRT statistic with the supplied χ² cutoff.",
        "Report the statistic and reject-or-fail-to-reject conclusion.",
    ),
    "wilks_df": (
        "Find the Wilks chi-square degrees of freedom from the parameter counts.",
        "Subtract the null dimension from the unrestricted dimension.",
        "How many restrictions determine the asymptotic χ² df?",
        "Report df and the free-parameter subtraction.",
    ),
}


def _site():
    record = f"lrt {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(STUDIES)} ({record})")


def _binomial_tail(n, cutoff, probability):
    terms = []
    rows = []
    complement = 1 - probability
    for successes in range(cutoff, n + 1):
        failures = n - successes
        coefficient = math.comb(n, successes)
        success_power = probability ** successes
        failure_power = complement ** failures
        term = coefficient * success_power * failure_power
        rows.append((successes, failures, coefficient, success_power,
                     failure_power, term))
        terms.append(term)
    return rows, sum(terms, Fraction(0))


class LikelihoodRatioTestGenerator(ProblemGenerator):
    """Generate exact likelihood-ratio calculations and Wilks checks.

    The module docstring lists variants, bounds, exactness construction,
    supplied-value policy, and op-codes.
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
                "operation": f"statistics_likelihood_ratio_test_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _np_ratio(self):
        n = random.randint(3, 6)
        successes = random.randint(0, n)
        failures = n - successes
        p0, p1 = random.choice(PARAMETER_PAIRS)
        q0, q1 = 1 - p0, 1 - p1
        p0_power, q0_power = p0 ** successes, q0 ** failures
        p1_power, q1_power = p1 ** successes, q1 ** failures
        numerator = p0_power * q0_power
        denominator = p1_power * q1_power
        ratio = numerator / denominator
        steps = [
            step("LR_FORMULA", "Λ = p0^S(1-p0)^(n-S) / "
                 "[p1^S(1-p1)^(n-S)]"),
            step("S", n, successes, failures),
            step("S", 1, str(p0), prob_txt(q0)),
            step("S", 1, str(p1), prob_txt(q1)),
            step("E", str(p0), successes, prob_txt(p0_power)),
            step("E", prob_txt(q0), failures, prob_txt(q0_power)),
            step("M", prob_txt(p0_power), prob_txt(q0_power), prob_txt(numerator)),
            step("E", str(p1), successes, prob_txt(p1_power)),
            step("E", prob_txt(q1), failures, prob_txt(q1_power)),
            step("M", prob_txt(p1_power), prob_txt(q1_power), prob_txt(denominator)),
            step("D", prob_txt(numerator), prob_txt(denominator), prob_txt(ratio)),
            step("CHECK", "binomial coefficient cancels", f"C({n},{successes})",
                 "same numerator and denominator"),
        ]
        problem = (f"At the {_site()}, n = {n} Bernoulli trials produced "
                   f"S = {successes} successes. Test simple H0: p = {p0} "
                   f"against simple H1: p = {p1}.\n"
                   f"{random.choice(QUERIES['np_ratio_bernoulli'])}")
        return self._result("np_ratio_bernoulli", problem, steps,
                            prob_txt(ratio))

    def _region(self):
        n = random.randint(4, 10)
        cutoff = random.randint(2, n)
        probability = Fraction(1, 2)
        rows, alpha = _binomial_tail(n, cutoff, probability)
        previous_rows, previous = _binomial_tail(n, cutoff - 1, probability)
        base = probability ** n
        steps = [step("LR_FORMULA", "reject H0 when S ≥ c; H0: p = 1/2"),
                 step("E", "1/2", n, prob_txt(base))]
        terms = []
        for successes, _, coefficient, _, _, term in rows:
            steps.extend([step("NCR", f"C({n},{successes})", coefficient),
                          step("M", coefficient, prob_txt(base),
                               prob_txt(term)),
                          step("TAIL_ROW", successes, prob_txt(term))])
            terms.append(term)
        steps.append(step("SUM", " + ".join(prob_txt(value) for value in terms),
                          prob_txt(alpha)))
        # Show why c-1 is too liberal without repeating the entire tail.
        previous_term = previous_rows[0][-1]
        steps.extend([
            step("NCR", f"C({n},{cutoff - 1})",
                 math.comb(n, cutoff - 1)),
            step("M", math.comb(n, cutoff - 1), prob_txt(base),
                 prob_txt(previous_term)),
            step("A", prob_txt(previous_term), prob_txt(alpha),
                 prob_txt(previous)),
            step("CHECK", "smallest cutoff",
                 f"P(S ≥ {cutoff}) = {prob_txt(alpha)} ≤ {prob_txt(alpha)}; "
                 f"P(S ≥ {cutoff - 1}) = {prob_txt(previous)} > {prob_txt(alpha)}",
                 cutoff),
        ])
        answer = f"c = {cutoff}; α = {prob_txt(alpha)}"
        problem = (f"At the {_site()}, under H0, S ~ Binomial(n = {n}, "
                   f"p = 1/2). Reject for S ≥ c. Choose the smallest c with "
                   f"Type-I error at most α0 = {prob_txt(alpha)}.\n"
                   f"{random.choice(QUERIES['np_region'])}")
        return self._result("np_region", problem, steps, answer)

    def _power(self):
        n = random.randint(4, 10)
        cutoff = random.randint(2, n)
        probability = random.choice(ALTERNATIVES)
        complement = 1 - probability
        rows, power = _binomial_tail(n, cutoff, probability)
        steps = [step("LR_FORMULA", "power = P_p1(S ≥ c)")]
        terms = []
        for successes, failures, coefficient, success_power, failure_power, term in rows:
            partial = coefficient * success_power
            steps.extend([
                step("S", n, successes, failures),
                step("NCR", f"C({n},{successes})", coefficient),
                step("E", str(probability), successes, prob_txt(success_power)),
                step("E", prob_txt(complement), failures, prob_txt(failure_power)),
                step("M", coefficient, prob_txt(success_power), prob_txt(partial)),
                step("M", prob_txt(partial), prob_txt(failure_power), prob_txt(term)),
                step("TAIL_ROW", successes, prob_txt(term)),
            ])
            terms.append(term)
        steps.append(step("SUM", " + ".join(prob_txt(value) for value in terms),
                          prob_txt(power)))
        problem = (f"At the {_site()}, a Bernoulli test with n = {n} rejects "
                   f"when S ≥ {cutoff}. At the alternative p1 = {probability}, "
                   f"find its power.\n"
                   f"{random.choice(QUERIES['np_power'])}")
        return self._result("np_power", problem, steps, prob_txt(power))

    def _wilks_normal(self):
        root_n = random.choice((2, 3, 4, 5))
        n = root_n ** 2
        scale = random.randint(1, 5)
        sigma = root_n * scale
        magnitude = random.choice((1, 2, 3))
        difference = random.choice((-1, 1)) * scale * magnitude
        mu0 = random.randint(20, 100)
        sample_mean = mu0 + difference
        difference_squared = difference ** 2
        numerator = n * difference_squared
        sigma_squared = sigma ** 2
        statistic = Fraction(numerator, sigma_squared)
        critical = Fraction("3.841")
        reject = statistic > critical
        relation = ">" if reject else "≤"
        verdict = "reject H0" if reject else "fail to reject H0"
        steps = [
            step("LR_FORMULA", "-2 ln Λ = n(x̄ - μ0)²/σ²"),
            step("S", sample_mean, mu0, difference),
            step("E", difference, 2, difference_squared),
            step("M", n, difference_squared, numerator),
            step("E", sigma, 2, sigma_squared),
            step("D", numerator, sigma_squared, exact(statistic)),
            step("LOOKUP_SUPPLIED", "χ² critical value (df = 1)", "3.841"),
            step("CHECK", "-2 ln Λ vs χ²",
                 f"{exact(statistic)} {relation} 3.841", verdict),
        ]
        answer = (f"-2 ln Λ = {exact(statistic)}; {verdict} "
                  f"({exact(statistic)} {relation} 3.841)")
        problem = (f"At the {_site()}, σ = {sigma}, n = {n}, and x̄ = "
                   f"{sample_mean}. Test H0: μ = {mu0} against the "
                   f"unrestricted normal-mean alternative; χ² critical "
                   f"value = 3.841 (df = 1).\n"
                   f"{random.choice(QUERIES['wilks_normal'])}")
        return self._result("wilks_normal", problem, steps, answer)

    def _wilks_df(self):
        null_parameters = random.randint(1, 3)
        unrestricted_parameters = random.randint(null_parameters + 1, 5)
        degrees = unrestricted_parameters - null_parameters
        steps = [step("LR_FORMULA", "Wilks df = unrestricted parameters - "
                      "null parameters"),
                 step("S", unrestricted_parameters, null_parameters, degrees),
                 step("CHECK", "number of independent restrictions", degrees)]
        answer = (f"df = {degrees}; {unrestricted_parameters} - "
                  f"{null_parameters}")
        problem = (f"At the {_site()}, an unrestricted model has "
                   f"{unrestricted_parameters} free parameters and its null "
                   f"submodel has {null_parameters} free parameters.\n"
                   f"{random.choice(QUERIES['wilks_df'])}")
        return self._result("wilks_df", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "np_ratio_bernoulli":
            return self._np_ratio()
        if variant == "np_region":
            return self._region()
        if variant == "np_power":
            return self._power()
        if variant == "wilks_normal":
            return self._wilks_normal()
        return self._wilks_df()

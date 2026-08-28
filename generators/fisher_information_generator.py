"""Exact Fisher information and Cramer-Rao lower-bound calculations.

Variants: ``bernoulli``, ``poisson``, ``exponential``, ``normal_mu``,
``geometric``, and ``crlb_check``. Parameters are short rational values and
all information / CRLB expressions reduce exactly. Geometric observations
count trials through the first success (support 1, 2, ...), and every problem
states that convention. CRLB checks use the exact variance of an efficient
sample-mean estimator. Op-codes: ``LOG_LIKELIHOOD``, ``DERIVATIVE``,
``FISHER_INFO``, ``CRLB``, ``CHECK``, ``S``, ``A``, ``M``, ``D``, ``E``,
and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact


STATISTICS = True

PROBABILITIES = (
    Fraction(1, 5), Fraction(1, 4), Fraction(1, 3), Fraction(2, 5),
    Fraction(1, 2), Fraction(3, 5), Fraction(2, 3), Fraction(3, 4),
    Fraction(4, 5),
)
RATES = (
    Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3),
    Fraction(3, 4), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3),
    Fraction(4),
)
SAMPLE_SIZES = (5, 8, 10, 12, 16, 20, 24, 25, 30, 40)
VARIANCES = (1, 2, 3, 4, 5, 8, 9, 10, 12, 16, 20, 25)
LOCATIONS = (
    "north lab", "south lab", "river office", "lake office",
    "maple center", "oak center", "pine archive", "cedar archive",
    "amber campus", "birch campus", "granite clinic", "harbor clinic",
)
STUDIES = (
    "information study", "likelihood review", "efficiency audit",
    "estimator trial", "sampling review", "calibration study",
    "model audit", "variance review", "method comparison",
    "quality study", "pilot analysis", "reliability review",
)

QUERIES = {
    "bernoulli": (
        "Compute I(p), I_n(p), and the CRLB for unbiased estimators of p.",
        "Find the one-observation and sample Fisher information for p.",
        "Use the score identity to obtain the exact Bernoulli CRLB.",
        "Report the Fisher information and reciprocal-information bound.",
    ),
    "poisson": (
        "Compute I(λ), I_n(λ), and the CRLB for unbiased estimators of λ.",
        "Find the one-observation and sample Fisher information for λ.",
        "Use the score identity to obtain the exact Poisson CRLB.",
        "Report the Fisher information and reciprocal-information bound.",
    ),
    "exponential": (
        "Compute I(λ), I_n(λ), and the CRLB for unbiased estimators of λ.",
        "Find the information in this exponential-rate sample.",
        "Use the second derivative to obtain the exact rate-parameter CRLB.",
        "Report the Fisher information and reciprocal-information bound.",
    ),
    "normal_mu": (
        "Compute I(μ), I_n(μ), and the CRLB for unbiased estimators of μ.",
        "Find the information for the normal mean with variance known.",
        "Use the score identity to obtain the exact mean-parameter CRLB.",
        "Report the Fisher information and reciprocal-information bound.",
    ),
    "geometric": (
        "Compute I(p), I_n(p), and the CRLB for unbiased estimators of p.",
        "Find the information in the stated geometric convention.",
        "Use the score variance to obtain the exact geometric CRLB.",
        "Report the Fisher information and reciprocal-information bound.",
    ),
    "crlb_check": (
        "Compare the estimator variance with the CRLB and state whether it attains the bound.",
        "Verify exact efficiency against reciprocal Fisher information.",
        "Does the stated unbiased estimator attain the Cramer-Rao bound?",
        "Compute both variances and report the efficiency verdict.",
    ),
}


def _site():
    record = f"info {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(STUDIES)} ({record})")


def _bernoulli(parameter, n):
    complement = 1 - parameter
    reciprocal_p = 1 / parameter
    reciprocal_q = 1 / complement
    information = reciprocal_p + reciprocal_q
    total = n * information
    bound = 1 / total
    steps = [
        step("LOG_LIKELIHOOD", "ell(p) = x log p + (1-x) log(1-p)"),
        step("DERIVATIVE", "score = x/p - (1-x)/(1-p)"),
        step("DERIVATIVE", "second = -x/p² - (1-x)/(1-p)²"),
        step("FISHER_INFO", "I(p) = -E[second] = 1/p + 1/(1-p)"),
        step("S", 1, str(parameter), exact(complement)),
        step("D", 1, str(parameter), exact(reciprocal_p)),
        step("D", 1, exact(complement), exact(reciprocal_q)),
        step("A", exact(reciprocal_p), exact(reciprocal_q),
             exact(information)),
        step("M", n, exact(information), exact(total)),
        step("D", 1, exact(total), exact(bound)),
        step("CRLB", "1/I_n(p)", exact(bound)),
    ]
    return information, total, bound, steps


def _poisson(parameter, n):
    squared = parameter ** 2
    information = parameter / squared
    total = n * information
    bound = 1 / total
    steps = [
        step("LOG_LIKELIHOOD", "ell(λ) = x log λ - λ - log(x!)"),
        step("DERIVATIVE", "score = x/λ - 1"),
        step("DERIVATIVE", "second = -x/λ²"),
        step("FISHER_INFO", "I(λ) = E[X]/λ² = λ/λ²"),
        step("E", str(parameter), 2, exact(squared)),
        step("D", str(parameter), exact(squared), exact(information)),
        step("M", n, exact(information), exact(total)),
        step("D", 1, exact(total), exact(bound)),
        step("CRLB", "1/I_n(λ)", exact(bound)),
    ]
    return information, total, bound, steps


def _exponential(parameter, n):
    squared = parameter ** 2
    information = 1 / squared
    total = n * information
    bound = 1 / total
    steps = [
        step("LOG_LIKELIHOOD", "ell(λ) = log λ - λx"),
        step("DERIVATIVE", "score = 1/λ - x"),
        step("DERIVATIVE", "second = -1/λ²"),
        step("FISHER_INFO", "I(λ) = -E[second] = 1/λ²"),
        step("E", str(parameter), 2, exact(squared)),
        step("D", 1, exact(squared), exact(information)),
        step("M", n, exact(information), exact(total)),
        step("D", 1, exact(total), exact(bound)),
        step("CRLB", "1/I_n(λ)", exact(bound)),
    ]
    return information, total, bound, steps


def _normal(variance, n):
    information = Fraction(1, variance)
    total = n * information
    bound = 1 / total
    steps = [
        step("LOG_LIKELIHOOD", "ell(μ) = constant - (x-μ)²/(2σ²)"),
        step("DERIVATIVE", "score = (x-μ)/σ²"),
        step("DERIVATIVE", "second = -1/σ²"),
        step("FISHER_INFO", "I(μ) = -E[second] = 1/σ²"),
        step("D", 1, variance, exact(information)),
        step("M", n, exact(information), exact(total)),
        step("D", 1, exact(total), exact(bound)),
        step("CRLB", "1/I_n(μ)", exact(bound)),
    ]
    return information, total, bound, steps


def _geometric(parameter, n):
    squared = parameter ** 2
    complement = 1 - parameter
    denominator = squared * complement
    information = 1 / denominator
    total = n * information
    bound = 1 / total
    steps = [
        step("LOG_LIKELIHOOD", "ell(p) = log p + (x-1) log(1-p)"),
        step("DERIVATIVE", "score = 1/p - (x-1)/(1-p)"),
        step("DERIVATIVE", "second = -1/p² - (x-1)/(1-p)²"),
        step("FISHER_INFO", "I(p) = Var(score) = 1/[p²(1-p)]"),
        step("E", str(parameter), 2, exact(squared)),
        step("S", 1, str(parameter), exact(complement)),
        step("M", exact(squared), exact(complement), exact(denominator)),
        step("D", 1, exact(denominator), exact(information)),
        step("M", n, exact(information), exact(total)),
        step("D", 1, exact(total), exact(bound)),
        step("CRLB", "1/I_n(p)", exact(bound)),
    ]
    return information, total, bound, steps


class FisherInformationGenerator(ProblemGenerator):
    """Generate exact Fisher-information and Cramer-Rao calculations.

    Family conventions, variants, exact parameter banks, and op-codes are
    documented in the module docstring.
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
                "operation": f"statistics_fisher_information_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _family(self, variant):
        n = random.choice(SAMPLE_SIZES)
        if variant == "bernoulli":
            parameter = random.choice(PROBABILITIES)
            information, total, bound, steps = _bernoulli(parameter, n)
            symbol = "p"
            setup = (f"n = {n} independent Bernoulli(p) observations with "
                     f"p = {parameter}")
        elif variant == "poisson":
            parameter = random.choice(RATES)
            information, total, bound, steps = _poisson(parameter, n)
            symbol = "λ"
            setup = (f"n = {n} independent Poisson(λ) observations with "
                     f"λ = {parameter}")
        elif variant == "exponential":
            parameter = random.choice(RATES)
            information, total, bound, steps = _exponential(parameter, n)
            symbol = "λ"
            setup = (f"n = {n} independent Exponential(rate λ) observations "
                     f"with λ = {parameter}")
        elif variant == "normal_mu":
            variance = random.choice(VARIANCES)
            mean = random.randint(-10, 20)
            information, total, bound, steps = _normal(variance, n)
            symbol = "μ"
            setup = (f"n = {n} independent Normal(μ, σ²) observations with "
                     f"μ = {mean} and known σ² = {variance}")
        else:
            parameter = random.choice(PROBABILITIES)
            information, total, bound, steps = _geometric(parameter, n)
            symbol = "p"
            setup = (f"n = {n} independent Geometric(p) observations on "
                     f"1, 2, ... with pmf p(1-p)^(x-1) and p = {parameter}")
        answer = (f"I({symbol}) = {exact(information)}; "
                  f"I_n({symbol}) = {exact(total)}; CRLB = {exact(bound)}")
        problem = (f"At the {_site()}, consider {setup}. Treat Fisher "
                   f"information as the expected squared score.\n"
                   f"{random.choice(QUERIES[variant])}")
        return self._result(variant, problem, steps, answer)

    def _check(self):
        family = random.choice(("bernoulli", "poisson", "normal_mu"))
        n = random.choice(SAMPLE_SIZES)
        if family == "bernoulli":
            parameter = random.choice(PROBABILITIES)
            information, total, bound, steps = _bernoulli(parameter, n)
            complement = 1 - parameter
            product = parameter * complement
            estimator_variance = product / n
            steps.extend([step("S", 1, str(parameter), exact(complement)),
                          step("M", str(parameter), exact(complement),
                               exact(product)),
                          step("D", exact(product), n,
                               exact(estimator_variance))])
            estimator = "p̂"
            setup = (f"n = {n} independent Bernoulli(p) observations with "
                     f"p = {parameter}; use p̂ = x̄")
        elif family == "poisson":
            parameter = random.choice(RATES)
            information, total, bound, steps = _poisson(parameter, n)
            estimator_variance = parameter / n
            steps.append(step("D", str(parameter), n,
                              exact(estimator_variance)))
            estimator = "λ̂"
            setup = (f"n = {n} independent Poisson(λ) observations with "
                     f"λ = {parameter}; use λ̂ = x̄")
        else:
            variance = random.choice(VARIANCES)
            mean = random.randint(-10, 20)
            information, total, bound, steps = _normal(variance, n)
            estimator_variance = Fraction(variance, n)
            steps.append(step("D", variance, n, exact(estimator_variance)))
            estimator = "x̄"
            setup = (f"n = {n} independent Normal(μ, σ²) observations with "
                     f"μ = {mean} and known σ² = {variance}; use x̄ for μ")
        steps.append(step("CHECK", f"Var({estimator}) vs CRLB",
                          f"{exact(estimator_variance)} = {exact(bound)}",
                          "attains the bound"))
        answer = (f"CRLB = {exact(bound)}; Var({estimator}) = "
                  f"{exact(estimator_variance)}; attains the bound")
        problem = (f"At the {_site()}, consider {setup}.\n"
                   f"{random.choice(QUERIES['crlb_check'])}")
        return self._result("crlb_check", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "crlb_check":
            return self._check()
        return self._family(variant)

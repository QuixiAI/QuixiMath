"""Factorization-theorem exercises with exact sufficient statistics.

Variants: ``identify_T``, ``factor_and_evaluate``, ``uniform_max``,
``two_dimensional``, and ``ratio_check``. The family bank covers Bernoulli,
Poisson, exponential, geometric, normal mean with known variance, uniform
endpoint, and normal with both parameters unknown. Data statistics and the
Poisson factorial factor are evaluated exactly; normal factors remain in the
plan's symbolic ``(2πσ²)^(-n/2)`` form. Op-codes: ``LOG_LIKELIHOOD``,
``LIKELIHOOD_FACTOR``, ``LIKELIHOOD_RATIO``, ``SUFFICIENT``, ``FACTORIAL``,
``SUM``, ``S``, ``M``, ``E``, ``CHECK``, and ``Z``.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact


STATISTICS = True

FAMILIES = (
    "bernoulli", "poisson", "exponential", "geometric", "normal_mu",
    "uniform", "normal_two",
)
LOCATIONS = (
    "north lab", "south lab", "river office", "lake office",
    "maple center", "oak center", "pine archive", "cedar archive",
    "amber campus", "birch campus", "granite clinic", "harbor clinic",
)
STUDIES = (
    "factorization study", "likelihood review", "sufficiency audit",
    "estimator trial", "sampling review", "model study", "method audit",
    "distribution review", "quality study", "pilot analysis",
    "calibration review", "reliability study",
)

QUERIES = {
    "identify_T": (
        "Use the factorization theorem to identify and evaluate a sufficient statistic.",
        "Which statistic T captures all parameter dependence?",
        "Factor the joint likelihood and report the sufficient statistic.",
        "Identify T and evaluate it on the printed sample.",
    ),
    "factor_and_evaluate": (
        "Factor the joint likelihood as g(T, parameter)h(x) and evaluate every data-only factor.",
        "Find T and the evaluated g and h factors.",
        "Apply the factorization theorem and report the exact factorization.",
        "Separate parameter dependence from the data-only term.",
    ),
    "uniform_max": (
        "Factor the likelihood and identify the sample maximum as sufficient.",
        "Evaluate the endpoint statistic T = max x_i.",
        "Use the indicator in the uniform likelihood to find T.",
        "Report the exact uniform-endpoint factorization.",
    ),
    "two_dimensional": (
        "Identify and evaluate the two-dimensional sufficient statistic.",
        "Factor the normal likelihood when both μ and σ² are unknown.",
        "Report (Σx_i, Σx_i²) for the sample.",
        "Separate the two data summaries needed by the likelihood.",
    ),
    "ratio_check": (
        "Use the equal sufficient statistics to compute L(p; x)/L(p; y).",
        "Verify the likelihood-ratio criterion for sufficiency.",
        "Show that the ratio for these two samples is free of p.",
        "Compute the exact likelihood ratio and the common T value.",
    ),
}


def _site():
    record = f"factor {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(STUDIES)} ({record})")


def _data_text(values):
    return "[" + ", ".join(map(str, values)) + "]"


def _case(family):
    if family == "bernoulli":
        n = random.randint(4, 8)
        successes = random.randint(2, n - 2)
        data = [1] * successes + [0] * (n - successes)
        random.shuffle(data)
        return data, None
    if family == "poisson":
        n = random.randint(3, 5)
        data = [random.randint(0, 5) for _ in range(n)]
        if sum(data) < 2:
            data[random.randrange(n)] = random.randint(2, 5)
        return data, None
    if family == "exponential":
        return [random.randint(1, 9) for _ in range(random.randint(3, 6))], None
    if family == "geometric":
        data = [random.randint(1, 6) for _ in range(random.randint(3, 6))]
        if sum(data) - len(data) < 2:
            data[0] += 2 - (sum(data) - len(data))
        return data, None
    if family == "normal_mu":
        data = [random.randint(1, 9) for _ in range(random.randint(3, 6))]
        return data, random.choice((1, 2, 3, 4, 5, 8, 9, 10))
    if family == "uniform":
        return random.sample(range(1, 25), random.randint(3, 6)), None
    return [random.randint(1, 9) for _ in range(random.randint(3, 6))], None


def _model_text(family, variance=None):
    return {
        "bernoulli": "Bernoulli(p)",
        "poisson": "Poisson(λ)",
        "exponential": "Exponential(rate λ)",
        "geometric": "Geometric(p) on {1, 2, ...}",
        "normal_mu": f"Normal(μ, known σ² = {variance})",
        "uniform": "Uniform(0, θ)",
        "normal_two": "Normal(μ, σ²) with both parameters unknown",
    }[family]


def _symbolic_factor(family, n, variance=None):
    if family == "bernoulli":
        return ("joint = p^Σx (1-p)^(n-Σx)",
                "g(T,p) = p^T (1-p)^(n-T)", "h(x) = 1")
    if family == "poisson":
        return ("joint = λ^Σx e^(-nλ) / Πx_i!",
                "g(T,λ) = λ^T e^(-nλ)", "h(x) = 1/Πx_i!")
    if family == "exponential":
        return ("joint = λ^n e^(-λΣx)",
                "g(T,λ) = λ^n e^(-λT)", "h(x) = 1")
    if family == "geometric":
        return ("joint = p^n (1-p)^(Σx-n)",
                "g(T,p) = p^n (1-p)^(T-n)", "h(x) = 1")
    if family == "normal_mu":
        return ("joint = (2πσ²)^(-n/2) exp[-Σ(x_i-μ)²/(2σ²)]",
                "g(T,μ) = exp[μT/σ² - nμ²/(2σ²)]",
                "h(x) = (2πσ²)^(-n/2) exp[-Σx_i²/(2σ²)]")
    if family == "uniform":
        return ("joint = θ^(-n) 1(max x_i ≤ θ)",
                "g(T,θ) = θ^(-n) 1(T ≤ θ)", "h(x) = 1")
    return (
        "joint = (2πσ²)^(-n/2) exp[-(Σx_i² - 2μΣx_i + nμ²)/(2σ²)]",
        "g(T,μ,σ²) = (2πσ²)^(-n/2) exp[-(T2 - 2μT1 + nμ²)/(2σ²)]",
        "h(x) = 1",
    )


def _summary_steps(family, data):
    total = sum(data)
    squares = [value ** 2 for value in data]
    sum_squares = sum(squares)
    steps = []
    if family == "uniform":
        maximum = max(data)
        steps.append(step("CHECK", "max of sample", _data_text(data), maximum))
        steps.append(step("SUFFICIENT", "T = max x_i", maximum))
        return steps, maximum, None
    steps.append(step("SUM", " + ".join(map(str, data)), total))
    if family == "normal_two":
        for value, square in zip(data, squares):
            steps.append(step("E", value, 2, square))
        steps.append(step("SUM", " + ".join(map(str, squares)), sum_squares))
        steps.append(step("SUFFICIENT", "T = (Σx_i, Σx_i²)",
                          f"({total}, {sum_squares})"))
        return steps, total, sum_squares
    steps.append(step("SUFFICIENT", "T = Σx_i", total))
    return steps, total, None


def _evaluated_factor(family, data, variance=None):
    n = len(data)
    total = sum(data)
    if family == "bernoulli":
        failures = n - total
        return f"p^{total}(1-p)^{failures}", "1"
    if family == "poisson":
        product = math.prod(math.factorial(value) for value in data)
        return f"λ^{total} e^(-{n}λ)", exact(Fraction(1, product))
    if family == "exponential":
        return f"λ^{n} e^(-{total}λ)", "1"
    if family == "geometric":
        return f"p^{n}(1-p)^{total - n}", "1"
    if family == "normal_mu":
        sum_squares = sum(value ** 2 for value in data)
        g = f"exp[μ·{total}/{variance} - {n}μ²/(2·{variance})]"
        h = (f"(2π·{variance})^(-{n}/2) "
             f"exp[-{sum_squares}/(2·{variance})]")
        return g, h
    maximum = max(data)
    return f"θ^(-{n}) 1({maximum} ≤ θ)", "1"


class SufficiencyFactorizationGenerator(ProblemGenerator):
    """Generate factorization-theorem and likelihood-ratio exercises.

    The module docstring lists the seven families, variants, symbolic-normal
    convention, op-codes, and exact data-factor construction.
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
                "operation": f"statistics_sufficiency_factorization_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _identify(self):
        family = random.choice(FAMILIES)
        data, variance = _case(family)
        joint, g_text, h_text = _symbolic_factor(family, len(data), variance)
        steps = [step("LOG_LIKELIHOOD", joint),
                 step("LIKELIHOOD_FACTOR", g_text, h_text)]
        summary, first, second = _summary_steps(family, data)
        steps.extend(summary)
        if family == "uniform":
            answer = f"T = max x_i = {first}"
        elif family == "normal_two":
            answer = f"T = (Σx_i, Σx_i²) = ({first}, {second})"
        else:
            answer = f"T = Σx_i = {first}"
        problem = (f"At the {_site()}, a sample from "
                   f"{_model_text(family, variance)} is {_data_text(data)}.\n"
                   f"{random.choice(QUERIES['identify_T'])}")
        return self._result("identify_T", problem, steps, answer)

    def _factor(self, forced_family=None, variant="factor_and_evaluate"):
        family = forced_family or random.choice(FAMILIES[:-1])
        data, variance = _case(family)
        n = len(data)
        joint, g_text, h_text = _symbolic_factor(family, n, variance)
        steps = [step("LOG_LIKELIHOOD", joint),
                 step("LIKELIHOOD_FACTOR", g_text, h_text)]
        summary, first, second = _summary_steps(family, data)
        steps.extend(summary)
        if family == "bernoulli":
            steps.append(step("S", n, first, n - first))
        elif family == "geometric":
            steps.append(step("S", first, n, first - n))
        elif family == "poisson":
            accumulator = 1
            for value in data:
                factorial = math.factorial(value)
                steps.append(step("FACTORIAL", value, factorial))
                product = accumulator * factorial
                steps.append(step("M", accumulator, factorial, product))
                accumulator = product
        elif family == "normal_mu":
            squares = [value ** 2 for value in data]
            for value, square in zip(data, squares):
                steps.append(step("E", value, 2, square))
            steps.append(step("SUM", " + ".join(map(str, squares)),
                              sum(squares)))
        g_value, h_value = _evaluated_factor(family, data, variance)
        steps.append(step("LIKELIHOOD_FACTOR", f"g = {g_value}",
                          f"h = {h_value}"))
        if family == "uniform":
            t_text = f"T = max x_i = {first}"
        else:
            t_text = f"T = Σx_i = {first}"
        answer = f"{t_text}; g = {g_value}; h = {h_value}"
        problem = (f"At the {_site()}, a sample from "
                   f"{_model_text(family, variance)} is {_data_text(data)}.\n"
                   f"{random.choice(QUERIES[variant])}")
        return self._result(variant, problem, steps, answer)

    def _two_dimensional(self):
        family = "normal_two"
        data, _ = _case(family)
        n = len(data)
        joint, g_text, h_text = _symbolic_factor(family, n)
        steps = [step("LOG_LIKELIHOOD", joint),
                 step("LIKELIHOOD_FACTOR", g_text, h_text)]
        summary, total, sum_squares = _summary_steps(family, data)
        steps.extend(summary)
        g_value = (f"(2πσ²)^(-{n}/2) exp[-({sum_squares} - "
                   f"2μ·{total} + {n}μ²)/(2σ²)]")
        steps.append(step("LIKELIHOOD_FACTOR", f"g = {g_value}", "h = 1"))
        answer = (f"T = (Σx_i, Σx_i²) = ({total}, {sum_squares}); "
                  f"g = {g_value}; h = 1")
        problem = (f"At the {_site()}, a sample from "
                   f"{_model_text(family)} is {_data_text(data)}.\n"
                   f"{random.choice(QUERIES['two_dimensional'])}")
        return self._result("two_dimensional", problem, steps, answer)

    def _ratio(self):
        n = random.randint(4, 8)
        successes = random.randint(1, n - 1)
        first = [1] * successes + [0] * (n - successes)
        random.shuffle(first)
        while True:
            second = list(first)
            random.shuffle(second)
            if second != first:
                break
        steps = [
            step("LOG_LIKELIHOOD", "L(p;x) = p^Σx(1-p)^(n-Σx)"),
            step("SUM", " + ".join(map(str, first)), sum(first)),
            step("SUM", " + ".join(map(str, second)), sum(second)),
            step("SUFFICIENT", "T(x) = T(y) = Σx_i", successes),
            step("LIKELIHOOD_RATIO", "L(p;x)/L(p;y)", "1"),
            step("CHECK", "ratio free of p", "1", "same sufficient statistic"),
        ]
        answer = f"ratio = 1; T(x) = T(y) = {successes}"
        problem = (f"At the {_site()}, two Bernoulli(p) samples are x = "
                   f"{_data_text(first)} and y = {_data_text(second)}.\n"
                   f"{random.choice(QUERIES['ratio_check'])}")
        return self._result("ratio_check", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "identify_T":
            return self._identify()
        if variant == "factor_and_evaluate":
            return self._factor()
        if variant == "uniform_max":
            return self._factor("uniform", "uniform_max")
        if variant == "two_dimensional":
            return self._two_dimensional()
        return self._ratio()

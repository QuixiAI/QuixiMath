"""Compute transformed expectations and variances from finite pmfs.

Variants: ``e_g_x``, ``var_shortcut``, ``linear_mean_var``, ``standardize``,
and ``compare_routes``. Op-codes: ``WEIGHT``, ``EV_FORMULA``, ``G_ROW``,
``VAR_FORMULA``, ``M``, ``A``, ``S``, ``D``, ``E``, ``ROOT``, ``CHECK``,
and ``Z``. Random supports, dyadic weights, functions, affine parameters,
and five phrasings give an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
QUERIES = {
    "e_g_x": (
        "Find E[g(X)].",
        "Evaluate g at every support value and compute the weighted sum.",
        "What is the exact expectation of the displayed function of X?",
        "Use the pmf to determine E[g(X)] directly.",
        "Build each g(x)·P(X=x) term and add them.",
    ),
    "var_shortcut": (
        "Find E[X²] and Var(X) using the shortcut formula.",
        "Compute both raw moments, then subtract (E[X])² from E[X²].",
        "Use Var(X) = E[X²] − (E[X])².",
        "What are the exact second moment and variance?",
        "Determine the variance from the two required expectations.",
    ),
    "linear_mean_var": (
        "Find E[Y] and Var(Y).",
        "Use the affine transformation rules for mean and variance.",
        "Compute both exact moments of Y from the moments of X.",
        "What are the expectation and variance after the displayed transformation?",
        "Apply E[aX+b] and Var(aX+b) to the finite distribution.",
    ),
    "standardize": (
        "Find μ, σ, and the z-score of the displayed x value.",
        "Compute the exact mean and variance, take its exact root, and standardize x.",
        "What is z = (x − μ)/σ for the stated observation?",
        "Use the pmf to verify the moments before finding the z-score.",
        "Determine the exact standard score with no decimal approximation.",
    ),
    "compare_routes": (
        "Compute Var(X) by both the shortcut and definition routes.",
        "Compare E[X²] − (E[X])² with the weighted squared-deviation sum.",
        "Find the exact variance twice and verify that the routes agree.",
        "Use both standard formulas for Var(X).",
        "Report the shortcut value and the direct-definition value.",
    ),
}


def _distribution(nonzero=False):
    size = random.randint(3, 5)
    pool = [value for value in range(-12, 16) if not nonzero or value != 0]
    support = tuple(sorted(random.sample(pool, size)))
    total = 2 ** random.randint(4, 8)
    cuts = sorted(random.sample(range(1, total), size - 1))
    counts = [cuts[0]]
    counts.extend(cuts[i] - cuts[i - 1] for i in range(1, len(cuts)))
    counts.append(total - cuts[-1])
    return support, tuple(Fraction(count, total) for count in counts)


def _pmf_text(support, weights):
    return "; ".join(f"P(X={x}) = {prob_txt(weight)}"
                     for x, weight in zip(support, weights))


def _expectation_steps(label, support, weights, function):
    steps = [step("EV_FORMULA", f"E[{label}] = Σ {label.lower()}·P(X=x)")]
    terms = []
    for x, weight in zip(support, weights):
        value = Fraction(function(x))
        term = value * weight
        steps.append(step("M", prob_txt(value), prob_txt(weight), prob_txt(term)))
        steps.append(step("G_ROW", f"x={x}", f"g = {prob_txt(value)}",
                          f"{prob_txt(value)} × {prob_txt(weight)} = {prob_txt(term)}"))
        terms.append(term)
    running = terms[0]
    for term in terms[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(term),
                          prob_txt(running + term)))
        running += term
    steps.append(step("CHECK", f"weighted sum for {label}", prob_txt(running)))
    return steps, running


def _shortcut_steps(support, weights):
    mean_steps, mean = _expectation_steps("X", support, weights, lambda x: x)
    square_steps, second = _expectation_steps("X²", support, weights,
                                              lambda x: x * x)
    mean_square = mean ** 2
    variance = second - mean_square
    steps = mean_steps + square_steps
    steps.extend([step("VAR_FORMULA", "Var(X) = E[X²] − (E[X])²"),
                  step("E", prob_txt(mean), 2, prob_txt(mean_square)),
                  step("S", prob_txt(second), prob_txt(mean_square),
                       prob_txt(variance))])
    return steps, mean, second, variance


def _definition_steps(support, weights, mean):
    steps = [step("VAR_FORMULA", "Var(X) = Σ P(X=x)(x − μ)²")]
    terms = []
    for x, weight in zip(support, weights):
        difference = Fraction(x) - mean
        square = difference ** 2
        term = square * weight
        steps.extend([step("S", x, prob_txt(mean), prob_txt(difference)),
                      step("E", prob_txt(difference), 2, prob_txt(square)),
                      step("M", prob_txt(square), prob_txt(weight), prob_txt(term))])
        terms.append(term)
    running = terms[0]
    for term in terms[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(term),
                          prob_txt(running + term)))
        running += term
    steps.append(step("CHECK", "definition variance", prob_txt(running)))
    return steps, running


def _affine_text(a, b):
    leading = "X" if a == 1 else "−X" if a == -1 else f"{a}X"
    if b > 0:
        return f"Y = {leading} + {b}"
    if b < 0:
        return f"Y = {leading} − {abs(b)}"
    return f"Y = {leading}"


class ExpectationOfFunctionGenerator(ProblemGenerator):
    """Generate exact expectation, variance, and standardization exercises."""

    VARIANTS = ("e_g_x", "var_shortcut", "linear_mean_var", "standardize",
                "compare_routes")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _e_g_x():
        kind = random.choice(("square", "affine", "absolute", "reciprocal"))
        support, weights = _distribution(nonzero=kind == "reciprocal")
        if kind == "square":
            rule, function = "g(x) = x²", lambda x: Fraction(x * x)
        elif kind == "affine":
            a = random.choice([value for value in range(-5, 6) if value not in (-1, 0, 1)])
            b = random.randint(-8, 8)
            rule = f"g(x) = {a}x" + (f" + {b}" if b > 0 else
                                      f" − {abs(b)}" if b < 0 else "")
            function = lambda x, a=a, b=b: Fraction(a * x + b)
        elif kind == "absolute":
            c = random.choice([value for value in range(-8, 9) if value])
            sign = f"x − {c}" if c >= 0 else f"x + {abs(c)}"
            rule, function = f"g(x) = abs({sign})", lambda x, c=c: Fraction(abs(x - c))
        else:
            rule, function = "g(x) = 1/x", lambda x: Fraction(1, x)
        prefix = f"X has pmf: {_pmf_text(support, weights)}. Let {rule}."
        steps = [step("WEIGHT", x, prob_txt(weight)) for x, weight in zip(support, weights)]
        extra, value = _expectation_steps("g(X)", support, weights, function)
        return prefix, steps + extra, f"E[g(X)] = {prob_txt(value)}"

    @staticmethod
    def _var_shortcut():
        support, weights = _distribution()
        prefix = f"X has pmf: {_pmf_text(support, weights)}."
        steps = [step("WEIGHT", x, prob_txt(weight)) for x, weight in zip(support, weights)]
        extra, _, second, variance = _shortcut_steps(support, weights)
        answer = f"E[X²] = {prob_txt(second)}; Var(X) = {prob_txt(variance)}"
        return prefix, steps + extra, answer

    @staticmethod
    def _linear():
        support, weights = _distribution()
        a = random.choice([value for value in range(-6, 7) if value])
        b = random.randint(-12, 12)
        prefix = f"X has pmf: {_pmf_text(support, weights)}. Define {_affine_text(a, b)}."
        steps = [step("WEIGHT", x, prob_txt(weight)) for x, weight in zip(support, weights)]
        shortcut, mean, _, variance = _shortcut_steps(support, weights)
        steps.extend(shortcut)
        scaled_mean = a * mean
        transformed_mean = scaled_mean + b
        steps.append(step("M", a, prob_txt(mean), prob_txt(scaled_mean)))
        if b:
            steps.append(step("A" if b > 0 else "S", prob_txt(scaled_mean), abs(b),
                              prob_txt(transformed_mean)))
        a_square = a ** 2
        transformed_variance = a_square * variance
        steps.extend([step("E", a, 2, a_square),
                      step("M", a_square, prob_txt(variance),
                           prob_txt(transformed_variance)),
                      step("CHECK", "affine variance ignores shift",
                           prob_txt(transformed_variance))])
        answer = (f"E[Y] = {prob_txt(transformed_mean)}; "
                  f"Var(Y) = {prob_txt(transformed_variance)}")
        return prefix, steps, answer

    @staticmethod
    def _standardize():
        mean = random.randint(-100, 100)
        sigma = random.randint(1, 20)
        spread = random.randint(2, 8)
        support = (mean - spread * sigma, mean, mean + spread * sigma)
        tail = Fraction(1, 2 * spread * spread)
        weights = (tail, 1 - 2 * tail, tail)
        z = random.choice([value for value in range(-6, 7) if value])
        observation = mean + z * sigma
        prefix = (f"X has pmf: {_pmf_text(support, weights)}. Standardize "
                  f"x = {observation}.")
        steps = [step("WEIGHT", x, prob_txt(weight)) for x, weight in zip(support, weights)]
        shortcut, checked_mean, _, variance = _shortcut_steps(support, weights)
        steps.extend(shortcut)
        difference = observation - checked_mean
        steps.extend([step("ROOT", prob_txt(variance), 2, sigma),
                      step("S", observation, prob_txt(checked_mean),
                           prob_txt(difference)),
                      step("D", prob_txt(difference), sigma, z),
                      step("CHECK", "constructed exact standard deviation", sigma)])
        answer = f"μ = {prob_txt(checked_mean)}; σ = {sigma}; z = {z}"
        return prefix, steps, answer

    @staticmethod
    def _compare():
        support, weights = _distribution()
        prefix = f"X has pmf: {_pmf_text(support, weights)}."
        steps = [step("WEIGHT", x, prob_txt(weight)) for x, weight in zip(support, weights)]
        shortcut, mean, _, variance = _shortcut_steps(support, weights)
        direct_steps, direct = _definition_steps(support, weights, mean)
        steps.extend(shortcut + direct_steps)
        steps.append(step("CHECK", "shortcut equals definition",
                          prob_txt(variance), prob_txt(direct)))
        answer = (f"shortcut {prob_txt(variance)}; "
                  f"definition {prob_txt(direct)}")
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "e_g_x":
            prefix, steps, answer = self._e_g_x()
        elif variant == "var_shortcut":
            prefix, steps, answer = self._var_shortcut()
        elif variant == "linear_mean_var":
            prefix, steps, answer = self._linear()
        elif variant == "standardize":
            prefix, steps, answer = self._standardize()
        else:
            prefix, steps, answer = self._compare()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_expectation_function_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

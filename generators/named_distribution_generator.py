"""Compute supplied-constant and exact named-distribution quantities.

Variants: ``poisson``, ``exponential``, ``uniform``, ``normal``,
``exponential_memoryless``, and ``poisson_mode``. Transcendental values are
supplied in four-decimal form; uniform moments and Poisson modes stay exact.
Op-codes: ``DIST_SETUP``, ``LOOKUP_SUPPLIED``, ``POW``, ``FACT``,
``MODE_RULE``, ``FLOOR``, ``A``, ``S``, ``M``, ``D``, ``ROUND``, ``CHECK``,
and ``Z``.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, p4, prob_txt


PROBABILITY = True
EXP_VALUES = {1: "0.3679", 2: "0.1353", 3: "0.0498", 4: "0.0183"}
PHI_VALUES = {-2: "0.0228", -1: "0.1587", 0: "0.5000",
              1: "0.8413", 2: "0.9772"}
MODE_LAMBDAS = (Fraction(3, 2), Fraction(2), Fraction(5, 2), Fraction(3),
                Fraction(7, 2), Fraction(4), Fraction(9, 2), Fraction(5))
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
QUERIES = {
    "poisson": (
        "Find this Poisson point mass to four decimal places.",
        "Use the supplied exponential value in the Poisson formula.",
        "Compute the requested count probability from the supplied constant.",
        "Evaluate P(X=k) to four decimals.",
        "Combine the exponential, power, and factorial terms.",
    ),
    "exponential": (
        "Find this exponential cdf value to four decimal places.",
        "Use the complement of the supplied survival probability.",
        "Compute P(X<t) from the supplied exponential value.",
        "Evaluate the requested probability to four decimals.",
        "Subtract the supplied tail probability from one.",
    ),
    "uniform": (
        "Find the interval probability, mean, and variance exactly.",
        "Use uniform lengths and moment formulas.",
        "Compute all three requested quantities as reduced fractions.",
        "Evaluate the uniform probability and its two moments.",
        "Report the exact interval mass, center, and variance.",
    ),
    "normal": (
        "Read the supplied normal-table value to four decimal places.",
        "Standardize x and use the supplied Phi value.",
        "Find this normal probability from the provided lookup.",
        "Evaluate P(X<x) to four decimals.",
        "Compute the z-score, then read its supplied cumulative probability.",
    ),
    "exponential_memoryless": (
        "Verify exponential memorylessness with a composite equality.",
        "Use the two supplied survival values to compare conditional and fresh tails.",
        "Show that elapsed time does not change the remaining survival chance.",
        "Compute the conditional tail and its equal fresh-start probability.",
        "Evaluate both sides of the memoryless identity to four decimals.",
    ),
    "poisson_mode": (
        "Find the mode or tied modes of this Poisson distribution.",
        "Apply the exact Poisson mode rule.",
        "Identify every count that maximizes the point mass.",
        "Use floor(lambda), accounting for the integer-lambda tie.",
        "Report the most likely count or counts.",
    ),
}


def fraction_text(value):
    """Compatibility renderer retained for callers of the legacy helper."""
    return prob_txt(value)


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} studies a named distribution.")


def _exp_label(exponent):
    return f"e^(-{exponent})"


def _round(value):
    answer = p4(value)
    return step("ROUND", exact(value), "4 decimal places", answer), answer


class NamedDistributionGenerator(ProblemGenerator):
    """Generate Poisson, exponential, uniform, and normal exercises."""

    VARIANTS = ("poisson", "exponential", "uniform", "normal",
                "exponential_memoryless", "poisson_mode")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _poisson():
        lam = random.choice(tuple(EXP_VALUES))
        k = random.randint(0, 5)
        supplied = EXP_VALUES[lam]
        supplied_value = Fraction(supplied)
        power = lam ** k
        factorial = math.factorial(k)
        numerator = supplied_value * power
        probability = numerator / factorial
        rounded, value = _round(probability)
        problem = (f"{_context()} Distribution: Poisson with lambda={lam}. "
                   f"Supplied value: {_exp_label(lam)} = {supplied}. Target: "
                   f"P(X={k}) to 4 decimal places.")
        steps = [
            step("DIST_SETUP", "poisson", f"lambda={lam}", f"k={k}"),
            step("LOOKUP_SUPPLIED", _exp_label(lam), supplied),
            step("POW", f"base {lam}, exponent {k}", power),
            step("FACT", k, factorial),
            step("M", supplied, power, exact(numerator)),
            step("D", exact(numerator), factorial, exact(probability)),
            rounded,
            step("CHECK", "Poisson point mass lies in [0,1]", value),
        ]
        return problem, steps, f"P(X={k}) = {value}"

    @staticmethod
    def _exponential():
        exponent = random.choice(tuple(EXP_VALUES))
        supplied = EXP_VALUES[exponent]
        probability = 1 - Fraction(supplied)
        rounded, value = _round(probability)
        problem = (f"{_context()} Distribution: exponential with "
                   f"lambda*t={exponent}. Supplied value: e^(-lambda*t) = "
                   f"{supplied}. Target: P(X<t) to 4 decimal places.")
        steps = [
            step("DIST_SETUP", "exponential", f"lambda*t={exponent}",
                 "P(X<t)"),
            step("LOOKUP_SUPPLIED", "e^(-lambda*t)", supplied),
            step("S", 1, supplied, exact(probability)),
            rounded,
            step("CHECK", "cdf plus survival", 1),
        ]
        return problem, steps, f"P(X<t) = {value}"

    @staticmethod
    def _uniform():
        low = random.randint(-8, 5)
        high = low + random.randint(4, 14)
        left = random.randint(low, high - 1)
        right = random.randint(left + 1, high)
        width = high - low
        favorable = right - left
        probability = Fraction(favorable, width)
        mean_sum = low + high
        mean = Fraction(mean_sum, 2)
        width_square = width ** 2
        variance = Fraction(width_square, 12)
        problem = (f"{_context()} Distribution: Uniform({low},{high}). Target: "
                   f"P({left}<X<{right}), E[X], and Var(X).")
        steps = [
            step("DIST_SETUP", "uniform", f"[{low},{high}]",
                 f"interval=({left},{right})"),
            step("S", high, low, width),
            step("S", right, left, favorable),
            step("D", favorable, width, prob_txt(probability)),
            step("A", low, high, mean_sum),
            step("D", mean_sum, 2, prob_txt(mean)),
            step("POW", f"base {width}, exponent 2", width_square),
            step("D", width_square, 12, prob_txt(variance)),
            step("CHECK", "interval lies within support", "yes"),
        ]
        answer = (f"P = {prob_txt(probability)}; mean = {prob_txt(mean)}; "
                  f"variance = {prob_txt(variance)}")
        return problem, steps, answer

    @staticmethod
    def _normal():
        z = random.choice(tuple(PHI_VALUES))
        sigma = random.randint(1, 8)
        mu = random.randint(-8, 8)
        x_value = mu + z * sigma
        supplied = PHI_VALUES[z]
        problem = (f"{_context()} Distribution: Normal(mu={mu}, sigma={sigma}). "
                   f"Supplied value: Phi({z}) = {supplied}. Target: "
                   f"P(X<{x_value}) to 4 decimal places.")
        difference = x_value - mu
        steps = [
            step("DIST_SETUP", "normal", f"mu={mu}, sigma={sigma}",
                 f"x={x_value}"),
            step("S", x_value, mu, difference),
            step("D", difference, sigma, z),
            step("LOOKUP_SUPPLIED", f"Phi({z})", supplied),
            step("CHECK", f"z={z}", supplied),
        ]
        return problem, steps, f"P(X<{x_value}) = {supplied}"

    @staticmethod
    def _memoryless():
        first, second = random.sample(tuple(EXP_VALUES), 2)
        first_value = EXP_VALUES[first]
        second_value = EXP_VALUES[second]
        joint = Fraction(first_value) * Fraction(second_value)
        conditional = joint / Fraction(first_value)
        problem = (f"{_context()} Distribution: exponential. The scaled times "
                   f"s and t satisfy lambda*s={first} and lambda*t={second}. "
                   f"Supplied values: e^(-lambda*s) = {first_value}; "
                   f"e^(-lambda*t) = {second_value}. Target: "
                   f"P(X>s+t given X>s) and P(X>t), to 4 decimal places.")
        steps = [
            step("DIST_SETUP", "exponential memoryless",
                 f"lambda*s={first}, lambda*t={second}",
                 "conditional tail versus fresh tail"),
            step("LOOKUP_SUPPLIED", "e^(-lambda*s)", first_value),
            step("LOOKUP_SUPPLIED", "e^(-lambda*t)", second_value),
            step("M", first_value, second_value, exact(joint)),
            step("D", exact(joint), first_value, exact(conditional)),
            step("CHECK", "conditional tail equals fresh tail", second_value),
        ]
        answer = (f"P(X > s+t given X > s) = {second_value} = "
                  f"P(X > t)")
        return problem, steps, answer

    @staticmethod
    def _mode():
        lam = random.choice(MODE_LAMBDAS)
        floor_value = lam.numerator // lam.denominator
        problem = (f"{_context()} Distribution: Poisson with lambda="
                   f"{prob_txt(lam)}. Target: every mode of X.")
        steps = [
            step("DIST_SETUP", "poisson mode", f"lambda={prob_txt(lam)}",
                 "maximize P(X=k)"),
            step("MODE_RULE", "mode=floor(lambda); integer lambda also has lambda-1"),
            step("FLOOR", prob_txt(lam), floor_value),
        ]
        if lam.denominator == 1:
            lower = floor_value - 1
            steps.extend([
                step("S", floor_value, 1, lower),
                step("CHECK", "integer lambda gives adjacent tie",
                     f"k={lower} and k={floor_value}"),
            ])
            answer = f"modes = {lower} and {floor_value}"
        else:
            steps.append(step("CHECK", "noninteger lambda gives unique mode",
                              f"k={floor_value}"))
            answer = f"mode = {floor_value}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "poisson":
            problem, steps, answer = self._poisson()
        elif variant == "exponential":
            problem, steps, answer = self._exponential()
        elif variant == "uniform":
            problem, steps, answer = self._uniform()
        elif variant == "normal":
            problem, steps, answer = self._normal()
        elif variant == "exponential_memoryless":
            problem, steps, answer = self._memoryless()
        else:
            problem, steps, answer = self._mode()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"named_distribution_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

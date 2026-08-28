"""Compute exact probabilities and moments for uniform and Bernoulli laws.

Variants: ``uniform_interval_prob``, ``uniform_moments``, ``uniform_shift``,
``bernoulli_moments``, and ``indicator``. Op-codes: ``UNIF_SETUP``,
``UNIF_FORMULA``, ``DIST_SETUP``, ``EVENT``, ``PROB_SETUP``, ``EV_FORMULA``,
``VAR_FORMULA``, ``A``, ``S``, ``M``, ``D``, ``E``, ``F``, ``CHECK``, and
``Z``. Random supports, intervals, shifts, contexts, and five phrasings give
an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt, roster


PROBABILITY = True
CONTEXTS = ("alarm", "battery", "controller", "fan", "filter", "motor",
            "panel", "pump", "relay", "router", "sensor", "server",
            "switch", "valve", "wire", "compressor", "gateway", "module")
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal",
          "white", "yellow")
QUERIES = {
    "uniform_interval_prob": (
        "Find the probability that X lies in the target interval.",
        "Count the favorable integers and divide by the support size.",
        "What is the exact probability of the displayed interval event?",
        "Use the discrete uniform model to measure the target range.",
        "Determine the favorable-to-total ratio for this interval.",
    ),
    "uniform_moments": (
        "Find E[X] and Var(X).",
        "Compute the exact mean and variance of the discrete uniform variable.",
        "Use the endpoint and support-size formulas for both moments.",
        "What are the expectation and variance of X?",
        "Determine both uniform moments and verify the variance by definition.",
    ),
    "uniform_shift": (
        "Find E[Y] and Var(Y).",
        "Shift the mean and show that adding a constant leaves variance unchanged.",
        "Compute both exact moments of the translated variable Y.",
        "What are the expectation and variance after the stated shift?",
        "Use the moments of X to determine the moments of Y.",
    ),
    "bernoulli_moments": (
        "Find E[X] and Var(X) for this Bernoulli variable.",
        "Use p and 1 − p to compute both exact moments.",
        "What are the mean and variance of the success indicator?",
        "Apply the Bernoulli moment formulas and simplify.",
        "Determine E[X] and p(1 − p) from the stated success chance.",
    ),
    "indicator": (
        "Find E[I].",
        "Use the event probability to compute the indicator expectation.",
        "What is the exact mean of this zero-one variable?",
        "Count the die outcomes where I=1 and determine E[I].",
        "Apply E[I] = P(I=1) to the displayed event.",
    ),
}


def _uniform_data():
    start = random.randint(-100, 100)
    size = random.randint(3, 30)
    return start, start + size - 1, size


def _uniform_moment_steps(start, end, size):
    summed = start + end
    mean = Fraction(summed, 2)
    square = size ** 2
    numerator = square - 1
    variance = Fraction(numerator, 12)
    deviation = (f"x − {prob_txt(mean)}" if mean >= 0
                 else f"x + {prob_txt(-mean)}")
    steps = [step("UNIF_SETUP", f"X uniform on integers {start} through {end}",
                  f"n = {size}"),
             step("UNIF_FORMULA", "E[X] = (a + b)/2; Var(X) = (n² − 1)/12"),
             step("A", start, end, summed),
             step("D", summed, 2, prob_txt(mean)),
             step("E", size, 2, square),
             step("S", square, 1, numerator),
             step("D", numerator, 12, prob_txt(variance)),
             step("CHECK", "definition variance",
                  f"Σ({deviation})²/{size}", prob_txt(variance))]
    return steps, mean, variance


def _fraction_steps(numerator, denominator):
    value = Fraction(numerator, denominator)
    raw = f"{numerator}/{denominator}"
    steps = [step("PROB_SETUP", numerator, denominator)]
    if raw != prob_txt(value):
        steps.append(step("F", raw, prob_txt(value)))
    return steps, value


class DiscreteUniformBernoulliGenerator(ProblemGenerator):
    """Generate exact finite uniform and Bernoulli exercises."""

    VARIANTS = ("uniform_interval_prob", "uniform_moments", "uniform_shift",
                "bernoulli_moments", "indicator")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _interval():
        start, end, size = _uniform_data()
        left = random.randint(start, end)
        right = random.randint(left, end)
        favorable = right - left + 1
        prefix = (f"X is discrete uniform on the integers {start} through {end}. "
                  f"Target interval: {left} through {right}.")
        steps = [step("UNIF_SETUP", f"X uniform on integers {start} through {end}",
                      f"n = {size}"),
                 step("EVENT", f"{left} ≤ X ≤ {right}",
                      roster(range(left, right + 1)), favorable)]
        extra, value = _fraction_steps(favorable, size)
        return prefix, steps + extra, prob_txt(value)

    @staticmethod
    def _moments():
        start, end, size = _uniform_data()
        prefix = f"X is discrete uniform on the integers {start} through {end}."
        steps, mean, variance = _uniform_moment_steps(start, end, size)
        answer = f"E[X] = {prob_txt(mean)}; Var(X) = {prob_txt(variance)}"
        return prefix, steps, answer

    @staticmethod
    def _shift():
        start, end, size = _uniform_data()
        shift = random.choice([value for value in range(-20, 21) if value])
        if shift > 0:
            definition = f"Y = X + {shift}"
        else:
            definition = f"Y = X − {abs(shift)}"
        prefix = (f"X is discrete uniform on the integers {start} through {end}. "
                  f"Define {definition}.")
        steps, mean, variance = _uniform_moment_steps(start, end, size)
        shifted_mean = mean + shift
        code = "A" if shift > 0 else "S"
        steps.append(step(code, prob_txt(mean), abs(shift), prob_txt(shifted_mean)))
        steps.append(step("CHECK", "translation variance", prob_txt(variance),
                          prob_txt(variance)))
        answer = (f"E[Y] = {prob_txt(shifted_mean)}; "
                  f"Var(Y) = {prob_txt(variance)}")
        return prefix, steps, answer

    @staticmethod
    def _bernoulli():
        denominator = random.randint(3, 100)
        probability = Fraction(random.randint(1, denominator - 1), denominator)
        context = random.choice(CONTEXTS)
        failure = 1 - probability
        variance = probability * failure
        prefix = (f"For the {context}, X is 1 on success and 0 on failure. "
                  f"The success probability is {prob_txt(probability)}.")
        steps = [step("DIST_SETUP", "Bernoulli", f"p = {prob_txt(probability)}"),
                 step("EV_FORMULA", "E[X] = p", prob_txt(probability)),
                 step("S", 1, prob_txt(probability), prob_txt(failure)),
                 step("VAR_FORMULA", "Var(X) = p(1 − p)"),
                 step("M", prob_txt(probability), prob_txt(failure),
                      prob_txt(variance)),
                 step("CHECK", "definition over {0, 1}", prob_txt(variance))]
        answer = (f"E[X] = {prob_txt(probability)}; "
                  f"Var(X) = {prob_txt(variance)}")
        return prefix, steps, answer

    @staticmethod
    def _indicator():
        sides = random.randint(6, 50)
        color = random.choice(COLORS)
        kind = random.choice(("even", "at_least", "multiple"))
        outcomes = tuple(range(1, sides + 1))
        if kind == "even":
            description = "the roll is even"
            event = tuple(value for value in outcomes if value % 2 == 0)
        elif kind == "at_least":
            cutoff = random.randint(2, sides)
            description = f"the roll is at least {cutoff}"
            event = tuple(value for value in outcomes if value >= cutoff)
        else:
            divisor = random.randint(2, min(12, sides))
            description = f"the roll is a multiple of {divisor}"
            event = tuple(value for value in outcomes if value % divisor == 0)
        value = Fraction(len(event), sides)
        prefix = (f"A fair {color} {sides}-sided die with faces 1 through {sides} "
                  f"is rolled. I=1 when {description}, and I=0 otherwise.")
        steps = [step("EVENT", "I=1", roster(event), len(event))]
        extra, _ = _fraction_steps(len(event), sides)
        steps.extend(extra)
        steps.extend([step("EV_FORMULA", "E[I] = P(I=1)", prob_txt(value)),
                      step("CHECK", "zero outcome contributes nothing",
                           f"1 × {prob_txt(value)}",
                           prob_txt(value))])
        return prefix, steps, f"E[I] = {prob_txt(value)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "uniform_interval_prob":
            prefix, steps, answer = self._interval()
        elif variant == "uniform_moments":
            prefix, steps, answer = self._moments()
        elif variant == "uniform_shift":
            prefix, steps, answer = self._shift()
        elif variant == "bernoulli_moments":
            prefix, steps, answer = self._bernoulli()
        else:
            prefix, steps, answer = self._indicator()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_discrete_uniform_bernoulli_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

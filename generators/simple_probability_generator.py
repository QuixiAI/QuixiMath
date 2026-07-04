import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class SimpleProbabilityGenerator(ProblemGenerator):
    """Single-event probability with uniform outcomes.

    The answer is the exact reduced fraction (2/6 -> 1/3), never a
    rounded decimal; degenerate certainties (favorable == total) are
    excluded.
    """

    def generate(self) -> dict:
        total = random.randint(3, 24)
        favorable = random.randint(1, total - 1)
        operation = "probability_simple"
        problem = f"If an event has {favorable} favorable outcomes out of {total} equally likely outcomes, what is P?"

        prob = Fraction(favorable, total)
        final_answer = f"{prob.numerator}/{prob.denominator}"

        steps = []
        steps.append(step("PROB_SETUP", favorable, total))
        if prob.denominator != total:
            steps.append(step("F", f"{favorable}/{total}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

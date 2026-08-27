import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


PLACES = [
    "classroom", "game club", "science lab", "training center",
    "statistics workshop", "school fair", "library", "museum activity",
    "research lab", "learning center", "math club", "survey office",
    "community center", "technical college", "study hall", "robotics lab",
    "design studio", "field station", "tutoring center", "computer lab",
]

CONTEXTS = [
    "At the {place}, a single-event model is being checked.",
    "A worksheet from the {place} gives this probability setup.",
    "During an activity at the {place}, the following event is studied.",
    "An exercise used by the {place} specifies these outcome counts.",
]


class SimpleProbabilityGenerator(ProblemGenerator):
    """Single-event probability with uniform outcomes.

    The answer is the exact reduced fraction (2/6 -> 1/3), never a
    rounded decimal; degenerate certainties (favorable == total) are
    excluded.
    """

    def generate(self) -> dict:
        total = random.randint(3, 200)
        favorable = random.randint(1, total - 1)
        operation = "probability_simple"
        context = random.choice(CONTEXTS).format(place=random.choice(PLACES))
        problem = (f"{context} If an event has {favorable} favorable outcomes "
                   f"out of {total} equally likely outcomes, what is P?")

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

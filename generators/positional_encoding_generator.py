import random

from base_generator import ProblemGenerator
from helpers import step, jid


ANGLE_TABLE = [
    ("0", "0", "1"),
    ("pi/6", "1/2", "sqrt(3)/2"),
    ("pi/4", "sqrt(2)/2", "sqrt(2)/2"),
    ("pi/3", "sqrt(3)/2", "1/2"),
    ("pi/2", "1", "0"),
    ("2pi/3", "sqrt(3)/2", "-1/2"),
    ("3pi/4", "sqrt(2)/2", "-sqrt(2)/2"),
    ("5pi/6", "1/2", "-sqrt(3)/2"),
    ("pi", "0", "-1"),
    ("3pi/2", "-1", "0"),
]


def vector_text(values):
    return "(" + ",".join(values) + ")"


class PositionalEncodingGenerator(ProblemGenerator):
    """
    Sinusoidal positional encoding at exact nice angles.

    Uses the d=2 encoding PE(theta) = (sin(theta), cos(theta)) with a provided
    angle from the unit-circle table.

    Op-codes used:
    - PE_SETUP / ANGLE / SIN / COS / PE_ENTRY
    - Z: exact positional encoding vector
    """

    def generate(self) -> dict:
        position = random.randint(0, 240)
        angle, sin_value, cos_value = random.choice(ANGLE_TABLE)
        steps = [
            step("PE_SETUP", f"position={position}", "d=2",
                 f"theta={angle}"),
            step("ANGLE", "theta", angle),
            step("SIN", angle, sin_value),
            step("PE_ENTRY", 0, sin_value),
            step("COS", angle, cos_value),
            step("PE_ENTRY", 1, cos_value),
        ]
        answer = f"PE={vector_text((sin_value, cos_value))}"
        steps.append(step("Z", answer))
        problem = (
            f"At position p={position}, the sinusoidal encoding angle is "
            f"theta={angle}. Compute the d=2 positional encoding "
            "PE=(sin(theta), cos(theta))."
        )
        return dict(
            problem_id=jid(),
            operation="positional_encoding_2d",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

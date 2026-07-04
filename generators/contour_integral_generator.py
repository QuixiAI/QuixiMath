import random

from base_generator import ProblemGenerator
from helpers import step, jid


def z_minus(a):
    if a == 0:
        return "z"
    if a > 0:
        return f"(z-{a})"
    return f"(z+{-a})"


def term_text(residue, pole):
    return f"{abs(residue)}/{z_minus(pole)}"


def function_text(residues, poles):
    parts = []
    for residue, pole in zip(residues, poles):
        text = term_text(residue, pole)
        if not parts:
            parts.append(text if residue > 0 else f"-{text}")
        else:
            parts.append(f"+ {text}" if residue > 0 else f"- {text}")
    return " ".join(parts)


def integral_text(residue_sum):
    if residue_sum == 0:
        return "0"
    coef = 2 * residue_sum
    if coef == 1:
        return "pi i"
    if coef == -1:
        return "-pi i"
    return f"{coef}pi i"


class ContourIntegralGenerator(ProblemGenerator):
    """
    Contour integrals by the residue theorem over positively oriented
    circles centered at the origin.

    Op-codes used:
    - CONTOUR_SETUP / POLE_TEST: contour and pole inclusion
    - RESIDUE / RESIDUE_SUM: residue bookkeeping
    - A / M (established/shared): sum residues and multiply by 2
    - Z: contour integral value
    """

    def generate(self) -> dict:
        radius = random.randint(2, 7)
        poles = random.sample([v for v in range(-8, 9) if v != 0], 3)
        residues = [random.choice([v for v in range(-6, 7) if v != 0])
                    for _ in poles]
        function = function_text(residues, poles)
        steps = [
            step("CONTOUR_SETUP", f"abs(z)={radius}", "positive orientation",
                 f"f={function}"),
        ]
        residue_sum = 0
        for pole, residue in zip(poles, residues):
            inside = abs(pole) < radius
            verdict = "inside" if inside else "outside"
            steps.append(step("POLE_TEST", f"pole {pole}",
                              f"abs({pole}) < {radius}", verdict))
            steps.append(step("RESIDUE", f"pole {pole}", residue, verdict))
            if inside:
                new_sum = residue_sum + residue
                steps.append(step("A", residue_sum, residue, new_sum))
                residue_sum = new_sum
        steps.append(step("RESIDUE_SUM", residue_sum))
        coefficient = 2 * residue_sum
        steps.append(step("M", 2, residue_sum, coefficient))
        answer = f"integral = {integral_text(residue_sum)}"
        problem = (
            f"Evaluate the positively oriented contour integral over |z|="
            f"{radius} of f(z) = {function}."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="contour_integral_residue_theorem",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

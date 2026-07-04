import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


def eq_txt(a, b, e):
    """'3x + 2y = 8' with unit coefficients hidden."""
    ax = {1: "x", -1: "-x"}.get(a, f"{a}x")
    by = f"+ {'y' if b == 1 else str(b) + 'y'}" if b > 0 \
        else f"- {'y' if b == -1 else str(-b) + 'y'}"
    return f"{ax} {by} = {e}"


class CramersRuleGenerator(ProblemGenerator):
    """
    2×2 linear systems by Cramer's rule: the coefficient determinant D
    (checked nonzero), the column-replaced determinants Dx and Dy each
    worked in full, and the two divisions. Systems are built from an
    integer solution so the quotients are exact.

    Op-codes used:
    - EQ_SETUP / DET_FORMULA / CHECK (established)
    - M / S / D: determinant work and the divisions (established)
    - REWRITE: each column-replaced matrix (established)
    - EVAL: D, Dx, Dy (established)
    - Z: 'x = ..., y = ...'
    """

    def generate(self) -> dict:
        while True:
            a, b, c, d = (random.choice(
                [v for v in range(-6, 7) if v != 0]) for _ in range(4))
            D = a * d - b * c
            if D != 0:
                break
        x0 = random.randint(-6, 6)
        y0 = random.randint(-6, 6)
        e = a * x0 + b * y0
        f = c * x0 + d * y0
        Dx = e * d - b * f
        Dy = a * f - e * c

        system = f"{eq_txt(a, b, e)}; {eq_txt(c, d, f)}"
        steps = [
            step("EQ_SETUP", system, "solve by Cramer's rule"),
            step("DET_FORMULA",
                 f"D = det {mat([[a, b], [c, d]])}"),
            step("M", a, d, a * d),
            step("M", b, c, b * c),
            step("S", a * d, b * c, D),
            step("EVAL", "D", D),
            step("CHECK", "solvable", f"D = {D} ≠ 0",
                 "unique solution"),
            step("REWRITE",
                 f"Dx: replace the x-column with the constants: "
                 f"{mat([[e, b], [f, d]])}"),
            step("M", e, d, e * d),
            step("M", b, f, b * f),
            step("S", e * d, b * f, Dx),
            step("EVAL", "Dx", Dx),
            step("REWRITE",
                 f"Dy: replace the y-column with the constants: "
                 f"{mat([[a, e], [c, f]])}"),
            step("M", a, f, a * f),
            step("M", e, c, e * c),
            step("S", a * f, e * c, Dy),
            step("EVAL", "Dy", Dy),
            step("D", Dx, D, x0),
            step("D", Dy, D, y0),
        ]
        answer = f"x = {x0}, y = {y0}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="cramers_rule",
            problem=(f"Solve the system using Cramer's rule: "
                     f"{system}."),
            steps=steps,
            final_answer=answer,
        )

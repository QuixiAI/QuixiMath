import random

from base_generator import ProblemGenerator
from helpers import step, jid


class SimplexGenerator(ProblemGenerator):
    """
    Two-pivot simplex tableau for a bounded two-variable LP.

    Op-codes used:
    - SIMPLEX_SETUP: objective and constraints
    - TABLEAU: tableau rows at each stage
    - ENTER: entering variable choice
    - RATIO: minimum-ratio test
    - PIVOT: pivot element
    - ROW_OP: tableau row operation
    - M / A / D (established/shared): exact arithmetic
    - CHECK: optimality check
    - Z: optimal point and objective value
    """

    def generate(self) -> dict:
        x_bound = random.randint(2, 25)
        y_bound = random.randint(2, 25)
        c1 = random.randint(4, 18)
        c2 = random.randint(1, c1 - 1)
        zx = c1 * x_bound
        zy = c2 * y_bound
        z_value = zx + zy

        steps = [
            step("SIMPLEX_SETUP", f"max z={c1}x+{c2}y",
                 f"x<={x_bound}", f"y<={y_bound}"),
            step("TABLEAU", "initial",
                 f"s1: x + s1 = {x_bound}",
                 f"s2: y + s2 = {y_bound}"),
            step("TABLEAU", "z row", f"-{c1}x - {c2}y + z = 0"),
            step("ENTER", "x", f"most negative reduced cost -{c1}"),
            step("D", x_bound, 1, x_bound),
            step("RATIO", "s1 row", f"{x_bound}/1", x_bound),
            step("PIVOT", "row=s1", "column=x", "pivot=1"),
            step("ROW_OP", f"z <- z + {c1}*s1"),
            step("M", c1, x_bound, zx),
            step("TABLEAU", "after x pivot",
                 f"x={x_bound} - s1",
                 f"z row: -{c2}y + {c1}s1 + z = {zx}"),
            step("ENTER", "y", f"remaining negative reduced cost -{c2}"),
            step("D", y_bound, 1, y_bound),
            step("RATIO", "s2 row", f"{y_bound}/1", y_bound),
            step("PIVOT", "row=s2", "column=y", "pivot=1"),
            step("ROW_OP", f"z <- z + {c2}*s2"),
            step("M", c2, y_bound, zy),
            step("A", zx, zy, z_value),
            step("TABLEAU", "final",
                 f"x={x_bound}, y={y_bound}",
                 f"z={z_value}"),
            step("CHECK", "reduced costs for x,y are 0",
                 "optimal tableau"),
        ]
        answer = f"x={x_bound}, y={y_bound}, max z={z_value}"
        steps.append(step("Z", answer))
        problem = (
            f"Use the simplex method to maximize z = {c1}x + {c2}y "
            f"subject to x <= {x_bound}, y <= {y_bound}, x >= 0, y >= 0."
        )
        return dict(
            problem_id=jid(),
            operation="simplex_two_variable_tableau",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

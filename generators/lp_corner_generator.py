import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.systems_elimination_generator import coeff_term


def vertex_text(x_value, y_value):
    return f"({x_value},{y_value})"


def objective_value(c1, c2, vertex):
    x_value, y_value = vertex
    return c1 * x_value + c2 * y_value


class LPCornerGenerator(ProblemGenerator):
    """
    Corner-point method for a two-variable linear program.

    Op-codes used:
    - LP_CORNER_SETUP: objective and inequalities
    - VERTEX_SOLVE: pair of boundary equations being solved
    - VERTEX: feasible corner point
    - OBJECTIVE: objective evaluation at a vertex
    - S / M / A (established/shared): exact arithmetic
    - CHECK: selected maximum
    - Z: optimal vertex and objective value
    """

    def generate(self) -> dict:
        while True:
            x_bound = random.randint(3, 24)
            y_bound = random.randint(3, 24)
            diagonal = random.randint(max(x_bound, y_bound) + 1,
                                      x_bound + y_bound - 1)
            c1 = random.randint(1, 15)
            c2 = random.randint(1, 15)
            vertices = [
                (0, 0),
                (x_bound, 0),
                (x_bound, diagonal - x_bound),
                (diagonal - y_bound, y_bound),
                (0, y_bound),
            ]
            values = [objective_value(c1, c2, vertex) for vertex in vertices]
            if values.count(max(values)) == 1:
                break

        y_on_right = diagonal - x_bound
        x_on_top = diagonal - y_bound
        best_index = values.index(max(values))
        best_vertex = vertices[best_index]
        best_value = values[best_index]

        steps = [
            step("LP_CORNER_SETUP", f"max z={coeff_term(c1, 'x')}+{coeff_term(c2, 'y')}",
                 f"0<=x<={x_bound}, 0<=y<={y_bound}",
                 f"x+y<={diagonal}"),
            step("VERTEX_SOLVE", "x=0", "y=0"),
            step("VERTEX", vertex_text(0, 0)),
            step("VERTEX_SOLVE", f"x={x_bound}", "y=0"),
            step("VERTEX", vertex_text(x_bound, 0)),
            step("VERTEX_SOLVE", f"x={x_bound}",
                 f"x+y={diagonal}"),
            step("S", diagonal, x_bound, y_on_right),
            step("VERTEX", vertex_text(x_bound, y_on_right)),
            step("VERTEX_SOLVE", f"y={y_bound}",
                 f"x+y={diagonal}"),
            step("S", diagonal, y_bound, x_on_top),
            step("VERTEX", vertex_text(x_on_top, y_bound)),
            step("VERTEX_SOLVE", "x=0", f"y={y_bound}"),
            step("VERTEX", vertex_text(0, y_bound)),
        ]
        for vertex, value in zip(vertices, values):
            x_value, y_value = vertex
            x_term = c1 * x_value
            y_term = c2 * y_value
            steps += [
                step("OBJECTIVE", f"at {vertex_text(x_value, y_value)}"),
                step("M", c1, x_value, x_term),
                step("M", c2, y_value, y_term),
                step("A", x_term, y_term, value),
            ]
        steps.append(step("CHECK", f"max value {best_value}",
                          f"at {vertex_text(*best_vertex)}"))
        answer = (
            f"optimal vertex={vertex_text(*best_vertex)}, "
            f"max z={best_value}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Use the corner-point method to maximize z = {coeff_term(c1, 'x')} + {coeff_term(c2, 'y')} "
            f"subject to 0 <= x <= {x_bound}, 0 <= y <= {y_bound}, "
            f"and x + y <= {diagonal}."
        )
        return dict(
            problem_id=jid(),
            operation="lp_corner_point",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

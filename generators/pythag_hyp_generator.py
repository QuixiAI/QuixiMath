from base_generator import ProblemGenerator
from helpers import step, jid
from generators.pythagorean_common import (
    random_scaled_triple,
    triangle_labels,
)

class PythagHypGenerator(ProblemGenerator):
    """Generates Pythagorean theorem problems (finding hypotenuse)."""

    def generate(self) -> dict:
        operation = "pythag_hyp"
        a, b, c_ans = random_scaled_triple()
        vertex_a, vertex_b, vertex_c = triangle_labels()
        leg_one = f"{vertex_a}{vertex_b}"
        leg_two = f"{vertex_b}{vertex_c}"
        hypotenuse = f"{vertex_a}{vertex_c}"
        problem = (
            f"In right triangle {vertex_a}{vertex_b}{vertex_c}, "
            f"{leg_one} and {leg_two} are perpendicular legs of lengths "
            f"{a} and {b}. Find hypotenuse {hypotenuse}."
        )

        a_sq = a * a
        b_sq = b * b
        sum_sq = a_sq + b_sq
        final_answer_str = str(c_ans)

        steps = [
            step("PYTHAG_SETUP", f"legs={a},{b}",
                 f"hypotenuse {hypotenuse}=?"),
            step("PYTHAG_FORMULA", "a² + b² = c²"),
            step("E", a, 2, a_sq),      # Square leg a
            step("E", b, 2, b_sq),      # Square leg b
            step("A", a_sq, b_sq, sum_sq), # Add squares
            step("ROOT", sum_sq, c_ans) # Square root of sum
        ]
        steps.append(step("Z", final_answer_str)) # Final answer step

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer_str
        )

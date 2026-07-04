import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["vector_norms", "frobenius_norm", "spectral_condition"]
PYTHAGOREAN = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def abs_step_value(value):
    return abs(value)


def perfect_square_matrix():
    for _ in range(200):
        matrix = [
            [random.randint(-6, 6), random.randint(-6, 6)],
            [random.randint(-6, 6), random.randint(-6, 6)],
        ]
        square_sum = sum(value * value for row in matrix for value in row)
        root = math.isqrt(square_sum)
        if square_sum and root * root == square_sum:
            return matrix, root
    return [[1, 2], [2, 4]], 5


class MatrixNormGenerator(ProblemGenerator):
    """
    Vector and matrix norms with exact square roots.

    Variants:
    - vector_norms: L1, L2, and Linf norms for a 2D vector.
    - frobenius_norm: Frobenius norm of a 2x2 matrix.
    - spectral_condition: spectral norm and 2-norm condition number for a
      diagonal 2x2 matrix via eigenvalues of A^T A.

    Op-codes used:
    - NORM_SETUP / ABS / MAX / MIN / ROOT / EIGENVALUES
    - A / E / D (established/shared): sums, squares, and ratios
    - Z: requested norms
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "vector_norms":
            problem, steps, answer = self._generate_vector_norms()
        elif variant == "frobenius_norm":
            problem, steps, answer = self._generate_frobenius_norm()
        else:
            problem, steps, answer = self._generate_spectral_condition()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"matrix_norm_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_vector_norms(self):
        a, b, hyp = random.choice(PYTHAGOREAN)
        scale = random.randint(1, 3)
        signs = [random.choice([-1, 1]), random.choice([-1, 1])]
        vector = [signs[0] * scale * a, signs[1] * scale * b]
        abs_values = [abs_step_value(value) for value in vector]
        l1 = sum(abs_values)
        linf = max(abs_values)
        square0 = vector[0] ** 2
        square1 = vector[1] ** 2
        square_sum = square0 + square1
        l2 = scale * hyp
        steps = [
            step("NORM_SETUP", f"v={vector_text(vector)}", "vector norms"),
        ]
        for value, abs_value in zip(vector, abs_values):
            steps.append(step("ABS", value, abs_value))
        steps.extend([
            step("A", abs_values[0], abs_values[1], l1),
            step("E", vector[0], 2, square0),
            step("E", vector[1], 2, square1),
            step("A", square0, square1, square_sum),
            step("ROOT", f"sqrt({square_sum})", l2),
            step("MAX", f"{abs_values[0]},{abs_values[1]}", linf),
        ])
        answer = f"L1={l1}; L2={l2}; Linf={linf}"
        problem = (
            f"For vector v={vector_text(vector)}, compute the L1, L2, "
            "and Linf norms."
        )
        return problem, steps, answer

    def _generate_frobenius_norm(self):
        matrix, root = perfect_square_matrix()
        steps = [
            step("NORM_SETUP", f"A={matrix_text(matrix)}", "Frobenius norm"),
        ]
        running = 0
        for row in matrix:
            for value in row:
                square = value ** 2
                new_running = running + square
                steps.append(step("E", value, 2, square))
                steps.append(step("A", running, square, new_running))
                running = new_running
        steps.append(step("ROOT", f"sqrt({running})", root))
        answer = f"Frobenius={root}"
        problem = f"For matrix A={matrix_text(matrix)}, compute the Frobenius norm."
        return problem, steps, answer

    def _generate_spectral_condition(self):
        first = random.choice([value for value in range(-9, 10) if value])
        second = random.choice([value for value in range(-9, 10)
                                if value and abs(value) != abs(first)])
        matrix = [[first, 0], [0, second]]
        first_sq = first ** 2
        second_sq = second ** 2
        lambda_max = max(first_sq, second_sq)
        lambda_min = min(first_sq, second_sq)
        sigma_max = math.isqrt(lambda_max)
        sigma_min = math.isqrt(lambda_min)
        cond = Fraction(sigma_max, sigma_min)
        steps = [
            step("NORM_SETUP", f"A={matrix_text(matrix)}",
                 "spectral norm and condition"),
            step("E", first, 2, first_sq),
            step("E", second, 2, second_sq),
            step("EIGENVALUES", "A^T A", f"{first_sq},{second_sq}"),
            step("MAX", f"{first_sq},{second_sq}", lambda_max),
            step("MIN", f"{first_sq},{second_sq}", lambda_min),
            step("ROOT", f"sqrt({lambda_max})", sigma_max),
            step("ROOT", f"sqrt({lambda_min})", sigma_min),
            step("D", sigma_max, sigma_min, fraction_text(cond)),
        ]
        answer = f"spectral={sigma_max}; cond={fraction_text(cond)}"
        problem = (
            f"For diagonal matrix A={matrix_text(matrix)}, compute the "
            "spectral norm and 2-norm condition number."
        )
        return problem, steps, answer

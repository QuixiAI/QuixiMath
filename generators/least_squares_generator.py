import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


def line_txt(a, b):
    if b == 0:
        return f"ŷ = {a}"
    mag = "x" if abs(b) == 1 else f"{abs(b)}x"
    if a == 0:
        return f"ŷ = {mag}" if b > 0 else f"ŷ = -{mag}"
    return f"ŷ = {a} + {mag}" if b > 0 else f"ŷ = {a} - {mag}"


def points_txt(xs, ys):
    return "[" + ", ".join(f"({x}, {y})" for x, y in zip(xs, ys)) + "]"


def design_matrix(xs):
    return [[1, x] for x in xs]


def normal_parts(xs, ys):
    n = len(xs)
    sum_x = sum(xs)
    sum_x2 = sum(x * x for x in xs)
    sum_y = sum(ys)
    sum_xy = sum(x * y for x, y in zip(xs, ys))
    return [[n, sum_x], [sum_x, sum_x2]], [sum_y, sum_xy]


def dot_cols_with_vector(X, r):
    return [
        sum(row[col] * r[i] for i, row in enumerate(X))
        for col in range(len(X[0]))
    ]


class LeastSquaresGenerator(ProblemGenerator):
    """
    Least-squares line fitting by normal equations. Centered x-values make
    X^T X diagonal, and residuals are constructed orthogonal to the columns of
    X so the fitted line, projection, and residual are exact integers.

    Variants: three_point_line and four_point_line.

    Op-codes used:
    - LS_SETUP: points and model
    - DESIGN_MATRIX: X and y
    - NORMAL_EQ: X^T X and X^T y
    - D (established): solve diagonal normal equations
    - LS_LINE: fitted coefficients and line
    - PROJECTION: X*beta
    - RESIDUAL: y - projection
    - CHECK (established): X^T residual equals zero
    - Z: line, projection, and residual
    """

    VARIANTS = ["three_point_line", "four_point_line"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _data(variant):
        if variant == "three_point_line":
            xs = [-1, 0, 1]
            residual_shape = [1, -2, 1]
        else:
            xs = [-3, -1, 1, 3]
            residual_shape = [1, -1, -1, 1]
        a = random.randint(5, 20)
        b = random.choice([-3, -2, -1, 1, 2, 3])
        t = random.choice([-3, -2, -1, 1, 2, 3])
        yhat = [a + b * x for x in xs]
        residual = [t * value for value in residual_shape]
        ys = [yh + r for yh, r in zip(yhat, residual)]
        return xs, ys, a, b, yhat, residual

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        xs, ys, a, b, yhat, residual = self._data(variant)
        X = design_matrix(xs)
        xtx, xty = normal_parts(xs, ys)
        check = dot_cols_with_vector(X, residual)
        assert check == [0, 0]

        steps = [
            step("LS_SETUP", f"points {points_txt(xs, ys)}",
                 "model y = a + bx"),
            step("DESIGN_MATRIX", f"X = {mat(X)}", f"y = {ys}"),
            step("NORMAL_EQ", "X^T X", mat(xtx)),
            step("NORMAL_EQ", "X^T y", str(xty)),
            step("D", xty[0], xtx[0][0], a),
            step("D", xty[1], xtx[1][1], b),
            step("LS_LINE", f"a = {a}, b = {b}", line_txt(a, b)),
            step("PROJECTION", "X*beta", str(yhat)),
            step("RESIDUAL", "y - X*beta", str(residual)),
            step("CHECK", "X^T residual", str(check), "orthogonal"),
        ]
        answer = (f"{line_txt(a, b)}; projection {yhat}; "
                  f"residual {residual}")
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"least_squares_{variant}",
            problem=(f"Use normal equations to find the least-squares line "
                     f"y = a + bx for points {points_txt(xs, ys)}."),
            steps=steps,
            final_answer=answer,
        )

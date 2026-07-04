import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def pair_text(pairs):
    return "[" + ", ".join(f"({x},{y})" for x, y in pairs) + "]"


def vector_text(vector):
    return "(" + ",".join(fraction_text(value) for value in vector) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


class KernelRidgeGenerator(ProblemGenerator):
    """
    Kernel ridge regression with a linear kernel on two training points.

    The generator forms K, solves (K + lambda I) alpha = y by the exact 2x2
    inverse formula, then predicts f(x*) = k(x*, X)^T alpha.

    Op-codes used:
    - KRR_SETUP / KERNEL_VALUE / RIDGE_ENTRY / DET / ALPHA / PREDICT
    - M / A / S / D (established/shared): matrix entries, solve, prediction
    - Z: exact alpha vector and prediction
    """

    def generate(self) -> dict:
        xs = random.sample([value for value in range(-6, 7) if value != 0], 2)
        ys = [random.randint(-6, 6), random.randint(-6, 6)]
        lam = random.choice([1, 2, 3])
        x_star = random.choice([value for value in range(-6, 7)
                                if value != 0])
        data = list(zip(xs, ys))
        k11 = xs[0] * xs[0]
        k12 = xs[0] * xs[1]
        k21 = xs[1] * xs[0]
        k22 = xs[1] * xs[1]
        gram = [[k11, k12], [k21, k22]]
        a = k11 + lam
        b = k12
        c = k21
        d = k22 + lam
        ridge = [[a, b], [c, d]]
        ad = a * d
        bc = b * c
        det = ad - bc
        d_y1 = d * ys[0]
        b_y2 = b * ys[1]
        num1 = d_y1 - b_y2
        a_y2 = a * ys[1]
        c_y1 = c * ys[0]
        num2 = a_y2 - c_y1
        alpha1 = Fraction(num1, det)
        alpha2 = Fraction(num2, det)
        k_star1 = x_star * xs[0]
        k_star2 = x_star * xs[1]
        term1 = k_star1 * alpha1
        term2 = k_star2 * alpha2
        prediction = term1 + term2

        steps = [
            step("KRR_SETUP", "kernel=linear",
                 f"data={pair_text(data)}", f"lambda={lam},x*={x_star}"),
            step("M", xs[0], xs[0], k11),
            step("KERNEL_VALUE", "1,1", k11),
            step("M", xs[0], xs[1], k12),
            step("KERNEL_VALUE", "1,2", k12),
            step("M", xs[1], xs[0], k21),
            step("KERNEL_VALUE", "2,1", k21),
            step("M", xs[1], xs[1], k22),
            step("KERNEL_VALUE", "2,2", k22),
            step("RIDGE_ENTRY", "K", matrix_text(gram)),
            step("A", k11, lam, a),
            step("RIDGE_ENTRY", "1,1", a),
            step("RIDGE_ENTRY", "1,2", b),
            step("RIDGE_ENTRY", "2,1", c),
            step("A", k22, lam, d),
            step("RIDGE_ENTRY", "2,2", d),
            step("RIDGE_ENTRY", "K+lambdaI", matrix_text(ridge)),
            step("M", a, d, ad),
            step("M", b, c, bc),
            step("S", ad, bc, det),
            step("DET", "K+lambdaI", det),
            step("M", d, ys[0], d_y1),
            step("M", b, ys[1], b_y2),
            step("S", d_y1, b_y2, num1),
            step("D", num1, det, fraction_text(alpha1)),
            step("ALPHA", "alpha1", fraction_text(alpha1)),
            step("M", a, ys[1], a_y2),
            step("M", c, ys[0], c_y1),
            step("S", a_y2, c_y1, num2),
            step("D", num2, det, fraction_text(alpha2)),
            step("ALPHA", "alpha2", fraction_text(alpha2)),
            step("M", x_star, xs[0], k_star1),
            step("KERNEL_VALUE", "x*,1", k_star1),
            step("M", x_star, xs[1], k_star2),
            step("KERNEL_VALUE", "x*,2", k_star2),
            step("M", k_star1, fraction_text(alpha1), fraction_text(term1)),
            step("M", k_star2, fraction_text(alpha2), fraction_text(term2)),
            step("A", fraction_text(term1), fraction_text(term2),
                 fraction_text(prediction)),
            step("PREDICT", "x*", fraction_text(prediction)),
        ]
        answer = (
            f"alpha={vector_text((alpha1, alpha2))}; "
            f"prediction={fraction_text(prediction)}"
        )
        steps.append(step("Z", answer))
        problem = (
            "For kernel ridge regression with linear kernel K(x,z)=xz, "
            f"training data {pair_text(data)}, lambda={lam}, and x*={x_star}, "
            "solve (K + lambda I) alpha = y and predict f(x*)."
        )
        return dict(
            problem_id=jid(),
            operation="kernel_ridge_linear_2point",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


PYTHAGOREAN_WEIGHTS = [
    (3, 4), (4, 3), (5, 12), (12, 5), (8, 15), (15, 8),
    (7, 24), (24, 7),
]


def fraction_text(value):
    return str(Fraction(value))


def vector_text(vector):
    return "(" + ",".join(str(value) for value in vector) + ")"


def class_text(score):
    return "+1" if score >= 0 else "-1"


class SVMMarginGenerator(ProblemGenerator):
    """
    Linear SVM decision-function and margin-width arithmetic.

    The support vectors are chosen so alpha_i y_i x_i sums to a Pythagorean
    weight vector, making ||w|| and 2/||w|| exact.

    Op-codes used:
    - SVM_SETUP / SUPPORT_TERM / WEIGHT_VECTOR / DECISION / MARGIN
    - CHECK (established): decision sign
    - M / A / E / ROOT / D (established/shared): w, f(x), norm, margin
    - Z: weight vector, score, class, margin width
    """

    def generate(self) -> dict:
        base = random.choice(PYTHAGOREAN_WEIGHTS)
        signs = (random.choice([-1, 1]), random.choice([-1, 1]))
        w = (signs[0] * base[0], signs[1] * base[1])
        y1 = random.choice([-1, 1])
        y2 = random.choice([-1, 1])
        alpha1 = 1
        alpha2 = 1
        x1 = (y1 * w[0], 0)
        x2 = (0, y2 * w[1])
        bias = random.randint(-5, 5)
        query = (random.randint(-5, 5), random.randint(-5, 5))

        beta1 = alpha1 * y1
        beta2 = alpha2 * y2
        c11 = beta1 * x1[0]
        c12 = beta1 * x1[1]
        c21 = beta2 * x2[0]
        c22 = beta2 * x2[1]
        w1 = c11 + c21
        w2 = c12 + c22
        dot1 = w1 * query[0]
        dot2 = w2 * query[1]
        dot = dot1 + dot2
        score = dot + bias
        w1_sq = w1 ** 2
        w2_sq = w2 ** 2
        norm_sq = w1_sq + w2_sq
        norm = int(norm_sq ** 0.5)
        margin = Fraction(2, norm)
        predicted = class_text(score)

        steps = [
            step("SVM_SETUP",
                 f"x1={vector_text(x1)},y1={y1},alpha1={alpha1}",
                 f"x2={vector_text(x2)},y2={y2},alpha2={alpha2}",
                 f"b={bias},x={vector_text(query)}"),
            step("M", alpha1, y1, beta1),
            step("M", beta1, x1[0], c11),
            step("M", beta1, x1[1], c12),
            step("SUPPORT_TERM", "1", vector_text((c11, c12))),
            step("M", alpha2, y2, beta2),
            step("M", beta2, x2[0], c21),
            step("M", beta2, x2[1], c22),
            step("SUPPORT_TERM", "2", vector_text((c21, c22))),
            step("A", c11, c21, w1),
            step("A", c12, c22, w2),
            step("WEIGHT_VECTOR", "w", vector_text((w1, w2))),
            step("M", w1, query[0], dot1),
            step("M", w2, query[1], dot2),
            step("A", dot1, dot2, dot),
            step("A", dot, bias, score),
            step("DECISION", "f(x)", score),
            step("CHECK", "f(x) >= 0", f"{score} >= 0",
                 f"class={predicted}"),
            step("E", w1, 2, w1_sq),
            step("E", w2, 2, w2_sq),
            step("A", w1_sq, w2_sq, norm_sq),
            step("ROOT", f"sqrt({norm_sq})", norm),
            step("D", 2, norm, fraction_text(margin)),
            step("MARGIN", "2/norm(w)", fraction_text(margin)),
        ]
        answer = (
            f"w={vector_text((w1, w2))}; f(x)={score}; "
            f"class={predicted}; margin_width={fraction_text(margin)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For a linear SVM with support vectors x1={vector_text(x1)}, "
            f"y1={y1}, alpha1={alpha1}; x2={vector_text(x2)}, y2={y2}, "
            f"alpha2={alpha2}; bias b={bias}, compute f(x) at "
            f"x={vector_text(query)} and margin width 2/norm(w)."
        )
        return dict(
            problem_id=jid(),
            operation="svm_margin_linear",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kernel_ridge_generator import KernelRidgeGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For kernel ridge regression with linear kernel K\(x,z\)=xz, "
    r"training data \[\(([-0-9]+),([-0-9]+)\), "
    r"\(([-0-9]+),([-0-9]+)\)\], lambda=([0-9]+), and x\*=([-0-9]+), "
    r"solve \(K \+ lambda I\) alpha = y and predict f\(x\*\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


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


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    xs = [int(match.group(1)), int(match.group(3))]
    ys = [int(match.group(2)), int(match.group(4))]
    lam = int(match.group(5))
    x_star = int(match.group(6))
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
        make_step("KRR_SETUP", "kernel=linear",
                  f"data={pair_text(data)}", f"lambda={lam},x*={x_star}"),
        make_step("M", xs[0], xs[0], k11),
        make_step("KERNEL_VALUE", "1,1", k11),
        make_step("M", xs[0], xs[1], k12),
        make_step("KERNEL_VALUE", "1,2", k12),
        make_step("M", xs[1], xs[0], k21),
        make_step("KERNEL_VALUE", "2,1", k21),
        make_step("M", xs[1], xs[1], k22),
        make_step("KERNEL_VALUE", "2,2", k22),
        make_step("RIDGE_ENTRY", "K", matrix_text(gram)),
        make_step("A", k11, lam, a),
        make_step("RIDGE_ENTRY", "1,1", a),
        make_step("RIDGE_ENTRY", "1,2", b),
        make_step("RIDGE_ENTRY", "2,1", c),
        make_step("A", k22, lam, d),
        make_step("RIDGE_ENTRY", "2,2", d),
        make_step("RIDGE_ENTRY", "K+lambdaI", matrix_text(ridge)),
        make_step("M", a, d, ad),
        make_step("M", b, c, bc),
        make_step("S", ad, bc, det),
        make_step("DET", "K+lambdaI", det),
        make_step("M", d, ys[0], d_y1),
        make_step("M", b, ys[1], b_y2),
        make_step("S", d_y1, b_y2, num1),
        make_step("D", num1, det, fraction_text(alpha1)),
        make_step("ALPHA", "alpha1", fraction_text(alpha1)),
        make_step("M", a, ys[1], a_y2),
        make_step("M", c, ys[0], c_y1),
        make_step("S", a_y2, c_y1, num2),
        make_step("D", num2, det, fraction_text(alpha2)),
        make_step("ALPHA", "alpha2", fraction_text(alpha2)),
        make_step("M", x_star, xs[0], k_star1),
        make_step("KERNEL_VALUE", "x*,1", k_star1),
        make_step("M", x_star, xs[1], k_star2),
        make_step("KERNEL_VALUE", "x*,2", k_star2),
        make_step("M", k_star1, fraction_text(alpha1), fraction_text(term1)),
        make_step("M", k_star2, fraction_text(alpha2), fraction_text(term2)),
        make_step("A", fraction_text(term1), fraction_text(term2),
                  fraction_text(prediction)),
        make_step("PREDICT", "x*", fraction_text(prediction)),
    ]
    answer = (
        f"alpha={vector_text((alpha1, alpha2))}; "
        f"prediction={fraction_text(prediction)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestKernelRidgeGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KernelRidgeGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "kernel_ridge_linear_2point")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

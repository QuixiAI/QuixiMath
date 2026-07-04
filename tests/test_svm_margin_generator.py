import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.svm_margin_generator import SVMMarginGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For a linear SVM with support vectors x1=(\([^)]+\)), y1=([-0-9]+), "
    r"alpha1=([0-9]+); x2=(\([^)]+\)), y2=([-0-9]+), alpha2=([0-9]+); "
    r"bias b=([-0-9]+), compute f\(x\) at x=(\([^)]+\)) and margin "
    r"width 2/norm\(w\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_vector(raw):
    left, right = raw.strip("()").split(",")
    return (int(left), int(right))


def vector_text(vector):
    return "(" + ",".join(str(value) for value in vector) + ")"


def class_text(score):
    return "+1" if score >= 0 else "-1"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    x1 = parse_vector(match.group(1))
    y1 = int(match.group(2))
    alpha1 = int(match.group(3))
    x2 = parse_vector(match.group(4))
    y2 = int(match.group(5))
    alpha2 = int(match.group(6))
    bias = int(match.group(7))
    query = parse_vector(match.group(8))
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
    norm = math.isqrt(norm_sq)
    margin = Fraction(2, norm)
    predicted = class_text(score)
    steps = [
        make_step("SVM_SETUP",
                  f"x1={vector_text(x1)},y1={y1},alpha1={alpha1}",
                  f"x2={vector_text(x2)},y2={y2},alpha2={alpha2}",
                  f"b={bias},x={vector_text(query)}"),
        make_step("M", alpha1, y1, beta1),
        make_step("M", beta1, x1[0], c11),
        make_step("M", beta1, x1[1], c12),
        make_step("SUPPORT_TERM", "1", vector_text((c11, c12))),
        make_step("M", alpha2, y2, beta2),
        make_step("M", beta2, x2[0], c21),
        make_step("M", beta2, x2[1], c22),
        make_step("SUPPORT_TERM", "2", vector_text((c21, c22))),
        make_step("A", c11, c21, w1),
        make_step("A", c12, c22, w2),
        make_step("WEIGHT_VECTOR", "w", vector_text((w1, w2))),
        make_step("M", w1, query[0], dot1),
        make_step("M", w2, query[1], dot2),
        make_step("A", dot1, dot2, dot),
        make_step("A", dot, bias, score),
        make_step("DECISION", "f(x)", score),
        make_step("CHECK", "f(x) >= 0", f"{score} >= 0",
                  f"class={predicted}"),
        make_step("E", w1, 2, w1_sq),
        make_step("E", w2, 2, w2_sq),
        make_step("A", w1_sq, w2_sq, norm_sq),
        make_step("ROOT", f"sqrt({norm_sq})", norm),
        make_step("D", 2, norm, fraction_text(margin)),
        make_step("MARGIN", "2/norm(w)", fraction_text(margin)),
    ]
    answer = (
        f"w={vector_text((w1, w2))}; f(x)={score}; "
        f"class={predicted}; margin_width={fraction_text(margin)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSVMMarginGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SVMMarginGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "svm_margin_linear")
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
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    radicand = int(fields[1][5:-1])
                    self.assertEqual(math.isqrt(radicand), int(fields[2]),
                                     raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

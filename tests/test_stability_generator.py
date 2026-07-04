import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.stability_generator import StabilityGenerator
from helpers import DELIM


def factor_text(root):
    if root == 0:
        return "y"
    return f"(y - {root})" if root > 0 else f"(y + {abs(root)})"


def f_text(leading, roots):
    body = "".join(factor_text(root) for root in roots)
    return body if leading > 0 else f"-{body}"


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def eval_poly(leading, roots, y):
    value = Fraction(leading)
    for root in roots:
        value *= y - root
    return value


def sign_word(value):
    return "positive" if value > 0 else "negative"


def arrow(value):
    return "up" if value > 0 else "down"


def interval_text(index, roots):
    if index == 0:
        return f"(-inf, {roots[0]})"
    if index == len(roots):
        return f"({roots[-1]}, inf)"
    return f"({roots[index - 1]}, {roots[index]})"


def test_point(index, roots):
    if index == 0:
        return Fraction(roots[0] - 1)
    if index == len(roots):
        return Fraction(roots[-1] + 1)
    return Fraction(roots[index - 1] + roots[index], 2)


def classify(left_sign, right_sign):
    if left_sign > 0 and right_sign < 0:
        return "stable"
    if left_sign < 0 and right_sign > 0:
        return "unstable"
    return "semistable"


def answer_text(roots, classes):
    return "equilibria: " + "; ".join(
        f"y={root} {cls}" for root, cls in zip(roots, classes)
    )


def parse_f(expr):
    leading = -1 if expr.startswith("-") else 1
    if leading < 0:
        expr = expr[1:]
    roots = []
    consumed = ""
    for match in re.finditer(r"\(y ([+-]) (\d+)\)|y", expr):
        consumed += match.group(0)
        if match.group(1):
            mag = int(match.group(2))
            roots.append(mag if match.group(1) == "-" else -mag)
        else:
            roots.append(0)
    assert consumed == expr, expr
    return leading, sorted(roots)


def parse_problem(problem):
    match = re.fullmatch(
        r"For dy/dt = (.+), find equilibria and classify stability by "
        r"sign analysis\.",
        problem,
    )
    assert match is not None, problem
    return parse_f(match.group(1))


def oracle_parts(example):
    leading, roots = parse_problem(example["problem"])
    signs = []
    for index in range(len(roots) + 1):
        value = eval_poly(leading, roots, test_point(index, roots))
        signs.append(1 if value > 0 else -1)
    classes = [
        classify(signs[index], signs[index + 1])
        for index in range(len(roots))
    ]
    return {
        "leading": leading,
        "roots": roots,
        "signs": signs,
        "classes": classes,
        "answer": answer_text(roots, classes),
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    sign_index = 0
    stability_index = 0
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            expected = [
                f"dy/dt = {f_text(parts['leading'], parts['roots'])}",
                "equilibria and stability",
            ]
            if fields[1:] != expected:
                return False
        elif op == "EQUILIBRIA":
            expected = ", ".join(f"y={root}" for root in parts["roots"])
            if fields[1:] != ["f(y) = 0", expected]:
                return False
        elif op == "SIGN_TEST":
            point = test_point(sign_index, parts["roots"])
            value = eval_poly(parts["leading"], parts["roots"], point)
            expected = [
                interval_text(sign_index, parts["roots"]),
                f"y = {fmt_frac(point)}",
                f"f(y) = {fmt_frac(value)} ({sign_word(value)})",
                arrow(value),
            ]
            if fields[1:] != expected:
                return False
            sign_index += 1
        elif op == "STABILITY":
            root = parts["roots"][stability_index]
            cls = parts["classes"][stability_index]
            left = parts["signs"][stability_index]
            right = parts["signs"][stability_index + 1]
            expected = [
                f"y={root}",
                f"left {arrow(left)}, right {arrow(right)}",
                cls,
            ]
            if fields[1:] != expected:
                return False
            stability_index += 1
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return (sign_index == len(parts["roots"]) + 1 and
            stability_index == len(parts["roots"]))


class TestStabilityGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = StabilityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_fixed_variant_constructor(self):
        gen = StabilityGenerator("factored_polynomial")
        result = gen.generate()
        self.assertEqual(result["operation"],
                         "stability_factored_polynomial")
        with self.assertRaises(ValueError):
            StabilityGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"\+ -|--|1\(y")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))
            for raw_step in result["steps"]:
                self.assertIsNone(bad.search(raw_step), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

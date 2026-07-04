import ast
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gradient_step_generator import GradientStepGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For linear model y_hat = w0 \+ w1\*x with samples (\[[^\]]+\]), "
    r"start at w=\(([^,]+),([^)]+)\)\. Use MSE L=\(1/n\) sum "
    r"\(y_hat-y\)\^2 and learning rate eta=([^.]*)\. Compute one "
    r"gradient-descent update\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def pair_text(left, right):
    return f"({fraction_text(left)},{fraction_text(right)})"


def samples_text(samples):
    return "[" + ", ".join(f"({x},{y})" for x, y in samples) + "]"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    samples = ast.literal_eval(match.group(1))
    w0 = Fraction(match.group(2))
    w1 = Fraction(match.group(3))
    eta = Fraction(match.group(4))
    return samples, w0, w1, eta


def expected_flow(example):
    samples, w0, w1, eta = parse_problem(example["problem"])
    steps = [
        make_step("MSE_SETUP", "model y_hat=w0+w1*x",
                  f"samples={samples_text(samples)}",
                  f"w={pair_text(w0, w1)}, eta={fraction_text(eta)}"),
        make_step("MSE_FORMULA", "L=(1/n) sum r_i^2",
                  "grad=(2/n) sum r_i*[1,x_i]"),
    ]

    sum_squared = Fraction(0)
    sum_residual = Fraction(0)
    sum_residual_x = Fraction(0)
    for index, (x_value, y_value) in enumerate(samples, start=1):
        x_frac = Fraction(x_value)
        y_frac = Fraction(y_value)
        linear_term = w1 * x_frac
        prediction = w0 + linear_term
        residual = prediction - y_frac
        squared = residual ** 2
        new_sum_squared = sum_squared + squared
        new_sum_residual = sum_residual + residual
        residual_x = residual * x_frac
        new_sum_residual_x = sum_residual_x + residual_x
        steps.extend([
            make_step("M", fraction_text(w1), x_value,
                      fraction_text(linear_term)),
            make_step("A", fraction_text(w0), fraction_text(linear_term),
                      fraction_text(prediction)),
            make_step("S", fraction_text(prediction), y_value,
                      fraction_text(residual)),
            make_step("E", fraction_text(residual), 2,
                      fraction_text(squared)),
            make_step("A", fraction_text(sum_squared),
                      fraction_text(squared),
                      fraction_text(new_sum_squared)),
            make_step("A", fraction_text(sum_residual),
                      fraction_text(residual),
                      fraction_text(new_sum_residual)),
            make_step("M", fraction_text(residual), x_value,
                      fraction_text(residual_x)),
            make_step("A", fraction_text(sum_residual_x),
                      fraction_text(residual_x),
                      fraction_text(new_sum_residual_x)),
            make_step("MSE_SAMPLE", f"i={index}",
                      f"pred={fraction_text(prediction)}",
                      f"r={fraction_text(residual)}"),
        ])
        sum_squared = new_sum_squared
        sum_residual = new_sum_residual
        sum_residual_x = new_sum_residual_x

    n = len(samples)
    loss = sum_squared / n
    double_residual = 2 * sum_residual
    grad_w0 = double_residual / n
    double_residual_x = 2 * sum_residual_x
    grad_w1 = double_residual_x / n
    delta_w0 = eta * grad_w0
    new_w0 = w0 - delta_w0
    delta_w1 = eta * grad_w1
    new_w1 = w1 - delta_w1
    steps.extend([
        make_step("D", fraction_text(sum_squared), n, fraction_text(loss)),
        make_step("M", 2, fraction_text(sum_residual),
                  fraction_text(double_residual)),
        make_step("D", fraction_text(double_residual), n,
                  fraction_text(grad_w0)),
        make_step("M", 2, fraction_text(sum_residual_x),
                  fraction_text(double_residual_x)),
        make_step("D", fraction_text(double_residual_x), n,
                  fraction_text(grad_w1)),
        make_step("MSE_GRADIENT", f"g0={fraction_text(grad_w0)}",
                  f"g1={fraction_text(grad_w1)}"),
        make_step("M", fraction_text(eta), fraction_text(grad_w0),
                  fraction_text(delta_w0)),
        make_step("S", fraction_text(w0), fraction_text(delta_w0),
                  fraction_text(new_w0)),
        make_step("M", fraction_text(eta), fraction_text(grad_w1),
                  fraction_text(delta_w1)),
        make_step("S", fraction_text(w1), fraction_text(delta_w1),
                  fraction_text(new_w1)),
        make_step("GD_UPDATE", f"w_old={pair_text(w0, w1)}",
                  f"eta={fraction_text(eta)}",
                  f"w_new={pair_text(new_w0, new_w1)}"),
    ])
    answer = (
        f"loss={fraction_text(loss)}; "
        f"gradient={pair_text(grad_w0, grad_w1)}; "
        f"w_new={pair_text(new_w0, new_w1)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestGradientStepGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GradientStepGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
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

    def test_variants_are_available(self):
        for variant in GradientStepGenerator.VARIANTS:
            result = GradientStepGenerator(variant).generate()
            self.assertEqual(result["operation"], f"gradient_step_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)
            samples, _, _, _ = parse_problem(result["problem"])
            self.assertEqual(
                len(samples), 2 if variant == "two_sample" else 3
            )

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GradientStepGenerator("bogus")

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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
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

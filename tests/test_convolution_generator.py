import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.convolution_generator import (
    ConvolutionGenerator,
    convolution,
    seq_text,
)
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Compute the discrete convolution of x=\[([0-9,]+)\] and "
    r"h=\[([0-9,]+)\]\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_seq(raw):
    return [int(part) for part in raw.split(",")]


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return parse_seq(match.group(1)), parse_seq(match.group(2))


def expected_flow(example):
    x_values, h_values = parse_problem(example["problem"])
    y_values = convolution(x_values, h_values)
    steps = [
        make_step("CONV_SETUP", f"x={seq_text(x_values)}",
                  f"h={seq_text(h_values)}"),
    ]
    for index in range(len(y_values)):
        terms = []
        products = []
        for j, x_value in enumerate(x_values):
            h_index = index - j
            if 0 <= h_index < len(h_values):
                terms.append(f"x{j}*h{h_index}")
                products.append(x_value * h_values[h_index])
        steps.append(make_step("CONV_WINDOW", f"n={index}",
                               " + ".join(terms)))
        for term_index, product in enumerate(products):
            x_part, h_part = terms[term_index].split("*")
            x_index = int(x_part[1:])
            h_index = int(h_part[1:])
            steps.append(make_step("M", x_values[x_index], h_values[h_index],
                                   product))
        if len(products) == 1:
            steps.append(make_step("CONV_SUM", f"n={index}", products[0]))
        else:
            running = products[0]
            for product in products[1:]:
                new_running = running + product
                steps.append(make_step("A", running, product, new_running))
                running = new_running
    answer = f"y={seq_text(y_values)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestConvolutionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ConvolutionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "discrete_convolution")
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
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_output_length(self):
        for _ in range(300):
            result = self.gen.generate()
            x_values, h_values = parse_problem(result["problem"])
            y_values = parse_seq(re.search(r"y=\[([0-9,]+)\]",
                                           result["final_answer"]).group(1))
            self.assertEqual(len(y_values), len(x_values) + len(h_values) - 1)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kernel_perceptron_generator import KernelPerceptronGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Run one epoch of the kernel perceptron with linear kernel K\(x,z\)=xz "
    r"on data \[\(([-0-9]+),([-0-9]+)\), \(([-0-9]+),([-0-9]+)\), "
    r"\(([-0-9]+),([-0-9]+)\)\], starting alpha=\(0,0,0\)\. "
    r"Use update alpha_i \+= 1 when y_i score_i <= 0\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def data_text(data):
    return "[" + ", ".join(f"({x},{y})" for x, y in data) + "]"


def bool_text(value):
    return "true" if value else "false"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    values = [int(match.group(index)) for index in range(1, 7)]
    data = [(values[0], values[1]), (values[2], values[3]),
            (values[4], values[5])]
    alphas = [0, 0, 0]
    updates = 0
    steps = [
        make_step("KP_SETUP", "kernel=linear", f"data={data_text(data)}",
                  "alpha0=(0,0,0)"),
    ]
    for i, (x_i, y_i) in enumerate(data):
        steps.append(make_step("KP_EXAMPLE", i + 1, f"x={x_i},y={y_i}",
                               f"alpha={vector_text(alphas)}"))
        terms = []
        for j, (x_j, y_j) in enumerate(data):
            kernel = x_j * x_i
            beta = alphas[j] * y_j
            term = beta * kernel
            steps.extend([
                make_step("M", x_j, x_i, kernel),
                make_step("KERNEL_VALUE", f"{j + 1},{i + 1}", kernel),
                make_step("M", alphas[j], y_j, beta),
                make_step("M", beta, kernel, term),
                make_step("KP_TERM", f"j={j + 1}", term),
            ])
            terms.append(term)
        partial = terms[0] + terms[1]
        score = partial + terms[2]
        margin = y_i * score
        should_update = margin <= 0
        steps.extend([
            make_step("A", terms[0], terms[1], partial),
            make_step("A", partial, terms[2], score),
            make_step("DECISION", f"score_{i + 1}", score),
            make_step("M", y_i, score, margin),
            make_step("CHECK", "y*score <= 0", f"{margin} <= 0",
                      f"update={bool_text(should_update)}"),
        ])
        if should_update:
            new_alpha = alphas[i] + 1
            steps.append(make_step("A", alphas[i], 1, new_alpha))
            alphas[i] = new_alpha
            updates += 1
        steps.append(make_step("UPDATE", f"alpha{i + 1}", alphas[i]))
    answer = f"alpha={vector_text(alphas)}; updates={updates}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestKernelPerceptronGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KernelPerceptronGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "kernel_perceptron_one_epoch")
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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.softmax_gradient_generator import SoftmaxGradientGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Given logits z=\(([0-9]+)\*ln\(([0-9]+)\),([0-9]+)\*ln\(([0-9]+)\),"
    r"([0-9]+)\*ln\(([0-9]+)\)\) with temperature T=([0-9]+) "
    r"and target class ([0-9]+), compute the temperature-scaled softmax, "
    r"log-softmax, cross-entropy, and gradient p-y\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def fraction_vector_text(values):
    return "(" + ",".join(fraction_text(value) for value in values) + ")"


def log_vector_text(values):
    return "(" + ",".join(f"ln({fraction_text(value)})" for value in values) + ")"


def logits_text(temp, weights):
    return "(" + ",".join(f"{temp}*ln({weight})" for weight in weights) + ")"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    temps = [int(match.group(1)), int(match.group(3)), int(match.group(5))]
    weights = [int(match.group(2)), int(match.group(4)),
               int(match.group(6))]
    temp = int(match.group(7))
    target = int(match.group(8))
    if temps != [temp, temp, temp]:
        raise AssertionError(example["problem"])
    total = sum(weights)
    probs = [Fraction(weight, total) for weight in weights]
    log_probs = probs[:]
    ce = Fraction(total, weights[target - 1])
    labels = [1 if index == target - 1 else 0 for index in range(3)]
    grads = [probs[index] - labels[index] for index in range(3)]
    steps = [
        make_step("SOFTMAX_SETUP", f"z={logits_text(temp, weights)}",
                  f"T={temp}", f"target={target}"),
    ]
    for index, weight in enumerate(weights, start=1):
        steps.extend([
            make_step("TEMP_SCALE", f"z{index}/T", f"ln({weight})"),
            make_step("SOFTMAX_EXP", index, weight),
        ])
    running = 0
    for weight in weights:
        new_running = running + weight
        steps.append(make_step("A", running, weight, new_running))
        running = new_running
    for index, prob in enumerate(probs, start=1):
        steps.extend([
            make_step("D", weights[index - 1], total, fraction_text(prob)),
            make_step("SOFTMAX_PROB", index, fraction_text(prob)),
            make_step("LOG_SOFTMAX", index, f"ln({fraction_text(prob)})"),
        ])
    steps.append(make_step("CROSS_ENTROPY", f"target={target}",
                           f"ln({fraction_text(ce)})"))
    for index, grad in enumerate(grads, start=1):
        steps.extend([
            make_step("S", fraction_text(probs[index - 1]),
                      labels[index - 1], fraction_text(grad)),
            make_step("GRAD", index, fraction_text(grad)),
        ])
    answer = (
        f"p={fraction_vector_text(probs)}; "
        f"log_softmax={log_vector_text(log_probs)}; "
        f"CE=ln({fraction_text(ce)}); "
        f"grad={fraction_vector_text(grads)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSoftmaxGradientGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SoftmaxGradientGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "softmax_gradient_exact")
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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
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

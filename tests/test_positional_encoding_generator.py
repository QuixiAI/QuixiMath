import os
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.positional_encoding_generator import (
    ANGLE_TABLE,
    PositionalEncodingGenerator,
)
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"At position p=([0-9]+), the sinusoidal encoding angle is theta=([^.]*)\. "
    r"Compute the d=2 positional encoding PE=\(sin\(theta\), cos\(theta\)\)\."
)
TABLE = {angle: (sin_value, cos_value)
         for angle, sin_value, cos_value in ANGLE_TABLE}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def vector_text(values):
    return "(" + ",".join(values) + ")"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    position = int(match.group(1))
    angle = match.group(2)
    sin_value, cos_value = TABLE[angle]
    steps = [
        make_step("PE_SETUP", f"position={position}", "d=2",
                  f"theta={angle}"),
        make_step("ANGLE", "theta", angle),
        make_step("SIN", angle, sin_value),
        make_step("PE_ENTRY", 0, sin_value),
        make_step("COS", angle, cos_value),
        make_step("PE_ENTRY", 1, cos_value),
    ]
    answer = f"PE={vector_text((sin_value, cos_value))}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPositionalEncodingGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PositionalEncodingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "positional_encoding_2d")
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

    def test_covers_unit_circle_table_values(self):
        seen = set()
        for _ in range(500):
            result = self.gen.generate()
            angle = PROBLEM_RE.fullmatch(result["problem"]).group(2)
            seen.add(angle)
        self.assertGreaterEqual(len(seen), 6)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

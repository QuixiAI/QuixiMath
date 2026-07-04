import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.routh_hurwitz_generator import (
    RouthHurwitzGenerator,
    first_column_text,
)
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Build the Routh-Hurwitz array for p\(s\)=s\^3\+(\d+)s\^2\+"
    r"(\d+)s\+(\d+) and determine stability\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    a1, a2, a3 = (
        int(value) for value in PROBLEM_RE.fullmatch(example["problem"]).groups()
    )
    product = a1 * a2
    numerator = product - a3
    s1_entry = Fraction(numerator, a1)
    first_column = [Fraction(1), Fraction(a1), s1_entry, Fraction(a3)]
    stability = "stable" if all(value > 0 for value in first_column) else "not stable"
    steps = [
        make_step("ROUTH_SETUP", f"p(s)=s^3+{a1}s^2+{a2}s+{a3}"),
        make_step("ROUTH_ROW", "s^3", f"1, {a2}"),
        make_step("ROUTH_ROW", "s^2", f"{a1}, {a3}"),
        make_step("M", a1, a2, product),
        make_step("S", product, a3, numerator),
        make_step("D", numerator, a1, fraction_text(s1_entry)),
        make_step("ROUTH_ROW", "s^1", f"{fraction_text(s1_entry)}, 0"),
        make_step("ROUTH_ROW", "s^0", f"{a3}"),
        make_step("CHECK", f"first column={first_column_text(first_column)}",
                  stability),
    ]
    answer = f"first column={first_column_text(first_column)}; {stability}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestRouthHurwitzGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RouthHurwitzGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "routh_hurwitz_cubic")
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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_both_stability_outcomes_appear(self):
        outcomes = {self.gen.generate()["final_answer"].rsplit("; ", 1)[1]
                    for _ in range(500)}
        self.assertIn("stable", outcomes)
        self.assertIn("not stable", outcomes)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

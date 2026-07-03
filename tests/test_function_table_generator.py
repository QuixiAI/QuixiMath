import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.function_table_generator import FunctionTableGenerator
from helpers import DELIM


def oracle_answer(example):
    """Independently builds the table from the problem text alone."""
    m = re.fullmatch(
        r"Complete the table for [a-z]\(([a-z])\) = (.+) "
        r"at \1 = (-?\d+(?:, -?\d+)*)\. Give the [a-z]\(\1\) values in order\.",
        example["problem"])
    assert m, example["problem"]
    var, rule, x_list = m.groups()
    xs = [int(v) for v in x_list.split(", ")]

    mm = re.fullmatch(rf"(?:(\d+) · )?(\d+)\^{var}", rule)
    if mm:  # exponential a · b^x
        a = int(mm.group(1) or 1)
        base = int(mm.group(2))
        return ", ".join(str(a * base ** x) for x in xs)

    mm = re.fullmatch(rf"(-?\d*){var}\^2 ([+-]) (\d+)", rule)
    if mm:  # quadratic ax^2 + c
        a = int(mm.group(1) + "1") if mm.group(1) in ("", "-") \
            else int(mm.group(1))
        c = int(mm.group(3)) * (1 if mm.group(2) == "+" else -1)
        return ", ".join(str(a * x * x + c) for x in xs)

    mm = re.fullmatch(rf"(-?\d+){var} ([+-]) (\d+)", rule)
    assert mm, rule
    a = int(mm.group(1))
    b = int(mm.group(3)) * (1 if mm.group(2) == "+" else -1)
    return ", ".join(str(a * x + b) for x in xs)


class TestFunctionTableGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FunctionTableGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "function_table")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: rebuild the table independently from the text."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_entries_match_answer_in_order(self):
        for _ in range(300):
            result = self.gen.generate()
            entries = [s.split(DELIM)[2] for s in result["steps"]
                       if s.startswith(f"TABLE_ENTRY{DELIM}")]
            self.assertEqual(len(entries), 4)
            self.assertEqual(", ".join(entries), result["final_answer"])

    def test_every_row_is_substituted(self):
        """Each listed input gets its own SUBST step, in order."""
        for _ in range(300):
            result = self.gen.generate()
            m = re.search(r" at [a-z] = (.+)\. Give", result["problem"])
            xs = m.group(1).split(", ")
            substs = [s.split(DELIM)[2] for s in result["steps"]
                      if s.startswith(f"SUBST{DELIM}")]
            self.assertEqual(substs, xs)

    def test_subst_parenthesizes_inputs(self):
        """Regression guard: no digit-smashed substitutions like -45 + 5."""
        gen = FunctionTableGenerator("linear")
        for _ in range(200):
            result = gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "SUBST":
                    self.assertIn(f"({f[2]})", f[3], s)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(150):
            p = self.gen.generate()["problem"]
            if "^2" in p:
                kinds.add("quadratic")
            elif re.search(r"\d\^[a-z]", p):
                kinds.add("exponential")
            else:
                kinds.add("linear")
        self.assertEqual(kinds, {"linear", "quadratic", "exponential"})

    def test_exponential_inputs_start_at_zero(self):
        gen = FunctionTableGenerator("exponential")
        for _ in range(100):
            result = gen.generate()
            self.assertIn("= 0, 1, 2, 3", result["problem"])

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FunctionTableGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

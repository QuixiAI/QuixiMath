import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ratio_table_generator import RatioTableGenerator
from helpers import DELIM


def parse_table(problem):
    """Extracts the two table rows (lists with None for '?') from the problem text."""
    lines = problem.split("\n")
    rows = []
    for line in lines[1:3]:
        cells = line.split(": ", 1)[1].split(", ")
        rows.append([None if c == "?" else int(c) for c in cells])
    return rows


def oracle_missing_value(rows):
    """Independently recomputes the missing value from the table alone."""
    row1, row2 = rows
    missing_row = 0 if None in row1 else 1
    missing_col = (row1 if missing_row == 0 else row2).index(None)
    anchor_col = next(i for i in range(4)
                      if row1[i] is not None and row2[i] is not None)
    # row1[c] / row2[c] is constant: solve for the blank via the anchor ratio.
    if missing_row == 0:
        return row1[anchor_col] * row2[missing_col] // row2[anchor_col]
    return row2[anchor_col] * row1[missing_col] // row1[anchor_col]


class TestRatioTableGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RatioTableGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "ratio_table")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM)[1], result["final_answer"])

    def test_expected_opcodes_present(self):
        result = self.gen.generate()
        codes = [s.split(DELIM)[0] for s in result["steps"]]
        for code in ("RATIO_TABLE", "RATIO_BASE", "D", "M", "CHECK", "Z"):
            self.assertIn(code, codes, f"Missing op-code {code}")

    def test_oracle_answer_from_problem_text(self):
        """A9-style oracle: re-derive the answer from the problem text alone."""
        for _ in range(300):
            result = self.gen.generate()
            rows = parse_table(result["problem"])
            self.assertEqual(str(oracle_missing_value(rows)),
                             result["final_answer"], result["problem"])

    def test_all_step_arithmetic_verified(self):
        """Every D, M, and CHECK step's arithmetic must be independently true."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                fields = s.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]), int(fields[3]), s)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0, s)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]), int(fields[3]), s)
                elif fields[0] == "CHECK":
                    self.assertEqual(fields[1], "cross_products", s)
                    products = []
                    for work in fields[2:4]:
                        m = re.fullmatch(r"(\d+)×(\d+)=(\d+)", work)
                        self.assertIsNotNone(m, s)
                        self.assertEqual(int(m.group(1)) * int(m.group(2)),
                                         int(m.group(3)), s)
                        products.append(int(m.group(3)))
                    self.assertEqual(products[0], products[1],
                                     f"Cross products differ: {s}")

    def test_base_ratio_is_simplest_form(self):
        for _ in range(200):
            result = self.gen.generate()
            base = next(s for s in result["steps"] if s.startswith(f"RATIO_BASE{DELIM}"))
            _, pair, g, simplest = base.split(DELIM)
            p1, p2 = (int(v) for v in pair.split(":"))
            s1, s2 = (int(v) for v in simplest.split(":"))
            self.assertEqual((p1 // int(g), p2 // int(g)), (s1, s2), base)
            # simplest form means coprime
            a, b = s1, s2
            while b:
                a, b = b, a % b
            self.assertEqual(a, 1, f"Not simplest form: {base}")

    def test_table_has_exactly_one_blank_and_four_columns(self):
        for _ in range(100):
            result = self.gen.generate()
            rows = parse_table(result["problem"])
            self.assertEqual(len(rows[0]), 4)
            self.assertEqual(len(rows[1]), 4)
            blanks = rows[0].count(None) + rows[1].count(None)
            self.assertEqual(blanks, 1)


if __name__ == "__main__":
    unittest.main()

import os
import random
import re
import sys
import unittest
from decimal import Decimal

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.normal_table_generator import NormalTableGenerator
from helpers import DELIM


def parse_problem(problem):
    """Returns (mu, sigma, kind, values, table) parsed from the text alone."""
    m = re.search(r"mean (\d+) \S+ and standard deviation (\d+)", problem)
    mu, sigma = int(m.group(1)), int(m.group(2))
    table = {Decimal(z): Decimal(v) for z, v in
             re.findall(r"z=(\d+\.\d{2}): (0\.\d{4})", problem)}
    if "between" in problem:
        q = re.search(r"between (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?) ", problem)
        return mu, sigma, "between", (Decimal(q.group(1)), Decimal(q.group(2))), table
    q = re.search(r"value (below|above) (\d+(?:\.\d+)?) ", problem)
    return mu, sigma, q.group(1), (Decimal(q.group(2)),), table


def oracle_answer(example):
    """Recomputes the probability using ONLY the printed table values."""
    mu, sigma, kind, vals, table = parse_problem(example["problem"])
    def z_of(x):
        z = (x - mu) / sigma
        assert z == z.quantize(Decimal("0.1")), f"z not clean: {z}"
        return z
    if kind == "between":
        z1, z2 = z_of(vals[0]), z_of(vals[1])
        return f"{table[z2] - table[z1]:.4f}"
    z = z_of(vals[0])
    if kind == "below" and z > 0:
        return f"{table[z]:.4f}"
    if kind == "below":  # negative z, symmetry
        return f"{Decimal('1') - table[-z]:.4f}"
    return f"{Decimal('1') - table[z]:.4f}"  # above


class TestNormalTableGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = NormalTableGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])
        self.assertRegex(result["final_answer"], r"^0\.\d{4}$")

    def test_oracle_from_printed_table_only(self):
        """A9 oracle: recompute the probability using only the z-table
        excerpt printed in the problem (Principle 5 end to end)."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_needed_z_in_table_with_decoys(self):
        for _ in range(200):
            result = self.gen.generate()
            mu, sigma, kind, vals, table = parse_problem(result["problem"])
            needed = {abs((x - mu) / sigma) for x in vals}
            for z in needed:
                self.assertIn(z, table, result["problem"])
            self.assertGreater(len(table), len(needed),
                               "no decoy rows in table")

    def test_subtraction_steps_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "S":
                    self.assertEqual(Decimal(f[1]) - Decimal(f[2]),
                                     Decimal(f[3]), s)
                elif f[0] == "TABLE_LOOKUP":
                    # the looked-up value must appear in the printed table
                    self.assertIn(f"{f[1].strip('Φ()')}: {f[2]}"
                                  .replace("Φ", ""),
                                  result["problem"].replace("z=", ""), s)

    def test_all_variants_reachable(self):
        ops = set()
        negatives = 0
        for _ in range(200):
            result = self.gen.generate()
            ops.add(result["operation"])
            if any(s.startswith(f"ZSCORE{DELIM}") and "|-" in s
                   for s in result["steps"]):
                negatives += 1
        self.assertEqual(ops, {"normal_below", "normal_above",
                               "normal_between"})
        self.assertGreater(negatives, 10, "symmetry cases should appear")

    def test_fixed_variant_constructor(self):
        gen = NormalTableGenerator("between")
        for _ in range(10):
            self.assertEqual(gen.generate()["operation"], "normal_between")
        with self.assertRaises(ValueError):
            NormalTableGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

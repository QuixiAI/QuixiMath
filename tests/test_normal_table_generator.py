import os
import random
import re
import sys
import unittest
from decimal import Decimal

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.normal_table_generator import QUERIES, NormalTableGenerator
from helpers import DELIM


def decimal_text(value):
    value = Decimal(value)
    if value == value.to_integral_value():
        return str(int(value))
    return format(value.normalize(), "f")


def parse_problem(problem):
    """Returns (mu, sigma, kind, values, table) parsed from the text alone."""
    m = re.search(r"mean (\d+) \S+ and standard deviation (\d+)", problem)
    mu, sigma = int(m.group(1)), int(m.group(2))
    table = {Decimal(z): Decimal(v) for z, v in
             re.findall(r"z=(\d+\.\d{2}): (0\.\d{4})", problem)}
    inverse = re.search(r"Find x such that P\(X < x\) = (0\.\d{4})", problem)
    if inverse:
        return mu, sigma, "inverse", (Decimal(inverse.group(1)),), table
    symmetric = re.search(
        r"symmetric interval from (-?\d+(?:\.\d+)?) to (-?\d+(?:\.\d+)?) ",
        problem)
    if symmetric:
        return (mu, sigma, "symmetric",
                (Decimal(symmetric.group(1)), Decimal(symmetric.group(2))), table)
    if "between" in problem:
        q = re.search(r"between (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?) ", problem)
        return mu, sigma, "between", (Decimal(q.group(1)), Decimal(q.group(2))), table
    q = re.search(r"value (below|above) (\d+(?:\.\d+)?) ", problem)
    return mu, sigma, q.group(1), (Decimal(q.group(2)),), table


def oracle_answer(example):
    """Recomputes the probability using ONLY the printed table values."""
    mu, sigma, kind, vals, table = parse_problem(example["problem"])
    if kind == "inverse":
        matches = [z for z, probability in table.items()
                   if probability == vals[0]]
        assert len(matches) == 1, (matches, table, vals[0])
        return decimal_text(Decimal(mu) + matches[0] * Decimal(sigma))
    if kind == "symmetric":
        z = (vals[1] - Decimal(mu)) / Decimal(sigma)
        assert vals[0] == Decimal(mu) - z * Decimal(sigma)
        return f"{Decimal(2) * table[z] - Decimal(1):.4f}"
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
        if result["operation"] == "normal_inverse_lookup":
            self.assertRegex(result["final_answer"], r"^-?\d+(?:\.\d+)?$")
        else:
            self.assertRegex(result["final_answer"], r"^0\.\d{4}$")

    def test_oracle_from_printed_table_only(self):
        """A9 oracle: recompute the probability using only the z-table
        excerpt printed in the problem (Principle 5 end to end)."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_needed_z_in_table_with_decoys(self):
        for _ in range(200):
            result = self.gen.generate()
            mu, sigma, kind, vals, table = parse_problem(result["problem"])
            if kind == "inverse":
                needed = {z for z, probability in table.items()
                          if probability == vals[0]}
            elif kind == "symmetric":
                needed = {abs((vals[1] - mu) / sigma)}
            else:
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
                elif f[0] == "M":
                    self.assertEqual(Decimal(f[1]) * Decimal(f[2]),
                                     Decimal(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(Decimal(f[1]) + Decimal(f[2]),
                                     Decimal(f[3]), s)
                elif f[0] == "TABLE_LOOKUP":
                    # Forward lookups quote the probability; inverse lookups
                    # quote the z value. Either must be visibly supplied.
                    self.assertIn(f[-1], result["problem"], s)

    def test_all_variants_reachable(self):
        ops = set()
        negatives = 0
        for _ in range(300):
            result = self.gen.generate()
            ops.add(result["operation"])
            if any(s.startswith(f"ZSCORE{DELIM}") and "|-" in s
                   for s in result["steps"]):
                negatives += 1
        self.assertEqual(ops, {"normal_below", "normal_above",
                               "normal_between", "normal_inverse_lookup",
                               "normal_symmetric_interval"})
        self.assertGreater(negatives, 10, "symmetry cases should appear")

    def test_fixed_variant_constructor(self):
        gen = NormalTableGenerator("between")
        for _ in range(10):
            self.assertEqual(gen.generate()["operation"], "normal_between")
        with self.assertRaises(ValueError):
            NormalTableGenerator("bogus")

    def test_inverse_lookup_and_symmetric_interval_fixed_variants(self):
        for variant, operation in (("inverse_lookup", "normal_inverse_lookup"),
                                   ("symmetric_interval",
                                    "normal_symmetric_interval")):
            gen = NormalTableGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                self.assertEqual(result["operation"], operation)
                self.assertEqual(result["final_answer"], oracle_answer(result))

    def test_all_variants_have_five_reachable_phrasings(self):
        for variant in NormalTableGenerator.VARIANTS:
            generator = NormalTableGenerator(variant)
            seen = set()
            for _ in range(300):
                problem = generator.generate()["problem"].splitlines()[0]
                for template in QUERIES[variant]:
                    fixed = re.escape(template)
                    fixed = re.sub(r"\\\{(?:x|a|b|lower|upper)\\\}",
                                   r"-?\\d+(?:\\.\\d+)?", fixed)
                    fixed = fixed.replace(r"\{unit\}", r"\S+")
                    fixed = fixed.replace(r"\{probability\}", r"0\.\d{4}")
                    if re.search(fixed + r"$", problem):
                        seen.add(template)
                        break
            self.assertEqual(seen, set(QUERIES[variant]))


if __name__ == "__main__":
    unittest.main()

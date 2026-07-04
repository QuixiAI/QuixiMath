import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.standard_deviation_generator import (
    StandardDeviationGenerator,
)
from helpers import DELIM


def sqrt_val(txt):
    m = re.fullmatch(r"(\d*)(?:√(\d+))?", txt)
    k = int(m.group(1)) if m.group(1) else 1
    return k * math.sqrt(int(m.group(2))) if m.group(2) else float(k)


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    data = [int(v) for v in
            re.search(r"data set: (.+)\. Give", p).group(1)
            .split(", ")]
    n = len(data)
    mean = Fraction(sum(data), n)
    ss = sum((Fraction(v) - mean) ** 2 for v in data)
    if "population variance" in p:
        return Fraction(ans) == ss / n
    if "sample variance" in p:
        return Fraction(ans) == ss / (n - 1)
    return abs(sqrt_val(ans) - math.sqrt(ss / n)) < 1e-9


class TestStandardDeviationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = StandardDeviationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recompute_from_problem(self):
        """A9 oracle: exact variance recomputed from the data."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_deviation_table_complete_and_consistent(self):
        for _ in range(200):
            result = self.gen.generate()
            data = [int(v) for v in
                    re.search(r"data set: (.+)\. Give",
                              result["problem"]).group(1).split(", ")]
            rows = [s.split(DELIM)[1:] for s in result["steps"]
                    if s.startswith(f"DEV_ROW{DELIM}")]
            self.assertEqual(sorted(int(r[0]) for r in rows),
                             sorted(data))
            for x, d, sq in rows:
                self.assertEqual(int(d) ** 2, int(sq))

    def test_mean_always_integer(self):
        for _ in range(300):
            result = self.gen.generate()
            data = [int(v) for v in
                    re.search(r"data set: (.+)\. Give",
                              result["problem"]).group(1).split(", ")]
            self.assertEqual(sum(data) % len(data), 0)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            StandardDeviationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

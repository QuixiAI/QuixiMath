import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.euler_method_generator import EulerMethodGenerator
from generators.exponential_model_generator import dec
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: rerun Euler exactly from the problem text alone."""
    m = re.fullmatch(r"Use Euler's method with step size h = (\S+) to "
                     r"approximate y\((\S+)\) for dy/dx = (.+) "
                     r"with y\(0\) = (\d+)\.", example["problem"])
    h = Fraction(m.group(1))
    target = Fraction(m.group(2))
    f = eval("lambda x, y: " +
             re.sub(r"(\d)([xy])", r"\1*\2", m.group(3)))
    y = Fraction(int(m.group(4)))
    n = target / h
    assert n.denominator == 1
    x = Fraction(0)
    for _ in range(int(n)):
        y = y + h * f(x, y)
        x = x + h
    return dec(y)


class TestEulerMethodGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EulerMethodGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_exact_recomputation(self):
        """A9 oracle: independent exact Euler run matches the answer."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result),
                             result["final_answer"], result["problem"])

    def test_table_rows_match_step_count(self):
        for variant, n in (("two_step", 2), ("three_step", 3)):
            gen = EulerMethodGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                rows = [s for s in result["steps"]
                        if s.startswith(f"TABLE_ENTRY{DELIM}")]
                self.assertEqual(len(rows), n + 1)
                slopes = [s for s in result["steps"]
                          if s.startswith(f"EVAL{DELIM}")]
                self.assertEqual(len(slopes), n)
                # The last table row holds the final answer.
                self.assertEqual(rows[-1].split(DELIM)[2],
                                 f"y = {result['final_answer']}")

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            for bad in (r"(?<!\d)1x", r"(?<!\d)1y", "--", r"\+ -"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            EulerMethodGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

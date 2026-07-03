import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometric_sequence_generator import (
    GeometricSequenceGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    """Independently recomputes from the shown terms alone."""
    p = example["problem"]
    m = re.match(
        r"The geometric (?:sequence|series) (-?\d+), (-?\d+), (-?\d+), "
        r"(-?\d+), \.\.\. continues( forever)?\. (.+)$", p)
    assert m, p
    t = [Fraction(int(m.group(i))) for i in range(1, 5)]
    r = t[1] / t[0]
    assert t[2] / t[1] == r and t[3] / t[2] == r
    q = m.group(6)

    mm = re.fullmatch(r"Find term (\d+)\.", q)
    if mm:
        n = int(mm.group(1))
        return str(t[0] * r ** (n - 1))
    mm = re.fullmatch(r"Find the sum of the first (\d+) terms\.", q)
    if mm:
        n = int(mm.group(1))
        return str(sum(t[0] * r ** i for i in range(n)))
    assert q == "Find the sum of the infinite series."
    assert abs(r) < 1
    return str(t[0] / (1 - r))


class TestGeometricSequenceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GeometricSequenceGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute every variant with exact fractions."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_ratio_computed_and_verified(self):
        for _ in range(300):
            result = self.gen.generate()
            cr = next(s for s in result["steps"]
                      if s.startswith(f"COMMON_RATIO{DELIM}"))
            f = cr.split(DELIM)
            num, den = f[1].split("/", 1)
            self.assertEqual(Fraction(int(num), int(den.strip("()"))),
                             Fraction(f[2]), cr)

    def test_step_arithmetic_exact(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("S", "M", "D") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"S": lambda: x - y, "M": lambda: x * y,
                           "D": lambda: x / y}[f[0]]()
                    self.assertEqual(got, z, s)
                elif f[0] == "E":
                    base = Fraction(f[1].strip("()"))
                    self.assertEqual(base ** int(f[2]), Fraction(f[3]), s)

    def test_infinite_sum_states_convergence(self):
        gen = GeometricSequenceGenerator("infinite_sum")
        for _ in range(200):
            result = gen.generate()
            conv = next(s for s in result["steps"]
                        if s.startswith(f"CONVERGE_CHECK{DELIM}"))
            m = re.fullmatch(r"abs\(r\) = ([\d/]+) < 1",
                             conv.split(DELIM)[1])
            self.assertIsNotNone(m, conv)
            self.assertLess(Fraction(m.group(1)), 1, conv)

    def test_no_pipe_inside_step_fields(self):
        """The delimiter must never appear inside a field's math text."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                op = s.split(DELIM)[0]
                self.assertTrue(op.isupper() and op.replace("_", "").isalpha(),
                                s)

    def test_partial_sum_integer_answers(self):
        gen = GeometricSequenceGenerator("partial_sum")
        for _ in range(200):
            result = gen.generate()
            self.assertNotIn("/", result["final_answer"])

    def test_fraction_answers_occur_for_nth_term(self):
        gen = GeometricSequenceGenerator("nth_term")
        kinds = set()
        for _ in range(200):
            kinds.add("/" in gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"geometric_sequence_nth_term",
                               "geometric_sequence_partial_sum",
                               "geometric_sequence_infinite_sum"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            GeometricSequenceGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

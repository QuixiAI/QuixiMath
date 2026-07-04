import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.polynomial_zeros_generator import PolynomialZerosGenerator
from tests.test_polynomial_long_division_generator import parse_poly
from helpers import DELIM


def parse_zero(text):
    """'x = 3' -> 3+0j; 'x = 2 + 3i' -> 2+3j; 'x = -i' -> -1j."""
    v = text.replace("x = ", "")
    m = re.fullmatch(r"(-?\d+)", v)
    if m:
        return complex(int(v), 0)
    m = re.fullmatch(r"(-?\d+) ([+-]) (?:(\d+))?i", v)
    if m:
        im = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
        return complex(int(m.group(1)), im)
    m = re.fullmatch(r"(-?)(?:(\d+))?i", v)
    assert m, text
    return complex(0, (-1 if m.group(1) == "-" else 1) * int(m.group(2) or 1))


def oracle_check(example):
    """All three claimed zeros satisfy P exactly (complex-int math)."""
    m = re.fullmatch(r"Given that x = (-?\d+) is a zero, find all zeros "
                     r"of P\(x\) = (.+)\.", example["problem"])
    assert m, example["problem"]
    coefs = parse_poly(m.group(2), "x")
    zeros = [parse_zero(z) for z in example["final_answer"].split(", ")]
    if len(zeros) != 3:
        return False
    if complex(int(m.group(1)), 0) not in zeros:
        return False
    for z in zeros:
        val = sum(c * z ** p for p, c in coefs.items())
        if abs(val.real) > 1e-6 or abs(val.imag) > 1e-6:
            return False
    return True


class TestPolynomialZerosGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PolynomialZerosGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_zeros_satisfy(self):
        """A9 oracle: every claimed zero satisfies P."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_deflation_row_ends_in_zero(self):
        for _ in range(300):
            result = self.gen.generate()
            row = next(s for s in result["steps"]
                       if s.startswith(f"SYN_ROW{DELIM}"))
            self.assertTrue(row.split(DELIM)[1].endswith(", 0"), row)
            self.assertIn(f"R{DELIM}0", result["steps"])

    def test_synthetic_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_factorable_real_roots_ascending(self):
        gen = PolynomialZerosGenerator("factorable")
        for _ in range(200):
            result = gen.generate()
            vals = [int(v.replace("x = ", ""))
                    for v in result["final_answer"].split(", ")]
            self.assertEqual(vals, sorted(vals))
            self.assertTrue(any(s.startswith(f"ACCEPT{DELIM}")
                                for s in result["steps"]))

    def test_complex_variant_conjugate_pair(self):
        gen = PolynomialZerosGenerator("complex")
        for _ in range(200):
            result = gen.generate()
            zeros = [parse_zero(z)
                     for z in result["final_answer"].split(", ")]
            self.assertEqual(zeros[1].conjugate(), zeros[2],
                             result["final_answer"])
            self.assertGreater(zeros[1].imag, 0)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(100):
            kinds.add("i" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PolynomialZerosGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

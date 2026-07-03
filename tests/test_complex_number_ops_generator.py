import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.complex_number_ops_generator import (
    ComplexNumberOpsGenerator,
)
from helpers import DELIM


def parse_cx(text):
    """'5 - 3i', '-i', '7', '4i' -> complex."""
    t = text.strip()
    m = re.fullmatch(r"(-?\d+) ([+-]) (?:(\d+))?i", t)
    if m:
        im = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
        return complex(int(m.group(1)), im)
    m = re.fullmatch(r"(-?)(?:(\d+))?i", t)
    if m:
        sign = -1 if m.group(1) == "-" else 1
        return complex(0, sign * int(m.group(2) or 1))
    return complex(int(t), 0)


def oracle_value(example):
    """Independently computes the exact complex value from the text."""
    p = example["problem"]
    m = re.fullmatch(r"Simplify: i\^(\d+)\.", p)
    if m:
        return 1j ** int(m.group(1))
    m = re.fullmatch(r"(?:Add|Subtract): \((.+?)\) ([+-]) \((.+?)\)\.", p)
    if m:
        z1, z2 = parse_cx(m.group(1)), parse_cx(m.group(3))
        return z1 + z2 if m.group(2) == "+" else z1 - z2
    m = re.fullmatch(r"Multiply: \((.+?)\)\((.+?)\)\.", p)
    assert m, p
    return parse_cx(m.group(1)) * parse_cx(m.group(2))


class TestComplexNumberOpsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ComplexNumberOpsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_value_from_problem_text(self):
        """A9 oracle: the answer parses to the true complex value."""
        for _ in range(600):
            result = self.gen.generate()
            want = oracle_value(result)
            got = parse_cx(result["final_answer"])
            self.assertAlmostEqual(got.real, want.real, msg=result)
            self.assertAlmostEqual(got.imag, want.imag, msg=result)

    def test_power_reduction_steps(self):
        gen = ComplexNumberOpsGenerator("power_i")
        for _ in range(200):
            result = gen.generate()
            n = int(re.search(r"i\^(\d+)", result["problem"]).group(1))
            d = next(s.split(DELIM) for s in result["steps"]
                     if s.startswith(f"D{DELIM}"))
            r = next(s.split(DELIM) for s in result["steps"]
                     if s.startswith(f"R{DELIM}"))
            self.assertEqual(int(d[3]) * 4 + int(r[1]), n)
            self.assertLess(int(r[1]), 4)

    def test_multiply_foil_and_i_square(self):
        gen = ComplexNumberOpsGenerator("multiply")
        for _ in range(300):
            result = gen.generate()
            f = {}
            for s in result["steps"]:
                parts = s.split(DELIM)
                f[parts[0]] = parts
            fv = int(f["FOIL_F"][2])
            lv = int(f["FOIL_L"][2].replace("i^2", ""))
            self.assertEqual(int(f["I_SQUARE"][2]), -lv, f["I_SQUARE"])
            adds = [s.split(DELIM) for s in result["steps"]
                    if s.startswith(f"A{DELIM}")]
            self.assertEqual(int(adds[0][1]), fv)  # first A combines reals
            # arithmetic of the two A steps
            for s in result["steps"]:
                parts = s.split(DELIM)
                if parts[0] == "A":
                    self.assertEqual(int(parts[1]) + int(parts[2]),
                                     int(parts[3]), s)

    def test_standard_form_rendering(self):
        for _ in range(400):
            result = self.gen.generate()
            a = result["final_answer"]
            self.assertNotIn("+ -", a)
            self.assertNotIn("- -", a)
            self.assertNotRegex(a, r"(?<!\d)1i", a)  # unit coef is bare i

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"complex_power_i", "complex_add",
                               "complex_subtract", "complex_multiply"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ComplexNumberOpsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

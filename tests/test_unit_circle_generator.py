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

from generators.unit_circle_generator import UnitCircleGenerator
from helpers import DELIM


def exact_to_float(txt):
    """'-√3/2' -> -0.866..., '1/2' -> 0.5, '√3' -> 1.732..., '0' -> 0."""
    t = txt.strip()
    sign = 1.0
    if t.startswith("-"):
        sign = -1.0
        t = t[1:]
    m = re.fullmatch(r"√(\d+)(?:/(\d+))?", t)
    if m:
        return sign * math.sqrt(int(m.group(1))) / int(m.group(2) or 1)
    m = re.fullmatch(r"(\d+)/(\d+)", t)
    if m:
        return sign * int(m.group(1)) / int(m.group(2))
    return sign * float(t)


def parse_angle(expr):
    """'sin 210°' or 'cos(5π/6)' -> (fn, degrees)."""
    m = re.fullmatch(r"(sin|cos|tan) (\d+)°", expr)
    if m:
        return m.group(1), int(m.group(2))
    m = re.fullmatch(r"(sin|cos|tan)\((?:(\d+))?π(?:/(\d+))?\)", expr)
    assert m, expr
    fr = Fraction(int(m.group(2) or 1), int(m.group(3) or 1))
    return m.group(1), int(fr * 180)


def oracle_check(example):
    """Numeric verification with math.sin/cos/tan/asin/acos/atan."""
    p = example["problem"]
    m = re.fullmatch(r"Find the exact value of (.+)\.", p)
    if m:
        fn, deg = parse_angle(m.group(1))
        want = {"sin": math.sin, "cos": math.cos,
                "tan": math.tan}[fn](math.radians(deg))
        got = exact_to_float(example["final_answer"])
        return abs(got - want) < 1e-9
    m = re.fullmatch(r"Evaluate (arcsin|arccos|arctan)\((.+)\)\. Give "
                     r"the answer in degrees\.", p)
    assert m, p
    fn, val = m.group(1), exact_to_float(m.group(2))
    want = math.degrees({"arcsin": math.asin, "arccos": math.acos,
                         "arctan": math.atan}[fn](val))
    got = float(example["final_answer"].rstrip("°"))
    return abs(got - want) < 1e-9


class TestUnitCircleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = UnitCircleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_verification(self):
        """A9 oracle: every exact answer matches math.* numerically."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_reference_angle_procedure(self):
        gen = UnitCircleGenerator("evaluate")
        for _ in range(300):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            if "QUADRANT" in ops:
                self.assertIn("SIGN_RULE", ops)
                self.assertIn("TABLE_LOOKUP", ops)
                self.assertLess(ops.index("QUADRANT"),
                                ops.index("SIGN_RULE"))
            else:
                self.assertIn("UC_POINT", ops)

    def test_inverse_answers_in_principal_range(self):
        gen = UnitCircleGenerator("inverse")
        for _ in range(300):
            result = gen.generate()
            ans = int(result["final_answer"].rstrip("°"))
            if "arcsin" in result["problem"]:
                self.assertTrue(-90 <= ans <= 90)
            elif "arccos" in result["problem"]:
                self.assertTrue(0 <= ans <= 180)
            else:
                self.assertTrue(-90 < ans < 90)

    def test_radian_inputs_occur_and_convert(self):
        gen = UnitCircleGenerator("evaluate")
        found = False
        for _ in range(200):
            result = gen.generate()
            if "π" in result["problem"]:
                found = True
                self.assertTrue(any(s.startswith(f"M{DELIM}")
                                    for s in result["steps"]))
        self.assertTrue(found)

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"unit_circle_evaluate",
                               "unit_circle_inverse"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            UnitCircleGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

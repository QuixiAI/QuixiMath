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

from generators.trig_identity_eval_generator import (
    TrigIdentityEvalGenerator,
)
from helpers import DELIM


def exact_to_float(txt):
    """'(√6 - √2)/4', '-(√6 + √2)/4', '24/25' -> float."""
    t = txt.strip()
    sign = 1.0
    if t.startswith("-"):
        sign, t = -1.0, t[1:]
    m = re.fullmatch(r"\(√(\d+) ([+-]) √(\d+)\)/(\d+)", t)
    if m:
        a = math.sqrt(int(m.group(1)))
        b = math.sqrt(int(m.group(3)))
        s = 1 if m.group(2) == "+" else -1
        return sign * (a + s * b) / int(m.group(4))
    return sign * float(Fraction(t))


def oracle_check(example):
    p = example["problem"]
    m = re.fullmatch(r"Find the exact value of (sin|cos) (\d+)° using a "
                     r"sum or difference identity\.", p)
    if m:
        fn, deg = m.group(1), int(m.group(2))
        want = {"sin": math.sin, "cos": math.cos}[fn](math.radians(deg))
        return abs(exact_to_float(example["final_answer"]) - want) < 1e-9
    m = re.fullmatch(r"Given sin θ = (-?\d+/\d+) with θ in quadrant "
                     r"(\w+), find sin 2θ and cos 2θ\.", p)
    if m:
        s = Fraction(m.group(1))
        q = {"I": 1, "II": 2, "III": 3, "IV": 4}[m.group(2)]
        cs = 1 if q in (1, 4) else -1
        c2 = 1 - s * s
        c = cs * Fraction(c2.numerator, c2.denominator) ** Fraction(1)
        # exact cos from the triple
        import math as _m
        num = _m.isqrt(c2.numerator)
        den = _m.isqrt(c2.denominator)
        assert num * num == c2.numerator and den * den == c2.denominator
        cos_v = Fraction(cs * num, den)
        want = (f"sin 2θ = {2 * s * cos_v}; "
                f"cos 2θ = {1 - 2 * s ** 2}")
        return example["final_answer"] == want
    m = re.fullmatch(r"Given cos θ = (-?\d+/\d+) with 0° < θ < 180°, "
                     r"find sin\(θ/2\) and cos\(θ/2\)\. \(θ/2 is in the "
                     r"first quadrant\.\)", p)
    assert m, p
    ct = Fraction(m.group(1))
    import math as _m
    s2 = (1 - ct) / 2
    c2 = (1 + ct) / 2
    sn = _m.isqrt(s2.numerator)
    sd = _m.isqrt(s2.denominator)
    cn = _m.isqrt(c2.numerator)
    cd = _m.isqrt(c2.denominator)
    assert sn * sn == s2.numerator and cn * cn == c2.numerator
    want = (f"sin(θ/2) = {Fraction(sn, sd)}; "
            f"cos(θ/2) = {Fraction(cn, cd)}")
    return example["final_answer"] == want


class TestTrigIdentityEvalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TrigIdentityEvalGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_verification(self):
        """A9 oracle: numeric for sum/diff, exact for double/half."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_identity_always_cited(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"THEOREM{DELIM}")
                                for s in result["steps"]))

    def test_step_arithmetic_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("M", "S", "A", "D", "E") and len(f) == 4 \
                        and "√" not in s and "θ" not in s:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"M": lambda: x * y, "S": lambda: x - y,
                           "A": lambda: x + y, "D": lambda: x / y,
                           "E": lambda: x ** int(f[2])}[f[0]]()
                    self.assertEqual(got, z, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            TrigIdentityEvalGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

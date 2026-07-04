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

from generators.taylor_series_generator import TaylorSeriesGenerator
from helpers import DELIM

FUNCS = {
    "e^x": math.exp,
    "sin(x)": math.sin,
    "cos(x)": math.cos,
    "ln(1 + x)": lambda x: math.log(1 + x),
    "1/(1 - x)": lambda x: 1 / (1 - x),
    "ln(x)": math.log,
    "1/x": lambda x: 1 / x,
}


def poly_eval(ptxt, x, center=0.0):
    s = ptxt.replace("(x - 1)", "u").replace("x", "u")
    s = s.replace("^", "**")
    s = re.sub(r"(\d)u", r"\1*u", s)
    return eval(s, {"u": x - center})


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    m = re.fullmatch(r"Find the Maclaurin polynomial of degree (\d+) "
                     r"for f\(x\) = (.+)\.", p)
    if m:
        deg, f = int(m.group(1)), FUNCS[m.group(2)]
        h = 0.05
        return all(abs(poly_eval(ans, x) - f(x)) < 2 * h ** (deg + 1)
                   for x in (h, -h))
    m = re.fullmatch(r"Find the Taylor polynomial of degree (\d+) for "
                     r"f\(x\) = (.+) centered at a = 1\.", p)
    if m:
        deg, f = int(m.group(1)), FUNCS[m.group(2)]
        h = 0.05
        return all(abs(poly_eval(ans, x, 1.0) - f(x)) <
                   2 * h ** (deg + 1)
                   for x in (1 + h, 1 - h))
    m = re.fullmatch(r"Use the degree-(\d+) Maclaurin polynomial of "
                     r"f\(x\) = (.+) to approximate (.+)\.", p)
    if m:
        deg, fname = int(m.group(1)), m.group(2)
        target = m.group(3)
        mm = re.fullmatch(r"(?:e\^|sin\(|cos\(|ln\()(-?[\d.]+)\)?",
                          target)
        v = float(mm.group(1))
        x = v - 1 if fname == "ln(1 + x)" else v
        f = FUNCS[fname]
        got = float(Fraction(ans))
        return (abs(got - f(x)) < abs(x) ** (deg + 1) and
                abs(got - f(x)) > 0)
    m = re.fullmatch(r"The Taylor polynomial P_(\d+) of f\(x\) = (.+) "
                     r"around 0 is used at x = (\S+)\. Bound the "
                     r"error with the Lagrange remainder\.( Use "
                     r"M = 3 .*)?", p)
    assert m, p
    n, fname = int(m.group(1)), m.group(2)
    x = Fraction(m.group(3))
    M = 3 if fname == "e^x" else 1
    want = Fraction(M) * x ** (n + 1) / math.factorial(n + 1)
    if Fraction(ans) != want:
        return False
    # The bound must actually dominate the true error.
    f = FUNCS[fname]
    xf = float(x)
    approx = sum((xf ** k / math.factorial(k)) *
                 {"e^x": 1,
                  "sin(x)": [0, 1, 0, -1][k % 4],
                  "cos(x)": [1, 0, -1, 0][k % 4]}[fname]
                 for k in range(n + 1))
    return abs(f(xf) - approx) <= float(want) + 1e-12


class TestTaylorSeriesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TaylorSeriesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: numeric agreement with the true function."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_derivative_table_present_for_construction(self):
        for v in ("maclaurin", "centered"):
            gen = TaylorSeriesGenerator(v)
            for _ in range(50):
                result = gen.generate()
                rows = [s for s in result["steps"]
                        if s.startswith(f"TABLE_ENTRY{DELIM}")]
                deg = int(re.search(r"degree (\d+)",
                                    result["problem"]).group(1))
                self.assertEqual(len(rows), deg + 1)

    def test_error_bound_informative(self):
        gen = TaylorSeriesGenerator("error_bound")
        for _ in range(100):
            result = gen.generate()
            self.assertLessEqual(Fraction(result["final_answer"]), 1)

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            for bad in (r"(?<!\d)1x", "--", r"\+ -", r"\^1\b",
                        r"(?<!\d)1\(x"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            TaylorSeriesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

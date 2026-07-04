import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.trig_equation_generator import TrigEquationGenerator
from helpers import DELIM

SPECIAL = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270,
           300, 315, 330]


def radical_to_float(txt):
    t = txt.strip()
    sign = -1.0 if t.startswith("-") else 1.0
    t = t.lstrip("-")
    m = re.fullmatch(r"√(\d+)(?:/(\d+))?", t)
    if m:
        return sign * math.sqrt(int(m.group(1))) / int(m.group(2) or 1)
    m = re.fullmatch(r"(\d+)/(\d+)", t)
    if m:
        return sign * int(m.group(1)) / int(m.group(2))
    return sign * float(t)


def eq_residual(eq_text, deg):
    """Evaluates the equation's left side at deg (degrees)."""
    x = math.radians(deg)
    s = eq_text.replace(" = 0", "")
    for fn, f in (("sin", math.sin), ("cos", math.cos),
                  ("tan", math.tan)):
        s = re.sub(rf"(\d*)\s*{fn}\^2 x",
                   lambda m, f=f: f"({m.group(1) or 1}*{f(x)**2})", s)
        s = re.sub(rf"(\d*)\s*{fn} x",
                   lambda m, f=f: f"({m.group(1) or 1}*{f(x)})", s)
    s = re.sub(r"√(\d+)", lambda m: str(math.sqrt(int(m.group(1)))), s)
    return eval(s)


def oracle_check(example):
    """Every claimed solution satisfies the equation; every special
    angle that satisfies it is claimed (completeness)."""
    m = re.fullmatch(r"Solve (.+) for 0° ≤ x < 360°\.",
                     example["problem"])
    eq = m.group(1)
    if "= 0" not in eq:
        eq += " - 0"  # 'tan x = 0' form
        eq = eq.replace(" = 0 - 0", " = 0")
    if not eq.endswith("= 0"):
        eq = eq.replace(" = ", " - ") + " = 0"
    claimed = sorted(int(v) for v in
                     re.findall(r"(\d+)°", example["final_answer"]))
    true_sols = []
    for d in SPECIAL:
        if d in (90, 270) and "tan" in eq:
            continue
        if abs(eq_residual(eq, d)) < 1e-9:
            true_sols.append(d)
    return claimed == true_sols


class TestTrigEquationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TrigEquationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_solutions_correct_and_complete(self):
        """A9 oracle: brute-force all special angles numerically."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_solutions_ascending(self):
        for _ in range(300):
            result = self.gen.generate()
            vals = [int(v) for v in
                    re.findall(r"(\d+)°", result["final_answer"])]
            self.assertEqual(vals, sorted(vals))

    def test_quadratic_factors_and_splits(self):
        gen = TrigEquationGenerator("quadratic")
        for _ in range(200):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertIn("ZERO_PRODUCT", ops)
            self.assertIn("SUBST", ops)
            self.assertGreaterEqual(ops.count("SOLUTIONS"), 2)

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"trig_equation_linear",
                               "trig_equation_quadratic"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            TrigEquationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

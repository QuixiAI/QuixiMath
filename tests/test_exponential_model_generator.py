import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.exponential_model_generator import (
    ExponentialModelGenerator,
    dec,
)
from helpers import DELIM


def oracle_answer(example):
    """Recomputes each model exactly from the problem text."""
    p = example["problem"]
    m = re.fullmatch(r"An investment of \$(\d+) grows (\d+)% per year\. "
                     r"What is it worth after (\d+) years\?", p)
    if m:
        P, r, t = (int(v) for v in m.groups())
        return _money(P * (1 + Fraction(r, 100)) ** t)
    m = re.fullmatch(r"A machine worth \$(\d+) loses (\d+)% of its value "
                     r"each year\. What is it worth after (\d+) years\?", p)
    if m:
        P, r, t = (int(v) for v in m.groups())
        return _money(P * (1 - Fraction(r, 100)) ** t)
    m = re.fullmatch(r"A sample of (\d+) g has a half-life of (\d+) "
                     r"years\. How much remains after (\d+) years\?", p)
    if m:
        m0, h, t = (int(v) for v in m.groups())
        assert t % h == 0
        return f"{m0 // 2 ** (t // h)} g"
    m = re.fullmatch(r"An investment of \$(\d+) earns (\d+)% interest "
                     r"compounded continuously\. Give its exact value "
                     r"in dollars after (\d+) years\.", p)
    assert m, p
    P, r, t = (int(v) for v in m.groups())
    return f"{P}e^{dec(Fraction(r * t, 100))}"


def _money(fr):
    cents = fr * 100
    assert cents.denominator == 1
    c = cents.numerator
    return f"${c // 100}.{c % 100:02d}"


class TestExponentialModelGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ExponentialModelGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute every model exactly."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic_exact(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("A", "S", "M", "D", "E") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"A": lambda: x + y, "S": lambda: x - y,
                           "M": lambda: x * y, "D": lambda: x / y,
                           "E": lambda: x ** int(f[2])}[f[0]]()
                    self.assertEqual(got, z, s)

    def test_half_life_halves_step_by_step(self):
        gen = ExponentialModelGenerator("half_life")
        for _ in range(200):
            result = gen.generate()
            divs = [s.split(DELIM) for s in result["steps"]
                    if s.startswith(f"D{DELIM}")]
            k = int(divs[0][3])  # first D is t/h
            self.assertEqual(len(divs) - 1, k, result["steps"])
            for d in divs[1:]:
                self.assertEqual(d[2], "2", d)

    def test_continuous_answers_stay_exact(self):
        gen = ExponentialModelGenerator("continuous")
        for _ in range(200):
            result = gen.generate()
            self.assertRegex(result["final_answer"], r"^\d+e\^[\d.]+$")
            self.assertNotIn("..", result["final_answer"])

    def test_money_answers_have_two_decimals(self):
        for v in ("growth", "decay"):
            gen = ExponentialModelGenerator(v)
            for _ in range(150):
                result = gen.generate()
                self.assertRegex(result["final_answer"], r"^\$\d+\.\d\d$")

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"exponential_growth", "exponential_decay",
                               "exponential_half_life",
                               "exponential_continuous"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ExponentialModelGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

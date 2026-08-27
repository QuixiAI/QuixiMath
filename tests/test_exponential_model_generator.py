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


GROWTH_WORDS = ("grows", "appreciates", "increases", "rises", "gains")
DECAY_WORDS = ("loses", "depreciates", "declines", "drops", "falls")


def oracle_answer(example):
    """A9 oracle: recompute every model exactly from the problem text.

    Parses whatever phrasing was chosen, then rebuilds the answer with
    exact Fraction arithmetic (repeated halving for half-life, a direct
    power for compound growth/decay).
    """
    p = example["problem"]

    if "half-life" in p:
        h = int(re.search(r"half-life[^\d]*(\d+)", p).group(1))
        m_txt, unit = re.search(r"(\d+) (mg|kg|g)\b", p).groups()
        tu = re.search(r"\d+ (years|days|hours)", p).group(1)
        times = [int(v) for v in re.findall(rf"(\d+) {tu}\b", p)]
        elapsed = {v for v in times if v != h}
        assert len(elapsed) == 1, p
        t = elapsed.pop()
        assert t % h == 0, p
        remaining = int(m_txt)
        for _ in range(t // h):
            assert remaining % 2 == 0, p
            remaining //= 2
        return f"{remaining} {unit}"

    P = int(re.search(r"\$(\d+)", p).group(1))
    r = int(re.search(r"(\d+)%", p).group(1))
    t = int(re.search(r"(\d+) years", p).group(1))

    if "continuously" in p:
        return f"{P}e^{dec(Fraction(r * t, 100))}"

    grew = any(w in p for w in GROWTH_WORDS)
    fell = any(w in p for w in DECAY_WORDS)
    assert grew != fell, p
    base = 1 + Fraction(r, 100) * (1 if grew else -1)
    return _money(P * base ** t)


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

    def test_every_phrasing_is_parsed(self):
        """All phrasings must round-trip through the independent parser."""
        seen = set()
        for _ in range(1500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])
            seen.add(result["problem"].split()[0])
        self.assertGreaterEqual(len(seen), 8)

    def test_every_variant_oracle(self):
        for variant in ExponentialModelGenerator.VARIANTS:
            gen = ExponentialModelGenerator(variant)
            for _ in range(300):
                result = gen.generate()
                self.assertEqual(oracle_answer(result),
                                 result["final_answer"], result["problem"])

    def test_pipe_safety(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)), 5, s)

    def test_half_life_answer_units(self):
        gen = ExponentialModelGenerator("half_life")
        units = set()
        for _ in range(300):
            result = gen.generate()
            self.assertRegex(result["final_answer"], r"^\d+ (mg|kg|g)$")
            units.add(result["final_answer"].split()[1])
        self.assertEqual(units, {"g", "mg", "kg"})

    def test_determinism_under_seed(self):
        random.seed(23)
        first = [self.gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [self.gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ExponentialModelGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

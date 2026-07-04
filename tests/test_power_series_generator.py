import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.power_series_generator import PowerSeriesGenerator
from helpers import DELIM

_cache = {}


def parse_center(x_txt):
    if x_txt == "x":
        return 0
    m = re.fullmatch(r"\(x ([+-]) (\d+)\)", x_txt)
    return -int(m.group(2)) if m.group(1) == "+" else int(m.group(2))


def make_mult(body):
    """Return (a, mult(n, u)) where t_{n+1} = t_n * mult and u = x-a."""
    m = re.fullmatch(r"n!·(.+)\^n", body)
    if m:
        return parse_center(m.group(1)), lambda n, u: (n + 1) * u
    m = re.fullmatch(r"(.+)\^n/n!", body)
    if m:
        return parse_center(m.group(1)), lambda n, u: u / (n + 1)
    m = re.fullmatch(r"(.+)\^n/\(n·(\d+)\^n\)", body)
    if m:
        c = int(m.group(2))
        return (parse_center(m.group(1)),
                lambda n, u: u / c * n / (n + 1))
    m = re.fullmatch(r"(.+)\^n/\(n\^2·(\d+)\^n\)", body)
    if m:
        c = int(m.group(2))
        return (parse_center(m.group(1)),
                lambda n, u: u / c * (n / (n + 1)) ** 2)
    m = re.fullmatch(r"(.+)\^n/(\d+)\^n", body)
    c = int(m.group(2))
    return parse_center(m.group(1)), lambda n, u: u / c


def converges_at(mult, a, x):
    """Numeric verdict: iterate terms and check tail behavior."""
    u = x - a
    t, s = u, u
    s_mid = None
    for n in range(1, 4001):
        t = t * mult(n, u)
        if abs(t) > 1e12:
            return False
        s += t
        if n == 2000:
            s_mid = s
    if abs(t) > 1e-2:
        return False
    return abs(s - s_mid) < 0.05


def oracle_check(example):
    key = example["problem"]
    if key in _cache:
        return _cache[key] == example["final_answer"]
    m = re.fullmatch(r"Find the radius and interval of convergence "
                     r"of Σ (.+) for n ≥ 1\.", key)
    a, mult = make_mult(m.group(1))
    ans = example["final_answer"]
    _cache[key] = ans
    if ans == "R = ∞, (-∞, ∞)":
        return all(converges_at(mult, a, x)
                   for x in (a - 9.5, a + 3.5, a + 20.5))
    m = re.fullmatch(r"R = 0, x = (-?\d+) only", ans)
    if m:
        return (int(m.group(1)) == a and
                not converges_at(mult, a, a + 0.5) and
                not converges_at(mult, a, a - 0.5))
    m = re.fullmatch(r"R = (\d+), ([\[\(])(-?\d+), (-?\d+)([\]\)])",
                     ans)
    if not m:
        return False
    R = int(m.group(1))
    lo, hi = int(m.group(3)), int(m.group(4))
    if lo != a - R or hi != a + R:
        return False
    checks = [
        converges_at(mult, a, a + 0.5 * R),
        not converges_at(mult, a, a + 1.5 * R),
        converges_at(mult, a, lo) == (m.group(2) == "["),
        converges_at(mult, a, hi) == (m.group(5) == "]"),
    ]
    return all(checks)


class TestPowerSeriesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PowerSeriesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_convergence(self):
        """A9 oracle: numeric convergence at interior, exterior, and
        endpoint sample points confirms R and both brackets."""
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_endpoints_checked_for_finite_radius(self):
        for v in ("open", "half_open", "closed"):
            gen = PowerSeriesGenerator(v)
            for _ in range(50):
                result = gen.generate()
                subs = [s for s in result["steps"]
                        if s.startswith(f"SUBST{DELIM}")]
                self.assertEqual(len(subs), 2, result["steps"])

    def test_all_bracket_types_occur(self):
        kinds = set()
        for _ in range(300):
            ans = self.gen.generate()["final_answer"]
            kinds.add((ans[-1], "[" in ans, "only" in ans,
                       "∞" in ans))
        self.assertGreaterEqual(len(kinds), 5)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(250):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PowerSeriesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

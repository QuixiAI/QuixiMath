import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rational_function_features_generator import (
    RationalFunctionFeaturesGenerator,
)
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def int_roots(coefs):
    return sorted(t for t in range(-30, 31) if poly_value(coefs, t) == 0)


def oracle_answer(example):
    """Recomputes VA/hole/HA from the function text alone."""
    m = re.fullmatch(
        r"Find the vertical asymptotes, holes, and horizontal asymptote "
        r"of [a-z]\(([a-z])\) = \((.+)\)/\((.+)\)\.", example["problem"])
    assert m, example["problem"]
    var, num_t, den_t = m.groups()
    num = parse_poly(num_t, var)
    den = parse_poly(den_t, var)
    nroots = set(int_roots(num))
    droots = set(int_roots(den))
    holes = sorted(nroots & droots)
    vas = sorted(droots - nroots)
    ndeg, ddeg = max(num), max(den)
    if ndeg < ddeg:
        ha = "y = 0"
    else:
        ha = f"y = {Fraction(num[ndeg], den[ddeg])}"

    parts = []
    if vas:
        parts.append("VA: " + ", ".join(f"{var} = {v}" for v in vas))
    for h in holes:
        parts.append(f"hole at {var} = {h}")
    parts.append(f"HA: {ha}")
    return "; ".join(parts)


class TestRationalFunctionFeaturesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RationalFunctionFeaturesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute all features independently."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_va_steps_match_answer(self):
        for _ in range(300):
            result = self.gen.generate()
            vas = [s.split(DELIM)[1] for s in result["steps"]
                   if s.startswith(f"VA{DELIM}")]
            for v in vas:
                self.assertIn(v, result["final_answer"])
            m = re.search(r"VA: ([^;]+)", result["final_answer"])
            self.assertEqual(len(m.group(1).split(", ")), len(vas))

    def test_hole_variant_cancels_before_declaring(self):
        gen = RationalFunctionFeaturesGenerator("hole")
        for _ in range(200):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertIn("CANCEL", ops)
            self.assertIn("HOLE", ops)
            self.assertLess(ops.index("CANCEL"), ops.index("HOLE"))
            hole = next(s for s in result["steps"]
                        if s.startswith(f"HOLE{DELIM}"))
            self.assertIn(f"hole at {hole.split(DELIM)[1]}",
                          result["final_answer"])

    def test_degree_compare_precedes_ha(self):
        for _ in range(200):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertLess(ops.index("DEGREE_COMPARE"), ops.index("HA"))

    def test_ha_ratio_is_reduced_fraction(self):
        gen = RationalFunctionFeaturesGenerator("ha_ratio")
        for _ in range(200):
            result = gen.generate()
            m = re.search(r"HA: y = (\d+)/(\d+)", result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])
            n, d = int(m.group(1)), int(m.group(2))
            self.assertEqual(str(Fraction(n, d)), f"{n}/{d}")

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(150):
            a = self.gen.generate()["final_answer"]
            if "hole" in a:
                kinds.add("hole")
            elif "y = 0" in a:
                kinds.add("va_ha")
            else:
                kinds.add("ha_ratio")
        self.assertEqual(kinds, {"hole", "va_ha", "ha_ratio"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RationalFunctionFeaturesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

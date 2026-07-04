import unittest
import random
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.place_value_rounding_generator import PlaceValueRoundingGenerator
from helpers import DELIM


class TestPlaceValueRoundingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = PlaceValueRoundingGenerator()

    def test_rounding_format(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        # Ensure final answer parses as float or int
        try:
            float(res["final_answer"])
        except ValueError:
            self.fail("Final answer not numeric")


    def test_oracle_half_up_rounding(self):
        """A9 oracle: recompute with explicit half-up Decimal rounding —
        catches float/banker's-rounding regressions on tie digits."""
        import re
        from decimal import Decimal, ROUND_HALF_UP
        gen = PlaceValueRoundingGenerator()
        quanta = {"10": Decimal(10), "100": Decimal(100),
                  "1000": Decimal(1000), "tenth": Decimal("0.1"),
                  "hundredth": Decimal("0.01")}
        for _ in range(500):
            res = gen.generate()
            value, target = re.match(
                r"Round ([\d.]+) to the nearest (\w+)", res["problem"]).groups()
            q = quanta[target]
            expected = (Decimal(value) / q).quantize(
                Decimal(1), rounding=ROUND_HALF_UP) * q
            self.assertEqual(Decimal(res["final_answer"]), expected,
                             res["problem"])
            self.assertNotRegex(res["final_answer"], r"\.\d*0$")


if __name__ == "__main__":
    unittest.main()

import unittest
import random
import re
import sys
import os
from fractions import Fraction

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.unit_conversion_generator import (
    UnitConversionGenerator, LENGTH, WEIGHT, TIME, MONEY,
)
from helpers import DELIM

FACTORS = {}
for _f, _t, _k in LENGTH + WEIGHT + TIME + MONEY:
    FACTORS[(_f, _t)] = Fraction(_k)
    FACTORS[(_t, _f)] = Fraction(1, _k)


class TestUnitConversionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = UnitConversionGenerator()

    def test_oracle_both_directions(self):
        """A9 oracle: apply the known unit factor to the parsed value;
        small->big conversions must divide exactly (integer answers)."""
        directions = set()
        for _ in range(500):
            res = self.gen.generate()
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            value, from_u, to_u = re.fullmatch(
                r"Convert (\d+) (\S+) to (\S+)", res["problem"]).groups()
            expected = int(value) * FACTORS[(from_u, to_u)]
            answer_num, answer_unit = res["final_answer"].rsplit(" ", 1)
            self.assertEqual(answer_unit, to_u)
            self.assertEqual(Fraction(answer_num), expected, res["problem"])
            self.assertEqual(expected.denominator, 1, "non-integer result")
            directions.add("reduce" if FACTORS[(from_u, to_u)] < 1 else "expand")
        self.assertEqual(directions, {"expand", "reduce"})


if __name__ == "__main__":
    unittest.main()

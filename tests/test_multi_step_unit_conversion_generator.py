import re
import unittest
from fractions import Fraction
from unittest.mock import patch

from generators.multi_step_unit_conversion_generator import (
    MultiStepUnitConversionGenerator, LENGTH_BASE,
)
from helpers import DELIM

FACTORS = {}
for _f, _t, _k in LENGTH_BASE:
    FACTORS[(_f, _t)] = Fraction(_k)
    FACTORS[(_t, _f)] = Fraction(1, _k)


class TestMultiStepUnitConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MultiStepUnitConversionGenerator()

    def _count_steps(self, steps, opcode):
        return sum(1 for s in steps if s.startswith(f"{opcode}{DELIM}"))

    def test_area_conversion_steps(self):
        with patch("generators.multi_step_unit_conversion_generator.random.choice", side_effect=[("m", "cm", 100), "area"]), \
             patch("generators.multi_step_unit_conversion_generator.random.random", return_value=0.1), \
             patch("generators.multi_step_unit_conversion_generator.random.randint", return_value=3):
            res = self.gen.generate()

        self.assertEqual(res["operation"], "convert_area")
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 2)
        self.assertEqual(self._count_steps(res["steps"], "M"), 2)
        self.assertIn("cm^2", res["final_answer"])
        self.assertEqual(res["final_answer"], "30000 cm^2")

    def test_volume_conversion_steps(self):
        with patch("generators.multi_step_unit_conversion_generator.random.choice", side_effect=[("ft", "in", 12), "volume"]), \
             patch("generators.multi_step_unit_conversion_generator.random.random", return_value=0.1), \
             patch("generators.multi_step_unit_conversion_generator.random.randint", return_value=2):
            res = self.gen.generate()

        self.assertEqual(res["operation"], "convert_volume")
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 3)
        self.assertEqual(self._count_steps(res["steps"], "M"), 3)
        self.assertIn("in^3", res["final_answer"])
        # 2 * 12^3 = 3456
        self.assertEqual(res["final_answer"], "3456 in^3")

    def test_reduce_direction_divides(self):
        with patch("generators.multi_step_unit_conversion_generator.random.choice", side_effect=[("m", "cm", 100), "area"]), \
             patch("generators.multi_step_unit_conversion_generator.random.random", return_value=0.9), \
             patch("generators.multi_step_unit_conversion_generator.random.randint", return_value=3):
            res = self.gen.generate()
        # 3 m^2 -> constructed problem is 30000 cm^2 back to 3 m^2
        self.assertEqual(res["final_answer"], "3 m^2")
        self.assertEqual(self._count_steps(res["steps"], "D"), 2)

    def test_oracle_both_directions(self):
        """A9 oracle: value * factor^power, exact integers both ways."""
        directions = set()
        for _ in range(500):
            res = self.gen.generate()
            value, from_u, power, to_u = re.fullmatch(
                r"Convert (\d+) (\S+)\^(\d) to (\S+)\^\d",
                res["problem"]).groups()
            expected = int(value) * FACTORS[(from_u, to_u)] ** int(power)
            answer_num = res["final_answer"].split(" ")[0]
            self.assertEqual(Fraction(answer_num), expected, res["problem"])
            self.assertEqual(expected.denominator, 1)
            directions.add("reduce" if FACTORS[(from_u, to_u)] < 1 else "expand")
        self.assertEqual(directions, {"expand", "reduce"})


if __name__ == "__main__":
    unittest.main()

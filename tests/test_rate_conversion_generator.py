import unittest
from unittest.mock import patch

from generators.rate_conversion_generator import RateConversionGenerator
from helpers import DELIM


class TestRateConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RateConversionGenerator()

    def _count_steps(self, steps, opcode):
        return sum(1 for s in steps if s.startswith(f"{opcode}{DELIM}"))

    def test_mph_to_ft_s(self):
        with patch("generators.rate_conversion_generator.random.choice") as mock_choice, \
             patch("generators.rate_conversion_generator.random.randint", return_value=2):
            # Choose mph -> ft/s scenario (index 0)
            mock_choice.return_value = {
                "from_unit": "mi/hr",
                "to_unit": "ft/s",
                "length_rel": ("mi", 5280, "ft"),
                "time_rel": ("hr", 3600, "s"),
                "value_mult": 15,
                "length_first": True,
            }
            res = self.gen.generate()

        self.assertEqual(res["operation"], "convert_rate")
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 2)
        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 1)
        # 2 * 15 = 30 mph; 30 * 5280 / 3600 = 44 ft/s
        self.assertIn("ft/s", res["final_answer"])
        self.assertEqual(res["final_answer"], "44 ft/s")

    def test_ft_s_to_mph(self):
        with patch("generators.rate_conversion_generator.random.choice") as mock_choice, \
             patch("generators.rate_conversion_generator.random.randint", return_value=3):
            mock_choice.return_value = {
                "from_unit": "ft/s",
                "to_unit": "mi/hr",
                "length_rel": ("mi", 5280, "ft"),
                "time_rel": ("hr", 3600, "s"),
                "value_mult": 22,
                "length_first": False,
            }
            res = self.gen.generate()

        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 1)
        # 3*22 = 66 ft/s -> mph: 66*3600/5280 = 45 mph
        self.assertEqual(res["final_answer"], "45 mi/hr")


    def test_oracle_and_canonical_factors(self):
        """A9 oracle: recompute the rate exactly; CONV_FACTOR must state
        the canonical 1-big = k-small relation, never the inverse."""
        import re
        from fractions import Fraction
        rates = {("mi/hr", "ft/s"): Fraction(5280, 3600),
                 ("ft/s", "mi/hr"): Fraction(3600, 5280),
                 ("km/hr", "m/s"): Fraction(1000, 3600),
                 ("m/s", "km/hr"): Fraction(3600, 1000),
                 ("m/min", "cm/s"): Fraction(100, 60),
                 ("cm/s", "m/min"): Fraction(60, 100)}
        valid_factors = {"1 mi|5280 ft", "1 hr|3600 s", "1 km|1000 m",
                         "1 m|100 cm", "1 min|60 s"}
        for _ in range(500):
            res = self.gen.generate()
            value, from_u, to_u = re.fullmatch(
                r"Convert (\d+) (\S+) to (\S+)", res["problem"]).groups()
            expected = int(value) * rates[(from_u, to_u)]
            self.assertEqual(expected.denominator, 1, res["problem"])
            self.assertEqual(res["final_answer"], f"{expected} {to_u}")
            for s in res["steps"]:
                if s.startswith("CONV_FACTOR"):
                    self.assertIn(s.split("|", 1)[1], valid_factors, s)


if __name__ == "__main__":
    unittest.main()

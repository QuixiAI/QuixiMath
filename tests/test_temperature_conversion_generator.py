import re
import unittest
from fractions import Fraction
from unittest.mock import patch

from generators.temperature_conversion_generator import TemperatureConversionGenerator
from helpers import DELIM

PROBLEM_RE = re.compile(r"^Convert (-?\d+) ([FCK]) to ([FCK])$")

KELVIN_OFFSET = Fraction(27315, 100)


def convert(value, from_unit, to_unit):
    """Independent exact conversion from the problem's quantities."""
    v = Fraction(value)
    # normalize to Celsius
    if from_unit == "F":
        celsius = (v - 32) * 5 / 9
    elif from_unit == "K":
        celsius = v - KELVIN_OFFSET
    else:
        celsius = v
    if to_unit == "F":
        return celsius * 9 / 5 + 32
    if to_unit == "K":
        return celsius + KELVIN_OFFSET
    return celsius


class TestTemperatureConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = TemperatureConversionGenerator()

    def test_f_to_c(self):
        with patch("generators.temperature_conversion_generator.random.choice", return_value=("F", "C")), \
             patch("generators.temperature_conversion_generator.random.randint", return_value=4):
            res = self.gen.generate()
        self.assertEqual(res["operation"], "convert_temperature")
        steps = res["steps"]
        self.assertTrue(steps[-1].startswith(f"Z{DELIM}"))
        # randint -> 4 means F = 32 + 9*4 = 68; 68F -> 20 C
        self.assertEqual(res["problem"], "Convert 68 F to C")
        self.assertEqual(res["final_answer"], "20 C")

    def test_c_to_f(self):
        with patch("generators.temperature_conversion_generator.random.choice", return_value=("C", "F")), \
             patch("generators.temperature_conversion_generator.random.randint", return_value=0):
            res = self.gen.generate()
        # 0C -> 32F
        self.assertEqual(res["final_answer"], "32 F")
        self.assertTrue(any(s.startswith("M|9") for s in res["steps"]))

    def test_k_to_f(self):
        with patch("generators.temperature_conversion_generator.random.choice", return_value=("K", "F")), \
             patch("generators.temperature_conversion_generator.random.randint", return_value=273):
            res = self.gen.generate()
        self.assertEqual(res["final_answer"], "31.73 F")
        self.assertTrue(any(s.startswith("A|") for s in res["steps"]))

    def test_oracle_recomputes_answer_from_problem_text(self):
        for _ in range(500):
            res = self.gen.generate()
            m = PROBLEM_RE.match(res["problem"])
            self.assertIsNotNone(m, res["problem"])
            value, from_unit, to_unit = int(m.group(1)), m.group(2), m.group(3)
            expected = convert(value, from_unit, to_unit)
            answer_num, answer_unit = res["final_answer"].rsplit(" ", 1)
            self.assertEqual(answer_unit, to_unit)
            self.assertEqual(Fraction(answer_num), expected, res["problem"])
            # answers are exact, not rounded: minimal digits, no float junk
            self.assertNotRegex(answer_num, r"\.\d*0$")
            self.assertNotRegex(answer_num, r"\.\d{5,}")
            # Fahrenheit sources are constructed to give integer Celsius
            if from_unit == "F" and to_unit == "C":
                self.assertEqual(Fraction(answer_num).denominator, 1)

    def test_step_arithmetic_is_exact(self):
        for _ in range(300):
            res = self.gen.generate()
            for raw in res["steps"]:
                fields = raw.split(DELIM)
                if fields[0] not in ("A", "S", "M", "D"):
                    continue
                x, y, z = (Fraction(f) for f in fields[1:4])
                op = {"A": lambda: x + y, "S": lambda: x - y,
                      "M": lambda: x * y, "D": lambda: x / y}[fields[0]]
                self.assertEqual(z, op(), raw)


if __name__ == "__main__":
    unittest.main()

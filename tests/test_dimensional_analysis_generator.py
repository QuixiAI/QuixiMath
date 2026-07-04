import re
import unittest
from fractions import Fraction
from unittest.mock import patch

from generators.dimensional_analysis_generator import DimensionalAnalysisGenerator
from helpers import DELIM

PROBLEM_RE = re.compile(r"Convert ([\d.]+) (\S+) to (\S+?)(?= using| at|$)")

# Independent unit-pair factors (target = value * factor)
FACTORS = {
    ("kg", "mg"): Fraction(10),                      # at 10 mg per kg
    ("L/min", "mL/hr"): Fraction(60000),
    ("psi", "kPa"): Fraction("6.9"),
    ("kPa", "atm"): 1 / Fraction("101.325"),
    ("atm", "kPa"): Fraction("101.325"),
    ("mcg/min", "mg/hr"): Fraction(60, 1000),
}


class TestDimensionalAnalysisGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = DimensionalAnalysisGenerator()

    def _count_steps(self, steps, opcode):
        return sum(1 for s in steps if s.startswith(f"{opcode}{DELIM}"))

    def test_dosing(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=2):
            mock_choice.return_value = {
                "type": "dosing",
                "desc": "Medication dosing",
                "value_unit": "kg",
                "target_unit": "mg",
                "factors": [("dosage", "10 mg", "1 kg")],
                "note": " at a dosage of 10 mg per kg",
            }
            res = self.gen.generate()
        self.assertEqual(res["operation"], "dimensional_analysis")
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 1)
        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 0)
        # value = 2*5 = 10 kg -> 100 mg (exact, minimal digits)
        self.assertEqual(res["final_answer"], "100 mg")
        self.assertIn("10 mg per kg", res["problem"])

    def test_flow(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=2):
            mock_choice.return_value = {
                "type": "flow",
                "desc": "IV flow rate",
                "value_unit": "L/min",
                "target_unit": "mL/hr",
                "factors": [("volume", "1000 mL", "1 L"), ("time", "60 min", "1 hr")],
            }
            res = self.gen.generate()
        self.assertEqual(self._count_steps(res["steps"], "M"), 2)
        self.assertEqual(self._count_steps(res["steps"], "D"), 0)
        # value = 2*2=4 L/min; 4*1000=4000; 4000*60=240000 mL/hr
        self.assertEqual(res["final_answer"], "240000 mL/hr")

    def test_pressure_kpa_to_atm(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=2):
            mock_choice.return_value = {
                "type": "pressure_atm",
                "desc": "Pressure conversion",
                "value_unit": "kPa",
                "target_unit": "atm",
                "factors": [("pressure", "1 atm", "101.325 kPa")],
                "note": " using 1 atm = 101.325 kPa",
            }
            res = self.gen.generate()
        # value constructed backward: 2 * 101.325 = 202.65 kPa -> exactly 2 atm
        self.assertIn("202.65 kPa", res["problem"])
        self.assertEqual(res["final_answer"], "2 atm")

    def test_dose_rate_mcg_min_to_mg_hr(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=1):
            mock_choice.return_value = {
                "type": "dose_rate",
                "desc": "Dose rate conversion",
                "value_unit": "mcg/min",
                "target_unit": "mg/hr",
                "factors": [
                    ("time", "60 min", "1 hr"),
                    ("mass", "1 mg", "1000 mcg"),
                ],
            }
            res = self.gen.generate()
        # value = 10 mcg/min -> *60 = 600; /1000 = 0.6 mg/hr
        self.assertEqual(res["final_answer"], "0.6 mg/hr")

    def test_pressure(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=3):
            mock_choice.return_value = {
                "type": "pressure",
                "desc": "Pressure conversion",
                "value_unit": "psi",
                "target_unit": "kPa",
                "factors": [("pressure", "6.9 kPa", "1 psi")],
                "note": " using 1 psi = 6.9 kPa",
            }
            res = self.gen.generate()
        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 0)
        # value = 3*3=9 psi; 9*6.9=62.1
        self.assertEqual(res["final_answer"], "62.1 kPa")

    def test_oracle_recomputes_answer_from_problem_text(self):
        for _ in range(400):
            res = self.gen.generate()
            m = PROBLEM_RE.search(res["problem"])
            self.assertIsNotNone(m, res["problem"])
            value = Fraction(m.group(1))
            from_unit, to_unit = m.group(2), m.group(3)
            expected = value * FACTORS[(from_unit, to_unit)]
            answer_num, answer_unit = res["final_answer"].rsplit(" ", 1)
            self.assertEqual(answer_unit, to_unit)
            self.assertEqual(Fraction(answer_num), expected, res["problem"])
            # exact minimal rendering: no trailing zeros, no float junk
            self.assertNotRegex(answer_num, r"\.\d*0$")
            self.assertNotRegex(answer_num, r"\.\d{7,}")

    def test_step_arithmetic_is_exact(self):
        for _ in range(300):
            res = self.gen.generate()
            for raw in res["steps"]:
                fields = raw.split(DELIM)
                if fields[0] not in ("M", "D"):
                    continue
                x, y, z = (Fraction(f) for f in fields[1:4])
                expected = x * y if fields[0] == "M" else x / y
                self.assertEqual(z, expected, raw)


if __name__ == "__main__":
    unittest.main()

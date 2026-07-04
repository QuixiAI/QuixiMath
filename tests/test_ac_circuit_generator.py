import os
import re
import sys
import unittest
from fractions import Fraction
from math import isqrt

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ac_circuit_generator import ACCircuitGenerator
from helpers import DELIM


SERIES_RE = re.compile(
    r"A series RLC circuit has R=(\d+) ohm, inductive reactance XL=(\d+) "
    r"ohm, capacitive reactance XC=(\d+) ohm, and source phasor V="
    r"(\d+)\+0j V\. Find total impedance and current phasor\."
)
RESONANCE_RE = re.compile(
    r"A series RLC circuit has R=(\d+) ohm, L=(\d+) H, and C=([^ ]+) F\. "
    r"Find the resonant angular frequency and impedance at resonance\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def imag_text(value):
    # Coefficient 1 is dropped: j / -j, not 1j / -1j
    value = Fraction(value)
    if value == 1:
        return "j"
    if value == -1:
        return "-j"
    return f"{fraction_text(value)}j"


def complex_text(real, imag):
    real = Fraction(real)
    imag = Fraction(imag)
    if imag == 0:
        return fraction_text(real)
    if real == 0:
        return imag_text(imag)
    sign = "+" if imag > 0 else "-"
    imag_part = "j" if abs(imag) == 1 else f"{fraction_text(abs(imag))}j"
    return f"{fraction_text(real)}{sign}{imag_part}"


def exact_square_root(value):
    value = Fraction(value)
    root_num = isqrt(value.numerator)
    root_den = isqrt(value.denominator)
    assert root_num * root_num == value.numerator
    assert root_den * root_den == value.denominator
    return Fraction(root_num, root_den)


def expected_series(problem):
    resistance, x_l, x_c, voltage = (
        int(value) for value in SERIES_RE.fullmatch(problem).groups()
    )
    reactance = x_l - x_c
    z_text = complex_text(resistance, reactance)
    r_sq = resistance ** 2
    x_sq = reactance ** 2
    denominator = r_sq + x_sq
    real_num = voltage * resistance
    neg_voltage = -voltage
    imag_num = neg_voltage * reactance
    current_real = Fraction(real_num, denominator)
    current_imag = Fraction(imag_num, denominator)
    current = complex_text(current_real, current_imag)
    steps = [
        make_step("AC_SETUP", "series_rlc", f"R={resistance}, XL={x_l}",
                  f"XC={x_c}, V={voltage}"),
        make_step("AC_FORMULA", "Z=R+j(XL-XC)"),
        make_step("S", x_l, x_c, reactance),
        make_step("AC_COMPLEX", "Z", resistance, imag_text(reactance)),
        make_step("AC_FORMULA", "I=V/Z=V*(R-jX)/(R^2+X^2)"),
        make_step("E", resistance, 2, r_sq),
        make_step("E", reactance, 2, x_sq),
        make_step("A", r_sq, x_sq, denominator),
        make_step("M", voltage, resistance, real_num),
        make_step("M", -1, voltage, neg_voltage),
        make_step("M", neg_voltage, reactance, imag_num),
        make_step("D", real_num, denominator, fraction_text(current_real)),
        make_step("D", imag_num, denominator, fraction_text(current_imag)),
        make_step("AC_COMPLEX", "I", fraction_text(current_real),
                  imag_text(current_imag)),
    ]
    answer = f"Z={z_text} ohm; I={current} A"
    return steps, answer


def expected_resonance(problem):
    resistance_raw, inductance_raw, capacitance_raw = (
        RESONANCE_RE.fullmatch(problem).groups()
    )
    resistance = int(resistance_raw)
    inductance = int(inductance_raw)
    capacitance = Fraction(capacitance_raw)
    lc_product = inductance * capacitance
    omega_sq = Fraction(1, lc_product)
    omega = exact_square_root(omega_sq)
    assert omega.denominator == 1
    steps = [
        make_step("AC_SETUP", "resonance", f"R={resistance}, L={inductance}",
                  f"C={fraction_text(capacitance)}"),
        make_step("AC_FORMULA", "omega0^2=1/(L*C)"),
        make_step("M", inductance, fraction_text(capacitance),
                  fraction_text(lc_product)),
        make_step("D", 1, fraction_text(lc_product), fraction_text(omega_sq)),
        make_step("ROOT", fraction_text(omega_sq), omega.numerator),
        make_step("AC_FORMULA", "at resonance XL=XC so Z=R"),
        make_step("AC_COMPLEX", "Z", resistance, "0j"),
    ]
    answer = f"omega0={omega.numerator} rad/s; Z={resistance} ohm"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if SERIES_RE.fullmatch(problem):
        steps, answer = expected_series(problem)
    else:
        steps, answer = expected_resonance(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestACCircuitGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ACCircuitGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[2]) * Fraction(fields[2]),
                                     Fraction(fields[1]), raw_step)

    def test_variants_are_available(self):
        for variant in ACCircuitGenerator.VARIANTS:
            result = ACCircuitGenerator(variant).generate()
            self.assertEqual(result["operation"], f"ac_circuit_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ACCircuitGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

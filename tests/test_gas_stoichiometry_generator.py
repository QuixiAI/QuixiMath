import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gas_stoichiometry_generator import GasStoichiometryGenerator
from helpers import DELIM


GAS_TO_MASS_RE = re.compile(
    r"Given balanced equation (.+), ([A-Za-z0-9]+) gas has P=(\d+) atm, "
    r"V=(\d+) L, T=(\d+) K with R=1\. How many grams of ([A-Za-z0-9]+) "
    r"form\? Molar mass ([A-Za-z0-9]+)=(\d+) g/mol\."
)
MASS_TO_VOLUME_RE = re.compile(
    r"Given balanced equation (.+), (\d+) g ([A-Za-z0-9]+) reacts\. "
    r"At P=(\d+) atm and T=(\d+) K with R=1, what volume V of "
    r"([A-Za-z0-9]+) gas forms\? Molar mass ([A-Za-z0-9]+)=(\d+) g/mol\."
)
MASS_TO_PRESSURE_RE = re.compile(
    r"Given balanced equation (.+), (\d+) g ([A-Za-z0-9]+) reacts and "
    r"([A-Za-z0-9]+) is collected in a V=(\d+) L vessel at T=(\d+) K "
    r"with R=1\. Find pressure P of ([A-Za-z0-9]+)\. Molar mass "
    r"([A-Za-z0-9]+)=(\d+) g/mol\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_term(term):
    pieces = term.split(" ", 1)
    if len(pieces) == 2 and pieces[0].isdigit():
        return int(pieces[0]), pieces[1]
    return 1, term


def parse_equation(equation):
    left_text, right_text = equation.split(" -> ")
    left = [parse_term(term) for term in left_text.split(" + ")]
    right = [parse_term(term) for term in right_text.split(" + ")]
    return left, right


def coefficient_for(parsed_equation, formula):
    left, right = parsed_equation
    for coefficient, species in left + right:
        if species == formula:
            return coefficient
    raise AssertionError(f"{formula} not in equation")


def expected_gas_to_mass(problem):
    (equation, gas, pressure_raw, volume_raw, temperature_raw, target,
     mm_name, mm_raw) = GAS_TO_MASS_RE.fullmatch(problem).groups()
    self_check = {mm_name: int(mm_raw)}
    target_mm = self_check[target]
    pressure = int(pressure_raw)
    volume = int(volume_raw)
    temperature = int(temperature_raw)
    parsed = parse_equation(equation)
    pv = pressure * volume
    gas_moles = Fraction(pv, temperature)
    gas_coef = coefficient_for(parsed, gas)
    target_coef = coefficient_for(parsed, target)
    ratio = Fraction(target_coef, gas_coef)
    target_moles = gas_moles * ratio
    target_mass = target_moles * target_mm
    steps = [
        make_step("GAS_STOICH_SETUP", "gas_to_mass", equation,
                  f"gas={gas}, target={target}"),
        make_step("GAS_FORMULA", "PV=nRT so n=PV/T with R=1"),
        make_step("M", pressure, volume, pv),
        make_step("D", pv, temperature, fraction_text(gas_moles)),
        make_step("STOICH_RATIO", f"{gas}->{target}",
                  f"{target_coef}/{gas_coef}={fraction_text(ratio)}"),
        make_step("M", fraction_text(gas_moles), fraction_text(ratio),
                  fraction_text(target_moles)),
        make_step("MOLAR_MASS", target, f"{target_mm} g/mol"),
        make_step("M", fraction_text(target_moles), target_mm,
                  fraction_text(target_mass)),
    ]
    answer = f"mass {target}={fraction_text(target_mass)} g"
    return steps, answer


def mass_to_gas_common(equation, given_mass, given, gas, given_mm):
    parsed = parse_equation(equation)
    given_moles = Fraction(given_mass, given_mm)
    given_coef = coefficient_for(parsed, given)
    gas_coef = coefficient_for(parsed, gas)
    ratio = Fraction(gas_coef, given_coef)
    gas_moles = given_moles * ratio
    steps = [
        make_step("MOLAR_MASS", given, f"{given_mm} g/mol"),
        make_step("D", given_mass, given_mm, fraction_text(given_moles)),
        make_step("STOICH_RATIO", f"{given}->{gas}",
                  f"{gas_coef}/{given_coef}={fraction_text(ratio)}"),
        make_step("M", fraction_text(given_moles), fraction_text(ratio),
                  fraction_text(gas_moles)),
    ]
    return gas_moles, steps


def expected_mass_to_volume(problem):
    (equation, given_mass_raw, given, pressure_raw, temperature_raw, gas,
     mm_name, mm_raw) = MASS_TO_VOLUME_RE.fullmatch(problem).groups()
    self_check = {mm_name: int(mm_raw)}
    given_mass = int(given_mass_raw)
    pressure = int(pressure_raw)
    temperature = int(temperature_raw)
    given_mm = self_check[given]
    gas_moles, common_steps = mass_to_gas_common(
        equation, given_mass, given, gas, given_mm
    )
    nt = gas_moles * temperature
    gas_volume = nt / pressure
    steps = [
        make_step("GAS_STOICH_SETUP", "mass_to_gas_volume", equation,
                  f"given={given_mass} g {given}, gas={gas}"),
    ]
    steps.extend(common_steps)
    steps.extend([
        make_step("GAS_FORMULA", "PV=nRT so V=nT/P with R=1"),
        make_step("M", fraction_text(gas_moles), temperature,
                  fraction_text(nt)),
        make_step("D", fraction_text(nt), pressure, fraction_text(gas_volume)),
    ])
    answer = f"V {gas}={fraction_text(gas_volume)} L"
    return steps, answer


def expected_mass_to_pressure(problem):
    (equation, given_mass_raw, given, gas1, vessel_volume_raw,
     temperature_raw, gas2, mm_name, mm_raw) = (
        MASS_TO_PRESSURE_RE.fullmatch(problem).groups()
    )
    self_check = {mm_name: int(mm_raw)}
    if gas1 != gas2:
        raise AssertionError(problem)
    given_mass = int(given_mass_raw)
    vessel_volume = int(vessel_volume_raw)
    temperature = int(temperature_raw)
    given_mm = self_check[given]
    gas_moles, common_steps = mass_to_gas_common(
        equation, given_mass, given, gas1, given_mm
    )
    nt = gas_moles * temperature
    pressure = nt / vessel_volume
    steps = [
        make_step("GAS_STOICH_SETUP", "mass_to_gas_pressure", equation,
                  f"given={given_mass} g {given}, gas={gas1}"),
    ]
    steps.extend(common_steps)
    steps.extend([
        make_step("GAS_FORMULA", "PV=nRT so P=nT/V with R=1"),
        make_step("M", fraction_text(gas_moles), temperature,
                  fraction_text(nt)),
        make_step("D", fraction_text(nt), vessel_volume,
                  fraction_text(pressure)),
    ])
    answer = f"P {gas1}={fraction_text(pressure)} atm"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if GAS_TO_MASS_RE.fullmatch(problem):
        steps, answer = expected_gas_to_mass(problem)
    elif MASS_TO_VOLUME_RE.fullmatch(problem):
        steps, answer = expected_mass_to_volume(problem)
    elif MASS_TO_PRESSURE_RE.fullmatch(problem):
        steps, answer = expected_mass_to_pressure(problem)
    else:
        raise AssertionError(f"unrecognized problem: {problem}")
    steps.append(make_step("Z", answer))
    return steps, answer


class TestGasStoichiometryGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GasStoichiometryGenerator()

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
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in GasStoichiometryGenerator.VARIANTS:
            result = GasStoichiometryGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"gas_stoichiometry_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GasStoichiometryGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

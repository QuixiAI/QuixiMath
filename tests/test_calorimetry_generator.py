import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.calorimetry_generator import CalorimetryGenerator
from helpers import DELIM


TEMP_RE = re.compile(
    r"A sample has mass m=(\d+) kg and specific heat c=(\d+) J/\(kg\*K\)\. "
    r"Its temperature changes from T1=(-?\d+) C to T2=(-?\d+) C\. Find "
    r"heat q\."
)
PHASE_RE = re.compile(
    r"A substance of mass m=(\d+) kg undergoes a phase change with latent "
    r"heat L=(\d+) J/kg\. Find heat q\."
)
ICE_RE = re.compile(
    r"Ice of mass m=(\d+) kg starts at Ti=(-?\d+) C and ends as liquid "
    r"water at Tf=(\d+) C\. Use c_ice=(\d+), Lf=(\d+), and c_water=(\d+)\. "
    r"Find total heat\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expected_temp(problem):
    mass, specific_heat, t1, t2 = (
        int(value) for value in TEMP_RE.fullmatch(problem).groups()
    )
    delta_t = t2 - t1
    mc = mass * specific_heat
    heat = mc * delta_t
    steps = [
        make_step("CAL_SETUP", "temperature_change",
                  f"m={mass}, c={specific_heat}", f"T1={t1}, T2={t2}"),
        make_step("CAL_FORMULA", "q=m*c*(T2-T1)"),
        make_step("S", t2, t1, delta_t),
        make_step("M", mass, specific_heat, mc),
        make_step("M", mc, delta_t, heat),
    ]
    answer = f"q={heat} J"
    return steps, answer


def expected_phase(problem):
    mass, latent_heat = (
        int(value) for value in PHASE_RE.fullmatch(problem).groups()
    )
    heat = mass * latent_heat
    steps = [
        make_step("CAL_SETUP", "phase_change", f"m={mass}",
                  f"L={latent_heat}"),
        make_step("CAL_FORMULA", "q=m*L"),
        make_step("M", mass, latent_heat, heat),
    ]
    answer = f"q={heat} J"
    return steps, answer


def expected_ice(problem):
    mass, start_temp, final_temp, c_ice, latent_heat, c_water = (
        int(value) for value in ICE_RE.fullmatch(problem).groups()
    )
    warm_ice_delta = 0 - start_temp
    warm_ice_mc = mass * c_ice
    warm_ice_heat = warm_ice_mc * warm_ice_delta
    melt_heat = mass * latent_heat
    warm_water_mc = mass * c_water
    warm_water_heat = warm_water_mc * final_temp
    partial = warm_ice_heat + melt_heat
    total = partial + warm_water_heat
    steps = [
        make_step("CAL_SETUP", "ice_to_water",
                  f"m={mass}, Ti={start_temp}, Tf={final_temp}",
                  f"c_ice={c_ice}, Lf={latent_heat}, c_water={c_water}"),
        make_step("CAL_FORMULA", "warm ice: q1=m*c_ice*(0-Ti)"),
        make_step("S", 0, start_temp, warm_ice_delta),
        make_step("M", mass, c_ice, warm_ice_mc),
        make_step("M", warm_ice_mc, warm_ice_delta, warm_ice_heat),
        make_step("CAL_FORMULA", "melt ice: q2=m*Lf"),
        make_step("M", mass, latent_heat, melt_heat),
        make_step("CAL_FORMULA", "warm water: q3=m*c_water*Tf"),
        make_step("M", mass, c_water, warm_water_mc),
        make_step("M", warm_water_mc, final_temp, warm_water_heat),
        make_step("A", warm_ice_heat, melt_heat, partial),
        make_step("A", partial, warm_water_heat, total),
    ]
    answer = f"q_total={total} J"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if TEMP_RE.fullmatch(problem):
        steps, answer = expected_temp(problem)
    elif PHASE_RE.fullmatch(problem):
        steps, answer = expected_phase(problem)
    else:
        steps, answer = expected_ice(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCalorimetryGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = CalorimetryGenerator()

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

    def test_variants_are_available(self):
        for variant in CalorimetryGenerator.VARIANTS:
            result = CalorimetryGenerator(variant).generate()
            self.assertEqual(result["operation"], f"calorimetry_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CalorimetryGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

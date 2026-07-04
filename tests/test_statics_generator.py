import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.statics_generator import StaticsGenerator
from helpers import DELIM


LEVER_RE = re.compile(
    r"A lever is in static equilibrium\. A (\d+) N downward force acts "
    r"(\d+) m left of the fulcrum\. What downward force must act (\d+) m "
    r"right of the fulcrum to balance torques\?"
)
BEAM_RE = re.compile(
    r"A simply supported beam is (\d+) m long with supports at A and B\. "
    r"A (\d+) N point load acts (\d+) m from support A\. Find reactions "
    r"RA and RB\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_lever(problem):
    force1, distance1, distance2 = (
        int(value) for value in LEVER_RE.fullmatch(problem).groups()
    )
    torque = force1 * distance1
    force2 = Fraction(torque, distance2)
    check_torque = force2 * distance2
    steps = [
        make_step("STATICS_SETUP", "lever_balance", f"F1={force1}",
                  f"d1={distance1}, d2={distance2}"),
        make_step("STATICS_FORMULA", "F1*d1=F2*d2"),
        make_step("M", force1, distance1, torque),
        make_step("D", torque, distance2, fraction_text(force2)),
        make_step("M", fraction_text(force2), distance2,
                  fraction_text(check_torque)),
        make_step("CHECK", "left torque", torque,
                  f"right torque {fraction_text(check_torque)}"),
    ]
    answer = f"F2={fraction_text(force2)} N"
    return steps, answer


def expected_beam(problem):
    length, load, load_position = (
        int(value) for value in BEAM_RE.fullmatch(problem).groups()
    )
    load_torque = load * load_position
    right_reaction = Fraction(load_torque, length)
    left_reaction = Fraction(load) - right_reaction
    force_sum = left_reaction + right_reaction
    steps = [
        make_step("STATICS_SETUP", "supported_beam", f"W={load}, L={length}",
                  f"x={load_position}"),
        make_step("STATICS_FORMULA", "sum_tau_left=0 => RB*L=W*x"),
        make_step("M", load, load_position, load_torque),
        make_step("D", load_torque, length, fraction_text(right_reaction)),
        make_step("STATICS_FORMULA", "sum_Fy=0 => RA+RB=W"),
        make_step("S", load, fraction_text(right_reaction),
                  fraction_text(left_reaction)),
        make_step("A", fraction_text(left_reaction),
                  fraction_text(right_reaction), fraction_text(force_sum)),
        make_step("CHECK", "vertical forces", fraction_text(force_sum),
                  f"load {load}"),
    ]
    answer = (
        f"RA={fraction_text(left_reaction)} N; "
        f"RB={fraction_text(right_reaction)} N"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if LEVER_RE.fullmatch(problem):
        steps, answer = expected_lever(problem)
    else:
        steps, answer = expected_beam(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestStaticsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = StaticsGenerator()

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

    def test_statics_checks_are_true(self):
        for _ in range(300):
            result = self.gen.generate()
            if result["operation"] == "statics_lever_balance":
                torque_step = [
                    raw for raw in result["steps"]
                    if raw.startswith(f"CHECK{DELIM}left torque")
                ][0]
                _, _, left, right_text = torque_step.split(DELIM)
                self.assertEqual(Fraction(left),
                                 Fraction(right_text.removeprefix(
                                     "right torque ")))
            else:
                check_step = [
                    raw for raw in result["steps"]
                    if raw.startswith(f"CHECK{DELIM}vertical forces")
                ][0]
                _, _, force_sum, load_text = check_step.split(DELIM)
                self.assertEqual(Fraction(force_sum),
                                 Fraction(load_text.removeprefix("load ")))

    def test_variants_are_available(self):
        for variant in StaticsGenerator.VARIANTS:
            result = StaticsGenerator(variant).generate()
            self.assertEqual(result["operation"], f"statics_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StaticsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

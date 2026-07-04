import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.continuous_distribution_generator import (
    ContinuousDistributionGenerator,
)
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For pdf f\(x\)=k\*x on 0<=x<=(\d+), first normalize k, then "
    r"compute P\((\d+)<X<(\d+)\), mean, and variance\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "a": int(match.group(1)),
        "left": int(match.group(2)),
        "right": int(match.group(3)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    a = parts["a"]
    left = parts["left"]
    right = parts["right"]
    a_sq = a ** 2
    integral_x = Fraction(a_sq, 2)
    k = Fraction(1, 1) / integral_x
    right_sq = right ** 2
    left_sq = left ** 2
    interval_diff = right_sq - left_sq
    prob_raw = k * interval_diff
    probability = prob_raw / 2
    a_cubed = a ** 3
    mean_raw = k * a_cubed
    mean = mean_raw / 3
    a_fourth = a ** 4
    second_raw = k * a_fourth
    second_moment = second_raw / 4
    mean_sq = mean * mean
    variance = second_moment - mean_sq
    steps = [
        make_step("CONT_DIST_SETUP", "f(x)=k*x", f"support=[0,{a}]",
                  f"interval=({left},{right})"),
        make_step("POWER_INTEGRAL", "int_0^a x dx", "a^2/2"),
        make_step("E", a, 2, a_sq),
        make_step("D", a_sq, 2, fraction_text(integral_x)),
        make_step("D", 1, fraction_text(integral_x), fraction_text(k)),
        make_step("POWER_INTEGRAL", "int_b^c x dx", "(c^2-b^2)/2"),
        make_step("E", right, 2, right_sq),
        make_step("E", left, 2, left_sq),
        make_step("S", right_sq, left_sq, interval_diff),
        make_step("M", fraction_text(k), interval_diff,
                  fraction_text(prob_raw)),
        make_step("D", fraction_text(prob_raw), 2,
                  fraction_text(probability)),
        make_step("POWER_INTEGRAL", "E[X]", "k*a^3/3"),
        make_step("E", a, 3, a_cubed),
        make_step("M", fraction_text(k), a_cubed, fraction_text(mean_raw)),
        make_step("D", fraction_text(mean_raw), 3, fraction_text(mean)),
        make_step("POWER_INTEGRAL", "E[X^2]", "k*a^4/4"),
        make_step("E", a, 4, a_fourth),
        make_step("M", fraction_text(k), a_fourth,
                  fraction_text(second_raw)),
        make_step("D", fraction_text(second_raw), 4,
                  fraction_text(second_moment)),
        make_step("M", fraction_text(mean), fraction_text(mean),
                  fraction_text(mean_sq)),
        make_step("S", fraction_text(second_moment), fraction_text(mean_sq),
                  fraction_text(variance)),
    ]
    answer = (
        f"k = {fraction_text(k)}, P = {fraction_text(probability)}, "
        f"mean = {fraction_text(mean)}, variance = {fraction_text(variance)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestContinuousDistributionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ContinuousDistributionGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_probability_is_between_zero_and_one(self):
        for _ in range(300):
            result = self.gen.generate()
            p_text = result["final_answer"].split("P = ")[1].split(",")[0]
            probability = Fraction(p_text)
            self.assertGreater(probability, 0)
            self.assertLessEqual(probability, 1)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

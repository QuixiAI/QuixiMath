import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.projectile_motion_generator import ProjectileMotionGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"A projectile is launched from ground level with horizontal velocity "
    r"(\d+) m/s and vertical velocity (\d+) m/s\. Use g=10 m/s\^2 to "
    r"compute time of flight, range, and maximum height\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    vx, vy = (int(value) for value in PROBLEM_RE.fullmatch(
        example["problem"]
    ).groups())
    g = 10
    time_up = Fraction(vy, g)
    flight_time = 2 * time_up
    range_value = vx * flight_time
    vy_sq = vy ** 2
    two_g = 2 * g
    max_height = Fraction(vy_sq, two_g)
    steps = [
        make_step("PROJECTILE_SETUP", f"vx={vx}", f"vy={vy}", f"g={g}"),
        make_step("FORMULA", "t_up=vy/g"),
        make_step("D", vy, g, fraction_text(time_up)),
        make_step("FORMULA", "T=2*t_up"),
        make_step("M", 2, fraction_text(time_up), fraction_text(flight_time)),
        make_step("FORMULA", "range=vx*T"),
        make_step("M", vx, fraction_text(flight_time),
                  fraction_text(range_value)),
        make_step("FORMULA", "h_max=vy^2/(2g)"),
        make_step("E", vy, 2, vy_sq),
        make_step("M", 2, g, two_g),
        make_step("D", vy_sq, two_g, fraction_text(max_height)),
    ]
    answer = (
        f"time={fraction_text(flight_time)} s; "
        f"range={fraction_text(range_value)} m; "
        f"max height={fraction_text(max_height)} m"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestProjectileMotionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ProjectileMotionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "projectile_motion_components")
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
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

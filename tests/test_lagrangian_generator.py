import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lagrangian_generator import LagrangianGenerator
from helpers import DELIM


SPRING_RE = re.compile(
    r"For a mass-spring system with mass m=(\d+) and spring constant "
    r"k=(\d+), write L=T-V and apply the Euler-Lagrange equation to find "
    r"xddot\."
)
PENDULUM_RE = re.compile(
    r"For a simple pendulum with mass m=(\d+), length L=(\d+), and g=10, "
    r"write L=T-V and apply the Euler-Lagrange equation to find thetaddot\."
)
ATWOOD_RE = re.compile(
    r"An Atwood machine has masses m1=(\d+) and m2=(\d+) with m2 heavier\. "
    r"Let y be downward displacement of m2\. Write L=T-V and apply the "
    r"Euler-Lagrange equation to find yddot\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def neg_coeff_times(coeff, body):
    coeff = Fraction(coeff)
    if coeff == 1:
        return f"-{body}"
    if coeff.denominator == 1:
        return f"-{coeff.numerator}*{body}"
    return f"-({coeff})*{body}"


def expected_spring(problem):
    mass, spring_k = (
        int(value) for value in SPRING_RE.fullmatch(problem).groups()
    )
    coeff = Fraction(spring_k, mass)
    acceleration = neg_coeff_times(coeff, "x")
    steps = [
        make_step("LAG_SETUP", "mass_spring", f"m={mass}, k={spring_k}",
                  "q=x"),
        make_step("ENERGY_TERM", "T=1/2*m*xdot^2"),
        make_step("ENERGY_TERM", "V=1/2*k*x^2"),
        make_step("LAGRANGIAN", "L=T-V",
                  "1/2*m*xdot^2 - 1/2*k*x^2"),
        make_step("PARTIAL", "dL/dxdot", "m*xdot"),
        make_step("TIME_DERIV", "d/dt(m*xdot)", "m*xddot"),
        make_step("PARTIAL", "dL/dx", "-k*x"),
        make_step("EL_EQUATION", "d/dt(dL/dxdot)-dL/dx=0"),
        make_step("EL_EQUATION", "m*xddot+k*x=0"),
        make_step("D", spring_k, mass, fraction_text(coeff)),
        make_step("EL_SOLVE", "xddot", acceleration),
    ]
    answer = f"xddot={acceleration}"
    return steps, answer


def expected_pendulum(problem):
    mass, length = (
        int(value) for value in PENDULUM_RE.fullmatch(problem).groups()
    )
    g = 10
    length_sq = length ** 2
    inertia_coeff = mass * length_sq
    mg = mass * g
    gravity_coeff = mg * length
    coeff = Fraction(gravity_coeff, inertia_coeff)
    acceleration = neg_coeff_times(coeff, "sin(theta)")
    steps = [
        make_step("LAG_SETUP", "pendulum", f"m={mass}, L={length}",
                  f"g={g}, q=theta"),
        make_step("ENERGY_TERM", "T=1/2*m*L^2*thetadot^2"),
        make_step("E", length, 2, length_sq),
        make_step("M", mass, length_sq, inertia_coeff),
        make_step("ENERGY_TERM", "V=m*g*L*(1-cos(theta))"),
        make_step("M", mass, g, mg),
        make_step("M", mg, length, gravity_coeff),
        make_step("LAGRANGIAN", "L=T-V"),
        make_step("PARTIAL", "dL/dthetadot", "m*L^2*thetadot"),
        make_step("TIME_DERIV", "d/dt(m*L^2*thetadot)",
                  "m*L^2*thetaddot"),
        make_step("PARTIAL", "dL/dtheta", "-m*g*L*sin(theta)"),
        make_step("EL_EQUATION", "mL^2*thetaddot+mgL*sin(theta)=0"),
        make_step("D", gravity_coeff, inertia_coeff, fraction_text(coeff)),
        make_step("EL_SOLVE", "thetaddot", acceleration),
    ]
    answer = f"thetaddot={acceleration}"
    return steps, answer


def expected_atwood(problem):
    m1, m2 = (int(value) for value in ATWOOD_RE.fullmatch(problem).groups())
    g = 10
    total_mass = m1 + m2
    potential_diff = m1 - m2
    potential_coeff = potential_diff * g
    driving_diff = m2 - m1
    driving_force = driving_diff * g
    acceleration = Fraction(driving_force, total_mass)
    steps = [
        make_step("LAG_SETUP", "atwood", f"m1={m1}, m2={m2}",
                  f"g={g}, q=y"),
        make_step("ENERGY_TERM", "T=1/2*(m1+m2)*ydot^2"),
        make_step("A", m1, m2, total_mass),
        make_step("ENERGY_TERM", "V=(m1-m2)*g*y"),
        make_step("S", m1, m2, potential_diff),
        make_step("M", potential_diff, g, potential_coeff),
        make_step("LAGRANGIAN", "L=T-V"),
        make_step("PARTIAL", "dL/dydot", "(m1+m2)*ydot"),
        make_step("TIME_DERIV", "d/dt((m1+m2)*ydot)",
                  "(m1+m2)*yddot"),
        make_step("PARTIAL", "dL/dy", "(m2-m1)*g"),
        make_step("S", m2, m1, driving_diff),
        make_step("M", driving_diff, g, driving_force),
        make_step("EL_EQUATION", "(m1+m2)*yddot-(m2-m1)g=0"),
        make_step("D", driving_force, total_mass, fraction_text(acceleration)),
        make_step("EL_SOLVE", "yddot", f"{fraction_text(acceleration)}"),
    ]
    answer = f"yddot={fraction_text(acceleration)} m/s^2 downward for m2"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if SPRING_RE.fullmatch(problem):
        steps, answer = expected_spring(problem)
    elif PENDULUM_RE.fullmatch(problem):
        steps, answer = expected_pendulum(problem)
    else:
        steps, answer = expected_atwood(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestLagrangianGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LagrangianGenerator()

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

    def test_variants_are_available(self):
        for variant in LagrangianGenerator.VARIANTS:
            result = LagrangianGenerator(variant).generate()
            self.assertEqual(result["operation"], f"lagrangian_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LagrangianGenerator("bogus")

    def test_rendering_is_not_degenerate(self):
        bad_patterns = [r"(?<!\d)1\*", r"--", r"\+ -"]
        for _ in range(300):
            result = self.gen.generate()
            joined = "\n".join([result["problem"], result["final_answer"],
                                *result["steps"]])
            for pattern in bad_patterns:
                self.assertIsNone(re.search(pattern, joined), joined)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hamiltonian_generator import HamiltonianGenerator
from helpers import DELIM


SPRING_RE = re.compile(
    r"For a mass-spring Hamiltonian with mass m=(\d+) and spring constant "
    r"k=(\d+), write H and Hamilton's equations\."
)
PENDULUM_RE = re.compile(
    r"For a pendulum Hamiltonian with mass m=(\d+), length L=(\d+), and "
    r"g=10, write H and Hamilton's equations\."
)
ATWOOD_RE = re.compile(
    r"For an Atwood Hamiltonian with masses m1=(\d+) and m2=(\d+), "
    r"m2 heavier, and g=10, use y downward for m2\. Write H and Hamilton's "
    r"equations\."
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


def momentum_over(momentum, denom):
    if denom == 1:
        return momentum
    return f"{momentum}/{denom}"


def expected_spring(problem):
    mass, spring_k = (
        int(value) for value in SPRING_RE.fullmatch(problem).groups()
    )
    xdot = momentum_over("p_x", mass)
    p_dot = neg_coeff_times(spring_k, "x")
    acceleration_coeff = Fraction(spring_k, mass)
    acceleration = neg_coeff_times(acceleration_coeff, "x")
    steps = [
        make_step("HAM_SETUP", "mass_spring", f"m={mass}, k={spring_k}",
                  "q=x, p=p_x"),
        make_step("HAMILTONIAN", "H=p_x^2/(2m)+1/2*k*x^2"),
        make_step("PARTIAL", "dH/dp_x", "p_x/m"),
        make_step("HAM_EQ", "xdot=dH/dp_x", f"xdot={xdot}"),
        make_step("PARTIAL", "dH/dx", "k*x"),
        make_step("HAM_EQ", "p_xdot=-dH/dx", f"p_xdot={p_dot}"),
        make_step("D", spring_k, mass, fraction_text(acceleration_coeff)),
        make_step("HAM_EQ", "xddot=p_xdot/m", f"xddot={acceleration}"),
    ]
    answer = f"xdot={xdot}; p_xdot={p_dot}; xddot={acceleration}"
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
    theta_dot = momentum_over("p_theta", inertia_coeff)
    p_dot = neg_coeff_times(gravity_coeff, "sin(theta)")
    acceleration_coeff = Fraction(gravity_coeff, inertia_coeff)
    acceleration = neg_coeff_times(acceleration_coeff, "sin(theta)")
    steps = [
        make_step("HAM_SETUP", "pendulum", f"m={mass}, L={length}",
                  f"g={g}, q=theta"),
        make_step("E", length, 2, length_sq),
        make_step("M", mass, length_sq, inertia_coeff),
        make_step("M", mass, g, mg),
        make_step("M", mg, length, gravity_coeff),
        make_step("HAMILTONIAN",
                  "H=p_theta^2/(2mL^2)+mgL*(1-cos(theta))"),
        make_step("PARTIAL", "dH/dp_theta", "p_theta/(mL^2)"),
        make_step("HAM_EQ", "thetadot=dH/dp_theta",
                  f"thetadot={theta_dot}"),
        make_step("PARTIAL", "dH/dtheta", "mgL*sin(theta)"),
        make_step("HAM_EQ", "p_thetadot=-dH/dtheta",
                  f"p_thetadot={p_dot}"),
        make_step("D", gravity_coeff, inertia_coeff,
                  fraction_text(acceleration_coeff)),
        make_step("HAM_EQ", "thetaddot=p_thetadot/(mL^2)",
                  f"thetaddot={acceleration}"),
    ]
    answer = (
        f"thetadot={theta_dot}; p_thetadot={p_dot}; "
        f"thetaddot={acceleration}"
    )
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
    ydot = momentum_over("p_y", total_mass)
    steps = [
        make_step("HAM_SETUP", "atwood", f"m1={m1}, m2={m2}",
                  f"g={g}, q=y, p=p_y"),
        make_step("A", m1, m2, total_mass),
        make_step("S", m1, m2, potential_diff),
        make_step("M", potential_diff, g, potential_coeff),
        make_step("S", m2, m1, driving_diff),
        make_step("M", driving_diff, g, driving_force),
        make_step("HAMILTONIAN", "H=p_y^2/(2(m1+m2))+(m1-m2)g*y"),
        make_step("PARTIAL", "dH/dp_y", "p_y/(m1+m2)"),
        make_step("HAM_EQ", "ydot=dH/dp_y", f"ydot={ydot}"),
        make_step("PARTIAL", "dH/dy", "(m1-m2)g"),
        make_step("HAM_EQ", "p_ydot=-dH/dy", f"p_ydot={driving_force}"),
        make_step("D", driving_force, total_mass, fraction_text(acceleration)),
        make_step("HAM_EQ", "yddot=p_ydot/(m1+m2)",
                  f"yddot={fraction_text(acceleration)}"),
    ]
    answer = (
        f"ydot={ydot}; p_ydot={driving_force}; "
        f"yddot={fraction_text(acceleration)} m/s^2 downward for m2"
    )
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


class TestHamiltonianGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = HamiltonianGenerator()

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
        for variant in HamiltonianGenerator.VARIANTS:
            result = HamiltonianGenerator(variant).generate()
            self.assertEqual(result["operation"], f"hamiltonian_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HamiltonianGenerator("bogus")

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

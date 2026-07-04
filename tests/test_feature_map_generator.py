import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.feature_map_generator import FeatureMapGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For the polynomial kernel K\(x,z\)=\(xz \+ 2\)\^2 with feature map "
    r"phi\(t\)=\(t\^2, 2t, 2\), verify K\(x,z\) for x=([-0-9]+) "
    r"and z=([-0-9]+) by expanding phi\(x\) dot phi\(z\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def vector_text(vector):
    return "(" + ",".join(str(value) for value in vector) + ")"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    x = int(match.group(1))
    z = int(match.group(2))
    phi_x = (x ** 2, 2 * x, 2)
    phi_z = (z ** 2, 2 * z, 2)
    term1 = phi_x[0] * phi_z[0]
    term2 = phi_x[1] * phi_z[1]
    term3 = phi_x[2] * phi_z[2]
    partial = term1 + term2
    dot_value = partial + term3
    xz = x * z
    base = xz + 2
    kernel_value = base ** 2
    steps = [
        make_step("FEATURE_MAP_SETUP", "K(x,z)=(xz+2)^2",
                  "phi(t)=(t^2,2t,2)", f"x={x},z={z}"),
        make_step("E", x, 2, phi_x[0]),
        make_step("M", 2, x, phi_x[1]),
        make_step("FEATURE_VECTOR", "phi(x)", vector_text(phi_x)),
        make_step("E", z, 2, phi_z[0]),
        make_step("M", 2, z, phi_z[1]),
        make_step("FEATURE_VECTOR", "phi(z)", vector_text(phi_z)),
        make_step("M", phi_x[0], phi_z[0], term1),
        make_step("M", phi_x[1], phi_z[1], term2),
        make_step("M", phi_x[2], phi_z[2], term3),
        make_step("A", term1, term2, partial),
        make_step("A", partial, term3, dot_value),
        make_step("DOT", "phi(x),phi(z)", dot_value),
        make_step("M", x, z, xz),
        make_step("A", xz, 2, base),
        make_step("KERNEL_BASE", "x,z", f"xz+2={xz}+2", base),
        make_step("E", base, 2, kernel_value),
        make_step("KERNEL_VALUE", "x,z", kernel_value),
        make_step("CHECK", "feature dot equals kernel",
                  f"{dot_value}={kernel_value}", "verified=true"),
    ]
    answer = (
        f"phi_x={vector_text(phi_x)}; phi_z={vector_text(phi_z)}; "
        f"dot={dot_value}; K={kernel_value}; verified=true"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestFeatureMapGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = FeatureMapGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "feature_map_polynomial_verify")
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
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

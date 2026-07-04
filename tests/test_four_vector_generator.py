import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.four_vector_generator import FourVectorGenerator
from helpers import DELIM


DOT_RE = re.compile(
    r"Using signature \(\+---\), compute the Minkowski dot product p\.q "
    r"for p=(\[[^\]]+\]) and q=(\[[^\]]+\])\."
)
MASS_RE = re.compile(
    r"In units c=1, solve E\^2 = p\^2 \+ m\^2 for momentum "
    r"p=(\d+) and mass m=(\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def vector_text(values):
    return "[" + ",".join(str(value) for value in values) + "]"


def parse_vector(text):
    return [int(value) for value in text.strip("[]").split(",")]


def parse_problem(problem):
    match = DOT_RE.fullmatch(problem)
    if match:
        return {
            "variant": "dot_product",
            "p": parse_vector(match.group(1)),
            "q": parse_vector(match.group(2)),
        }
    match = MASS_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "mass_shell",
        "p": int(match.group(1)),
        "m": int(match.group(2)),
    }


def expected_dot(p, q):
    time_part = p[0] * q[0]
    spatial = [p[i] * q[i] for i in range(1, 4)]
    spatial_sum = spatial[0] + spatial[1]
    spatial_total = spatial_sum + spatial[2]
    dot = time_part - spatial_total
    steps = [
        make_step("FOUR_VECTOR_SETUP", "signature=+---",
                  f"p={vector_text(p)}", f"q={vector_text(q)}"),
        make_step("M", p[0], q[0], time_part),
    ]
    for i in range(1, 4):
        steps.append(make_step("M", p[i], q[i], spatial[i - 1]))
    steps.extend([
        make_step("A", spatial[0], spatial[1], spatial_sum),
        make_step("A", spatial_sum, spatial[2], spatial_total),
        make_step("S", time_part, spatial_total, dot),
    ])
    answer = f"p.q = {dot}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_mass_shell(momentum, mass):
    p_sq = momentum ** 2
    m_sq = mass ** 2
    e_sq = p_sq + m_sq
    energy = int(e_sq ** 0.5)
    assert energy * energy == e_sq
    steps = [
        make_step("FOUR_VECTOR_SETUP", "mass_shell", "c=1",
                  f"p={momentum}, m={mass}"),
        make_step("E", momentum, 2, p_sq),
        make_step("E", mass, 2, m_sq),
        make_step("A", p_sq, m_sq, e_sq),
        make_step("ROOT", f"sqrt({e_sq})", energy),
    ]
    answer = f"E = {energy}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "dot_product":
        return expected_dot(parts["p"], parts["q"])
    return expected_mass_shell(parts["p"], parts["m"])


class TestFourVectorGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FourVectorGenerator()

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
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    root = int(fields[2])
                    radicand = int(fields[1].removeprefix("sqrt(").rstrip(")"))
                    self.assertEqual(root * root, radicand, raw_step)

    def test_variants_are_available(self):
        for variant in FourVectorGenerator.VARIANTS:
            result = FourVectorGenerator(variant).generate()
            self.assertEqual(result["operation"], f"four_vector_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FourVectorGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

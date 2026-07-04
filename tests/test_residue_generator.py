import ast
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.residue_generator import ResidueGenerator
from helpers import DELIM


HIGHER_RE = re.compile(
    r"Find the residue at z=(-?\d+) of f\(z\) = (.+), whose numerator "
    r"coefficients in powers of (.+) are (\[[^]]+\])\."
)
SIMPLE_RE = re.compile(
    r"Find the residue at z=(-?\d+) of f\(z\) = (.+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def z_minus(a):
    if a == 0:
        return "z"
    if a > 0:
        return f"(z-{a})"
    return f"(z+{-a})"


def parse_problem(problem):
    match = HIGHER_RE.fullmatch(problem)
    if match:
        a = int(match.group(1))
        function = match.group(2)
        coeffs = ast.literal_eval(match.group(4))
        order = int(re.search(r"\^(\d+)$", function).group(1))
        return {"variant": "higher_order", "a": a, "function": function,
                "coeffs": coeffs, "order": order}
    match = SIMPLE_RE.fullmatch(problem)
    assert match is not None, problem
    a = int(match.group(1))
    function = match.group(2)
    residue = int(re.match(r"(-?\d+)/", function).group(1))
    return {"variant": "simple", "a": a, "function": function,
            "residue": residue}


def expected_simple(a, function, residue):
    base = z_minus(a)
    steps = [
        make_step("RESIDUE_SETUP", f"a={a}", f"f={function}"),
        make_step("POLE_ORDER", 1),
        make_step("LAURENT_TERM", f"{residue}{base}^-1"),
        make_step("RESIDUE", residue),
    ]
    return steps, f"residue = {residue}"


def expected_higher(a, function, coeffs, order):
    base = z_minus(a)
    steps = [
        make_step("RESIDUE_SETUP", f"a={a}", f"f={function}"),
        make_step("POLE_ORDER", order),
    ]
    for power, coef in enumerate(coeffs):
        steps.append(make_step("LAURENT_TERM",
                               f"{coef}{base}^{power - order}"))
    residue = coeffs[order - 1]
    steps.append(make_step("RESIDUE", residue))
    return steps, f"residue = {residue}"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "simple":
        steps, answer = expected_simple(parts["a"], parts["function"],
                                        parts["residue"])
    else:
        steps, answer = expected_higher(parts["a"], parts["function"],
                                        parts["coeffs"], parts["order"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestResidueGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ResidueGenerator()

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

    def test_residue_is_laurent_minus_one_coefficient(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            if parts["variant"] == "higher_order":
                residue = parts["coeffs"][parts["order"] - 1]
            else:
                residue = parts["residue"]
            self.assertEqual(result["final_answer"], f"residue = {residue}")

    def test_variants_are_available(self):
        for variant in ("simple", "higher_order"):
            gen = ResidueGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"], f"residue_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ResidueGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

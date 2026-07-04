import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.scaling_law_generator import ScalingLawGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For scaling-law arithmetic with N=([0-9]+) parameters, D=([0-9]+) "
    r"tokens, and training budget F=([0-9]+) FLOPs/s, compute C=6ND, "
    r"Chinchilla-optimal tokens 20N, and tokens/s=F/\(6N\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    params = int(match.group(1))
    tokens = int(match.group(2))
    flops_per_second = int(match.group(3))
    nd = params * tokens
    compute = 6 * nd
    optimal_tokens = 20 * params
    denom = 6 * params
    tokens_per_second = Fraction(flops_per_second, denom)
    steps = [
        make_step("SCALING_SETUP", f"N={params}", f"D={tokens}",
                  f"F={flops_per_second}"),
        make_step("M", params, tokens, nd),
        make_step("M", 6, nd, compute),
        make_step("SCALING_COMPUTE", "6ND", compute),
        make_step("M", 20, params, optimal_tokens),
        make_step("CHINCHILLA", "20N", optimal_tokens),
        make_step("M", 6, params, denom),
        make_step("D", flops_per_second, denom,
                  fraction_text(tokens_per_second)),
        make_step("THROUGHPUT", "tokens_per_second",
                  fraction_text(tokens_per_second)),
    ]
    answer = (
        f"C={compute}; optimal_tokens={optimal_tokens}; "
        f"tokens_per_second={fraction_text(tokens_per_second)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestScalingLawGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ScalingLawGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "scaling_law_compute")
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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

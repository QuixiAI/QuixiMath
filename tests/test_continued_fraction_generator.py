import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.continued_fraction_generator import ContinuedFractionGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Find the simple continued fraction for (\d+)/(\d+) and list all "
    r"convergents\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def cf_text(partials):
    if len(partials) == 1:
        return f"[{partials[0]}]"
    return f"[{partials[0]}; {', '.join(str(v) for v in partials[1:])}]"


def frac_text(num, den):
    return f"{num}/{den}"


def convergent_text(convergents):
    return ", ".join(frac_text(num, den) for num, den in convergents)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return tuple(map(int, match.groups()))


def continued_fraction(num, den):
    partials = []
    divisions = []
    x, y = num, den
    while y:
        q = x // y
        r = x - q * y
        divisions.append((x, y, q, r))
        partials.append(q)
        x, y = y, r
    return partials, divisions


def expected_flow(num, den):
    partials, divisions = continued_fraction(num, den)
    steps = [
        make_step("CF_SETUP", frac_text(num, den)),
    ]
    for idx, (x, y, q, r) in enumerate(divisions):
        product = q * y
        steps.append(make_step("EUCLID_DIV", x, y, q, r))
        steps.append(make_step("M", q, y, product))
        steps.append(make_step("S", x, product, r))
        steps.append(make_step("CF_PARTIAL", f"a_{idx}", q))
    steps.append(make_step("CF_RESULT", cf_text(partials)))

    h_prev2, h_prev1 = 0, 1
    k_prev2, k_prev1 = 1, 0
    steps.append(make_step("CONV_INIT", "h_-2=0,h_-1=1",
                           "k_-2=1,k_-1=0"))
    convergents = []
    for idx, partial in enumerate(partials):
        h_prod = partial * h_prev1
        h = h_prod + h_prev2
        k_prod = partial * k_prev1
        k = k_prod + k_prev2
        steps.append(make_step("M", partial, h_prev1, h_prod))
        steps.append(make_step("A", h_prod, h_prev2, h))
        steps.append(make_step("M", partial, k_prev1, k_prod))
        steps.append(make_step("A", k_prod, k_prev2, k))
        steps.append(make_step("CONV_STEP", f"i={idx}", f"h={h}",
                               f"k={k}"))
        steps.append(make_step("CONVERGENT", f"i={idx}", frac_text(h, k)))
        convergents.append((h, k))
        h_prev2, h_prev1 = h_prev1, h
        k_prev2, k_prev1 = k_prev1, k

    answer = (
        f"continued fraction = {cf_text(partials)}; "
        f"convergents = {convergent_text(convergents)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer, convergents


class TestContinuedFractionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ContinuedFractionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "continued_fraction")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            num, den = parse_problem(result["problem"])
            expected_steps, answer, _ = expected_flow(num, den)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_convergents_and_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            num, den = parse_problem(result["problem"])
            self.assertEqual(gcd(num, den), 1)
            _, _, convergents = expected_flow(num, den)
            self.assertEqual(convergents[-1], (num, den))
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "EUCLID_DIV":
                    dividend, divisor, quotient, remainder = map(
                        int, fields[1:]
                    )
                    self.assertEqual(dividend, quotient * divisor + remainder)
                    self.assertGreaterEqual(remainder, 0)
                    self.assertLess(remainder, divisor)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
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

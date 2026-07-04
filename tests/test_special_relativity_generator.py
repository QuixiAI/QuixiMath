import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.special_relativity_generator import SpecialRelativityGenerator
from helpers import DELIM


TIME_RE = re.compile(
    r"A clock has proper time tau=(\d+) s and moves with beta=([^ ]+) "
    r"where gamma=([^ ]+)\. Find the dilated time t\."
)
LENGTH_RE = re.compile(
    r"A rod has proper length L0=(\d+) m and moves with beta=([^ ]+) "
    r"where gamma=([^ ]+)\. Find the contracted length L\."
)
EVENT_RE = re.compile(
    r"A frame has beta=([^ ]+) and gamma=([^ ]+)\. For event ct=(-?\d+), "
    r"x=(-?\d+) in c=1 units, compute ct_prime and x_prime\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_time(problem):
    proper_raw, beta_raw, gamma_raw = TIME_RE.fullmatch(problem).groups()
    proper_time = int(proper_raw)
    beta = Fraction(beta_raw)
    gamma = Fraction(gamma_raw)
    observed = gamma * proper_time
    steps = [
        make_step("REL_SETUP", "time_dilation",
                  f"beta={fraction_text(beta)}", f"gamma={fraction_text(gamma)}"),
        make_step("REL_FORMULA", "t=gamma*tau"),
        make_step("M", fraction_text(gamma), proper_time,
                  fraction_text(observed)),
    ]
    answer = f"t={fraction_text(observed)} s"
    return steps, answer


def expected_length(problem):
    length_raw, beta_raw, gamma_raw = LENGTH_RE.fullmatch(problem).groups()
    proper_length = int(length_raw)
    beta = Fraction(beta_raw)
    gamma = Fraction(gamma_raw)
    contracted = Fraction(proper_length, 1) / gamma
    steps = [
        make_step("REL_SETUP", "length_contraction",
                  f"beta={fraction_text(beta)}", f"gamma={fraction_text(gamma)}"),
        make_step("REL_FORMULA", "L=L0/gamma"),
        make_step("D", proper_length, fraction_text(gamma),
                  fraction_text(contracted)),
    ]
    answer = f"L={fraction_text(contracted)} m"
    return steps, answer


def expected_event(problem):
    beta_raw, gamma_raw, ct_raw, x_raw = EVENT_RE.fullmatch(problem).groups()
    beta = Fraction(beta_raw)
    gamma = Fraction(gamma_raw)
    ct = int(ct_raw)
    x = int(x_raw)
    beta_x = beta * x
    ct_minus = Fraction(ct) - beta_x
    ct_prime = gamma * ct_minus
    beta_ct = beta * ct
    x_minus = Fraction(x) - beta_ct
    x_prime = gamma * x_minus
    steps = [
        make_step("REL_SETUP", "lorentz_event",
                  f"beta={fraction_text(beta)}, gamma={fraction_text(gamma)}",
                  f"ct={ct}, x={x}"),
        make_step("REL_FORMULA",
                  "ct_prime=gamma*(ct-beta*x), x_prime=gamma*(x-beta*ct)"),
        make_step("M", fraction_text(beta), x, fraction_text(beta_x)),
        make_step("S", ct, fraction_text(beta_x), fraction_text(ct_minus)),
        make_step("M", fraction_text(gamma), fraction_text(ct_minus),
                  fraction_text(ct_prime)),
        make_step("M", fraction_text(beta), ct, fraction_text(beta_ct)),
        make_step("S", x, fraction_text(beta_ct), fraction_text(x_minus)),
        make_step("M", fraction_text(gamma), fraction_text(x_minus),
                  fraction_text(x_prime)),
    ]
    answer = (
        f"ct_prime={fraction_text(ct_prime)}; "
        f"x_prime={fraction_text(x_prime)}"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if TIME_RE.fullmatch(problem):
        steps, answer = expected_time(problem)
    elif LENGTH_RE.fullmatch(problem):
        steps, answer = expected_length(problem)
    else:
        steps, answer = expected_event(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSpecialRelativityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SpecialRelativityGenerator()

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
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in SpecialRelativityGenerator.VARIANTS:
            result = SpecialRelativityGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"special_relativity_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SpecialRelativityGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

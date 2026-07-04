import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.game_theory_generator import GameTheoryGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For the zero-sum 2x2 payoff matrix \[\[(\d+),(\d+)\],\[(\d+),(\d+)\]\] "
    r"for the row player, compute expected payoffs, the mixed-strategy "
    r"equilibrium, and the game value\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    a, b, c, d = (
        int(value) for value in PROBLEM_RE.fullmatch(example["problem"]).groups()
    )
    q_num = d - b
    p_num = d - c
    den_first = a - b
    den_value = den_first + p_num
    q = Fraction(q_num, den_value)
    p = Fraction(p_num, den_value)
    one_minus_q = 1 - q
    one_minus_p = 1 - p
    row1_q_term = q * a
    row1_other = one_minus_q * b
    row1_payoff = row1_q_term + row1_other
    row2_q_term = q * c
    row2_other = one_minus_q * d
    row2_payoff = row2_q_term + row2_other
    col1_p_term = p * a
    col1_other = one_minus_p * c
    col1_payoff = col1_p_term + col1_other
    col2_p_term = p * b
    col2_other = one_minus_p * d
    col2_payoff = col2_p_term + col2_other
    ad = a * d
    bc = b * c
    value_num = ad - bc
    value = Fraction(value_num, den_value)
    steps = [
        make_step("GAME_SETUP", f"payoffs=({a},{b};{c},{d})",
                  "row player maximizes, column player minimizes"),
        make_step("MIX_FORMULA", "q=(d-b)/(a-b-c+d)",
                  "p=(d-c)/(a-b-c+d)"),
        make_step("S", d, b, q_num),
        make_step("S", d, c, p_num),
        make_step("S", a, b, den_first),
        make_step("A", den_first, p_num, den_value),
        make_step("D", q_num, den_value, fraction_text(q)),
        make_step("D", p_num, den_value, fraction_text(p)),
        make_step("EXPECTED_PAYOFF", "row1 against q"),
        make_step("M", fraction_text(q), a, fraction_text(row1_q_term)),
        make_step("S", 1, fraction_text(q), fraction_text(one_minus_q)),
        make_step("M", fraction_text(one_minus_q), b,
                  fraction_text(row1_other)),
        make_step("A", fraction_text(row1_q_term), fraction_text(row1_other),
                  fraction_text(row1_payoff)),
        make_step("EXPECTED_PAYOFF", "row2 against q"),
        make_step("M", fraction_text(q), c, fraction_text(row2_q_term)),
        make_step("M", fraction_text(one_minus_q), d,
                  fraction_text(row2_other)),
        make_step("A", fraction_text(row2_q_term), fraction_text(row2_other),
                  fraction_text(row2_payoff)),
        make_step("EXPECTED_PAYOFF", "col1 against p"),
        make_step("M", fraction_text(p), a, fraction_text(col1_p_term)),
        make_step("S", 1, fraction_text(p), fraction_text(one_minus_p)),
        make_step("M", fraction_text(one_minus_p), c,
                  fraction_text(col1_other)),
        make_step("A", fraction_text(col1_p_term), fraction_text(col1_other),
                  fraction_text(col1_payoff)),
        make_step("EXPECTED_PAYOFF", "col2 against p"),
        make_step("M", fraction_text(p), b, fraction_text(col2_p_term)),
        make_step("M", fraction_text(one_minus_p), d,
                  fraction_text(col2_other)),
        make_step("A", fraction_text(col2_p_term), fraction_text(col2_other),
                  fraction_text(col2_payoff)),
        make_step("VALUE_FORMULA", "v=(ad-bc)/(a-b-c+d)"),
        make_step("M", a, d, ad),
        make_step("M", b, c, bc),
        make_step("S", ad, bc, value_num),
        make_step("D", value_num, den_value, fraction_text(value)),
        make_step("CHECK", f"row payoffs={fraction_text(row1_payoff)}",
                  f"column payoffs={fraction_text(col1_payoff)}"),
    ]
    answer = (
        f"row mix=({fraction_text(p)},{fraction_text(one_minus_p)}); "
        f"column mix=({fraction_text(q)},{fraction_text(one_minus_q)}); "
        f"value={fraction_text(value)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestGameTheoryGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GameTheoryGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "game_theory_zero_sum_2x2")
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

    def test_mixes_are_interior(self):
        for _ in range(300):
            result = self.gen.generate()
            answer = result["final_answer"]
            p, p_other, q, q_other = (
                Fraction(value) for value in re.search(
                    r"row mix=\(([^,]+),([^)]+)\); column mix=\(([^,]+),([^)]+)\)",
                    answer,
                ).groups()
            )
            for value in (p, p_other, q, q_other):
                self.assertGreater(value, 0)
                self.assertLess(value, 1)
            self.assertEqual(p + p_other, 1)
            self.assertEqual(q + q_other, 1)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

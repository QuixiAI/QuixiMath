import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.commutator_generator import CommutatorGenerator
from helpers import DELIM


DX_RE = re.compile(
    r"For test function f\(x\)=x(?:\^(\d+))?, compute \[D,x\]f where "
    r"D=d/dx\."
)
DX2_RE = re.compile(
    r"For test function f\(x\)=x(?:\^(\d+))?, compute \[D,x\^2\]f where "
    r"D=d/dx\."
)
XP_RE = re.compile(
    r"For test function f\(x\)=x(?:\^(\d+))? with hbar=(\d+), compute "
    r"\[x,p\]f where p=-i\*hbar\*d/dx\."
)
TERM_RE = re.compile(r"(?:(-?\d+)\*)?x(?:\^(\d+))?$")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def power_text(exp):
    if exp == 0:
        return "1"
    if exp == 1:
        return "x"
    return f"x^{exp}"


def term_text(coeff, exp):
    if coeff == 0:
        return "0"
    body = power_text(exp)
    if exp == 0:
        return str(coeff)
    if coeff == 1:
        return body
    if coeff == -1:
        return f"-{body}"
    return f"{coeff}*{body}"


def imag_term_text(coeff, exp):
    if coeff == 0:
        return "0"
    body = power_text(exp)
    if coeff == 1:
        head = "i"
    elif coeff == -1:
        head = "-i"
    else:
        head = f"{coeff}i"
    if exp == 0:
        return head
    return f"{head}*{body}"


def parse_exp(raw):
    return int(raw) if raw is not None else 1


def expected_d_x(n):
    n_plus_1 = n + 1
    xf = power_text(n_plus_1)
    d_xf = term_text(n_plus_1, n)
    df = term_text(n, n - 1)
    x_df = term_text(n, n)
    coeff = n_plus_1 - n
    result = term_text(coeff, n)
    steps = [
        make_step("COMM_SETUP", "[D,x]f", f"f={power_text(n)}", "D=d/dx"),
        make_step("COMM_FORMULA", "[A,B]f=A(Bf)-B(Af)"),
        make_step("APPLY_OPERATOR", "x f", xf),
        make_step("A", n, 1, n_plus_1),
        make_step("POWER_RULE", xf, d_xf),
        make_step("POWER_RULE", power_text(n), df),
        make_step("APPLY_OPERATOR", "x Df", x_df),
        make_step("S", n_plus_1, n, coeff),
        make_step("COMM_RESULT", "[D,x]f", result),
        make_step("CHECK", "identity", "[D,x]=1", "matches f"),
    ]
    answer = f"[D,x]f={result}"
    return steps, answer


def expected_d_x_squared(n):
    n_plus_2 = n + 2
    x2f = power_text(n_plus_2)
    d_x2f = term_text(n_plus_2, n + 1)
    df = term_text(n, n - 1)
    x2_df = term_text(n, n + 1)
    coeff = n_plus_2 - n
    result = term_text(coeff, n + 1)
    steps = [
        make_step("COMM_SETUP", "[D,x^2]f", f"f={power_text(n)}", "D=d/dx"),
        make_step("COMM_FORMULA", "[A,B]f=A(Bf)-B(Af)"),
        make_step("APPLY_OPERATOR", "x^2 f", x2f),
        make_step("A", n, 2, n_plus_2),
        make_step("POWER_RULE", x2f, d_x2f),
        make_step("POWER_RULE", power_text(n), df),
        make_step("APPLY_OPERATOR", "x^2 Df", x2_df),
        make_step("S", n_plus_2, n, coeff),
        make_step("COMM_RESULT", "[D,x^2]f", result),
        make_step("CHECK", "identity", "[D,x^2]=2x", "matches 2x f"),
    ]
    answer = f"[D,x^2]f={result}"
    return steps, answer


def expected_x_p(n, hbar):
    n_plus_1 = n + 1
    df = term_text(n, n - 1)
    hbar_n = hbar * n
    pf = imag_term_text(-hbar_n, n - 1)
    x_pf = imag_term_text(-hbar_n, n)
    xf = power_text(n_plus_1)
    d_xf = term_text(n_plus_1, n)
    hbar_n_plus_1 = hbar * n_plus_1
    p_xf = imag_term_text(-hbar_n_plus_1, n)
    coeff = -hbar_n - (-hbar_n_plus_1)
    result = imag_term_text(coeff, n)
    steps = [
        make_step("COMM_SETUP", "[x,p]f", f"f={power_text(n)}",
                  f"p=-i*hbar*D, hbar={hbar}"),
        make_step("COMM_FORMULA", "[A,B]f=A(Bf)-B(Af)"),
        make_step("POWER_RULE", power_text(n), df),
        make_step("M", hbar, n, hbar_n),
        make_step("APPLY_OPERATOR", "p f", pf),
        make_step("APPLY_OPERATOR", "x p f", x_pf),
        make_step("APPLY_OPERATOR", "x f", xf),
        make_step("A", n, 1, n_plus_1),
        make_step("POWER_RULE", xf, d_xf),
        make_step("M", hbar, n_plus_1, hbar_n_plus_1),
        make_step("APPLY_OPERATOR", "p(x f)", p_xf),
        make_step("S", -hbar_n, -hbar_n_plus_1, coeff),
        make_step("COMM_RESULT", "[x,p]f", result),
        make_step("CHECK", "identity", "[x,p]=i*hbar", f"matches {result}"),
    ]
    answer = f"[x,p]f={result}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    match = DX_RE.fullmatch(problem)
    if match:
        steps, answer = expected_d_x(parse_exp(match.group(1)))
    else:
        match = DX2_RE.fullmatch(problem)
        if match:
            steps, answer = expected_d_x_squared(parse_exp(match.group(1)))
        else:
            match = XP_RE.fullmatch(problem)
            assert match is not None, problem
            steps, answer = expected_x_p(parse_exp(match.group(1)),
                                         int(match.group(2)))
    steps.append(make_step("Z", answer))
    return steps, answer


def parse_power(text):
    if text == "1":
        return 0
    if text == "x":
        return 1
    match = re.fullmatch(r"x\^(\d+)", text)
    assert match is not None, text
    return int(match.group(1))


def parse_term(text):
    if text == "0":
        return 0, 0
    try:
        return int(text), 0
    except ValueError:
        pass
    if text == "x":
        return 1, 1
    if text == "-x":
        return -1, 1
    match = TERM_RE.fullmatch(text)
    assert match is not None, text
    coeff = int(match.group(1)) if match.group(1) is not None else 1
    exp = int(match.group(2)) if match.group(2) is not None else 1
    return coeff, exp


class TestCommutatorGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = CommutatorGenerator()

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

    def test_arithmetic_and_power_rule_steps(self):
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
                elif fields[0] == "POWER_RULE":
                    exp = parse_power(fields[1])
                    coeff, out_exp = parse_term(fields[2])
                    self.assertEqual(coeff, exp, raw_step)
                    self.assertEqual(out_exp, exp - 1, raw_step)

    def test_variants_are_available(self):
        for variant in CommutatorGenerator.VARIANTS:
            result = CommutatorGenerator(variant).generate()
            self.assertEqual(result["operation"], f"commutator_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CommutatorGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

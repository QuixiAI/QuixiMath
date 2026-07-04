import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.recurrence_generator import RecurrenceGenerator
from helpers import DELIM


RECURRENCE_RE = re.compile(
    r"For n >= 2, a_n = (-?\d+) a_\(n-1\) ([+-]) "
    r"(\d+) a_\(n-2\)(?: ([+-]) (\d+))?, with a_0 = (-?\d+) "
    r"and a_1 = (-?\d+)\. Use the characteristic-root method to find "
    r"a_(\d+)\."
)


def parse_problem(problem):
    match = RECURRENCE_RE.fullmatch(problem)
    assert match is not None, problem
    p_text, q_sign, q_abs, b_sign, b_abs, a0, a1, n = match.groups()
    q = int(q_abs) if q_sign == "+" else -int(q_abs)
    b = 0
    if b_sign is not None:
        b = int(b_abs) if b_sign == "+" else -int(b_abs)
    return {
        "variant": "constant" if b_sign is not None else "homogeneous",
        "p": int(p_text),
        "q": q,
        "b": b,
        "a0": int(a0),
        "a1": int(a1),
        "n": int(n),
    }


def iterate_answer(parts):
    if parts["n"] == 0:
        value = parts["a0"]
    elif parts["n"] == 1:
        value = parts["a1"]
    else:
        prev2 = parts["a0"]
        prev1 = parts["a1"]
        value = prev1
        for _ in range(2, parts["n"] + 1):
            value = parts["p"] * prev1 + parts["q"] * prev2 + parts["b"]
            prev2, prev1 = prev1, value
    return f"a_{parts['n']} = {value}"


def oracle_answer(example):
    return iterate_answer(parse_problem(example["problem"]))


def parse_roots(raw_field):
    match = re.fullmatch(r"lambda = (-?\d+), (-?\d+)", raw_field)
    assert match is not None, raw_field
    return tuple(map(int, match.groups()))


def coeff_term(coef, body):
    if coef == 1:
        return body
    if coef == -1:
        return f"-{body}"
    return f"{coef} {body}"


def signed_term(coef, body):
    sign = "+" if coef >= 0 else "-"
    magnitude = abs(coef)
    term_body = body if magnitude == 1 else f"{magnitude} {body}"
    return f"{sign} {term_body}"


def signed_const(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign} {abs(value)}"


def recurrence_text(parts):
    text = (
        f"a_n = {coeff_term(parts['p'], 'a_(n-1)')} "
        f"{signed_term(parts['q'], 'a_(n-2)')}"
    )
    if parts["variant"] == "constant":
        text = f"{text} {signed_const(parts['b'])}"
    return text


def check_step_arithmetic(example):
    parts = parse_problem(example["problem"])
    roots = None
    offset = 0
    if parts["variant"] == "constant":
        denom = 1 - parts["p"] - parts["q"]
        offset_fraction = Fraction(parts["b"], denom)
        if offset_fraction.denominator != 1:
            return False
        offset = offset_fraction.numerator

    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "REC_SETUP":
            if fields[1:] != [
                recurrence_text(parts),
                f"a_0 = {parts['a0']}, a_1 = {parts['a1']}",
            ]:
                return False
        elif op == "CHAR_ROOTS":
            roots = parse_roots(fields[1])
            r, s = roots
            if r == s or fields[2] != "distinct":
                return False
            if r * r - parts["p"] * r - parts["q"] != 0:
                return False
            if s * s - parts["p"] * s - parts["q"] != 0:
                return False
        elif op == "PARTICULAR_CHECK":
            match = re.fullmatch(r"K = (-?\d+)", fields[1])
            if match is None:
                return False
            k_value = int(match.group(1))
            if k_value != offset:
                return False
            if parts["p"] * k_value + parts["q"] * k_value + parts["b"] != k_value:
                return False
        elif op == "SHIFT":
            match = re.fullmatch(r"b_0 = (-?\d+), b_1 = (-?\d+)", fields[2])
            if match is None:
                return False
            b0, b1 = map(int, match.groups())
            if b0 != parts["a0"] - offset or b1 != parts["a1"] - offset:
                return False
        elif op == "CONST_SOLVE":
            if roots is None:
                return False
            match1 = re.fullmatch(r"C1 = (-?\d+)", fields[1])
            match2 = re.fullmatch(r"C2 = (-?\d+)", fields[2])
            if match1 is None or match2 is None:
                return False
            c1, c2 = int(match1.group(1)), int(match2.group(1))
            b0 = parts["a0"] - offset
            b1 = parts["a1"] - offset
            r, s = roots
            if c1 + c2 != b0:
                return False
            if c1 * r + c2 * s != b1:
                return False
        elif op == "POW":
            match = re.fullmatch(r"\((-?\d+)\)\^(\d+)", fields[1])
            if match is None:
                return False
            base, exponent = map(int, match.groups())
            if base ** exponent != int(fields[2]):
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "Z":
            if fields[1:] != [iterate_answer(parts)]:
                return False
    return True


class TestRecurrenceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RecurrenceGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("homogeneous", "constant"):
            gen = RecurrenceGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"], f"recurrence_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RecurrenceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.base_arithmetic_generator import BaseArithmeticGenerator
from generators.base_conversion_generator import DIGITS, from_base, to_base
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute base arithmetic from the prompt."""
    problem = example["problem"]
    m = re.search(
        r"In base (\d+), add ([0-9A-F]+)_\1 \+ ([0-9A-F]+)_\1",
        problem,
    )
    if m:
        base = int(m.group(1))
        a = from_base(m.group(2), base)
        b = from_base(m.group(3), base)
        return f"{to_base(a + b, base)}_{base}"
    m = re.search(
        r"In base (\d+), multiply ([0-9A-F]+)_\1 by ([0-9A-F])_\1",
        problem,
    )
    base = int(m.group(1))
    a = from_base(m.group(2), base)
    b = DIGITS.index(m.group(3))
    return f"{to_base(a * b, base)}_{base}"


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "BASE_ADD_COL":
            a_ch, b_ch, carry = re.fullmatch(
                r"([0-9A-F]) \+ ([0-9A-F]) \+ carry (\d+)", parts[2]
            ).groups()
            total, digit, out_carry = re.fullmatch(
                r"(\d+) -> digit ([0-9A-F]), carry (\d+)", parts[3]
            ).groups()
            total = int(total)
            out_carry = int(out_carry)
            base = (total - DIGITS.index(digit)) // out_carry if out_carry else None
            expected = DIGITS.index(a_ch) + DIGITS.index(b_ch) + int(carry)
            if total != expected:
                return False
            if out_carry and total != base * out_carry + DIGITS.index(digit):
                return False
        elif code == "BASE_MUL_COL":
            a_ch, b_ch, carry = re.fullmatch(
                r"([0-9A-F]) \* ([0-9A-F]) \+ carry (\d+)", parts[2]
            ).groups()
            total, _, _ = re.fullmatch(
                r"(\d+) -> digit ([0-9A-F]), carry (\d+)", parts[3]
            ).groups()
            expected = DIGITS.index(a_ch) * DIGITS.index(b_ch) + int(carry)
            if int(total) != expected:
                return False
        elif code == "BASE_CARRY":
            carry = int(parts[1].split()[1])
            digit, new_carry = re.fullmatch(
                r"digit ([0-9A-F]), carry (\d+)", parts[2]
            ).groups()
            # The actual base is in the setup step; any valid carry emission
            # must reduce the carry and emit a digit.
            if int(new_carry) >= carry or DIGITS.index(digit) < 0:
                return False
        elif code == "REVERSE":
            digits = parts[1].split(",")
            if "".join(reversed(digits)) != parts[2]:
                return False
    return True


class TestBaseArithmeticGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BaseArithmeticGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_column_steps_present(self):
        for variant in BaseArithmeticGenerator.VARIANTS:
            result = BaseArithmeticGenerator(variant).generate()
            codes = {s.split(DELIM)[0] for s in result["steps"]}
            self.assertTrue({"BASE_ADD_COL", "BASE_MUL_COL"} & codes)

    def test_answer_has_base_suffix(self):
        for _ in range(200):
            self.assertRegex(self.gen.generate()["final_answer"],
                             r"^[0-9A-F]+_(2|8|16)$")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(50):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            BaseArithmeticGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

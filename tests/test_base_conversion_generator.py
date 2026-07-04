import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.base_conversion_generator import (
    BaseConversionGenerator, DIGITS, from_base, to_base,
)
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute conversion from the problem text alone."""
    problem = example["problem"]
    m = re.search(r"binary ([01]+)_2 to decimal", problem)
    if m:
        return str(from_base(m.group(1), 2))
    m = re.search(r"decimal (\d+) to binary", problem)
    if m:
        return to_base(int(m.group(1)), 2)
    m = re.search(r"hexadecimal ([0-9A-F]+)_16 to decimal", problem)
    if m:
        return str(from_base(m.group(1), 16))
    m = re.search(r"decimal (\d+) to hexadecimal", problem)
    if m:
        return to_base(int(m.group(1)), 16)
    value = int(re.search(r"Represent (-\d+) in 8-bit", problem).group(1))
    return to_base(256 + value, 2).rjust(8, "0")


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "PLACE_VALUE":
            digit, base, pos = re.fullmatch(
                r"([0-9A-F]) \* (\d+)\^(\d+)", parts[1]
            ).groups()
            expected = DIGITS.index(digit) * (int(base) ** int(pos))
            if expected != int(parts[2]):
                return False
        elif code == "A":
            if int(parts[1]) + int(parts[2]) != int(parts[3]):
                return False
        elif code == "DIVMOD":
            n = int(parts[1])
            base = int(parts[2])
            q = int(parts[3])
            r = int(parts[4].split("=")[1])
            if n != base * q + r or not (0 <= r < base):
                return False
        elif code == "REVERSE":
            remainders = [r for r in parts[1].split(",") if r]
            if "".join(reversed(remainders)) != parts[2].lstrip("0"):
                # Two's-complement rows may left-pad to exactly 8 bits.
                if parts[2].lstrip("0") != "".join(reversed(remainders)):
                    return False
    return True


class TestBaseConversionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BaseConversionGenerator()

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

    def test_twos_complement_width(self):
        gen = BaseConversionGenerator("twos_complement")
        for _ in range(100):
            result = gen.generate()
            self.assertRegex(result["final_answer"], r"^[01]{8}$")

    def test_formula_steps_present(self):
        for variant in BaseConversionGenerator.VARIANTS:
            result = BaseConversionGenerator(variant).generate()
            codes = {s.split(DELIM)[0] for s in result["steps"]}
            self.assertTrue({"PLACE_VALUE", "DIVMOD"} & codes)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            BaseConversionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

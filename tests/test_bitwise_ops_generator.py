import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.bitwise_ops_generator import BitwiseOpsGenerator, OPS, bits
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute truth table or mask result from the prompt."""
    problem = example["problem"]
    m = re.search(r"truth table for bitwise (AND|OR|XOR)", problem)
    if m:
        op = m.group(1)
        rows = []
        for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
            rows.append(f"{a}{b}->{OPS[op](a, b)}")
        return ", ".join(rows)
    m = re.search(
        r"bitwise (AND|OR|XOR) to 4-bit value ([01]{4})_2 with mask "
        r"([01]{4})_2",
        problem,
    )
    op, value_bits, mask_bits = m.groups()
    value = int(value_bits, 2)
    mask = int(mask_bits, 2)
    result = OPS[op](value, mask)
    return f"{bits(result)}_2 = {result}"


def check_step_arithmetic(example):
    setup_op = None
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "BIT_RULE":
            setup_op = parts[1]
        elif code == "BIT_ROW":
            if len(parts) == 3:
                a, op, b = re.fullmatch(r"([01]) (AND|OR|XOR) ([01])",
                                        parts[1]).groups()
                if OPS[op](int(a), int(b)) != int(parts[2]):
                    return False
            else:
                a, op, b = re.fullmatch(r"([01]) (AND|OR|XOR) ([01])",
                                        parts[2]).groups()
                if setup_op != op or OPS[op](int(a), int(b)) != int(parts[3]):
                    return False
        elif code == "REVERSE":
            low_bits = parts[1].split(",")
            if "".join(reversed(low_bits)) != parts[2]:
                return False
    return True


class TestBitwiseOpsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BitwiseOpsGenerator()

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

    def test_mask_has_four_bit_rows(self):
        gen = BitwiseOpsGenerator("mask")
        for _ in range(100):
            rows = [s for s in gen.generate()["steps"]
                    if s.startswith(f"BIT_ROW{DELIM}")]
            self.assertEqual(len(rows), 4)

    def test_all_ops_occur(self):
        seen = set()
        for _ in range(200):
            result = self.gen.generate()
            m = re.search(r"\b(AND|OR|XOR)\b", result["problem"])
            seen.add(m.group(1))
        self.assertEqual(seen, {"AND", "OR", "XOR"})

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
            BitwiseOpsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

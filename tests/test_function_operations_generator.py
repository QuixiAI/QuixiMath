import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.function_operations_generator import (
    FunctionOperationsGenerator,
)
from helpers import DELIM


def parse_rule(rule, var):
    """'3x + 5' or 'x^2 - 4' -> a callable on Fraction."""
    m = re.fullmatch(rf"{var}\^2 ([+-]) (\d+)", rule)
    if m:
        c = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
        return lambda x: x * x + c
    m = re.fullmatch(rf"(-?\d+){var} ([+-]) (\d+)", rule)
    assert m, rule
    a = int(m.group(1))
    b = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
    return lambda x: a * x + b


def oracle_answer(example):
    """Independently evaluates the function operation from the text."""
    m = re.fullmatch(
        r"Given ([a-z])\(([a-z])\) = (.+) and ([a-z])\(\2\) = (.+), "
        r"find \(\1 ?([+\-·/]) ?\4\)\((-?\d+)\)\.", example["problem"])
    assert m, example["problem"]
    var = m.group(2)
    f = parse_rule(m.group(3), var)
    g = parse_rule(m.group(5), var)
    op, k = m.group(6), Fraction(m.group(7))
    fv, gv = f(k), g(k)
    value = {"+": fv + gv, "-": fv - gv, "·": fv * gv,
             "/": fv / gv if gv else None}[op]
    return str(value)


class TestFunctionOperationsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FunctionOperationsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-evaluate with Fraction arithmetic."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(500):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] in ("M", "A", "S", "D") and len(f) == 4:
                    x, y, z = (Fraction(v) for v in f[1:])
                    got = {"M": lambda: x * y, "A": lambda: x + y,
                           "S": lambda: x - y, "D": lambda: x / y}[f[0]]()
                    self.assertEqual(got, z, s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "FRAC_REDUCE":
                    raw, red = f[1], f[2]
                    n, d = raw.split("/")
                    self.assertEqual(Fraction(int(n), int(d)),
                                     Fraction(red), s)
                    self.assertNotEqual(raw, red, s)

    def test_evals_match_combine_operands(self):
        """The two EVAL values feed the combining step."""
        for _ in range(300):
            result = self.gen.generate()
            evals = [s.split(DELIM)[2] for s in result["steps"]
                     if s.startswith(f"EVAL{DELIM}")]
            self.assertEqual(len(evals), 2, result["steps"])
            combine = result["steps"][-2]
            if combine.startswith(f"FRAC_REDUCE{DELIM}") or \
                    combine.startswith(f"REWRITE{DELIM}"):
                raw = next(s for s in result["steps"]
                           if s.startswith(f"REWRITE{DELIM}"))
                self.assertEqual(raw.split(DELIM)[1],
                                 f"{evals[0]}/{evals[1]}", result["steps"])
            else:
                fields = combine.split(DELIM)
                self.assertEqual(fields[1:3], evals, result["steps"])

    def test_funcop_unfolds_notation(self):
        for _ in range(200):
            result = self.gen.generate()
            unfold = next(s for s in result["steps"]
                          if s.startswith(f"FUNC_OP{DELIM}"))
            m = re.search(r"find (.+)\.$", result["problem"])
            self.assertEqual(unfold.split(DELIM)[1], m.group(1))

    def test_divide_never_divides_by_zero(self):
        gen = FunctionOperationsGenerator("divide")
        for _ in range(300):
            result = gen.generate()
            evals = [int(s.split(DELIM)[2]) for s in result["steps"]
                     if s.startswith(f"EVAL{DELIM}")]
            self.assertNotEqual(evals[1], 0, result["problem"])

    def test_divide_produces_integers_and_fractions(self):
        gen = FunctionOperationsGenerator("divide")
        kinds = set()
        for _ in range(200):
            result = gen.generate()
            kinds.add("frac" if "/" in result["final_answer"] else "int")
        self.assertEqual(kinds, {"frac", "int"})

    def test_fraction_answers_are_reduced_positive_den(self):
        gen = FunctionOperationsGenerator("divide")
        for _ in range(300):
            result = gen.generate()
            if "/" in result["final_answer"]:
                n, d = result["final_answer"].split("/")
                self.assertGreater(int(d), 1, result["final_answer"])
                self.assertEqual(str(Fraction(int(n), int(d))),
                                 result["final_answer"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"function_op_add", "function_op_subtract",
                               "function_op_multiply", "function_op_divide"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FunctionOperationsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

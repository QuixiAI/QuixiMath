import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.derangement_generator import DerangementGenerator
from helpers import DELIM


def derangements(n):
    values = [1, 0]
    for m in range(2, n + 1):
        values.append((m - 1) * (values[m - 1] + values[m - 2]))
    return values


def parse_problem(problem):
    match = re.fullmatch(
        r"How many derangements are there of (\d+) distinct [a-z]+\?",
        problem,
    )
    assert match is not None, problem
    return int(match.group(1))


def oracle_parts(example):
    n = parse_problem(example["problem"])
    values = derangements(n)
    return {"n": n, "values": values, "answer": f"D_{n} = {values[n]}"}


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    seen = {}
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "DERANGE_SETUP":
            if fields[1:] != [f"n = {parts['n']}", "no item fixed"]:
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "DERANGE_VALUE":
            m = int(fields[1].removeprefix("D_"))
            value = int(fields[2])
            if value != parts["values"][m]:
                return False
            seen[m] = value
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return all(m in seen for m in range(2, parts["n"] + 1))


class TestDerangementGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DerangementGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_fixed_variant_constructor(self):
        gen = DerangementGenerator("recurrence")
        result = gen.generate()
        self.assertEqual(result["operation"], "derangement_recurrence")
        with self.assertRaises(ValueError):
            DerangementGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

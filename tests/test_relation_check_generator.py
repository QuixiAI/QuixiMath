import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.relation_check_generator import RelationCheckGenerator
from helpers import DELIM


def fmt_set(values):
    return "{" + ", ".join(str(v) for v in values) + "}"


def fmt_pair(pair):
    return f"({pair[0]}, {pair[1]})"


def fmt_relation(pairs):
    ordered = sorted(pairs)
    return "{" + ", ".join(fmt_pair(pair) for pair in ordered) + "}" if ordered else "{}"


def parse_set(text):
    return [int(x.strip()) for x in text[1:-1].split(",") if x.strip()]


def parse_relation(text):
    if text == "{}":
        return []
    return [(int(a), int(b)) for a, b in re.findall(r"\((\d+), (\d+)\)", text)]


def yes_no(value):
    return "yes" if value else "no"


def properties(A, R):
    Rset = set(R)
    reflexive = all((a, a) in Rset for a in A)
    symmetric = all((b, a) in Rset for a, b in Rset)
    antisymmetric = all(a == b or (b, a) not in Rset for a, b in Rset)
    transitive = True
    for a, b in Rset:
        for c, d in Rset:
            if b == c and (a, d) not in Rset:
                transitive = False
    return reflexive, symmetric, antisymmetric, transitive


def answer_text(props):
    names = ["reflexive", "symmetric", "antisymmetric", "transitive"]
    return "; ".join(f"{name} {yes_no(value)}"
                     for name, value in zip(names, props))


def parse_problem(problem):
    match = re.fullmatch(
        r"For A = (\{.*\}) and R = (\{.*\}), determine whether R is "
        r"reflexive, symmetric, antisymmetric, and transitive\.",
        problem,
    )
    assert match is not None, problem
    return parse_set(match.group(1)), parse_relation(match.group(2))


def oracle_parts(example):
    A, R = parse_problem(example["problem"])
    props = properties(A, R)
    return {
        "A": A,
        "R": sorted(R),
        "Rset": set(R),
        "props": props,
        "answer": answer_text(props),
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    prop_results = {}
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "REL_SETUP":
            expected = [f"A = {fmt_set(parts['A'])}",
                        f"R = {fmt_relation(parts['R'])}"]
            if fields[1:] != expected:
                return False
        elif op == "REFLEXIVE_CHECK":
            pair = tuple(map(int, re.fullmatch(r"\((\d+), (\d+)\)", fields[1]).groups()))
            present = pair in parts["Rset"]
            if fields[2] != ("present" if present else "missing"):
                return False
        elif op == "SYMMETRIC_CHECK":
            pair = tuple(map(int, re.fullmatch(r"\((\d+), (\d+)\)", fields[1]).groups()))
            reverse = (pair[1], pair[0])
            if fields[2] != f"reverse {fmt_pair(reverse)}":
                return False
            if fields[3] != ("present" if reverse in parts["Rset"] else "missing"):
                return False
        elif op == "ANTISYM_CHECK":
            pair = tuple(map(int, re.fullmatch(r"\((\d+), (\d+)\)", fields[1]).groups()))
            reverse = (pair[1], pair[0])
            violation = reverse in parts["Rset"]
            if fields[2] != f"reverse {fmt_pair(reverse)}":
                return False
            if fields[3] != ("violation" if violation else "ok"):
                return False
        elif op == "TRANSITIVE_CHECK":
            pairs = re.findall(r"\((\d+), (\d+)\)", fields[1])
            first = tuple(map(int, pairs[0]))
            second = tuple(map(int, pairs[1]))
            needed = (first[0], second[1])
            if fields[2] != f"need {fmt_pair(needed)}":
                return False
            if fields[3] != ("present" if needed in parts["Rset"] else "missing"):
                return False
        elif op == "PROPERTY_RESULT":
            prop_results[fields[1]] = fields[2]
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    names = ["reflexive", "symmetric", "antisymmetric", "transitive"]
    return all(prop_results.get(name) == yes_no(value)
               for name, value in zip(names, parts["props"]))


class TestRelationCheckGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RelationCheckGenerator()

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

    def test_fixed_variant_constructor(self):
        gen = RelationCheckGenerator("property_check")
        result = gen.generate()
        self.assertEqual(result["operation"], "relation_check_property_check")
        with self.assertRaises(ValueError):
            RelationCheckGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

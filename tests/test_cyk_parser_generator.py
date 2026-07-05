import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.cyk_parser_generator import CYKParserGenerator
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def set_text(values):
    values = sorted(values)
    return "{" + ",".join(values) + "}" if values else "{}"


def parse_problem(problem):
    grammar = re.search(r"grammar (.+?); string ([ab]+)", problem)
    if grammar:
        return grammar.group(1), grammar.group(2)
    grammar = re.search(r"string ([ab]+) with grammar (.+?)\.", problem)
    if grammar:
        return grammar.group(2), grammar.group(1)
    grammar = re.search(r"grammar (.+?) and input ([ab]+)", problem)
    assert grammar is not None, problem
    return grammar.group(1), grammar.group(2)


def parse_rules(text):
    rules = {}
    for clause in text.split("; "):
        lhs, rhs_text = clause.split("->")
        rules[lhs] = [tuple(rhs.split()) for rhs in rhs_text.split(" or ")]
    return rules


def oracle(problem):
    grammar_text, text = parse_problem(problem)
    rules = parse_rules(grammar_text)
    rev = {}
    for lhs, alternatives in rules.items():
        for rhs in alternatives:
            rev.setdefault(rhs, set()).add(lhs)
    n = len(text)
    table = [[set() for _ in range(n)] for _ in range(n)]
    for i, ch in enumerate(text):
        table[i][i] = set(rev.get((ch,), set()))
    for span in range(2, n + 1):
        for i in range(n - span + 1):
            j = i + span - 1
            cell = set()
            for k in range(i, j):
                for left in table[i][k]:
                    for right in table[k + 1][j]:
                        cell.update(rev.get((left, right), set()))
            table[i][j] = cell
    top = table[0][n - 1]
    status = "accepted" if "S" in top else "rejected"
    return f"{status}; top cell = {set_text(top)}"


class TestCYKParserGenerator(unittest.TestCase):
    def test_contract_oracle_and_diverse_phrasing(self):
        random.seed(123)
        gen = CYKParserGenerator()
        openings = set()
        saw = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["operation"], "cyk_parser_membership")
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
            saw.add(result["final_answer"].split(";", 1)[0])
            openings.add(result["problem"].split(" ", 2)[0])
        self.assertEqual(saw, {"accepted", "rejected"})
        self.assertGreaterEqual(len(openings), 2)


if __name__ == "__main__":
    unittest.main()

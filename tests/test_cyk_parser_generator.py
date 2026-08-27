import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.cyk_parser_generator import CYKParserGenerator
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


RULE_RE = r"[A-Z]->(?:[a-z]|[A-Z] [A-Z])(?: or (?:[a-z]|[A-Z] [A-Z]))*"
GRAMMAR_RE = re.compile(rf"{RULE_RE}(?:; {RULE_RE})*")
STRING_RE = re.compile(r"(?:string|input|word) ([a-z]+)")


def set_text(values):
    values = sorted(values)
    return "{" + ",".join(values) + "}" if values else "{}"


def parse_problem(problem):
    """Pull the grammar and the input string out of any phrasing."""
    grammar = GRAMMAR_RE.search(problem)
    assert grammar is not None, problem
    text = STRING_RE.search(problem)
    assert text is not None, problem
    return grammar.group(0), text.group(1)


def parse_rules(text):
    rules = {}
    for clause in text.split("; "):
        lhs, rhs_text = clause.split("->")
        assert lhs not in rules, text
        rules[lhs] = [tuple(rhs.split()) for rhs in rhs_text.split(" or ")]
    return rules


def derives(rules, symbol, word, memo):
    """Top-down memoized derivation test (independent of the CYK table)."""
    key = (symbol, word)
    if key in memo:
        return memo[key]
    result = False
    for rhs in rules.get(symbol, []):
        if len(rhs) == 1:
            if word == rhs[0]:
                result = True
        else:
            for cut in range(1, len(word)):
                if (derives(rules, rhs[0], word[:cut], memo)
                        and derives(rules, rhs[1], word[cut:], memo)):
                    result = True
                    break
        if result:
            break
    memo[key] = result
    return result


def oracle_cell(rules, word, memo):
    return {name for name in rules if derives(rules, name, word, memo)}


def oracle(problem):
    grammar, word = parse_problem(problem)
    rules = parse_rules(grammar)
    memo = {}
    top = oracle_cell(rules, word, memo)
    status = "accepted" if "S" in top else "rejected"
    return f"{status}; top cell = {set_text(top)}"


def check_steps(case, result):
    grammar, word = parse_problem(result["problem"])
    rules = parse_rules(grammar)
    memo = {}
    n = len(word)
    seen = set()
    for raw_step in result["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        seen.add(op)
        if op == "CYK_SETUP":
            case.assertEqual(fields[1], f"string {word}")
            case.assertEqual(fields[2], f"length {n}")
        elif op == "CYK_RULE":
            case.assertIn(fields[1], rules)
            expected = " or ".join(
                " ".join(rhs) for rhs in
                sorted(rules[fields[1]], key=lambda r: (len(r), r)))
            case.assertEqual(fields[2], expected)
        elif op == "CYK_TERMINAL":
            index = int(fields[1].split(" ")[1].split(",")[0]) - 1
            case.assertEqual(fields[2], word[index])
            case.assertEqual(fields[3],
                             set_text(oracle_cell(rules, word[index], memo)))
        elif op == "CYK_CELL":
            i, j = (int(part) for part in fields[1].split(","))
            case.assertEqual(
                fields[2], set_text(oracle_cell(rules, word[i - 1:j], memo)))
        elif op == "CYK_SPLIT":
            cell = fields[1].split(" ")[1]
            i, j = (int(part) for part in cell.split(","))
            left, right = fields[2].split(" x ")
            li, lj = (int(part) for part in left.split(","))
            ri, rj = (int(part) for part in right.split(","))
            case.assertEqual((li, rj), (i, j))
            case.assertEqual(ri, lj + 1)
            left_set, right_set = fields[3].split(" x ")
            case.assertEqual(
                left_set, set_text(oracle_cell(rules, word[li - 1:lj], memo)))
            case.assertEqual(
                right_set, set_text(oracle_cell(rules, word[ri - 1:rj], memo)))
        elif op == "CYK_COMBINE":
            lvar, rvar = fields[1].split(" ")
            parents = {name for name in rules
                       if (lvar, rvar) in rules[name]}
            case.assertEqual(fields[2], set_text(parents))
            case.assertTrue(parents)
        elif op == "CHECK":
            case.assertEqual(fields[1], "S in top cell")
            case.assertEqual(fields[2],
                             result["final_answer"].split(";", 1)[0])
        elif op == "Z":
            case.assertEqual(fields[1:], [result["final_answer"]])
        elif op != "CYK_SPAN":
            raise AssertionError(f"unexpected op-code {op}")
    case.assertLessEqual({"CYK_SETUP", "CYK_RULE", "CYK_TERMINAL", "CYK_CELL",
                          "CYK_SPLIT", "CHECK", "Z"}, seen)


class TestCYKParserGenerator(unittest.TestCase):
    def test_contract_oracle_and_diverse_phrasing(self):
        random.seed(123)
        gen = CYKParserGenerator()
        openings = set()
        grammars = set()
        lengths = set()
        saw = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertNotIn(DELIM, result["problem"])
            self.assertEqual(result["operation"], "cyk_parser_membership")
            self.assertEqual(result["final_answer"], oracle(result["problem"]),
                             result["problem"])
            grammar, word = parse_problem(result["problem"])
            grammars.add(grammar)
            lengths.add(len(word))
            saw.add(result["final_answer"].split(";", 1)[0])
            openings.add(result["problem"].split(" ", 2)[0])
        self.assertEqual(saw, {"accepted", "rejected"})
        self.assertGreaterEqual(len(openings), 4)
        self.assertGreaterEqual(len(grammars), 250)
        self.assertGreaterEqual(len(lengths), 3)

    def test_step_content(self):
        random.seed(7)
        gen = CYKParserGenerator()
        for _ in range(120):
            check_steps(self, gen.generate())

    def test_deterministic_under_seed(self):
        gen = CYKParserGenerator()
        random.seed(99)
        first = [gen.generate() for _ in range(15)]
        random.seed(99)
        second = [gen.generate() for _ in range(15)]
        self.assertEqual([ex["problem"] for ex in first],
                         [ex["problem"] for ex in second])
        self.assertEqual([ex["steps"] for ex in first],
                         [ex["steps"] for ex in second])


if __name__ == "__main__":
    unittest.main()

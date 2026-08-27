"""Independent parser/evaluator checks for SetExpressionGenerator."""
import random
import re
import unittest

from generators.set_expression_generator import QUERIES, SetExpressionGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def operation_count(node):
    kind = node[0]
    if kind in ("name", "literal", "universe"):
        return 0
    if kind == "comp":
        return 1 + operation_count(node[1])
    return 1 + operation_count(node[1]) + operation_count(node[2])


def contains_kind(node, wanted):
    if node[0] == wanted:
        return True
    if node[0] in ("name", "literal", "universe"):
        return False
    if node[0] == "comp":
        return contains_kind(node[1], wanted)
    return contains_kind(node[1], wanted) or contains_kind(node[2], wanted)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"U = (.+)\. A = (.+)\. B = (.+)\. C = (.+)\. Expression: (.+)\.",
        body,
    )
    assert match is not None, body
    universe, set_a, set_b, set_c = (
        oracle.parse_set(match.group(index)) for index in range(1, 5)
    )
    expression = oracle.parse_set_expression(match.group(5))
    env = {"A": set_a, "B": set_b, "C": set_c}
    result = oracle.eval_set_expression(expression, env, universe)
    return {"variant": variant, "query": query, "U": universe, "env": env,
            "expression": expression, "result": result,
            "answer": oracle.roster_text(result)}


class SetExpressionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(602117)

    def test_output_contract(self):
        example = SetExpressionGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SetExpressionGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_subexpressions_scans_and_rewrites_are_exact(self):
        generator = SetExpressionGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [item.split(DELIM) for item in example["steps"]]
            index = 1
            rewrite_results = []
            while steps[index][0] == "SUBEXPR":
                subexpression = oracle.parse_set_expression(steps[index][1])
                result = oracle.eval_set_expression(
                    subexpression, parts["env"], parts["U"])
                self.assertEqual(steps[index][2], oracle.roster_text(result))
                kind = subexpression[0]
                if kind == "comp":
                    left = oracle.eval_set_expression(
                        subexpression[1], parts["env"], parts["U"])
                    right = None
                else:
                    left = oracle.eval_set_expression(
                        subexpression[1], parts["env"], parts["U"])
                    right = oracle.eval_set_expression(
                        subexpression[2], parts["env"], parts["U"])
                index += 1
                scanned = []
                while steps[index][0] == "ELEMENT_SCAN":
                    element = int(steps[index][1])
                    scanned.append(element)
                    if right is None:
                        expected_membership = (
                            f"operand={'yes' if element in left else 'no'}")
                    else:
                        expected_membership = (
                            f"left={'yes' if element in left else 'no'}, "
                            f"right={'yes' if element in right else 'no'}")
                    self.assertEqual(steps[index][2], expected_membership)
                    self.assertEqual(steps[index][3],
                                     "keep" if element in result else "skip")
                    index += 1
                self.assertEqual(scanned, sorted(parts["U"]))
                self.assertEqual(steps[index][0], "REWRITE")
                rewritten = oracle.parse_set_expression(steps[index][1])
                self.assertEqual(
                    oracle.eval_set_expression(rewritten, parts["env"], parts["U"]),
                    parts["result"],
                )
                rewrite_results.append(rewritten)
                index += 1
            self.assertEqual(oracle.eval_set_expression(
                rewrite_results[-1], parts["env"], parts["U"]), parts["result"])

    def test_all_variants_phrasings_and_shapes(self):
        for variant in SetExpressionGenerator.VARIANTS:
            generator = SetExpressionGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"set_expression_{variant}")
                seen_queries.add(parts["query"])
                count = operation_count(parts["expression"])
                if variant == "two_step":
                    self.assertEqual(count, 2)
                elif variant == "three_step":
                    self.assertEqual(count, 3)
                elif variant == "with_complement":
                    self.assertTrue(contains_kind(parts["expression"], "comp"))
                else:
                    self.assertTrue(contains_kind(parts["expression"], "symdiff"))
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SetExpressionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SetExpressionGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

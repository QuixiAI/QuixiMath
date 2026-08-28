"""Independent Cantor-normal-form oracle for OrdinalArithmeticGenerator."""
import random
import re
import unittest

from generators.ordinal_arithmetic_generator import OrdinalArithmeticGenerator, QUERIES
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def comparison_symbol(left, right):
    return "<" if left < right else ">" if left > right else "="


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "add":
        match = re.fullmatch(
            r"Using ordinal arithmetic, compute the sum\. Left operand: "
            r"(.+)\. Right operand: (.+)\.", body)
        assert match is not None, body
        left, right = map(oracle.parse_ordinal, match.groups())
        answer = str(left + right)
        expression = f"{match.group(1)} + {match.group(2)}"
    elif variant == "multiply":
        match = re.fullmatch(
            r"Using ordinal arithmetic, compute the product\. Left operand: "
            r"(.+)\. Right operand: (.+)\.", body)
        assert match is not None, body
        left, right = map(oracle.parse_ordinal, match.groups())
        answer = str(left * right)
        expression = f"({match.group(1)}) · ({match.group(2)})"
    elif variant == "compare":
        match = re.fullmatch(
            r"Compare two ordinals in Cantor normal form\. Left ordinal: "
            r"(.+)\. Right ordinal: (.+)\.", body)
        assert match is not None, body
        left, right = map(oracle.parse_ordinal, match.groups())
        answer = (f"{match.group(1)} {comparison_symbol(left, right)} "
                  f"{match.group(2)}")
        expression = None
    else:
        match = re.fullmatch(
            r"Convert an ordinal expression to Cantor normal form\. "
            r"Expression: (.+)\.", body)
        assert match is not None, body
        expression = match.group(1)
        left = right = None
        answer = str(oracle.parse_ordinal(expression))
    return {"variant": variant, "query": query, "answer": answer,
            "left": left, "right": right, "expression": expression}


class OrdinalArithmeticGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(577215)

    def test_output_contract(self):
        example = OrdinalArithmeticGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = OrdinalArithmeticGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_cnf_and_step_arithmetic_are_exact(self):
        generator = OrdinalArithmeticGenerator()
        for _ in range(350):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "CNF":
                    self.assertTrue(oracle.is_canonical_ordinal(fields[1]),
                                    fields[1])

    def test_rewrite_steps_preserve_ordinal_value(self):
        generator = OrdinalArithmeticGenerator("normal_form")
        for _ in range(250):
            example = generator.generate()
            rewrite = next(raw.split(DELIM, 1)[1] for raw in example["steps"]
                           if raw.startswith("REWRITE" + DELIM))
            expression, result = rewrite.rsplit(" = ", 1)
            self.assertEqual(oracle.parse_ordinal(expression),
                             oracle.parse_ordinal(result))

    def test_noncommutative_examples_occur(self):
        one_plus_omega = oracle.parse_ordinal("1 + ω")
        omega_plus_one = oracle.parse_ordinal("ω + 1")
        self.assertEqual(str(one_plus_omega), "ω")
        self.assertEqual(str(omega_plus_one), "ω + 1")
        self.assertNotEqual(one_plus_omega, omega_plus_one)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in OrdinalArithmeticGenerator.VARIANTS:
            generator = OrdinalArithmeticGenerator(variant)
            seen_queries = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"ordinal_arithmetic_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            OrdinalArithmeticGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = OrdinalArithmeticGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

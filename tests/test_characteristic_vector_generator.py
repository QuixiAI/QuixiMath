"""Independent ordered-bit oracle for CharacteristicVectorGenerator."""
import random
import re
import unittest

from generators.characteristic_vector_generator import QUERIES, CharacteristicVectorGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def bits(universe, subset):
    return "".join("1" if element in subset else "0" for element in universe)


def apply_expression(expression, universe, first, second):
    if expression == "A ∩ B":
        return first & second
    if expression == "A ∪ B":
        return first | second
    if expression == "A Δ B":
        return first ^ second
    if expression in ("A − B", "A ∩ Bᶜ"):
        return first - second
    if expression == "Aᶜ":
        return frozenset(universe) - first
    raise AssertionError(expression)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "encode":
        match = re.fullmatch(r"Ordered universe U = (.+)\. A = (.+)\.", body)
        assert match is not None, body
        universe = tuple(oracle.parse_roster(match.group(1)))
        first = oracle.parse_set(match.group(2))
        answer = bits(universe, first)
        return {"variant": variant, "query": query, "U": universe,
                "A": first, "answer": answer}
    if variant == "decode":
        match = re.fullmatch(
            r"Ordered universe U = (.+)\. Vector v = ([01]+)\.", body)
        assert match is not None, body
        universe = tuple(oracle.parse_roster(match.group(1)))
        vector = match.group(2)
        result = frozenset(element for element, bit in zip(universe, vector)
                           if bit == "1")
        return {"variant": variant, "query": query, "U": universe,
                "vector": vector, "result": result,
                "answer": oracle.roster_text(result)}
    if variant == "bitwise_op":
        match = re.fullmatch(
            r"Ordered universe U = (.+)\. A = (.+)\. B = (.+)\. "
            r"Expression: (.+)\.", body)
        assert match is not None, body
        expression = match.group(4)
    else:
        match = re.fullmatch(
            r"Ordered universe U = (.+)\. A = (.+)\. B = (.+)\. "
            r"Set operation: (.+)\. Boolean form: (.+)\.", body)
        assert match is not None, body
        expression = match.group(4)
    universe = tuple(oracle.parse_roster(match.group(1)))
    first, second = oracle.parse_set(match.group(2)), oracle.parse_set(match.group(3))
    result = apply_expression(expression, universe, first, second)
    vector = bits(universe, result)
    return {"variant": variant, "query": query, "U": universe,
            "A": first, "B": second, "expression": expression,
            "result": result, "vector": vector,
            "answer": f"{vector} = {oracle.roster_text(result)}"}


class CharacteristicVectorGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(419921)

    def test_output_contract(self):
        example = CharacteristicVectorGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CharacteristicVectorGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_each_membership_bit_operation_and_decode_is_exact(self):
        generator = CharacteristicVectorGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [item.split(DELIM) for item in example["steps"]]
            bit_rows = [item for item in steps if item[0] == "BIT"]
            self.assertEqual(len(bit_rows), len(parts["U"]))
            for element, row in zip(parts["U"], bit_rows):
                self.assertEqual(row[1], str(element))
                if "A" in parts:
                    self.assertEqual(row[2],
                                     f"A={1 if element in parts['A'] else 0}")
            if "result" in parts:
                decode = next(item for item in steps if item[0] == "DECODE")
                expected_vector = parts.get("vector", bits(parts["U"], parts["result"]))
                self.assertEqual(decode, ["DECODE", expected_vector,
                                          oracle.roster_text(parts["result"])])
            if parts["variant"] in ("bitwise_op", "duality"):
                bitwise = next(item for item in steps if item[0] == "BITWISE")
                self.assertEqual(bitwise[-1], parts["vector"])

    def test_all_variants_phrasings_and_operations_are_reachable(self):
        operations = set()
        for variant in CharacteristicVectorGenerator.VARIANTS:
            generator = CharacteristicVectorGenerator(variant)
            seen_queries = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"characteristic_vector_{variant}")
                seen_queries.add(parts["query"])
                if "expression" in parts:
                    operations.add(parts["expression"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))
        self.assertTrue({"A ∩ B", "A ∪ B", "A Δ B", "Aᶜ"} <= operations)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CharacteristicVectorGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CharacteristicVectorGenerator()
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

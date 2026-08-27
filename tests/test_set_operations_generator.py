"""Independent A9 checks for the expanded SetOperationsGenerator."""
import itertools
import random
import re
import unittest

from generators.set_operations_generator import QUERIES, SetOperationsGenerator
from helpers import DELIM
from tests import foundations_oracle as set_oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            if problem.endswith(f" {query}"):
                return problem[:-(len(query) + 1)], variant, query
    raise AssertionError(problem)


def roster_text(values):
    return set_oracle.roster_text(values)


def power_text(values):
    groups = [frozenset(combo) for size in range(len(values) + 1)
              for combo in itertools.combinations(values, size)]
    return "{" + ", ".join(roster_text(group) for group in groups) + "}"


def pair_roster(values_a, values_b):
    pairs = [(first, second) for first in values_a for second in values_b]
    return set_oracle.roster_text(pairs)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("algebra", "integer_elements", "symmetric_difference"):
        if variant == "symmetric_difference":
            match = re.fullmatch(r"A = (.+)\. B = (.+)\.", body)
            symbol = "Δ"
        else:
            match = re.fullmatch(r"A = (.+)\. B = (.+)\. Operation: A ([∪∩−]) B\.",
                                 body)
            symbol = match.group(3) if match else None
        assert match is not None, body
        values_a, values_b = set_oracle.parse_set(match.group(1)), set_oracle.parse_set(match.group(2))
        if symbol == "∪":
            result = values_a | values_b
        elif symbol == "∩":
            result = values_a & values_b
        elif symbol == "−":
            result = values_a - values_b
        else:
            result = values_a ^ values_b
        return {"variant": variant, "A": values_a, "B": values_b,
                "result": result, "answer": roster_text(result), "query": query}
    if variant == "power_set":
        match = re.fullmatch(r"S = (.+)\.", body)
        assert match is not None, body
        values = tuple(set_oracle.parse_roster(match.group(1)))
        result = power_text(values)
        return {"variant": variant, "S": values,
                "answer": f"P(S) = {result}", "query": query}
    if variant == "cartesian_product":
        match = re.fullmatch(r"A = (.+)\. B = (.+)\.", body)
        assert match is not None, body
        values_a = tuple(set_oracle.parse_roster(match.group(1)))
        values_b = tuple(set_oracle.parse_roster(match.group(2)))
        result = pair_roster(values_a, values_b)
        return {"variant": variant, "A": values_a, "B": values_b,
                "answer": f"A × B = {result}", "query": query}
    if variant == "complement":
        match = re.fullmatch(r"U = (.+)\. A = (.+)\.", body)
        assert match is not None, body
        universe, values_a = set_oracle.parse_set(match.group(1)), set_oracle.parse_set(match.group(2))
        result = universe - values_a
        return {"variant": variant, "U": universe, "A": values_a,
                "result": result, "answer": roster_text(result), "query": query}

    match = re.fullmatch(r"A = (.+)\. B = (.+)\. C = (.+)\. Expression: (.+)\.", body)
    assert match is not None, body
    values_a, values_b, values_c = (set_oracle.parse_set(match.group(index))
                                    for index in (1, 2, 3))
    expression = match.group(4)
    if expression == "(A ∪ B) − C":
        inner, result = values_a | values_b, (values_a | values_b) - values_c
    elif expression == "(A ∩ B) ∪ C":
        inner, result = values_a & values_b, (values_a & values_b) | values_c
    elif expression == "A Δ (B − C)":
        inner, result = values_b - values_c, values_a ^ (values_b - values_c)
    else:
        assert expression == "(A − B) ∩ C"
        inner, result = values_a - values_b, (values_a - values_b) & values_c
    return {"variant": variant, "A": values_a, "B": values_b, "C": values_c,
            "expression": expression, "inner": inner, "result": result,
            "answer": roster_text(result), "query": query}


class SetOperationsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_output_contract(self):
        example = SetOperationsGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SetOperationsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_step_arithmetic_and_intermediate_sets(self):
        generator = SetOperationsGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            subexpressions = []
            cart_pairs = 0
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]), int(fields[3]))
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]), int(fields[3]))
                elif fields[0] == "COUNT" and "result" in parts:
                    self.assertEqual(fields[2], str(len(parts["result"])))
                elif fields[0] == "SUBEXPR":
                    subexpressions.append(fields[2])
                elif fields[0] == "CART_PAIR":
                    self.assertEqual(fields[3], f"({fields[1]}, {fields[2]})")
                    cart_pairs += 1
            if parts["variant"] == "two_step":
                self.assertEqual(subexpressions,
                                 [roster_text(parts["inner"]), roster_text(parts["result"])])
            if parts["variant"] == "cartesian_product":
                self.assertEqual(cart_pairs, len(parts["A"]) * len(parts["B"]))

    def test_all_seven_variants_and_five_phrasings_are_reachable(self):
        for variant in SetOperationsGenerator.VARIANTS:
            generator = SetOperationsGenerator(variant)
            seen = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"set_operations_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SetOperationsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SetOperationsGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

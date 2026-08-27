"""Independent A9 checks for OperationPropertiesGenerator."""
import random
import re
import unittest

from generators.operation_properties_generator import (
    OperationPropertiesGenerator,
    PROPERTY_NAMES,
    QUERIES,
)
from helpers import DELIM


def split_query(problem, variant):
    for query in QUERIES[variant]:
        if problem.endswith(f" {query}"):
            return problem[:-(len(query) + 1)], query
    raise AssertionError(problem)


def analyze_left(left):
    match = re.fullmatch(r"(\d+) \+ 0", left)
    if match:
        value = int(match.group(1))
        return "identity_add", str(value), value
    match = re.fullmatch(r"(\d+) \+ (\d+)", left)
    if match:
        a, b = map(int, match.groups())
        return "commutative_add", f"{b} + {a}", a + b
    match = re.fullmatch(r"\((\d+) \+ (\d+)\) \+ (\d+)", left)
    if match:
        a, b, c = map(int, match.groups())
        return "associative_add", f"{a} + ({b} + {c})", a + b + c
    match = re.fullmatch(r"(\d+) × \((\d+) \+ (\d+)\)", left)
    if match:
        a, b, c = map(int, match.groups())
        return "distributive", f"{a} × {b} + {a} × {c}", a * (b + c)
    match = re.fullmatch(r"(\d+) × 1", left)
    assert match is not None, left
    value = int(match.group(1))
    return "identity_multiply", str(value), value


def oracle_parts(example):
    problem = example["problem"]
    if problem.startswith("Equality: "):
        body, query = split_query(problem, "identify")
        equality = body[len("Equality: "):-1]
        left, right = equality.split(" = ", 1)
        kind, expected_right, value = analyze_left(left)
        assert right == expected_right, equality
        property_name = PROPERTY_NAMES[kind]
        answer = f"{property_name}; both sides = {value}"
        return {"variant": "identify", "left": left, "right": right,
                "property": property_name, "value": value, "answer": answer,
                "query": query}
    if problem.startswith("Expression: "):
        body, query = split_query(problem, "apply")
        match = re.fullmatch(r"Expression: (.+)\. Requested property: (.+)\.", body)
        assert match is not None, body
        left, stated_property = match.groups()
        kind, right, value = analyze_left(left)
        property_name = PROPERTY_NAMES[kind]
        assert stated_property == property_name
        answer = (f"rewritten: {right}; value = {value}; "
                  f"property = {property_name}")
        return {"variant": "apply", "left": left, "right": right,
                "property": property_name, "value": value, "answer": answer,
                "query": query}

    body, query = split_query(problem, "equality_chain")
    match = re.fullmatch(r"Facts: (.+)\. Find ([a-z])\.", body)
    assert match is not None, body
    facts = match.group(1).split("; ")
    first = match.group(2)
    links = [fact.split(" = ") for fact in facts]
    assert links[0][0] == first
    for current, following in zip(links, links[1:]):
        assert current[1] == following[0]
    value = int(links[-1][1])
    answer = f"{first} = {value}; transitive property of equality"
    return {"variant": "equality_chain", "facts": facts, "first": first,
            "value": value, "answer": answer, "query": query}


class OperationPropertiesGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(173867)

    def test_output_contract(self):
        example = OperationPropertiesGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = OperationPropertiesGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_arithmetic_property_and_rewrite_steps(self):
        generator = OperationPropertiesGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            saw_property = False
            rewrites = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "PROPERTY_MATCH":
                    if parts["variant"] == "equality_chain":
                        self.assertEqual(fields[1],
                                         "transitive property of equality")
                    else:
                        self.assertEqual(fields[1], parts["property"])
                    saw_property = True
                elif fields[0] == "REWRITE":
                    rewrites.append(fields[1:])
            self.assertTrue(saw_property)
            if parts["variant"] == "apply":
                self.assertIn([parts["left"], parts["right"]], rewrites)
            elif parts["variant"] == "equality_chain":
                self.assertEqual(rewrites[-1],
                                 [f"{parts['first']} = {parts['value']}"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in OperationPropertiesGenerator.VARIANTS:
            generator = OperationPropertiesGenerator(variant)
            seen = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"operation_properties_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            OperationPropertiesGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = OperationPropertiesGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            # ``+ 0`` and ``× 1`` are intentional identity-property cases.
            self.assertNotRegex(example["problem"], r"1x|\^1|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

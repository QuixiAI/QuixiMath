"""Independent A9 checks for AttributeSortingGenerator."""
import random
import re
import unittest

from generators.attribute_sorting_generator import (
    AttributeSortingGenerator,
    QUERY_TEMPLATES,
)
from helpers import DELIM


def parse_problem(problem):
    match = re.fullmatch(
        r"Numbers: \[([0-9, ]+)\]\. Attributes: (.+?)\. (.+)", problem
    )
    assert match is not None, problem
    numbers = [int(part) for part in match.group(1).split(", ")]
    attributes = []
    for part in match.group(2).split("; "):
        attr_match = re.fullmatch(r"([ABC]) = (.+)", part)
        assert attr_match is not None, part
        attributes.append((attr_match.group(1), attr_match.group(2)))
    return numbers, attributes, match.group(3)


def evaluate_attribute(value, description):
    if description == "even":
        return value % 2 == 0
    if description == "odd":
        return value % 2 == 1
    if description == "one-digit":
        return value < 10
    match = re.fullmatch(r"multiple of (\d+)", description)
    if match:
        return value % int(match.group(1)) == 0
    match = re.fullmatch(r"greater than (\d+)", description)
    if match:
        return value > int(match.group(1))
    match = re.fullmatch(r"less than (\d+)", description)
    if match:
        return value < int(match.group(1))
    raise AssertionError(f"unknown attribute: {description}")


def fmt_roster(values):
    return "{" + ", ".join(map(str, values)) + "}" if values else "∅"


def oracle_parts(example):
    numbers, attributes, query = parse_problem(example["problem"])
    masks = {
        number: tuple(evaluate_attribute(number, description)
                      for _, description in attributes)
        for number in numbers
    }
    if len(attributes) == 3:
        variant = "three_attributes"
        layout = (
            ((True, True, True), "all three"),
            ((True, True, False), "A and B only"),
            ((True, False, True), "A and C only"),
            ((False, True, True), "B and C only"),
            ((True, False, False), "A only"),
            ((False, True, False), "B only"),
            ((False, False, True), "C only"),
            ((False, False, False), "none"),
        )
    elif query.endswith("Report only the neither region and its count."):
        variant = "neither_region"
        layout = (((False, False), "neither"),)
    else:
        variant = "two_attributes"
        layout = (
            ((True, True), "both"),
            ((True, False), "only A"),
            ((False, True), "only B"),
            ((False, False), "neither"),
        )
    rows = [(label, [number for number in numbers if masks[number] == mask])
            for mask, label in layout]
    if variant == "neither_region":
        values = rows[0][1]
        answer = f"neither: {fmt_roster(values)}; count = {len(values)}"
    else:
        answer = "; ".join(f"{label}: {fmt_roster(values)}"
                           for label, values in rows)
    return {
        "numbers": numbers,
        "attributes": attributes,
        "masks": masks,
        "variant": variant,
        "rows": rows,
        "answer": answer,
        "query": query,
    }


class AttributeSortingGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(104729)

    def test_output_contract(self):
        example = AttributeSortingGenerator().generate()
        self.assertEqual(
            set(("problem_id", "operation", "problem", "steps", "final_answer"))
            - set(example),
            set(),
        )
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = AttributeSortingGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_emitted_checks_and_regions_are_arithmetically_correct(self):
        generator = AttributeSortingGenerator()
        for _ in range(200):
            example = generator.generate()
            parts = oracle_parts(example)
            expected_checks = [
                (str(number), f"{label}: {description}",
                 "yes" if evaluate_attribute(number, description) else "no")
                for number in parts["numbers"]
                for label, description in parts["attributes"]
            ]
            seen_checks = []
            seen_regions = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "ATTR_CHECK":
                    seen_checks.append(tuple(fields[1:]))
                elif fields[0] == "REGION":
                    seen_regions.append(tuple(fields[1:]))
                elif fields[0] == "COUNT":
                    self.assertEqual(parts["variant"], "neither_region")
                    self.assertEqual(fields[1:], ["neither",
                                                  str(len(parts["rows"][0][1]))])
            self.assertEqual(seen_checks, expected_checks)
            self.assertEqual(
                seen_regions,
                [(label, fmt_roster(values)) for label, values in parts["rows"]],
            )

    def test_all_variants_and_phrasings_are_reachable(self):
        for variant in AttributeSortingGenerator.VARIANTS:
            seen_queries = set()
            generator = AttributeSortingGenerator(variant)
            for _ in range(500):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"attribute_sorting_{variant}")
                query = parts["query"].removesuffix(
                    " Report only the neither region and its count."
                )
                seen_queries.add(query)
            self.assertEqual(seen_queries, set(QUERY_TEMPLATES))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            AttributeSortingGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = AttributeSortingGenerator()
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

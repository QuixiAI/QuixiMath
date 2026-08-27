"""Independent finite-table oracle for FunctionPropertiesGenerator."""
import itertools
import math
import random
import re
import unittest

from generators.function_properties_generator import QUERIES, FunctionPropertiesGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_element(text):
    values = oracle.parse_set("{" + text + "}")
    assert len(values) == 1
    return next(iter(values))


def parse_map(text):
    table = {}
    for entry in text.split(", "):
        left, right = entry.split("→")
        table[parse_element(left)] = parse_element(right)
    return table


def map_text(table):
    return ", ".join(
        f"{oracle.element_text(key)}→{oracle.element_text(table[key])}"
        for key in sorted(table, key=oracle.element_key)
    )


def classify_answer(table, codomain):
    collision, missed = oracle.brute_function_properties(table, codomain)
    if collision is None:
        injective = "injective yes"
    else:
        first, second, value = collision
        injective = (f"injective no (f({first}) = f({second}) = {value})")
    surjective = ("surjective yes" if missed is None else
                  f"surjective no (misses {missed})")
    bijective = collision is None and missed is None
    return f"{injective}; {surjective}; bijective {'yes' if bijective else 'no'}"


def count_maps(domain, codomain, prop):
    m, n = len(domain), len(codomain)
    if prop == "injective":
        return math.factorial(n) // math.factorial(n - m)
    if prop == "bijective":
        return math.factorial(m)
    return sum(((-1) ** index) * math.comb(n, index)
               * (n - index) ** m for index in range(n + 1))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "compose_tables":
        match = re.fullmatch(
            r"A = (.+)\. B = (.+)\. C = (.+)\. Table f: (.+)\. Table g: (.+)\.",
            body,
        )
        assert match is not None, body
        set_a, set_b, set_c = (oracle.parse_set(match.group(index))
                               for index in (1, 2, 3))
        first, second = parse_map(match.group(4)), parse_map(match.group(5))
        composed = {key: second[first[key]] for key in set_a}
        answer = f"g ∘ f = {map_text(composed)}"
        return {"variant": variant, "query": query, "A": set_a, "B": set_b,
                "C": set_c, "f": first, "g": second, "result": composed,
                "answer": answer}
    if variant == "fixed_points":
        match = re.fullmatch(r"A = (.+)\. Table f: (.+)\.", body)
        assert match is not None, body
        set_a, table = oracle.parse_set(match.group(1)), parse_map(match.group(2))
        fixed = frozenset(key for key in set_a if table[key] == key)
        return {"variant": variant, "query": query, "A": set_a, "f": table,
                "result": fixed, "answer": oracle.roster_text(fixed)}
    if variant == "count_by_property":
        match = re.fullmatch(r"A = (.+)\. B = (.+)\. Property: (\w+)\.", body)
        assert match is not None, body
        set_a, set_b = oracle.parse_set(match.group(1)), oracle.parse_set(match.group(2))
        prop = match.group(3)
        answer = count_maps(set_a, set_b, prop)
        return {"variant": variant, "query": query, "A": set_a, "B": set_b,
                "property": prop, "answer": str(answer)}
    if variant == "image_preimage":
        match = re.fullmatch(
            r"A = (.+)\. B = (.+)\. Table f: (.+)\. S = (.+)\. T = (.+)\.",
            body,
        )
        assert match is not None, body
        set_a, set_b = oracle.parse_set(match.group(1)), oracle.parse_set(match.group(2))
        table = parse_map(match.group(3))
        subset_s, subset_t = oracle.parse_set(match.group(4)), oracle.parse_set(match.group(5))
        forward = frozenset(table[key] for key in subset_s)
        backward = frozenset(key for key in set_a if table[key] in subset_t)
        answer = (f"f(S) = {oracle.roster_text(forward)}; "
                  f"f⁻¹(T) = {oracle.roster_text(backward)}")
        return {"variant": variant, "query": query, "A": set_a, "B": set_b,
                "f": table, "S": subset_s, "T": subset_t,
                "forward": forward, "backward": backward, "answer": answer}
    match = re.fullmatch(r"A = (.+)\. B = (.+)\. Table f: (.+)\.", body)
    assert match is not None, body
    set_a, set_b = oracle.parse_set(match.group(1)), oracle.parse_set(match.group(2))
    table = parse_map(match.group(3))
    if variant == "classify":
        answer = classify_answer(table, set_b)
        result = None
    else:
        assert variant == "inverse_table"
        result = {value: key for key, value in table.items()}
        answer = f"f⁻¹ = {map_text(result)}"
    return {"variant": variant, "query": query, "A": set_a, "B": set_b,
            "f": table, "result": result, "answer": answer}


class FunctionPropertiesGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(316927)

    def test_output_contract(self):
        example = FunctionPropertiesGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = FunctionPropertiesGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_table_steps_and_variant_derivations(self):
        generator = FunctionPropertiesGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [item.split(DELIM) for item in example["steps"]]
            maps = [item for item in steps if item[0] == "MAP"]
            expected_map_count = len(parts.get("f", {})) + len(parts.get("g", {}))
            if expected_map_count:
                self.assertEqual(len(maps), expected_map_count)
            if parts["variant"] == "classify":
                collision, missed = oracle.brute_function_properties(
                    parts["f"], parts["B"])
                self.assertEqual(any(item[0] == "COLLISION" for item in steps),
                                 collision is not None)
                self.assertEqual(any(item[0] == "MISSED" for item in steps),
                                 missed is not None)
            elif parts["variant"] == "image_preimage":
                image_values = {parse_element(item[2]) for item in steps
                                if item[0] == "IMAGE"}
                self.assertEqual(image_values, parts["forward"])
                preimage_union = set()
                for item in steps:
                    if item[0] == "PREIMAGE":
                        preimage_union.update(oracle.parse_set(item[2]))
                self.assertEqual(preimage_union, set(parts["backward"]))
            elif parts["variant"] == "compose_tables":
                compose = [item for item in steps if item[0] == "COMPOSE"]
                self.assertEqual(len(compose), len(parts["A"]))
            elif parts["variant"] == "inverse_table":
                inverse_pairs = [item for item in steps if item[0] == "INVERSE_PAIR"]
                self.assertEqual(len(inverse_pairs), len(parts["A"]))
            elif parts["variant"] == "fixed_points":
                checks = [item for item in steps if item[0] == "FIXED_CHECK"]
                self.assertEqual(len(checks), len(parts["A"]))

    def test_count_arithmetic_and_small_brute_force(self):
        generator = FunctionPropertiesGenerator("count_by_property")
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            running = None
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "RUNNING_TOTAL":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                    running = int(fields[3])
            if parts["property"] == "surjective":
                self.assertEqual(running, int(parts["answer"]))
        for domain_size in range(1, 4):
            for codomain_size in range(1, 4):
                functions = itertools.product(range(codomain_size),
                                              repeat=domain_size)
                onto = sum(set(outputs) == set(range(codomain_size))
                           for outputs in functions)
                expected = count_maps(range(domain_size), range(codomain_size),
                                      "surjective")
                self.assertEqual(onto, expected)

    def test_all_variants_phrasings_and_classification_outcomes(self):
        for variant in FunctionPropertiesGenerator.VARIANTS:
            generator = FunctionPropertiesGenerator(variant)
            seen_queries = set()
            answers = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"function_properties_{variant}")
                seen_queries.add(parts["query"])
                answers.add(parts["answer"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))
            if variant == "classify":
                self.assertTrue(any("bijective yes" in answer for answer in answers))
                self.assertTrue(any("injective no" in answer for answer in answers))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FunctionPropertiesGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = FunctionPropertiesGenerator()
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

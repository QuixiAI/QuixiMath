"""Independent finite-model oracle for QuantifierFiniteDomainGenerator."""
import itertools
import random
import re
import unittest

from generators.quantifier_finite_domain_generator import (
    QUERIES, QuantifierFiniteDomainGenerator,
)
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_two_formula(text):
    match = re.fullmatch(r"∀x ∃y \((.+)\)", text)
    if match:
        return "forall_exists", None, match.group(1)
    match = re.fullmatch(r"∃x ∀y \((.+)\)", text)
    if match:
        return "exists_forall", None, match.group(1)
    match = re.fullmatch(r"∀x \((.+) → ∃y \((.+)\)\)", text)
    assert match is not None, text
    return "restricted_forall", match.group(1), match.group(2)


def restriction_function(text):
    if text is None:
        return None
    if text == "Even(x)":
        return lambda value: value % 2 == 0
    if text == "Odd(x)":
        return lambda value: value % 2 == 1
    match = re.fullmatch(r"x ≥ (\d+)", text)
    assert match is not None, text
    cutoff = int(match.group(1))
    return lambda value: value >= cutoff


def solve_two(domain, prefix, predicate, restriction=None):
    if prefix == "forall_exists":
        witnesses = []
        for first in domain:
            witness = next((second for second in domain
                            if predicate(first, second)), None)
            if witness is None:
                return f"false; counterexample x = {first}"
            witnesses.append(witness)
        return "true; witnesses y = " + ", ".join(map(str, witnesses))
    if prefix == "exists_forall":
        witness = next((first for first in domain
                        if all(predicate(first, second) for second in domain)),
                       None)
        return (f"true; witness x = {witness}" if witness is not None
                else "false; no x works")
    witnesses = []
    for first in domain:
        if not restriction(first):
            continue
        witness = next((second for second in domain
                        if predicate(first, second)), None)
        if witness is None:
            return f"false; counterexample x = {first}"
        witnesses.append((first, witness))
    pairs = ", ".join(f"{first}→{second}" for first, second in witnesses)
    return f"true; witnesses x→y = {pairs}" if pairs else "true; no P-cases"


def arithmetic_predicate(text):
    if text == "x < y":
        return lambda first, second: first < second
    if text == "x ∣ y":
        return lambda first, second: second % first == 0
    if text == "x² > y":
        return lambda first, second: first * first > second
    match = re.fullmatch(r"x \+ y = (\d+)", text)
    assert match is not None, text
    target = int(match.group(1))
    return lambda first, second: first + second == target


def function_predicate(text, mapping):
    if text == "f(x) = y":
        return lambda first, second: mapping[first] == second
    if text == "f(y) = x":
        return lambda first, second: mapping[second] == first
    assert text == "f(y) ≠ x", text
    return lambda first, second: mapping[second] != first


def nested_result(domain, relation, prefix_text, matrix_text):
    if matrix_text == "(R(x, y) ∧ R(y, z)) → R(x, z)":
        matrix = lambda x, y, z: not (
            (x, y) in relation and (y, z) in relation) or (x, z) in relation
    elif matrix_text == "R(x, y) ∧ R(y, z)":
        matrix = lambda x, y, z: ((x, y) in relation and (y, z) in relation)
    elif matrix_text == "R(x, z) ∨ R(z, y)":
        matrix = lambda x, y, z: ((x, z) in relation or (z, y) in relation)
    else:
        assert matrix_text == "R(x, z) ∧ R(y, z)", matrix_text
        matrix = lambda x, y, z: ((x, z) in relation and (y, z) in relation)
    prefix = [("forall" if symbol == "∀" else "exists", variable)
              for symbol, variable in re.findall(r"([∀∃])(\w)", prefix_text)]

    def quantify(index, environment):
        if index == len(prefix):
            return matrix(environment["x"], environment["y"], environment["z"])
        kind, variable = prefix[index]
        values = []
        for value in domain:
            extended = dict(environment)
            extended[variable] = value
            values.append(quantify(index + 1, extended))
        return all(values) if kind == "forall" else any(values)

    column = "".join("T" if matrix(*values) else "F"
                     for values in itertools.product(domain, repeat=3))
    result = quantify(0, {})
    return f"{'true' if result else 'false'}; atomic column = {column}", column


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "arithmetic_predicate":
        match = re.fullmatch(r"Domain D = (.+)\. Formula: (.+)\.", body)
        assert match is not None, body
        domain = tuple(oracle.parse_roster(match.group(1)))
        prefix, restriction, condition = parse_two_formula(match.group(2))
        predicate = arithmetic_predicate(condition)
        answer = solve_two(domain, prefix, predicate,
                           restriction_function(restriction))
        relation = mapping = column = None
    elif variant == "relation_table":
        match = re.fullmatch(
            r"Domain D = (.+)\. R = (.+)\. Formula: (.+)\.", body)
        assert match is not None, body
        domain = tuple(oracle.parse_roster(match.group(1)))
        relation = frozenset(oracle.parse_pair_roster(match.group(2)))
        prefix, restriction, condition = parse_two_formula(match.group(3))
        assert condition == "R(x, y)", condition
        predicate = lambda first, second: (first, second) in relation
        answer = solve_two(domain, prefix, predicate,
                           restriction_function(restriction))
        mapping = column = None
    elif variant == "function_table":
        match = re.fullmatch(
            r"Domain D = (.+)\. Function table: (.+)\. Formula: (.+)\.", body)
        assert match is not None, body
        domain = tuple(oracle.parse_roster(match.group(1)))
        entries = re.findall(r"f\((\d+)\)=(\d+)", match.group(2))
        mapping = {int(first): int(second) for first, second in entries}
        assert set(mapping) == set(domain)
        prefix, restriction, condition = parse_two_formula(match.group(3))
        assert restriction is None
        predicate = function_predicate(condition, mapping)
        answer = solve_two(domain, prefix, predicate)
        relation = column = None
    else:
        match = re.fullmatch(
            r"Domain D = (.+)\. R = (.+)\. Formula: "
            r"((?:[∀∃]\w )+)\((.+)\)\. Triple order: x, then y, then z\.",
            body)
        assert match is not None, body
        domain = tuple(oracle.parse_roster(match.group(1)))
        relation = frozenset(oracle.parse_pair_roster(match.group(2)))
        prefix, condition = match.group(3).strip(), match.group(4)
        answer, column = nested_result(domain, relation, prefix, condition)
        mapping = predicate = restriction = None
    return {"variant": variant, "query": query, "domain": domain,
            "relation": relation, "mapping": mapping, "predicate": predicate,
            "restriction": restriction, "column": column, "answer": answer}


class QuantifierFiniteDomainGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(872311)

    def test_output_contract(self):
        example = QuantifierFiniteDomainGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = QuantifierFiniteDomainGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_emitted_witnesses_and_counterexamples_obey_model(self):
        generator = QuantifierFiniteDomainGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            if parts["variant"] == "nested_three":
                emitted = "".join(
                    fields[2].split("=")[1]
                    for fields in (raw.split(DELIM) for raw in example["steps"])
                    if fields[0] == "QUANT_CASE")
                self.assertEqual(emitted, parts["column"])
                continue
            domain, predicate = parts["domain"], parts["predicate"]
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "WITNESS" and fields[1].startswith("x="):
                    first = int(fields[1].split("=")[1])
                    if fields[2].startswith("y="):
                        second = int(fields[2].split("=")[1])
                        expected = next(value for value in domain
                                        if predicate(first, value))
                        self.assertEqual(second, expected)
                    else:
                        self.assertTrue(all(predicate(first, second)
                                            for second in domain))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in QuantifierFiniteDomainGenerator.VARIANTS:
            generator = QuantifierFiniteDomainGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"quantifier_finite_domain_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            QuantifierFiniteDomainGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = QuantifierFiniteDomainGenerator()
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

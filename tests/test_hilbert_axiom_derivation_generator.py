"""Independent schema matcher for HilbertAxiomDerivationGenerator."""
import random
import re
import unittest

from generators.hilbert_axiom_derivation_generator import (
    HilbertAxiomDerivationGenerator, QUERIES,
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


def ast_match(schema, formula, bindings=None):
    bindings = {} if bindings is None else dict(bindings)
    if schema[0] == "var" and schema[1] in ("p", "q", "r"):
        old = bindings.get(schema[1])
        if old is not None and old != formula:
            return None
        bindings[schema[1]] = formula
        return bindings
    if schema[0] != formula[0]:
        return None
    if schema[0] in ("var", "const"):
        return bindings if schema == formula else None
    if schema[0] == "not":
        return ast_match(schema[1], formula[1], bindings)
    bindings = ast_match(schema[1], formula[1], bindings)
    return None if bindings is None else ast_match(
        schema[2], formula[2], bindings)


def ast_substitute(node, mapping):
    if node[0] == "var":
        return mapping.get(node[1], node)
    if node[0] == "const":
        return node
    if node[0] == "not":
        return ("not", ast_substitute(node[1], mapping))
    return (node[0], ast_substitute(node[1], mapping),
            ast_substitute(node[2], mapping))


def parse_mapping(text):
    mapping = {}
    for item in text.split("; "):
        name, formula = item.split(" := ", 1)
        mapping[name] = oracle.parse_formula(formula)
    return mapping


def binding_formula_text(node):
    text = oracle.render(node)
    return f"({text})" if node[0] not in ("var", "const", "not") else text


def binding_text(mapping):
    return ", ".join(
        f"{name} := {binding_formula_text(mapping[name])}"
        for name in ("p", "q", "r") if name in mapping)


def parse_schema_table(text):
    table = []
    for item in text.split("; "):
        label, formula = item.split(" = ", 1)
        table.append((label, oracle.parse_formula(formula)))
    return table


def identify(table, candidate):
    matches = []
    for label, schema in table:
        mapping = ast_match(schema, candidate)
        if mapping is not None:
            matches.append((label, mapping))
    assert len(matches) == 1, matches
    return matches[0]


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("pm_axioms", "lukasiewicz_axioms"):
        system = "PM" if variant == "pm_axioms" else "Łukasiewicz"
        convention = (r"PM convention: A → B abbreviates ¬A ∨ B\. "
                      if variant == "pm_axioms" else "")
        match = re.fullmatch(
            rf"Named {system} axiom: (.+) = (.+)\. {convention}"
            rf"Substitution: (.+)\.",
            body)
        assert match is not None, body
        schema = oracle.parse_formula(match.group(2))
        mapping = parse_mapping(match.group(3))
        answer = oracle.render(ast_substitute(schema, mapping))
        details = {"mapping": mapping, "schema": schema}
    elif variant == "instance_identify":
        match = re.fullmatch(
            r"Axiom system: (PM|Lukasiewicz)\. "
            r"(?:PM convention: A → B abbreviates ¬A ∨ B\. )?"
            r"Schemas: (.+)\. "
            r"Candidate formula: (.+)\.", body)
        assert match is not None, body
        table = parse_schema_table(match.group(2))
        candidate = oracle.parse_formula(match.group(3))
        label, mapping = identify(table, candidate)
        answer = f"{label} [{binding_text(mapping)}]"
        details = {"mapping": mapping, "schema": dict(table)[label]}
    elif variant == "substitute":
        match = re.fullmatch(
            r"Formula schema: (.+)\. Uniform substitution: (.+)\.", body)
        assert match is not None, body
        schema = oracle.parse_formula(match.group(1))
        mapping = parse_mapping(match.group(2))
        answer = oracle.render(ast_substitute(schema, mapping))
        details = {"mapping": mapping, "schema": schema}
    else:
        match = re.fullmatch(
            r"Lukasiewicz schema: L1 = (.+)\. Lines marked axiom are L1 "
            r"instances; lines marked derived use modus ponens from the "
            r"unique earlier pair\. Derivation: (.+)\.", body)
        assert match is not None, body
        schema = oracle.parse_formula(match.group(1))
        lines = []
        answers = []
        for item in match.group(2).split("; "):
            line = re.fullmatch(r"(\d+)\. (.+) \[(axiom|derived) ____\]", item)
            assert line is not None, item
            number, formula, kind = int(line.group(1)), oracle.parse_formula(line.group(2)), line.group(3)
            assert number == len(lines) + 1
            if kind == "axiom":
                mapping = ast_match(schema, formula)
                assert mapping is not None
                justification = f"L1 [{binding_text(mapping)}]"
            else:
                pairs = []
                for antecedent_index, antecedent in enumerate(lines, 1):
                    for implication_index, implication in enumerate(lines, 1):
                        if (implication[0] == "imp" and
                                implication[1] == antecedent and
                                implication[2] == formula):
                            pairs.append((antecedent_index, implication_index))
                assert pairs, (number, formula)
                antecedent_index, implication_index = pairs[-1]
                justification = f"MP {antecedent_index},{implication_index}"
            lines.append(formula)
            answers.append(f"{number}: {justification}")
        answer = "; ".join(answers)
        details = {"lines": lines, "schema": schema}
    return {"variant": variant, "query": query, "answer": answer,
            "details": details}


class HilbertAxiomDerivationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(173205)

    def test_output_contract(self):
        example = HilbertAxiomDerivationGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = HilbertAxiomDerivationGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_every_substitute_step_is_exact(self):
        generator = HilbertAxiomDerivationGenerator()
        for _ in range(300):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] != "SUBSTITUTE" or fields[1].startswith(("PM ", "L")):
                    continue
                schema = oracle.parse_formula(fields[1])
                mapping = parse_mapping(fields[2])
                self.assertEqual(oracle.render(ast_substitute(schema, mapping)),
                                 fields[3])

    def test_identification_instances_are_unique(self):
        generator = HilbertAxiomDerivationGenerator("instance_identify")
        for _ in range(200):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in HilbertAxiomDerivationGenerator.VARIANTS:
            generator = HilbertAxiomDerivationGenerator(variant)
            seen_queries = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"hilbert_axiom_derivation_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HilbertAxiomDerivationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = HilbertAxiomDerivationGenerator()
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

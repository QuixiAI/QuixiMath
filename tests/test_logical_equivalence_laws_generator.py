"""Independent problem-text oracle for LogicalEquivalenceLawsGenerator."""
import random
import re
import unittest

from generators.logical_equivalence_laws_generator import (
    QUERIES, LogicalEquivalenceLawsGenerator,
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


def nand_only(node):
    kind = node[0]
    if kind in ("var", "const"):
        return node
    if kind == "not":
        child = nand_only(node[1])
        return ("nand", child, child)
    left, right = nand_only(node[1]), nand_only(node[2])
    if kind == "and":
        joined = ("nand", left, right)
        return ("nand", joined, joined)
    if kind == "or":
        return ("nand", ("nand", left, left), ("nand", right, right))
    if kind == "nand":
        return ("nand", left, right)
    raise AssertionError(node)


def implication_free(node):
    kind = node[0]
    if kind in ("var", "const"):
        return node
    if kind == "not":
        return ("not", implication_free(node[1]))
    left, right = implication_free(node[1]), implication_free(node[2])
    if kind == "imp":
        return ("or", ("not", left), right)
    if kind == "iff":
        return ("and", ("or", ("not", left), right),
                ("or", ("not", right), left))
    return (kind, left, right)


def forced_distribution(source, variant):
    if variant == "to_cnf":
        outer, inner = "or", "and"
    else:
        outer, inner = "and", "or"
    assert source[0] == outer, source
    left, right = source[1], source[2]
    if left[0] == inner:
        return (inner, (outer, left[1], right), (outer, left[2], right))
    assert right[0] == inner, source
    return (inner, (outer, left, right[1]), (outer, left, right[2]))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "simplify":
        match = re.fullmatch(r"Formula: (.+)\. Target family: (.+)\.", body)
        assert match is not None, body
        source = oracle.parse_formula(match.group(1))
        family = [oracle.parse_formula(item)
                  for item in match.group(2).split("; ")]
        names = sorted(set(oracle.formula_variables(source)).union(
            *(set(oracle.formula_variables(item)) for item in family)))
        source_column = oracle.truth_column(source, names)
        matches = [item for item in family
                   if oracle.truth_column(item, names) == source_column]
        assert len(matches) == 1, matches
        target = matches[0]
    else:
        match = re.fullmatch(r"Formula: (.+)\.", body)
        assert match is not None, body
        source = oracle.parse_formula(match.group(1))
        if variant in ("to_cnf", "to_dnf"):
            target = forced_distribution(source, variant)
        elif variant == "nand_only":
            target = nand_only(source)
        else:
            target = implication_free(source)
    return {"variant": variant, "query": query, "source": source,
            "target": target, "answer": oracle.render(target)}


def connective_kinds(node):
    if node[0] in ("var", "const"):
        return set()
    if node[0] == "not":
        return {"not"} | connective_kinds(node[1])
    return ({node[0]} | connective_kinds(node[1])
            | connective_kinds(node[2]))


class LogicalEquivalenceLawsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(772043)

    def test_output_contract(self):
        example = LogicalEquivalenceLawsGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = LogicalEquivalenceLawsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_law_rewrites_and_truth_column_checks(self):
        generator = LogicalEquivalenceLawsGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            law_count = 0
            rewrites = []
            checks = []
            for index, raw_step in enumerate(example["steps"]):
                fields = raw_step.split(DELIM)
                if fields[0] == "LAW":
                    law_count += 1
                    before = oracle.parse_formula(fields[2])
                    after = oracle.parse_formula(fields[3])
                    self.assertTrue(oracle.equivalent(before, after), raw_step)
                    self.assertEqual(example["steps"][index + 1].split(DELIM)[0],
                                     "REWRITE")
                elif fields[0] == "REWRITE":
                    rewritten = oracle.parse_formula(fields[1])
                    self.assertTrue(oracle.equivalent(parts["source"], rewritten),
                                    raw_step)
                    rewrites.append(rewritten)
                elif fields[0] == "CHECK":
                    checks.append(fields)
            self.assertGreater(law_count, 0)
            self.assertEqual(rewrites[-1], parts["target"])
            self.assertEqual(len(checks), 1)
            names = sorted(set(oracle.formula_variables(parts["source"]))
                           | set(oracle.formula_variables(parts["target"])))
            expected = oracle.truth_column(parts["source"], names)
            self.assertEqual(checks[0], ["CHECK", "truth columns", expected,
                                         expected])

    def test_all_variants_phrasings_and_target_shapes(self):
        for variant in LogicalEquivalenceLawsGenerator.VARIANTS:
            generator = LogicalEquivalenceLawsGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"logical_equivalence_laws_{variant}")
                seen_queries.add(parts["query"])
                if variant == "to_cnf":
                    self.assertTrue(oracle.is_cnf(parts["target"]))
                elif variant == "to_dnf":
                    self.assertTrue(oracle.is_dnf(parts["target"]))
                elif variant == "nand_only":
                    self.assertLessEqual(connective_kinds(parts["target"]),
                                         {"nand"})
                elif variant == "implication_free":
                    self.assertTrue(connective_kinds(parts["target"])
                                    <= {"not", "and", "or"})
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_nand_law_steps_use_the_three_exact_identities(self):
        generator = LogicalEquivalenceLawsGenerator("nand_only")
        for _ in range(150):
            example = generator.generate()
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] != "LAW":
                    continue
                before, after = (oracle.parse_formula(fields[2]),
                                 oracle.parse_formula(fields[3]))
                self.assertIn(fields[1], ("Sheffer negation",
                                          "Sheffer conjunction",
                                          "Sheffer disjunction"))
                self.assertEqual(after, nand_only(before))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LogicalEquivalenceLawsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = LogicalEquivalenceLawsGenerator()
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

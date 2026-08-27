"""Independent alpha-renaming, prenex, and finite-model oracle."""
import itertools
import random
import re
import unittest

from generators.prenex_normal_form_generator import (
    QUERIES, PrenexNormalFormGenerator,
)
from helpers import DELIM
from tests.test_quantifier_negation_generator import (
    evaluate, parse_formula, predicate_arities, render,
)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def free_variables(node, bound=frozenset()):
    kind = node[0]
    if kind == "atom":
        return set(node[2]) - set(bound)
    if kind == "not":
        return free_variables(node[1], bound)
    if kind in ("forall", "exists"):
        return free_variables(node[2], bound | {node[1]})
    return free_variables(node[1], bound) | free_variables(node[2], bound)


def all_variables(node):
    kind = node[0]
    if kind == "atom":
        return set(node[2])
    if kind == "not":
        return all_variables(node[1])
    if kind in ("forall", "exists"):
        return {node[1]} | all_variables(node[2])
    return all_variables(node[1]) | all_variables(node[2])


def rename_bound(node, old, new):
    kind = node[0]
    if kind == "atom":
        return ("atom", node[1],
                tuple(new if value == old else value for value in node[2]))
    if kind == "not":
        return ("not", rename_bound(node[1], old, new))
    if kind in ("forall", "exists"):
        if node[1] == old:
            return node
        return (kind, node[1], rename_bound(node[2], old, new))
    return (kind, rename_bound(node[1], old, new),
            rename_bound(node[2], old, new))


def nnf(node, positive=True):
    kind = node[0]
    if kind == "atom":
        return node if positive else ("not", node)
    if kind == "not":
        return nnf(node[1], not positive)
    if kind in ("forall", "exists"):
        output_kind = kind if positive else {
            "forall": "exists", "exists": "forall"}[kind]
        return (output_kind, node[1], nnf(node[2], positive))
    output_kind = kind if positive else {"and": "or", "or": "and"}[kind]
    return (output_kind, nnf(node[1], positive), nnf(node[2], positive))


def standardize(node):
    free = free_variables(node)
    used = set()
    changes = []

    def visit(item):
        kind = item[0]
        if kind == "atom":
            return item
        if kind == "not":
            return ("not", visit(item[1]))
        if kind in ("forall", "exists"):
            variable, body = item[1], item[2]
            if variable in used or variable in free:
                suffix = 1
                fresh = f"{variable}{suffix}"
                unavailable = used | free | free_variables(body)
                while fresh in unavailable:
                    suffix += 1
                    fresh = f"{variable}{suffix}"
                body = rename_bound(body, variable, fresh)
                changes.append((variable, fresh))
                variable = fresh
            used.add(variable)
            return (kind, variable, visit(body))
        return (kind, visit(item[1]), visit(item[2]))

    return visit(node), changes


def prenex(node):
    kind = node[0]
    if kind in ("atom", "not"):
        return [], node
    if kind in ("forall", "exists"):
        prefix, matrix = prenex(node[2])
        return [(kind, node[1])] + prefix, matrix
    left_prefix, left_matrix = prenex(node[1])
    right_prefix, right_matrix = prenex(node[2])
    return left_prefix + right_prefix, (kind, left_matrix, right_matrix)


def wrap(prefix, matrix):
    result = matrix
    for kind, variable in reversed(prefix):
        result = (kind, variable, result)
    return result


def has_quantifier(node):
    kind = node[0]
    if kind in ("forall", "exists"):
        return True
    if kind == "atom":
        return False
    if kind == "not":
        return has_quantifier(node[1])
    return has_quantifier(node[1]) or has_quantifier(node[2])


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"Formula: (.+)\. Policy: (.+)\. Required renaming: (.+)\.", body)
    assert match is not None, body
    source = parse_formula(match.group(1))
    normalized = nnf(source)
    standardized, changes = standardize(normalized)
    stated = [] if match.group(3) == "none" else [
        tuple(item.split("→")) for item in match.group(3).split(", ")]
    assert stated == changes, (stated, changes, body)
    prefix, matrix = prenex(standardized)
    assert not has_quantifier(matrix)
    target = wrap(prefix, matrix)
    return {"variant": variant, "query": query, "policy": match.group(2),
            "source": source, "normalized": normalized,
            "standardized": standardized, "renamings": changes,
            "prefix": prefix, "matrix": matrix, "target": target,
            "answer": render(target)}


def random_model(node, domain):
    model = {}
    for name, arity in predicate_arities(node).items():
        model[name] = {
            values for values in itertools.product(domain, repeat=arity)
            if random.choice((True, False))
        }
    return model


class PrenexNormalFormGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(661409)

    def test_output_contract(self):
        example = PrenexNormalFormGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PrenexNormalFormGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_source_and_prenex_answer_agree_in_random_finite_models(self):
        generator = PrenexNormalFormGenerator()
        for _ in range(250):
            parts = oracle_parts(generator.generate())
            domain = tuple(range(random.randint(2, 3)))
            model = random_model(parts["source"], domain)
            free = free_variables(parts["source"])
            for values in itertools.product(domain, repeat=len(free)):
                environment = dict(zip(sorted(free), values))
                self.assertEqual(
                    evaluate(parts["source"], domain, model, environment),
                    evaluate(parts["target"], domain, model, environment),
                )

    def test_trace_prefix_order_renaming_and_matrix(self):
        generator = PrenexNormalFormGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            fields = [raw.split(DELIM) for raw in example["steps"]]
            pulled = [item[1] for item in fields if item[0] == "PULL"]
            expected = [("∀" if kind == "forall" else "∃") + variable
                        for kind, variable in parts["prefix"]]
            self.assertEqual(pulled, expected)
            renamed = [(item[1][1:], item[2][1:])
                       for item in fields if item[0] == "RENAME"]
            self.assertEqual(renamed, parts["renamings"])
            check = next(item for item in fields if item[0] == "CHECK")
            self.assertEqual(parse_formula(check[2]), parts["matrix"])
            rewrites = [parse_formula(item[1]) for item in fields
                        if item[0] == "REWRITE"]
            self.assertEqual(rewrites[-1], parts["target"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in PrenexNormalFormGenerator.VARIANTS:
            generator = PrenexNormalFormGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"prenex_normal_form_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PrenexNormalFormGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PrenexNormalFormGenerator()
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

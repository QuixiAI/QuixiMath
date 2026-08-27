"""Independent parser, saturation oracle, and brute-force resolution checks."""
import itertools
import random
import re
import unittest

from generators.resolution_proof_generator import QUERIES, ResolutionProofGenerator
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def literal_name(literal):
    return literal[1:] if literal.startswith("¬") else literal


def complement(literal):
    return literal[1:] if literal.startswith("¬") else "¬" + literal


def literal_key(literal):
    return literal_name(literal), literal.startswith("¬")


def parse_clause(text):
    if text == "□":
        return ()
    match = re.fullmatch(r"\((.*)\)", text)
    assert match is not None, text
    return tuple(sorted(set(match.group(1).split(" ∨ ")), key=literal_key))


def clauses_from_problem(problem):
    prefix = problem.split(". Policy:", 1)[0]
    return [parse_clause(raw) for raw in re.findall(r"C\d+=(\([^)]*\)|□)", prefix)]


def resolve(first, second, pivot):
    opposite = complement(pivot)
    values = [item for item in first if item != pivot]
    values += [item for item in second if item != opposite]
    return tuple(sorted(set(values), key=literal_key))


def tautological(clause):
    values = set(clause)
    return any(complement(value) in values for value in values)


def independent_saturation(initial):
    clauses = list(initial)
    actions = []
    while clauses[-1]:
        seen = set(clauses)
        selected = None
        for first_index, first in enumerate(clauses):
            for second_index in range(first_index + 1, len(clauses)):
                second = clauses[second_index]
                for pivot in sorted(first, key=literal_key):
                    if complement(pivot) not in second:
                        continue
                    resolvent = resolve(first, second, pivot)
                    if tautological(resolvent) or resolvent in seen:
                        actions.append(("skip", first_index + 1,
                                        second_index + 1, resolvent))
                        continue
                    selected = (first_index + 1, second_index + 1,
                                pivot, resolvent)
                    break
                if selected:
                    break
            if selected:
                break
        assert selected is not None, clauses
        clauses.append(selected[3])
        actions.append(("derive",) + selected)
    return clauses, actions


def satisfies(clauses, assignment):
    return all(any((not assignment[literal_name(literal)])
                       if literal.startswith("¬")
                       else assignment[literal]
                   for literal in clause)
               for clause in clauses)


def oracle_answer(problem):
    clauses, _ = independent_saturation(clauses_from_problem(problem))
    return f"unsatisfiable; empty clause = C{len(clauses)}"


class TestResolutionProofGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(123947)

    def test_contract_and_500_problem_text_oracles(self):
        generator = ResolutionProofGenerator()
        for _ in range(500):
            result = generator.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             oracle_answer(result["problem"]))

    def test_trace_exactly_follows_canonical_pair_and_pivot_scan(self):
        generator = ResolutionProofGenerator()
        for _ in range(300):
            result = generator.generate()
            clauses, actions = independent_saturation(
                clauses_from_problem(result["problem"]))
            emitted = []
            steps = [raw.split(DELIM) for raw in result["steps"]]
            index = 0
            while index < len(steps):
                fields = steps[index]
                if fields[0] == "RES_SKIP":
                    emitted.append(("skip", int(fields[1][1:]),
                                    int(fields[2][1:]),
                                    parse_clause(fields[3])))
                elif fields[0] == "RESOLVE":
                    derived = steps[index + 1]
                    self.assertEqual(derived[0], "DERIVED")
                    emitted.append(("derive", int(fields[1][1:]),
                                    int(fields[2][1:]), fields[3],
                                    parse_clause(derived[2])))
                    index += 1
                index += 1
            self.assertEqual(emitted, actions)
            empty = next(fields[1] for fields in steps if fields[0] == "RES_EMPTY")
            self.assertEqual(empty, f"C{len(clauses)}")

    def test_random_variant_has_three_to_five_clauses_and_three_or_four_variables(self):
        generator = ResolutionProofGenerator("random_unsatisfiable")
        for _ in range(500):
            result = generator.generate()
            clauses = clauses_from_problem(result["problem"])
            variables = {literal_name(literal)
                         for clause in clauses for literal in clause}
            self.assertIn(len(clauses), (3, 4, 5))
            self.assertIn(len(variables), (3, 4))

    def test_problem_cnf_is_unsatisfiable_by_brute_force(self):
        for _ in range(500):
            result = ResolutionProofGenerator().generate()
            clauses = clauses_from_problem(result["problem"])
            variables = sorted({literal_name(literal)
                                for clause in clauses for literal in clause})
            models = []
            for values in itertools.product((False, True), repeat=len(variables)):
                assignment = dict(zip(variables, values))
                if satisfies(clauses, assignment):
                    models.append(assignment)
            self.assertFalse(models, result["problem"])

    def test_original_named_variants_remain_selectable(self):
        originals = ("unit_refutation", "chain_refutation", "binary_refutation")
        for variant in originals:
            for _ in range(100):
                result = ResolutionProofGenerator(variant).generate()
                self.assertEqual(result["operation"], f"resolution_proof_{variant}")
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result["problem"]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ResolutionProofGenerator.VARIANTS:
            generator = ResolutionProofGenerator(variant)
            seen = set()
            for _ in range(350):
                result = generator.generate()
                self.assertEqual(result["operation"], f"resolution_proof_{variant}")
                query = next(query for query in QUERIES
                             if result["problem"].endswith(query))
                seen.add(query)
            self.assertEqual(seen, set(QUERIES))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            ResolutionProofGenerator("bad")

    def test_pipe_safety_and_render_sanity(self):
        generator = ResolutionProofGenerator()
        for _ in range(250):
            result = generator.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            self.assertNotRegex(result["problem"], r"\b(?:AND|OR|NOT)\b")
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

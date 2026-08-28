"""Independent finite-measure oracle for ProbabilityAxiomsFiniteGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.probability_axioms_finite_generator import (
    ProbabilityAxiomsFiniteGenerator, QUERIES,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_roster(text):
    return tuple() if text == "∅" else tuple(int(item) for item in text[1:-1].split(", "))


def parse_weights(text):
    weights = {}
    missing = None
    for item in text.split("; "):
        match = re.fullmatch(r"P\((-?\d+)\) = (.+)", item)
        atom, value = int(match.group(1)), match.group(2)
        if value == "x":
            missing = atom
        else:
            weights[atom] = Fraction(value)
    return weights, missing


def ptext(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "missing_weight":
        match = re.fullmatch(
            r"Outcomes Ω = (\{[^{}]+\})\. Weights: (.+)\. Event odd = "
            r"(\{[^{}]+\})\.", body)
        assert match is not None, body
        atoms, odd = parse_roster(match.group(1)), parse_roster(match.group(3))
        weights, missing = parse_weights(match.group(2))
        missing_value = 1 - sum(weights.values(), Fraction())
        weights[missing] = missing_value
        event_value = sum((weights[atom] for atom in odd), Fraction())
        answer = f"x = {ptext(missing_value)}; P(odd) = {ptext(event_value)}"
        case = "missing"
    else:
        relation = (r"Weights" if variant != "valid_assignment" else
                    r"Candidate weights")
        match = re.fullmatch(
            rf"Outcomes Ω = (\{{[^{{}}]+\}})\. {relation}: (.+?)\."
            r"(?: Event A = (\{[^{}]+\})\.| Disjoint events: A = "
            r"(\{[^{}]+\}); B = (\{[^{}]+\})\.)?", body)
        assert match is not None, body
        atoms = parse_roster(match.group(1))
        weights, missing = parse_weights(match.group(2))
        assert missing is None and set(atoms) == set(weights)
        total = sum(weights.values(), Fraction())
        if variant == "event_sum":
            event = parse_roster(match.group(3))
            value = sum((weights[atom] for atom in event), Fraction())
            answer, case = f"P(A) = {ptext(value)}", "event"
        elif variant == "valid_assignment":
            answer = ("valid; sum = 1" if total == 1 else
                      f"invalid; sum = {ptext(total)}")
            case = "valid" if total == 1 else "invalid"
        elif variant == "complement_from_weights":
            event = parse_roster(match.group(3))
            value = sum((weight for atom, weight in weights.items()
                         if atom not in event), Fraction())
            answer, case = f"P(Aᶜ) = {ptext(value)}", "complement"
        else:
            first, second = parse_roster(match.group(4)), parse_roster(match.group(5))
            assert set(first).isdisjoint(second)
            value = sum((weights[atom] for atom in first + second), Fraction())
            answer, case = f"P(A ∪ B) = {ptext(value)}", "union"
    return {"variant": variant, "query": query, "answer": answer,
            "case": case}


class ProbabilityAxiomsFiniteGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(223607)

    def test_output_contract(self):
        example = ProbabilityAxiomsFiniteGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ProbabilityAxiomsFiniteGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_valid_and_invalid_assignments_are_reachable(self):
        generator = ProbabilityAxiomsFiniteGenerator("valid_assignment")
        self.assertEqual({oracle_parts(generator.generate())["case"]
                          for _ in range(300)}, {"valid", "invalid"})

    def test_weight_steps_match_problem_assignments(self):
        generator = ProbabilityAxiomsFiniteGenerator()
        for _ in range(300):
            example = generator.generate()
            body, _, _ = split_query(example["problem"])
            shown = dict(re.findall(r"P\((-?\d+)\) = ([^;.]+)", body))
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "WEIGHT":
                    self.assertEqual(fields[2], shown[fields[1]])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ProbabilityAxiomsFiniteGenerator.VARIANTS:
            generator = ProbabilityAxiomsFiniteGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_axioms_finite_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ProbabilityAxiomsFiniteGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ProbabilityAxiomsFiniteGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

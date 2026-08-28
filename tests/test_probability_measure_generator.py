"""Independent set-expression and weight-sum oracle for ProbabilityMeasureGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.probability_measure_generator import QUERIES, ProbabilityMeasureGenerator
from helpers import DELIM
from tests import foundations_oracle as set_oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_problem(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"Ω = (\{[^{}]+\})\. Weights: (.+)\. A = (\{[^{}]*\}|∅)\. "
        r"B = (\{[^{}]*\}|∅)\.(?: C = (\{[^{}]*\}|∅)\.)?"
        r"(?: Expression: (.+)\.)?", body)
    assert match is not None, body
    universe = tuple(set_oracle.parse_set(match.group(1)))
    universe = tuple(sorted(universe))
    weights = {}
    for item in match.group(2).split("; "):
        weight_match = re.fullmatch(r"P\(([a-z])\) = (\d+(?:/\d+)?)", item)
        assert weight_match is not None, item
        weights[weight_match.group(1)] = Fraction(weight_match.group(2))
    assert tuple(weights) == universe
    assert sum(weights.values(), Fraction()) == 1
    env = {"A": set_oracle.parse_set(match.group(3)),
           "B": set_oracle.parse_set(match.group(4))}
    if match.group(5) is not None:
        env["C"] = set_oracle.parse_set(match.group(5))
    return {"variant": variant, "query": query, "universe": universe,
            "weights": weights, "env": env, "expression": match.group(6)}


def measure(parts, members):
    return sum((parts["weights"][atom] for atom in members), Fraction())


def oracle_parts(example):
    parts = parse_problem(example)
    variant, env = parts["variant"], parts["env"]
    if variant == "set_expression":
        node = set_oracle.parse_set_expression(parts["expression"])
        event = set_oracle.eval_set_expression(node, env, parts["universe"])
        answer = ptext(measure(parts, event))
    elif variant == "derive_identity":
        left = measure(parts, env["B"] - env["A"])
        right = measure(parts, env["B"]) - measure(parts, env["A"] & env["B"])
        assert left == right
        answer = (f"P(B − A) = {ptext(left)}; "
                  f"P(B) − P(A ∩ B) = {ptext(right)}")
    elif variant == "monotonicity":
        assert env["A"] < env["B"]
        p_a, p_b = measure(parts, env["A"]), measure(parts, env["B"])
        answer = f"A ⊆ B; P(A) = {ptext(p_a)} ≤ P(B) = {ptext(p_b)}"
    elif variant == "inclusion_exclusion_three":
        answer = ptext(measure(parts, env["A"] | env["B"] | env["C"]))
    elif variant == "union_bound_compare":
        union = measure(parts, env["A"] | env["B"])
        bound = measure(parts, env["A"]) + measure(parts, env["B"])
        assert union <= bound
        answer = f"P(A ∪ B) = {ptext(union)} ≤ P(A) + P(B) = {ptext(bound)}"
    else:
        mass = measure(parts, env["B"])
        values = [(atom, parts["weights"][atom] / mass)
                  for atom in parts["universe"] if atom in env["B"]]
        answer = "; ".join(f"{atom}: {ptext(value)}"
                           for atom, value in values) + "; others 0"
    return {**parts, "answer": answer}


class ProbabilityMeasureGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(282843)

    def test_output_contract(self):
        example = ProbabilityMeasureGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ProbabilityMeasureGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_set_and_measure_steps_match_prompt(self):
        generator = ProbabilityMeasureGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "WEIGHT":
                    self.assertEqual(Fraction(fields[2]), parts["weights"][fields[1]])
                elif fields[0] == "SUBEXPR":
                    node = set_oracle.parse_set_expression(fields[1])
                    result = set_oracle.eval_set_expression(
                        node, parts["env"], parts["universe"])
                    self.assertEqual(fields[2], set_oracle.roster_text(result))
                elif fields[0] == "MEASURE":
                    members = set_oracle.parse_set(fields[2])
                    self.assertEqual(Fraction(fields[3]), measure(parts, members))
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "RENORMALIZE":
                    self.assertEqual(Fraction(fields[3]),
                                     parts["weights"][fields[1]] /
                                     measure(parts, parts["env"]["B"]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ProbabilityMeasureGenerator.VARIANTS:
            generator = ProbabilityMeasureGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_measure_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ProbabilityMeasureGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ProbabilityMeasureGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

"""Problem-text oracle for LikelihoodLanguageGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.likelihood_language_generator import (
    LikelihoodLanguageGenerator, QUERIES,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def probability_text(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def category(value):
    if value == 0:
        return "impossible"
    if value < Fraction(1, 2):
        return "unlikely"
    if value == Fraction(1, 2):
        return "even chance"
    if value < 1:
        return "likely"
    return "certain"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"Experiment: (.+)\. Outcome counts: (.+)\. All individual outcomes "
        r"are equally likely\. Scale: 0 impossible; between 0 and 1/2 "
        r"unlikely; 1/2 even chance; between 1/2 and 1 likely; 1 certain\. "
        r"Focus event(?:s)?: (.+)\.", body)
    assert match is not None, body
    counts = {}
    for item in match.group(2).split("; "):
        label, count = item.split("=")
        counts[label] = int(count)
    total = sum(counts.values())
    focus = match.group(3)
    if variant == "classify":
        label = re.fullmatch(r"outcome ([a-z]+)", focus).group(1)
        value = Fraction(counts[label], total)
        answer = f"{category(value)}; {probability_text(value)}"
        case = category(value)
    elif variant == "compare_two_events":
        left, right = re.fullmatch(
            r"outcome ([a-z]+) and outcome ([a-z]+)", focus).groups()
        first, second = Fraction(counts[left], total), Fraction(counts[right], total)
        if first > second:
            winner, loser, high, low = left, right, first, second
        else:
            winner, loser, high, low = right, left, second, first
        answer = (f"{winner} is more likely than {loser}; "
                  f"{probability_text(high)} > {probability_text(low)}")
        case = "compare"
    elif variant == "order_events":
        labels = re.fullmatch(r"outcomes (.+)", focus).group(1).split(", ")
        answer = ", ".join(sorted(labels, key=lambda label: counts[label]))
        case = "order"
    else:
        if focus == "one of the three listed outcomes":
            answer, case = "certain; 1", "certain"
        else:
            absent = re.fullmatch(r"outcome ([a-z]+)", focus).group(1)
            assert absent not in counts
            answer, case = "impossible; 0", "impossible"
    return {"variant": variant, "query": query, "answer": answer,
            "case": case, "counts": counts, "total": total}


class LikelihoodLanguageGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(707107)

    def test_output_contract(self):
        example = LikelihoodLanguageGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = LikelihoodLanguageGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_sum_and_probability_steps_are_exact(self):
        generator = LikelihoodLanguageGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "SUM":
                    self.assertEqual(sum(map(int, fields[1].split(" + "))),
                                     int(fields[2]))
                elif fields[0] == "PROB_SETUP":
                    value = Fraction(int(fields[1]), int(fields[2]))
                    self.assertGreaterEqual(value, 0)
                    self.assertLessEqual(value, 1)
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
            self.assertEqual(sum(parts["counts"].values()), parts["total"])

    def test_every_likelihood_endpoint_and_interior_case_is_reachable(self):
        classify = LikelihoodLanguageGenerator("classify")
        self.assertEqual({oracle_parts(classify.generate())["case"]
                          for _ in range(300)},
                         {"unlikely", "even chance", "likely"})
        endpoint = LikelihoodLanguageGenerator("certain_impossible")
        self.assertEqual({oracle_parts(endpoint.generate())["case"]
                          for _ in range(200)}, {"certain", "impossible"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in LikelihoodLanguageGenerator.VARIANTS:
            generator = LikelihoodLanguageGenerator(variant)
            seen_queries = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_likelihood_language_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LikelihoodLanguageGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = LikelihoodLanguageGenerator()
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

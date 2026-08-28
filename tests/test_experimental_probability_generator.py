"""Independent frequency oracle for ExperimentalProbabilityGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.experimental_probability_generator import (
    ExperimentalProbabilityGenerator, QUERIES,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ptext(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "relative_frequency":
        match = re.fullmatch(
            r"[A-Z][a-z]+ records spinner tallies: (.+)\. Focus outcome: "
            r"([a-z]+)\.", body)
        assert match is not None, body
        counts = {label: int(count) for label, count in
                  (item.split("=") for item in match.group(1).split("; "))}
        value = Fraction(counts[match.group(2)], sum(counts.values()))
        answer, case = ptext(value), "relative"
    elif variant == "from_sequence":
        match = re.fullmatch(r"Coin trial sequence: ([HT ]+)\. Focus face: ([HT])\.", body)
        assert match is not None, body
        sequence = match.group(1).split()
        value = Fraction(sequence.count(match.group(2)), len(sequence))
        answer, case = ptext(value), "sequence"
    elif variant == "predict_count":
        match = re.fullmatch(
            r"A uniform spinner has (\d+) equal sectors, of which (\d+) "
            r"belongs? to event A\. It will be spun (\d+) times\.", body)
        assert match is not None, body
        sectors, favorable, trials = map(int, match.groups())
        value = Fraction(favorable, sectors)
        predicted = value * trials
        assert predicted.denominator == 1
        answer, case = str(predicted.numerator), "predict"
    else:
        match = re.fullmatch(
            r"A fair (\d+)-sided die was rolled (\d+) times; face (\d+) "
            r"appeared (\d+) times\.", body)
        assert match is not None, body
        sides, trials, _, observed = map(int, match.groups())
        experimental, theoretical = Fraction(observed, trials), Fraction(1, sides)
        relation = ("higher" if experimental > theoretical else
                    "lower" if experimental < theoretical else "equal")
        value = experimental
        answer = (f"experimental {ptext(experimental)}; theoretical "
                  f"{ptext(theoretical)}; experimental is {relation}")
        case = relation
    return {"variant": variant, "query": query, "answer": answer,
            "value": value, "case": case}


class ExperimentalProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(707106)

    def test_output_contract(self):
        example = ExperimentalProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ExperimentalProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = ExperimentalProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "REL_FREQ":
                    self.assertEqual(Fraction(fields[2]), Fraction(fields[3]))

    def test_all_comparison_outcomes_are_reachable(self):
        generator = ExperimentalProbabilityGenerator("compare_theoretical")
        self.assertEqual({oracle_parts(generator.generate())["case"]
                          for _ in range(300)}, {"higher", "lower", "equal"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ExperimentalProbabilityGenerator.VARIANTS:
            generator = ExperimentalProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_experimental_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ExperimentalProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ExperimentalProbabilityGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

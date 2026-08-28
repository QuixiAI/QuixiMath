"""Independent product-count oracle for FundamentalCountingPrincipleGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.fundamental_counting_principle_generator import (
    FundamentalCountingPrincipleGenerator, QUERIES,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_counts(text):
    return {name: int(count) for name, count in
            (item.split("=") for item in text.split("; "))}


def ptext(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "codes":
        match = re.fullmatch(
            r"A (.+) has length (\d+) and an alphabet of (\d+) symbols\. "
            r"Repetition is allowed in the full code space\. Event A is that "
            r"no symbol repeats\.", body)
        assert match is not None, body
        length, alphabet = int(match.group(2)), int(match.group(3))
        total = alphabet ** length
        favorable = math.prod(range(alphabet - length + 1, alphabet + 1))
        answer = (f"{favorable} no-repeat codes; "
                  f"{ptext(Fraction(favorable, total))}")
        details = (total, favorable)
    else:
        match = re.fullmatch(
            r"A (.+) has choice counts: (.+)\. Choose exactly one option "
            r"from each category\.|A (.+) has choice counts: (.+)\. Choose "
            r"one from each\. Event A requires (.+)\.|A (.+) has choice "
            r"counts: (.+)\. Choose one from each\. Restriction: (.+)\.", body)
        assert match is not None, body
        count_text = match.group(2) or match.group(4) or match.group(7)
        counts = parse_counts(count_text)
        total = math.prod(counts.values())
        if variant in ("count_only", "tree_count"):
            favorable = None
            answer = f"{total} selections"
        elif variant == "count_then_probability":
            requirements = match.group(5).split(", ")
            constrained = {item.removesuffix(" option 1") for item in requirements}
            favorable = math.prod(count for name, count in counts.items()
                                     if name not in constrained)
            answer = (f"{total} selections; "
                      f"{ptext(Fraction(favorable, total))}")
        else:
            restriction = re.fullmatch(
                r"(.+) option 1 cannot be paired with (.+) option 1",
                match.group(8))
            first, second = restriction.groups()
            forbidden = math.prod(count for name, count in counts.items()
                                  if name not in (first, second))
            favorable = total - forbidden
            answer = f"{favorable} valid selections"
        details = (total, favorable)
    return {"variant": variant, "query": query, "answer": answer,
            "details": details}


class FundamentalCountingPrincipleGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(141592)

    def test_output_contract(self):
        example = FundamentalCountingPrincipleGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = FundamentalCountingPrincipleGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_running_products_and_fractions_are_exact(self):
        generator = FundamentalCountingPrincipleGenerator()
        for _ in range(300):
            example = generator.generate()
            running = 1
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] in ("FCP", "TREE_LEVEL") and fields[2].isdigit():
                    if fields[1] == "all codes":
                        continue
                    running *= int(fields[2])
                    self.assertEqual(running, int(fields[3]))
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in FundamentalCountingPrincipleGenerator.VARIANTS:
            generator = FundamentalCountingPrincipleGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_fundamental_counting_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FundamentalCountingPrincipleGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = FundamentalCountingPrincipleGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

"""Independent complement oracle for ComplementProbabilityGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.complement_probability_generator import (
    ComplementProbabilityGenerator, QUERIES,
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
    return tuple(int(item) for item in text[1:-1].split(", "))


def ptext(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    body = re.sub(r"^At the [a-z ]+, ", "", body)
    if variant in ("not_event", "complement_of_described"):
        match = re.search(r"S = (\{[^{}]+\}).+ A = (\{[^{}]+\})\.", body)
        assert match is not None, body
        sample, event = map(parse_roster, match.groups())
        value = Fraction(len(sample) - len(event), len(sample))
        answer = ptext(value)
        details = {"event": len(event), "total": len(sample)}
    elif variant == "missing_probability":
        match = re.fullmatch(
            r"a finite model has outcomes (.+)\. Known weights: (.+); "
            r"P\(([a-z]+)\) = x\.", body)
        assert match is not None, body
        known = []
        for item in match.group(2).split("; "):
            weight = re.fullmatch(r"P\([a-z]+\) = (.+)", item)
            known.append(Fraction(weight.group(1)))
        value = 1 - sum(known, Fraction())
        answer, details = ptext(value), {"known": known}
    else:
        match = re.fullmatch(
            r"two independent stages are performed\. Stage 1 succeeds in "
            r"(\d+) of (\d+) equally likely outcomes; stage 2 succeeds in "
            r"(\d+) of (\d+) equally likely outcomes\.", body)
        assert match is not None, body
        a, b, c, d = map(int, match.groups())
        value = 1 - (1 - Fraction(a, b)) * (1 - Fraction(c, d))
        answer, details = ptext(value), {"stage_counts": (a, b, c, d)}
    return {"variant": variant, "query": query, "answer": answer,
            "value": value, "details": details}


class ComplementProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(866025)

    def test_output_contract(self):
        example = ComplementProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ComplementProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = ComplementProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S" and fields[1] == "1":
                    self.assertEqual(Fraction(1) - Fraction(fields[2]),
                                     Fraction(fields[3]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ComplementProbabilityGenerator.VARIANTS:
            generator = ComplementProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_complement_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ComplementProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ComplementProbabilityGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

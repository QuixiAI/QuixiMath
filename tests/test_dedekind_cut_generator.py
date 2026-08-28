"""Independent exact-arithmetic oracle for DedekindCutGenerator."""
from fractions import Fraction
import random
import re
import unittest

from generators.dedekind_cut_generator import DedekindCutGenerator, QUERIES
from helpers import DELIM


def parse_fraction(text):
    text = text.replace("−", "-")
    if "/" in text:
        numerator, denominator = text.split("/")
        return Fraction(int(numerator), int(denominator))
    return Fraction(int(text), 1)


def fraction_text(value):
    value = Fraction(value)
    numerator = str(value.numerator).replace("-", "−")
    return (numerator if value.denominator == 1
            else f"{numerator}/{value.denominator}")


def in_sqrt2_cut(value):
    return value < 0 or value * value < 2


def evidence(value):
    if value < 0:
        return f"{fraction_text(value)} < 0"
    square = value * value
    return f"{fraction_text(square)} {'<' if square < 2 else '>'} 2"


def parse_list(text):
    return [parse_fraction(token) for token in text.split(", ")]


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "membership":
        match = re.fullmatch(
            r"Define L\(√2\) by q ∈ L\(√2\) iff q < 0 or q² < 2\. "
            r"Listed rationals: \[([^]]+)\]\.", body)
        assert match is not None, body
        values = parse_list(match.group(1))
        answer = "; ".join(
            f"{fraction_text(value)} {'∈' if in_sqrt2_cut(value) else '∉'} "
            f"L(√2) ({evidence(value)})" for value in values)
    elif variant == "largest_of_list":
        match = re.fullmatch(
            r"Define L\(√2\) by q ∈ L\(√2\) iff q < 0 or q² < 2\. "
            r"Candidate list: \[([^]]+)\]\.", body)
        assert match is not None, body
        values = parse_list(match.group(1))
        largest = max(value for value in values if in_sqrt2_cut(value))
        answer = (f"largest listed member: {fraction_text(largest)} "
                  f"({evidence(largest)})")
    elif variant == "compare_cuts":
        match = re.fullmatch(
            r"Define L\(√2\) by q ∈ L\(√2\) iff q < 0 or q² < 2, and "
            r"define L\(3/2\) by q ∈ L\(3/2\) iff q < 3/2\. "
            r"Candidate list: \[([^]]+)\]\.", body)
        assert match is not None, body
        values = parse_list(match.group(1))
        separators = [value for value in values
                      if value < Fraction(3, 2) and not in_sqrt2_cut(value)]
        assert len(separators) == 1, values
        separator = separators[0]
        answer = (f"separator: {fraction_text(separator)} "
                  f"({fraction_text(separator)} ∈ L(3/2), "
                  f"{fraction_text(separator)} ∉ L(√2))")
    else:
        match = re.fullmatch(
            r"Define L\(([^)]+)\) by x ∈ L\(\1\) iff x < \1\. "
            r"Given q = ([^ ]+) in L\(\1\),", body)
        assert match is not None, body
        rational, lower = parse_fraction(match.group(1)), parse_fraction(match.group(2))
        midpoint = (lower + rational) / 2
        answer = (f"no largest; {fraction_text(lower)} < "
                  f"{fraction_text(midpoint)} < {fraction_text(rational)}")
        values = [lower, midpoint, rational]
    return {"variant": variant, "query": query, "answer": answer,
            "values": values}


class DedekindCutGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(428107)

    def test_output_contract(self):
        example = DedekindCutGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = DedekindCutGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_exact_arithmetic_inside_steps(self):
        generator = DedekindCutGenerator()
        for _ in range(350):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "E":
                    self.assertEqual(parse_fraction(fields[1]) ** int(fields[2]),
                                     parse_fraction(fields[3]))
                elif fields[0] == "A":
                    self.assertEqual(parse_fraction(fields[1]) +
                                     parse_fraction(fields[2]),
                                     parse_fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(parse_fraction(fields[1]) /
                                     parse_fraction(fields[2]),
                                     parse_fraction(fields[3]))
                elif fields[0] == "CMP":
                    left, right, relation = (parse_fraction(fields[1]),
                                             parse_fraction(fields[2]),
                                             fields[3])
                    if relation == "<":
                        self.assertLess(left, right)
                    elif relation == "=":
                        self.assertEqual(left, right)
                    else:
                        self.assertGreater(left, right)

    def test_generated_semantic_invariants(self):
        for variant in DedekindCutGenerator.VARIANTS:
            generator = DedekindCutGenerator(variant)
            for _ in range(120):
                example = generator.generate()
                parts = oracle_parts(example)
                values = parts["values"]
                if variant == "membership":
                    self.assertEqual(sum(in_sqrt2_cut(v) for v in values), 1)
                elif variant == "largest_of_list":
                    self.assertGreaterEqual(sum(in_sqrt2_cut(v) for v in values), 3)
                elif variant == "compare_cuts":
                    separators = [v for v in values
                                  if v < Fraction(3, 2) and not in_sqrt2_cut(v)]
                    self.assertEqual(len(separators), 1)
                else:
                    lower, midpoint, rational = values
                    self.assertLess(lower, midpoint)
                    self.assertLess(midpoint, rational)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in DedekindCutGenerator.VARIANTS:
            generator = DedekindCutGenerator(variant)
            seen_queries = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"dedekind_cut_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DedekindCutGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = DedekindCutGenerator()
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

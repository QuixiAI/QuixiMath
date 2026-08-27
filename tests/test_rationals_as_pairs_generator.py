"""Independent Fraction oracle for RationalsAsPairsGenerator."""
from fractions import Fraction
import random
import re
import unittest

from generators.rationals_as_pairs_generator import QUERIES, RationalsAsPairsGenerator
from helpers import DELIM


def parse_int(text):
    return int(text.replace("−", "-"))


def parse_pair(text):
    match = re.fullmatch(r"\(([−-]?\d+), (\d+)\)", text)
    assert match is not None, text
    return parse_int(match.group(1)), int(match.group(2))


def int_text(value):
    return str(value).replace("-", "−")


def pair_text(value):
    return f"({int_text(value.numerator)}, {value.denominator})"


def fraction_text(value):
    return (int_text(value.numerator) if value.denominator == 1
            else f"{int_text(value.numerator)}/{value.denominator}")


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "equivalence_check":
        match = re.fullmatch(
            r"Pairs: (\([−-]?\d+, \d+\)) and (\([−-]?\d+, \d+\))\. "
            r"Definition: \(a, b\) ~ \(c, d\) iff ad = bc, with b,d > 0\.",
            body)
        assert match is not None, body
        first, second = map(parse_pair, match.groups())
        left, right = first[0] * second[1], first[1] * second[0]
        result = left == right
        answer = (f"equivalent: {'yes' if result else 'no'} "
                  f"({int_text(left)} {'=' if result else '≠'} {int_text(right)})")
        pairs = [first, second]
    elif variant == "add":
        match = re.fullmatch(
            r"Add (\([−-]?\d+, \d+\)) \+ (\([−-]?\d+, \d+\))\. Rule: "
            r"\(a, b\) \+ \(c, d\) = \(ad \+ bc, bd\)\.", body)
        assert match is not None, body
        first, second = map(parse_pair, match.groups())
        value = Fraction(*first) + Fraction(*second)
        result = (first[0] * second[1] + first[1] * second[0],
                  first[1] * second[1])
        answer = f"{pair_text(value)} = {fraction_text(value)}"
        pairs = [first, second]
    elif variant == "multiply":
        match = re.fullmatch(
            r"Multiply (\([−-]?\d+, \d+\)) · (\([−-]?\d+, \d+\))\. Rule: "
            r"\(a, b\) · \(c, d\) = \(ac, bd\)\.", body)
        assert match is not None, body
        first, second = map(parse_pair, match.groups())
        value = Fraction(*first) * Fraction(*second)
        result = first[0] * second[0], first[1] * second[1]
        answer = f"{pair_text(value)} = {fraction_text(value)}"
        pairs = [first, second]
    elif variant == "canonical_form":
        match = re.fullmatch(
            r"Pair: (\([−-]?\d+, \d+\))\. Canonical form has positive "
            r"denominator and gcd\(abs\(a\), b\) = 1\.", body)
        assert match is not None, body
        original = parse_pair(match.group(1))
        value = Fraction(*original)
        result = original
        answer = f"{pair_text(value)} = {fraction_text(value)}"
        pairs = [original]
    else:
        match = re.fullmatch(
            r"Statement: (\([−-]?\d+, \d+\)) ([<≤]) "
            r"(\([−-]?\d+, \d+\))\. Denominators are positive; compare "
            r"ad \2 bc\.", body)
        assert match is not None, body
        first, operator, second = parse_pair(match.group(1)), match.group(2), parse_pair(match.group(3))
        left, right = first[0] * second[1], first[1] * second[0]
        result = left < right if operator == "<" else left <= right
        answer = (f"{'true' if result else 'false'}; {int_text(left)} "
                  f"{operator} {int_text(right)} is "
                  f"{'true' if result else 'false'}")
        pairs = [first, second]
    return {"variant": variant, "query": query, "pairs": pairs,
            "result": result, "answer": answer}


class RationalsAsPairsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(701933)

    def test_output_contract(self):
        example = RationalsAsPairsGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = RationalsAsPairsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_integer_steps_euclid_and_reductions_are_exact(self):
        generator = RationalsAsPairsGenerator()
        for _ in range(300):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "A":
                    self.assertEqual(parse_int(fields[1]) + parse_int(fields[2]),
                                     parse_int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(parse_int(fields[1]) * parse_int(fields[2]),
                                     parse_int(fields[3]))
                elif fields[0] == "GCD_DIV":
                    first, second, quotient, remainder = map(int, fields[1:])
                    self.assertEqual(first, second * quotient + remainder)
                    self.assertTrue(0 <= remainder < second)
                elif fields[0] == "REDUCE":
                    original, reduced = parse_pair(fields[1]), parse_pair(fields[2])
                    self.assertEqual(Fraction(*original), Fraction(*reduced))
                    self.assertEqual(Fraction(*reduced).numerator, reduced[0])
                    self.assertEqual(Fraction(*reduced).denominator, reduced[1])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in RationalsAsPairsGenerator.VARIANTS:
            generator = RationalsAsPairsGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"rationals_as_pairs_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RationalsAsPairsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = RationalsAsPairsGenerator()
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

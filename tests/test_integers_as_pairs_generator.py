"""Independent integer-arithmetic oracle for IntegersAsPairsGenerator."""
import random
import re
import unittest

from generators.integers_as_pairs_generator import QUERIES, IntegersAsPairsGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_pair(text):
    match = re.fullmatch(r"\((\d+), (\d+)\)", text)
    assert match is not None, text
    return tuple(map(int, match.groups()))


def signed(value):
    return str(value).replace("-", "−")


def canonical(pair):
    common = min(pair)
    return pair[0] - common, pair[1] - common


def value(pair):
    return pair[0] - pair[1]


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "equivalence_check":
        match = re.fullmatch(
            r"Pairs: (\(\d+, \d+\)) and (\(\d+, \d+\))\. Definition: "
            r"\(a, b\) ~ \(c, d\) iff a \+ d = b \+ c\.", body)
        assert match is not None, body
        first, second = map(parse_pair, match.groups())
        left, right = first[0] + second[1], first[1] + second[0]
        result = left == right
        answer = (f"equivalent: {'yes' if result else 'no'} "
                  f"({left} {'=' if result else '≠'} {right})")
        pairs = [first, second]
    elif variant == "canonical_representative":
        match = re.fullmatch(
            r"Pair: (\(\d+, \d+\))\. Equivalence: \(a, b\) ~ \(c, d\) "
            r"iff a \+ d = b \+ c\.", body)
        assert match is not None, body
        original = parse_pair(match.group(1))
        reduced = canonical(original)
        answer = f"({reduced[0]}, {reduced[1]}) ~ {signed(value(original))}"
        pairs, result = [original], reduced
    elif variant == "add":
        match = re.fullmatch(
            r"Add (\(\d+, \d+\)) \+ (\(\d+, \d+\))\. Rule: "
            r"\(a, b\) \+ \(c, d\) = \(a \+ c, b \+ d\)\.", body)
        assert match is not None, body
        first, second = map(parse_pair, match.groups())
        raw = first[0] + second[0], first[1] + second[1]
        reduced = canonical(raw)
        answer = f"({reduced[0]}, {reduced[1]}) ~ {signed(value(raw))}"
        pairs, result = [first, second], raw
    elif variant == "multiply":
        match = re.fullmatch(
            r"Multiply (\(\d+, \d+\)) · (\(\d+, \d+\))\. Rule: "
            r"\(a, b\) · \(c, d\) = \(ac \+ bd, ad \+ bc\)\.", body)
        assert match is not None, body
        first, second = map(parse_pair, match.groups())
        raw = (first[0] * second[0] + first[1] * second[1],
               first[0] * second[1] + first[1] * second[0])
        reduced = canonical(raw)
        answer = f"({reduced[0]}, {reduced[1]}) ~ {signed(value(raw))}"
        pairs, result = [first, second], raw
    else:
        match = re.fullmatch(
            r"Compare classes \[(\d+), (\d+)\] and \[(\d+), (\d+)\]\. "
            r"Definition: \[a, b\] ≤ \[c, d\] iff a \+ d ≤ b \+ c\.",
            body)
        assert match is not None, body
        numbers = list(map(int, match.groups()))
        first, second = tuple(numbers[:2]), tuple(numbers[2:])
        left, right = first[0] + second[1], first[1] + second[0]
        result = left <= right
        relation = "≤" if result else ">"
        answer = (f"{'true' if result else 'false'}; {signed(value(first))} "
                  f"{relation} {signed(value(second))} "
                  f"({left} {relation} {right})")
        pairs = [first, second]
    return {"variant": variant, "query": query, "pairs": pairs,
            "result": result, "answer": answer}


class IntegersAsPairsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(409913)

    def test_output_contract(self):
        example = IntegersAsPairsGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = IntegersAsPairsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_emitted_integer_arithmetic_and_reductions_are_exact(self):
        generator = IntegersAsPairsGenerator()
        for _ in range(300):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "REDUCE":
                    original, reduced = parse_pair(fields[1]), parse_pair(fields[2])
                    self.assertEqual(value(original), value(reduced))
                    self.assertEqual(min(reduced), 0)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in IntegersAsPairsGenerator.VARIANTS:
            generator = IntegersAsPairsGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"integers_as_pairs_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            IntegersAsPairsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = IntegersAsPairsGenerator()
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

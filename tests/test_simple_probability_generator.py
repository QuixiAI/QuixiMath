"""Independent finite-count oracle for SimpleProbabilityGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.simple_probability_generator import QUERIES, SimpleProbabilityGenerator
from helpers import DELIM


def split_query(problem):
    for query in QUERIES:
        suffix = " " + query
        if problem.endswith(suffix):
            return problem[:-len(suffix)], query
    raise AssertionError(problem)


def parse_roster(text):
    return [] if text == "∅" else [int(item) for item in text[1:-1].split(", ")]


def terminating_text(value):
    denominator = value.denominator
    places = 0
    while denominator % 2 == 0:
        denominator //= 2
        places += 1
    while denominator % 5 == 0:
        denominator //= 5
        places += 1
    assert denominator == 1
    rendered = f"{float(value):.{places}f}"
    return rendered.rstrip("0").rstrip(".") if "." in rendered else rendered


def oracle_parts(example):
    body, query = split_query(example["problem"])
    variant = (example["operation"].removeprefix("probability_simple_")
               if example["operation"] != "probability_simple" else "bare")
    output = re.search(
        r"Report P\(A\) as a (reduced fraction|fraction|percent|decimal)\.", body)
    assert output is not None, body
    form = output.group(1)
    if variant == "bare":
        match = re.search(
            r"uniform event has (\d+) favorable outcomes? among (\d+) total", body)
        favorable, total = map(int, match.groups())
    elif variant in ("spinner", "numbered_cards", "die"):
        match = re.search(r"S = (\{[^{}]+\}).+ A = (\{[^{}]+\})", body)
        sample, event = map(parse_roster, match.groups())
        favorable, total = len(event), len(sample)
    elif variant == "bag":
        match = re.search(
            r"bag color counts are (.+)\. Event A is drawing ([a-z]+)", body)
        counts = {name: int(count) for name, count in
                  (item.split("=") for item in match.group(1).split("; "))}
        favorable, total = counts[match.group(2)], sum(counts.values())
    elif variant == "letter_tiles":
        word = re.search(r"letter tiles spell ([A-Z]+)", body).group(1)
        favorable, total = sum(letter in "AEIOU" for letter in word), len(word)
    else:
        match = re.search(r"S = (\{[^{}]+\}).+first (\d+) tickets", body)
        total, favorable = len(parse_roster(match.group(1))), int(match.group(2))
    value = Fraction(favorable, total)
    if form == "percent":
        answer = terminating_text(value * 100) + "%"
    elif form == "decimal":
        answer = terminating_text(value)
    else:
        answer = str(value.numerator) if value.denominator == 1 else str(value)
    return {"variant": variant, "query": query, "answer": answer,
            "value": value, "favorable": favorable, "total": total}


class SimpleProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_output_contract_and_original_operation(self):
        example = SimpleProbabilityGenerator("bare").generate()
        self.assertEqual(example["operation"], "probability_simple")
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SimpleProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_step_arithmetic(self):
        generator = SimpleProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "PROB_SETUP":
                    self.assertEqual((int(fields[1]), int(fields[2])),
                                     (parts["favorable"], parts["total"]))
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in SimpleProbabilityGenerator.VARIANTS:
            generator = SimpleProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                parts = oracle_parts(generator.generate())
                self.assertEqual(parts["variant"], variant)
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SimpleProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SimpleProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

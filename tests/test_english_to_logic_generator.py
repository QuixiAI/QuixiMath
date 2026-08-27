"""Independent controlled-English inversion for EnglishToLogicGenerator."""
import random
import re
import unittest

from generators.english_to_logic_generator import QUERIES, EnglishToLogicGenerator
from helpers import DELIM
from tests.test_quantifier_negation_generator import parse_formula, render


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def unary_key(text, count):
    first = re.match(
        r"([A-Z])\(x\): x is (?:a|an) (\w+); ", text)
    assert first is not None, text
    noun_symbol, noun = first.groups()
    rest = text[first.end():]
    properties = []
    for index in range(count - 1):
        suffix = "; " if index < count - 2 else ""
        match = re.match(rf"([A-Z])\(x\): x is (\w+){re.escape(suffix)}", rest)
        assert match is not None, rest
        properties.append(match.groups())
        rest = rest[match.end():]
    assert not rest, rest
    return noun_symbol, noun, properties


def binary_key(text):
    match = re.fullmatch(
        r"([A-Z])\(x\): x is (?:a|an) (\w+); "
        r"([A-Z])\(y\): y is (?:a|an) (\w+); "
        r"([A-Z])\(x, y\): x (\w+) y", text)
    assert match is not None, text
    return match.groups()


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(r"Sentence: (.+)\. Predicate key: (.+)\.", body)
    assert match is not None, body
    sentence, key = match.groups()
    if variant in ("universal", "existential"):
        noun_symbol, noun, properties = unary_key(key, 2)
        property_symbol, prop = properties[0]
        noun_atom = f"{noun_symbol}(x)"
        property_atom = f"{property_symbol}(x)"
        if variant == "universal":
            positive = {
                f"Every {noun} is {prop}",
                f"All {noun}s are {prop}",
                f"Each {noun} is {prop}",
                f"Any {noun} is {prop}",
            }
            if sentence in positive:
                answer = f"∀x ({noun_atom} → {property_atom})"
            else:
                assert sentence == f"No {noun} is {prop}", sentence
                answer = f"∀x ({noun_atom} → ¬{property_atom})"
        else:
            positive = {
                f"Some {noun} is {prop}",
                f"At least one {noun} is {prop}",
                f"There is {'an' if noun[0] in 'aeiou' else 'a'} {noun} that is {prop}",
            }
            negative = {
                f"Some {noun} is not {prop}",
                f"There is {'an' if noun[0] in 'aeiou' else 'a'} {noun} that is not {prop}",
            }
            assert sentence in positive | negative, sentence
            second = property_atom if sentence in positive else "¬" + property_atom
            answer = f"∃x ({noun_atom} ∧ {second})"
    elif variant == "restricted_quantifier":
        noun_symbol, noun, properties = unary_key(key, 3)
        (first_symbol, first_property), (second_symbol, second_property) = properties
        restriction = f"({noun_symbol}(x) ∧ {first_symbol}(x))"
        if sentence in {
                f"Every {noun} who is {first_property} is {second_property}",
                f"All {noun}s who are {first_property} are {second_property}"}:
            answer = f"∀x ({restriction} → {second_symbol}(x))"
        elif sentence == (f"Some {noun} who is {first_property} is "
                          f"{second_property}"):
            answer = f"∃x ({restriction} ∧ {second_symbol}(x))"
        else:
            assert sentence == (f"No {noun} who is {first_property} is "
                                f"{second_property}"), sentence
            answer = f"∀x ({restriction} → ¬{second_symbol}(x))"
    else:
        (subject_symbol, subject, object_symbol, object_noun,
         relation_symbol, verb) = binary_key(key)
        subject_atom = f"{subject_symbol}(x)"
        object_atom = f"{object_symbol}(y)"
        relation_atom = f"{relation_symbol}(x, y)"
        if sentence == f"Every {subject} {verb} some {object_noun}":
            answer = (f"∀x ({subject_atom} → "
                      f"∃y ({object_atom} ∧ {relation_atom}))")
        elif sentence == f"Some {subject} {verb} every {object_noun}":
            answer = (f"∃x ({subject_atom} ∧ "
                      f"∀y ({object_atom} → {relation_atom}))")
        elif sentence == f"Every {subject} {verb} every {object_noun}":
            answer = (f"∀x ({subject_atom} → "
                      f"∀y ({object_atom} → {relation_atom}))")
        else:
            assert sentence == f"Some {subject} {verb} some {object_noun}", sentence
            answer = (f"∃x ({subject_atom} ∧ "
                      f"∃y ({object_atom} ∧ {relation_atom}))")
    return {"variant": variant, "query": query, "sentence": sentence,
            "key": key, "answer": answer}


class EnglishToLogicGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(552197)

    def test_output_contract(self):
        example = EnglishToLogicGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = EnglishToLogicGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_answers_parse_and_round_trip_canonically(self):
        generator = EnglishToLogicGenerator()
        for _ in range(400):
            example = generator.generate()
            parsed = parse_formula(example["final_answer"])
            self.assertEqual(render(parsed), example["final_answer"])

    def test_steps_repeat_key_and_finish_with_oracle_formula(self):
        generator = EnglishToLogicGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            fields = [raw.split(DELIM) for raw in example["steps"]]
            self.assertEqual(next(item[1] for item in fields
                                  if item[0] == "PREDICATES"), parts["key"])
            self.assertTrue(any(item[0] == "QUANT_CHOICE" for item in fields))
            self.assertTrue(any(item[0] == "SHAPE" for item in fields))
            rewrite = next(item[1] for item in fields if item[0] == "REWRITE")
            self.assertEqual(rewrite, parts["answer"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in EnglishToLogicGenerator.VARIANTS:
            generator = EnglishToLogicGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"english_to_logic_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EnglishToLogicGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = EnglishToLogicGenerator()
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

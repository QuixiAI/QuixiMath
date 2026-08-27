"""Independent finite-model oracle for SyllogismGenerator."""
import itertools
import random
import re
import unittest

from generators.syllogism_generator import QUERIES, SyllogismGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_proposition(text):
    patterns = (
        ("O", r"Some (\w+) are not (\w+)"),
        ("A", r"All (\w+) are (\w+)"),
        ("E", r"No (\w+) are (\w+)"),
        ("I", r"Some (\w+) are (\w+)"),
    )
    for letter, pattern in patterns:
        match = re.fullmatch(pattern, text)
        if match is not None:
            return letter, match.group(1), match.group(2)
    raise AssertionError(text)


def statement_holds(statement, model):
    letter, subject, predicate = statement
    subject_set, predicate_set = model[subject], model[predicate]
    if letter == "A":
        return subject_set <= predicate_set
    if letter == "E":
        return subject_set.isdisjoint(predicate_set)
    if letter == "I":
        return bool(subject_set & predicate_set)
    if letter == "O":
        return bool(subject_set - predicate_set)
    raise AssertionError(statement)


def infer_figure(major, minor, conclusion):
    subject, predicate = conclusion[1], conclusion[2]
    terms = ({major[1], major[2], minor[1], minor[2]}
             - {subject, predicate})
    assert len(terms) == 1, terms
    middle = terms.pop()
    positions = ((middle, predicate, subject, middle),
                 (predicate, middle, subject, middle),
                 (middle, predicate, middle, subject),
                 (predicate, middle, middle, subject))
    actual = (major[1], major[2], minor[1], minor[2])
    assert actual in positions, (actual, positions)
    return positions.index(actual) + 1


def all_term_subsets():
    universe = range(3)
    return [frozenset(item for item in universe if mask & (1 << item))
            for mask in range(8)]


def first_countermodel(major, minor, conclusion):
    names = sorted({major[1], major[2], minor[1], minor[2],
                    conclusion[1], conclusion[2]})
    for choices in itertools.product(all_term_subsets(), repeat=3):
        model = dict(zip(names, choices))
        if (statement_holds(major, model)
                and statement_holds(minor, model)
                and not statement_holds(conclusion, model)):
            return model
    return None


def membership_column(items):
    return "".join("T" if index in items else "F" for index in range(3))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(r"Premises: (.+); (.+)\. Conclusion: (.+)\.", body)
    assert match is not None, body
    major, minor, conclusion = map(parse_proposition, match.groups())
    mood = major[0] + minor[0] + conclusion[0]
    figure = infer_figure(major, minor, conclusion)
    countermodel = first_countermodel(major, minor, conclusion)
    answer = f"{'valid' if countermodel is None else 'invalid'}; {mood}-{figure}"
    return {"variant": variant, "query": query, "major": major,
            "minor": minor, "conclusion": conclusion, "mood": mood,
            "figure": figure, "countermodel": countermodel,
            "answer": answer}


def expected_venn(statement, witness):
    letter, subject, predicate = statement
    if letter == "A":
        return ["VENN_SHADE", f"{subject} − {predicate}", "empty"]
    if letter == "E":
        return ["VENN_SHADE", f"{subject} ∩ {predicate}", "empty"]
    if letter == "I":
        return ["VENN_MARK", f"{subject} ∩ {predicate}", witness]
    return ["VENN_MARK", f"{subject} ∩ ¬{predicate}", witness]


class SyllogismGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(910331)

    def test_output_contract(self):
        example = SyllogismGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SyllogismGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_mood_venn_steps_and_finite_model_checks(self):
        generator = SyllogismGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [item.split(DELIM) for item in example["steps"]]
            self.assertEqual(steps[0], ["MOOD", parts["mood"],
                                        f"figure {parts['figure']}"])
            self.assertEqual(steps[1], expected_venn(parts["major"], "x1"))
            self.assertEqual(steps[2], expected_venn(parts["minor"], "x2"))
            if parts["countermodel"] is None:
                self.assertEqual(steps[3], ["CONCLUSION_CHECK", "forced"])
                self.assertIn(["CHECK", "all 512 assignments",
                               "no countermodel"], steps)
                self.assertFalse(any(item[0] == "COUNTERMODEL" for item in steps))
            else:
                self.assertEqual(steps[3], ["CONCLUSION_CHECK", "not forced"])
                counter_step = next(item for item in steps
                                    if item[0] == "COUNTERMODEL")
                printed = dict(field.split("=")
                               for field in counter_step[1].split(", "))
                expected_names = {parts["major"][1], parts["major"][2],
                                  parts["minor"][1], parts["minor"][2]}
                self.assertEqual(set(printed), expected_names)
                printed_model = {
                    name: frozenset(index for index, value in enumerate(column)
                                    if value == "T")
                    for name, column in printed.items()
                }
                self.assertTrue(statement_holds(parts["major"], printed_model))
                self.assertTrue(statement_holds(parts["minor"], printed_model))
                self.assertFalse(statement_holds(parts["conclusion"],
                                                 printed_model))
                self.assertIn(["CHECK", "countermodel", "premises=T,T",
                               "conclusion=F"], steps)

    def test_all_variants_phrasings_and_validity_outcomes(self):
        for variant in SyllogismGenerator.VARIANTS:
            generator = SyllogismGenerator(variant)
            seen_queries = set()
            outcomes = set()
            for _ in range(500):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"syllogism_{variant}")
                seen_queries.add(parts["query"])
                outcomes.add(parts["countermodel"] is None)
            self.assertEqual(seen_queries, set(QUERIES[variant]))
            self.assertEqual(outcomes, {False, True})

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SyllogismGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SyllogismGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

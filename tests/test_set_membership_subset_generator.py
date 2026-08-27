"""Independent A9 checks for SetMembershipSubsetGenerator."""
import random
import re
import unittest

from generators.set_membership_subset_generator import (
    QUERIES,
    SetMembershipSubsetGenerator,
)
from helpers import DELIM
from tests import foundations_oracle as set_oracle


def split_query(problem, variant):
    for query in QUERIES[variant]:
        if problem.endswith(f" {query}"):
            return problem[:-(len(query) + 1)], query
    raise AssertionError(problem)


def parse_raw(text):
    assert text.startswith("[") and text.endswith("]"), text
    return [] if text == "[]" else [int(item) for item in text[1:-1].split(", ")]


def oracle_parts(example):
    problem = example["problem"]
    if problem.startswith("Set A = ") and ". Focus value: " in problem:
        body, query = split_query(problem, "membership")
        match = re.fullmatch(r"Set A = (.+)\. Focus value: (\d+)\.", body)
        assert match is not None, body
        values = set_oracle.parse_set(match.group(1))
        focus = int(match.group(2))
        answer = (f"{focus} ∈ A: {'yes' if focus in values else 'no'}; "
                  f"A = {set_oracle.roster_text(values)}")
        return {"variant": "membership", "A": values, "focus": focus,
                "answer": answer, "query": query}
    if problem.startswith("Set A = ") and ". Set B = " in problem:
        body, query = split_query(problem, "subset")
        match = re.fullmatch(r"Set A = (.+)\. Set B = (.+)\.", body)
        assert match is not None, body
        values_a = set_oracle.parse_set(match.group(1))
        values_b = set_oracle.parse_set(match.group(2))
        missing = values_a - values_b
        answer = (f"A ⊆ B: {'yes' if not missing else 'no'}; "
                  f"missing = {set_oracle.roster_text(missing)}")
        return {"variant": "subset", "A": values_a, "B": values_b,
                "missing": missing, "answer": answer, "query": query}
    if problem.startswith("Raw entries A = ") and ". Raw entries B = " in problem:
        body, query = split_query(problem, "equality")
        match = re.fullmatch(
            r"Raw entries A = (\[[^]]*\])\. Raw entries B = (\[[^]]*\])\.",
            body,
        )
        assert match is not None, body
        raw_a, raw_b = parse_raw(match.group(1)), parse_raw(match.group(2))
        values_a, values_b = frozenset(raw_a), frozenset(raw_b)
        answer = (f"A = B: {'yes' if values_a == values_b else 'no'}; "
                  f"reduced A = {set_oracle.roster_text(values_a)}; "
                  f"reduced B = {set_oracle.roster_text(values_b)}")
        return {"variant": "equality", "raw_a": raw_a, "raw_b": raw_b,
                "A": values_a, "B": values_b, "answer": answer,
                "query": query}
    if problem.startswith("Set A = "):
        body, query = split_query(problem, "element_vs_subset")
        match = re.fullmatch(r"Set A = (.+)\. Focus value n = (\d+)\.", body)
        assert match is not None, body
        values = set_oracle.parse_set(match.group(1))
        focus = int(match.group(2))
        singleton = frozenset((focus,))
        answer = (
            f"{focus} ∈ A: {'yes' if focus in values else 'no'}; "
            f"{{{focus}}} ⊆ A: {'yes' if singleton <= values else 'no'}; "
            f"{{{focus}}} ∈ A: {'yes' if singleton in values else 'no'}"
        )
        return {"variant": "element_vs_subset", "A": values,
                "focus": focus, "answer": answer, "query": query}

    body, query = split_query(problem, "count")
    match = re.fullmatch(r"Raw entries A = (\[[^]]*\])\.", body)
    assert match is not None, body
    raw = parse_raw(match.group(1))
    values = frozenset(raw)
    answer = f"card(A) = {len(values)}; A = {set_oracle.roster_text(values)}"
    return {"variant": "count", "raw_a": raw, "A": values,
            "answer": answer, "query": query}


class SetMembershipSubsetGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(196613)

    def test_output_contract(self):
        example = SetMembershipSubsetGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SetMembershipSubsetGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_element_subset_dedup_and_count_steps(self):
        generator = SetMembershipSubsetGenerator()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            saw_scan = False
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "DEDUP":
                    label = fields[1][0]
                    raw = parts["raw_a"] if label == "A" else parts["raw_b"]
                    expected = set_oracle.roster_text(frozenset(raw))
                    self.assertEqual(fields[2], expected)
                elif fields[0] == "SUBSET_CHECK":
                    saw_scan = True
                    if parts["variant"] == "subset":
                        value = int(fields[1])
                        self.assertEqual(fields[2], "in B?")
                        self.assertEqual(fields[3],
                                         "yes" if value in parts["B"] else "no")
                    else:
                        self.assertEqual(parts["variant"], "element_vs_subset")
                        singleton = frozenset((parts["focus"],))
                        self.assertEqual(fields[3],
                                         "yes" if singleton <= parts["A"] else "no")
                elif fields[0] == "COUNT":
                    self.assertEqual(parts["variant"], "count")
                    self.assertEqual(fields[1:], ["A", str(len(parts["A"]))])
                elif fields[0] == "ELEMENT_SCAN":
                    saw_scan = True
            if parts["variant"] in ("membership", "subset", "equality",
                                    "element_vs_subset"):
                self.assertTrue(saw_scan)

    def test_all_variants_phrasings_and_verdicts_are_reachable(self):
        for variant in SetMembershipSubsetGenerator.VARIANTS:
            generator = SetMembershipSubsetGenerator(variant)
            seen_queries = set()
            answers = []
            for _ in range(500):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"set_membership_subset_{variant}")
                seen_queries.add(parts["query"])
                answers.append(parts["answer"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))
            if variant in ("membership", "subset", "equality",
                           "element_vs_subset"):
                self.assertTrue(any(": yes" in answer for answer in answers))
                self.assertTrue(any(": no" in answer for answer in answers))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            SetMembershipSubsetGenerator("bogus")

    def test_pipe_safety_canonical_rosters_and_render_sanity(self):
        generator = SetMembershipSubsetGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for token in re.findall(r"\{[^{}]*\}",
                                    example["problem"] + example["final_answer"]):
                items = set_oracle.parse_roster(token)
                self.assertEqual(len(items), len(set(items)))
                self.assertTrue(set_oracle.roster_order_ok(items))
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

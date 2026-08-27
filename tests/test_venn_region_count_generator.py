"""Independent A9 checks for VennRegionCountGenerator."""
import random
import re
import unittest

from generators.venn_region_count_generator import QUERIES, VennRegionCountGenerator
from helpers import DELIM


def ending_query(problem, choices):
    for query in choices:
        if problem.endswith(f" {query}"):
            return problem[:-(len(query) + 1)], query
    raise AssertionError(problem)


def oracle_parts(example):
    problem = example["problem"]
    if problem.startswith("Survey: "):
        body, query = ending_query(problem, QUERIES["word"])
        match = re.fullmatch(
            r"Survey: (\d+) students total\. Category A: (.+)\. "
            r"Category B: (.+)\. card\(A\) = (\d+); "
            r"card\(B\) = (\d+); card\(A ∩ B\) = (\d+)\.", body
        )
        assert match is not None, body
        card_u, card_a, card_b, both = map(
            int, (match.group(1), match.group(4), match.group(5), match.group(6))
        )
        variant = "word_problem"
    elif "card(C)" not in problem:
        body, query = ending_query(problem, QUERIES["two"])
        match = re.fullmatch(
            r"card\(U\) = (\d+); card\(A\) = (\d+); card\(B\) = (\d+); "
            r"card\(A ∩ B\) = (\d+)\.", body
        )
        assert match is not None, body
        card_u, card_a, card_b, both = map(int, match.groups())
        variant = "two_set"
    else:
        body, query = ending_query(problem, QUERIES["three"])
        match = re.fullmatch(
            r"card\(U\) = (\d+); card\(A\) = (\d+); card\(B\) = (\d+); "
            r"card\(C\) = (\d+); card\(A ∩ B\) = (\d+); "
            r"card\(A ∩ C\) = (\d+); card\(B ∩ C\) = (\d+); "
            r"card\(A ∩ B ∩ C\) = (\d+)\.", body
        )
        assert match is not None, body
        card_u, card_a, card_b, card_c, ab, ac, bc, triple = map(
            int, match.groups()
        )
        ab_only, ac_only, bc_only = ab - triple, ac - triple, bc - triple
        only_a = card_a - ab_only - ac_only - triple
        only_b = card_b - ab_only - bc_only - triple
        only_c = card_c - ac_only - bc_only - triple
        none = card_u - sum((only_a, only_b, only_c, ab_only, ac_only,
                             bc_only, triple))
        regions = {
            "only A": only_a, "only B": only_b, "only C": only_c,
            "A and B only": ab_only, "A and C only": ac_only,
            "B and C only": bc_only, "all three": triple, "none": none,
        }
        answer = (
            f"only A = {only_a}; only B = {only_b}; only C = {only_c}; "
            f"A and B only = {ab_only}; A and C only = {ac_only}; "
            f"B and C only = {bc_only}; all three = {triple}; none = {none}"
        )
        return {"variant": "three_set", "card_u": card_u,
                "regions": regions, "answer": answer, "query": query}

    only_a, only_b = card_a - both, card_b - both
    neither = card_u - only_a - only_b - both
    regions = {"only A": only_a, "only B": only_b, "both": both,
               "neither": neither}
    answer = (f"only A = {only_a}; only B = {only_b}; both = {both}; "
              f"neither = {neither}")
    return {"variant": variant, "card_u": card_u, "regions": regions,
            "answer": answer, "query": query}


class VennRegionCountGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(262147)

    def test_output_contract(self):
        example = VennRegionCountGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = VennRegionCountGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_step_arithmetic_regions_and_checks(self):
        generator = VennRegionCountGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_regions = {}
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "REGION":
                    seen_regions[fields[1]] = int(fields[2])
                elif fields[0] == "REGION_EQ":
                    label = "all three" if fields[1] == "A ∩ B ∩ C" else "both"
                    self.assertEqual(int(fields[2]), parts["regions"][label])
                elif fields[0] == "CHECK":
                    self.assertEqual(fields[1:],
                                     ["sum of regions", str(parts["card_u"]),
                                      "card(U)"])
            self.assertEqual(seen_regions, parts["regions"])
            self.assertEqual(sum(parts["regions"].values()), parts["card_u"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        query_key = {"two_set": "two", "three_set": "three",
                     "word_problem": "word"}
        for variant in VennRegionCountGenerator.VARIANTS:
            generator = VennRegionCountGenerator(variant)
            seen = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"venn_region_count_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[query_key[variant]]))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            VennRegionCountGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = VennRegionCountGenerator()
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

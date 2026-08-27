"""Independent A9 checks for OneToOneCorrespondenceGenerator."""
import random
import re
import unittest

from generators.one_to_one_correspondence_generator import (
    OneToOneCorrespondenceGenerator,
    QUERIES,
)
from helpers import DELIM


def parse_roster(text):
    if text == "∅":
        return []
    assert text.startswith("{") and text.endswith("}"), text
    return text[1:-1].split(", ")


def fmt_roster(values):
    return "{" + ", ".join(values) + "}" if values else "∅"


def split_query(problem, variant):
    for query in QUERIES[variant]:
        suffix = f" {query}"
        if problem.endswith(suffix):
            return problem[:-len(suffix)], query
    raise AssertionError(problem)


def oracle_parts(example):
    problem = example["problem"]
    if problem.startswith("A = "):
        prefix, query = split_query(problem, "compare_by_pairing")
        match = re.fullmatch(r"A = (\{.*\}|∅)\. B = (\{.*\}|∅)\.", prefix)
        assert match is not None, prefix
        values_a = parse_roster(match.group(1))
        values_b = parse_roster(match.group(2))
        if len(values_a) == len(values_b):
            answer = f"same size ({len(values_a)} each)"
            unmatched = ("neither", [])
        elif len(values_a) > len(values_b):
            answer = (f"A has {len(values_a) - len(values_b)} more "
                      f"({len(values_a)} vs {len(values_b)})")
            unmatched = ("A", values_a[len(values_b):])
        else:
            answer = (f"B has {len(values_b) - len(values_a)} more "
                      f"({len(values_b)} vs {len(values_a)})")
            unmatched = ("B", values_b[len(values_a):])
        return {
            "variant": "compare_by_pairing",
            "sets": [values_a, values_b],
            "answer": answer,
            "unmatched": unmatched,
            "query": query,
        }
    if problem.startswith("Objects = "):
        prefix, query = split_query(problem, "count_by_pairing")
        match = re.fullmatch(
            r"Objects = (\{.*\}|∅)\. Labels = (\{.*\}|∅)\.", prefix
        )
        assert match is not None, prefix
        objects = parse_roster(match.group(1))
        labels = parse_roster(match.group(2))
        size = len(objects)
        return {
            "variant": "count_by_pairing",
            "sets": [objects, labels],
            "answer": f"card(Objects) = {size}; paired all {size} objects",
            "query": query,
        }

    prefix, query = split_query(problem, "cardinal_class")
    assert prefix.startswith("Sets: "), prefix
    assignments = prefix[len("Sets: "):-1].split("; ")
    sets = []
    for index, assignment in enumerate(assignments):
        match = re.fullmatch(r"([ABCD]) = (\{.*\}|∅)", assignment)
        assert match is not None, assignment
        assert match.group(1) == chr(65 + index)
        sets.append(parse_roster(match.group(2)))
    groups = {}
    for index, values in enumerate(sets):
        groups.setdefault(len(values), []).append(chr(65 + index))
    answer = "; ".join(
        f"card {size}: {', '.join(groups[size])}" for size in sorted(groups)
    )
    return {
        "variant": "cardinal_class",
        "sets": sets,
        "groups": groups,
        "answer": answer,
        "query": query,
    }


class OneToOneCorrespondenceGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(130363)

    def test_output_contract(self):
        example = OneToOneCorrespondenceGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = OneToOneCorrespondenceGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_pair_count_and_unpaired_steps(self):
        for variant in OneToOneCorrespondenceGenerator.VARIANTS:
            generator = OneToOneCorrespondenceGenerator(variant)
            for _ in range(150):
                example = generator.generate()
                parts = oracle_parts(example)
                steps = [raw.split(DELIM) for raw in example["steps"]]
                pairs = [fields[1:] for fields in steps if fields[0] == "PAIR"]
                counts = [fields[1:] for fields in steps if fields[0] == "COUNT"]
                if variant == "compare_by_pairing":
                    left, right = parts["sets"]
                    self.assertEqual(pairs,
                                     [[a, b] for a, b in zip(left, right)])
                    side, values = parts["unmatched"]
                    self.assertIn(["UNPAIRED", side, fmt_roster(values)], steps)
                    self.assertEqual(counts,
                                     [["A", str(len(left))],
                                      ["B", str(len(right))]])
                elif variant == "count_by_pairing":
                    objects, labels = parts["sets"]
                    self.assertEqual(pairs,
                                     [[a, b] for a, b in zip(objects, labels)])
                    self.assertEqual(counts, [["Objects", str(len(objects))]])
                else:
                    self.assertEqual(
                        counts,
                        [[chr(65 + index), str(len(values))]
                         for index, values in enumerate(parts["sets"])],
                    )
                    for left, right in pairs:
                        left_set, left_value = left.split(": ", 1)
                        right_set, right_value = right.split(": ", 1)
                        self.assertEqual(len(parts["sets"][ord(left_set) - 65]),
                                         len(parts["sets"][ord(right_set) - 65]))
                        self.assertIn(left_value,
                                      parts["sets"][ord(left_set) - 65])
                        self.assertIn(right_value,
                                      parts["sets"][ord(right_set) - 65])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in OneToOneCorrespondenceGenerator.VARIANTS:
            generator = OneToOneCorrespondenceGenerator(variant)
            seen = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"one_to_one_correspondence_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            OneToOneCorrespondenceGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = OneToOneCorrespondenceGenerator()
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

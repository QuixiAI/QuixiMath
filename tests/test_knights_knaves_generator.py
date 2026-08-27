"""Independent brute-force oracle for KnightsKnavesGenerator."""
import itertools
import random
import re
import unittest

from generators.knights_knaves_generator import KnightsKnavesGenerator, QUERIES
from helpers import DELIM


def statement_value(text, assignment):
    match = re.fullmatch(r"([A-Z][a-z]+) is a (knight|knave)", text)
    if match:
        value = assignment[match.group(1)]
        return value if match.group(2) == "knight" else not value
    match = re.fullmatch(
        r"([A-Z][a-z]+) and ([A-Z][a-z]+) are (the same type|different types)",
        text,
    )
    if match:
        same = assignment[match.group(1)] == assignment[match.group(2)]
        return same if match.group(3) == "the same type" else not same
    match = re.fullmatch(
        r"at least one of ([A-Z][a-z]+) and ([A-Z][a-z]+) is a knight", text
    )
    if match:
        return assignment[match.group(1)] or assignment[match.group(2)]
    match = re.fullmatch(
        r"both ([A-Z][a-z]+) and ([A-Z][a-z]+) are knaves", text
    )
    assert match is not None, text
    return not assignment[match.group(1)] and not assignment[match.group(2)]


def assignment_text(names, assignment):
    return ", ".join(
        f"{name}={'knight' if assignment[name] else 'knave'}" for name in names
    )


def answer_text(names, assignment):
    return ", ".join(
        f"{name} {'knight' if assignment[name] else 'knave'}" for name in names
    )


def oracle_parts(example):
    problem = example["problem"]
    query = next((item for item in QUERIES if problem.endswith(f" {item}")), None)
    assert query is not None, problem
    body = problem[:-(len(query) + 1)]
    match = re.fullmatch(
        r"Puzzle format: (two islanders|three islanders|one statement each)\. "
        r"Each person is either a knight who always tells the truth or a knave "
        r"who always lies\. (.+) Check assignments with names in listed order "
        r"and knight before knave\.", body
    )
    assert match is not None, body
    statements = re.findall(r'([A-Z][a-z]+) says "(.+?)\."', match.group(2))
    names = tuple(speaker for speaker, _ in statements)
    assert len(names) == len(set(names))
    assignments = [dict(zip(names, values))
                   for values in itertools.product((True, False), repeat=len(names))]
    survivors = []
    for assignment in assignments:
        if all(statement_value(text, assignment) == assignment[speaker]
               for speaker, text in statements):
            survivors.append(assignment)
    assert len(survivors) == 1
    variant = match.group(1).replace(" ", "_")
    return {"variant": variant, "names": names, "statements": statements,
            "assignments": assignments, "solution": survivors[0],
            "answer": answer_text(names, survivors[0]), "query": query}


class KnightsKnavesGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(350377)

    def test_output_contract(self):
        example = KnightsKnavesGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = KnightsKnavesGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_case_order_statement_values_and_unique_accept(self):
        generator = KnightsKnavesGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            expected_cases = [assignment_text(parts["names"], assignment)
                              for assignment in parts["assignments"]]
            seen_cases = []
            accepted = []
            current_assignment = None
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "CASE":
                    seen_cases.append(fields[1])
                    index = expected_cases.index(fields[1])
                    current_assignment = parts["assignments"][index]
                elif fields[0] == "STATEMENT_EVAL":
                    match = re.fullmatch(r"([A-Z][a-z]+) says (.+)", fields[1])
                    self.assertIsNotNone(match)
                    truth = statement_value(match.group(2), current_assignment)
                    self.assertEqual(fields[2], "T" if truth else "F")
                    consistent = truth == current_assignment[match.group(1)]
                    self.assertEqual(fields[3],
                                     "consistent" if consistent else "contradiction")
                elif fields[0] == "ACCEPT":
                    accepted.append(fields[1])
            self.assertEqual(seen_cases, expected_cases)
            self.assertEqual(accepted,
                             [assignment_text(parts["names"], parts["solution"])])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in KnightsKnavesGenerator.VARIANTS:
            generator = KnightsKnavesGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"knights_knaves_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            KnightsKnavesGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = KnightsKnavesGenerator()
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

"""Independent permutation oracle for LogicGridPuzzleGenerator."""
import itertools
import random
import re
import unittest

from generators.logic_grid_puzzle_generator import LogicGridPuzzleGenerator, QUERIES
from helpers import DELIM


def parse_list(text):
    assert text.startswith("[") and text.endswith("]"), text
    return tuple(text[1:-1].split(", "))


def mapping_text(names, candidate):
    if isinstance(candidate[0], tuple):
        return "; ".join(f"{name}: {pet}, {drink}"
                         for name, pet, drink in zip(names, candidate[0], candidate[1]))
    return "; ".join(f"{name}: {item}" for name, item in zip(names, candidate))


def clue_holds(text, names, candidate, item_order=None):
    two_categories = isinstance(candidate[0], tuple)
    match = re.fullmatch(r"the person with (\w+) drinks (\w+)", text)
    if match:
        pets, drinks = candidate
        return drinks[pets.index(match.group(1))] == match.group(2)
    match = re.fullmatch(r"([A-Z][a-z]+)'s item comes before "
                         r"([A-Z][a-z]+)'s item in the listed order", text)
    if match:
        first, second = names.index(match.group(1)), names.index(match.group(2))
        return item_order.index(candidate[first]) < item_order.index(candidate[second])
    match = re.fullmatch(r"([A-Z][a-z]+) does not drink (\w+)", text)
    if match:
        return candidate[1][names.index(match.group(1))] != match.group(2)
    match = re.fullmatch(r"([A-Z][a-z]+) drinks (\w+)", text)
    if match:
        return candidate[1][names.index(match.group(1))] == match.group(2)
    match = re.fullmatch(r"([A-Z][a-z]+) does not have (\w+)", text)
    if match:
        values = candidate[0] if two_categories else candidate
        return values[names.index(match.group(1))] != match.group(2)
    match = re.fullmatch(r"([A-Z][a-z]+) has (\w+)", text)
    assert match is not None, text
    values = candidate[0] if two_categories else candidate
    return values[names.index(match.group(1))] == match.group(2)


def oracle_parts(example):
    problem = example["problem"]
    query = next((item for item in QUERIES if problem.endswith(f" {item}")), None)
    assert query is not None, problem
    body = problem[:-(len(query) + 1)]
    prefix_match = re.match(
        r"Puzzle format: (three by three|three by three two categories|four by four)\. ",
        body,
    )
    assert prefix_match is not None, body
    variant = prefix_match.group(1).replace(" ", "_")
    rest = body[prefix_match.end():]
    if variant == "three_by_three_two_categories":
        match = re.fullmatch(
            r"People: (\[[^\]]+\])\. Pets: (\[[^\]]+\])\. Drinks: "
            r"(\[[^\]]+\])\. Clues: (.+)", rest
        )
        assert match is not None, rest
        names, pets, drinks = map(parse_list, match.groups()[:3])
        candidates = [(pet_perm, drink_perm)
                      for pet_perm in itertools.permutations(pets)
                      for drink_perm in itertools.permutations(drinks)]
        item_order = None
    else:
        match = re.fullmatch(
            r"People: (\[[^\]]+\])\. Items in order: (\[[^\]]+\])\. "
            r"Clues: (.+)", rest
        )
        assert match is not None, rest
        names, items = parse_list(match.group(1)), parse_list(match.group(2))
        candidates = list(itertools.permutations(items))
        item_order = items
    clues = [text for _, text in re.findall(r"\((\d+)\) (.+?)\.", match.group(4)
                                             if variant == "three_by_three_two_categories"
                                             else match.group(3))]
    assert clues
    survivor_counts = [len(candidates)]
    survivors = candidates
    for clue in clues:
        survivors = [candidate for candidate in survivors
                     if clue_holds(clue, names, candidate, item_order)]
        survivor_counts.append(len(survivors))
    assert len(survivors) == 1
    return {"variant": variant, "names": names, "clues": clues,
            "candidate_count": len(candidates), "survivor_counts": survivor_counts,
            "solution": survivors[0], "answer": mapping_text(names, survivors[0]),
            "query": query, "item_order": item_order}


class LogicGridPuzzleGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(371293)

    def test_output_contract(self):
        example = LogicGridPuzzleGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = LogicGridPuzzleGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_clue_application_counts_deductions_and_checks(self):
        generator = LogicGridPuzzleGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            clue_steps = []
            checks = []
            deductions = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "CLUE_APPLY":
                    clue_steps.append(fields)
                elif fields[0] == "CHECK":
                    checks.append(fields)
                elif fields[0] == "DEDUCE":
                    deductions.append(fields)
            self.assertEqual(len(clue_steps), len(parts["clues"]))
            for index, fields in enumerate(clue_steps):
                self.assertEqual(fields[1], f"clue {index + 1}")
                self.assertEqual(fields[2], parts["clues"][index])
                self.assertEqual(
                    fields[3],
                    f"{parts['survivor_counts'][index]} → "
                    f"{parts['survivor_counts'][index + 1]} candidates",
                )
            self.assertTrue(all(fields[2] == "holds" for fields in checks))
            expected_deductions = len(parts["names"]) * (
                2 if parts["variant"] == "three_by_three_two_categories" else 1
            )
            self.assertEqual(len(deductions), expected_deductions)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in LogicGridPuzzleGenerator.VARIANTS:
            generator = LogicGridPuzzleGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"logic_grid_puzzle_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            LogicGridPuzzleGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = LogicGridPuzzleGenerator()
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

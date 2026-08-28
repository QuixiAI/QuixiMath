"""Independent finite-space oracle for ClassicProbabilityPuzzlesGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.classic_probability_puzzles_generator import (
    QUERIES, ClassicProbabilityPuzzlesGenerator,
)
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def monty_switch_probability(doors, opened, pick):
    total = Fraction()
    door_set = set(range(1, doors + 1))
    for prize in door_set:
        eligible = door_set - {pick, prize}
        host_options = tuple(itertools.combinations(sorted(eligible), opened))
        for host_tuple in host_options:
            host = set(host_tuple)
            switch_options = door_set - host - {pick}
            for switch_pick in switch_options:
                if switch_pick == prize:
                    total += (Fraction(1, doors)
                              * Fraction(1, len(host_options))
                              * Fraction(1, len(switch_options)))
    return total


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("monty_hall", "monty_hall_n_doors"):
        match = re.fullmatch(
            r"At the (.+) in ([A-Za-z]+), ([A-Za-z]+) plays for a ([a-z]+)\. "
            r"There are (\d+) doors and \3 initially chooses door (\d+)\. The host "
            r"knows the prize location and opens (\d+) losing doors uniformly among "
            r"valid choices\. If switching, the contestant chooses uniformly among "
            r"the other unopened doors\.", body)
        assert match is not None, body
        doors, pick, opened = map(int, match.group(5, 6, 7))
        switch = monty_switch_probability(doors, opened, pick)
        stay = Fraction(1, doors)
        answer = f"switch; {ptext(switch)} vs {ptext(stay)}"
    elif variant in ("birthday", "birthday_expected_pairs"):
        pattern = (r"At the (.+) in ([A-Za-z]+), (\d+) people have birthdays "
                   r"independently and uniformly among (\d+) calendar days\.")
        if variant == "birthday_expected_pairs":
            pattern += r" Let Y count unordered pairs who share a birthday\."
        match = re.fullmatch(pattern, body)
        assert match is not None, body
        people, days = int(match.group(3)), int(match.group(4))
        if variant == "birthday":
            different = Fraction(1)
            for index in range(people):
                different *= Fraction(days - index, days)
            answer = ptext(1 - different)
        else:
            # Sum the expectation of one equality indicator for each pair.
            indicators = [Fraction(1, days)
                          for _ in itertools.combinations(range(people), 2)]
            answer = f"E[matching pairs] = {ptext(sum(indicators, Fraction()))}"
    elif variant == "birthday_specific_person":
        match = re.fullmatch(
            r"At the (.+) in ([A-Za-z]+), ([A-Za-z]+) is one of (\d+) people "
            r"whose birthdays are independent and uniform among (\d+) calendar days\.",
            body)
        assert match is not None, body
        people, days = int(match.group(4)), int(match.group(5))
        # Enumerate only match/miss statuses for the other people.
        probability = Fraction()
        for statuses in itertools.product((False, True), repeat=people - 1):
            weight = Fraction(1)
            for matches in statuses:
                weight *= Fraction(1, days) if matches else Fraction(days - 1, days)
            if any(statuses):
                probability += weight
        answer = ptext(probability)
    elif variant == "two_child":
        match = re.fullmatch(
            r"The ([A-Za-z]+) family is visiting the (.+) in ([A-Za-z]+)\. Two "
            r"children are independently equally likely to be B or G, ordered older "
            r"then younger\. Information: (.+)\.", body)
        assert match is not None, body
        condition = match.group(4)
        outcomes = tuple("".join(bits) for bits in itertools.product("BG", repeat=2))
        if condition == "at least one child is B":
            space = tuple(outcome for outcome in outcomes if "B" in outcome)
        else:
            assert condition == "the older child is B"
            space = tuple(outcome for outcome in outcomes if outcome[0] == "B")
        probability = Fraction(space.count("BB"), len(space))
        answer = f"{ptext(probability)}; sample space {{{', '.join(space)}}}"
    else:
        match = re.fullmatch(
            r"At the (.+) in ([A-Za-z]+), three boxes contain ([a-z]+)-\3, "
            r"\3-([a-z]+), and \4-\4 tokens\. A box is chosen uniformly, then one "
            r"token from it is observed uniformly and is \3\. Target: P\(the other "
            r"token is \3\)\.", body)
        assert match is not None, body
        first, second = match.group(3), match.group(4)
        boxes = ((first, first), (first, second), (second, second))
        observed = [(box, index) for box in boxes for index in range(2)
                    if box[index] == first]
        favorable = sum(box[1 - index] == first for box, index in observed)
        answer = ptext(Fraction(favorable, len(observed)))
    return {"variant": variant, "query": query, "answer": answer}


class ClassicProbabilityPuzzlesGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(820417)

    def test_output_contract(self):
        example = ClassicProbabilityPuzzlesGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ClassicProbabilityPuzzlesGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_counting_and_fraction_steps_are_exact(self):
        generator = ClassicProbabilityPuzzlesGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            fcp_running = 1
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"\(?([0-9/]+)\)?\^(\d+)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))
                elif fields[0] == "FRAC_BUILD":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
                elif fields[0] == "FCP":
                    fcp_running *= int(fields[2])
                    self.assertEqual(fcp_running, int(fields[3]))

    def test_monty_switch_probability_exceeds_stay(self):
        for variant in ("monty_hall", "monty_hall_n_doors"):
            generator = ClassicProbabilityPuzzlesGenerator(variant)
            for _ in range(120):
                answer = generator.generate()["final_answer"]
                match = re.fullmatch(r"switch; ([0-9/]+) vs ([0-9/]+)", answer)
                self.assertIsNotNone(match)
                self.assertGreater(Fraction(match.group(1)), Fraction(match.group(2)))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ClassicProbabilityPuzzlesGenerator.VARIANTS:
            generator = ClassicProbabilityPuzzlesGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_classic_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ClassicProbabilityPuzzlesGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ClassicProbabilityPuzzlesGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()

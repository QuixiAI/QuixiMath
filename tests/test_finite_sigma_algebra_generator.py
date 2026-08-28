"""Brute-force closure oracle for FiniteSigmaAlgebraGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.finite_sigma_algebra_generator import QUERIES, FiniteSigmaAlgebraGenerator
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_set(text):
    text = text.strip()
    if text == "∅":
        return frozenset()
    return frozenset(map(int, re.findall(r"-?\d+", text)))


def set_text(values):
    values = sorted(values)
    return "∅" if not values else "{" + ", ".join(map(str, values)) + "}"


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def sigma_closure(universe, generators):
    events = {frozenset(), universe, *generators}
    changed = True
    while changed:
        changed = False
        snapshot = list(events)
        candidates = {universe - event for event in snapshot}
        candidates |= {left | right for left in snapshot for right in snapshot}
        if not candidates <= events:
            events |= candidates
            changed = True
    return events


def atoms_of(events):
    nonempty = [event for event in events if event]
    atoms = [event for event in nonempty
             if not any(other < event for other in nonempty)]
    return sorted(atoms, key=lambda event: min(event))


def parse_base(body):
    universe = parse_set(re.search(r"Omega=(\{[^}]+\})", body).group(1))
    match = re.search(r"Let G=sigma\((.*?)\)\.", body)
    generators = [parse_set(value) for value in re.findall(r"\{[^}]+\}|∅",
                                                             match.group(1))]
    events = sigma_closure(universe, generators)
    return universe, generators, events, atoms_of(events)


def parse_mapping(body):
    text = re.search(r"X=([^\.]+)\. Target", body).group(1)
    return {int(key): int(value) for key, value in
            re.findall(r"(\d+):(-?\d+)", text)}


def atoms_answer(atoms):
    return "atoms " + ", ".join(set_text(atom) for atom in atoms)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "sigma_of_random_variable":
        universe = parse_set(re.search(r"Omega=(\{[^}]+\})", body).group(1))
        mapping = parse_mapping(body)
        levels = {frozenset(omega for omega in universe if mapping[omega] == value)
                  for value in set(mapping.values())}
        events = sigma_closure(universe, list(levels))
        atoms = atoms_of(events)
        answer = f"{atoms_answer(atoms)}; {len(events)} events"
    else:
        universe, _, events, atoms = parse_base(body)
        if variant == "generated_sigma_algebra":
            answer = f"{atoms_answer(atoms)}; {len(events)} events"
        elif variant == "measurability_check":
            event = parse_set(re.search(r"Event A=(\{[^}]+\}|∅)", body).group(1))
            if event in events:
                chosen = [atom for atom in atoms if atom <= event]
                answer = ("G-measurable; A is union of atoms "
                          + " and ".join(set_text(atom) for atom in chosen))
            else:
                split = next(atom for atom in atoms if event & atom and not atom <= event)
                answer = f"not G-measurable; A splits atom {set_text(split)}"
        elif variant == "conditional_expectation_atoms":
            mapping = parse_mapping(body)
            averages = [sum((Fraction(mapping[value]) for value in atom), Fraction())
                        / len(atom) for atom in atoms]
            answer = "E[X given G] = " + "; ".join(
                f"{ptext(value)} on {set_text(atom)}"
                for atom, value in zip(atoms, averages))
        else:
            event = parse_set(re.search(r"Event A=(\{[^}]+\}|∅)", body).group(1))
            probabilities = [Fraction(len(event & atom), len(atom)) for atom in atoms]
            answer = "P(A given G) = " + "; ".join(
                f"{ptext(value)} on {set_text(atom)}"
                for atom, value in zip(atoms, probabilities))
    return {"variant": variant, "query": query, "answer": answer}


class FiniteSigmaAlgebraGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240770)

    def test_output_contract(self):
        example = FiniteSigmaAlgebraGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = FiniteSigmaAlgebraGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = FiniteSigmaAlgebraGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))

    def test_plan_partition_example_closure(self):
        universe = frozenset(range(1, 7))
        events = sigma_closure(universe, [frozenset({1, 2}), frozenset({3})])
        atoms = atoms_of(events)
        self.assertEqual(atoms, [frozenset({1, 2}), frozenset({3}),
                                 frozenset({4, 5, 6})])
        self.assertEqual(len(events), 8)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in FiniteSigmaAlgebraGenerator.VARIANTS:
            generator = FiniteSigmaAlgebraGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_finite_sigma_algebra_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FiniteSigmaAlgebraGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = FiniteSigmaAlgebraGenerator()
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

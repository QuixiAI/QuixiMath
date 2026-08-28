"""BFS, SCC, and Boolean-power oracle for state classification."""
import math
import random
import re
import unittest

from generators.markov_state_classification_generator import (
    QUERIES, MarkovStateClassificationGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def set_text(values):
    return "{" + ", ".join(map(str, sorted(values))) + "}"


def parse_graph(body):
    states = list(map(int, re.search(r"states are \{([^}]+)\}", body).group(1).split(", ")))
    edge_text = re.search(r"Positive transitions are (.+?)\. Every listed", body).group(1)
    edges = {tuple(map(int, pair)) for pair in re.findall(r"(\d+)→(\d+)", edge_text)}
    assert all(any(source == state for source, _ in edges) for state in states)
    return states, edges


def reachability(states, edges):
    result = []
    for start in states:
        reached, frontier = {start}, [start]
        while frontier:
            source = frontier.pop()
            for left, right in edges:
                if left == source and right not in reached:
                    reached.add(right)
                    frontier.append(right)
        result.append(reached)
    return result


def classes_of(states, reach):
    remaining = set(states)
    classes = []
    while remaining:
        state = min(remaining)
        component = {other for other in remaining
                     if other in reach[state - 1] and state in reach[other - 1]}
        classes.append(component)
        remaining -= component
    return classes


def return_lengths(states, edges):
    n = len(states)
    adjacency = [[int((row + 1, column + 1) in edges) for column in range(n)]
                 for row in range(n)]
    current = [[int(row == column) for column in range(n)] for row in range(n)]
    lengths = []
    for length in range(1, 4 * n + 1):
        current = [[int(any(current[row][middle] and adjacency[middle][column]
                            for middle in range(n)))
                    for column in range(n)] for row in range(n)]
        if current[0][0]:
            lengths.append(length)
    return lengths


def rows_text(states, reach):
    return "; ".join(f"R{state}=(" + ",".join(
        "1" if target in reach[state - 1] else "0" for target in states) + ")"
        for state in states)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    states, edges = parse_graph(body)
    reach = reachability(states, edges)
    classes = classes_of(states, reach)
    if variant == "communicating_classes":
        answer = "classes " + ", ".join(set_text(c) for c in classes)
    elif variant == "transient_recurrent":
        recurrent = [component for component in classes
                     if all(target in component for source, target in edges
                            if source in component)]
        transient = [component for component in classes if component not in recurrent]
        answer = ("transient classes " + ", ".join(set_text(c) for c in transient)
                  + "; recurrent classes " + ", ".join(set_text(c) for c in recurrent))
    elif variant == "period":
        period = 0
        for length in return_lengths(states, edges):
            period = math.gcd(period, length)
        answer = f"period {period}; class {set_text(states)}"
    elif variant == "absorbing_states":
        absorbing = [state for state in states
                     if {target for source, target in edges if source == state} == {state}]
        nonabsorbing = [state for state in states if state not in absorbing]
        answer = (f"absorbing states {set_text(absorbing)}; nonabsorbing states "
                  f"{set_text(nonabsorbing)}")
    elif variant == "irreducible_check":
        if len(classes) == 1:
            answer = "irreducible yes; all states communicate"
        else:
            answer = "irreducible no; classes " + ", ".join(set_text(c) for c in classes)
    else:
        answer = rows_text(states, reach)
    return {"variant": variant, "query": query, "answer": answer}


class MarkovStateClassificationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240773)

    def test_output_contract(self):
        example = MarkovStateClassificationGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = MarkovStateClassificationGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_reachability_steps_have_reflexive_boolean_rows(self):
        generator = MarkovStateClassificationGenerator()
        for _ in range(200):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "REACH_PASS":
                    rows = re.findall(r"R(\d+)=\(([01,]+)\)", fields[2])
                    self.assertTrue(rows, raw)
                    for state, values in rows:
                        bits = values.split(",")
                        self.assertEqual(bits[int(state) - 1], "1", raw)

    def test_plan_classification_example(self):
        states = [1, 2, 3, 4, 5]
        edges = {(1, 2), (2, 1), (2, 3), (3, 4), (4, 5), (5, 3)}
        classes = classes_of(states, reachability(states, edges))
        self.assertEqual(classes, [{1, 2}, {3, 4, 5}])
        self.assertEqual(math.gcd(*return_lengths([1, 2], {(1, 2), (2, 1)})), 2)
        self.assertEqual(math.gcd(*return_lengths([1, 2, 3],
                                                  {(1, 2), (2, 3), (3, 1)})), 3)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in MarkovStateClassificationGenerator.VARIANTS:
            generator = MarkovStateClassificationGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_markov_state_classification_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MarkovStateClassificationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MarkovStateClassificationGenerator()
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

import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.nfa_simulation_generator import NFASimulationGenerator
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def parse_set(text):
    body = text.strip()[1:-1]
    return set() if not body else set(body.split(","))


def set_text(values):
    values = sorted(values)
    return "{" + ",".join(values) + "}" if values else "{}"


def parse_problem(problem):
    match = re.search(
        r"states ([^;]+); alphabet ([^;]+); start ([^;]+); accepting states "
        r"([^;]+); transitions (.+); input ([ab]+)",
        problem,
    )
    assert match is not None, problem
    states, alphabet, start, accept, trans_text, input_text = match.groups()
    transitions = {}
    epsilons = {}
    for clause in trans_text.split("; "):
        state, entries = clause.split(":", 1)
        for symbol, target_text in re.findall(r"(a|b|epsilon)->(\{[^}]*\})",
                                               entries):
            targets = parse_set(target_text)
            if symbol == "epsilon":
                epsilons[state] = targets
            else:
                transitions[(state, symbol)] = targets
    return {
        "states": states.split(", "),
        "alphabet": alphabet.split(", "),
        "start": start,
        "accept": set(accept.split(", ")) if accept != "none" else set(),
        "transitions": transitions,
        "epsilons": epsilons,
        "input": input_text,
    }


def epsilon_closure(states, epsilons):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for target in epsilons.get(state, set()):
            if target not in closure:
                closure.add(target)
                stack.append(target)
    return closure


def oracle(problem):
    parts = parse_problem(problem)
    active = epsilon_closure({parts["start"]}, parts["epsilons"])
    sets = [set_text(active)]
    for symbol in parts["input"]:
        moved = set()
        for state in active:
            moved.update(parts["transitions"].get((state, symbol), set()))
        active = epsilon_closure(moved, parts["epsilons"])
        sets.append(set_text(active))
    status = "accepted" if active & parts["accept"] else "rejected"
    return f"{status}; sets = {' -> '.join(sets)}"


class TestNFASimulationGenerator(unittest.TestCase):
    def test_contract_oracle_and_pipe_safety(self):
        random.seed(123)
        gen = NFASimulationGenerator()
        saw = set()
        openings = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertNotIn(DELIM, result["final_answer"])
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(";", 1)[0])
        self.assertEqual(saw, {f"nfa_simulation_{v}"
                               for v in NFASimulationGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_explicit_variants(self):
        for variant in NFASimulationGenerator.VARIANTS:
            result = NFASimulationGenerator(variant).generate()
            self.assertEqual(result["operation"], f"nfa_simulation_{variant}")
            self.assertEqual(result["final_answer"], oracle(result["problem"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            NFASimulationGenerator("bad")


if __name__ == "__main__":
    unittest.main()

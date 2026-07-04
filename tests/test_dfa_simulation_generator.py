import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.dfa_simulation_generator import DFASimulationGenerator
from helpers import DELIM


DFA_RE = re.compile(
    r"Simulate the DFA with states ([^;]+); alphabet ([^;]+); start (q\d+); "
    r"accepting states ([^;]+); transitions (.+) on input ([01]+)\. "
    r"Give the state sequence and accept/reject result\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def comma_text(values):
    return ", ".join(values) if values else "none"


def state_path(states):
    return "->".join(states)


def parse_list(text):
    if text == "none":
        return []
    return text.split(", ")


def parse_problem(problem):
    match = DFA_RE.fullmatch(problem)
    assert match is not None, problem
    states_text, alphabet_text, start, accept_text, transition_text, input_string = (
        match.groups()
    )
    states = parse_list(states_text)
    alphabet = parse_list(alphabet_text)
    accept = parse_list(accept_text)
    transitions = {}
    for clause in transition_text.split("; "):
        state, entries_text = clause.split(":")
        for entry in entries_text.split(","):
            symbol, target = entry.split("->")
            transitions[(state, symbol)] = target
    return {
        "states": states,
        "alphabet": alphabet,
        "start": start,
        "accept": accept,
        "transitions": transitions,
        "input": input_string,
    }


def simulate(parts):
    current = parts["start"]
    states = [current]
    for symbol in parts["input"]:
        current = parts["transitions"][(current, symbol)]
        states.append(current)
    status = "accepted" if current in parts["accept"] else "rejected"
    return states, status


def expected_steps(example):
    parts = parse_problem(example["problem"])
    steps = [
        make_step("DFA_SETUP", f"states {comma_text(parts['states'])}",
                  f"alphabet {comma_text(parts['alphabet'])}",
                  f"start {parts['start']}"),
        make_step("DFA_ACCEPT", comma_text(parts["accept"])),
    ]
    for state in parts["states"]:
        for symbol in parts["alphabet"]:
            steps.append(make_step("DFA_TRANSITION", state, symbol,
                                   parts["transitions"][(state, symbol)]))
    steps.extend([
        make_step("DFA_INPUT", parts["input"]),
        make_step("DFA_STATE", "start", parts["start"]),
    ])

    current = parts["start"]
    seen_states = [current]
    for pos, symbol in enumerate(parts["input"], start=1):
        next_state = parts["transitions"][(current, symbol)]
        steps.append(make_step("DFA_READ", f"pos {pos}", symbol))
        steps.append(make_step("DFA_STEP", current, symbol, next_state))
        current = next_state
        seen_states.append(current)
        steps.append(make_step("DFA_STATE", f"after {pos}",
                               state_path(seen_states)))

    status = "accepted" if current in parts["accept"] else "rejected"
    steps.append(make_step("CHECK", f"{current} in accepting states", status))
    answer = f"{status}; states = {state_path(seen_states)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestDFASimulationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DFASimulationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            steps, answer = expected_steps(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], steps, result["problem"])

    def test_accept_reject_matches_final_state(self):
        saw = set()
        for _ in range(500):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            states, status = simulate(parts)
            saw.add(status)
            self.assertEqual(result["final_answer"],
                             f"{status}; states = {state_path(states)}")
        self.assertEqual(saw, {"accepted", "rejected"})

    def test_variants_are_available(self):
        for variant in ("even_zeros", "ends_with_one", "contains_11"):
            gen = DFASimulationGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"dfa_simulation_{variant}")
                parse_problem(result["problem"])

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DFASimulationGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

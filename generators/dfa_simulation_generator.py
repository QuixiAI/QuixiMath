import random

from base_generator import ProblemGenerator
from helpers import step, jid


ALPHABET = ["0", "1"]


def comma_text(values):
    return ", ".join(values) if values else "none"


def state_path(states):
    return "->".join(states)


def transition_text(states, transitions):
    clauses = []
    for state in states:
        entries = [
            f"{symbol}->{transitions[(state, symbol)]}"
            for symbol in ALPHABET
        ]
        clauses.append(f"{state}:{','.join(entries)}")
    return "; ".join(clauses)


TEMPLATES = {
    "even_zeros": dict(
        states=["q0", "q1"],
        start="q0",
        accept=["q0"],
        transitions={
            ("q0", "0"): "q1",
            ("q0", "1"): "q0",
            ("q1", "0"): "q0",
            ("q1", "1"): "q1",
        },
    ),
    "ends_with_one": dict(
        states=["q0", "q1"],
        start="q0",
        accept=["q1"],
        transitions={
            ("q0", "0"): "q0",
            ("q0", "1"): "q1",
            ("q1", "0"): "q0",
            ("q1", "1"): "q1",
        },
    ),
    "contains_11": dict(
        states=["q0", "q1", "q2"],
        start="q0",
        accept=["q2"],
        transitions={
            ("q0", "0"): "q0",
            ("q0", "1"): "q1",
            ("q1", "0"): "q0",
            ("q1", "1"): "q2",
            ("q2", "0"): "q2",
            ("q2", "1"): "q2",
        },
    ),
}


class DFASimulationGenerator(ProblemGenerator):
    """
    DFA simulation with a complete state-sequence trace.

    Variants:
    - even_zeros: accepts strings with an even number of 0s
    - ends_with_one: accepts strings ending in 1
    - contains_11: accepts strings containing the substring 11

    Op-codes used:
    - DFA_SETUP / DFA_ACCEPT / DFA_TRANSITION / DFA_INPUT: automaton setup
    - DFA_STATE / DFA_READ / DFA_STEP: per-symbol simulation trace
    - CHECK: final accepting-state check
    - Z: accept/reject result and state sequence
    """

    VARIANTS = ["even_zeros", "ends_with_one", "contains_11"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        spec = TEMPLATES[variant]
        states = spec["states"]
        start = spec["start"]
        accept = spec["accept"]
        transitions = spec["transitions"]
        input_string = "".join(random.choice(ALPHABET)
                               for _ in range(random.randint(4, 8)))

        steps = [
            step("DFA_SETUP", f"states {comma_text(states)}",
                 f"alphabet {comma_text(ALPHABET)}", f"start {start}"),
            step("DFA_ACCEPT", comma_text(accept)),
        ]
        for state in states:
            for symbol in ALPHABET:
                steps.append(step("DFA_TRANSITION", state, symbol,
                                  transitions[(state, symbol)]))
        steps.extend([
            step("DFA_INPUT", input_string),
            step("DFA_STATE", "start", start),
        ])

        current = start
        seen_states = [current]
        for pos, symbol in enumerate(input_string, start=1):
            next_state = transitions[(current, symbol)]
            steps.append(step("DFA_READ", f"pos {pos}", symbol))
            steps.append(step("DFA_STEP", current, symbol, next_state))
            current = next_state
            seen_states.append(current)
            steps.append(step("DFA_STATE", f"after {pos}",
                              state_path(seen_states)))

        status = "accepted" if current in accept else "rejected"
        steps.append(step("CHECK", f"{current} in accepting states", status))
        answer = f"{status}; states = {state_path(seen_states)}"
        problem = (
            f"Simulate the DFA with states {comma_text(states)}; alphabet "
            f"{comma_text(ALPHABET)}; start {start}; accepting states "
            f"{comma_text(accept)}; transitions "
            f"{transition_text(states, transitions)} on input {input_string}. "
            f"Give the state sequence and accept/reject result."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"dfa_simulation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

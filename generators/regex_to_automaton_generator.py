import random

from base_generator import ProblemGenerator
from helpers import step, jid


ALPHABET = ["a", "b"]


AUTOMATA = {
    "a_star_b": {
        "regex": "a*b",
        "states": ["q0", "q1", "qd"],
        "start": "q0",
        "accept": ["q1"],
        "transitions": {
            ("q0", "a"): "q0", ("q0", "b"): "q1",
            ("q1", "a"): "qd", ("q1", "b"): "qd",
            ("qd", "a"): "qd", ("qd", "b"): "qd",
        },
        "notes": [("q0", "still reading a*"), ("q1", "final b consumed"),
                  ("qd", "dead state")],
    },
    "contains_ab": {
        "regex": "(a|b)*ab(a|b)*",
        "states": ["q0", "q1", "q2"],
        "start": "q0",
        "accept": ["q2"],
        "transitions": {
            ("q0", "a"): "q1", ("q0", "b"): "q0",
            ("q1", "a"): "q1", ("q1", "b"): "q2",
            ("q2", "a"): "q2", ("q2", "b"): "q2",
        },
        "notes": [("q0", "no useful suffix"), ("q1", "suffix a"),
                  ("q2", "seen ab")],
    },
    "ends_ab_or_ba": {
        "regex": "(a|b)*(ab|ba)",
        "states": ["q0", "q1", "q2", "q3", "q4"],
        "start": "q0",
        "accept": ["q3", "q4"],
        "transitions": {
            ("q0", "a"): "q1", ("q0", "b"): "q2",
            ("q1", "a"): "q1", ("q1", "b"): "q3",
            ("q2", "a"): "q4", ("q2", "b"): "q2",
            ("q3", "a"): "q4", ("q3", "b"): "q2",
            ("q4", "a"): "q1", ("q4", "b"): "q3",
        },
        "notes": [("q0", "start"), ("q1", "last char a"),
                  ("q2", "last char b"), ("q3", "ends ab"),
                  ("q4", "ends ba")],
    },
}


PROBLEM_TEMPLATES = [
    ("Convert regex {regex} over alphabet a,b to the canonical progress DFA. "
     "Name states as listed by the construction and include all transitions."),
    ("Build the direct DFA for regular expression {regex} over alphabet a,b. "
     "Report start, accepting states, and transition table."),
    ("Using progress states, construct a DFA for {regex} on alphabet a,b."),
]


def list_text(values):
    return ", ".join(values)


def transition_answer(states, transitions):
    rows = []
    for state in states:
        rows.append(
            f"{state}:a->{transitions[(state, 'a')]},b->{transitions[(state, 'b')]}"
        )
    return "; ".join(rows)


def step_regex_text(regex):
    return regex.replace("|", " or ")


class RegexToAutomatonGenerator(ProblemGenerator):
    """
    Direct DFA construction for small regular expressions.

    The problem fixes canonical progress-state names, giving a unique table.

    Op-codes used:
    - REGEX_SETUP / REGEX_STATE / REGEX_TRANSITION / REGEX_ACCEPT
    - CHECK
    - Z: start, accepting states, and complete transition table
    """

    VARIANTS = ["a_star_b", "contains_ab", "ends_ab_or_ba"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        spec = AUTOMATA[variant]
        states = spec["states"]
        transitions = spec["transitions"]
        steps = [
            step("REGEX_SETUP", step_regex_text(spec["regex"]), "alphabet a,b",
                 "canonical progress DFA"),
        ]
        for state, meaning in spec["notes"]:
            steps.append(step("REGEX_STATE", state, meaning))
        steps.append(step("REGEX_ACCEPT", list_text(spec["accept"])))
        for state in states:
            for symbol in ALPHABET:
                steps.append(step("REGEX_TRANSITION", state, symbol,
                                  transitions[(state, symbol)]))
        table = transition_answer(states, transitions)
        answer = (
            f"start={spec['start']}; accept={list_text(spec['accept'])}; "
            f"transitions={table}"
        )
        steps.append(step("CHECK", "complete table", f"{len(states)} states"))
        problem = random.choice(PROBLEM_TEMPLATES).format(regex=spec["regex"])
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"regex_to_automaton_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

import random

from base_generator import ProblemGenerator
from helpers import step, jid


ALPHABET = ["a", "b"]


def set_text(values):
    ordered = sorted(values)
    return "{" + ",".join(ordered) + "}" if ordered else "{}"


def list_text(values):
    return ", ".join(values) if values else "none"


def transition_text(states, transitions, epsilons):
    clauses = []
    for state in states:
        entries = []
        for symbol in ALPHABET:
            targets = transitions.get((state, symbol), set())
            entries.append(f"{symbol}->{set_text(targets)}")
        if epsilons.get(state):
            entries.append(f"epsilon->{set_text(epsilons[state])}")
        clauses.append(f"{state}:{','.join(entries)}")
    return "; ".join(clauses)


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


TEMPLATES = {
    "ends_with_ab": dict(
        states=["q0", "q1", "q2"],
        start="q0",
        accept=["q2"],
        transitions={
            ("q0", "a"): {"q0", "q1"},
            ("q0", "b"): {"q0"},
            ("q1", "b"): {"q2"},
        },
        epsilons={},
        inputs=["ab", "aab", "babab", "abba", "baab"],
    ),
    "contains_ab": dict(
        states=["q0", "q1", "q2"],
        start="q0",
        accept=["q2"],
        transitions={
            ("q0", "a"): {"q0", "q1"},
            ("q0", "b"): {"q0"},
            ("q1", "b"): {"q2"},
            ("q2", "a"): {"q2"},
            ("q2", "b"): {"q2"},
        },
        epsilons={},
        inputs=["baab", "bbbb", "aaba", "baba", "aaab"],
    ),
    "epsilon_optional_a": dict(
        states=["q0", "q1", "q2"],
        start="q0",
        accept=["q2"],
        transitions={
            ("q0", "a"): {"q1"},
            ("q1", "b"): {"q2"},
            ("q2", "b"): {"q2"},
        },
        epsilons={"q0": {"q1"}},
        inputs=["b", "ab", "abb", "a", "bbab"],
    ),
}


PROBLEM_TEMPLATES = [
    ("Run the NFA with states {states}; alphabet {alphabet}; start {start}; "
     "accepting states {accept}; transitions {transitions}; input {input}. "
     "List the active-state sets after each symbol and give the result."),
    ("Trace active states for this NFA: states {states}; alphabet {alphabet}; "
     "start {start}; accepting states {accept}; transitions {transitions}; "
     "input {input}. Decide accept or reject."),
    ("For the NFA described by states {states}; alphabet {alphabet}; start "
     "{start}; accepting states {accept}; transitions {transitions}; input "
     "{input}, compute each active set and the final decision."),
]


class NFASimulationGenerator(ProblemGenerator):
    """
    NFA and epsilon-NFA simulation with active-state-set traces.

    Variants:
    - ends_with_ab: nondeterministically guesses the final "ab" suffix
    - contains_ab: keeps an accepting state once "ab" has appeared
    - epsilon_optional_a: uses an epsilon edge to make the initial "a" optional

    Op-codes used:
    - NFA_SETUP / NFA_ACCEPT / NFA_TRANSITION / NFA_EPSILON / NFA_INPUT
    - EPS_CLOSURE / NFA_ACTIVE / NFA_READ / NFA_MOVE
    - CHECK: final active-set intersection with accepting states
    - Z: deterministic active-set trace and accept/reject result
    """

    VARIANTS = ["ends_with_ab", "contains_ab", "epsilon_optional_a"]

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
        epsilons = spec["epsilons"]
        input_string = random.choice(spec["inputs"])

        steps = [
            step("NFA_SETUP", f"states {list_text(states)}",
                 f"alphabet {list_text(ALPHABET)}", f"start {start}"),
            step("NFA_ACCEPT", list_text(accept)),
        ]
        for state in states:
            for symbol in ALPHABET:
                targets = transitions.get((state, symbol), set())
                steps.append(step("NFA_TRANSITION", state, symbol,
                                  set_text(targets)))
            if epsilons.get(state):
                steps.append(step("NFA_EPSILON", state,
                                  set_text(epsilons[state])))

        active = epsilon_closure({start}, epsilons)
        active_sets = [set_text(active)]
        steps.extend([
            step("NFA_INPUT", input_string),
            step("EPS_CLOSURE", set_text({start}), set_text(active)),
            step("NFA_ACTIVE", "start", set_text(active)),
        ])

        for pos, symbol in enumerate(input_string, start=1):
            moved = set()
            pieces = []
            for state in sorted(active):
                targets = transitions.get((state, symbol), set())
                moved.update(targets)
                pieces.append(f"{state}->{set_text(targets)}")
            move_text = "; ".join(pieces) if pieces else "none"
            closed = epsilon_closure(moved, epsilons)
            steps.append(step("NFA_READ", f"pos {pos}", symbol))
            steps.append(step("NFA_MOVE", set_text(active), symbol,
                              move_text, set_text(moved)))
            steps.append(step("EPS_CLOSURE", set_text(moved),
                              set_text(closed)))
            active = closed
            active_sets.append(set_text(active))
            steps.append(step("NFA_ACTIVE", f"after {pos}",
                              set_text(active)))

        accepting_seen = sorted(set(active) & set(accept))
        status = "accepted" if accepting_seen else "rejected"
        steps.append(step("CHECK", f"active ∩ accept = {list_text(accepting_seen)}",
                          status))
        answer = f"{status}; sets = {' -> '.join(active_sets)}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            states=list_text(states),
            alphabet=list_text(ALPHABET),
            start=start,
            accept=list_text(accept),
            transitions=transition_text(states, transitions, epsilons),
            input=input_string,
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"nfa_simulation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

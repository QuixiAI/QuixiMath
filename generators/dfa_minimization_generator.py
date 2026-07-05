import random

from base_generator import ProblemGenerator
from helpers import step, jid


ALPHABET = ["0", "1"]


def list_text(values):
    return ", ".join(values) if values else "none"


def block_text(block):
    return "{" + ",".join(sorted(block)) + "}"


def partition_text(partition):
    return ", ".join(block_text(block) for block in partition)


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
    "ends_with_one_clones": dict(
        states=["A", "B", "C", "D"],
        start="A",
        accept=["B", "D"],
        transitions={
            ("A", "0"): "C", ("A", "1"): "B",
            ("B", "0"): "C", ("B", "1"): "B",
            ("C", "0"): "C", ("C", "1"): "D",
            ("D", "0"): "C", ("D", "1"): "D",
        },
    ),
    "two_accept_clones": dict(
        states=["A", "B", "C"],
        start="A",
        accept=["B", "C"],
        transitions={
            ("A", "0"): "A", ("A", "1"): "B",
            ("B", "0"): "C", ("B", "1"): "B",
            ("C", "0"): "C", ("C", "1"): "B",
        },
    ),
    "all_distinct": dict(
        states=["A", "B", "C"],
        start="A",
        accept=["C"],
        transitions={
            ("A", "0"): "A", ("A", "1"): "B",
            ("B", "0"): "C", ("B", "1"): "B",
            ("C", "0"): "C", ("C", "1"): "C",
        },
    ),
}


PROBLEM_TEMPLATES = [
    ("Minimize the DFA with states {states}; alphabet {alphabet}; start "
     "{start}; accepting states {accept}; transitions {transitions}. Give "
     "the final state blocks and transition table."),
    ("Use partition refinement to minimize this DFA: states {states}; "
     "alphabet {alphabet}; start {start}; accepting states {accept}; "
     "transitions {transitions}."),
    ("For the DFA states {states}; alphabet {alphabet}; start {start}; "
     "accepting states {accept}; transitions {transitions}, find the "
     "minimal equivalent DFA."),
]


def block_index(partition, state):
    for idx, block in enumerate(partition):
        if state in block:
            return idx
    raise ValueError(state)


def normalize_partition(blocks):
    normalized = [tuple(sorted(block)) for block in blocks if block]
    return sorted(normalized, key=lambda block: block[0])


def refine_partition(states, transitions, partition):
    groups = {}
    for state in states:
        signature = tuple(
            block_index(partition, transitions[(state, symbol)])
            for symbol in ALPHABET
        )
        key = (block_index(partition, state), signature)
        groups.setdefault(key, []).append(state)
    return normalize_partition(groups.values())


class DFAMinimizationGenerator(ProblemGenerator):
    """
    DFA minimization by table-free partition refinement.

    Variants:
    - ends_with_one_clones: two pairs of equivalent states collapse
    - two_accept_clones: two accepting states collapse
    - all_distinct: refinement proves all states stay separate

    Op-codes used:
    - DFA_MIN_SETUP / DFA_MIN_TRANSITION: automaton description
    - MIN_INITIAL / MIN_SIGNATURE / MIN_REFINE / MIN_STABLE: refinement trace
    - MIN_STATE / MIN_TRANSITION / CHECK: minimized DFA construction
    - Z: blocks, start block, accepting blocks, and transitions
    """

    VARIANTS = ["ends_with_one_clones", "two_accept_clones", "all_distinct"]

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

        steps = [
            step("DFA_MIN_SETUP", f"states {list_text(states)}",
                 f"alphabet {list_text(ALPHABET)}", f"start {start}"),
            step("DFA_ACCEPT", list_text(accept)),
        ]
        for state in states:
            for symbol in ALPHABET:
                steps.append(step("DFA_MIN_TRANSITION", state, symbol,
                                  transitions[(state, symbol)]))

        non_accept = [s for s in states if s not in accept]
        partition = normalize_partition([non_accept, accept])
        steps.append(step("MIN_INITIAL", f"nonaccept {list_text(non_accept)}",
                          f"accept {list_text(accept)}",
                          partition_text(partition)))

        round_no = 1
        while True:
            for state in states:
                sig = ",".join(
                    f"{symbol}->B{block_index(partition, transitions[(state, symbol)])}"
                    for symbol in ALPHABET
                )
                steps.append(step("MIN_SIGNATURE", f"round {round_no}",
                                  state, sig))
            refined = refine_partition(states, transitions, partition)
            steps.append(step("MIN_REFINE", f"round {round_no}",
                              partition_text(refined)))
            if refined == partition:
                steps.append(step("MIN_STABLE", partition_text(partition)))
                break
            partition = refined
            round_no += 1

        block_names = {block: block_text(block) for block in partition}
        accepting_blocks = [
            block for block in partition if set(block) & set(accept)
        ]
        start_block = partition[block_index(partition, start)]
        min_transitions = []
        for block in partition:
            representative = block[0]
            pieces = []
            for symbol in ALPHABET:
                target = transitions[(representative, symbol)]
                target_block = partition[block_index(partition, target)]
                pieces.append(f"{symbol}->{block_names[target_block]}")
                steps.append(step("MIN_TRANSITION", block_names[block],
                                  symbol, block_names[target_block]))
            min_transitions.append(f"{block_names[block]}:{','.join(pieces)}")
            steps.append(step("CHECK", f"representative {representative}",
                              ",".join(pieces)))

        answer = (
            f"blocks = {partition_text(partition)}; "
            f"start = {block_names[start_block]}; "
            f"accepting = {partition_text(accepting_blocks)}; "
            f"transitions = {'; '.join(min_transitions)}"
        )
        problem = random.choice(PROBLEM_TEMPLATES).format(
            states=list_text(states),
            alphabet=list_text(ALPHABET),
            start=start,
            accept=list_text(accept),
            transitions=transition_text(states, transitions),
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"dfa_minimization_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

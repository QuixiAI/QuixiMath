import random

from base_generator import ProblemGenerator
from helpers import step, jid


BLANK = "_"


MACHINES = {
    "unary_increment": {
        "inputs": ["1", "11", "111", "1111"],
        "rules": {
            ("q0", "1"): ("q0", "1", "R"),
            ("q0", BLANK): ("qH", "1", "S"),
        },
    },
    "binary_flip": {
        "inputs": ["0", "1", "101", "0011", "1100"],
        "rules": {
            ("q0", "0"): ("q0", "1", "R"),
            ("q0", "1"): ("q0", "0", "R"),
            ("q0", BLANK): ("qH", BLANK, "S"),
        },
    },
    "erase_ones": {
        "inputs": ["1", "11", "111", "1111"],
        "rules": {
            ("q0", "1"): ("q0", BLANK, "R"),
            ("q0", BLANK): ("qH", BLANK, "S"),
        },
    },
}


PROBLEM_TEMPLATES = [
    ("Run bounded TM {name} on input {input} for at most {limit} steps. "
     "Rules: {rules}. Blank is _. Report final status, state, trimmed tape, "
     "and head position."),
    ("Trace the Turing machine {name}: input {input}, step bound {limit}, "
     "blank _. Rules: {rules}. Give the final configuration."),
    ("Starting with input {input}, execute TM {name} for no more than {limit} "
     "steps using rules {rules}. Return status, state, tape, and head."),
]


def rules_text(rules):
    return "; ".join(
        f"{state},{read}->{new_state},{write},{move}"
        for (state, read), (new_state, write, move) in sorted(rules.items())
    )


def tape_text(tape):
    last = -1
    for idx, symbol in enumerate(tape):
        if symbol != BLANK:
            last = idx
    if last < 0:
        return BLANK
    return "".join(tape[:last + 1])


class TuringMachineTraceGenerator(ProblemGenerator):
    """
    Bounded deterministic Turing-machine execution on short inputs.

    Variants:
    - unary_increment: scan right, write one more 1, halt
    - binary_flip: flip bits until blank, halt
    - erase_ones: replace all 1s by blanks, halt

    Op-codes used:
    - TM_SETUP / TM_RULE / TM_CONFIG / TM_READ / TM_WRITE / TM_MOVE
    - TM_HALT / CHECK
    - Z: final status, state, trimmed tape, and head position
    """

    VARIANTS = ["unary_increment", "binary_flip", "erase_ones"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        spec = MACHINES[variant]
        input_text = random.choice(spec["inputs"])
        limit = len(input_text) + 3
        rules = spec["rules"]
        tape = list(input_text) + [BLANK] * (limit + 2)
        head = 0
        state = "q0"
        steps = [
            step("TM_SETUP", variant, f"input={input_text}", f"limit={limit}"),
        ]
        for (old_state, read), (new_state, write, move) in sorted(rules.items()):
            steps.append(step("TM_RULE", f"{old_state},{read}",
                              f"{new_state},{write},{move}"))
        for count in range(limit + 1):
            steps.append(step("TM_CONFIG", f"step {count}", f"state={state}",
                              f"head={head}", f"tape={tape_text(tape)}"))
            if state == "qH":
                steps.append(step("TM_HALT", f"step {count}", "halted"))
                break
            if count == limit:
                break
            read = tape[head] if 0 <= head < len(tape) else BLANK
            new_state, write, move = rules[(state, read)]
            steps.append(step("TM_READ", f"head={head}", read))
            tape[head] = write
            steps.append(step("TM_WRITE", f"head={head}", write))
            old_head = head
            if move == "R":
                head += 1
            elif move == "L":
                head -= 1
            steps.append(step("TM_MOVE", old_head, move, head))
            state = new_state
        status = "halted" if state == "qH" else "bounded"
        trimmed = tape_text(tape)
        steps.append(step("CHECK", status, f"state={state}",
                          f"tape={trimmed}"))
        answer = f"{status}; state={state}; tape={trimmed}; head={head}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            name=variant,
            input=input_text,
            limit=limit,
            rules=rules_text(rules),
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"turing_machine_trace_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

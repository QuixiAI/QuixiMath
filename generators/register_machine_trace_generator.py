"""Register-machine traces, one step per executed instruction (depth strand).

Strand S of ``plans/depth_plan.md``. Programs come from a bank of
Minsky-style shapes (test-and-decrement, increment, halt) whose
termination and exact execution length are certain by construction:

- ``transfer``:      drain r2 into r1            (2*b + 1 steps)
- ``double_move``:   drain r2 into r1 twice over (3*b + 1 steps)
- ``drain_pair``:    drain r1 and r2 together into r3 (3*a + 1 steps,
                     a < b so r1 empties first)

Registers stay below ~600 forever. Each executed instruction is one
chained ``RM_STEP`` (previous register state first, the instruction in
the middle, new state last); a failing DEC (register already zero)
executes as a step whose state is unchanged.

Variants:

- ``final_registers``: the register state at halt.
- ``halting_step``: how many instructions execute before HALT.
- ``trace_invariant``: milestones at every tier carry the program's
  conserved quantity. A milestone can fire mid-unit (after a DEC,
  before its matching INC), so the invariant is program-counter-aware:
  base quantity plus a per-label in-flight adjustment, true at EVERY
  step. The answer states the final registers and the conserved value.

Op-codes: ``RM_STEP`` (new), ``MILESTONE``, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, MILESTONE_SPACING, TIER_FLOORS, pick_tier,
                          tier_difficulty, tier_target)

DEPTH = True

PROMPTS = {
    "final_registers": (
        "Run this register machine from {init} (step states are written "
        "({order};label)) until it halts (at most "
        "{cap} instructions): {program}. What are the final register "
        "values?",
        "Execute the program {program} starting at {init} (step states "
        "({order};label)), one "
        "instruction at a time (at most {cap} instructions). Report the "
        "registers at halt.",
        "Trace the register machine {program} from the state {init} to "
        "its HALT (at most {cap} instructions). Give the final "
        "registers.",
        "Step the machine {program} from {init} until HALT (at most "
        "{cap} instructions) and state the final register values.",
    ),
    "halting_step": (
        "Run this register machine from {init} (step states are written "
        "({order};label)) until it halts (at most "
        "{cap} instructions): {program}. How many instructions execute "
        "before HALT?",
        "Execute the program {program} starting at {init} (at most {cap} "
        "instructions). Count the instructions executed.",
        "Trace the register machine {program} from the state {init} (at "
        "most {cap} instructions). After how many executed instructions "
        "does it halt?",
        "Step the machine {program} from {init} to HALT (at most {cap} "
        "instructions) and report the executed-instruction count.",
    ),
    "trace_invariant": (
        "Run this register machine from {init} (step states are written "
        "({order};label)) until it halts (at most "
        "{cap} instructions): {program}. The quantity {invariant} is "
        "conserved; report the final registers and its value.",
        "Execute the program {program} starting at {init} (at most {cap} "
        "instructions), tracking the conserved quantity {invariant}. "
        "Give the final registers and the conserved value.",
        "Trace {program} from {init} to HALT (at most {cap} "
        "instructions); {invariant} never changes. State the final "
        "registers and that value.",
        "Step the machine {program} from {init} until HALT (at most "
        "{cap} instructions). Report the final registers and the "
        "conserved {invariant}.",
    ),
}

#: shape -> (program lines, invariant text, base fn, per-label in-flight
#: adjustment, sizing). The adjusted invariant base + adjust[pc] is
#: conserved at EVERY step, including mid-unit.
SHAPES = {
    "transfer": (
        ("L1: DEC r2 -> L2 else L3", "L2: INC r1 -> L1", "L3: HALT"),
        "r1 + r2 (+1 while at L2)",
        lambda regs: regs["r1"] + regs["r2"],
        {"L2": 1},
        lambda target, rng: {"r1": rng.randint(0, 300),
                             "r2": max(1, (target - 1) // 2)},
    ),
    "double_move": (
        ("L1: DEC r2 -> L2 else L4", "L2: INC r1 -> L3",
         "L3: INC r1 -> L1", "L4: HALT"),
        "r1 + 2*r2 (+2 at L2, +1 at L3)",
        lambda regs: regs["r1"] + 2 * regs["r2"],
        {"L2": 2, "L3": 1},
        lambda target, rng: {"r1": rng.randint(0, 300),
                             "r2": max(1, (target - 1) // 3)},
    ),
    "drain_pair": (
        ("L1: DEC r1 -> L2 else L4", "L2: DEC r2 -> L3 else L4",
         "L3: INC r3 -> L1", "L4: HALT"),
        "r1 + r3 (+1 at L2 or L3)",
        lambda regs: regs["r1"] + regs["r3"],
        {"L2": 1, "L3": 1},
        lambda target, rng: (lambda a: {"r1": a,
                                        "r2": a + rng.randint(5, 300),
                                        "r3": rng.randint(0, 200)})(
            max(1, (target - 1) // 3)),
    ),
}


def _reg_txt(regs):
    return "(" + ", ".join(f"{name}={regs[name]}"
                           for name in sorted(regs)) + ")"


def _state_txt(state):
    """Compact positional render — RM_STEP rows must stay ~55 chars so a
    d200 trace fits the 16k record cap; the problem header declares the
    tuple order."""
    regs, pc = state
    values = ",".join(str(regs[name]) for name in sorted(regs))
    return f"({values};{pc})"


def _parse_line(line):
    """'L1: DEC r2 -> L2 else L3' -> (label, op, reg, goto, else_goto)."""
    label, body = line.split(": ", 1)
    if body == "HALT":
        return label, "HALT", None, None, None
    parts = body.split(" ")
    op, reg = parts[0], parts[1]
    goto = parts[3]
    else_goto = parts[5] if len(parts) > 5 else None
    return label, op, reg, goto, else_goto


def run_program(lines, regs, chain=None, limit=2000):
    """(executed, final regs). With ``chain``, emits RM_STEP per step;
    the chain state is (registers, pc) so milestones can apply the
    per-label in-flight adjustment."""
    table = {label: (op, reg, goto, other)
             for label, op, reg, goto, other in map(_parse_line, lines)}
    regs = dict(regs)
    pc = _parse_line(lines[0])[0]
    executed = 0
    while True:
        op, reg, goto, other = table[pc]
        if op == "HALT":
            return executed, regs
        executed += 1
        if op == "INC":
            regs[reg] += 1
            note = f"{pc}: INC {reg} -> {goto}"
            pc = goto
        else:  # DEC: test-and-decrement
            if regs[reg] > 0:
                regs[reg] -= 1
                note = f"{pc}: DEC {reg} pos -> {goto}"
                pc = goto
            else:
                note = f"{pc}: DEC {reg} zero -> {other}"
                pc = other
        if chain is not None:
            chain.apply("RM_STEP", note, (dict(regs), pc))
        if executed > limit:  # pragma: no cover - shapes terminate
            raise ValueError("program failed to halt")


class RegisterMachineTraceGenerator(ProblemGenerator):
    """Tier-length register-machine executions (depth strand)."""

    VARIANTS = ("final_registers", "halting_step", "trace_invariant")
    BASE_DIFFICULTY = 3

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and tier not in ("d50", "d100", "d200"):
            raise ValueError("tier must be d50, d100, d200, or None")
        self.variant = variant
        self.tier = tier

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        tier = self.tier or pick_tier()
        target = tier_target(tier)
        if tier == "d200":
            target = min(target, 230)  # compact rows x 245 stay under 16k
        lo, hi = TIER_FLOORS[tier], target + 15

        for _ in range(200):
            shape = random.choice(sorted(SHAPES))
            lines, inv_txt, inv_fn, adjust, sizing = SHAPES[shape]
            # jitter the sizing target: the //2 and //3 formulas can
            # round to one-below-floor when the target sits exactly on it
            t = random.randint(lo + 3, hi - 10)
            regs0 = sizing(t, random)
            executed, final = run_program(lines, regs0)
            if lo <= executed <= hi:
                break
        else:  # pragma: no cover - sizing lands in-window directly
            raise ValueError("no program shape fit the tier")

        milestone = True if (tier != "d50"
                             or variant == "trace_invariant") else None
        start_label = lines[0].split(":", 1)[0]
        chain = Chain((dict(regs0), start_label), render=_state_txt,
                      milestone_spacing=(MILESTONE_SPACING
                                         if milestone else None))
        chain.set_invariant(
            inv_txt,
            lambda state, k: inv_fn(state[0]) + adjust.get(state[1], 0))
        run_program(lines, regs0, chain=chain)

        conserved = inv_fn(regs0)
        cap = ((executed + 24) // 25) * 25
        program = "; ".join(lines)
        init = _reg_txt(regs0)
        if variant == "final_registers":
            answer = _reg_txt(final)
        elif variant == "halting_step":
            answer = str(executed)
        else:
            answer = f"{_reg_txt(final)}; {inv_txt} = {conserved} conserved"
        problem = random.choice(PROMPTS[variant]).format(
            program=program, init=init, cap=cap, invariant=inv_txt,
            order=",".join(sorted(regs0)))
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"register_machine_trace_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )

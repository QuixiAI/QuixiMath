import random

from base_generator import ProblemGenerator
from helpers import step, jid


QUANTITIES = ["Q", "B", "Le", "Lmu"]
PARTICLES = {
    "n": {"Q": 0, "B": 1, "Le": 0, "Lmu": 0},
    "p": {"Q": 1, "B": 1, "Le": 0, "Lmu": 0},
    "anti_p": {"Q": -1, "B": -1, "Le": 0, "Lmu": 0},
    "e-": {"Q": -1, "B": 0, "Le": 1, "Lmu": 0},
    "e+": {"Q": 1, "B": 0, "Le": -1, "Lmu": 0},
    "nu_e": {"Q": 0, "B": 0, "Le": 1, "Lmu": 0},
    "anti_nu_e": {"Q": 0, "B": 0, "Le": -1, "Lmu": 0},
    "mu-": {"Q": -1, "B": 0, "Le": 0, "Lmu": 1},
    "mu+": {"Q": 1, "B": 0, "Le": 0, "Lmu": -1},
    "nu_mu": {"Q": 0, "B": 0, "Le": 0, "Lmu": 1},
    "anti_nu_mu": {"Q": 0, "B": 0, "Le": 0, "Lmu": -1},
    "pi+": {"Q": 1, "B": 0, "Le": 0, "Lmu": 0},
    "pi-": {"Q": -1, "B": 0, "Le": 0, "Lmu": 0},
    "pi0": {"Q": 0, "B": 0, "Le": 0, "Lmu": 0},
    "gamma": {"Q": 0, "B": 0, "Le": 0, "Lmu": 0},
}

BASE_REACTIONS = [
    (["n"], ["p", "e-", "anti_nu_e"]),
    (["mu-"], ["e-", "anti_nu_e", "nu_mu"]),
    (["e+", "e-"], ["gamma", "gamma"]),
    (["p", "anti_p"], ["pi+", "pi-"]),
    (["pi+"], ["mu+", "nu_mu"]),
    (["n"], ["p", "e-", "nu_e"]),
    (["p"], ["e+", "gamma"]),
    (["p", "anti_p"], ["pi+", "pi0"]),
    (["mu-"], ["e-", "anti_nu_mu", "nu_e"]),
]
NEUTRALS = ["gamma", "pi0"]


def format_reaction(left, right):
    return f"{' + '.join(left)} -> {' + '.join(right)}"


def unique_in_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def table_text(particles):
    entries = []
    for name in particles:
        qn = PARTICLES[name]
        entries.append(
            f"{name}(Q={qn['Q']},B={qn['B']},Le={qn['Le']},"
            f"Lmu={qn['Lmu']})"
        )
    return "; ".join(entries)


def side_total(side, quantity):
    return sum(PARTICLES[name][quantity] for name in side)


def signed_change(value):
    return f"+{value}" if value > 0 else str(value)


class ConservationLawGenerator(ProblemGenerator):
    """
    Charge, baryon number, and lepton-family bookkeeping for reactions.

    The problem supplies every particle's quantum numbers, so the task is
    arithmetic audit rather than lookup. Final answers include the first
    failing conservation reason(s), not just yes/no.

    Op-codes used:
    - CONSERVATION_SETUP: reaction and quantities checked
    - PARTICLE_TABLE: supplied particle quantum numbers
    - QN_ADD: cumulative addition for one quantum number on one side
    - CONSERVE_CHECK: compare left and right totals
    - Z: allowed/forbidden verdict with reason
    """

    VARIANTS = ["audit"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        left, right = [list(side) for side in random.choice(BASE_REACTIONS)]
        self._add_neutral_spectators(left, right)
        random.shuffle(left)
        random.shuffle(right)
        reaction = format_reaction(left, right)
        particles = unique_in_order(left + right)
        table = table_text(particles)
        steps = [
            step("CONSERVATION_SETUP", reaction, "check=Q,B,Le,Lmu"),
            step("PARTICLE_TABLE", table),
        ]
        left_totals = {}
        right_totals = {}
        for quantity in QUANTITIES:
            left_totals[quantity] = self._add_side_steps(
                steps, quantity, "left", left
            )
            right_totals[quantity] = self._add_side_steps(
                steps, quantity, "right", right
            )
            status = (
                "conserved" if left_totals[quantity] == right_totals[quantity]
                else "violated"
            )
            steps.append(
                step("CONSERVE_CHECK", quantity,
                     f"left={left_totals[quantity]},right="
                     f"{right_totals[quantity]}", status)
            )
        failures = []
        for quantity in QUANTITIES:
            delta = right_totals[quantity] - left_totals[quantity]
            if delta != 0:
                failures.append(
                    f"{quantity} changes by {signed_change(delta)}"
                )
        if failures:
            answer = f"forbidden - {'; '.join(failures)}"
            outcome = "forbidden"
        else:
            answer = "allowed - Q, B, Le, Lmu conserved"
            outcome = "allowed"
        steps.append(step("Z", answer))
        problem = (
            "Audit conservation of Q, B, Le, Lmu for reaction "
            f"{reaction}. Quantum numbers: {table}."
        )
        return dict(
            problem_id=jid(),
            operation=f"conservation_law_{outcome}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _add_neutral_spectators(self, left, right):
        for side in (left, right):
            for _ in range(random.randint(0, 2)):
                side.append(random.choice(NEUTRALS))

    def _add_side_steps(self, steps, quantity, side_name, particles):
        total = 0
        for particle in particles:
            value = PARTICLES[particle][quantity]
            next_total = total + value
            steps.append(
                step("QN_ADD", quantity, side_name,
                     f"{total} + {particle}({value})", next_total)
            )
            total = next_total
        return total

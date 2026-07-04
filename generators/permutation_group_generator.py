import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def list_text(values):
    return ", ".join(str(value) for value in values)


def perm_text(perm):
    return "[" + list_text(perm) + "]"


def compose(sigma, tau):
    return [sigma[tau[i] - 1] for i in range(len(sigma))]


def cycles_of(perm):
    n = len(perm)
    seen = [False] * n
    cycles = []
    for start in range(1, n + 1):
        if seen[start - 1]:
            continue
        current = start
        cycle = []
        while not seen[current - 1]:
            seen[current - 1] = True
            cycle.append(current)
            current = perm[current - 1]
        if len(cycle) > 1:
            cycles.append(cycle)
    return cycles


def cycle_text(cycles):
    if not cycles:
        return "identity"
    return "".join("(" + " ".join(str(value) for value in cycle) + ")"
                   for cycle in cycles)


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


class PermutationGroupGenerator(ProblemGenerator):
    """
    Permutation composition, cycle notation, order, and parity.

    Op-codes used:
    - PERM_SETUP / PERM_COMPOSE / PERM_RESULT: composition trace
    - CYCLE_TRACE / CYCLE / CYCLE_LENGTHS: cycle decomposition
    - GCD_RESULT / LCM_STEP / PARITY: order and parity computation
    - S / A (established/shared): transposition count arithmetic
    - Z: composition, cycles, order, and parity
    """

    def generate(self) -> dict:
        n = random.randint(4, 6)
        sigma = list(range(1, n + 1))
        tau = list(range(1, n + 1))
        random.shuffle(sigma)
        random.shuffle(tau)
        composed = compose(sigma, tau)
        cycles = cycles_of(composed)

        steps = [
            step("PERM_SETUP", f"n={n}", f"sigma={perm_text(sigma)}",
                 f"tau={perm_text(tau)}"),
        ]
        for idx, tau_value in enumerate(tau, start=1):
            image = sigma[tau_value - 1]
            steps.append(step("PERM_COMPOSE", f"i={idx}",
                              f"tau(i)={tau_value}", f"sigma(tau(i))={image}"))
        steps.append(step("PERM_RESULT", perm_text(composed)))

        for cycle in cycles:
            trace = "->".join(str(value) for value in cycle + [cycle[0]])
            steps.append(step("CYCLE_TRACE", f"start {cycle[0]}", trace))
            steps.append(step("CYCLE", cycle_text([cycle])))
        lengths = [len(cycle) for cycle in cycles]
        steps.append(step("CYCLE_LENGTHS", list_text(lengths) or "none"))

        order = 1
        for length in lengths:
            g = gcd(order, length)
            new_order = lcm(order, length)
            steps.append(step("GCD_RESULT", f"gcd({order},{length})", g))
            steps.append(step("LCM_STEP", order, length, new_order))
            order = new_order

        transpositions = 0
        for length in lengths:
            contribution = length - 1
            steps.append(step("S", length, 1, contribution))
            new_total = transpositions + contribution
            steps.append(step("A", transpositions, contribution, new_total))
            transpositions = new_total
        parity = "even" if transpositions % 2 == 0 else "odd"
        steps.append(step("PARITY", f"transpositions {transpositions}", parity))

        cycles_string = cycle_text(cycles)
        answer = (
            f"composition = {perm_text(composed)}; cycles = {cycles_string}; "
            f"order = {order}; parity = {parity}"
        )
        problem = (
            f"In S_{n}, let sigma={perm_text(sigma)} and tau={perm_text(tau)}, "
            f"where each list gives images of 1..{n}. Compute sigma after "
            f"tau, then give cycle notation, order, and parity."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="permutation_group",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

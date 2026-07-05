import math
import random

from base_generator import ProblemGenerator
from helpers import step, jid


CASES = [(23, 5), (29, 2), (31, 3)]


class BabyStepGiantStepGenerator(ProblemGenerator):
    """
    Baby-step giant-step discrete logarithm in small prime fields.

    Op-codes used:
    - BSGS_SETUP / BABY_STEP / GIANT_FACTOR / GIANT_STEP / BSGS_MATCH
    - CHECK
    - Z: discrete logarithm x
    """

    def generate(self) -> dict:
        p, g = random.choice(CASES)
        order = p - 1
        x_secret = random.randint(2, order - 2)
        h = pow(g, x_secret, p)
        m = math.ceil(math.sqrt(order))
        steps = [step("BSGS_SETUP", f"p={p}", f"g={g}", f"h={h}",
                      f"m={m}")]
        table = {}
        value = 1
        for j in range(m):
            table.setdefault(value, j)
            steps.append(step("BABY_STEP", f"j={j}", value))
            value = (value * g) % p
        factor = pow(pow(g, m, p), -1, p)
        steps.append(step("GIANT_FACTOR", f"g^-m mod p", factor))
        gamma = h
        found = None
        for i in range(m + 1):
            steps.append(step("GIANT_STEP", f"i={i}", gamma))
            if gamma in table:
                j = table[gamma]
                found = i * m + j
                steps.append(step("BSGS_MATCH", f"i={i}", f"j={j}",
                                  f"x={found}"))
                break
            gamma = (gamma * factor) % p
        steps.append(step("CHECK", f"{g}^{found} mod {p}", h))
        answer = f"x = {found}"
        problem = (
            f"Use baby-step giant-step to solve {g}^x congruent to {h} "
            f"modulo {p}, with 0 <= x < {order}."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="baby_step_giant_step",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

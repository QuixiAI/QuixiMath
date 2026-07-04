import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def coprime_pair():
    while True:
        m = random.randint(12, 90)
        n = random.randint(10, 85)
        if m != n and gcd(m, n) == 1:
            return m, n


class ExtendedEuclidGenerator(ProblemGenerator):
    """
    Extended Euclidean algorithm with explicit Bezout coefficient rows.

    Op-codes used:
    - EXT_GCD_SETUP: original integers
    - EUCLID_DIV: quotient and remainder line
    - BACK_SUB_ROW: row r = x*a + y*b in the coefficient table
    - M / S / A (established): quotient products and coefficient arithmetic
    - BEZOUT_CHECK / CHECK: final identity verification
    - Z: gcd and one pair of Bezout coefficients
    """

    def generate(self) -> dict:
        scale = random.choice([1, 1, 2, 3, 4, 5, 6, 7])
        m, n = coprime_pair()
        a, b = sorted((scale * m, scale * n), reverse=True)

        old_r, r = a, b
        old_x, x = 1, 0
        old_y, y = 0, 1
        steps = [
            step("EXT_GCD_SETUP", a, b),
            step("BACK_SUB_ROW", f"r={old_r}", f"x={old_x}", f"y={old_y}"),
            step("BACK_SUB_ROW", f"r={r}", f"x={x}", f"y={y}"),
        ]

        while r != 0:
            q = old_r // r
            product = q * r
            new_r = old_r - product
            steps.append(step("EUCLID_DIV", old_r, r, q, new_r))
            steps.append(step("M", q, r, product))
            steps.append(step("S", old_r, product, new_r))

            qx = q * x
            new_x = old_x - qx
            steps.append(step("M", q, x, qx))
            steps.append(step("S", old_x, qx, new_x))

            qy = q * y
            new_y = old_y - qy
            steps.append(step("M", q, y, qy))
            steps.append(step("S", old_y, qy, new_y))
            steps.append(step("BACK_SUB_ROW", f"r={new_r}",
                              f"x={new_x}", f"y={new_y}"))

            old_r, r = r, new_r
            old_x, x = x, new_x
            old_y, y = y, new_y

        ax = a * old_x
        by = b * old_y
        steps.extend([
            step("M", a, old_x, ax),
            step("M", b, old_y, by),
            step("A", ax, by, old_r),
            step("BEZOUT_CHECK", f"{a}*{old_x} + {b}*{old_y}", old_r),
            step("CHECK", "gcd is last nonzero remainder", old_r),
        ])
        answer = f"gcd = {old_r}; x = {old_x}; y = {old_y}"
        problem = (
            f"Use the extended Euclidean algorithm to find gcd({a}, {b}) "
            f"and coefficients x,y with {a}x + {b}y = gcd."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="extended_euclid",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

import random
import math
from base_generator import ProblemGenerator
from helpers import step, jid

TERMINATING_DENOMS = [2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50]
REPEATING_DENOMS = [3, 6, 7, 9, 11, 12, 13, 14, 15, 18, 21, 22]


class RepeatingDecimalGenerator(ProblemGenerator):
    """
    Determines whether a fraction converts to a terminating or repeating
    decimal and shows the exact decimal expansion.

    The denominator is factored completely (PF_PRIME only for true primes),
    the expansion digits come from visible long-division D steps, and a
    repeating decimal is written exactly with its repetend in parentheses
    (0.8(3)) — never a rounded float like 0.833333.
    """

    def generate(self) -> dict:
        denom = random.choice(TERMINATING_DENOMS + REPEATING_DENOMS)
        num = random.randint(1, denom - 1)

        steps = []
        # Simplify fraction (skip the no-op when already reduced)
        g = math.gcd(num, denom)
        simp_num, simp_den = num // g, denom // g
        if g > 1:
            steps.append(step("F", f"{num}/{denom}", f"{simp_num}/{simp_den}"))

        # Factor the reduced denominator completely
        factors = []
        d = simp_den
        p = 2
        while p * p <= d:
            while d % p == 0:
                factors.append(p)
                steps.append(step("PF_STEP", d, p, d // p))
                d //= p
            p += 1
        if d > 1:
            factors.append(d)
            steps.append(step("PF_PRIME", d))

        kind = ("terminating" if all(f in (2, 5) for f in factors)
                else "repeating")
        steps.append(step("DEC_TYPE", f"{simp_num}/{simp_den}", kind))

        # Exact expansion by long division with remainder-cycle detection
        digits = []
        seen = {}
        rem = simp_num % simp_den
        repetend_start = None
        while rem:
            if rem in seen:
                repetend_start = seen[rem]
                break
            seen[rem] = len(digits)
            current = rem * 10
            digit = current // simp_den
            steps.append(step("D", current, simp_den, digit))
            digits.append(str(digit))
            rem = current % simp_den

        if repetend_start is None:
            decimal_str = "0." + "".join(digits) if digits else "0"
        else:
            prefix = "".join(digits[:repetend_start])
            repetend = "".join(digits[repetend_start:])
            steps.append(step("REPEAT_DETECT",
                              f"remainder {rem} repeats",
                              f"repetend {repetend}"))
            decimal_str = f"0.{prefix}({repetend})"

        steps.append(step("DEC_VALUE", f"{simp_num}/{simp_den}", decimal_str))
        final_answer = f"{decimal_str} ({kind})"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="repeating_decimal",
            problem=f"Determine if {num}/{denom} is terminating or repeating, and give the decimal.",
            steps=steps,
            final_answer=final_answer,
        )

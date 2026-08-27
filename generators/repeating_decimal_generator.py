import random
import math
from base_generator import ProblemGenerator
from helpers import step, jid

# Every non-1 core is coprime to 10 and has a decimal period of at most 18.
# Multiplying by 2^a*5^b adds at most two nonrepeating digits, so the visible
# long division remains hand-sized while the fraction space is large.
DECIMAL_CORES = [
    1, 3, 7, 9, 11, 13, 17, 19, 21, 27, 31, 33, 37, 39, 41, 51,
    53, 57, 63, 73, 77, 79, 81, 91, 93, 99,
]

PROBLEM_TEMPLATES = [
    "Determine if {fraction} is terminating or repeating, and give the decimal.",
    "Classify {fraction} as terminating or repeating and write its exact decimal.",
    "Write {fraction} as an exact decimal and state whether it terminates or repeats.",
    "For the fraction {fraction}, decide whether its decimal terminates or repeats, then give it exactly.",
    "Find the exact decimal for {fraction} and identify it as terminating or repeating.",
]


def fraction_instance():
    """Construct a reducible or reduced proper fraction with a short period."""
    while True:
        core = random.choice(DECIMAL_CORES)
        reduced_den = core * (2 ** random.randint(0, 2)) * (5 ** random.randint(0, 2))
        if reduced_den > 1:
            break
    while True:
        reduced_num = random.randint(1, reduced_den - 1)
        if math.gcd(reduced_num, reduced_den) == 1:
            break
    common_factor = random.randint(1, 5)
    return reduced_num * common_factor, reduced_den * common_factor


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
        num, denom = fraction_instance()

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
            problem=random.choice(PROBLEM_TEMPLATES).format(
                fraction=f"{num}/{denom}"),
            steps=steps,
            final_answer=final_answer,
        )

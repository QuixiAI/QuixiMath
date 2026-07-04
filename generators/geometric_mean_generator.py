import math
import random
from base_generator import ProblemGenerator
from helpers import step, jid


def simp_sqrt(n):
    """√n simplified: returns (k, m) with n = k^2·m, m squarefree."""
    k = 1
    for f in range(int(math.isqrt(n)), 1, -1):
        if n % (f * f) == 0:
            k = f
            break
    return k, n // (k * k)


def sqrt_txt(n):
    """'6', '3√2', '√10'."""
    k, m = simp_sqrt(n)
    if m == 1:
        return str(k)
    return f"√{m}" if k == 1 else f"{k}√{m}"


class GeometricMeanGenerator(ProblemGenerator):
    """
    Geometric mean relationships in a right triangle with the altitude
    drawn to the hypotenuse: h = √(p·q), leg = √(p·c), and the reverse
    solve q = h²/p. Radical answers are simplified.

    Op-codes used:
    - GEO_SETUP: the configuration and the goal (given, goal)
    - THEOREM: the geometric mean relation used (established)
    - A / M / E / D: hypotenuse sum and the arithmetic (established)
    - ROOT_SIMPLIFY: pull the square factor out (established)
    - Z: 'h = 3√2', 'leg = 6', 'q = 9'
    """

    VARIANTS = ["altitude", "leg", "find_segment"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "altitude":
            p = random.randint(2, 12)
            q = random.randint(2, 12)
            n = p * q
            steps = [
                step("GEO_SETUP",
                     f"right triangle, altitude to hypotenuse; the "
                     f"altitude splits the hypotenuse into p = {p} and "
                     f"q = {q}", "altitude h"),
                step("THEOREM", "geometric mean (altitude)",
                     "h = √(p·q)"),
                step("M", p, q, n),
            ]
            val = sqrt_txt(n)
            if "√" in val:
                steps.append(step("ROOT_SIMPLIFY", f"√{n} = {val}"))
            else:
                steps.append(step("E", val, 2, n))
            answer = f"h = {val}"
            problem = (f"In a right triangle, the altitude to the "
                       f"hypotenuse splits it into segments of length "
                       f"{p} and {q}. Find the altitude h.")
        elif variant == "leg":
            p = random.randint(2, 10)
            q = random.randint(2, 10)
            c = p + q
            n = p * c
            steps = [
                step("GEO_SETUP",
                     f"right triangle, altitude to hypotenuse; segments "
                     f"p = {p} (adjacent to the leg) and q = {q}",
                     "the leg adjacent to p"),
                step("A", p, q, c),
                step("THEOREM", "geometric mean (leg)",
                     "leg = √(p·c)"),
                step("M", p, c, n),
            ]
            val = sqrt_txt(n)
            if "√" in val:
                steps.append(step("ROOT_SIMPLIFY", f"√{n} = {val}"))
            else:
                steps.append(step("E", val, 2, n))
            answer = f"leg = {val}"
            problem = (f"In a right triangle, the altitude to the "
                       f"hypotenuse splits it into segments p = {p} and "
                       f"q = {q}. Find the leg adjacent to the segment "
                       f"of length {p}.")
        else:
            h = random.randint(4, 12)
            divisors = [d for d in range(2, h * h) if h * h % d == 0]
            p = random.choice(divisors)
            q = h * h // p
            steps = [
                step("GEO_SETUP",
                     f"right triangle, altitude h = {h} to the "
                     f"hypotenuse; one segment p = {p}",
                     "the other segment q"),
                step("THEOREM", "geometric mean (altitude)",
                     "h^2 = p·q"),
                step("E", h, 2, h * h),
                step("D", h * h, p, q),
            ]
            answer = f"q = {q}"
            problem = (f"The altitude to the hypotenuse of a right "
                       f"triangle has length {h}, and it splits the "
                       f"hypotenuse into two segments, one of length "
                       f"{p}. Find the other segment q.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"geometric_mean_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


def wrap(v):
    """Parenthesizes negative or fractional values for display."""
    t = str(v)
    return f"({t})" if (isinstance(v, Fraction) and v.denominator != 1) \
        or v < 0 else t


class GeometricSequenceGenerator(ProblemGenerator):
    """
    Geometric sequences from four shown terms: the nth term, the partial
    sum (integer ratios), and the infinite sum when |r| < 1.

    The common ratio is computed from the first pair and verified on a
    second pair (A1). Infinite sums state the convergence condition
    before summing. All shown terms are integers by construction; later
    terms and sums may be exact fractions.

    Op-codes used:
    - SEQ_SETUP: the shown terms and the goal (established)
    - COMMON_RATIO: ratio of consecutive terms (work, value)
    - CHECK: verify r on another consecutive pair (established)
    - CONVERGE_CHECK: |r| < 1 so the infinite series converges
      (comparison, verdict)
    - SEQ_FORMULA / SEQ_APPLY: state then instantiate (established)
    - E / S / M / D: the arithmetic, exact fractions where needed
    - Z: final answer (integer or reduced fraction)
    """

    VARIANTS = ["nth_term", "partial_sum", "infinite_sum"]

    FRACTION_RS = [
        (Fraction(1, 2), [8, 16, 24, 32, 40, 48, -8, -16, -24, -32]),
        (Fraction(-1, 2), [8, 16, 24, 32, 40, 48, -8, -16, -24, -32]),
        (Fraction(1, 3), [27, 54, 81, 108, 135, -27, -54, -81]),
        (Fraction(-1, 3), [27, 54, 81, 108, -27, -54]),
        (Fraction(2, 3), [27, 54, 81, 108, -27, -54]),
        (Fraction(-2, 3), [27, 54, 81, -27, -54]),
        (Fraction(1, 4), [64, 128, 192, -64, -128]),
        (Fraction(3, 4), [64, 128, 192, -64]),
        (Fraction(1, 5), [125, 250, -125]),
        (Fraction(-1, 5), [125, 250, -125]),
        (Fraction(2, 5), [125, 250, -125]),
        (Fraction(3, 5), [125, 250, -125]),
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "partial_sum":
            r = Fraction(random.choice([2, 3, -2]))
            a = random.choice([v for v in range(-6, 7) if v != 0])
        elif variant == "infinite_sum":
            r, pool = random.choice(self.FRACTION_RS)
            a = random.choice(pool)
        else:
            if random.random() < 0.4:
                r, pool = random.choice(self.FRACTION_RS[:3])
                a = random.choice(pool)
            else:
                r = Fraction(random.choice([2, 3, -2]))
                a = random.choice([v for v in range(-6, 7) if v != 0])

        terms = [a * r ** i for i in range(4)]
        assert all(t.denominator == 1 for t in terms)
        shown = ", ".join(str(t.numerator) for t in terms)
        t = [t.numerator for t in terms]

        steps = [step("SEQ_SETUP", f"{shown}, ...", "")]  # goal set below

        def ratio_steps(goal):
            steps[0] = step("SEQ_SETUP", f"{shown}, ...", goal)
            steps.append(step("COMMON_RATIO", f"{t[1]}/{wrap(t[0])}", r))
            steps.append(step("CHECK", "ratio",
                              f"{t[2]}/{wrap(t[1])} = {r}", r))

        if variant == "nth_term":
            n = random.randint(5, 8 if abs(r) == 2 else
                               (6 if r == 3 else 7))
            value = a * r ** (n - 1)
            ratio_steps(f"term {n}")
            steps.append(step("SEQ_FORMULA", "a_n = a_1·r^(n - 1)"))
            steps.append(step("SEQ_APPLY",
                              f"a_{n} = {a}·{wrap(r)}^{n - 1}"))
            steps.append(step("E", wrap(r), n - 1, r ** (n - 1)))
            steps.append(step("M", a, r ** (n - 1), value))
            answer = str(value)
            steps.append(step("Z", answer))
            problem = (f"The geometric sequence {shown}, ... continues. "
                       f"Find term {n}.")
        elif variant == "partial_sum":
            n = random.randint(4, 5 if r == 3 else 7)
            rn = r ** n
            num = a * (rn - 1)
            den = r - 1
            total = num / den
            assert total.denominator == 1
            ratio_steps(f"sum of first {n} terms")
            steps.append(step("SEQ_FORMULA",
                              "S_n = a_1(r^n - 1)/(r - 1)"))
            steps.append(step("SEQ_APPLY",
                              f"S_{n} = {a}·({wrap(r)}^{n} - 1)/"
                              f"({r} - 1)"))
            steps.append(step("E", wrap(r), n, rn))
            steps.append(step("S", rn, 1, rn - 1))
            steps.append(step("M", a, rn - 1, num))
            steps.append(step("S", r, 1, den))
            if den != 1:
                steps.append(step("D", num, den, total))
            answer = str(total)
            steps.append(step("Z", answer))
            problem = (f"The geometric sequence {shown}, ... continues. "
                       f"Find the sum of the first {n} terms.")
        else:
            total = a / (1 - r)
            ratio_steps("sum of the infinite series")
            steps.append(step("CONVERGE_CHECK", f"abs(r) = {abs(r)} < 1",
                              "converges"))
            steps.append(step("SEQ_FORMULA", "S = a_1/(1 - r)"))
            steps.append(step("SEQ_APPLY", f"S = {a}/(1 - {wrap(r)})"))
            steps.append(step("S", 1, r, 1 - r))
            steps.append(step("D", a, 1 - r, total))
            answer = str(total)
            steps.append(step("Z", answer))
            problem = (f"The geometric series {shown}, ... continues "
                       f"forever. Find the sum of the infinite series.")

        return dict(
            problem_id=jid(),
            operation=f"geometric_sequence_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

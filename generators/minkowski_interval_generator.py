import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


RAPIDITIES = [
    Fraction(-5, 3),
    Fraction(-4, 3),
    Fraction(-3, 2),
    Fraction(-2, 3),
    Fraction(-1, 2),
    Fraction(1, 3),
    Fraction(1, 2),
    Fraction(2, 3),
    Fraction(3, 2),
    Fraction(4, 3),
]


def fraction_text(value):
    return str(Fraction(value))


def interval_class(s2):
    if s2 > 0:
        return "timelike"
    if s2 < 0:
        return "spacelike"
    return "lightlike"


class MinkowskiIntervalGenerator(ProblemGenerator):
    """
    Minkowski interval classification and rapidity addition.

    Variants:
    - interval_classification: s2=ct^2-x^2 and timelike/spacelike/lightlike.
    - rapidity_addition: eta_total=eta1+eta2 for collinear boosts.

    Op-codes used:
    - MINKOWSKI_SETUP / MINKOWSKI_FORMULA
    - INTERVAL_CLASS / RAPIDITY_SUM
    - A / S / E (established/shared): exact arithmetic
    - Z: interval classification or total rapidity
    """

    VARIANTS = ["interval_classification", "rapidity_addition"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "interval_classification":
            problem, steps, answer = self._generate_interval()
        else:
            problem, steps, answer = self._generate_rapidity()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"minkowski_interval_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_interval(self):
        ct = random.randint(-30, 30)
        x = random.randint(-30, 30)
        if ct == 0 and x == 0:
            ct = 1
        ct_sq = ct ** 2
        x_sq = x ** 2
        s2 = ct_sq - x_sq
        classification = interval_class(s2)
        steps = [
            step("MINKOWSKI_SETUP", "interval_classification",
                 f"ct={ct}", f"x={x}"),
            step("MINKOWSKI_FORMULA", "s2=ct^2-x^2"),
            step("E", ct, 2, ct_sq),
            step("E", x, 2, x_sq),
            step("S", ct_sq, x_sq, s2),
            step("INTERVAL_CLASS", f"s2={s2}", classification),
        ]
        answer = f"s2={s2}; class={classification}"
        problem = (
            f"In c=1 units, an event separation has ct={ct} and x={x}. "
            "Compute s2=ct^2-x^2 and classify the interval."
        )
        return problem, steps, answer

    def _generate_rapidity(self):
        eta1 = random.choice(RAPIDITIES)
        eta2 = random.choice(RAPIDITIES)
        total = eta1 + eta2
        steps = [
            step("MINKOWSKI_SETUP", "rapidity_addition",
                 f"eta1={fraction_text(eta1)}", f"eta2={fraction_text(eta2)}"),
            step("MINKOWSKI_FORMULA", "eta_total=eta1+eta2"),
            step("A", fraction_text(eta1), fraction_text(eta2),
                 fraction_text(total)),
            step("RAPIDITY_SUM", "collinear boosts", fraction_text(total)),
        ]
        answer = f"eta_total={fraction_text(total)}"
        problem = (
            f"Two collinear boosts have rapidities eta1={fraction_text(eta1)} "
            f"and eta2={fraction_text(eta2)}. Compute the total rapidity."
        )
        return problem, steps, answer

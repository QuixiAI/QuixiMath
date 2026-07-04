import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


QUARK_CHARGES = {
    "u": Fraction(2, 3),
    "d": Fraction(-1, 3),
    "s": Fraction(-1, 3),
    "c": Fraction(2, 3),
    "b": Fraction(-1, 3),
}
QUARKS = list(QUARK_CHARGES)


def fraction_text(value):
    return str(Fraction(value))


def signed_fraction(value):
    fr = Fraction(value)
    if fr > 0:
        return f"+{fraction_text(fr)}"
    return fraction_text(fr)


def quark_charge(name):
    if name.startswith("anti_"):
        return -QUARK_CHARGES[name.removeprefix("anti_")]
    return QUARK_CHARGES[name]


class QuarkCompositionGenerator(ProblemGenerator):
    """
    Hadron electric charge from quark constituents.

    The prompt supplies quark charges and the antiquark sign rule. The trace
    records each constituent's charge, then adds the fractions cumulatively.

    Op-codes used:
    - QUARK_SETUP: hadron kind, constituents, and supplied charge table
    - QUARK_CHARGE: constituent charge lookup from the supplied table/rule
    - A (established/shared): cumulative exact charge addition
    - Z: total hadron charge
    """

    VARIANTS = ["baryon", "antibaryon", "meson"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "baryon":
            constituents = [random.choice(QUARKS) for _ in range(3)]
        elif variant == "antibaryon":
            constituents = [
                f"anti_{random.choice(QUARKS)}" for _ in range(3)
            ]
        else:
            q1 = random.choice(QUARKS)
            q2 = f"anti_{random.choice(QUARKS)}"
            constituents = [q1, q2]
            random.shuffle(constituents)
        total = Fraction(0)
        table = "u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge"
        steps = [
            step("QUARK_SETUP", variant, " ".join(constituents), table),
        ]
        for name in constituents:
            charge = quark_charge(name)
            next_total = total + charge
            steps.append(step("QUARK_CHARGE", name, fraction_text(charge)))
            steps.append(
                step("A", fraction_text(total), fraction_text(charge),
                     fraction_text(next_total))
            )
            total = next_total
        answer = f"Q = {signed_fraction(total)}"
        steps.append(step("Z", answer))
        article = "an" if variant[0] in "aeiou" else "a"
        problem = (
            "Given quark charges u=2/3, d=-1/3, s=-1/3, c=2/3, "
            "b=-1/3 and antiquarks have opposite charge, compute the "
            f"electric charge of {article} {variant} with constituents "
            f"{' '.join(constituents)}."
        )
        return dict(
            problem_id=jid(),
            operation=f"quark_composition_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

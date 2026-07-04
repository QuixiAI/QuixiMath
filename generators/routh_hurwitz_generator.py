import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def first_column_text(values):
    return "[" + ",".join(fraction_text(value) for value in values) + "]"


class RouthHurwitzGenerator(ProblemGenerator):
    """
    Cubic Routh-Hurwitz stability array.

    Op-codes used:
    - ROUTH_SETUP: characteristic polynomial
    - ROUTH_ROW: row entries in the Routh array
    - M / S / D (established/shared): exact row-entry arithmetic
    - CHECK: first-column sign criterion
    - Z: first column and stability conclusion
    """

    def generate(self) -> dict:
        a1 = random.randint(1, 40)
        a2 = random.randint(1, 40)
        a3 = random.randint(1, 80)
        product = a1 * a2
        numerator = product - a3
        s1_entry = Fraction(numerator, a1)
        first_column = [Fraction(1), Fraction(a1), s1_entry, Fraction(a3)]
        stable = all(value > 0 for value in first_column)
        stability = "stable" if stable else "not stable"
        steps = [
            step("ROUTH_SETUP", f"p(s)=s^3+{a1}s^2+{a2}s+{a3}"),
            step("ROUTH_ROW", "s^3", f"1, {a2}"),
            step("ROUTH_ROW", "s^2", f"{a1}, {a3}"),
            step("M", a1, a2, product),
            step("S", product, a3, numerator),
            step("D", numerator, a1, fraction_text(s1_entry)),
            step("ROUTH_ROW", "s^1", f"{fraction_text(s1_entry)}, 0"),
            step("ROUTH_ROW", "s^0", f"{a3}"),
            step("CHECK", f"first column={first_column_text(first_column)}",
                 stability),
        ]
        answer = (
            f"first column={first_column_text(first_column)}; "
            f"{stability}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Build the Routh-Hurwitz array for p(s)=s^3+{a1}s^2+{a2}s+"
            f"{a3} and determine stability."
        )
        return dict(
            problem_id=jid(),
            operation="routh_hurwitz_cubic",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

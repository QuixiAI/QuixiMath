import random
import math
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class FractionComparisonGenerator(ProblemGenerator):
    """Compares two fractions using common denominator (human LCD method).

    Fractions are shown as written (2/4 stays 2/4, not 1/2), so
    equivalent-fraction pairs occur and the '=' relation is learnable;
    about one in ten problems is deliberately an equivalent pair.
    """

    def generate(self) -> dict:
        n1, d1 = random.randint(1, 9), random.randint(2, 12)
        if random.random() < 0.1:
            # Deliberately equivalent pair rendered differently (2/4 vs 1/2)
            k = random.choice([2, 3])
            n2, d2 = n1 * k, d1 * k
        else:
            n2, d2 = random.randint(1, 9), random.randint(2, 12)

        text1, text2 = f"{n1}/{d1}", f"{n2}/{d2}"

        steps = []
        # LCD of the denominators as written
        lcd = math.lcm(d1, d2)
        if d1 != d2:
            steps.append(step("L", d1, d2, lcd))

        n1c = n1 * (lcd // d1)
        n2c = n2 * (lcd // d2)
        if d1 != lcd:
            steps.append(step("C", text1, lcd, f"{n1c}/{lcd}"))
        if d2 != lcd:
            steps.append(step("C", text2, lcd, f"{n2c}/{lcd}"))

        # Compare converted numerators
        if n1c > n2c:
            relation = ">"
        elif n1c < n2c:
            relation = "<"
        else:
            relation = "="
        steps.append(step("CMP", f"{n1c}/{lcd}", f"{n2c}/{lcd}", relation))

        final_answer = f"{text1} {relation} {text2}"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="fraction_compare",
            problem=f"Compare: {text1} ? {text2}",
            steps=steps,
            final_answer=final_answer,
        )

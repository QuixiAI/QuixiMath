import math
import random

from base_generator import ProblemGenerator
from helpers import step, jid


def phi(z):
    """Standard normal CDF rounded to 4 decimals (table convention)."""
    return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)


def p4(x):
    """Renders a probability with 4 decimals: 0.0968."""
    return f"{x:.4f}"


class NormalTableGenerator(ProblemGenerator):
    """
    Normal-distribution probabilities with the z-table excerpt supplied in
    the problem text (Principle 5: no lookups the problem doesn't provide).
    The scratchpad standardizes, reads the provided table, and applies the
    complement / symmetry / between rule explicitly.

    Op-codes used:
    - NORM_SETUP: distribution and target probability (distribution, target)
    - ZSCORE: standardize (work, z)
    - TABLE_LOOKUP: read a provided table value (entry, value)
    - REWRITE: probability rule being applied (string)
    - S: subtraction on table values (a, b, difference)
    - Z: final answer (4-decimal probability)
    """

    CONTEXTS = [
        ("Exam scores", "points", 70, 90, 5, 15),
        ("Adult heights", "cm", 160, 178, 5, 9),
        ("Battery lifetimes", "hours", 40, 60, 4, 10),
        ("Package weights", "grams", 480, 520, 5, 12),
        ("Commute times", "minutes", 25, 45, 4, 9),
    ]

    VARIANTS = ["below", "below_negative", "above", "between"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _fmt(v):
        """Trims trailing zeros from a tenth-precision value: 119.5, 120."""
        return f"{v:g}"

    def _table(self, zs):
        """Renders the excerpt for the needed |z| values plus two decoys."""
        need = sorted({abs(z) for z in zs})
        decoys = [round(z, 1) for z in (need[0] + 0.2, need[-1] + 0.3)]
        rows = sorted(set(need + [d for d in decoys if 0 < d <= 3.4]))
        cells = "; ".join(f"z={z:.2f}: {p4(phi(z))}" for z in rows)
        return f"Standard normal table, Φ(z) = P(Z < z): {cells}"

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        name, unit, mu_lo, mu_hi, s_lo, s_hi = random.choice(self.CONTEXTS)
        mu = random.randint(mu_lo, mu_hi)
        sigma = random.randint(s_lo, s_hi)

        def zpick():
            return round(random.randint(3, 25) / 10, 1)

        steps = []
        if variant == "between":
            z1, z2 = sorted(random.sample([round(v / 10, 1)
                                           for v in range(3, 26)], 2))
            a = mu + z1 * sigma
            b = mu + z2 * sigma
            target = f"P({self._fmt(a)} < X < {self._fmt(b)})"
            table = self._table([z1, z2])
            steps.append(step("NORM_SETUP", f"X ~ N({mu}, {sigma})", target))
            steps.append(step("ZSCORE", f"({self._fmt(a)} - {mu})/{sigma}", f"{z1:.2f}"))
            steps.append(step("ZSCORE", f"({self._fmt(b)} - {mu})/{sigma}", f"{z2:.2f}"))
            steps.append(step("TABLE_LOOKUP", f"Φ({z1:.2f})", p4(phi(z1))))
            steps.append(step("TABLE_LOOKUP", f"Φ({z2:.2f})", p4(phi(z2))))
            steps.append(step("REWRITE", f"{target} = Φ({z2:.2f}) - Φ({z1:.2f})"))
            answer = round(phi(z2) - phi(z1), 4)
            steps.append(step("S", p4(phi(z2)), p4(phi(z1)), p4(answer)))
            question = (f"What is the probability of a value between "
                        f"{self._fmt(a)} and {self._fmt(b)} {unit}?")
        else:
            z = zpick()
            if variant == "below_negative":
                x = mu - z * sigma
                target = f"P(X < {self._fmt(x)})"
                z_signed = -z
            elif variant == "above":
                x = mu + z * sigma
                target = f"P(X > {self._fmt(x)})"
                z_signed = z
            else:  # below
                x = mu + z * sigma
                target = f"P(X < {self._fmt(x)})"
                z_signed = z
            table = self._table([z])
            steps.append(step("NORM_SETUP", f"X ~ N({mu}, {sigma})", target))
            steps.append(step("ZSCORE",
                              f"({self._fmt(x)} - {mu})/{sigma}", f"{z_signed:.2f}"))
            steps.append(step("TABLE_LOOKUP", f"Φ({z:.2f})", p4(phi(z))))
            if variant == "below":
                answer = phi(z)
            elif variant == "above":
                steps.append(step("REWRITE",
                                  f"{target} = 1 - Φ({z:.2f})"))
                answer = round(1 - phi(z), 4)
                steps.append(step("S", "1.0000", p4(phi(z)), p4(answer)))
            else:  # below_negative: symmetry
                steps.append(step("REWRITE",
                                  f"Φ({z_signed:.2f}) = 1 - Φ({z:.2f})"))
                answer = round(1 - phi(z), 4)
                steps.append(step("S", "1.0000", p4(phi(z)), p4(answer)))
            question = {
                "below": f"What is the probability of a value below {self._fmt(x)} {unit}?",
                "below_negative": f"What is the probability of a value below {self._fmt(x)} {unit}?",
                "above": f"What is the probability of a value above {self._fmt(x)} {unit}?",
            }[variant]

        steps.append(step("Z", p4(answer)))
        problem = (f"{name} are normally distributed with mean {mu} {unit} "
                   f"and standard deviation {sigma} {unit}. {question}\n{table}")

        return dict(
            problem_id=jid(),
            operation=f"normal_{'below' if variant == 'below_negative' else variant}",
            problem=problem,
            steps=steps,
            final_answer=p4(answer),
        )

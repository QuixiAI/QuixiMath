import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def sqrt_txt(n):
    return f"√{n}"


class TelescopingGenerator(ProblemGenerator):
    """
    Telescoping finite sums and products with exact rational or symbolic
    radical answers.

    Variants:
    - rational_sum: Σ 1/(k(k+d)) by partial fractions.
    - radical_sum: Σ (√(k+1)-√k).
    - product: Π k/(k+1).
    - reciprocal_gap: Σ (1/k - 1/(k+1)).

    Op-codes used:
    - TELE_SETUP / PARTFRAC_SETUP / TELESCOPE_CANCEL
    - A / S / M / D (established)
    - Z: exact finite result
    """

    VARIANTS = ["rational_sum", "radical_sum", "product", "reciprocal_gap"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "rational_sum":
            m = random.randint(1, 60)
            d = random.randint(1, 12)
            n = random.randint(m + d + 2, m + d + 100)
            left = sum(Fraction(1, k) for k in range(m, m + d))
            right = sum(Fraction(1, k) for k in range(n + 1, n + d + 1))
            diff = left - right
            value = diff / d
            steps = [
                step("TELE_SETUP", f"Σ k={m}..{n} 1/(k(k+{d}))"),
                step("PARTFRAC_SETUP",
                     f"1/(k(k+{d})) = 1/{d}(1/k - 1/(k+{d}))"),
                step("TELESCOPE_CANCEL",
                     f"survive k={m}..{m + d - 1}",
                     f"subtract k={n + 1}..{n + d}"),
                step("S", fmt_frac(left), fmt_frac(right), fmt_frac(diff)),
                step("D", fmt_frac(diff), d, fmt_frac(value)),
            ]
            answer = fmt_frac(value)
            problem = f"Evaluate Σ_{{k={m}}}^{{{n}}} 1/(k(k+{d}))."
        elif variant == "radical_sum":
            m = random.randint(1, 120)
            n = random.randint(m + 2, m + 160)
            answer = f"{sqrt_txt(n + 1)} - {sqrt_txt(m)}"
            steps = [
                step("TELE_SETUP",
                     f"Σ k={m}..{n} (√(k+1) - √k)"),
                step("TELESCOPE_CANCEL", "middle radicals cancel",
                     answer),
            ]
            problem = f"Evaluate Σ_{{k={m}}}^{{{n}}} (√(k+1) - √k)."
        elif variant == "product":
            m = random.randint(1, 120)
            n = random.randint(m + 2, m + 160)
            value = Fraction(m, n + 1)
            steps = [
                step("TELE_SETUP", f"Π k={m}..{n} k/(k+1)"),
                step("TELESCOPE_CANCEL", "all middle factors cancel",
                     f"{m}/{n + 1}"),
                step("D", m, n + 1, fmt_frac(value)),
            ]
            answer = fmt_frac(value)
            problem = f"Evaluate Π_{{k={m}}}^{{{n}}} k/(k+1)."
        else:
            m = random.randint(1, 120)
            n = random.randint(m + 2, m + 160)
            value = Fraction(1, m) - Fraction(1, n + 1)
            steps = [
                step("TELE_SETUP", f"Σ k={m}..{n} (1/k - 1/(k+1))"),
                step("TELESCOPE_CANCEL", "survive first and last",
                     f"1/{m} - 1/{n + 1}"),
                step("S", fmt_frac(Fraction(1, m)),
                     fmt_frac(Fraction(1, n + 1)), fmt_frac(value)),
            ]
            answer = fmt_frac(value)
            problem = f"Evaluate Σ_{{k={m}}}^{{{n}}} (1/k - 1/(k+1))."
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"telescoping_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

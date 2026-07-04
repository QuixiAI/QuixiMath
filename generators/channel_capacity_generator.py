import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def dec(value):
    value = Fraction(value)
    num, den = value.numerator, value.denominator
    p10 = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        p10 += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        p10 += 1
    assert den == 1, value
    if p10 == 0:
        return str(num)
    s = str(abs(num)).rjust(p10 + 1, "0")
    out = f"{s[:-p10]}.{s[-p10:]}".rstrip("0").rstrip(".")
    return ("-" if num < 0 else "") + out


def info_lookup(probability):
    value = -math.log2(float(probability))
    return Fraction(int(round(value * 1000)), 1000)


class ChannelCapacityGenerator(ProblemGenerator):
    """
    Binary symmetric channel entropy and capacity using supplied log values.

    Variants:
    - binary_entropy: compute H_b(p).
    - capacity: compute C=1-H_b(p).
    - block_bits: compute N*C for a number of channel uses.

    Op-codes used:
    - BSC_SETUP / BSC_FORMULA
    - S / M / A (established/shared): complement, entropy terms, capacity
    - Z: binary entropy, capacity, or maximum reliable bits
    """

    VARIANTS = ["binary_entropy", "capacity", "block_bits"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        p = Fraction(random.randint(1, 49), 100)
        n_uses = random.randint(10, 1000)
        q = 1 - p
        info_p = info_lookup(p)
        info_q = info_lookup(q)
        steps, entropy, capacity = self._trace(p, q, info_p, info_q)
        if variant == "binary_entropy":
            answer = f"H_b={dec(entropy)} bits"
            problem = self._problem(p, info_p, info_q, "Find H_b(p).")
        elif variant == "capacity":
            answer = f"C={dec(capacity)} bits/use"
            problem = self._problem(p, info_p, info_q,
                                    "Find capacity C=1-H_b(p).")
        else:
            max_bits = n_uses * capacity
            steps.append(step("BSC_FORMULA", "max_bits=N*C"))
            steps.append(step("M", n_uses, dec(capacity), dec(max_bits)))
            answer = f"max_bits={dec(max_bits)} bits"
            problem = self._problem(
                p,
                info_p,
                info_q,
                f"For N={n_uses} channel uses, find maximum reliable bits N*C.",
            )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"channel_capacity_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _problem(self, p, info_p, info_q, task):
        return (
            f"A binary symmetric channel has crossover probability "
            f"p={fraction_text(p)}. Use -log2(p)={dec(info_p)} and "
            f"-log2(1-p)={dec(info_q)}. {task}"
        )

    def _trace(self, p, q, info_p, info_q):
        term_p = p * info_p
        term_q = q * info_q
        entropy = term_p + term_q
        capacity = 1 - entropy
        steps = [
            step("BSC_SETUP", f"p={fraction_text(p)}",
                 f"-log2(p)={dec(info_p)}",
                 f"-log2(1-p)={dec(info_q)}"),
            step("S", 1, fraction_text(p), fraction_text(q)),
            step("BSC_FORMULA",
                 "H_b=p*(-log2 p)+(1-p)*(-log2(1-p))"),
            step("M", fraction_text(p), dec(info_p), dec(term_p)),
            step("M", fraction_text(q), dec(info_q), dec(term_q)),
            step("A", dec(term_p), dec(term_q), dec(entropy)),
            step("BSC_FORMULA", "C=1-H_b"),
            step("S", 1, dec(entropy), dec(capacity)),
        ]
        return steps, entropy, capacity

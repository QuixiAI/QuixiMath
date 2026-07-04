import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(fraction_text(value) for value in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def log2_power(value):
    value = Fraction(value)
    exponent = 0
    while value > 1:
        value /= 2
        exponent += 1
    while value < 1:
        value *= 2
        exponent -= 1
    if value != 1:
        raise ValueError(f"ratio is not a power of two: {value}")
    return exponent


def binary_pair():
    high = Fraction(2 ** random.randint(1, 10), 1)
    low = Fraction(1, 2 ** random.randint(1, 10))
    q0 = (1 - low) / (high - low)
    q1 = 1 - q0
    p0 = q0 * high
    p1 = q1 * low
    pairs = [(p0, q0), (p1, q1)]
    random.shuffle(pairs)
    p, q = zip(*pairs)
    return list(p), list(q)


def ternary_pair():
    high = Fraction(2 ** random.randint(1, 8), 1)
    low = Fraction(1, 2 ** random.randint(1, 8))
    above = high - 1
    below = 1 - low
    denom = 2 * (above + below)
    q0 = below / denom
    q1 = above / denom
    q2 = Fraction(1, 2)
    p0 = q0 * high
    p1 = q1 * low
    p2 = q2
    pairs = [(p0, q0), (p1, q1), (p2, q2)]
    random.shuffle(pairs)
    p, q = zip(*pairs)
    return list(p), list(q)


class KLDivergenceGenerator(ProblemGenerator):
    """
    KL divergence for small distributions with exact power-of-two ratios.

    Variants:
    - binary_forward: compute D_KL(P to Q) for two outcomes.
    - binary_reverse: compute D_KL(Q to P) for two outcomes.
    - ternary_forward: compute D_KL(P to Q) for three outcomes.
    - ternary_reverse: compute D_KL(Q to P) for three outcomes.

    Op-codes used:
    - KL_SETUP / KL_FORMULA / LOG2_RATIO
    - D / M / A (established/shared): ratios, weighted log terms, sum
    - Z: KL divergence in bits
    """

    VARIANTS = [
        "binary_forward",
        "binary_reverse",
        "ternary_forward",
        "ternary_reverse",
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant.startswith("binary"):
            p, q = binary_pair()
        else:
            p, q = ternary_pair()
        if variant.endswith("forward"):
            source, target = p, q
            source_name, target_name = "P", "Q"
        else:
            source, target = q, p
            source_name, target_name = "Q", "P"
        steps, divergence = self._trace(
            p, q, source, target, source_name, target_name
        )
        answer = (
            f"D_KL({source_name} to {target_name})="
            f"{fraction_text(divergence)} {bit_unit(divergence)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For distributions P={list_text(p)} and Q={list_text(q)}, "
            f"compute D_KL({source_name} to {target_name}) in bits."
        )
        return dict(
            problem_id=jid(),
            operation=f"kl_divergence_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _trace(self, p, q, source, target, source_name, target_name):
        steps = [
            step("KL_SETUP", f"P={list_text(p)}", f"Q={list_text(q)}",
                 f"direction={source_name} to {target_name}"),
            step("KL_FORMULA", "D=sum source_i*log2(source_i/target_i)"),
        ]
        running = Fraction(0)
        for idx, (source_i, target_i) in enumerate(zip(source, target)):
            ratio = source_i / target_i
            log_ratio = log2_power(ratio)
            term = source_i * log_ratio
            steps.append(step("D", fraction_text(source_i),
                              fraction_text(target_i), fraction_text(ratio)))
            steps.append(step("LOG2_RATIO", f"i={idx}",
                              f"ratio={fraction_text(ratio)}",
                              f"log={log_ratio}"))
            steps.append(step("M", fraction_text(source_i), log_ratio,
                              fraction_text(term)))
            new_running = running + term
            steps.append(step("A", fraction_text(running),
                              fraction_text(term), fraction_text(new_running)))
            running = new_running
        return steps, running

import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


CASES = [
    (Fraction(1, 4), Fraction(1, 2)),
    (Fraction(1, 2), Fraction(1, 4)),
    (Fraction(1, 4), Fraction(1, 4)),
]


INFO = {
    Fraction(1, 2): Fraction(1),
    Fraction(1, 4): Fraction(2),
    Fraction(3, 4): Fraction(415, 1000),
}


def ftxt(value):
    return str(Fraction(value))


def dec(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.6f}".rstrip("0").rstrip(".")


class EntropyRateMarkovGenerator(ProblemGenerator):
    """
    Entropy rate of a two-state Markov chain using supplied log values.

    Op-codes used:
    - MARKOV_SETUP / STATIONARY / ROW_ENTROPY / ENTROPY_TERM
    - M / A
    - Z: entropy rate in bits per symbol
    """

    def generate(self) -> dict:
        a, b = random.choice(CASES)
        p00, p01 = 1 - a, a
        p10, p11 = b, 1 - b
        pi0 = b / (a + b)
        pi1 = a / (a + b)
        rows = [(p00, p01), (p10, p11)]
        row_entropy = []
        steps = [
            step("MARKOV_SETUP", f"P00={ftxt(p00)},P01={ftxt(p01)}",
                 f"P10={ftxt(p10)},P11={ftxt(p11)}"),
            step("STATIONARY", f"pi0={ftxt(pi0)}", f"pi1={ftxt(pi1)}"),
        ]
        for idx, row in enumerate(rows):
            running = Fraction(0)
            for probability in row:
                term = probability * INFO[probability]
                steps.append(step("ENTROPY_TERM", f"row {idx}",
                                  f"p={ftxt(probability)}",
                                  f"I={dec(INFO[probability])}",
                                  ftxt(term)))
                running += term
            row_entropy.append(running)
            steps.append(step("ROW_ENTROPY", f"H{idx}", ftxt(running)))
        term0 = pi0 * row_entropy[0]
        term1 = pi1 * row_entropy[1]
        rate = term0 + term1
        steps.extend([
            step("M", ftxt(pi0), ftxt(row_entropy[0]), ftxt(term0)),
            step("M", ftxt(pi1), ftxt(row_entropy[1]), ftxt(term1)),
            step("A", ftxt(term0), ftxt(term1), ftxt(rate)),
        ])
        answer = f"entropy_rate = {dec(rate)} bits/symbol"
        logs = ", ".join(f"I({ftxt(k)})={dec(v)}" for k, v in sorted(INFO.items()))
        problem = (
            f"For a two-state Markov chain with P00={ftxt(p00)}, "
            f"P01={ftxt(p01)}, P10={ftxt(p10)}, P11={ftxt(p11)}, use "
            f"{logs}. Find the entropy rate."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="entropy_rate_markov",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

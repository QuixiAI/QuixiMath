import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


DISTRIBUTIONS = [
    [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)],
    [Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)],
    [Fraction(1, 2), Fraction(1, 8), Fraction(1, 8), Fraction(1, 4)],
    [Fraction(1, 8), Fraction(3, 8), Fraction(1, 4), Fraction(1, 4)],
]


def fraction_text(value):
    return str(Fraction(value))


def distribution_text(symbols, probabilities):
    return ", ".join(
        f"{symbol}={fraction_text(probability)}"
        for symbol, probability in zip(symbols, probabilities)
    )


def interval_text(low, high):
    return f"[{fraction_text(low)},{fraction_text(high)})"


def cumulative_intervals(symbols, probabilities):
    running = Fraction(0)
    intervals = {}
    for symbol, probability in zip(symbols, probabilities):
        high = running + probability
        intervals[symbol] = (running, high)
        running = high
    return intervals


class ArithmeticCodingGenerator(ProblemGenerator):
    """
    Arithmetic coding interval narrowing with exact rational endpoints.

    Op-codes used:
    - ARITH_SETUP / CUM_INTERVAL / ARITH_SYMBOL / ARITH_INTERVAL
    - S / M / A / D (established/shared): width, scaled offsets, midpoint
    - Z: final interval and midpoint code value
    """

    def generate(self) -> dict:
        probabilities = list(random.choice(DISTRIBUTIONS))
        symbols = list("ABCD"[:len(probabilities)])
        intervals = cumulative_intervals(symbols, probabilities)
        message = "".join(random.choice(symbols) for _ in range(
            random.randint(3, 6)
        ))
        steps = [
            step("ARITH_SETUP", distribution_text(symbols, probabilities),
                 f"message={message}"),
        ]
        for symbol in symbols:
            low, high = intervals[symbol]
            steps.append(step("CUM_INTERVAL", symbol, interval_text(low, high)))

        low = Fraction(0)
        high = Fraction(1)
        for symbol in message:
            sym_low, sym_high = intervals[symbol]
            width = high - low
            low_offset = width * sym_low
            high_offset = width * sym_high
            new_low = low + low_offset
            new_high = low + high_offset
            steps.extend([
                step("ARITH_SYMBOL", symbol,
                     f"cum={interval_text(sym_low, sym_high)}"),
                step("S", fraction_text(high), fraction_text(low),
                     fraction_text(width)),
                step("M", fraction_text(width), fraction_text(sym_low),
                     fraction_text(low_offset)),
                step("A", fraction_text(low), fraction_text(low_offset),
                     fraction_text(new_low)),
                step("M", fraction_text(width), fraction_text(sym_high),
                     fraction_text(high_offset)),
                step("A", fraction_text(low), fraction_text(high_offset),
                     fraction_text(new_high)),
                step("ARITH_INTERVAL", interval_text(new_low, new_high)),
            ])
            low, high = new_low, new_high
        endpoint_sum = low + high
        code = endpoint_sum / 2
        steps.append(step("A", fraction_text(low), fraction_text(high),
                          fraction_text(endpoint_sum)))
        steps.append(step("D", fraction_text(endpoint_sum), 2,
                          fraction_text(code)))
        answer = (
            f"interval={interval_text(low, high)}; "
            f"code={fraction_text(code)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Arithmetic-code message {message} using symbol probabilities "
            f"{distribution_text(symbols, probabilities)}. Find the final "
            "interval and midpoint code."
        )
        return dict(
            problem_id=jid(),
            operation="arithmetic_coding",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

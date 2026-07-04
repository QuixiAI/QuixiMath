import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

KELVIN_OFFSET = Fraction(27315, 100)  # 273.15, exact


class TemperatureConversionGenerator(ProblemGenerator):
    """
    Converts between Fahrenheit, Celsius, and Kelvin using explicit
    add/subtract and multiply/divide steps.

    All arithmetic is exact (Fraction, rendered as terminating decimals).
    Fahrenheit inputs are constructed with (F - 32) divisible by 9 so the
    Celsius result is an integer; every other path terminates naturally
    (division by 5, ±273.15).
    """

    def generate(self) -> dict:
        scenarios = [
            ("F", "C"),
            ("C", "F"),
            ("C", "K"),
            ("K", "C"),
            ("F", "K"),
            ("K", "F"),
        ]
        from_unit, to_unit = random.choice(scenarios)

        # Keep values reasonable and allow negative Celsius/Fahrenheit.
        if from_unit == "F":
            # (F - 32) divisible by 9 -> exact integer Celsius
            value = 32 + 9 * random.randint(-12, 24)
        else:
            value = random.randint(-40, 212)
        steps = []

        def add(x, y):
            res = x + y
            steps.append(step("A", dec(x), dec(y), dec(res)))
            return res

        def sub(x, y):
            res = x - y
            steps.append(step("S", dec(x), dec(y), dec(res)))
            return res

        def mul(x, y):
            res = x * y
            steps.append(step("M", dec(x), dec(y), dec(res)))
            return res

        def div(x, y):
            res = x / y
            steps.append(step("D", dec(x), dec(y), dec(res)))
            return res

        current = Fraction(value)
        thirty_two = Fraction(32)
        five = Fraction(5)
        nine = Fraction(9)
        if from_unit == "F" and to_unit == "C":
            current = sub(current, thirty_two)
            current = mul(five, current)
            current = div(current, nine)
        elif from_unit == "C" and to_unit == "F":
            current = mul(nine, current)
            current = div(current, five)
            current = add(current, thirty_two)
        elif from_unit == "C" and to_unit == "K":
            current = add(current, KELVIN_OFFSET)
        elif from_unit == "K" and to_unit == "C":
            current = sub(current, KELVIN_OFFSET)
        elif from_unit == "F" and to_unit == "K":
            current = sub(current, thirty_two)
            current = mul(five, current)
            current = div(current, nine)
            current = add(current, KELVIN_OFFSET)
        else:  # K to F
            current = sub(current, KELVIN_OFFSET)
            current = mul(nine, current)
            current = div(current, five)
            current = add(current, thirty_two)

        final_answer = f"{dec(current)} {to_unit}"
        problem = f"Convert {value} {from_unit} to {to_unit}"
        steps.append(step("CONV_RESULT", f"{value} {from_unit}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="convert_temperature",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

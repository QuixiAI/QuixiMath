import random
from base_generator import ProblemGenerator
from helpers import step, jid


class RateConversionGenerator(ProblemGenerator):
    """
    Converts rates like mph -> ft/s (and reverse) using factor-label steps
    with explicit numerator/denominator conversions.

    CONV_FACTOR always states the canonical relation (1 big = k small),
    e.g. '1 hr = 3600 s', regardless of conversion direction.
    """

    def generate(self) -> dict:
        # Scenarios chosen to keep integer intermediates/finals;
        # length_rel/time_rel are canonical (big_unit, k, small_unit)
        scenarios = [
            dict(
                from_unit="mi/hr", to_unit="ft/s",
                length_rel=("mi", 5280, "ft"), time_rel=("hr", 3600, "s"),
                value_mult=15,  # value * 22/15 = integer
                length_first=True,
            ),
            dict(
                from_unit="ft/s", to_unit="mi/hr",
                length_rel=("mi", 5280, "ft"), time_rel=("hr", 3600, "s"),
                value_mult=22,  # value * 15/22 = integer
                length_first=False,  # multiply time first, then divide length
            ),
            dict(
                from_unit="km/hr", to_unit="m/s",
                length_rel=("km", 1000, "m"), time_rel=("hr", 3600, "s"),
                value_mult=18,  # value * 5/18 = integer
                length_first=True,
            ),
            dict(
                from_unit="m/s", to_unit="km/hr",
                length_rel=("km", 1000, "m"), time_rel=("hr", 3600, "s"),
                value_mult=5,  # value * 18/5 = integer
                length_first=False,
            ),
            dict(
                from_unit="m/min", to_unit="cm/s",
                length_rel=("m", 100, "cm"), time_rel=("min", 60, "s"),
                value_mult=3,  # value * 5/3 = integer
                length_first=True,
            ),
            dict(
                from_unit="cm/s", to_unit="m/min",
                length_rel=("m", 100, "cm"), time_rel=("min", 60, "s"),
                value_mult=5,  # value * 3/5 = integer
                length_first=False,
            ),
        ]

        scenario = random.choice(scenarios)
        value = random.randint(1, 25) * scenario["value_mult"]
        steps = []

        def multiply(val, factor):
            product = val * factor
            steps.append(step("M", val, factor, product))
            return product

        def divide(val, divisor):
            quotient = val // divisor
            steps.append(step("D", val, divisor, quotient))
            return quotient

        length_big, length_k, length_small = scenario["length_rel"]
        time_big, time_k, time_small = scenario["time_rel"]
        length_factor_step = step("CONV_FACTOR", f"1 {length_big}",
                                  f"{length_k} {length_small}")
        time_factor_step = step("CONV_FACTOR", f"1 {time_big}",
                                f"{time_k} {time_small}")

        problem = f"Convert {value} {scenario['from_unit']} to {scenario['to_unit']}"

        current = value
        if scenario["length_first"]:
            # big/small -> small/smaller: scale length up, then per-time down
            steps.append(length_factor_step)
            current = multiply(current, length_k)
            steps.append(time_factor_step)
            current = divide(current, time_k)
        else:
            # small/small -> big/big: scale time up, then length down
            steps.append(time_factor_step)
            current = multiply(current, time_k)
            steps.append(length_factor_step)
            current = divide(current, length_k)

        final_answer = f"{current} {scenario['to_unit']}"
        steps.append(step("CONV_RESULT", f"{value} {scenario['from_unit']}", final_answer))
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="convert_rate",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

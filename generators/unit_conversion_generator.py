import random
from base_generator import ProblemGenerator
from helpers import step, jid

LENGTH = [("m", "cm", 100), ("km", "m", 1000), ("ft", "in", 12)]
WEIGHT = [("kg", "g", 1000), ("lb", "oz", 16)]
TIME = [("hr", "min", 60), ("min", "sec", 60)]
MONEY = [("dollar", "cent", 100)]


class UnitConversionGenerator(ProblemGenerator):
    """Performs one-step unit conversions with factor-label style steps.

    Both directions are generated: big->small multiplies, small->big
    divides (values constructed to divide exactly).
    """

    def generate(self) -> dict:
        category = random.choice(["length", "weight", "time", "money"])
        if category == "length":
            from_u, to_u, factor = random.choice(LENGTH)
        elif category == "weight":
            from_u, to_u, factor = random.choice(WEIGHT)
        elif category == "time":
            from_u, to_u, factor = random.choice(TIME)
        else:
            from_u, to_u, factor = random.choice(MONEY)

        steps = []
        if random.random() < 0.5:
            # big -> small: multiply
            value = random.randint(1, 50)
            result = value * factor
            problem = f"Convert {value} {from_u} to {to_u}"
            steps.append(step("CONV_FACTOR", f"1 {from_u}", f"{factor} {to_u}"))
            steps.append(step("M", value, factor, result))
            steps.append(step("CONV_RESULT", f"{value} {from_u}", f"{result} {to_u}"))
            final_answer = f"{result} {to_u}"
            operation = f"convert_{from_u}_to_{to_u}"
        else:
            # small -> big: divide (constructed to divide exactly)
            result = random.randint(1, 50)
            value = result * factor
            problem = f"Convert {value} {to_u} to {from_u}"
            steps.append(step("CONV_FACTOR", f"1 {from_u}", f"{factor} {to_u}"))
            steps.append(step("D", value, factor, result))
            steps.append(step("CONV_RESULT", f"{value} {to_u}", f"{result} {from_u}"))
            final_answer = f"{result} {from_u}"
            operation = f"convert_{to_u}_to_{from_u}"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

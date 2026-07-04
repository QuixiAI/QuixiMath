import random
from decimal import Decimal, ROUND_HALF_UP
from base_generator import ProblemGenerator
from helpers import step, jid


class PlaceValueRoundingGenerator(ProblemGenerator):
    """Rounds whole numbers or decimals to a specified place with digit inspection steps.

    Rounding is school-style half-up (never float/banker's rounding), the
    inspected digits always exist (no degenerate 'round 49.5 to the nearest
    hundredth'), and ROUND_CHECK always means
    (digit at target place, decision digit one place below, verdict).
    """

    def generate(self) -> dict:
        mode = random.choice(["whole", "decimal"])
        if mode == "whole":
            target = random.choice([10, 100, 1000])
            # number >= target so the answer is never the degenerate 0
            number = random.randint(target, 99999)
            operation = f"round_to_{target}"
            problem = f"Round {number} to the nearest {target}"
            target_digit = (number // target) % 10
            decision_digit = (number // (target // 10)) % 10
            round_up = decision_digit >= 5
            steps = []
            steps.append(step("ROUND_CHECK", target_digit, decision_digit,
                              ">=5" if round_up else "<5"))
            base = (number // target) * target
            rounded = base + (target if round_up else 0)
            steps.append(step("ROUND_RESULT", str(number), str(rounded)))
            steps.append(step("Z", str(rounded)))
            return dict(
                problem_id=jid(),
                operation=operation,
                problem=problem,
                steps=steps,
                final_answer=str(rounded),
            )
        else:
            # decimal rounding to tenths or hundredths; the number always has
            # one more decimal digit than the target place (kept significant)
            target_place = random.choice(["tenth", "hundredth"])
            place = {"tenth": 1, "hundredth": 2}[target_place]
            whole = random.randint(1, 99)
            dec_digits = [random.randint(0, 9) for _ in range(place + 1)]
            if dec_digits[-1] == 0:
                dec_digits[-1] = random.randint(1, 9)
            num_str = f"{whole}." + "".join(str(d) for d in dec_digits)
            operation = f"round_to_{target_place}"
            problem = f"Round {num_str} to the nearest {target_place}"

            target_digit = dec_digits[place - 1]
            decision_digit = dec_digits[place]
            round_up = decision_digit >= 5

            quantum = Decimal(1).scaleb(-place)  # 0.1 or 0.01
            rounded = Decimal(num_str).quantize(quantum, rounding=ROUND_HALF_UP)
            # minimal-digit rendering per the answer conventions (50, not 50.0)
            rounded_str = str(rounded)
            if "." in rounded_str:
                rounded_str = rounded_str.rstrip("0").rstrip(".")

            steps = []
            steps.append(step("ROUND_CHECK", target_digit, decision_digit,
                              ">=5" if round_up else "<5"))
            steps.append(step("ROUND_RESULT", num_str, rounded_str))
            steps.append(step("Z", rounded_str))

            return dict(
                problem_id=jid(),
                operation=operation,
                problem=problem,
                steps=steps,
                final_answer=rounded_str,
            )

import random
from base_generator import ProblemGenerator
from helpers import step, jid

class AbacusAdditionGenerator(ProblemGenerator):
    """Generates addition problems solved abacus-style: left to right,
    adding one place value of the addend at a time to a running total.

    This is the genuine soroban strategy (most-significant digit first,
    running total updated after every move), deliberately distinct from
    MultiDigitAdditionGenerator's right-to-left column algorithm — the
    same "a + b" problem with a different valid scratchpad.

    Op-codes used:
    - AB_SET: place the first number on the abacus
    - AB_ADD: add one place-value component; payload is
      (component, previous_total, new_total)
    - Z: final answer
    """

    def generate(self) -> dict:
        operation = "abacus_addition"
        num1 = random.randint(10, 9999)
        num2 = random.randint(10, 9999)
        result = num1 + num2
        final_answer_str = str(result)
        problem = f"{num1} + {num2}" # Neutral problem statement

        steps = []
        steps.append(step("AB_SET", num1)) # Set the first number

        # Add num2 one place value at a time, most significant first
        total = num1
        s2 = str(num2)
        for i, digit_char in enumerate(s2):
            digit = int(digit_char)
            component = digit * 10 ** (len(s2) - 1 - i)
            if component == 0:
                continue
            new_total = total + component
            steps.append(step("AB_ADD", f"+{component}", total, new_total))
            total = new_total

        steps.append(step("Z", final_answer_str)) # Final answer step

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer_str
        )

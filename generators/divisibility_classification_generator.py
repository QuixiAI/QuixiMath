import random
from base_generator import ProblemGenerator
from helpers import step, jid

# Primes up to isqrt(400) — enough to classify anything in range
TRIAL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19]


class DivisibilityClassificationGenerator(ProblemGenerator):
    """Checks divisibility by small primes and classifies as prime/composite.

    Human flow: trial-divide primes up to sqrt(n) and STOP at the first
    factor found. Composite answers carry the witness pair so the label
    isn't a gradable coin flip: 'composite (2 × 20)'.
    """

    def generate(self) -> dict:
        n = random.randint(10, 400)
        steps = []
        factor = None
        for p in TRIAL_PRIMES:
            if p * p > n:
                break
            rem = n % p
            steps.append(step("DIV_CHECK", n, p, rem))
            if rem == 0:
                factor = p
                break

        if factor is None:
            steps.append(step("PRIME", n))
            final_answer = "prime"
        else:
            other = n // factor
            steps.append(step("COMPOSITE_FACTOR", factor, other))
            final_answer = f"composite ({factor} × {other})"
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="divisibility_classify",
            problem=f"Classify {n} as prime or composite",
            steps=steps,
            final_answer=final_answer,
        )

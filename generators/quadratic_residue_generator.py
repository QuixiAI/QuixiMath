import random

from base_generator import ProblemGenerator
from helpers import step, jid


PRIMES = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]


class QuadraticResidueGenerator(ProblemGenerator):
    """
    Legendre symbol computation by Euler's criterion.

    Op-codes used:
    - LEGENDRE_SETUP / EULER_CRITERION / LEGENDRE_RESULT: theorem trace
    - BINARY_EXPONENT / MODEXP_SQUARE / MODEXP_MULTIPLY / MODEXP_STATE:
      modular exponentiation for a^((p-1)/2)
    - S / D / M / MOD_REDUCE (established/shared): arithmetic
    - Z: Legendre symbol value
    """

    def generate(self) -> dict:
        prime = random.choice(PRIMES)
        while True:
            a = random.randint(2, 4 * prime)
            if a % prime != 0:
                break
        exponent = (prime - 1) // 2
        a_mod = a % prime
        bits = bin(exponent)[2:]

        steps = [
            step("LEGENDRE_SETUP", f"a={a}", f"p={prime}"),
            step("S", prime, 1, prime - 1),
            step("D", prime - 1, 2, exponent),
            step("MOD_REDUCE", a, f"mod {prime}", a_mod),
            step("BINARY_EXPONENT", exponent, bits),
        ]

        result = 1
        for idx, bit in enumerate(bits, start=1):
            squared = result * result
            reduced_square = squared % prime
            steps.append(step("M", result, result, squared))
            steps.append(step("MOD_REDUCE", squared, f"mod {prime}",
                              reduced_square))
            steps.append(step("MODEXP_SQUARE", f"bit {idx}={bit}",
                              reduced_square))
            result = reduced_square
            if bit == "1":
                product = result * a_mod
                reduced_product = product % prime
                steps.append(step("M", result, a_mod, product))
                steps.append(step("MOD_REDUCE", product, f"mod {prime}",
                                  reduced_product))
                steps.append(step("MODEXP_MULTIPLY", f"bit {idx}=1",
                                  reduced_product))
                result = reduced_product
            else:
                steps.append(step("MODEXP_MULTIPLY", f"bit {idx}=0",
                                  "skip"))
            steps.append(step("MODEXP_STATE", f"after bit {idx}", result))

        if result == 1:
            symbol = 1
            meaning = "quadratic residue"
        else:
            symbol = -1
            meaning = "quadratic nonresidue"
        steps.extend([
            step("EULER_CRITERION", f"{a}^{exponent} mod {prime}", result),
            step("LEGENDRE_RESULT", result, symbol, meaning),
        ])
        answer = f"Legendre({a},{prime}) = {symbol}"
        problem = (
            f"Use Euler's criterion to compute Legendre({a},{prime})."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="quadratic_residue_legendre",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

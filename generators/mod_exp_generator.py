import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


class ModExpGenerator(ProblemGenerator):
    """
    Fast modular exponentiation by left-to-right square-and-multiply.

    Op-codes used:
    - MODEXP_SETUP / BINARY_EXPONENT: problem setup
    - MODEXP_SQUARE / MODEXP_MULTIPLY / MODEXP_STATE: bit-by-bit trace
    - M / MOD_REDUCE (established or shared): arithmetic
    - Z: final residue
    """

    def generate(self) -> dict:
        while True:
            base = random.randint(2, 60)
            exponent = random.randint(5, 90)
            modulus = random.randint(11, 97)
            base_mod = base % modulus
            if base_mod not in (0, 1) and gcd(base_mod, modulus) == 1:
                break
        bits = bin(exponent)[2:]

        steps = [
            step("MODEXP_SETUP", f"base {base}", f"exponent {exponent}",
                 f"modulus {modulus}"),
            step("MOD_REDUCE", base, f"mod {modulus}", base_mod),
            step("BINARY_EXPONENT", exponent, bits),
        ]
        result = 1
        for idx, bit in enumerate(bits, start=1):
            squared = result * result
            reduced_square = squared % modulus
            steps.append(step("M", result, result, squared))
            steps.append(step("MOD_REDUCE", squared, f"mod {modulus}",
                              reduced_square))
            steps.append(step("MODEXP_SQUARE", f"bit {idx}={bit}",
                              reduced_square))
            result = reduced_square

            if bit == "1":
                product = result * base_mod
                reduced_product = product % modulus
                steps.append(step("M", result, base_mod, product))
                steps.append(step("MOD_REDUCE", product, f"mod {modulus}",
                                  reduced_product))
                steps.append(step("MODEXP_MULTIPLY", f"bit {idx}=1",
                                  reduced_product))
                result = reduced_product
            else:
                steps.append(step("MODEXP_MULTIPLY", f"bit {idx}=0",
                                  "skip"))
            steps.append(step("MODEXP_STATE", f"after bit {idx}", result))

        answer = f"{base}^{exponent} mod {modulus} = {result}"
        problem = (
            f"Use square-and-multiply to compute {base}^{exponent} "
            f"modulo {modulus}."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="mod_exp",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

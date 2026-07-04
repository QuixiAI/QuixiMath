import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


MODULUS_POOL = [3, 4, 5, 7, 9, 11, 13]


def list_text(values):
    return ", ".join(str(value) for value in values)


def product(values):
    out = 1
    for value in values:
        out *= value
    return out


def inverse_mod(a, modulus):
    residue = a % modulus
    for candidate in range(modulus):
        if (residue * candidate) % modulus == 1:
            return candidate
    raise ValueError("inverse does not exist")


def random_pairwise_coprime_moduli(count):
    while True:
        moduli = sorted(random.sample(MODULUS_POOL, count))
        if all(gcd(a, b) == 1
               for i, a in enumerate(moduli)
               for b in moduli[i + 1:]):
            return moduli


class CRTGenerator(ProblemGenerator):
    """
    Chinese Remainder Theorem construction for pairwise-coprime moduli.

    Op-codes used:
    - CRT_SETUP / CRT_CONGRUENCE / CRT_TOTAL_MODULUS: system setup
    - CRT_FACTOR / MOD_INVERSE / CRT_TERM: constructive CRT terms
    - A / M / D / MOD_REDUCE (established or shared): arithmetic
    - CRT_CHECK: final congruence verification
    - Z: least nonnegative solution modulo the product
    """

    def generate(self) -> dict:
        count = random.choice([2, 3, 3])
        moduli = random_pairwise_coprime_moduli(count)
        residues = [random.randint(0, modulus - 1) for modulus in moduli]
        total_modulus = product(moduli)

        steps = [
            step("CRT_SETUP", f"{count} congruences"),
            step("CRT_TOTAL_MODULUS", list_text(moduli), total_modulus),
        ]
        for idx, (residue, modulus) in enumerate(zip(residues, moduli),
                                                start=1):
            steps.append(step("CRT_CONGRUENCE", f"i={idx}",
                              f"x={residue}", f"mod {modulus}"))

        running_sum = 0
        for idx, (residue, modulus) in enumerate(zip(residues, moduli),
                                                start=1):
            partial = total_modulus // modulus
            inverse = inverse_mod(partial, modulus)
            steps.append(step("D", total_modulus, modulus, partial))
            steps.append(step("CRT_FACTOR", f"i={idx}",
                              f"M_i={partial}", f"mod {modulus}"))
            steps.append(step("MOD_INVERSE",
                              f"{partial} mod {modulus}", inverse))
            first_product = residue * partial
            term = first_product * inverse
            steps.append(step("M", residue, partial, first_product))
            steps.append(step("M", first_product, inverse, term))
            steps.append(step("CRT_TERM", f"i={idx}", term))
            new_sum = running_sum + term
            steps.append(step("A", running_sum, term, new_sum))
            running_sum = new_sum

        solution = running_sum % total_modulus
        steps.append(step("MOD_REDUCE", running_sum,
                          f"mod {total_modulus}", solution))
        for idx, (residue, modulus) in enumerate(zip(residues, moduli),
                                                start=1):
            check = solution % modulus
            steps.append(step("MOD_REDUCE", solution, f"mod {modulus}",
                              check))
            steps.append(step("CRT_CHECK", f"i={idx}", check, residue))

        answer = f"x = {solution} mod {total_modulus}"
        clauses = [
            f"x congruent to {residue} modulo {modulus}"
            for residue, modulus in zip(residues, moduli)
        ]
        problem = (
            f"Solve the CRT system {'; '.join(clauses)}. Give the least "
            f"nonnegative solution modulo the product."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="crt",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

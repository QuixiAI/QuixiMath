import random

from base_generator import ProblemGenerator
from helpers import step, jid


COEFFS = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
INDICES = [1, 2, 3]


def epsilon(a, b, c):
    values = [a, b, c]
    if len(set(values)) < 3:
        return 0
    inversions = sum(
        1
        for i in range(3)
        for j in range(i + 1, 3)
        if values[i] > values[j]
    )
    return -1 if inversions % 2 else 1


def delta(a, b):
    return 1 if a == b else 0


def scaled_target_text(coeff, j, k, l, m):
    body = f"sum_i eps_i{j}{k} eps_i{l}{m}"
    if coeff == 1:
        return body
    if coeff == -1:
        return f"-{body}"
    return f"{coeff}*{body}"


class IndexGymnasticsGenerator(ProblemGenerator):
    """
    Levi-Civita contraction arithmetic:
    sum_i eps_ijk eps_ilm = delta_jl delta_km - delta_jm delta_kl.

    Op-codes used:
    - INDEX_SETUP / IDENTITY / EPSILON_VALUE / DELTA_VALUE / CHECK
    - A / M / S (established/shared): exact integer arithmetic
    - Z: scaled contraction result
    """

    def generate(self) -> dict:
        coeff = random.choice(COEFFS)
        j, k, l, m = [random.choice(INDICES) for _ in range(4)]
        eps_products = []
        steps = [
            step("INDEX_SETUP", f"c={coeff}", f"j={j}, k={k}",
                 f"l={l}, m={m}"),
            step("IDENTITY", "sum_i eps_ijk eps_ilm",
                 "delta_jl delta_km - delta_jm delta_kl"),
        ]
        for i in INDICES:
            left = epsilon(i, j, k)
            right = epsilon(i, l, m)
            product = left * right
            eps_products.append(product)
            steps.extend([
                step("EPSILON_VALUE", f"eps_{i}{j}{k}", left),
                step("EPSILON_VALUE", f"eps_{i}{l}{m}", right),
                step("M", left, right, product),
            ])
        partial = eps_products[0] + eps_products[1]
        lhs = partial + eps_products[2]
        d_jl = delta(j, l)
        d_km = delta(k, m)
        d_jm = delta(j, m)
        d_kl = delta(k, l)
        rhs_left = d_jl * d_km
        rhs_right = d_jm * d_kl
        rhs = rhs_left - rhs_right
        scaled = coeff * lhs
        steps.extend([
            step("A", eps_products[0], eps_products[1], partial),
            step("A", partial, eps_products[2], lhs),
            step("DELTA_VALUE", f"delta_{j}{l}", d_jl),
            step("DELTA_VALUE", f"delta_{k}{m}", d_km),
            step("DELTA_VALUE", f"delta_{j}{m}", d_jm),
            step("DELTA_VALUE", f"delta_{k}{l}", d_kl),
            step("M", d_jl, d_km, rhs_left),
            step("M", d_jm, d_kl, rhs_right),
            step("S", rhs_left, rhs_right, rhs),
            step("CHECK", "epsilon contraction", rhs, "identity"),
            step("M", coeff, lhs, scaled),
        ])
        target = scaled_target_text(coeff, j, k, l, m)
        answer = f"{target} = {scaled}"
        steps.append(step("Z", answer))
        problem = (
            f"Evaluate c * sum_i eps_i{j}{k} eps_i{l}{m} with c={coeff} "
            f"for j={j}, k={k}, l={l}, m={m} in 3D, and verify the "
            "Kronecker-delta identity."
        )
        return dict(
            problem_id=jid(),
            operation="index_gymnastics_levi_civita",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

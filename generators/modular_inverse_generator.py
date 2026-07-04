import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def list_text(values):
    return ", ".join(str(value) for value in values)


def extended_trace(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    steps = [
        step("EXT_GCD_SETUP", a, b),
        step("BACK_SUB_ROW", f"r={old_r}", f"x={old_x}", f"y={old_y}"),
        step("BACK_SUB_ROW", f"r={r}", f"x={x}", f"y={y}"),
    ]
    while r != 0:
        q = old_r // r
        product = q * r
        new_r = old_r - product
        steps.append(step("EUCLID_DIV", old_r, r, q, new_r))
        steps.append(step("M", q, r, product))
        steps.append(step("S", old_r, product, new_r))

        qx = q * x
        new_x = old_x - qx
        steps.append(step("M", q, x, qx))
        steps.append(step("S", old_x, qx, new_x))

        qy = q * y
        new_y = old_y - qy
        steps.append(step("M", q, y, qy))
        steps.append(step("S", old_y, qy, new_y))
        steps.append(step("BACK_SUB_ROW", f"r={new_r}",
                          f"x={new_x}", f"y={new_y}"))

        old_r, r = r, new_r
        old_x, x = x, new_x
        old_y, y = y, new_y
    return steps, old_r, old_x, old_y


class ModularInverseGenerator(ProblemGenerator):
    """
    Modular inverses and linear congruence solving.

    Variants:
    - inverse: find a^-1 modulo m when gcd(a, m) = 1
    - linear_congruence: solve ax congruent to b modulo m

    Op-codes used:
    - MOD_SETUP / GCD_RESULT: modular problem setup
    - EXT_GCD_SETUP / EUCLID_DIV / BACK_SUB_ROW: extended-Euclid trace
    - CONGRUENCE_REDUCE / CONGRUENCE_SOLUTIONS: linear congruence solving
    - MOD_NORMALIZE / MOD_INVERSE / MOD_REDUCE: residue arithmetic
    - M / S / D / CHECK (established): arithmetic verification
    - Z: inverse or solution classes
    """

    VARIANTS = ["inverse", "linear_congruence"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "inverse":
            problem, steps, answer, operation = self._generate_inverse()
        else:
            problem, steps, answer, operation = self._generate_linear()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_inverse(self):
        while True:
            modulus = random.randint(11, 70)
            a = random.randint(modulus + 1, 3 * modulus)
            if gcd(a, modulus) == 1:
                break
        steps = [
            step("MOD_SETUP", "inverse", f"a={a}", f"modulus={modulus}"),
        ]
        euclid_steps, g, x, _ = extended_trace(a, modulus)
        steps.extend(euclid_steps)
        steps.extend([
            step("GCD_RESULT", f"gcd({a},{modulus})", g),
            step("CHECK", "gcd = 1", "inverse exists"),
        ])
        inverse = x % modulus
        product = a * inverse
        reduced = product % modulus
        steps.extend([
            step("MOD_NORMALIZE", x, f"mod {modulus}", inverse),
            step("MOD_INVERSE", f"{a} mod {modulus}", inverse),
            step("M", a, inverse, product),
            step("MOD_REDUCE", product, f"mod {modulus}", reduced),
            step("CHECK", "a*inverse mod m", reduced),
        ])
        answer = f"{a}^-1 mod {modulus} = {inverse}"
        problem = f"Find the modular inverse of {a} modulo {modulus}."
        return problem, steps, answer, "modular_inverse"

    def _generate_linear(self):
        while True:
            d = random.randint(1, 4)
            reduced_modulus = random.randint(5, 18)
            reduced_residue = random.randint(2, reduced_modulus - 1)
            if gcd(reduced_residue, reduced_modulus) == 1:
                break
        reduced_a = reduced_residue + random.randint(1, 2) * reduced_modulus
        modulus = d * reduced_modulus
        a = d * reduced_a
        base_solution = random.randint(1, reduced_modulus - 1)
        b = (a * base_solution) % modulus
        reduced_b = b // d

        steps = [
            step("MOD_SETUP", "linear congruence", f"a={a}",
                 f"b={b}", f"modulus={modulus}"),
            step("GCD_RESULT", f"gcd({a},{modulus})", d),
            step("CHECK", f"{d} divides {b}", "solutions exist"),
            step("D", a, d, reduced_a),
            step("D", b, d, reduced_b),
            step("D", modulus, d, reduced_modulus),
            step("CONGRUENCE_REDUCE",
                 f"{reduced_a}x congruent to {reduced_b}",
                 f"mod {reduced_modulus}"),
        ]
        euclid_steps, g, x, _ = extended_trace(reduced_a, reduced_modulus)
        steps.extend(euclid_steps)
        inverse = x % reduced_modulus
        product = inverse * reduced_b
        base = product % reduced_modulus
        solutions = [base + k * reduced_modulus for k in range(d)]
        steps.extend([
            step("GCD_RESULT",
                 f"gcd({reduced_a},{reduced_modulus})", g),
            step("MOD_NORMALIZE", x, f"mod {reduced_modulus}", inverse),
            step("MOD_INVERSE",
                 f"{reduced_a} mod {reduced_modulus}", inverse),
            step("M", inverse, reduced_b, product),
            step("MOD_REDUCE", product, f"mod {reduced_modulus}", base),
            step("CONGRUENCE_SOLUTIONS", f"base {base}",
                 f"step {reduced_modulus}", list_text(solutions)),
        ])
        answer = f"solutions mod {modulus} = {list_text(solutions)}"
        problem = (
            f"Solve the linear congruence {a}x congruent to {b} "
            f"modulo {modulus}."
        )
        return problem, steps, answer, "linear_congruence"

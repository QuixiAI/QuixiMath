import random

from base_generator import ProblemGenerator
from helpers import step, jid


MODULI = [45, 63, 65, 77, 91, 99, 105, 143, 165]

PROBLEM_TEMPLATES = [
    "Compute the Jacobi symbol ({a}/{n}) using the standard reciprocity algorithm.",
    "Use quadratic reciprocity steps to evaluate Jacobi({a},{n}).",
    "Find the Jacobi symbol for a={a} and odd modulus n={n}.",
]


class JacobiSymbolGenerator(ProblemGenerator):
    """
    Jacobi symbol computation by the iterative reciprocity algorithm.

    Op-codes used:
    - JACOBI_SETUP / JACOBI_REDUCE / JACOBI_TWO_RULE
    - JACOBI_RECIPROCITY / JACOBI_SWAP / JACOBI_END
    - MOD_REDUCE / D (established/shared): reduction and powers of two
    - Z: Jacobi symbol value
    """

    def generate(self) -> dict:
        n = random.choice(MODULI)
        a = random.randint(2, 3 * n)
        value, steps = self._trace(a, n)
        answer = f"Jacobi({a},{n}) = {value}"
        problem = random.choice(PROBLEM_TEMPLATES).format(a=a, n=n)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="jacobi_symbol",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _trace(self, a, n):
        original_a = a
        original_n = n
        result = 1
        steps = [
            step("JACOBI_SETUP", f"a={a}", f"n={n}", "n odd"),
        ]
        a %= n
        steps.append(step("MOD_REDUCE", original_a, f"mod {n}", a))
        while a:
            while a % 2 == 0:
                before = a
                a //= 2
                steps.append(step("D", before, 2, a))
                if n % 8 in (3, 5):
                    result = -result
                    effect = "flip sign"
                else:
                    effect = "keep sign"
                steps.append(step("JACOBI_TWO_RULE", f"n mod 8 = {n % 8}",
                                  effect, f"sign {result}"))
            if a == 1:
                steps.append(step("JACOBI_END", "a=1", f"sign {result}"))
                return result, steps

            if a % 4 == 3 and n % 4 == 3:
                result = -result
                effect = "flip sign"
            else:
                effect = "keep sign"
            steps.append(step("JACOBI_RECIPROCITY",
                              f"a mod 4 = {a % 4}",
                              f"n mod 4 = {n % 4}", effect))
            a, n = n, a
            steps.append(step("JACOBI_SWAP", f"a={a}", f"n={n}",
                              f"sign {result}"))
            reduced = a % n
            steps.append(step("MOD_REDUCE", a, f"mod {n}", reduced))
            a = reduced
        final = result if n == 1 else 0
        reason = "n=1" if n == 1 else f"gcd({original_a},{original_n})>1"
        steps.append(step("JACOBI_END", reason, final))
        return final, steps

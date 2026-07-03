import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def term(coef, var, power, lead=False):
    """Sign-aware term: '2x^3', '+ 6x^2', '- 5x', '+ 15', leading '-x^3'."""
    mag = "" if abs(coef) == 1 and power > 0 else str(abs(coef))
    core = {0: mag or "1", 1: f"{mag}{var}"}.get(power, f"{mag}{var}^{power}")
    if power == 0:
        core = str(abs(coef))
    if lead:
        return core if coef > 0 else f"-{core}"
    return f"+ {core}" if coef > 0 else f"- {core}"


class FactorGroupingGenerator(ProblemGenerator):
    """
    Factors four-term cubics by grouping. Built from (ax + b)(cx² + d) with
    each factor primitive and the quadratic factor irreducible over the
    integers, so the grouping answer is the complete factorization.

    Op-codes used (shared with the ac-method generator):
    - POLY_SETUP: the four-term polynomial (string)
    - GROUP: the two grouped halves (group1, group2)
    - FACTOR_GROUP: factor one group (group, gcf, common binomial)
    - REWRITE: the factored form (string)
    - CHECK: expand back to the original (method, lhs, rhs)
    - Z: final answer
    """

    def generate(self) -> dict:
        var = random.choice(["x", "x", "x", "y", "n"])
        while True:
            a = random.randint(1, 3)
            b = random.choice([v for v in range(-6, 7) if v != 0])
            c = random.randint(1, 3)
            d = random.choice([v for v in range(-9, 10) if v != 0])
            if gcd(a, abs(b)) != 1 or gcd(c, abs(d)) != 1:
                continue
            # keep the quadratic factor irreducible over the integers
            if c == 1 and d < 0 and int((-d) ** 0.5) ** 2 == -d:
                continue
            break

        t3, t2, t1, t0 = a * c, b * c, a * d, b * d
        original = (f"{term(t3, var, 3, lead=True)} {term(t2, var, 2)} "
                    f"{term(t1, var, 1)} {term(t0, var, 0)}")

        lin_txt = f"({term(a, var, 1, lead=True)} {term(b, var, 0)})"
        quad_inner = f"{term(c, var, 2, lead=True)} {term(d, var, 0)}"
        quad_txt = f"({quad_inner})"
        factored = f"{lin_txt}{quad_txt}"

        g1 = f"{term(t3, var, 3, lead=True)} {term(t2, var, 2)}"
        g2 = f"{term(t1, var, 1, lead=True)} {term(t0, var, 0)}"
        gcf1 = f"{term(c, var, 2, lead=True)}"
        gcf2 = str(d)

        steps = [
            step("POLY_SETUP", original),
            step("GROUP", f"({g1})", f"({g2})"),
            step("FACTOR_GROUP", g1, gcf1, lin_txt),
            step("FACTOR_GROUP", g2, gcf2, lin_txt),
            step("REWRITE", factored),
            step("CHECK", "expand",
                 f"{term(t3, var, 3, lead=True)} {term(t1, var, 1)} "
                 f"{term(t2, var, 2)} {term(t0, var, 0)}", original),
            step("Z", factored),
        ]

        return dict(
            problem_id=jid(),
            operation="factor_by_grouping",
            problem=f"Factor by grouping: {original}",
            steps=steps,
            final_answer=factored,
        )

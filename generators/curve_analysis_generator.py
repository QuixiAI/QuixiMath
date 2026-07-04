import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search
from generators.polynomial_long_division_generator import poly_txt


class CurveAnalysisGenerator(ProblemGenerator):
    """
    Curve analysis on cubics engineered to have integer critical
    points (f' = 3(x - p)(x - q), p + q even so all coefficients and
    the inflection point are integers).

    Variants:
    - critical:   find both critical points (factor sweep), classify
                  each with the second derivative test
    - inflection: find the inflection point and the concavity
                  intervals from the sign of f''

    Op-codes used:
    - CURVE_SETUP: the function and the goal
    - POWER_RULE / REWRITE / FACTOR_GROUP / FACTOR_PAIR_GOAL / TRY /
      REJECT / ACCEPT / ZERO_PRODUCT (established)
    - SUBST / M / A / EVAL (established)
    - SECOND_DERIV_TEST: the sign verdict (value and sign, conclusion)
    - EQ_OP_BOTH / D: solving f'' = 0 (established)
    - Z: the classified points or the concavity summary
    """

    VARIANTS = ["critical", "inflection"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        while True:
            p = random.randint(-5, 3)
            q = random.randint(p + 2, 6)
            if (p + q) % 2 == 0 and p * q != 0 and p + q != 0:
                break
        C = random.randint(-8, 8)
        A2 = -3 * (p + q) // 2          # x² coefficient of f
        B = 3 * p * q
        f_coefs = [1, A2, B, C]
        f_txt = poly_txt(f_coefs, "x")
        d1 = [3, -3 * (p + q), 3 * p * q]
        d1_txt = poly_txt(d1, "x")
        mono = poly_txt([1, -(p + q), p * q], "x")
        mid = (p + q) // 2

        steps = [step("CURVE_SETUP", f"f(x) = {f_txt}",
                      "critical points and their nature"
                      if variant == "critical"
                      else "inflection point and concavity")]
        for c, n in zip(f_coefs, (3, 2, 1, 0)):
            if n >= 1 and c != 0:
                steps.append(step("POWER_RULE",
                                  poly_txt([c] + [0] * n, "x")
                                  .split(" ")[0],
                                  poly_txt([c * n] + [0] * (n - 1),
                                           "x").split(" ")[0]))
        steps.append(step("REWRITE", f"f'(x) = {d1_txt}"))

        if variant == "critical":
            steps.append(step("FACTOR_GROUP", d1_txt, 3, f"({mono})"))
            m, n = pair_search(steps, p * q, -(p + q))
            f1, f2 = binomial("x", m), binomial("x", n)
            steps.append(step("ZERO_PRODUCT", f"{f1}{f2} = 0",
                              f"x = {p} or x = {q}"))
            d2_txt = poly_txt([6, -3 * (p + q)], "x")
            steps.append(step("REWRITE", f"f''(x) = {d2_txt}"))
            results = []
            for r in (p, q):
                v = 6 * r - 3 * (p + q)
                wr = f"({r})" if r < 0 else str(r)
                steps.append(step("SUBST", "x", r,
                                  f"6{wr} - {3 * (p + q)}"
                                  if (p + q) > 0 else
                                  f"6{wr} + {-3 * (p + q)}"))
                steps.append(step("M", 6, r, 6 * r))
                steps.append(step("A", 6 * r, -3 * (p + q), v))
                kind = "local maximum" if v < 0 else "local minimum"
                steps.append(step("SECOND_DERIV_TEST",
                                  f"f''({r}) = {v} "
                                  f"{'<' if v < 0 else '>'} 0",
                                  f"{kind} at x = {r}"))
                results.append(f"local {'max' if v < 0 else 'min'} "
                               f"at x = {r}")
            answer = "; ".join(results)
            problem = (f"Find the critical points of f(x) = {f_txt} "
                       f"and classify each using the second derivative "
                       f"test.")
        else:
            d2_txt = poly_txt([6, -3 * (p + q)], "x")
            steps.append(step("REWRITE", f"f''(x) = {d2_txt}"))
            steps.append(step("EQ_OP_BOTH",
                              "add" if (p + q) > 0 else "subtract",
                              abs(3 * (p + q)), "6x", 3 * (p + q)))
            steps.append(step("D", 3 * (p + q), 6, mid))
            steps.append(step("SECOND_DERIV_TEST",
                              f"f'' < 0 for x < {mid}, f'' > 0 for "
                              f"x > {mid}", "concavity changes"))
            answer = (f"inflection at x = {mid}; concave down on "
                      f"(-∞, {mid}), concave up on ({mid}, ∞)")
            problem = (f"Find the inflection point of f(x) = {f_txt} "
                       f"and state where the curve is concave up and "
                       f"concave down.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"curve_analysis_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

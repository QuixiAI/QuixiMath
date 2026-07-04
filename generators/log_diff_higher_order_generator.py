import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.derivative_power_rule_generator import poly_pow, term_pow


class LogDiffHigherOrderGenerator(ProblemGenerator):
    """
    Two extensions of the derivative toolbox.

    Variants:
    - log_diff: y = x^(kx) (k = 1 gives the classic x^x) by
      logarithmic differentiation - take ln of both sides, pull the
      power out, differentiate implicitly, multiply back through
    - second / third: higher-order derivatives of a polynomial, each
      pass worked term by term with the power rule

    Op-codes used:
    - DERIV_SETUP / DERIV_RULE / POWER_RULE / M (established)
    - LOG_BOTH_SIDES / LOG_POWER (established)
    - IMPLICIT_DIFF / EQ_OP_BOTH / SUBST / REWRITE (established)
    - Z: the derivative
    """

    VARIANTS = ["log_diff", "second", "third"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "log_diff":
            k = random.choice([1, 1, 2, 3])
            y_txt = "x^x" if k == 1 else f"x^({k}x)"
            inner = "x ln x" if k == 1 else f"{k}x ln x"
            dprod = "ln x + 1" if k == 1 else f"{k}(ln x + 1)"
            answer = (f"y' = {y_txt}(ln x + 1)" if k == 1
                      else f"y' = {k}·{y_txt}(ln x + 1)")
            steps = [
                step("DERIV_SETUP", f"y = {y_txt}",
                     "y' by logarithmic differentiation"),
                step("LOG_BOTH_SIDES", f"ln y = ln({y_txt})"),
                step("LOG_POWER", f"ln({y_txt})", inner),
                step("IMPLICIT_DIFF", "d/dx of ln y", "y'/y"),
                step("DERIV_RULE", "product rule",
                     f"d/dx of {inner} = {dprod}"),
                step("REWRITE", f"y'/y = {dprod}"),
                step("EQ_OP_BOTH", "multiply", "y", "y'",
                     f"y·({dprod})"),
                step("SUBST", "y", y_txt, answer),
            ]
            problem = (f"Use logarithmic differentiation to find y' "
                       f"for y = {y_txt}.")
            op = "log_differentiation"
        else:
            order = 2 if variant == "second" else 3
            deg = random.randint(order + 1, 5)
            terms = [(random.choice([v for v in range(-6, 7) if v != 0]),
                      n) for n in range(deg, -1, -1)
                     if random.random() < 0.8 or n == deg]
            f_txt = poly_pow(terms)
            steps = [step("DERIV_SETUP", f"f(x) = {f_txt}",
                          f"f{chr(39) * order}(x)")]
            cur = terms
            for pass_n in range(order):
                nxt = []
                for c, n in cur:
                    if n == 0:
                        continue
                    if n != 1:
                        steps.append(step("M", c, n, c * n))
                    steps.append(step("POWER_RULE", term_pow(c, n),
                                      term_pow(c * n, n - 1)))
                    nxt.append((c * n, n - 1))
                cur = nxt
                steps.append(step("REWRITE",
                                  f"f{chr(39) * (pass_n + 1)}(x) = "
                                  f"{poly_pow(cur)}"))
            answer = f"f{chr(39) * order}(x) = {poly_pow(cur)}"
            problem = (f"Find the {'second' if order == 2 else 'third'} "
                       f"derivative of f(x) = {f_txt}.")
            op = f"derivative_order_{order}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

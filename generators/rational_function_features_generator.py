import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt
from generators.factor_trinomial_generator import binomial, pair_search


class RationalFunctionFeaturesGenerator(ProblemGenerator):
    """
    Reads the features of a rational function by hand: factor top and
    bottom, cancel a shared factor into a hole, the remaining
    denominator zeros become vertical asymptotes, and the horizontal
    asymptote comes from comparing degrees.

    Variants:
    - va_ha:    linear over factorable quadratic - two VAs, HA y = 0
    - hole:     shared linear factor - one hole, one VA, HA y = 1
    - ha_ratio: equal degrees - HA is the ratio of leading
      coefficients (a fraction), VAs from the factored denominator

    Op-codes used:
    - FUNC_SETUP: the function and the goal (established)
    - FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT: factor sweeps
      (established)
    - REWRITE: factored form (established)
    - CANCEL: shared factor removed (established)
    - HOLE: the hole left by a cancelled factor (x = h)
    - VA: one vertical asymptote (x = v)
    - DEGREE_COMPARE: degree comparison and its conclusion
      (comparison, conclusion)
    - HA: the horizontal asymptote (y = ...)
    - Z: 'VA: ...; hole at ...; HA: ...'
    """

    VARIANTS = ["va_ha", "hole", "ha_ratio"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = "x"
        fname = random.choice(["f", "g", "h"])

        p, q = sorted(random.sample([v for v in range(-5, 6) if v != 0], 2))
        den_quad = [1, -(p + q), p * q]
        if 0 in den_quad:
            return self.generate()
        den_txt = poly_txt(den_quad, var)

        if variant == "va_ha":
            while True:
                a = random.choice([v for v in range(-4, 5) if v != 0])
                b = random.choice([v for v in range(-9, 10) if v != 0])
                if a * p + b != 0 and a * q + b != 0:
                    break
            num_txt = poly_txt([a, b], var)
            rule = f"({num_txt})/({den_txt})"
            steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}",
                          "asymptotes and holes")]
            m, n = pair_search(steps, p * q, -(p + q))
            f1, f2 = binomial(var, m), binomial(var, n)
            steps.append(step("REWRITE",
                              f"({num_txt})/({f1}{f2})"))
            steps.append(step("VA", f"{var} = {p}"))
            steps.append(step("VA", f"{var} = {q}"))
            steps.append(step("DEGREE_COMPARE",
                              "deg num = 1 < deg den = 2", "y = 0"))
            steps.append(step("HA", "y = 0"))
            answer = (f"VA: {var} = {p}, {var} = {q}; HA: y = 0")
        elif variant == "hole":
            h = random.choice([v for v in range(-5, 6)
                               if v not in (0, p, q)])
            # numerator (x - h)(x - p), denominator (x - h)(x - q)
            num_quad = [1, -(h + p), h * p]
            den_quad = [1, -(h + q), h * q]
            if 0 in num_quad or 0 in den_quad:
                return self.generate()
            num_txt = poly_txt(num_quad, var)
            den_txt = poly_txt(den_quad, var)
            rule = f"({num_txt})/({den_txt})"
            steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}",
                          "asymptotes and holes")]
            m1, n1 = pair_search(steps, h * p, -(h + p))
            top = f"{binomial(var, m1)}{binomial(var, n1)}"
            steps.append(step("REWRITE", f"numerator = {top}"))
            m2, n2 = pair_search(steps, h * q, -(h + q))
            bot = f"{binomial(var, m2)}{binomial(var, n2)}"
            steps.append(step("REWRITE", f"denominator = {bot}"))
            shared = binomial(var, -h)
            steps.append(step("CANCEL", shared,
                              f"{binomial(var, -p)}/{binomial(var, -q)}"))
            steps.append(step("HOLE", f"{var} = {h}"))
            steps.append(step("VA", f"{var} = {q}"))
            steps.append(step("DEGREE_COMPARE",
                              "deg num = deg den = 2", "y = 1/1"))
            steps.append(step("HA", "y = 1"))
            answer = (f"VA: {var} = {q}; hole at {var} = {h}; HA: y = 1")
        else:
            a = random.choice([3, 4, 5, 6, 7])
            c = random.randint(1, 9)
            bden = random.choice([2, 3])
            if math.gcd(a, bden) != 1:  # keep the HA a proper fraction
                return self.generate()
            num_txt = poly_txt([a, 0, c], var)
            den_full = [bden, -bden * (p + q), bden * p * q]
            den_txt = poly_txt(den_full, var)
            rule = f"({num_txt})/({den_txt})"
            steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}",
                          "asymptotes and holes")]
            steps.append(step("REWRITE",
                              f"denominator = {bden}({poly_txt(den_quad, var)})"))
            m, n = pair_search(steps, p * q, -(p + q))
            f1, f2 = binomial(var, m), binomial(var, n)
            steps.append(step("REWRITE",
                              f"denominator = {bden}{f1}{f2}"))
            steps.append(step("VA", f"{var} = {p}"))
            steps.append(step("VA", f"{var} = {q}"))
            ha = Fraction(a, bden)
            steps.append(step("DEGREE_COMPARE",
                              "deg num = deg den = 2",
                              f"y = {a}/{bden}"))
            steps.append(step("HA", f"y = {ha}"))
            answer = (f"VA: {var} = {p}, {var} = {q}; HA: y = {ha}")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="rational_function_features",
            problem=(f"Find the vertical asymptotes, holes, and "
                     f"horizontal asymptote of {fname}({var}) = {rule}."),
            steps=steps,
            final_answer=answer,
        )

import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search


def lin(a, b, var):
    """Renders ax + b sign-aware, hiding unit coefficients."""
    head = {1: var, -1: f"-{var}"}.get(a, f"{a}{var}")
    if b == 0:
        return head
    return f"{head} + {b}" if b > 0 else f"{head} - {-b}"


class DomainRangeGenerator(ProblemGenerator):
    """
    Finds the domain of a function from its equation: exclude zero
    denominators, require radicands nonnegative (strictly positive when
    the radical is itself a denominator).

    Variants:
    - rational_linear:    f = num/(ax + b) -> one excluded value
    - rational_quadratic: f = num/(x^2 + Bx + C) -> factor (the usual
      TRY/REJECT/ACCEPT pair sweep), zero-product, two exclusions
    - rational_none:      f = num/(x^2 + c), c > 0 -> never zero,
      domain is all real numbers
    - radical:            f = sqrt(ax + b) -> solve ax + b >= 0, with the
      sign flip when dividing by a negative
    - radical_den:        f = num/sqrt(ax + b) -> strict: ax + b > 0
    - combined:           f = sqrt(x + p)/(x - q) -> radicand condition
      AND a denominator exclusion inside it

    Op-codes used:
    - FUNC_SETUP: the function and the goal (established)
    - DOMAIN_COND: one domain requirement (requirement, condition)
    - INEQ_OP_BOTH / INEQ_SIMPLIFY / INEQ_FLIP / INEQ_RESULT: solve the
      condition (established; '≠' rides along as a relation)
    - FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT: the factor pair sweep
    - REWRITE / ZERO_PRODUCT: factored condition (established)
    - DOMAIN_NOTE: why a denominator can never be zero (established)
    - Z: the domain, e.g. 'x ≠ 5', 'x ≥ -4, x ≠ 2', 'All real numbers'
    """

    VARIANTS = ["rational_linear", "rational_quadratic", "rational_none",
                "radical", "radical_den", "combined"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _numerator(var):
        if random.random() < 0.5:
            return str(random.randint(1, 9))
        n = random.choice([v for v in range(-9, 10) if v != 0])
        return f"({lin(1, n, var)})"

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        fname = random.choice(["f", "g", "h"])
        var = random.choice(["x", "x", "t"])
        return getattr(self, f"_{variant}")(fname, var)

    def _solve_ne(self, steps, a, b, r, var):
        """ax + b ≠ 0  ->  x ≠ r, using the two-step inequality flow."""
        head = {1: var, -1: f"-{var}"}.get(a, f"{a}{var}")
        if b != 0:
            op, v = ("subtract", b) if b > 0 else ("add", -b)
            steps.append(step("INEQ_OP_BOTH", op, abs(b), head, -b))
            steps.append(step("INEQ_SIMPLIFY", f"{head} ≠ {-b}"))
        if a != 1:
            steps.append(step("INEQ_OP_BOTH", "divide", a, var, r))
        steps.append(step("INEQ_RESULT", var, "≠", r))

    def _rational_linear(self, fname, var):
        a = random.choice([1, 1, 2, 3, -2])
        r = random.randint(-9, 9)
        b = -a * r
        den = lin(a, b, var)
        num = self._numerator(var)
        rule = f"{num}/({den})"
        steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}", "domain"),
                 step("DOMAIN_COND", "denominator ≠ 0", f"{den} ≠ 0")]
        self._solve_ne(steps, a, b, r, var)
        answer = f"{var} ≠ {r}"
        steps.append(step("Z", answer))
        return self._pack(fname, var, rule, steps, answer)

    def _rational_quadratic(self, fname, var):
        p, q = random.sample([v for v in range(-6, 7) if v != 0], 2)
        B, C = -(p + q), p * q
        den = f"{var}^2"
        if B != 0:
            bt = var if abs(B) == 1 else f"{abs(B)}{var}"
            den += f" + {bt}" if B > 0 else f" - {bt}"
        den += f" + {C}" if C > 0 else f" - {-C}"
        num = self._numerator(var)
        rule = f"{num}/({den})"
        steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}", "domain"),
                 step("DOMAIN_COND", "denominator ≠ 0", f"{den} ≠ 0")]
        m, n = pair_search(steps, C, B)
        f1, f2 = binomial(var, m), binomial(var, n)
        steps.append(step("REWRITE", f"{f1}{f2} ≠ 0"))
        steps.append(step("ZERO_PRODUCT", f"{f1}{f2} = 0",
                          f"{f1[1:-1]} = 0 or {f2[1:-1]} = 0"))
        lo, hi = sorted([-m, -n])
        steps.append(step("INEQ_RESULT", var, "≠", lo))
        steps.append(step("INEQ_RESULT", var, "≠", hi))
        answer = f"{var} ≠ {lo}, {var} ≠ {hi}"
        steps.append(step("Z", answer))
        return self._pack(fname, var, rule, steps, answer)

    def _rational_none(self, fname, var):
        c = random.randint(1, 9)
        den = f"{var}^2 + {c}"
        num = self._numerator(var)
        rule = f"{num}/({den})"
        steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}", "domain"),
                 step("DOMAIN_COND", "denominator ≠ 0", f"{den} ≠ 0"),
                 step("DOMAIN_NOTE", f"{var}^2 ≥ 0 for all {var}",
                      f"{den} ≥ {c}, never zero")]
        answer = "All real numbers"
        steps.append(step("Z", answer))
        return self._pack(fname, var, rule, steps, answer)

    def _solve_ineq(self, steps, a, b, m, var, rel):
        """ax + b rel 0 solved for x; rel is '≥' or '>'."""
        head = {1: var, -1: f"-{var}"}.get(a, f"{a}{var}")
        flipped = {"≥": "≤", ">": "<"}[rel]
        if b != 0:
            op = "subtract" if b > 0 else "add"
            steps.append(step("INEQ_OP_BOTH", op, abs(b), head, -b))
            steps.append(step("INEQ_SIMPLIFY", f"{head} {rel} {-b}"))
        if a < 0:
            steps.append(step("INEQ_FLIP",
                              "Dividing by negative number reverses "
                              "inequality"))
        if a != 1:
            steps.append(step("INEQ_OP_BOTH", "divide", a, var, m))
        final_rel = rel if a > 0 else flipped
        steps.append(step("INEQ_RESULT", var, final_rel, m))
        return final_rel

    def _radical(self, fname, var):
        a = random.choice([1, 1, 2, 3, -1, -2, -3])
        m = random.randint(-8, 8)
        b = -a * m
        radicand = lin(a, b, var)
        rule = f"√({radicand})"
        steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}", "domain"),
                 step("DOMAIN_COND", "radicand ≥ 0", f"{radicand} ≥ 0")]
        rel = self._solve_ineq(steps, a, b, m, var, "≥")
        answer = f"{var} {rel} {m}"
        steps.append(step("Z", answer))
        return self._pack(fname, var, rule, steps, answer)

    def _radical_den(self, fname, var):
        a = random.choice([1, 1, 2, 3, -1, -2, -3])
        m = random.randint(-8, 8)
        b = -a * m
        radicand = lin(a, b, var)
        num = random.choice([str(random.randint(1, 9)), var])
        rule = f"{num}/√({radicand})"
        steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}", "domain"),
                 step("DOMAIN_COND", "radicand in a denominator: > 0",
                      f"{radicand} > 0")]
        rel = self._solve_ineq(steps, a, b, m, var, ">")
        answer = f"{var} {rel} {m}"
        steps.append(step("Z", answer))
        return self._pack(fname, var, rule, steps, answer)

    def _combined(self, fname, var):
        p = random.randint(-6, 8)          # radicand x + p, domain x ≥ -p
        q = random.randint(-p + 1, -p + 9)  # exclusion inside the domain
        radicand = lin(1, p, var)
        den = lin(1, -q, var)
        rule = f"√({radicand})/({den})"
        steps = [step("FUNC_SETUP", f"{fname}({var}) = {rule}", "domain"),
                 step("DOMAIN_COND", "radicand ≥ 0", f"{radicand} ≥ 0")]
        self._solve_ineq(steps, 1, p, -p, var, "≥")
        steps.append(step("DOMAIN_COND", "denominator ≠ 0", f"{den} ≠ 0"))
        self._solve_ne(steps, 1, -q, q, var)
        answer = f"{var} ≥ {-p}, {var} ≠ {q}"
        steps.append(step("Z", answer))
        return self._pack(fname, var, rule, steps, answer)

    def _pack(self, fname, var, rule, steps, answer):
        return dict(
            problem_id=jid(),
            operation="function_domain",
            problem=f"Find the domain of {fname}({var}) = {rule}.",
            steps=steps,
            final_answer=answer,
        )

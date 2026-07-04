import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search


class LogEquationGenerator(ProblemGenerator):
    """
    Solves logarithmic equations with an explicit domain check on every
    candidate - the extraneous-solution trap is the point (A1).

    Variants:
    - basic:      log_b(ax + c) = d -> convert to exponential form,
                  solve the linear, check the argument is positive
    - product:    log_b(x) + log_b(x + k) = d -> condense, convert,
                  solve the quadratic; the negative candidate is
                  rejected as extraneous
    - both_sides: log_b(ax + c) = log_b(x + e) -> equate arguments;
                  some instances make the arguments negative at the
                  solution and the answer is 'No solution'

    Op-codes used:
    - EQ_SETUP / DOMAIN_NOTE: setup and the domain requirement
      (established)
    - LOG_PRODUCT: condense the sum (established)
    - LOG_FORM: log form <-> exponential form (established)
    - LOG_ONE_TO_ONE: equal bases -> equal arguments (equation)
    - E / EQ_OP_BOTH / D: arithmetic and solving (established)
    - FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT / ZERO_PRODUCT:
      quadratic path and candidate checks (established)
    - CHECK: substitute the solution into each argument (established)
    - Z: 'x = ...' or 'No solution'
    """

    VARIANTS = ["basic", "product", "both_sides"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    @staticmethod
    def _lin(a, c):
        head = "x" if a == 1 else f"{a}x"
        if c == 0:
            return head
        return f"{head} + {c}" if c > 0 else f"{head} - {-c}"

    def _basic(self):
        b = random.choice([2, 3, 5, 10])
        cap = {2: 6, 3: 4, 5: 3, 10: 3}[b]
        while True:
            d = random.randint(1, cap)
            a = random.choice([1, 2, 3])
            x0 = random.randint(-5, 12)
            c = b ** d - a * x0
            if -9 <= c <= 9 and c != 0:
                break
        arg = self._lin(a, c)
        eq = f"log_{b}({arg}) = {d}"
        rhs = b ** d
        steps = [
            step("EQ_SETUP", eq, "solve"),
            step("DOMAIN_NOTE", f"{arg} > 0", "argument must be positive"),
            step("LOG_FORM", f"log_{b}({arg}) = {d} ⟺ {arg} = {b}^{d}"),
            step("E", b, d, rhs),
        ]
        lhs_var = "x" if a == 1 else f"{a}x"
        if c != 0:
            op, v = ("subtract", c) if c > 0 else ("add", -c)
            steps.append(step("EQ_OP_BOTH", op, abs(c), lhs_var, rhs - c))
        if a > 1:
            steps.append(step("EQ_OP_BOTH", "divide", a, "x", x0))
        steps.append(step("CHECK", "domain",
                          f"{arg} = {rhs} > 0 at x = {x0}", "valid"))
        answer = f"x = {x0}"
        steps.append(step("Z", answer))
        return self._pack("log_eq_basic", f"Solve: {eq}.", steps, answer)

    def _product(self):
        combos = []
        for b, dmax in ((2, 6), (3, 4), (10, 2)):
            for d in range(2, dmax + 1):
                N = b ** d
                for p in range(1, int(N ** 0.5) + 1):
                    if N % p == 0 and N // p > p:
                        combos.append((b, d, p, N // p - p))
        b, d, p, k = random.choice(combos)
        N = b ** d
        other = -(p + k)
        eq = f"log_{b}(x) + log_{b}({self._lin(1, k)}) = {d}"
        steps = [
            step("EQ_SETUP", eq, "solve"),
            step("DOMAIN_NOTE", f"x > 0 and x + {k} > 0",
                 "arguments must be positive"),
            step("LOG_PRODUCT", f"log_{b}(x) + log_{b}(x + {k})",
                 f"log_{b}(x(x + {k}))"),
            step("LOG_FORM",
                 f"log_{b}(x(x + {k})) = {d} ⟺ x(x + {k}) = {b}^{d}"),
            step("E", b, d, N),
            step("REWRITE", f"x^2 + {k}x - {N} = 0"),
        ]
        m, n = pair_search(steps, -N, k)
        f1, f2 = binomial("x", m), binomial("x", n)
        steps.append(step("REWRITE", f"{f1}{f2} = 0"))
        steps.append(step("ZERO_PRODUCT", f"{f1}{f2} = 0",
                          f"{f1[1:-1]} = 0 or {f2[1:-1]} = 0"))
        steps.append(step("TRY", f"x = {p}",
                          f"arguments {p} > 0 and {p + k} > 0"))
        steps.append(step("ACCEPT", f"x = {p}", "both logs defined"))
        steps.append(step("TRY", f"x = {other}",
                          f"log_{b}({other}) undefined"))
        steps.append(step("REJECT", f"x = {other}",
                          "argument negative, extraneous"))
        answer = f"x = {p}"
        steps.append(step("Z", answer))
        return self._pack("log_eq_product", f"Solve: {eq}.", steps, answer)

    def _both_sides(self):
        b = random.choice([2, 3, 5, 10])
        while True:
            a = random.choice([2, 3, 4])
            x0 = random.choice([v for v in range(-9, 13) if v != 0])
            e = random.randint(-9, 9)
            c = x0 + e - a * x0
            if not (-9 <= c <= 9) or c == 0 or e == c:
                continue
            v = x0 + e  # both arguments equal v at the solution
            if v != 0:
                break
        arg1, arg2 = self._lin(a, c), self._lin(1, e)
        eq = f"log_{b}({arg1}) = log_{b}({arg2})"
        steps = [
            step("EQ_SETUP", eq, "solve"),
            step("DOMAIN_NOTE", f"{arg1} > 0 and {arg2} > 0",
                 "arguments must be positive"),
            step("LOG_ONE_TO_ONE", f"{arg1} = {arg2}"),
        ]
        # solve ax + c = x + e
        diff = a - 1
        steps.append(step("EQ_OP_BOTH", "subtract", "x",
                          self._lin(diff, c), e))
        steps.append(step("EQ_OP_BOTH",
                          "subtract" if c > 0 else "add", abs(c),
                          f"{diff}x" if diff > 1 else "x", e - c))
        if diff > 1:
            steps.append(step("EQ_OP_BOTH", "divide", diff, "x", x0))
        if v > 0:
            steps.append(step("CHECK", "domain",
                              f"both arguments equal {v} > 0", "valid"))
            answer = f"x = {x0}"
        else:
            steps.append(step("CHECK", "domain",
                              f"both arguments equal {v} ≤ 0",
                              "extraneous"))
            steps.append(step("REJECT", f"x = {x0}",
                              "logs of non-positive numbers undefined"))
            answer = "No solution"
        steps.append(step("Z", answer))
        return self._pack("log_eq_both_sides", f"Solve: {eq}.", steps,
                          answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

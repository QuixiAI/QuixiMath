import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


class RiemannSumGenerator(ProblemGenerator):
    """
    Riemann sums and the trapezoidal rule as pure tables: Δx computed,
    every sample point evaluated in its own step, the values summed
    left to right, and the final scaling by Δx (or Δx/2).

    Variants: left, right, midpoint (Δx = 2 so midpoints stay
    integers), trapezoid (interior values doubled explicitly).

    Op-codes used:
    - RIEMANN_SETUP: function, interval, n, and method
    - S / D / EVAL: Δx (established)
    - SUBST / E / M / A: the table and the sum (established)
    - Z: the sum (exact decimal when Δx/2 introduces halves)
    """

    VARIANTS = ["left", "right", "midpoint", "trapezoid"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        kind = random.choice(["sq", "sqc", "lin"])
        c = random.choice([v for v in range(-5, 6) if v != 0])
        if kind == "sq":
            f_txt = "x^2"

            def f(x):
                return x * x
        elif kind == "sqc":
            f_txt = f"x^2 {'+' if c > 0 else '-'} {abs(c)}"

            def f(x):
                return x * x + c
        else:
            m = random.choice([2, 3, 4])
            f_txt = f"{m}x {'+' if c > 0 else '-'} {abs(c)}"

            def f(x):
                return m * x + c

        n = 4
        dx = 2 if variant == "midpoint" else random.choice([1, 2])
        a = random.randint(-2, 2)
        b = a + n * dx

        if variant == "left":
            pts = [a + i * dx for i in range(n)]
        elif variant == "right":
            pts = [a + (i + 1) * dx for i in range(n)]
        elif variant == "midpoint":
            pts = [a + i * dx + dx // 2 for i in range(n)]
        else:
            pts = [a + i * dx for i in range(n + 1)]

        steps = [
            step("RIEMANN_SETUP",
                 f"f(x) = {f_txt} on [{a}, {b}], n = {n}",
                 f"{variant} {'Riemann sum' if variant != 'trapezoid' else 'rule'}"),
            step("S", b, a, b - a),
            step("D", b - a, n, dx),
            step("EVAL", "Δx", dx),
        ]
        vals = []
        for x in pts:
            fx = f(x)
            steps.append(step("EVAL", f"f({x})", fx))
            vals.append(fx)

        if variant == "trapezoid":
            weighted = [vals[0]]
            for v in vals[1:-1]:
                steps.append(step("M", 2, v, 2 * v))
                weighted.append(2 * v)
            weighted.append(vals[-1])
            acc = weighted[0]
            for v in weighted[1:]:
                steps.append(step("A", acc, v, acc + v))
                acc += v
            total = Fraction(dx, 2) * acc
            steps.append(step("M", dec(Fraction(dx, 2)), acc,
                              dec(total)))
            answer = dec(total)
        else:
            acc = vals[0]
            for v in vals[1:]:
                steps.append(step("A", acc, v, acc + v))
                acc += v
            total = acc * dx
            steps.append(step("M", acc, dx, total))
            answer = str(total)
        steps.append(step("Z", answer))

        method = {"left": "left Riemann sum",
                  "right": "right Riemann sum",
                  "midpoint": "midpoint Riemann sum",
                  "trapezoid": "trapezoidal rule"}[variant]
        return dict(
            problem_id=jid(),
            operation=f"riemann_{variant}",
            problem=(f"Approximate ∫ from {a} to {b} of ({f_txt}) dx "
                     f"using the {method} with n = {n}."),
            steps=steps,
            final_answer=answer,
        )

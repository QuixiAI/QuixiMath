import random
from base_generator import ProblemGenerator
from helpers import step, jid

CORES = [2, 3, 5, 6, 7, 10, 13, 15]


def rad(coef, f):
    """'5√2', '√3', or plain integer when f == 1."""
    if f == 1:
        return str(coef)
    if coef == 1:
        return f"√{f}"
    return f"{coef}√{f}"


def split_square(n):
    """n -> (s, f) with n = s²·f and f square-free-largest."""
    s = 1
    for cand in range(1, int(n ** 0.5) + 1):
        if n % (cand * cand) == 0:
            s = cand
    return s, n // (s * s)


class RadicalMultiplyGenerator(ProblemGenerator):
    """
    Multiplies radicals: √a · √b = √(ab), then simplify what appears.

    Variants:
    - product:    a√m · b√n — multiply coefficients and radicands, simplify
    - square:     (a√m)² — integer result
    - distribute: √m(b + c√m) — distribute, √m·√m collapses to m
    - binomial:   (a + √m)(b + √m) — FOIL with a shared radical

    Op-codes used:
    - ROOT_SETUP: the expression (string)
    - FORM_IDENTIFY: the radical product rule (name, formula)
    - M: multiply coefficients / radicands / radical pairs (x, y, product)
    - DIST: distribute over the sum (factor, expression, result)
    - SQUARE_FACTOR / ROOT: simplify the product radical (shared codes)
    - REWRITE: current form (string)
    - Z: final answer
    """

    VARIANTS = ["product", "square", "distribute", "binomial"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _product(self):
        m, n = random.choice(CORES), random.choice(CORES)
        a, b = random.randint(1, 5), random.randint(1, 5)
        original = f"{rad(a, m)} · {rad(b, n)}"
        steps = [
            step("ROOT_SETUP", original),
            step("FORM_IDENTIFY", "product_of_radicals",
                 "√a · √b = √(ab)"),
        ]
        if a * b > 1:
            steps.append(step("M", a, b, a * b))
        steps.append(step("M", m, n, m * n))
        steps.append(step("REWRITE", rad(a * b, m * n)
                          if m * n > 1 else str(a * b)))
        s, f = split_square(m * n)
        if s > 1:
            steps.append(step("SQUARE_FACTOR", m * n, f"{s * s} × {f}",
                              s * s))
            steps.append(step("ROOT", s * s, s))
            if s * s != m * n:
                steps.append(step("M", a * b, s, a * b * s))
            answer = rad(a * b * s, f)
            steps.append(step("REWRITE", answer))
        else:
            answer = rad(a * b, m * n)
        steps.append(step("Z", answer))
        return self._pack("radical_multiply", original, steps, answer)

    def _square(self):
        m = random.choice(CORES)
        a = random.randint(2, 6)
        original = f"({rad(a, m)})^2"
        value = a * a * m
        steps = [
            step("ROOT_SETUP", original),
            step("FORM_IDENTIFY", "square_of_radical",
                 "(a√b)^2 = a^2 · b"),
            step("E", a, 2, a * a),
            step("M", a * a, m, value),
            step("Z", str(value)),
        ]
        return self._pack("radical_multiply", original, steps, str(value))

    def _distribute(self):
        m = random.choice(CORES)
        b, c = random.randint(2, 6), random.randint(2, 6)
        original = f"√{m}({b} + {c}√{m})"
        rational = c * m
        answer = f"{rational} + {rad(b, m)}"
        steps = [
            step("ROOT_SETUP", original),
            step("DIST", f"√{m}", f"{b} + {c}√{m}",
                 f"{b}√{m} + {c}√{m}·√{m}"),
            step("M", f"√{m}", f"√{m}", str(m)),
            step("M", c, m, rational),
            step("REWRITE", answer),
            step("Z", answer),
        ]
        return self._pack("radical_multiply", original, steps, answer)

    def _binomial(self):
        m = random.choice(CORES)
        a, b = random.randint(1, 6), random.randint(1, 6)
        original = f"({a} + √{m})({b} + √{m})"
        rational = a * b + m
        rad_coef = a + b
        answer = f"{rational} + {rad(rad_coef, m)}"
        steps = [
            step("ROOT_SETUP", original),
            step("FOIL_SETUP", original),
            step("M", a, b, a * b),
            step("M", a, f"√{m}", rad(a, m)),
            step("M", f"√{m}", b, rad(b, m)),
            step("M", f"√{m}", f"√{m}", str(m)),
            step("REWRITE", f"{a * b} + {rad(a, m)} + {rad(b, m)} + {m}"),
            step("A", a * b, m, rational),
            step("A", rad(a, m), rad(b, m), rad(rad_coef, m)),
            step("REWRITE", answer),
            step("Z", answer),
        ]
        return self._pack("radical_multiply", original, steps, answer)

    @staticmethod
    def _pack(op, original, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=f"Multiply and simplify: {original}",
            steps=steps,
            final_answer=answer,
        )

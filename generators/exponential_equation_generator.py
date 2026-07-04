import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class ExponentialEquationGenerator(ProblemGenerator):
    """
    Solves exponential equations: by matching bases when the right side
    is a power of the base (equate exponents, solve the linear), and by
    taking logs when it is not (the answer stays exact, e.g.
    x = log_5(17) or x = ln(10)/2).

    Variants:
    - same_base:   b^(ax + c) = b^d, sometimes behind a multiplier that
                   must be divided away first
    - common_base: B1^x = B2 with both powers of one prime; fractional
                   answers like x = 3/2
    - log_exact:   b^x = C with C not a power of b -> x = log_b(C)
    - ln_exact:    e^(ax) = C -> x = ln(C)/a

    Op-codes used:
    - EQ_SETUP: the equation (established)
    - D: divide away a multiplier (established)
    - E: justify the power rewrite (established)
    - REWRITE: right side as a power of the base (established)
    - EQUATE_EXP: same base on both sides -> equate exponents
      (new: the resulting linear equation)
    - EQ_OP_BOTH: solve the linear (established)
    - LOG_BOTH_SIDES: take log_b (or ln) of both sides (statement)
    - LOG_IDENT: log_b(b^u) = u (established)
    - Z: exact answer
    """

    VARIANTS = ["same_base", "common_base", "log_exact", "ln_exact"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _same_base(self):
        b = random.choice([2, 3, 5])
        cap = {2: 8, 3: 5, 5: 4}[b]
        while True:
            x0 = random.randint(-3, 5)
            a = random.randint(1, 3)
            c = random.randint(-4, 4)
            d = a * x0 + c
            if 1 <= d <= cap:
                break
        rhs = b ** d
        exp_txt = (f"{a}x" if a > 1 else "x") + \
            (f" + {c}" if c > 0 else (f" - {-c}" if c < 0 else ""))
        isolate = random.random() < 0.35
        steps = []
        if isolate:
            m = random.choice([2, 3, 4, 5, 6, 7])
            eq = f"{m} · {b}^({exp_txt}) = {m * rhs}"
            steps.append(step("EQ_SETUP", eq, "solve"))
            steps.append(step("D", m * rhs, m, rhs))
            steps.append(step("REWRITE", f"{b}^({exp_txt}) = {rhs}"))
        else:
            eq = f"{b}^({exp_txt}) = {rhs}"
            steps.append(step("EQ_SETUP", eq, "solve"))
        steps.append(step("E", b, d, rhs))
        steps.append(step("REWRITE", f"{rhs} = {b}^{d}"))
        steps.append(step("EQUATE_EXP", f"{exp_txt} = {d}"))
        lhs_var = f"{a}x" if a > 1 else "x"
        if c != 0:
            op, v = ("subtract", c) if c > 0 else ("add", -c)
            steps.append(step("EQ_OP_BOTH", op, abs(c), lhs_var, d - c))
        if a > 1:
            steps.append(step("EQ_OP_BOTH", "divide", a, "x", x0))
        answer = f"x = {x0}"
        steps.append(step("Z", answer))
        return self._pack("exponential_eq_same_base", f"Solve: {eq}.",
                          steps, answer)

    def _common_base(self):
        p, u, v = random.choice([
            (2, 2, 3), (2, 3, 2), (2, 2, 5), (2, 5, 2), (2, 3, 5),
            (2, 5, 3), (2, 3, 4), (2, 2, 7), (3, 2, 3), (3, 3, 2),
            (5, 2, 3), (5, 3, 2)])
        B1, B2 = p ** u, p ** v
        x = Fraction(v, u)
        eq = f"{B1}^x = {B2}"
        steps = [
            step("EQ_SETUP", eq, "solve"),
            step("E", p, u, B1),
            step("REWRITE", f"{B1} = {p}^{u}"),
            step("E", p, v, B2),
            step("REWRITE", f"{B2} = {p}^{v}"),
            step("REWRITE", f"{p}^({u}x) = {p}^{v}"),
            step("EQUATE_EXP", f"{u}x = {v}"),
            step("D", v, u, x),
        ]
        answer = f"x = {x}"
        steps.append(step("Z", answer))
        return self._pack("exponential_eq_common_base", f"Solve: {eq}.",
                          steps, answer)

    def _log_exact(self):
        b = random.choice([2, 3, 5, 7, 10])
        while True:
            C = random.randint(5, 60)
            L = math.log(C, b)
            if abs(L - round(L)) > 1e-9:
                break
        eq = f"{b}^x = {C}"
        answer = f"x = log_{b}({C})"
        steps = [
            step("EQ_SETUP", eq, "solve; exact answer"),
            step("LOG_BOTH_SIDES", f"log_{b}({b}^x) = log_{b}({C})"),
            step("LOG_IDENT", f"log_{b}({b}^x) = x", "x"),
            step("Z", answer),
        ]
        return self._pack("exponential_eq_log", f"Solve: {eq}. Give the "
                          f"exact answer.", steps, answer)

    def _ln_exact(self):
        a = random.randint(1, 4)
        C = random.randint(5, 50)
        exp_txt = f"{a}x" if a > 1 else "x"
        eq = f"e^({exp_txt}) = {C}" if a > 1 else f"e^x = {C}"
        steps = [
            step("EQ_SETUP", eq, "solve; exact answer"),
            step("LOG_BOTH_SIDES", f"ln(e^({exp_txt})) = ln({C})"),
            step("LOG_IDENT", f"ln(e^({exp_txt})) = {exp_txt}", exp_txt),
        ]
        if a > 1:
            answer = f"x = ln({C})/{a}"
            steps.append(step("EQ_OP_BOTH", "divide", a, "x",
                              f"ln({C})/{a}"))
        else:
            answer = f"x = ln({C})"
        steps.append(step("Z", answer))
        return self._pack("exponential_eq_ln", f"Solve: {eq}. Give the "
                          f"exact answer.", steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

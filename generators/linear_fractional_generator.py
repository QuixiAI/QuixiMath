import random
from fractions import Fraction
from math import lcm

from base_generator import ProblemGenerator
from helpers import step, jid


def fstr(fr):
    """Renders a Fraction: '19/6', '-2/3', or '7' when the denominator is 1."""
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"


class LinearFractionalGenerator(ProblemGenerator):
    """
    Linear equations and inequalities with fraction or decimal coefficients,
    solved the way it's taught: clear the fractions/decimals first (multiply
    every term by the LCD or by 10), then solve the resulting integer
    two-step problem. Inequalities flip when dividing by a negative.

    Variants (operation strings):
    - linear_eq_fractions,  linear_ineq_fractions
    - linear_eq_decimals,   linear_ineq_decimals

    Op-codes used:
    - EQ_SETUP / INEQ_SETUP: the original problem (string)
    - L: least common multiple of two denominators (d1, d2, lcm)
    - MUL_TERM: multiply one term by the clearing factor (factor, term, result)
    - REWRITE: the cleared integer equation/inequality (string)
    - EQ_OP_BOTH / INEQ_OP_BOTH: (verb, value, left_side, new_right)
    - EQ_SIMPLIFY: current form after an operation (string)
    - INEQ_FLIP: note the direction flip (reason)
    - EQ_RESULT (var, value) / INEQ_RESULT (var, relation, value)
    - CHECK: substitute the solution/boundary back (method, lhs_work, rhs)
    - Z: final answer
    """

    DENOMS = [2, 3, 4, 5, 6, 8, 10, 12]
    RELATIONS = ['<', '>', '≤', '≥']
    FLIPPED = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}

    def __init__(self, problem_type=None):
        valid = ["fractions", "decimals", None]
        if problem_type not in valid:
            raise ValueError(f"problem_type must be one of {valid}")
        self.problem_type = problem_type

    # ---------- helpers ----------

    def _pick_fraction(self):
        """A non-integer fraction with a small denominator, in lowest terms."""
        while True:
            den = random.choice(self.DENOMS)
            num = random.randint(-9, 9)
            fr = Fraction(num, den)
            if num != 0 and fr.denominator != 1:
                return fr

    def _solve_cleared(self, steps, A, B, C, rel):
        """Solve A·x + B (rel) C in integers; emits steps, returns answer str.

        rel is None for equations. x0 = (C - B) / A is an integer by
        construction. Returns the final answer string.
        """
        is_ineq = rel is not None
        x0 = (C - B) // A
        rel_out = rel

        if B != 0:
            verb = "subtract" if B > 0 else "add"
            steps.append(step("INEQ_OP_BOTH" if is_ineq else "EQ_OP_BOTH",
                              verb, abs(B), f"{A}x", C - B))
            mid = f"{A}x {rel} {C - B}" if is_ineq else f"{A}x = {C - B}"
            steps.append(step("INEQ_SIMPLIFY" if is_ineq else "EQ_SIMPLIFY",
                              mid))

        steps.append(step("INEQ_OP_BOTH" if is_ineq else "EQ_OP_BOTH",
                          "divide", A, "x", x0))
        if is_ineq and A < 0:
            rel_out = self.FLIPPED[rel]
            steps.append(step("INEQ_FLIP",
                              "Dividing by negative number reverses inequality"))

        if is_ineq:
            steps.append(step("INEQ_RESULT", "x", rel_out, x0))
            return f"x {rel_out} {x0}", x0
        steps.append(step("EQ_RESULT", "x", x0))
        return str(x0), x0

    # ---------- variants ----------

    def _fraction_problem(self, is_ineq):
        af = self._pick_fraction()
        bf = self._pick_fraction()
        x0 = random.randint(-12, 12)
        rhs = af * x0 + bf
        rel = random.choice(self.RELATIONS) if is_ineq else "="

        sign = "+" if bf > 0 else "-"
        lhs_txt = f"({fstr(af)})x {sign} {fstr(abs(bf))}"
        original = f"{lhs_txt} {rel} {fstr(rhs)}"

        steps = [step("INEQ_SETUP" if is_ineq else "EQ_SETUP", original)]

        # LCD via chained lcms (a human folds one pair at a time).
        l12 = lcm(af.denominator, bf.denominator)
        steps.append(step("L", af.denominator, bf.denominator, l12))
        L = lcm(l12, rhs.denominator)
        if L != l12:
            steps.append(step("L", l12, rhs.denominator, L))

        A = int(af * L)
        B = int(bf * L)
        C = int(rhs * L)
        steps.append(step("MUL_TERM", L, f"({fstr(af)})x", f"{A}x"))
        steps.append(step("MUL_TERM", L, f"{sign} {fstr(abs(bf))}".replace("+ ", ""),
                          B))
        steps.append(step("MUL_TERM", L, fstr(rhs), C))
        bsign = "+" if B > 0 else "-"
        steps.append(step("REWRITE", f"{A}x {bsign} {abs(B)} {rel} {C}"))

        answer, x_sol = self._solve_cleared(steps, A, B, C,
                                            rel if is_ineq else None)

        # Verify: substituting x0 (the boundary, for inequalities) reproduces
        # the right-hand side exactly.
        lhs_val = af * x_sol + bf
        method = "boundary_equality" if is_ineq else "substitute"
        work = (f"({fstr(af)})({x_sol}) {sign} {fstr(abs(bf))} = {fstr(lhs_val)}")
        steps.append(step("CHECK", method, work, fstr(rhs)))
        steps.append(step("Z", answer))

        op = "linear_ineq_fractions" if is_ineq else "linear_eq_fractions"
        verb = "Solve the inequality" if is_ineq else "Solve for x"
        return dict(problem_id=jid(), operation=op,
                    problem=f"{verb}: {original}",
                    steps=steps, final_answer=answer)

    def _decimal_problem(self, is_ineq):
        # One-decimal-place coefficients; ×10 clears everything.
        def tenth():
            while True:
                k = random.randint(-99, 99)
                if k != 0 and k % 10 != 0:
                    return k

        ka, kb = tenth(), tenth()
        x0 = random.randint(-12, 12)
        kc = ka * x0 + kb  # rhs in tenths
        rel = random.choice(self.RELATIONS) if is_ineq else "="

        a_txt, b_abs = f"{ka / 10:.1f}", f"{abs(kb) / 10:.1f}"
        c_txt = f"{kc / 10:.1f}"
        sign = "+" if kb > 0 else "-"
        original = f"{a_txt}x {sign} {b_abs} {rel} {c_txt}"

        steps = [step("INEQ_SETUP" if is_ineq else "EQ_SETUP", original)]
        steps.append(step("MUL_TERM", 10, f"{a_txt}x", f"{ka}x"))
        steps.append(step("MUL_TERM", 10, f"{sign} {b_abs}".replace("+ ", ""), kb))
        steps.append(step("MUL_TERM", 10, c_txt, kc))
        bsign = "+" if kb > 0 else "-"
        steps.append(step("REWRITE", f"{ka}x {bsign} {abs(kb)} {rel} {kc}"))

        answer, x_sol = self._solve_cleared(steps, ka, kb, kc,
                                            rel if is_ineq else None)

        lhs_val = Fraction(ka, 10) * x_sol + Fraction(kb, 10)
        check_val = f"{float(lhs_val):.1f}"
        method = "boundary_equality" if is_ineq else "substitute"
        work = f"{a_txt}({x_sol}) {sign} {b_abs} = {check_val}"
        steps.append(step("CHECK", method, work, c_txt))
        steps.append(step("Z", answer))

        op = "linear_ineq_decimals" if is_ineq else "linear_eq_decimals"
        verb = "Solve the inequality" if is_ineq else "Solve for x"
        return dict(problem_id=jid(), operation=op,
                    problem=f"{verb}: {original}",
                    steps=steps, final_answer=answer)

    def generate(self) -> dict:
        kind = self.problem_type or random.choice(["fractions", "decimals"])
        is_ineq = random.random() < 0.5
        if kind == "fractions":
            return self._fraction_problem(is_ineq)
        return self._decimal_problem(is_ineq)

import random
from base_generator import ProblemGenerator
from helpers import step, jid


def sgn_num(n):
    """Renders a signed number for work strings: '6' or '(-1)'."""
    return f"({n})" if n < 0 else str(n)


def binomial(var, r):
    """Renders (x + r) sign-aware: '(x + 2)', '(x - 4)'."""
    return f"({var} + {r})" if r > 0 else f"({var} - {-r})"


class FactorTrinomialGenerator(ProblemGenerator):
    """
    Factors monic trinomials x² + bx + c by the find-two-numbers method,
    SHOWING the trial-and-error (A2): divisor pairs of c are tried in
    ascending order with the human sign heuristic (the bigger number takes
    b's sign), each miss is rejected with its reason, and the winner is
    accepted — then verified by FOIL expansion (A1).

    Op-codes used:
    - POLY_SETUP: the trinomial (string)
    - FACTOR_PAIR_GOAL: what the two numbers must satisfy (product, sum)
    - TRY: test a candidate pair (candidate, test_work)
    - REJECT: candidate fails (candidate, reason)
    - ACCEPT: candidate works (candidate, confirmation)
    - REWRITE: the factored form (string)
    - CHECK: FOIL the answer back to the original (method, lhs, rhs)
    - Z: final answer
    """

    def generate(self) -> dict:
        var = random.choice(["x", "x", "x", "y", "n"])
        while True:
            p = random.choice([n for n in range(-9, 10) if n != 0])
            q = random.choice([n for n in range(-9, 10) if n != 0])
            if p != q and p + q != 0:
                break
        p, q = sorted((p, q))
        b, c = p + q, p * q

        b_abs = "" if abs(b) == 1 else str(abs(b))
        b_txt = f"+ {b_abs}{var}" if b > 0 else f"- {b_abs}{var}"
        c_txt = f"+ {c}" if c > 0 else f"- {-c}"
        original = f"{var}^2 {b_txt} {c_txt}"

        steps = [step("POLY_SETUP", original)]
        steps.append(step("FACTOR_PAIR_GOAL", f"m·n = {c}", f"m + n = {b}"))

        # Divisor pairs of |c| in ascending order, signed per the human
        # heuristic; stop at the winner.
        for d in range(1, abs(c) + 1):
            if d * d > abs(c):
                break
            if abs(c) % d != 0:
                continue
            big = abs(c) // d
            if c > 0:
                m, n = (d, big) if b > 0 else (-d, -big)
            else:
                m, n = (-d, big) if b > 0 else (d, -big)
            s = m + n
            work = f"{sgn_num(m)}·{sgn_num(n)}={c}, {sgn_num(m)}+{sgn_num(n)}={s}"
            steps.append(step("TRY", f"({m}, {n})", work))
            if s == b:
                steps.append(step("ACCEPT", f"({m}, {n})",
                                  f"product {c} ✓, sum {b} ✓"))
                break
            steps.append(step("REJECT", f"({m}, {n})", f"sum is {s}, need {b}"))

        factored = f"{binomial(var, p)}{binomial(var, q)}"
        steps.append(step("REWRITE", factored))

        q_abs = "" if abs(q) == 1 else str(abs(q))
        p_abs = "" if abs(p) == 1 else str(abs(p))
        mid1 = f"+ {q_abs}{var}" if q > 0 else f"- {q_abs}{var}"
        mid2 = f"+ {p_abs}{var}" if p > 0 else f"- {p_abs}{var}"
        foil = f"{var}^2 {mid1} {mid2} {c_txt}"
        steps.append(step("CHECK", "foil", foil, original))
        steps.append(step("Z", factored))

        return dict(
            problem_id=jid(),
            operation="factor_trinomial",
            problem=f"Factor: {original}",
            steps=steps,
            final_answer=factored,
        )

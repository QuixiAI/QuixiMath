import random
from base_generator import ProblemGenerator
from helpers import step, jid


def lin(m, c, var="x"):
    """Renders m·x + c sign-aware: '4x + 12', '4x - 3', '4x', '12'."""
    if m == 0:
        return str(c)
    mtxt = f"{var}" if m == 1 else f"-{var}" if m == -1 else f"{m}{var}"
    if c == 0:
        return mtxt
    return f"{mtxt} + {c}" if c > 0 else f"{mtxt} - {-c}"


class SpecialSolutionEquationGenerator(ProblemGenerator):
    """
    Linear equations with variables on both sides whose outcome may be a
    unique solution, an identity (all real numbers), or a contradiction
    (no solution). All three outcomes are mixed so the classification must
    be earned by simplifying, never guessed.

    Left side is disguised with a distribution: f(gx + h) + jx + k.

    Op-codes used:
    - EQ_SETUP: the original equation (string)
    - DIST: distribute (factor, expression, result)
    - COMB_X: combine x-terms (term1, term2, result)
    - COMB_CONST: combine constants (const1, const2, result)
    - REWRITE: simplified equation (string)
    - MOVE_TERM: move a term across (term, target_side, resulting_equation)
    - SPECIAL_SOLUTION: classify the reduced equation (reduced, classification)
    - EQ_OP_BOTH: (verb, value, left_side, new_right) — unique case
    - EQ_RESULT: (variable, value) — unique case
    - CHECK: substitute the solution, both sides agree (method, lhs, rhs)
    - CHECK_POINT: evaluate both sides at a test point (point, lhs_work,
      rhs_work) — agreement NOT required; disagreement demonstrates a
      contradiction, agreement at several points supports an identity
    - Z: final answer
    """

    def __init__(self, outcome=None):
        valid = ["unique", "identity", "contradiction", None]
        if outcome not in valid:
            raise ValueError(f"outcome must be one of {valid}")
        self.outcome = outcome

    def _point_work(self, m, c, x):
        """'{m}·{x} + {c} = {value}' with sign-aware rendering."""
        val = m * x + c
        sign = "+" if c >= 0 else "-"
        xtxt = f"({x})" if x < 0 else str(x)
        return f"{m}·{xtxt} {sign} {abs(c)} = {val}"

    def generate(self) -> dict:
        outcome = self.outcome or random.choice(
            ["unique", "identity", "contradiction"])

        # Disguised left side: f(gx + h) + jx + k  ->  m x + p
        f = random.randint(2, 5)
        g = random.randint(1, 4)
        h = random.randint(1, 6)
        j = random.randint(1, 9)
        k = random.randint(-9, 9)
        m = f * g + j
        p = f * h + k

        if outcome == "unique":
            mp = random.choice([v for v in range(1, 13) if v != m])
            x0 = random.randint(-9, 9)
            q = p + (m - mp) * x0
        else:
            mp = m
            q = p if outcome == "identity" else p + random.choice(
                [d for d in range(-9, 10) if d != 0])

        inner = lin(g, h)
        lhs_txt = f"{f}({inner}) + {lin(j, k)}"
        rhs_txt = lin(mp, q)
        original = f"{lhs_txt} = {rhs_txt}"

        steps = [step("EQ_SETUP", original)]
        steps.append(step("DIST", f, inner, lin(f * g, f * h)))
        steps.append(step("COMB_X", f"{f * g}x", f"{j}x", f"{m}x"))
        if k != 0:
            steps.append(step("COMB_CONST", f * h, k, p))
        steps.append(step("REWRITE", f"{lin(m, p)} = {rhs_txt}"))
        steps.append(step("MOVE_TERM", f"{mp}x", "left",
                          f"{lin(m - mp, p)} = {q}"))

        if outcome == "unique":
            dm = m - mp
            if p != 0:
                steps.append(step("MOVE_TERM", str(p), "right",
                                  f"{lin(dm, 0)} = {q - p}"))
            steps.append(step("EQ_OP_BOTH", "divide", dm, "x", x0))
            steps.append(step("EQ_RESULT", "x", x0))
            steps.append(step("CHECK", "substitute",
                              self._point_work(m, p, x0),
                              self._point_work(mp, q, x0)))
            steps.append(step("Z", x0))
            answer = str(x0)
            op = "linear_eq_unique"

        elif outcome == "identity":
            steps.append(step("SPECIAL_SOLUTION", f"{p} = {q}",
                              "identity: true for every x"))
            for pt in (0, 1):
                steps.append(step("CHECK_POINT", f"x={pt}",
                                  self._point_work(m, p, pt),
                                  self._point_work(mp, q, pt)))
            steps.append(step("Z", "All real numbers"))
            answer = "All real numbers"
            op = "linear_eq_identity"

        else:  # contradiction
            steps.append(step("SPECIAL_SOLUTION", f"{p} = {q}",
                              "contradiction: no value of x works"))
            steps.append(step("CHECK_POINT", "x=0",
                              self._point_work(m, p, 0),
                              self._point_work(mp, q, 0)))
            steps.append(step("Z", "No solution"))
            answer = "No solution"
            op = "linear_eq_contradiction"

        return dict(
            problem_id=jid(),
            operation=op,
            problem=f"Solve for x: {original}",
            steps=steps,
            final_answer=answer,
        )

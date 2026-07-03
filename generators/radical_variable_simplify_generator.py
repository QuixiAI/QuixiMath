import random
from base_generator import ProblemGenerator
from helpers import step, jid

SQUARE_FREE = [1, 2, 3, 5, 6, 7, 10, 11, 13, 15]


class RadicalVariableSimplifyGenerator(ProblemGenerator):
    """
    Simplifies radicals with variables: √(50x³) → 5x√(2x).

    Procedure: split the coefficient into (largest perfect square) × (square-
    free part), split the variable power into (even part) × (leftover), take
    the roots, assemble, and verify by squaring back.

    Op-codes used:
    - ROOT_SETUP: the radical (string) — shared with RootsAndRadicals
    - SQUARE_FACTOR: split off the largest square factor
      (value, factorization, square part) — numeric and symbolic
    - ROOT: square roots of the square parts (value, root)
    - REWRITE: the assembled simplified form (string)
    - CHECK: square the answer back to the radicand (method, work, radicand)
    - Z: final answer
    """

    def generate(self) -> dict:
        var = random.choice(["x", "x", "x", "y", "n"])
        while True:
            s = random.randint(1, 7)
            f = random.choice(SQUARE_FREE)
            p = random.randint(1, 5)
            k, rem = divmod(p, 2)
            if s == 1 and k == 0:
                continue          # nothing to pull out
            if f == 1 and rem == 0:
                continue          # nothing left under the radical
            break

        n = s * s * f
        pow_txt = var if p == 1 else f"{var}^{p}"
        radicand = f"{n}{pow_txt}" if n > 1 else pow_txt
        original = f"√({radicand})"

        # outside part: s · var^k
        if k == 0:
            outside = str(s)
        elif k == 1:
            outside = f"{s}{var}" if s > 1 else var
        else:
            outside = f"{s}{var}^{k}" if s > 1 else f"{var}^{k}"
        # inside part: f · var^rem
        if rem == 0:
            inside = f"√{f}"
        elif f == 1:
            inside = f"√{var}"
        else:
            inside = f"√({f}{var})"
        answer = f"{outside}{inside}" if not (s == 1 and k == 0) else inside

        steps = [step("ROOT_SETUP", original)]
        if n > 1:
            steps.append(step("SQUARE_FACTOR", n, f"{s * s} × {f}", s * s))
        if p >= 2:
            even_pow = var + ("^2" if 2 * k == 2 else f"^{2 * k}")
            leftover = "" if rem == 0 else f" · {var}"
            steps.append(step("SQUARE_FACTOR", pow_txt,
                              f"{even_pow}{leftover}", even_pow))
        if s > 1:
            steps.append(step("ROOT", s * s, s))
        if k >= 1:
            even_pow = f"{var}^2" if k == 1 else f"{var}^{2 * k}"
            root_txt = var if k == 1 else f"{var}^{k}"
            steps.append(step("ROOT", even_pow, root_txt))
        steps.append(step("REWRITE", answer))

        sq_out = f"{s * s}" if k == 0 else (
            f"{s * s}{var}^{2 * k}" if s > 1 else f"{var}^{2 * k}")
        in_val = (f"{f}" if rem == 0 else
                  (f"{var}" if f == 1 else f"{f}{var}"))
        steps.append(step("CHECK", "square_back",
                          f"({answer})^2 = {sq_out} · {in_val} = {radicand}",
                          radicand))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="simplify_radical_variables",
            problem=f"Simplify: {original}",
            steps=steps,
            final_answer=answer,
        )

import random
from base_generator import ProblemGenerator
from helpers import step, jid


def center_txt(a):
    """(x - a), (x + a), or x."""
    if a == 0:
        return "x"
    return f"(x - {a})" if a > 0 else f"(x + {-a})"


def inner_txt(a):
    """x - a without parentheses, for use inside abs(...)."""
    if a == 0:
        return "x"
    return f"x - {a}" if a > 0 else f"x + {-a}"


class PowerSeriesGenerator(ProblemGenerator):
    """
    Radius and interval of convergence by the ratio test, with the
    endpoints checked one at a time. The five families produce every
    bracket combination plus the degenerate radii:
    1/c^n (open), 1/(n·c^n) (half-open), 1/(n^2·c^n) (closed),
    n!·(x-a)^n (R = 0), (x-a)^n/n! (R = ∞).

    Op-codes used:
    - SERIES_SETUP / TEST_CHOOSE (shared with series convergence)
    - REWRITE / CANCEL / LIMIT_SETUP / CHECK / EVAL / SUBST
      (established)
    - Z: "R = ..., interval"

    Variants: open, half_open, closed, zero_radius, infinite
    """

    VARIANTS = ["open", "half_open", "closed", "zero_radius",
                "infinite"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a = random.randint(-5, 5)
        X, ix = center_txt(a), inner_txt(a)
        AX = f"abs({ix})"

        if variant in ("open", "half_open", "closed"):
            c = random.randint(2, 5)
            lo, hi = a - c, a + c
            if variant == "open":
                body = f"{X}^n/{c}^n"
                nfac, nfac_lim = "", ""
            elif variant == "half_open":
                body = f"{X}^n/(n·{c}^n)"
                nfac, nfac_lim = "n/(n + 1)", "lim n→∞ n/(n + 1) = 1"
            else:
                body = f"{X}^n/(n^2·{c}^n)"
                nfac = "(n/(n + 1))^2"
                nfac_lim = "lim n→∞ (n/(n + 1))^2 = 1"
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                     "radius and interval of convergence"),
                step("TEST_CHOOSE", "ratio test", "power series"),
                step("CANCEL", f"{AX}^(n+1)/{AX}^n = {AX}",
                     f"{c}^(n+1)/{c}^n = {c}"),
                step("REWRITE",
                     f"abs(a_(n+1)/a_n) = {AX}/{c}" +
                     (f" · {nfac}" if nfac else "")),
            ]
            if nfac:
                steps.append(step("LIMIT_SETUP", nfac_lim))
            steps += [
                step("REWRITE", f"L = {AX}/{c}"),
                step("CHECK", "ratio test", f"{AX}/{c} < 1",
                     f"converges when {AX} < {c}"),
                step("EVAL", "radius", f"R = {c}"),
            ]
            if variant == "open":
                steps += [
                    step("SUBST", "x", hi,
                         f"Σ {c}^n/{c}^n = Σ 1"),
                    step("CHECK", "nth-term", "terms are 1, not → 0",
                         f"diverges at x = {hi}"),
                    step("SUBST", "x", lo,
                         f"Σ (-{c})^n/{c}^n = Σ (-1)^n"),
                    step("CHECK", "nth-term", "terms do not approach 0",
                         f"diverges at x = {lo}"),
                ]
                answer = f"R = {c}, ({lo}, {hi})"
            elif variant == "half_open":
                steps += [
                    step("SUBST", "x", hi,
                         f"Σ {c}^n/(n·{c}^n) = Σ 1/n"),
                    step("CHECK", "p-series", "p = 1 ≤ 1",
                         f"diverges at x = {hi}"),
                    step("SUBST", "x", lo,
                         f"Σ (-{c})^n/(n·{c}^n) = Σ (-1)^n/n"),
                    step("CHECK", "AST", "1/n decreases to 0",
                         f"converges at x = {lo}"),
                ]
                answer = f"R = {c}, [{lo}, {hi})"
            else:
                steps += [
                    step("SUBST", "x", hi,
                         f"Σ {c}^n/(n^2·{c}^n) = Σ 1/n^2"),
                    step("CHECK", "p-series", "p = 2 > 1",
                         f"converges at x = {hi}"),
                    step("SUBST", "x", lo,
                         f"Σ (-{c})^n/(n^2·{c}^n) = Σ (-1)^n/n^2"),
                    step("CHECK", "absolute convergence",
                         "Σ 1/n^2 converges",
                         f"converges at x = {lo}"),
                ]
                answer = f"R = {c}, [{lo}, {hi}]"
        elif variant == "zero_radius":
            body = f"n!·{X}^n"
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                     "radius and interval of convergence"),
                step("TEST_CHOOSE", "ratio test", "power series"),
                step("CANCEL", "(n+1)!/n! = n + 1",
                     f"{AX}^(n+1)/{AX}^n = {AX}"),
                step("REWRITE",
                     f"abs(a_(n+1)/a_n) = (n + 1)·{AX}"),
                step("LIMIT_SETUP",
                     f"lim n→∞ (n + 1)·{AX} = ∞ for {AX} > 0"),
                step("CHECK", "ratio test", f"L = ∞ unless x = {a}",
                     f"converges only at x = {a}"),
            ]
            answer = f"R = 0, x = {a} only"
        else:
            body = f"{X}^n/n!"
            steps = [
                step("SERIES_SETUP", f"Σ {body}, n ≥ 1",
                     "radius and interval of convergence"),
                step("TEST_CHOOSE", "ratio test", "power series"),
                step("CANCEL", f"{AX}^(n+1)/{AX}^n = {AX}",
                     "(n+1)!/n! = n + 1"),
                step("REWRITE",
                     f"abs(a_(n+1)/a_n) = {AX}/(n + 1)"),
                step("LIMIT_SETUP",
                     f"lim n→∞ {AX}/(n + 1) = 0 for every x"),
                step("CHECK", "ratio test", "0 < 1 for all x",
                     "converges for all x"),
            ]
            answer = "R = ∞, (-∞, ∞)"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"power_series_{variant}",
            problem=(f"Find the radius and interval of convergence "
                     f"of Σ {body} for n ≥ 1."),
            steps=steps,
            final_answer=answer,
        )

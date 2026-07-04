import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Critical values are supplied in the problem (Principle 5).
CRITS = ["1.645", "1.96", "2.326", "2.576"]
SQUARE_N = [25, 100, 400]
# Standard errors s/√n chosen so both s and t stay exact.
SE_CHOICES = ["0.5", "1", "2", "2.5", "4", "5"]


class HypothesisTestGenerator(ProblemGenerator):
    """
    Two-sided significance tests — a one-proportion z-test and a
    one-sample t-test — with the critical value given in the problem
    (Principle 5). The null proportion is 0.5 and n is a perfect
    square, and the t-test's standard error is constructed to divide
    evenly, so every test statistic is an exact terminating decimal.

    Variants:
    - prop_z_stat:     the z statistic for a proportion
    - prop_z_decision: z statistic, then reject / fail to reject
    - t_stat:          the t statistic for a mean
    - t_decision:      t statistic, then reject / fail to reject

    Op-codes used:
    - HT_SETUP: the hypotheses, data, and critical value
    - TEST_STAT_FORMULA: the test-statistic formula
    - ROOT / M / D / S (established)
    - CHECK (established): |statistic| vs the critical value
    - Z: the statistic, or "reject H0" / "fail to reject H0"
    """

    VARIANTS = ["prop_z_stat", "prop_z_decision", "t_stat",
                "t_decision"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _decision_step(stat, crit):
        reject = abs(stat) > crit
        verdict = "reject H0" if reject else "fail to reject H0"
        rel = ">" if reject else "≤"
        return step("CHECK", "abs(stat) vs critical value",
                    f"{dec(abs(stat))} {rel} {dec(crit)}",
                    verdict), verdict

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        crit = Fraction(random.choice(CRITS))

        if variant.startswith("prop_z"):
            n = random.choice(SQUARE_N)
            root = math.isqrt(n)
            x = random.randint(int(0.30 * n), int(0.70 * n))
            phat = Fraction(x, n)
            se = Fraction(1, 2) / root
            z = (phat - Fraction(1, 2)) / se
            steps = [
                step("HT_SETUP",
                     f"H0: p = 0.5; Ha: p ≠ 0.5",
                     f"n = {n}, {x} successes, critical value = {dec(crit)}"),
                step("D", x, n, dec(phat)),
                step("TEST_STAT_FORMULA",
                     "z = (p̂ - p0)/√(p0(1-p0)/n)"),
                step("M", "0.5", "0.5", "0.25"),
                step("D", "0.25", n, dec(Fraction(1, 4) / n)),
                step("ROOT", f"√{dec(Fraction(1, 4) / n)}", dec(se)),
                step("S", dec(phat), "0.5", dec(phat - Fraction(1, 2))),
                step("D", dec(phat - Fraction(1, 2)), dec(se), dec(z)),
            ]
            if variant == "prop_z_decision":
                dstep, verdict = self._decision_step(z, crit)
                steps.append(dstep)
                answer = verdict
            else:
                answer = dec(z)
            problem = (f"In a two-sided one-proportion z-test of "
                       f"H0: p = 0.5, a sample of size {n} has {x} "
                       f"successes. Using a critical value of "
                       f"{dec(crit)}, "
                       + ("what is the test statistic z?"
                          if variant == "prop_z_stat"
                          else "state the conclusion (reject H0 or "
                          "fail to reject H0)."))
        else:
            n = random.choice(SQUARE_N)
            root = math.isqrt(n)
            se = Fraction(random.choice(SE_CHOICES))
            s = se * root
            mu0 = random.randint(20, 100)
            diff = random.choice([d for d in range(-12, 13) if d != 0])
            xbar = mu0 + diff
            t = Fraction(diff) / se
            steps = [
                step("HT_SETUP",
                     f"H0: μ = {mu0}; Ha: μ ≠ {mu0}",
                     f"n = {n}, x̄ = {xbar}, s = {dec(s)}, "
                     f"critical value = {dec(crit)}"),
                step("TEST_STAT_FORMULA", "t = (x̄ - μ0)/(s/√n)"),
                step("ROOT", f"√{n}", root),
                step("D", dec(s), root, dec(se)),
                step("S", xbar, mu0, diff),
                step("D", diff, dec(se), dec(t)),
            ]
            if variant == "t_decision":
                dstep, verdict = self._decision_step(t, crit)
                steps.append(dstep)
                answer = verdict
            else:
                answer = dec(t)
            problem = (f"In a two-sided one-sample t-test of "
                       f"H0: μ = {mu0}, a sample of size {n} has mean "
                       f"x̄ = {xbar} and standard deviation s = {dec(s)}. "
                       f"Using a critical value of {dec(crit)}, "
                       + ("what is the test statistic t?"
                          if variant == "t_stat"
                          else "state the conclusion (reject H0 or "
                          "fail to reject H0)."))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"hypothesis_test_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


CRITS = ["1.645", "1.96", "2.326", "2.576"]


class TwoSampleTestGenerator(ProblemGenerator):
    """
    Two-sample t and two-proportion z tests with supplied critical values
    and exact-friendly standard errors.

    Variants:
    - t_stat: two-sample mean-difference t statistic.
    - t_decision: t statistic plus reject/fail decision.
    - prop_z_stat: two-proportion z statistic.
    - prop_z_decision: z statistic plus reject/fail decision.

    Op-codes used:
    - HT_SETUP / TEST_STAT_FORMULA / CHECK
    - A / S / M / D / ROOT (established)
    - Z: statistic or composite verdict
    """

    VARIANTS = ["t_stat", "t_decision", "prop_z_stat", "prop_z_decision"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _decision(stat, crit):
        reject = abs(stat) > crit
        rel = ">" if reject else "≤"
        head = "reject H0" if reject else "fail to reject H0"
        comparison = f"{dec(abs(stat))} {rel} {dec(crit)}"
        return step("CHECK", "abs(stat) vs critical value",
                    comparison, head), f"{head} ({comparison})"

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        crit = Fraction(random.choice(CRITS))
        if variant.startswith("t_"):
            n1 = n2 = 8
            s1 = s2 = 4
            mu1 = random.randint(30, 80)
            diff = random.choice([d for d in range(-12, 13) if d != 0])
            mu2 = mu1 - diff
            se = Fraction(2)
            stat = Fraction(diff, 2)
            steps = [
                step("HT_SETUP", "H0: μ1 = μ2; Ha: μ1 ≠ μ2",
                     f"n1={n1}, x̄1={mu1}, s1={s1}; n2={n2}, x̄2={mu2}, s2={s2}; critical value={dec(crit)}"),
                step("TEST_STAT_FORMULA",
                     "t = (x̄1 - x̄2)/sqrt(s1^2/n1 + s2^2/n2)"),
                step("M", s1, s1, s1 * s1),
                step("D", s1 * s1, n1, dec(Fraction(s1 * s1, n1))),
                step("M", s2, s2, s2 * s2),
                step("D", s2 * s2, n2, dec(Fraction(s2 * s2, n2))),
                step("A", dec(Fraction(s1 * s1, n1)),
                     dec(Fraction(s2 * s2, n2)), "4"),
                step("ROOT", "√4", se),
                step("S", mu1, mu2, diff),
                step("D", diff, se, dec(stat)),
            ]
            problem = (
                f"In a two-sided two-sample t-test of H0: μ1 = μ2, "
                f"sample 1 has n1={n1}, x̄1={mu1}, s1={s1}; sample 2 "
                f"has n2={n2}, x̄2={mu2}, s2={s2}. Using a critical "
                f"value of {dec(crit)}, "
                + ("what is the test statistic t?"
                   if variant == "t_stat"
                   else "state the conclusion (reject H0 or fail to reject H0).")
            )
        else:
            n1 = n2 = 50
            d = random.choice([v for v in range(-12, 13) if v != 0])
            x1 = 25 + d
            x2 = 25 - d
            pooled = Fraction(x1 + x2, n1 + n2)
            diff = Fraction(x1, n1) - Fraction(x2, n2)
            se = Fraction(1, 10)
            stat = diff / se
            steps = [
                step("HT_SETUP", "H0: p1 = p2; Ha: p1 ≠ p2",
                     f"n1={n1}, x1={x1}; n2={n2}, x2={x2}; critical value={dec(crit)}"),
                step("D", x1, n1, dec(Fraction(x1, n1))),
                step("D", x2, n2, dec(Fraction(x2, n2))),
                step("TEST_STAT_FORMULA",
                     "z = (p̂1-p̂2)/sqrt(pooled(1-pooled)(1/n1+1/n2))"),
                step("A", x1, x2, x1 + x2),
                step("A", n1, n2, n1 + n2),
                step("D", x1 + x2, n1 + n2, dec(pooled)),
                step("S", dec(Fraction(x1, n1)), dec(Fraction(x2, n2)),
                     dec(diff)),
                step("ROOT", "√0.01", dec(se)),
                step("D", dec(diff), dec(se), dec(stat)),
            ]
            problem = (
                f"In a two-sided two-proportion z-test of H0: p1 = p2, "
                f"sample 1 has n1={n1}, x1={x1}; sample 2 has n2={n2}, "
                f"x2={x2}. Using a critical value of {dec(crit)}, "
                + ("what is the test statistic z?"
                   if variant == "prop_z_stat"
                   else "state the conclusion (reject H0 or fail to reject H0).")
            )
        if variant.endswith("_decision"):
            dstep, answer = self._decision(stat, crit)
            steps.append(dstep)
        else:
            answer = dec(stat)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"two_sample_test_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

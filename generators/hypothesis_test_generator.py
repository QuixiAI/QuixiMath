"""Exact one-sample hypothesis-test statistics and decisions.

Variants retain the original two-sided proportion-z and sample-t cases and
add one-sided t decisions plus known-sigma mean-z procedures. Square sample
sizes make every standard error exact; all decision critical values are
printed in the problem. Each variant has the original direct framing plus
three contextual phrasings. Op-codes: ``HT_SETUP``, ``TEST_STAT_FORMULA``,
``LOOKUP_SUPPLIED``, ``ROOT``, ``M``, ``D``, ``S``, ``CHECK``, and ``Z``.
"""
import hashlib
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
ONE_SIDED = [("0.10", "1.28"), ("0.05", "1.645"), ("0.01", "2.33")]
LEGACY_VARIANTS = ("prop_z_stat", "prop_z_decision", "t_stat", "t_decision")
EXTENSION_VARIANTS = ("one_sided_left", "one_sided_right", "z_mean_stat",
                      "z_mean_decision")
STATISTICS = True
SETTINGS = ("amber study", "birch survey", "cedar trial", "delta project",
            "ember lab", "forest audit", "granite program", "harbor test",
            "indigo review", "jade pilot", "kestrel study", "lunar trial")
LOCATIONS = ("north campus", "south campus", "east annex", "west annex",
             "river center", "lake center", "hill school", "valley school",
             "maple office", "oak office", "pine clinic", "cedar clinic")


def _frame(core):
    """Original direct wording plus three contextual phrasings."""
    code = f"cohort {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    location, setting = random.choice(LOCATIONS), random.choice(SETTINGS)
    site = f"{location} during the {setting} ({code})"
    lowered = core[0].lower() + core[1:]
    return random.choice((
        f"{core} Context: {site}.",
        f"At the {site}, {lowered}",
        f"For records from the {site}, {lowered}",
        f"During the {setting} at the {location} ({code}), {lowered}",
    ))


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
    - one_sided_left / one_sided_right: one-sample t decision
    - z_mean_stat / z_mean_decision: known-sigma mean z procedure

    Op-codes used:
    - HT_SETUP: the hypotheses, data, and critical value
    - TEST_STAT_FORMULA: the test-statistic formula
    - ROOT / M / D / S (established)
    - CHECK (established): |statistic| vs the critical value
    - Z: the statistic, or "reject H0" / "fail to reject H0"
    """

    VARIANTS = ["prop_z_stat", "prop_z_decision", "t_stat", "t_decision",
                "one_sided_left", "one_sided_right", "z_mean_stat",
                "z_mean_decision"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _decision_step(stat, crit):
        reject = abs(stat) > crit
        rel = ">" if reject else "≤"
        comparison = f"{dec(abs(stat))} {rel} {dec(crit)}"
        head = "reject H0" if reject else "fail to reject H0"
        # composite verdict: the bare label would be a gradable coin flip
        verdict = f"{head} ({comparison})"
        return step("CHECK", "abs(stat) vs critical value",
                    comparison, head), verdict

    def generate(self) -> dict:
        if self.variant is not None:
            return self._generate_variant(self.variant)

        # Preserve the legacy call's exact global-RNG advancement. This class
        # sits mid-registry, so extra random draws would churn examples for
        # hundreds of unrelated generators in the generated documentation.
        legacy_variant = random.choice(LEGACY_VARIANTS)
        legacy_crit = Fraction(random.choice(CRITS))
        legacy = self._generate_variant(legacy_variant, legacy_crit,
                                        apply_frame=False)
        post_legacy_state = random.getstate()
        digest = hashlib.sha256(
            legacy["problem"].encode("utf-8")
            + repr(post_legacy_state).encode("ascii")
        ).digest()
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            if digest[0] < 128:
                legacy["problem"] = _frame(legacy["problem"])
                return legacy
            extension = EXTENSION_VARIANTS[digest[0] % len(EXTENSION_VARIANTS)]
            return self._generate_variant(extension)
        finally:
            random.setstate(post_legacy_state)

    def _generate_variant(self, variant, crit=None, apply_frame=True):
        crit = crit if crit is not None else Fraction(random.choice(CRITS))

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
        elif variant in ("t_stat", "t_decision"):
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
        elif variant in ("one_sided_left", "one_sided_right"):
            alpha, crit_text = random.choice(ONE_SIDED)
            crit = Fraction(crit_text)
            n = random.choice(SQUARE_N)
            root = math.isqrt(n)
            se = Fraction(random.choice(SE_CHOICES))
            s = se * root
            mu0 = random.randint(20, 100)
            magnitude = random.randint(1, 12)
            diff = -magnitude if variant == "one_sided_left" else magnitude
            xbar = mu0 + diff
            t = Fraction(diff) / se
            relation = "<" if variant == "one_sided_left" else ">"
            tail = "left" if variant == "one_sided_left" else "right"
            hypotheses = f"H0: μ = {mu0}; Ha: μ {relation} {mu0}"
            steps = [
                step("HT_SETUP", hypotheses,
                     f"n = {n}, x̄ = {xbar}, s = {dec(s)}, α = {alpha}"),
                step("TEST_STAT_FORMULA", "t = (x̄ - μ0)/(s/√n)"),
                step("ROOT", f"√{n}", root),
                step("D", dec(s), root, dec(se)),
                step("S", xbar, mu0, diff),
                step("D", diff, dec(se), dec(t)),
                step("LOOKUP_SUPPLIED", f"{tail}-tail critical (α = {alpha})",
                     crit_text),
            ]
            if variant == "one_sided_left":
                reject = t < -crit
                comparison = (f"{dec(t)} {'<' if reject else '≥'} "
                              f"-{crit_text}")
            else:
                reject = t > crit
                comparison = (f"{dec(t)} {'>' if reject else '≤'} "
                              f"{crit_text}")
            head = "reject H0" if reject else "fail to reject H0"
            steps.append(step("CHECK", f"t vs {tail}-tail critical",
                              comparison, head))
            answer = f"{head} ({comparison})"
            problem = (
                f"In a one-sided one-sample t-test of {hypotheses}, a sample "
                f"of size {n} has mean x̄ = {xbar} and sample standard "
                f"deviation s = {dec(s)}. At α = {alpha}, use the supplied "
                f"{tail}-tail critical value {crit_text}. Compute t and state "
                "the conclusion."
            )
        else:
            n = random.choice(SQUARE_N)
            root = math.isqrt(n)
            se = Fraction(random.choice(SE_CHOICES))
            sigma = se * root
            mu0 = random.randint(20, 100)
            diff = random.choice([d for d in range(-12, 13) if d != 0])
            xbar = mu0 + diff
            z = Fraction(diff) / se
            steps = [
                step("HT_SETUP", f"H0: μ = {mu0}; Ha: μ ≠ {mu0}",
                     f"n = {n}, x̄ = {xbar}, σ = {dec(sigma)}"),
                step("TEST_STAT_FORMULA", "z = (x̄ - μ0)/(σ/√n)"),
                step("ROOT", f"√{n}", root),
                step("D", dec(sigma), root, dec(se)),
                step("S", xbar, mu0, diff),
                step("D", diff, dec(se), dec(z)),
            ]
            if variant == "z_mean_decision":
                crit_text = random.choice(CRITS)
                crit = Fraction(crit_text)
                steps.append(step("LOOKUP_SUPPLIED", "two-sided critical value",
                                  crit_text))
                dstep, answer = self._decision_step(z, crit)
                steps.append(dstep)
                request = "State the conclusion (reject H0 or fail to reject H0)."
                critical_clause = f" Using a two-sided critical value of {crit_text},"
            else:
                answer = dec(z)
                request = "What is the test statistic z?"
                critical_clause = ""
            problem = (
                f"In a two-sided known-σ one-sample z-test of H0: μ = {mu0}, "
                f"a sample of size {n} has mean x̄ = {xbar} and population "
                f"standard deviation σ = {dec(sigma)}.{critical_clause} {request}"
            )
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"hypothesis_test_{variant}",
            problem=_frame(problem) if apply_frame else problem,
            steps=steps,
            final_answer=answer,
        )

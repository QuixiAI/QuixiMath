"""Exact two-sample t and pooled-proportion z procedures.

Variants retain the four original unpooled-t/equal-n-proportion cases while
de-hard-coding their t inputs, and add ``t_pooled_stat``,
``t_pooled_decision``, ``t_welch_stat``, and ``prop_z_unequal_n``. Shared
perfect-square SE and pooled-SD banks keep all roots rational. Critical values
are printed with df when used. Op-codes: ``HT_SETUP``,
``TEST_STAT_FORMULA``, ``RULE``, ``LOOKUP_SUPPLIED``, ``ROOT``, ``A``,
``S``, ``M``, ``D``, ``E``, ``CHECK``, and ``Z``.
"""
import hashlib
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec
from stats_common import (N_PAIR_BANK, POOLED_S_PAIRS, TWO_SAMPLE_SE_BANK,
                          is_perfect_square, num_txt, sqrt_fraction)


CRITS = ["1.645", "1.96", "2.326", "2.576"]
POOLED_CRITS = (("0.10", "1.761"), ("0.05", "2.145"),
                ("0.01", "2.977"))
LEGACY_VARIANTS = ("t_stat", "t_decision", "prop_z_stat", "prop_z_decision")
EXTENSION_VARIANTS = ("t_pooled_stat", "t_pooled_decision", "t_welch_stat",
                      "prop_z_unequal_n")
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


def _prop_cases():
    out = []
    for n1, n2, reciprocal_sum in N_PAIR_BANK:
        if n1 == n2:
            continue
        for pooled in (Fraction(1, 5), Fraction(1, 2), Fraction(4, 5)):
            variance = pooled * (1 - pooled) * reciprocal_sum
            total_successes = pooled * (n1 + n2)
            if (total_successes.denominator != 1 or
                    not is_perfect_square(variance)):
                continue
            se = sqrt_fraction(variance)
            total_successes = int(total_successes)
            lower = max(0, total_successes - n2)
            upper = min(n1, total_successes)
            for x1 in range(lower, upper + 1):
                x2 = total_successes - x1
                if Fraction(x1, n1) != Fraction(x2, n2):
                    out.append((n1, x1, n2, x2, pooled, se))
    return tuple(out)


UNEQUAL_PROP_CASES = _prop_cases()


class TwoSampleTestGenerator(ProblemGenerator):
    """
    Two-sample t and two-proportion z tests with supplied critical values
    and exact-friendly standard errors.

    Variants:
    - t_stat: two-sample mean-difference t statistic.
    - t_decision: t statistic plus reject/fail decision.
    - prop_z_stat: two-proportion z statistic.
    - prop_z_decision: z statistic plus reject/fail decision.
    - t_pooled_stat / t_pooled_decision: equal-variance pooled t.
    - t_welch_stat: unpooled t with conservative df.
    - prop_z_unequal_n: pooled-proportion z with unequal n.

    Op-codes used:
    - HT_SETUP / TEST_STAT_FORMULA / CHECK
    - A / S / M / D / ROOT (established)
    - Z: statistic or composite verdict
    """

    VARIANTS = [*LEGACY_VARIANTS, *EXTENSION_VARIANTS]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _decision(stat, crit):
        reject = abs(stat) > crit
        rel = ">" if reject else "≤"
        head = "reject H0" if reject else "fail to reject H0"
        comparison = f"{num_txt(abs(stat))} {rel} {num_txt(crit)}"
        return step("CHECK", "abs(stat) vs critical value",
                    comparison, head), f"{head} ({comparison})"

    def generate(self) -> dict:
        if self.variant is not None:
            return self._generate_variant(self.variant)

        # Simulate the legacy call exactly, then derive the expanded output
        # locally while restoring the legacy post-call RNG state.
        legacy_variant = random.choice(LEGACY_VARIANTS)
        legacy_crit = Fraction(random.choice(CRITS))
        legacy = self._simulate_legacy(legacy_variant, legacy_crit)
        post_legacy_state = random.getstate()
        digest = hashlib.sha256(
            legacy["problem"].encode("utf-8")
            + repr(post_legacy_state).encode("ascii")
        ).digest()
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            return self._generate_variant(
                self.VARIANTS[digest[0] % len(self.VARIANTS)])
        finally:
            random.setstate(post_legacy_state)

    @staticmethod
    def _result(variant, problem, steps, answer):
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"two_sample_test_{variant}",
                "problem": _frame(problem), "steps": steps,
                "final_answer": answer}

    @classmethod
    def _unpooled(cls, variant):
        s1, n1, s2, n2, variance = random.choice(TWO_SAMPLE_SE_BANK)
        se = Fraction(math.isqrt(variance))
        mean1 = random.randint(40, 180)
        difference = random.choice([value for value in range(-24, 25) if value])
        mean2 = mean1 - difference
        statistic = Fraction(difference, 1) / se
        crit = Fraction(random.choice(CRITS))
        term1, term2 = Fraction(s1 * s1, n1), Fraction(s2 * s2, n2)
        steps = [
            step("HT_SETUP", "H0: μ1 = μ2; Ha: μ1 ≠ μ2",
                 f"n1={n1}, x̄1={mean1}, s1={s1}; n2={n2}, x̄2={mean2}, s2={s2}"),
            step("TEST_STAT_FORMULA",
                 "t = (x̄1 − x̄2)/√(s1²/n1 + s2²/n2)"),
            step("E", s1, 2, s1 * s1),
            step("D", s1 * s1, n1, num_txt(term1)),
            step("E", s2, 2, s2 * s2),
            step("D", s2 * s2, n2, num_txt(term2)),
            step("A", num_txt(term1), num_txt(term2), num_txt(variance)),
            step("ROOT", num_txt(variance), 2, num_txt(se)),
            step("S", mean1, mean2, difference),
            step("D", difference, num_txt(se), num_txt(statistic)),
        ]
        if variant == "t_decision":
            steps.append(step("LOOKUP_SUPPLIED", "two-sided critical value",
                              num_txt(crit)))
            dstep, answer = cls._decision(statistic, crit)
            steps.append(dstep)
            request = "state the conclusion (reject H0 or fail to reject H0)."
        else:
            answer = num_txt(statistic)
            request = "what is the test statistic t?"
        problem = (f"In a two-sided two-sample t-test of H0: μ1 = μ2, sample 1 "
                   f"has n1={n1}, x̄1={mean1}, s1={s1}; sample 2 has n2={n2}, "
                   f"x̄2={mean2}, s2={s2}. Using a critical value of "
                   f"{num_txt(crit)}, {request}")
        return cls._result(variant, problem, steps, answer)

    @classmethod
    def _legacy_prop_current(cls, variant):
        n1 = n2 = 50
        d = random.choice([value for value in range(-12, 13) if value])
        x1, x2 = 25 + d, 25 - d
        pooled = Fraction(x1 + x2, n1 + n2)
        diff = Fraction(x1, n1) - Fraction(x2, n2)
        se = Fraction(1, 10)
        statistic = diff / se
        crit = Fraction(random.choice(CRITS))
        steps = [
            step("HT_SETUP", "H0: p1 = p2; Ha: p1 ≠ p2",
                 f"n1={n1}, x1={x1}; n2={n2}, x2={x2}"),
            step("D", x1, n1, num_txt(Fraction(x1, n1))),
            step("D", x2, n2, num_txt(Fraction(x2, n2))),
            step("TEST_STAT_FORMULA",
                 "z = (p̂1 − p̂2)/√(pooled(1 − pooled)(1/n1 + 1/n2))"),
            step("A", x1, x2, x1 + x2),
            step("A", n1, n2, n1 + n2),
            step("D", x1 + x2, n1 + n2, num_txt(pooled)),
            step("S", num_txt(Fraction(x1, n1)), num_txt(Fraction(x2, n2)),
                 num_txt(diff)),
            step("ROOT", "0.01", 2, num_txt(se)),
            step("D", num_txt(diff), num_txt(se), num_txt(statistic)),
        ]
        if variant == "prop_z_decision":
            steps.append(step("LOOKUP_SUPPLIED", "two-sided critical value",
                              num_txt(crit)))
            dstep, answer = cls._decision(statistic, crit)
            steps.append(dstep)
            request = "state the conclusion (reject H0 or fail to reject H0)."
        else:
            answer = num_txt(statistic)
            request = "what is the test statistic z?"
        problem = (f"In a two-sided two-proportion z-test of H0: p1 = p2, sample "
                   f"1 has n1={n1}, x1={x1}; sample 2 has n2={n2}, x2={x2}. "
                   f"Using a critical value of {num_txt(crit)}, {request}")
        return cls._result(variant, problem, steps, answer)

    @classmethod
    def _pooled(cls, variant):
        n1 = n2 = 8
        s1, s2, pooled_sd = random.choice(POOLED_S_PAIRS)
        mean1 = random.randint(40, 180)
        difference = random.choice([value for value in range(-24, 25) if value])
        mean2 = mean1 - difference
        df = n1 + n2 - 2
        pooled_variance = Fraction(s1 * s1 + s2 * s2, 2)
        se = Fraction(pooled_sd, 2)
        statistic = Fraction(difference, 1) / se
        alpha, crit_text = random.choice(POOLED_CRITS)
        crit = Fraction(crit_text)
        weighted1, weighted2 = (n1 - 1) * s1 * s1, (n2 - 1) * s2 * s2
        steps = [
            step("HT_SETUP", "H0: μ1 = μ2; Ha: μ1 ≠ μ2",
                 f"equal variances, df = {df}, α = {alpha}"),
            step("TEST_STAT_FORMULA",
                 "t = (x̄1 − x̄2)/(sp·√(1/n1 + 1/n2))"),
            step("E", s1, 2, s1 * s1),
            step("M", n1 - 1, s1 * s1, weighted1),
            step("E", s2, 2, s2 * s2),
            step("M", n2 - 1, s2 * s2, weighted2),
            step("A", weighted1, weighted2, weighted1 + weighted2),
            step("A", n1 - 1, n2 - 1, df),
            step("D", weighted1 + weighted2, df, num_txt(pooled_variance)),
            step("ROOT", num_txt(pooled_variance), 2, pooled_sd),
            step("D", 1, n1, num_txt(Fraction(1, n1))),
            step("D", 1, n2, num_txt(Fraction(1, n2))),
            step("A", num_txt(Fraction(1, n1)), num_txt(Fraction(1, n2)), "0.25"),
            step("ROOT", "0.25", 2, "0.5"),
            step("M", pooled_sd, "0.5", num_txt(se)),
            step("S", mean1, mean2, difference),
            step("D", difference, num_txt(se), num_txt(statistic)),
        ]
        if variant == "t_pooled_decision":
            steps.append(step("LOOKUP_SUPPLIED", f"t critical (df = {df}, α = {alpha})",
                              crit_text))
            dstep, answer = cls._decision(statistic, crit)
            steps.append(dstep)
            request = "compute the pooled t statistic and state the conclusion."
        else:
            answer = num_txt(statistic)
            request = "compute the pooled t statistic."
        problem = (f"In an equal-variance two-sample t procedure, sample 1 has "
                   f"n1={n1}, x̄1={mean1}, s1={s1}; sample 2 has n2={n2}, "
                   f"x̄2={mean2}, s2={s2}. Use t critical value {crit_text} "
                   f"(df = {df}, α = {alpha}) and {request}")
        return cls._result(variant, problem, steps, answer)

    @classmethod
    def _welch(cls):
        s1, n1, s2, n2, variance = random.choice(TWO_SAMPLE_SE_BANK)
        se = Fraction(math.isqrt(variance))
        mean1 = random.randint(40, 180)
        difference = random.choice([value for value in range(-24, 25) if value])
        mean2 = mean1 - difference
        statistic = Fraction(difference, 1) / se
        df = min(n1 - 1, n2 - 1)
        term1, term2 = Fraction(s1 * s1, n1), Fraction(s2 * s2, n2)
        steps = [
            step("HT_SETUP", "H0: μ1 = μ2; Ha: μ1 ≠ μ2", "unequal variances"),
            step("TEST_STAT_FORMULA",
                 "t = (x̄1 − x̄2)/√(s1²/n1 + s2²/n2)"),
            step("RULE", "conservative df", "df = min(n1 − 1, n2 − 1)"),
            step("S", n1, 1, n1 - 1),
            step("S", n2, 1, n2 - 1),
            step("MIN", f"{n1 - 1},{n2 - 1}", df),
            step("E", s1, 2, s1 * s1),
            step("D", s1 * s1, n1, num_txt(term1)),
            step("E", s2, 2, s2 * s2),
            step("D", s2 * s2, n2, num_txt(term2)),
            step("A", num_txt(term1), num_txt(term2), num_txt(variance)),
            step("ROOT", num_txt(variance), 2, num_txt(se)),
            step("S", mean1, mean2, difference),
            step("D", difference, num_txt(se), num_txt(statistic)),
        ]
        answer = f"t = {num_txt(statistic)}; df = {df}"
        problem = (f"For a Welch two-sample t statistic, sample 1 has n1={n1}, "
                   f"x̄1={mean1}, s1={s1}; sample 2 has n2={n2}, x̄2={mean2}, "
                   f"s2={s2}. Use conservative df = min(n1 − 1, n2 − 1).")
        return cls._result("t_welch_stat", problem, steps, answer)

    @classmethod
    def _unequal_prop(cls):
        n1, x1, n2, x2, pooled, se = random.choice(UNEQUAL_PROP_CASES)
        phat1, phat2 = Fraction(x1, n1), Fraction(x2, n2)
        diff = phat1 - phat2
        reciprocal_sum = Fraction(1, n1) + Fraction(1, n2)
        variance = pooled * (1 - pooled) * reciprocal_sum
        statistic = diff / se
        steps = [
            step("HT_SETUP", "H0: p1 = p2; Ha: p1 ≠ p2",
                 f"n1={n1}, x1={x1}; n2={n2}, x2={x2}"),
            step("TEST_STAT_FORMULA",
                 "z = (p̂1 − p̂2)/√(p̂pool(1 − p̂pool)(1/n1 + 1/n2))"),
            step("D", x1, n1, num_txt(phat1)),
            step("D", x2, n2, num_txt(phat2)),
            step("A", x1, x2, x1 + x2),
            step("A", n1, n2, n1 + n2),
            step("D", x1 + x2, n1 + n2, num_txt(pooled)),
            step("S", 1, num_txt(pooled), num_txt(1 - pooled)),
            step("D", 1, n1, num_txt(Fraction(1, n1))),
            step("D", 1, n2, num_txt(Fraction(1, n2))),
            step("A", num_txt(Fraction(1, n1)), num_txt(Fraction(1, n2)),
                 num_txt(reciprocal_sum)),
            step("M", num_txt(pooled), num_txt(1 - pooled),
                 num_txt(pooled * (1 - pooled))),
            step("M", num_txt(pooled * (1 - pooled)), num_txt(reciprocal_sum),
                 num_txt(variance)),
            step("ROOT", num_txt(variance), 2, num_txt(se)),
            step("S", num_txt(phat1), num_txt(phat2), num_txt(diff)),
            step("D", num_txt(diff), num_txt(se), num_txt(statistic)),
        ]
        problem = (f"In a two-proportion z-test with unequal sample sizes, sample "
                   f"1 has n1={n1}, x1={x1}; sample 2 has n2={n2}, x2={x2}. "
                   "Compute the pooled-proportion z statistic.")
        return cls._result("prop_z_unequal_n", problem, steps, num_txt(statistic))

    def _generate_variant(self, variant):
        if variant in ("t_stat", "t_decision"):
            return self._unpooled(variant)
        if variant in ("prop_z_stat", "prop_z_decision"):
            return self._legacy_prop_current(variant)
        if variant in ("t_pooled_stat", "t_pooled_decision"):
            return self._pooled(variant)
        if variant == "t_welch_stat":
            return self._welch()
        return self._unequal_prop()

    def _simulate_legacy(self, variant, crit):
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

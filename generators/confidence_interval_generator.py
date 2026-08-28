"""Exact z confidence intervals, margins, sample sizes, and width effects.

Variants retain the five original mean/proportion margin and sample-size
procedures and add ``prop_ci``, ``diff_means_ci``, ``diff_props_ci``, and
``width_effect``. Perfect-square standard-error banks make every extension
exact; every z* is printed. Op-codes: ``CI_SETUP``, ``MOE_FORMULA``,
``CI_FORMULA``, ``SAMPLE_SIZE_FORMULA``, ``WIDTH_FORMULA``,
``LOOKUP_SUPPLIED``, ``ROOT``, ``A``, ``S``, ``M``, ``D``, ``E``,
``CEIL``, ``REWRITE``, ``CHECK``, and ``Z``.
"""
import hashlib
import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec
from stats_common import (DIFF_PROP_SE_BANK, PROP_SE_BANK, TWO_SAMPLE_SE_BANK,
                          num_txt)

# Critical values are supplied in the problem text (Principle 5).
Z_STARS = ["1.28", "1.645", "1.96", "2.05", "2.576"]
# Perfect-square sample sizes, so √n is an integer and σ/√n and
# 0.5/√n terminate.
SQUARE_N = [25, 100, 400]
# Margins whose reciprocal terminates, so (z*·σ/E) stays exact.
MARGINS = ["0.1", "0.25", "0.5", "1", "2", "5"]
# Proportions are bounded in [0, 1], so their margins are small
# (reciprocals 50/40/25/20/10 all terminate).
PROP_MARGINS = ["0.02", "0.025", "0.04", "0.05", "0.1"]
LEGACY_VARIANTS = ("mean_margin", "mean_ci", "prop_margin",
                   "sample_size_mean", "sample_size_prop")
EXTENSION_VARIANTS = ("prop_ci", "diff_means_ci", "diff_props_ci",
                      "width_effect")
STATISTICS = True
SETTINGS = ("amber study", "birch survey", "cedar trial", "delta project",
            "ember lab", "forest audit", "granite program", "harbor test",
            "indigo review", "jade pilot", "kestrel study", "lunar trial")
LOCATIONS = ("north campus", "south campus", "east annex", "west annex",
             "river center", "lake center", "hill school", "valley school",
             "maple office", "oak office", "pine clinic", "cedar clinic")
EXTENSION_QUERIES = {
    "prop_ci": (
        "Find the confidence interval for p.",
        "Compute p̂ ± z*·SE(p̂).",
        "Use the supplied critical value to report the proportion interval.",
        "Give the exact one-proportion z confidence interval.",
    ),
    "diff_means_ci": (
        "Find the confidence interval for μ1 − μ2.",
        "Use the known population SDs to form the difference-of-means interval.",
        "Compute (x̄1 − x̄2) ± z*·SE.",
        "Report the exact known-σ two-mean confidence interval.",
    ),
    "diff_props_ci": (
        "Find the confidence interval for p1 − p2.",
        "Compute (p̂1 − p̂2) ± z*·SE.",
        "Use both sample proportions to report the difference interval.",
        "Give the exact two-proportion confidence interval.",
    ),
    "width_effect": (
        "Describe the interval-width effect and include the changing quantity.",
        "Compare the two margins and state whether the interval widens or narrows.",
        "How does this change affect confidence-interval width?",
        "Give a composite width verdict supported by the calculation.",
    ),
}


def _frame(core):
    code = f"cohort {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"At the {random.choice(LOCATIONS)} during the "
            f"{random.choice(SETTINGS)} ({code}), {core[0].lower() + core[1:]}")


class ConfidenceIntervalGenerator(ProblemGenerator):
    """
    Confidence intervals for a mean or a proportion, margins of error,
    and minimum sample sizes — with the critical value z* given in the
    problem (Principle 5). Sample sizes are perfect squares and the
    margins are chosen so √n is an integer and every quantity is an
    exact terminating decimal.

    Variants:
    - mean_margin: E = z*·σ/√n
    - mean_ci:     x̄ ± E as an interval
    - prop_margin: E = z*·√(p̂(1-p̂)/n) with p̂ = 0.5
    - sample_size_mean: n = ⌈(z*·σ/E)²⌉
    - sample_size_prop: n = ⌈(z*/E)²·p̂(1-p̂)⌉
    - prop_ci: p̂ ± z*·SE
    - diff_means_ci / diff_props_ci: intervals for two-sample differences
    - width_effect: exact effect of changing confidence or sample size

    Op-codes used:
    - CI_SETUP: the givens and the goal
    - MOE_FORMULA / CI_FORMULA / SAMPLE_SIZE_FORMULA: the formula
    - ROOT / M / D / E / A / S / REWRITE (established)
    - CEIL: round a sample size up to the next whole unit
    - Z: the margin, interval, or sample size
    """

    VARIANTS = [*LEGACY_VARIANTS, *EXTENSION_VARIANTS]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        if self.variant in EXTENSION_VARIANTS:
            return self._generate_extension(self.variant)
        if self.variant is not None:
            return self._generate_legacy(self.variant)

        # Keep the exact post-call RNG state of the legacy generator so this
        # mid-registry extension does not churn unrelated seeded catalog rows.
        legacy = self._generate_legacy(random.choice(LEGACY_VARIANTS))
        post_legacy_state = random.getstate()
        digest = hashlib.sha256(
            legacy["problem"].encode("utf-8")
            + repr(post_legacy_state).encode("ascii")
        ).digest()
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            index = digest[0] % len(self.VARIANTS)
            if index < len(LEGACY_VARIANTS):
                legacy["problem"] = _frame(legacy["problem"])
                return legacy
            return self._generate_extension(
                EXTENSION_VARIANTS[index - len(LEGACY_VARIANTS)])
        finally:
            random.setstate(post_legacy_state)

    @staticmethod
    def _extension_result(variant, core, steps, answer):
        problem = f"{_frame(core)}\n{random.choice(EXTENSION_QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"confidence_interval_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    @staticmethod
    def _interval_tail(center, se, z_text):
        z = Fraction(z_text)
        margin = z * se
        lower, upper = center - margin, center + margin
        steps = [step("LOOKUP_SUPPLIED", "z*", z_text),
                 step("MOE_FORMULA", "E = z*·SE"),
                 step("M", z_text, num_txt(se), num_txt(margin)),
                 step("CI_FORMULA", "estimate ± E"),
                 step("S", num_txt(center), num_txt(margin), num_txt(lower)),
                 step("A", num_txt(center), num_txt(margin), num_txt(upper)),
                 step("REWRITE", f"({num_txt(lower)}, {num_txt(upper)})")]
        return steps, f"({num_txt(lower)}, {num_txt(upper)})"

    @classmethod
    def _prop_ci(cls):
        phat, n, se = random.choice(PROP_SE_BANK)
        z_text = random.choice(Z_STARS)
        q = 1 - phat
        product = phat * q
        variance = product / n
        core = (f"A sample of size {n} has p̂ = {num_txt(phat)}. Using "
                f"z* = {z_text}, find the confidence interval for p.")
        steps = [step("CI_SETUP", f"p̂ = {num_txt(phat)}, n = {n}",
                      f"z* = {z_text}"),
                 step("S", 1, num_txt(phat), num_txt(q)),
                 step("M", num_txt(phat), num_txt(q), num_txt(product)),
                 step("D", num_txt(product), n, num_txt(variance)),
                 step("ROOT", num_txt(variance), 2, num_txt(se))]
        tail, answer = cls._interval_tail(phat, se, z_text)
        steps.extend(tail)
        return cls._extension_result("prop_ci", core, steps, answer)

    @classmethod
    def _diff_means(cls):
        sigma1, n1, sigma2, n2, variance = random.choice(TWO_SAMPLE_SE_BANK)
        se = Fraction(math.isqrt(variance))
        mean1 = random.randint(50, 220)
        difference = random.choice([value for value in range(-30, 31) if value])
        mean2 = mean1 - difference
        z_text = random.choice(Z_STARS)
        term1, term2 = Fraction(sigma1 * sigma1, n1), Fraction(sigma2 * sigma2, n2)
        core = (f"Independent samples have x̄1 = {mean1}, population σ1 = "
                f"{sigma1}, n1 = {n1}; x̄2 = {mean2}, population σ2 = "
                f"{sigma2}, n2 = {n2}. Using z* = {z_text}, find the "
                "confidence interval for μ1 − μ2.")
        steps = [step("CI_SETUP", f"x̄1 = {mean1}, x̄2 = {mean2}",
                      f"σ1 = {sigma1}, n1 = {n1}, σ2 = {sigma2}, n2 = {n2}"),
                 step("E", sigma1, 2, sigma1 * sigma1),
                 step("D", sigma1 * sigma1, n1, num_txt(term1)),
                 step("E", sigma2, 2, sigma2 * sigma2),
                 step("D", sigma2 * sigma2, n2, num_txt(term2)),
                 step("A", num_txt(term1), num_txt(term2), num_txt(variance)),
                 step("ROOT", num_txt(variance), 2, num_txt(se)),
                 step("S", mean1, mean2, difference)]
        tail, answer = cls._interval_tail(Fraction(difference), se, z_text)
        steps.extend(tail)
        return cls._extension_result("diff_means_ci", core, steps, answer)

    @classmethod
    def _diff_props(cls):
        (phat1, n1), (phat2, n2), se = random.choice(DIFF_PROP_SE_BANK)
        if random.choice((True, False)):
            phat1, phat2, n1, n2 = phat2, phat1, n2, n1
        z_text = random.choice(Z_STARS)
        q1, q2 = 1 - phat1, 1 - phat2
        product1, product2 = phat1 * q1, phat2 * q2
        term1, term2 = product1 / n1, product2 / n2
        variance = term1 + term2
        difference = phat1 - phat2
        core = (f"Independent samples have p̂1 = {num_txt(phat1)}, n1 = {n1}; "
                f"p̂2 = {num_txt(phat2)}, n2 = {n2}. Using z* = {z_text}, "
                "find the confidence interval for p1 − p2.")
        steps = [step("CI_SETUP", f"p̂1 = {num_txt(phat1)}, n1 = {n1}",
                      f"p̂2 = {num_txt(phat2)}, n2 = {n2}"),
                 step("S", 1, num_txt(phat1), num_txt(q1)),
                 step("M", num_txt(phat1), num_txt(q1), num_txt(product1)),
                 step("D", num_txt(product1), n1, num_txt(term1)),
                 step("S", 1, num_txt(phat2), num_txt(q2)),
                 step("M", num_txt(phat2), num_txt(q2), num_txt(product2)),
                 step("D", num_txt(product2), n2, num_txt(term2)),
                 step("A", num_txt(term1), num_txt(term2), num_txt(variance)),
                 step("ROOT", num_txt(variance), 2, num_txt(se)),
                 step("S", num_txt(phat1), num_txt(phat2), num_txt(difference))]
        tail, answer = cls._interval_tail(difference, se, z_text)
        steps.extend(tail)
        return cls._extension_result("diff_props_ci", core, steps, answer)

    @classmethod
    def _width_effect(cls):
        if random.choice((True, False)):
            lower_text, upper_text = sorted(random.sample(Z_STARS, 2),
                                            key=Fraction)
            se = Fraction(random.randint(1, 5))
            lower_margin = Fraction(lower_text) * se
            upper_margin = Fraction(upper_text) * se
            lower_width, upper_width = 2 * lower_margin, 2 * upper_margin
            core = (f"With SE = {num_txt(se)}, change the supplied critical "
                    f"value from z* = {lower_text} to z* = {upper_text}. "
                    "Compare confidence-interval width.")
            steps = [step("WIDTH_FORMULA", "width = 2E, E = z*·SE"),
                     step("LOOKUP_SUPPLIED", "old z*", lower_text),
                     step("LOOKUP_SUPPLIED", "new z*", upper_text),
                     step("M", lower_text, num_txt(se), num_txt(lower_margin)),
                     step("M", 2, num_txt(lower_margin), num_txt(lower_width)),
                     step("M", upper_text, num_txt(se), num_txt(upper_margin)),
                     step("M", 2, num_txt(upper_margin), num_txt(upper_width)),
                     step("CHECK", "new width vs old width",
                          f"{num_txt(upper_width)} > {num_txt(lower_width)}",
                          "wider")]
            answer = f"wider; z* {lower_text} → {upper_text}"
        else:
            old_root, new_root = random.choice(((5, 10), (10, 20)))
            old_n, new_n = old_root * old_root, new_root * new_root
            sigma = random.randint(5, 30)
            z_text = random.choice(Z_STARS)
            old_se, new_se = Fraction(sigma, old_root), Fraction(sigma, new_root)
            old_margin, new_margin = Fraction(z_text) * old_se, Fraction(z_text) * new_se
            core = (f"Keep σ = {sigma} and z* = {z_text}, but increase sample "
                    f"size from n = {old_n} to n = {new_n}. Compare "
                    "confidence-interval width.")
            steps = [step("WIDTH_FORMULA", "width = 2E, E = z*·σ/√n"),
                     step("LOOKUP_SUPPLIED", "z*", z_text),
                     step("ROOT", old_n, 2, old_root),
                     step("ROOT", new_n, 2, new_root),
                     step("D", sigma, old_root, num_txt(old_se)),
                     step("D", sigma, new_root, num_txt(new_se)),
                     step("M", z_text, num_txt(old_se), num_txt(old_margin)),
                     step("M", z_text, num_txt(new_se), num_txt(new_margin)),
                     step("CHECK", "new E vs old E",
                          f"{num_txt(new_margin)} = {num_txt(old_margin)}/2",
                          "narrower")]
            answer = f"narrower; √n {old_root} → {new_root} halves E"
        return cls._extension_result("width_effect", core, steps, answer)

    def _generate_extension(self, variant):
        if variant == "prop_ci":
            return self._prop_ci()
        if variant == "diff_means_ci":
            return self._diff_means()
        if variant == "diff_props_ci":
            return self._diff_props()
        return self._width_effect()

    def _generate_legacy(self, variant):
        z = random.choice(Z_STARS)
        zf = Fraction(z)

        if variant in ("mean_margin", "mean_ci"):
            n = random.choice(SQUARE_N)
            root = int(math.isqrt(n))
            sigma = random.randint(2, 30)
            zsig = zf * sigma
            E = zsig / root
            steps = [
                step("CI_SETUP",
                     f"σ = {sigma}, n = {n}, z* = {z}",
                     "margin of error" if variant == "mean_margin"
                     else "confidence interval for μ"),
                step("MOE_FORMULA", "E = z*·σ/√n"),
                step("ROOT", f"√{n}", root),
                step("M", z, sigma, dec(zsig)),
                step("D", dec(zsig), root, dec(E)),
            ]
            if variant == "mean_margin":
                answer = dec(E)
                problem = random.choice([
                    f"A sample of size {n} has population standard deviation σ = {sigma}. Using z* = {z}, find the margin of error for a confidence interval for the mean.",
                    f"For a mean confidence interval, a sample of size {n} has population standard deviation σ = {sigma}. Using z* = {z}, find the margin of error.",
                    f"Using z* = {z}, find the margin of error for a confidence interval for the mean when a sample of size {n} has σ = {sigma}.",
                ])
            else:
                xbar = random.randint(20, 200)
                lo, hi = xbar - E, xbar + E
                steps += [
                    step("CI_FORMULA", "x̄ ± E"),
                    step("S", xbar, dec(E), dec(lo)),
                    step("A", xbar, dec(E), dec(hi)),
                    step("REWRITE", f"({dec(lo)}, {dec(hi)})"),
                ]
                answer = f"({dec(lo)}, {dec(hi)})"
                problem = random.choice([
                    f"A sample of size {n} has mean x̄ = {xbar} and population standard deviation σ = {sigma}. Using z* = {z}, find the confidence interval for the mean.",
                    f"Using z* = {z}, find the confidence interval for the mean for a sample of size {n} with x̄ = {xbar} and σ = {sigma}.",
                    f"A study reports x̄ = {xbar}, σ = {sigma}, and a sample of size {n}. Using z* = {z}, find the confidence interval for the mean.",
                ])
        elif variant == "prop_margin":
            n = random.choice(SQUARE_N)
            root = int(math.isqrt(n))
            phat = Fraction(1, 2)
            pq = phat * (1 - phat)
            se = pq / n
            se_root = Fraction(1, 2) / root
            E = zf * se_root
            steps = [
                step("CI_SETUP", f"p̂ = 0.5, n = {n}, z* = {z}",
                     "margin of error"),
                step("MOE_FORMULA", "E = z*·√(p̂(1-p̂)/n)"),
                step("M", "0.5", "0.5", dec(pq)),
                step("D", dec(pq), n, dec(se)),
                step("ROOT", f"√{dec(se)}", dec(se_root)),
                step("M", z, dec(se_root), dec(E)),
            ]
            answer = dec(E)
            problem = random.choice([
                f"A sample of size {n} has sample proportion p̂ = 0.5. Using z* = {z}, find the margin of error for a confidence interval for the proportion.",
                f"Using z* = {z}, find the margin of error for a confidence interval for the proportion when a sample of size {n} has p̂ = 0.5.",
                f"In a proportion study, a sample of size {n} has p̂ = 0.5. Using z* = {z}, find the margin of error for a confidence interval for the proportion.",
            ])
        elif variant == "sample_size_mean":
            sigma = random.randint(2, 30)
            E = random.choice(MARGINS)
            Ef = Fraction(E)
            zsig = zf * sigma
            ratio = zsig / Ef
            sq = ratio * ratio
            n = math.ceil(sq)
            steps = [
                step("CI_SETUP",
                     f"σ = {sigma}, E = {E}, z* = {z}",
                     "minimum sample size for the mean"),
                step("SAMPLE_SIZE_FORMULA", "n = (z*·σ/E)^2"),
                step("M", z, sigma, dec(zsig)),
                step("D", dec(zsig), E, dec(ratio)),
                step("E", dec(ratio), 2, dec(sq)),
                step("CEIL", dec(sq), n),
            ]
            answer = str(n)
            problem = random.choice([
                f"You want a margin of error of {E} for a confidence interval for the mean, with population standard deviation σ = {sigma}. Using z* = {z}, find the minimum sample size.",
                f"Using z* = {z}, find the minimum sample size for a mean confidence interval with margin of error of {E} and σ = {sigma}.",
                f"A planned mean confidence interval needs margin of error of {E}, with σ = {sigma}. Using z* = {z}, find the minimum sample size.",
            ])
        else:
            phat = Fraction(random.choice([2, 3, 4, 5, 6, 7, 8]), 10)
            E = random.choice(PROP_MARGINS)
            Ef = Fraction(E)
            ratio = zf / Ef
            sq = ratio * ratio
            pq = phat * (1 - phat)
            val = sq * pq
            n = math.ceil(val)
            steps = [
                step("CI_SETUP",
                     f"p̂ = {dec(phat)}, E = {E}, z* = {z}",
                     "minimum sample size for the proportion"),
                step("SAMPLE_SIZE_FORMULA", "n = (z*/E)^2·p̂(1-p̂)"),
                step("D", z, E, dec(ratio)),
                step("E", dec(ratio), 2, dec(sq)),
                step("M", dec(phat), dec(1 - phat), dec(pq)),
                step("M", dec(sq), dec(pq), dec(val)),
                step("CEIL", dec(val), n),
            ]
            answer = str(n)
            problem = random.choice([
                f"You want a margin of error of {E} for a confidence interval for a proportion, with estimated p̂ = {dec(phat)}. Using z* = {z}, find the minimum sample size.",
                f"Using z* = {z}, find the minimum sample size for a proportion confidence interval with margin of error of {E} and estimated p̂ = {dec(phat)}.",
                f"A planned proportion interval uses estimated p̂ = {dec(phat)} and margin of error of {E}. Using z* = {z}, find the minimum sample size.",
            ])
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"confidence_interval_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

"""Type-II error and power for exact, supplied-table one-sided z tests.

Variants: ``critical_xbar``, ``beta``, ``power``, ``alpha_from_cutoff``, and
``effect_of_n``. Perfect-square sample sizes make ``SE = σ/√n`` exact;
the true mean is constructed backward from an exact two- or three-decimal z,
so no statistic is rounded onto a Φ row. Every required row plus two decoys
is printed. Op-codes: ``HT_SETUP``, ``CRIT_REGION``, ``POWER_FORMULA``,
``TABLE_LOOKUP``, ``REWRITE``, ``ROOT``, ``ZSCORE``, ``M``, ``D``, ``A``,
``S``, ``CHECK``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import p4, phi
from stats_common import num_txt


STATISTICS = True
CRITICAL_BANK = (
    ("0.10", Fraction("1.28")),
    ("0.05", Fraction("1.645")),
    ("0.02", Fraction("2.05")),
    ("0.01", Fraction("2.33")),
)
STANDARD_ERRORS = (Fraction(1, 2), Fraction(1), Fraction(2),
                   Fraction(4), Fraction(5), Fraction(10))
ROOT_N_BANK = (2, 4, 10, 20)
BETA_Z_BANK = tuple(Fraction(value, 100) for value in
                    (25, 40, 55, 70, 85, 100, 115, 130, 145, 160,
                     175, 190, 205, 220, 235, 250))
EFFECT_SE_PAIRS = ((Fraction(1), Fraction(1, 2)),
                   (Fraction(2), Fraction(1)),
                   (Fraction(4), Fraction(2)),
                   (Fraction(10), Fraction(5)))
EFFECT_MAGNITUDES = tuple(Fraction(value, 100)
                          for value in (25, 35, 45, 50))

VENUES = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
QUERIES = {
    "critical_xbar": (
        "Find the critical sample-mean cutoff.",
        "Compute the x̄ boundary of the rejection region.",
        "At what sample mean does rejection begin?",
        "Use z* and SE to obtain the critical x̄ value.",
    ),
    "beta": (
        "At the stated true mean, find the Type-II error probability β.",
        "Compute the probability of failing to reject this false null.",
        "Use the cutoff to determine β at the alternative mean.",
        "Find β from the supplied Φ excerpt.",
    ),
    "power": (
        "At the stated true mean, find β and the power.",
        "Compute the Type-II error probability and then 1 − β.",
        "Use the rejection cutoff to obtain the test's power.",
        "Report both β and power from the supplied Φ row.",
    ),
    "alpha_from_cutoff": (
        "Find the right-tail significance level α from the cutoff.",
        "Standardize the critical x̄ value and compute its upper tail.",
        "What Type-I error probability corresponds to this boundary?",
        "Use the supplied z and Φ row to recover α.",
    ),
    "effect_of_n": (
        "Compare the power before and after increasing the sample size.",
        "Compute both powers and state how SE changes.",
        "Quantify the effect of the larger n on power.",
        "Report the old-to-new power and standard-error comparison.",
    ),
}


def _site():
    code = f"cohort {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(VENUES)} ({code})")


def _z_text(value):
    value = Fraction(value)
    places = 3 if (value * 100).denominator != 1 else 2
    return f"{float(value):.{places}f}"


def _phi_excerpt(required):
    needed = sorted({abs(Fraction(value)) for value in required})
    candidates = []
    for base, offset in ((needed[0], Fraction(1, 5)),
                         (needed[-1], Fraction(3, 10)),
                         (needed[0], Fraction(-1, 5)),
                         (needed[-1], Fraction(-3, 10)),
                         (needed[0], Fraction(2, 5)),
                         (needed[-1], Fraction(-2, 5))):
        candidate = base + offset
        if (0 < candidate <= Fraction(17, 5) and candidate not in needed
                and candidate not in candidates):
            candidates.append(candidate)
        if len(candidates) == 2:
            break
    assert len(candidates) == 2
    rows = sorted([*needed, *candidates])
    cells = "; ".join(
        f"z={_z_text(value)}: {p4(phi(float(value)))}" for value in rows
    )
    return f"Standard normal table, Φ(z) = P(Z < z): {cells}"


def _lookup_value(magnitude):
    return Fraction(p4(phi(float(abs(magnitude)))))


def _base_case():
    alpha, critical_z = random.choice(CRITICAL_BANK)
    se = random.choice(STANDARD_ERRORS)
    root_n = random.choice(ROOT_N_BANK)
    sigma = se * root_n
    mu0 = random.randint(20, 200)
    cutoff = Fraction(mu0) + critical_z * se
    return alpha, critical_z, se, root_n, sigma, mu0, cutoff


def _se_steps(sigma, root_n, se):
    return [step("ROOT", root_n * root_n, 2, root_n),
            step("D", num_txt(sigma), root_n, num_txt(se))]


def _cutoff_steps(mu0, critical_z, se, cutoff):
    margin = critical_z * se
    return [step("M", _z_text(critical_z), num_txt(se), num_txt(margin)),
            step("A", mu0, num_txt(margin), num_txt(cutoff)),
            step("CRIT_REGION",
                 f"reject if x̄ > {mu0} + {_z_text(critical_z)}·{num_txt(se)}",
                 num_txt(cutoff))]


def _beta_steps(cutoff, true_mean, se, z_beta):
    magnitude = abs(z_beta)
    lookup = _lookup_value(magnitude)
    steps = [
        step("POWER_FORMULA",
             f"β = P(x̄ ≤ {num_txt(cutoff)} given μ = {num_txt(true_mean)})"),
        step("ZSCORE",
             f"({num_txt(cutoff)} − {num_txt(true_mean)})/{num_txt(se)}",
             _z_text(z_beta)),
        step("TABLE_LOOKUP", f"Φ({_z_text(magnitude)})", p4(lookup)),
    ]
    if z_beta < 0:
        beta = 1 - lookup
        steps.extend([
            step("REWRITE", f"Φ({_z_text(z_beta)}) = 1 − "
                 f"Φ({_z_text(magnitude)})"),
            step("S", "1.0000", p4(lookup), p4(beta)),
        ])
    else:
        beta = lookup
    power = 1 - beta
    steps.append(step("S", "1.0000", p4(beta), p4(power)))
    return steps, beta, power


class TypeErrorPowerGenerator(ProblemGenerator):
    """Generate critical cutoffs, Type-II errors, and exact table powers.

    Variants are ``critical_xbar``, ``beta``, ``power``,
    ``alpha_from_cutoff``, and ``effect_of_n``. Sample sizes are perfect
    squares, and alternative means are constructed from exact z rows rather
    than rounded onto them. Op-codes are ``HT_SETUP``, ``CRIT_REGION``,
    ``POWER_FORMULA``, ``TABLE_LOOKUP``, ``REWRITE``, ``ROOT``, ``ZSCORE``,
    ``M``, ``D``, ``A``, ``S``, ``CHECK``, and ``Z``.
    """

    VARIANTS = tuple(QUERIES)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _setup(mu0, sigma, n, alpha=None, critical_z=None):
        detail = f"σ = {num_txt(sigma)}, n = {n}"
        if alpha is not None:
            detail += f", α = {alpha}, z* = {_z_text(critical_z)}"
        return step("HT_SETUP", f"H0: μ = {mu0}; Ha: μ > {mu0}", detail)

    @staticmethod
    def _problem(prefix, table, query):
        pieces = [prefix]
        if table is not None:
            pieces.append(table)
        pieces.append(query)
        return "\n".join(pieces)

    @staticmethod
    def _result(variant, problem, steps, answer):
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_type_error_power_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _single_n(self, variant):
        alpha, critical_z, se, root_n, sigma, mu0, cutoff = _base_case()
        n = root_n * root_n
        steps = [self._setup(mu0, sigma, n, alpha, critical_z)]
        steps.extend(_se_steps(sigma, root_n, se))
        steps.extend(_cutoff_steps(mu0, critical_z, se, cutoff))
        table = None
        true_text = ""
        if variant == "critical_xbar":
            answer = num_txt(cutoff)
        else:
            eligible = [value for value in BETA_Z_BANK
                        if value < critical_z]
            magnitude = random.choice(eligible)
            z_beta = random.choice((-magnitude, magnitude))
            true_mean = cutoff - z_beta * se
            assert true_mean > mu0
            extra, beta, power = _beta_steps(cutoff, true_mean, se, z_beta)
            steps.extend(extra)
            table = _phi_excerpt([abs(z_beta)])
            true_text = f" The true mean is μ = {num_txt(true_mean)}."
            if variant == "beta":
                answer = f"β = {p4(beta)}"
            else:
                answer = f"β = {p4(beta)}; power = {p4(power)}"
        prefix = (f"At the {_site()}, a right-tailed known-σ test uses "
                  f"H0: μ = {mu0} versus Ha: μ > {mu0}. Data: σ = "
                  f"{num_txt(sigma)}, n = {n}, α = {alpha} "
                  f"(z* = {_z_text(critical_z)}).{true_text}")
        problem = self._problem(prefix, table, random.choice(QUERIES[variant]))
        return self._result(variant, problem, steps, answer)

    def _alpha_from_cutoff(self):
        _, critical_z, se, root_n, sigma, mu0, cutoff = _base_case()
        n = root_n * root_n
        lookup = _lookup_value(critical_z)
        alpha = 1 - lookup
        prefix = (f"At the {_site()}, a right-tailed known-σ test uses "
                  f"H0: μ = {mu0} versus Ha: μ > {mu0}. Data: σ = "
                  f"{num_txt(sigma)}, n = {n}, critical x̄ = "
                  f"{num_txt(cutoff)}, and supplied z = "
                  f"{_z_text(critical_z)}.")
        table = _phi_excerpt([critical_z])
        steps = [self._setup(mu0, sigma, n)]
        steps.extend(_se_steps(sigma, root_n, se))
        steps.extend([
            step("S", num_txt(cutoff), mu0, num_txt(cutoff - mu0)),
            step("D", num_txt(cutoff - mu0), num_txt(se),
                 _z_text(critical_z)),
            step("TABLE_LOOKUP", f"Φ({_z_text(critical_z)})", p4(lookup)),
            step("S", "1.0000", p4(lookup), p4(alpha)),
        ])
        answer = f"α = {p4(alpha)}"
        problem = self._problem(
            prefix, table, random.choice(QUERIES["alpha_from_cutoff"]))
        return self._result("alpha_from_cutoff", problem, steps, answer)

    def _effect_of_n(self):
        alpha, critical_z = random.choice(CRITICAL_BANK)
        old_se, new_se = random.choice(EFFECT_SE_PAIRS)
        old_root = random.choice((4, 10, 20))
        new_root = 2 * old_root
        sigma = old_se * old_root
        assert sigma == new_se * new_root
        old_n, new_n = old_root * old_root, new_root * new_root
        mu0 = random.randint(20, 200)
        old_cutoff = Fraction(mu0) + critical_z * old_se
        new_cutoff = Fraction(mu0) + critical_z * new_se
        old_magnitude = random.choice(EFFECT_MAGNITUDES)
        effect = (critical_z + old_magnitude) * old_se
        true_mean = Fraction(mu0) + effect
        old_z = -old_magnitude
        new_z = critical_z - effect / new_se
        assert -Fraction(17, 5) <= new_z < old_z < 0
        old_lookup, new_lookup = (_lookup_value(abs(old_z)),
                                  _lookup_value(abs(new_z)))
        old_power, new_power = old_lookup, new_lookup
        prefix = (f"At the {_site()}, a right-tailed known-σ test uses "
                  f"H0: μ = {mu0} versus Ha: μ > {mu0}, with σ = "
                  f"{num_txt(sigma)}, α = {alpha} "
                  f"(z* = {_z_text(critical_z)}), and true μ = "
                  f"{num_txt(true_mean)}. Compare n = {old_n} with "
                  f"n = {new_n}.")
        table = _phi_excerpt([abs(old_z), abs(new_z)])
        steps = [self._setup(mu0, sigma, old_n, alpha, critical_z)]
        steps.extend(_se_steps(sigma, old_root, old_se))
        steps.extend(_cutoff_steps(mu0, critical_z, old_se, old_cutoff))
        old_steps, _, checked_old_power = _beta_steps(
            old_cutoff, true_mean, old_se, old_z)
        steps.extend(old_steps)
        steps.append(step("HT_SETUP", f"same H0 and Ha; n = {new_n}",
                          f"σ = {num_txt(sigma)}, z* = {_z_text(critical_z)}"))
        steps.extend(_se_steps(sigma, new_root, new_se))
        steps.extend(_cutoff_steps(mu0, critical_z, new_se, new_cutoff))
        new_steps, _, checked_new_power = _beta_steps(
            new_cutoff, true_mean, new_se, new_z)
        steps.extend(new_steps)
        assert checked_old_power == old_power
        assert checked_new_power == new_power
        steps.append(step("CHECK", "larger n effect",
                          f"{p4(old_power)} < {p4(new_power)}",
                          "power increases"))
        answer = (f"power {p4(old_power)} → {p4(new_power)}; SE "
                  f"{num_txt(old_se)} → {num_txt(new_se)}")
        problem = self._problem(
            prefix, table, random.choice(QUERIES["effect_of_n"]))
        return self._result("effect_of_n", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("critical_xbar", "beta", "power"):
            return self._single_n(variant)
        if variant == "alpha_from_cutoff":
            return self._alpha_from_cutoff()
        return self._effect_of_n()

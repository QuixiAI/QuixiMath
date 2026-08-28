"""Approximate binomial probabilities with a supplied normal table.

Variants: ``at_most``, ``at_least``, ``exactly``, ``between``,
``check_conditions``, and ``mean_sd``. Op-codes: ``BINOM_SETUP``,
``CONT_CORR``, ``ZSCORE``, ``TABLE_LOOKUP``, ``REWRITE``, ``ROOT``, ``M``,
``A``, ``S``, ``D``, ``CHECK``, and ``Z``. Probability cases are built from
``NP_BANK`` pairs with perfect-square ``np(1-p)`` and backward half-integer
boundaries, so z-scores are exact two-decimal table entries; the needed Φ
values and two decoys are always supplied in the problem.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import NP_BANK, binomial_sigma, exact, p4, phi, phi_table, prob_txt


PROBABILITY = True
STATISTICS = True
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
CONTEXTS = ("inspected components that pass", "customers who subscribe",
            "free throws that score", "seeds that germinate",
            "packages that arrive on time", "devices that connect",
            "applicants who qualify", "samples that test positive",
            "orders that ship today", "questions answered correctly")
QUERIES = {
    "at_most": (
        "Estimate the displayed lower-tail probability to four decimal places.",
        "Apply the continuity correction and read the supplied Φ excerpt.",
        "Use the normal approximation to find P(X at most the cutoff).",
        "What is the corrected normal estimate of this binomial lower tail?",
        "Standardize the upper boundary and use the printed table only.",
    ),
    "at_least": (
        "Estimate the displayed upper-tail probability to four decimal places.",
        "Apply the continuity correction and complement the supplied Φ value.",
        "Use the normal approximation to find P(X at least the cutoff).",
        "What is the corrected normal estimate of this binomial upper tail?",
        "Standardize the lower boundary and use the printed table only.",
    ),
    "exactly": (
        "Estimate the displayed point probability to four decimal places.",
        "Use both continuity-corrected boundaries around the target count.",
        "Approximate P(X exactly the target) from the supplied Φ excerpt.",
        "What normal area corresponds to this single binomial count?",
        "Subtract the two printed cumulative probabilities after standardizing.",
    ),
    "between": (
        "Estimate the displayed inclusive interval probability to four decimal places.",
        "Apply continuity correction at both ends and use the supplied table.",
        "Approximate the binomial probability between the two counts.",
        "What corrected normal area represents this inclusive count interval?",
        "Standardize both outer boundaries and subtract the printed Φ values.",
    ),
    "check_conditions": (
        "Decide whether the usual normal-approximation count conditions hold.",
        "Check both np ≥ 10 and n(1 − p) ≥ 10.",
        "Report whether a normal approximation is justified by the count rule.",
        "Evaluate both expected success and expected failure counts.",
        "Give a composite pass-or-fail condition statement.",
    ),
    "mean_sd": (
        "Find the binomial mean and standard deviation.",
        "Compute μ = np and σ = sqrt(np(1 − p)).",
        "Report the exact center and spread used by the normal approximation.",
        "What are the mean and standard deviation of X?",
        "Build the normal model's parameters from n and p.",
    ),
}


APPROX_BANK = tuple((n, p) for n, p in NP_BANK
                    if n * p >= 10 and n * (1 - p) >= 10)


def _z_text(value):
    return f"{float(value):.2f}"


def _table_probability(z):
    return Fraction(p4(phi(float(abs(z)))))


def _cdf_steps(z):
    magnitude = abs(z)
    lookup = _table_probability(z)
    steps = [step("TABLE_LOOKUP", f"Φ({_z_text(magnitude)})", p4(lookup))]
    if z < 0:
        value = 1 - lookup
        steps.extend([step("REWRITE",
                           f"Φ({_z_text(z)}) = 1 − Φ({_z_text(magnitude)})"),
                      step("S", "1.0000", p4(lookup), p4(value))])
        return steps, value
    return steps, lookup


def _moments_steps(n, p):
    mean = n * p
    q = 1 - p
    variance = mean * q
    sigma = binomial_sigma(n, p)
    return [step("M", n, prob_txt(p), prob_txt(mean)),
            step("S", 1, prob_txt(p), prob_txt(q)),
            step("M", prob_txt(mean), prob_txt(q), prob_txt(variance)),
            step("ROOT", prob_txt(variance), 2, sigma)], mean, variance, sigma


def _valid_half_offsets(n, mean, sigma, mode):
    candidates = []
    for half_units in range(-5 * sigma, 5 * sigma + 1):
        if half_units % 2 == 0:
            continue
        boundary = mean + Fraction(half_units, 2)
        count = boundary - Fraction(1, 2) if mode == "at_most" else boundary + Fraction(1, 2)
        if count.denominator == 1 and 0 <= count <= n:
            if mode != "at_least" or half_units > 0:
                candidates.append((half_units, int(count)))
    return candidates


class NormalApproxBinomialGenerator(ProblemGenerator):
    """Generate exact-setup, supplied-table binomial normal approximations."""

    VARIANTS = ("at_most", "at_least", "exactly", "between",
                "check_conditions", "mean_sd")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _prefix(n, p, goal, table=None):
        venue, city = random.choice(VENUES), random.choice(CITIES)
        context = random.choice(CONTEXTS)
        text = (f"At the {venue} in {city}, X counts {context} in {n} independent "
                f"trials with success probability p = {prob_txt(p)}. Target: {goal}.")
        if table:
            text += f" Use a normal approximation with continuity correction. {table}."
        return text

    @staticmethod
    def _conditions(n, p):
        successes = n * p
        failures = n * (1 - p)
        ok = successes >= 10 and failures >= 10
        relation_success = "≥" if successes >= 10 else "<"
        relation_failure = "≥" if failures >= 10 else "<"
        answer = (f"{'ok' if ok else 'fails'}; np = {prob_txt(successes)} "
                  f"{relation_success} 10, n(1 − p) = {prob_txt(failures)} "
                  f"{relation_failure} 10")
        steps = [step("M", n, prob_txt(p), prob_txt(successes)),
                 step("S", 1, prob_txt(p), prob_txt(1 - p)),
                 step("M", n, prob_txt(1 - p), prob_txt(failures)),
                 step("CHECK", "np ≥ 10 and n(1 − p) ≥ 10",
                      f"{prob_txt(successes)}, {prob_txt(failures)}",
                      "ok" if ok else "fails")]
        return steps, answer

    @staticmethod
    def _probability(variant):
        n, p = random.choice(APPROX_BANK)
        moments, mean, _, sigma = _moments_steps(n, p)
        condition_steps, _ = NormalApproxBinomialGenerator._conditions(n, p)
        condition_check = condition_steps[-1]
        if variant in ("at_most", "at_least"):
            half_units, cutoff = random.choice(
                _valid_half_offsets(n, mean, sigma, variant))
            boundary = mean + Fraction(half_units, 2)
            z = Fraction(half_units, 2 * sigma)
            goal = f"P(X {'≤' if variant == 'at_most' else '≥'} {cutoff})"
            normal_goal = (f"P(Y {'≤' if variant == 'at_most' else '≥'} "
                           f"{exact(boundary)})")
            table = phi_table([float(abs(z))])
            steps = [step("BINOM_SETUP", f"n = {n}, p = {prob_txt(p)}", goal),
                     condition_check] + moments
            steps.extend([step("CONT_CORR", goal, normal_goal),
                          step("ZSCORE",
                               f"({exact(boundary)} − {prob_txt(mean)})/{sigma}",
                               _z_text(z))])
            cdf_steps, cdf = _cdf_steps(z)
            steps.extend(cdf_steps)
            if variant == "at_most":
                value = cdf
            else:
                value = 1 - cdf
                steps.extend([step("REWRITE", f"{normal_goal} = 1 − Φ({_z_text(z)})"),
                              step("S", "1.0000", p4(cdf), p4(value))])
        elif variant == "exactly":
            max_delta = min(n - int(mean), int(Fraction(5 * sigma - 1, 2)))
            cutoff = int(mean) + random.randint(1, max_delta)
            low = Fraction(2 * cutoff - 1, 2)
            high = Fraction(2 * cutoff + 1, 2)
            z_low, z_high = (low - mean) / sigma, (high - mean) / sigma
            goal = f"P(X = {cutoff})"
            normal_goal = f"P({exact(low)} < Y < {exact(high)})"
            table = phi_table([float(z_low), float(z_high)])
            steps = [step("BINOM_SETUP", f"n = {n}, p = {prob_txt(p)}", goal),
                     condition_check] + moments
            steps.extend([step("CONT_CORR", goal, normal_goal),
                          step("ZSCORE", f"({exact(low)} − {prob_txt(mean)})/{sigma}",
                               _z_text(z_low)),
                          step("ZSCORE", f"({exact(high)} − {prob_txt(mean)})/{sigma}",
                               _z_text(z_high))])
            low_steps, cdf_low = _cdf_steps(z_low)
            high_steps, cdf_high = _cdf_steps(z_high)
            value = cdf_high - cdf_low
            steps.extend(low_steps + high_steps)
            steps.append(step("S", p4(cdf_high), p4(cdf_low), p4(value)))
        else:
            max_upper = min(n - int(mean), 2 * sigma)
            lower_delta = random.randint(1, max(1, max_upper - 1))
            upper_delta = random.randint(lower_delta + 1, max_upper)
            lower_count, upper_count = int(mean) + lower_delta, int(mean) + upper_delta
            low = Fraction(2 * lower_count - 1, 2)
            high = Fraction(2 * upper_count + 1, 2)
            z_low, z_high = (low - mean) / sigma, (high - mean) / sigma
            goal = f"P({lower_count} ≤ X ≤ {upper_count})"
            normal_goal = f"P({exact(low)} < Y < {exact(high)})"
            table = phi_table([float(z_low), float(z_high)])
            steps = [step("BINOM_SETUP", f"n = {n}, p = {prob_txt(p)}", goal),
                     condition_check] + moments
            steps.extend([step("CONT_CORR", goal, normal_goal),
                          step("ZSCORE", f"({exact(low)} − {prob_txt(mean)})/{sigma}",
                               _z_text(z_low)),
                          step("ZSCORE", f"({exact(high)} − {prob_txt(mean)})/{sigma}",
                               _z_text(z_high))])
            low_steps, cdf_low = _cdf_steps(z_low)
            high_steps, cdf_high = _cdf_steps(z_high)
            value = cdf_high - cdf_low
            steps.extend(low_steps + high_steps)
            steps.append(step("S", p4(cdf_high), p4(cdf_low), p4(value)))
        prefix = NormalApproxBinomialGenerator._prefix(n, p, goal, table)
        return prefix, steps, p4(value)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("at_most", "at_least", "exactly", "between"):
            prefix, steps, answer = self._probability(variant)
        elif variant == "check_conditions":
            n, p = random.choice(NP_BANK)
            goal = "check normal-approximation conditions"
            prefix = self._prefix(n, p, goal)
            setup = step("BINOM_SETUP", f"n = {n}, p = {prob_txt(p)}", goal)
            extra, answer = self._conditions(n, p)
            steps = [setup] + extra
        else:
            n, p = random.choice(NP_BANK)
            goal = "find mean and standard deviation"
            prefix = self._prefix(n, p, goal)
            setup = step("BINOM_SETUP", f"n = {n}, p = {prob_txt(p)}", goal)
            extra, mean, _, sigma = _moments_steps(n, p)
            steps = [setup] + extra
            answer = f"mean {prob_txt(mean)}; sd {sigma}"
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_normal_approx_binomial_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

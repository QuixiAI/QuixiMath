import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
# The supplied-table helpers live in prob_common (plans/probability_plan.md §4);
# they stay importable from this module for the generators and tests that
# already reach for them here.
from prob_common import exact, p4, phi, phi_table


PROBABILITY = True
STATISTICS = True
SETTINGS = ("amber study", "birch survey", "cedar trial", "delta project",
            "ember lab", "forest audit", "granite program", "harbor test",
            "indigo review", "jade pilot", "kestrel study", "lunar trial",
            "maple project", "nova lab", "onyx survey", "pearl audit",
            "quartz program", "river test", "solar review", "topaz pilot",
            "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
QUERIES = {
    "below": (
        "What is the probability of a value below {x} {unit}?",
        "Find the probability of a value below {x} {unit}.",
        "Use the supplied table to compute the probability of a value below {x} {unit}.",
        "Determine the normal-model probability of a value below {x} {unit}.",
        "Standardize, then report the probability of a value below {x} {unit}.",
    ),
    "below_negative": (
        "What is the probability of a value below {x} {unit}?",
        "Find the probability of a value below {x} {unit} using symmetry.",
        "Use the supplied table to compute the probability of a value below {x} {unit}.",
        "Determine the lower-tail probability of a value below {x} {unit}.",
        "Standardize the negative z-score and find the probability of a value below {x} {unit}.",
    ),
    "above": (
        "What is the probability of a value above {x} {unit}?",
        "Find the probability of a value above {x} {unit}.",
        "Use the supplied table to compute the probability of a value above {x} {unit}.",
        "Determine the upper-tail probability of a value above {x} {unit}.",
        "Standardize, then report the probability of a value above {x} {unit}.",
    ),
    "between": (
        "What is the probability of a value between {a} and {b} {unit}?",
        "Find the probability of a value between {a} and {b} {unit}.",
        "Use the table to compute the probability of a value between {a} and {b} {unit}.",
        "Determine the normal area for a value between {a} and {b} {unit}.",
        "Standardize both bounds and report the probability of a value between {a} and {b} {unit}.",
    ),
    "inverse_lookup": (
        "Find x such that P(X < x) = {probability} by reading the supplied table backwards.",
        "Find x such that P(X < x) = {probability} using the matching supplied z entry.",
        "Find x such that P(X < x) = {probability}; invert the standardization exactly.",
        "Find x such that P(X < x) = {probability} from the supplied inverse lookup.",
        "Find x such that P(X < x) = {probability}, then check the resulting raw score.",
    ),
    "symmetric_interval": (
        "What is the probability in the symmetric interval from {lower} to {upper} {unit}?",
        "Find the probability in the symmetric interval from {lower} to {upper} {unit}.",
        "Use the table to compute the symmetric interval from {lower} to {upper} {unit}.",
        "Determine the normal area in the symmetric interval from {lower} to {upper} {unit}.",
        "Standardize the symmetric interval from {lower} to {upper} {unit} and report its probability.",
    ),
}


def _query(variant, selector, **fields):
    """Choose wording from generated parameters without consuming RNG state."""
    templates = QUERIES[variant]
    return templates[selector % len(templates)].format(**fields)


class NormalTableGenerator(ProblemGenerator):
    """
    Normal-distribution probabilities with the z-table excerpt supplied in
    the problem text (Principle 5: no lookups the problem doesn't provide).
    The scratchpad standardizes, reads the provided table, and applies the
    complement / symmetry / between rule explicitly.

    Variants: below, below_negative, above, between, inverse_lookup, and
    symmetric_interval. Inverse cases use half-integer z values with even
    standard deviations, and symmetric cases are constructed from an exact
    z radius, so every boundary is exact.

    Op-codes used:
    - NORM_SETUP: distribution and target probability (distribution, target)
    - ZSCORE: standardize (work, z)
    - TABLE_LOOKUP: read a provided table value (entry, value)
    - REWRITE: probability rule being applied (string)
    - RAW_FORMULA: invert x = μ + zσ
    - M / A / S: exact arithmetic on parameters and table values
    - Z: final answer (4-decimal probability)
    """

    CONTEXTS = [
        ("Exam scores", "points", 70, 90, 5, 15),
        ("Adult heights", "cm", 160, 178, 5, 9),
        ("Battery lifetimes", "hours", 40, 60, 4, 10),
        ("Package weights", "grams", 480, 520, 5, 12),
        ("Commute times", "minutes", 25, 45, 4, 9),
    ]

    VARIANTS = ["below", "below_negative", "above", "between",
                "inverse_lookup", "symmetric_interval"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _fmt(v):
        """Trims trailing zeros from a tenth-precision value: 119.5, 120."""
        return f"{v:g}"

    def _table(self, zs):
        """Renders the excerpt for the needed |z| values plus two decoys."""
        return phi_table(zs)

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        name, unit, mu_lo, mu_hi, s_lo, s_hi = random.choice(self.CONTEXTS)
        mu = random.randint(mu_lo, mu_hi)
        sigma = random.randint(s_lo, s_hi)

        def zpick():
            return round(random.randint(3, 25) / 10, 1)

        steps = []
        if variant == "inverse_lookup":
            even_sigmas = [value for value in range(s_lo, s_hi + 1)
                           if value % 2 == 0]
            sigma = random.choice(even_sigmas)
            z_fraction = random.choice((Fraction(1, 2), Fraction(1),
                                        Fraction(3, 2), Fraction(2),
                                        Fraction(5, 2)))
            z = float(z_fraction)
            target_probability = p4(phi(z))
            x = Fraction(mu) + z_fraction * sigma
            table = self._table([z])
            target = f"find x with P(X < x) = {target_probability}"
            steps.extend([
                step("NORM_SETUP", f"X ~ N({mu}, {sigma})", target),
                step("TABLE_LOOKUP", f"Φ(z) = {target_probability}",
                     f"{z:.2f}"),
                step("RAW_FORMULA", "x = μ + z·σ"),
                step("M", f"{z:.2f}", sigma, exact(z_fraction * sigma)),
                step("A", mu, exact(z_fraction * sigma), exact(x)),
                step("CHECK", f"P(X < {exact(x)})", target_probability),
            ])
            answer = exact(x)
            question = _query(variant, mu + sigma + int(10 * z),
                              probability=target_probability)
        elif variant == "symmetric_interval":
            z = round(random.randint(3, 25) / 10, 1)
            z_fraction = Fraction(str(z))
            radius = z_fraction * sigma
            lower, upper = Fraction(mu) - radius, Fraction(mu) + radius
            target = f"P({exact(lower)} < X < {exact(upper)})"
            table = self._table([z])
            cdf = Fraction(p4(phi(z)))
            doubled = 2 * cdf
            answer_value = doubled - 1
            steps.extend([
                step("NORM_SETUP", f"X ~ N({mu}, {sigma})", target),
                step("ZSCORE", f"({exact(upper)} - {mu})/{sigma}", f"{z:.2f}"),
                step("TABLE_LOOKUP", f"Φ({z:.2f})", p4(cdf)),
                step("REWRITE", f"{target} = 2Φ({z:.2f}) − 1"),
                step("M", 2, p4(cdf), p4(doubled)),
                step("S", p4(doubled), "1.0000", p4(answer_value)),
                step("CHECK", "symmetric tails have equal area", p4(answer_value)),
            ])
            answer = p4(answer_value)
            question = _query(variant, mu + sigma + int(10 * z),
                              lower=exact(lower), upper=exact(upper), unit=unit)
        elif variant == "between":
            z1, z2 = sorted(random.sample([round(v / 10, 1)
                                           for v in range(3, 26)], 2))
            a = mu + z1 * sigma
            b = mu + z2 * sigma
            target = f"P({self._fmt(a)} < X < {self._fmt(b)})"
            table = self._table([z1, z2])
            steps.append(step("NORM_SETUP", f"X ~ N({mu}, {sigma})", target))
            steps.append(step("ZSCORE", f"({self._fmt(a)} - {mu})/{sigma}", f"{z1:.2f}"))
            steps.append(step("ZSCORE", f"({self._fmt(b)} - {mu})/{sigma}", f"{z2:.2f}"))
            steps.append(step("TABLE_LOOKUP", f"Φ({z1:.2f})", p4(phi(z1))))
            steps.append(step("TABLE_LOOKUP", f"Φ({z2:.2f})", p4(phi(z2))))
            steps.append(step("REWRITE", f"{target} = Φ({z2:.2f}) - Φ({z1:.2f})"))
            answer = round(phi(z2) - phi(z1), 4)
            steps.append(step("S", p4(phi(z2)), p4(phi(z1)), p4(answer)))
            question = _query(variant,
                              mu + sigma + int(10 * z1) + int(10 * z2),
                              a=self._fmt(a), b=self._fmt(b), unit=unit)
        else:
            z = zpick()
            if variant == "below_negative":
                x = mu - z * sigma
                target = f"P(X < {self._fmt(x)})"
                z_signed = -z
            elif variant == "above":
                x = mu + z * sigma
                target = f"P(X > {self._fmt(x)})"
                z_signed = z
            else:  # below
                x = mu + z * sigma
                target = f"P(X < {self._fmt(x)})"
                z_signed = z
            table = self._table([z])
            steps.append(step("NORM_SETUP", f"X ~ N({mu}, {sigma})", target))
            steps.append(step("ZSCORE",
                              f"({self._fmt(x)} - {mu})/{sigma}", f"{z_signed:.2f}"))
            steps.append(step("TABLE_LOOKUP", f"Φ({z:.2f})", p4(phi(z))))
            if variant == "below":
                answer = phi(z)
            elif variant == "above":
                steps.append(step("REWRITE",
                                  f"{target} = 1 - Φ({z:.2f})"))
                answer = round(1 - phi(z), 4)
                steps.append(step("S", "1.0000", p4(phi(z)), p4(answer)))
            else:  # below_negative: symmetry
                steps.append(step("REWRITE",
                                  f"Φ({z_signed:.2f}) = 1 - Φ({z:.2f})"))
                answer = round(1 - phi(z), 4)
                steps.append(step("S", "1.0000", p4(phi(z)), p4(answer)))
            question = _query(variant, mu + sigma + int(10 * z),
                              x=self._fmt(x), unit=unit)

        final_answer = answer if variant in ("inverse_lookup", "symmetric_interval") \
            else p4(answer)
        steps.append(step("Z", final_answer))
        setting, city = random.choice(SETTINGS), random.choice(CITIES)
        problem = (f"At the {setting} in {city}, {name} are normally distributed "
                   f"with mean {mu} {unit} "
                   f"and standard deviation {sigma} {unit}. {question}\n{table}")

        return dict(
            problem_id=jid(),
            operation=f"normal_{'below' if variant == 'below_negative' else variant}",
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

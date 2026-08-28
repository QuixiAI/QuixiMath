"""Invert supplied normal-percentile z-scores with exact arithmetic.

Variants: ``cutoff_above``, ``cutoff_below``, ``middle_interval``,
``sigma_from_cutoff``, and ``mu_from_cutoff``. Each problem supplies the
needed percentile-z entry plus one decoy. The sigma-recovery bank uses z
values with terminating reciprocals and constructs cutoffs backward from an
exact sigma. Random models, targets, contexts, sites, decoys, and four
phrasings give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import num_txt, ordinal


STATISTICS = True
MAIN_BANK = (
    (Fraction(80), Fraction(84, 100)),
    (Fraction(90), Fraction(128, 100)),
    (Fraction(95), Fraction(1645, 1000)),
    (Fraction(195, 2), Fraction(196, 100)),
    (Fraction(99), Fraction(233, 100)),
)
SIGMA_BANK = (
    (Fraction(394, 5), Fraction(4, 5)),
    (Fraction(447, 5), Fraction(5, 4)),
    (Fraction(90), Fraction(32, 25)),
    (Fraction(189, 2), Fraction(8, 5)),
    (Fraction(497, 5), Fraction(5, 2)),
)
CONTEXTS = (
    ("exam scores", "points"), ("adult heights", "cm"),
    ("battery lifetimes", "hours"), ("package weights", "grams"),
    ("commute times", "minutes"), ("reaction times", "ms"),
    ("daily sales", "items"), ("plant heights", "cm"),
)
SETTINGS = (
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
    "cutoff_above": (
        "Find the cutoff separating the stated top percentage.",
        "Use the supplied percentile z-score to calculate the upper cutoff.",
        "What raw value begins the requested upper tail?",
        "Convert the selected upper percentile back to the measurement scale.",
    ),
    "cutoff_below": (
        "Find the cutoff separating the stated bottom percentage.",
        "Use symmetry and the supplied positive z-score for the lower cutoff.",
        "What raw value ends the requested lower tail?",
        "Convert the selected lower percentile back to the measurement scale.",
    ),
    "middle_interval": (
        "Find the symmetric interval containing the stated middle percentage.",
        "Use the supplied upper percentile z-score to calculate both bounds.",
        "What raw-score interval leaves equal tails outside it?",
        "Convert ±z from the selected central coverage to two cutoffs.",
    ),
    "sigma_from_cutoff": (
        "Find the standard deviation σ.",
        "Use the supplied z-score and cutoff to solve for σ.",
        "Recover the model's exact standard deviation from this percentile.",
        "Rearrange x = μ + zσ and report σ.",
    ),
    "mu_from_cutoff": (
        "Find the mean μ.",
        "Use the supplied percentile cutoff and standard deviation to solve for μ.",
        "Recover the model's exact mean from this raw percentile.",
        "Rearrange x = μ + zσ and report μ.",
    ),
}


def _site():
    return f"{random.choice(LOCATIONS)} during the {random.choice(SETTINGS)}"


def _percent_text(value):
    return f"{num_txt(value)}%"


def _selected_table(bank, target):
    decoy = random.choice([entry for entry in bank if entry != target])
    rows = sorted([target, decoy])
    return "Selected z-scores: " + "; ".join(
        f"{ordinal(percentile)} percentile z = {num_txt(z)}"
        for percentile, z in rows)


def _lookup_step(percentile, z):
    return step("LOOKUP_SUPPLIED", f"z for {ordinal(percentile)} percentile",
                num_txt(z))


class InverseNormalGenerator(ProblemGenerator):
    """Generate exact inverse-normal calculations from supplied z entries."""

    VARIANTS = ("cutoff_above", "cutoff_below", "middle_interval",
                "sigma_from_cutoff", "mu_from_cutoff")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _forward(variant):
        percentile, z = random.choice(MAIN_BANK)
        mean = random.randint(30, 150)
        sigma = random.randint(2, 20)
        context, unit = random.choice(CONTEXTS)
        table = _selected_table(MAIN_BANK, (percentile, z))
        header = (f"At the {_site()}, normally distributed {context} have "
                  f"mean μ = {mean} {unit} and standard deviation σ = "
                  f"{sigma} {unit}. {table}.")
        steps = [step("NORM_SETUP", f"X ~ N({mean}, {sigma})",
                      variant.replace("_", " ")),
                 _lookup_step(percentile, z),
                 step("RAW_FORMULA", "x = μ + z·σ")]
        if variant == "cutoff_above":
            tail = 100 - percentile
            target = (f"Target: top {_percent_text(tail)}, whose boundary is "
                      f"the {ordinal(percentile)} percentile.")
            offset = z * sigma
            cutoff = mean + offset
            steps.extend([step("M", num_txt(z), sigma, num_txt(offset)),
                          step("A", mean, num_txt(offset), num_txt(cutoff)),
                          step("CHECK", "upper-tail cutoff",
                               ordinal(percentile), num_txt(cutoff))])
            answer = num_txt(cutoff)
        elif variant == "cutoff_below":
            tail = 100 - percentile
            target = (f"Target: bottom {_percent_text(tail)}; by symmetry use "
                      f"z = −{num_txt(z)} from the {ordinal(percentile)} "
                      f"upper entry.")
            signed_z = -z
            offset = signed_z * sigma
            cutoff = mean + offset
            steps.extend([step("REWRITE", f"lower z = −{num_txt(z)}"),
                          step("M", num_txt(signed_z), sigma, num_txt(offset)),
                          step("A", mean, num_txt(offset), num_txt(cutoff)),
                          step("CHECK", "lower-tail cutoff",
                               _percent_text(tail), num_txt(cutoff))])
            answer = num_txt(cutoff)
        else:
            middle = 2 * percentile - 100
            target = (f"Target: middle {_percent_text(middle)}, bounded by "
                      f"z = ±{num_txt(z)} from the {ordinal(percentile)} "
                      f"upper entry.")
            offset = z * sigma
            lower, upper = mean - offset, mean + offset
            steps.extend([step("M", num_txt(z), sigma, num_txt(offset)),
                          step("S", mean, num_txt(offset), num_txt(lower)),
                          step("A", mean, num_txt(offset), num_txt(upper)),
                          step("CHECK", "equal-tail interval",
                               f"±{num_txt(z)}", f"({num_txt(lower)}, {num_txt(upper)})")])
            answer = f"({num_txt(lower)}, {num_txt(upper)})"
        return f"{header}\n{target}", steps, answer

    @staticmethod
    def _sigma():
        percentile, z = random.choice(SIGMA_BANK)
        sigma = random.randint(2, 25)
        mean = random.randint(30, 150)
        cutoff = Fraction(mean) + z * sigma
        context, unit = random.choice(CONTEXTS)
        table = _selected_table(SIGMA_BANK, (percentile, z))
        prefix = (f"At the {_site()}, normally distributed {context} have "
                  f"mean μ = {mean} {unit}. Their {ordinal(percentile)} "
                  f"percentile cutoff is {num_txt(cutoff)} {unit}. {table}.")
        difference = cutoff - mean
        steps = [step("NORM_SETUP", "normal model with unknown σ",
                      f"x={num_txt(cutoff)}, μ={mean}"),
                 _lookup_step(percentile, z),
                 step("RAW_FORMULA", "σ = (x - μ)/z"),
                 step("S", num_txt(cutoff), mean, num_txt(difference)),
                 step("D", num_txt(difference), num_txt(z), sigma),
                 step("CHECK", "substitute x = μ + zσ",
                      num_txt(cutoff), sigma)]
        return prefix, steps, str(sigma)

    @staticmethod
    def _mean():
        percentile, z = random.choice(MAIN_BANK)
        mean = random.randint(30, 150)
        sigma = random.randint(2, 20)
        cutoff = Fraction(mean) + z * sigma
        context, unit = random.choice(CONTEXTS)
        table = _selected_table(MAIN_BANK, (percentile, z))
        prefix = (f"At the {_site()}, normally distributed {context} have "
                  f"standard deviation σ = {sigma} {unit}. Their "
                  f"{ordinal(percentile)} percentile cutoff is "
                  f"{num_txt(cutoff)} {unit}. {table}.")
        offset = z * sigma
        steps = [step("NORM_SETUP", "normal model with unknown μ",
                      f"x={num_txt(cutoff)}, σ={sigma}"),
                 _lookup_step(percentile, z),
                 step("RAW_FORMULA", "μ = x - z·σ"),
                 step("M", num_txt(z), sigma, num_txt(offset)),
                 step("S", num_txt(cutoff), num_txt(offset), mean),
                 step("CHECK", "substitute x = μ + zσ",
                      num_txt(cutoff), mean)]
        return prefix, steps, str(mean)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("cutoff_above", "cutoff_below", "middle_interval"):
            prefix, steps, answer = self._forward(variant)
        elif variant == "sigma_from_cutoff":
            prefix, steps, answer = self._sigma()
        else:
            prefix, steps, answer = self._mean()
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_inverse_normal_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

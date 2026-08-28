"""Distinguish populations, samples, statistics, and finite estimates.

Variants: ``identify``, ``parameter_vs_statistic``, ``scale_up``, and
``capture_recapture``. Op-codes: ``STAT_SETUP``, ``LABEL``, ``D``, ``M``,
``CHECK``, and ``Z``. Survey sample sizes have only 2-and-5 prime factors so
sample proportions terminate; population totals are multiples of sample size,
and capture-recapture values are built backward from an integer population.
Context, size, trait, setting, and four phrasing banks give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import num_txt


STATISTICS = True
SURVEYS = (
    ("households", "a town", "have solar panels"),
    ("students", "a school district", "ride the bus"),
    ("trees", "a managed forest", "show leaf damage"),
    ("voters", "a county", "support the proposal"),
    ("packages", "a warehouse shipment", "have damaged corners"),
    ("customers", "a store membership list", "use digital receipts"),
    ("employees", "a company", "work remotely"),
    ("books", "a library collection", "are checked out"),
)
ANIMALS = ("fish", "turtles", "rabbits", "deer", "frogs", "beetles",
           "butterflies", "crabs")
SETTINGS = ("amber study", "birch survey", "cedar trial", "delta project",
            "ember lab", "forest audit", "granite program", "harbor test",
            "indigo review", "jade pilot", "kestrel study", "lunar trial",
            "maple project", "nova lab", "onyx survey", "pearl audit")
SAMPLE_SIZES = (20, 25, 40, 50, 80, 100, 200, 250, 400, 500)
QUERIES = {
    "identify": (
        "Identify the population, the sample, and the observed sample statistic.",
        "Name the full group and sampled group, then report the sample proportion.",
        "Classify the population and sample and compute the statistic from the sample.",
        "State all three: population, sample, and exact sample statistic.",
    ),
    "parameter_vs_statistic": (
        "Identify the population parameter and the sample statistic.",
        "Which displayed proportion is a parameter, and which is a statistic?",
        "Classify the census proportion and sample proportion with their values.",
        "Distinguish the fixed population value from the sample-based value.",
    ),
    "scale_up": (
        "Use the sample proportion to estimate the population count.",
        "Scale the observed sample rate to the full population.",
        "Estimate how many members of the population have the stated trait.",
        "Compute the exact proportional population estimate.",
    ),
    "capture_recapture": (
        "Use M times C divided by R to estimate the population.",
        "Apply the capture-recapture ratio and report the estimated total.",
        "Estimate the animal population from the marked recaptures.",
        "Solve the proportional mark-recapture estimate exactly.",
    ),
}


def _survey_data(with_census=False):
    group, place, trait = random.choice(SURVEYS)
    sample = random.choice(SAMPLE_SIZES)
    population = sample * random.randint(8, 240)
    observed = random.randint(1, sample - 1)
    if with_census:
        census_count = random.randint(1, population - 1)
        return group, place, trait, population, sample, observed, census_count
    return group, place, trait, population, sample, observed


class PopulationSampleGenerator(ProblemGenerator):
    """Generate exact finite-population sampling and labeling exercises."""

    VARIANTS = ("identify", "parameter_vs_statistic", "scale_up",
                "capture_recapture")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _identify():
        group, place, trait, population, sample, observed = _survey_data()
        proportion = Fraction(observed, sample)
        problem = (f"At the {random.choice(SETTINGS)}, the population is all "
                   f"{population} {group} in {place}. A random sample contains "
                   f"{sample} {group}; {observed} {trait}.")
        steps = [
            step("STAT_SETUP", "population and sample identification",
                 f"{observed} of {sample}"),
            step("LABEL", "population", f"{population} {group}"),
            step("LABEL", "sample", f"{sample} {group}"),
            step("D", observed, sample, num_txt(proportion)),
            step("LABEL", "statistic", num_txt(proportion)),
            step("CHECK", "statistic comes from sample", "yes"),
        ]
        answer = (f"population: {population} {group}; sample: {sample} {group}; "
                  f"statistic: {num_txt(proportion)}")
        return problem, steps, answer

    @staticmethod
    def _parameter_statistic():
        (group, place, trait, population, sample, observed,
         census_count) = _survey_data(with_census=True)
        parameter = Fraction(census_count, population)
        statistic = Fraction(observed, sample)
        problem = (f"At the {random.choice(SETTINGS)}, a complete census of "
                   f"{population} {group} in {place} finds {census_count} that "
                   f"{trait}. A random sample of {sample} {group} finds "
                   f"{observed} that {trait}.")
        steps = [
            step("STAT_SETUP", "census versus sample proportion",
                 f"population N={population}, sample n={sample}"),
            step("D", census_count, population, num_txt(parameter)),
            step("LABEL", "parameter", num_txt(parameter)),
            step("D", observed, sample, num_txt(statistic)),
            step("LABEL", "statistic", num_txt(statistic)),
            step("CHECK", "parameter uses whole population", "yes"),
        ]
        answer = (f"parameter: {num_txt(parameter)}; "
                  f"statistic: {num_txt(statistic)}")
        return problem, steps, answer

    @staticmethod
    def _scale_up():
        group, place, trait, population, sample, observed = _survey_data()
        proportion = Fraction(observed, sample)
        estimate = proportion * population
        problem = (f"At the {random.choice(SETTINGS)}, {place} contains "
                   f"{population} {group}. In a random sample of {sample} "
                   f"{group}, {observed} {trait}.")
        steps = [
            step("STAT_SETUP", "scale sample proportion to population",
                 f"{observed} of {sample}"),
            step("D", observed, sample, num_txt(proportion)),
            step("M", num_txt(proportion), population, num_txt(estimate)),
            step("CHECK", "estimate within population",
                 f"0 < {num_txt(estimate)} < {population}"),
        ]
        answer = f"estimated count: {num_txt(estimate)} {group}"
        return problem, steps, answer

    @staticmethod
    def _capture_recapture():
        animal = random.choice(ANIMALS)
        marked = random.randint(12, 90)
        recaptured = random.randint(3, marked - 1)
        multiplier = random.randint(2, 30)
        second_capture = recaptured * multiplier
        population = marked * multiplier
        problem = (f"At the {random.choice(SETTINGS)}, a wildlife team marks "
                   f"M={marked} {animal} and releases them. Later it captures "
                   f"C={second_capture} {animal}; R={recaptured} of those are "
                   f"marked. Assume the marked fraction mixed uniformly.")
        product = marked * second_capture
        steps = [
            step("STAT_SETUP", "capture-recapture", "N=M·C/R"),
            step("LABEL", "M, C, R",
                 f"{marked}, {second_capture}, {recaptured}"),
            step("M", marked, second_capture, product),
            step("D", product, recaptured, population),
            step("CHECK", "marked fraction",
                 f"{marked}/{population} = {recaptured}/{second_capture}"),
        ]
        answer = f"estimated population: {population} {animal}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "identify":
            problem, steps, answer = self._identify()
        elif variant == "parameter_vs_statistic":
            problem, steps, answer = self._parameter_statistic()
        elif variant == "scale_up":
            problem, steps, answer = self._scale_up()
        else:
            problem, steps, answer = self._capture_recapture()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_population_sample_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

"""Compute and compare experimental relative frequencies.

Variants: ``relative_frequency``, ``from_sequence``, ``predict_count``, and
``compare_theoretical``. Op-codes: ``TALLY``, ``SUM``, ``REL_FREQ``, ``F``,
``M``, ``L``, ``C``, ``CMP``, ``CHECK``, and ``Z``. Random trials, counts,
contexts, and five phrasings per variant give an unbounded problem space.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
NAMES = ("Ari", "Bea", "Cleo", "Dara", "Eli", "Finn", "Gia", "Hugo",
         "Iris", "Jae", "Kira", "Luca", "Mara", "Nico")
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal")
QUERIES = {
    "relative_frequency": (
        "Find the experimental probability of the focus outcome.",
        "Use its relative frequency to estimate the event chance.",
        "Add the trials, then give the observed event proportion.",
        "Compute the exact experimental probability from the tally.",
        "Report the focus count divided by the total number of trials.",
    ),
    "from_sequence": (
        "Scan the sequence and find the experimental probability of the focus face.",
        "Tally the requested face directly from the displayed trials.",
        "Count the focus results, then divide by the sequence length.",
        "Use the raw trial sequence to compute the relative frequency.",
        "Determine the exact observed probability from the sequence.",
    ),
    "predict_count": (
        "Predict the event count using the theoretical probability.",
        "Multiply the number of future trials by the event chance.",
        "Find the expected long-run count for the stated event.",
        "Use the uniform model to predict how often the event occurs.",
        "Compute the theoretical event frequency over the planned trials.",
    ),
    "compare_theoretical": (
        "Compare the experimental and theoretical probabilities.",
        "Give both exact probabilities and state which is larger.",
        "Use a common denominator to compare observed and model chances.",
        "Determine whether the experimental chance is higher, lower, or equal.",
        "Report the relative frequency, the fair-model probability, and their comparison.",
    ),
}


class ExperimentalProbabilityGenerator(ProblemGenerator):
    """Generate exact relative-frequency and prediction exercises."""

    VARIANTS = ("relative_frequency", "from_sequence", "predict_count",
                "compare_theoretical")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _relative():
        labels = tuple(sorted(random.sample(COLORS, 3)))
        counts = tuple(random.randint(1, 60) for _ in labels)
        focus_index = random.randrange(3)
        total = sum(counts)
        value = Fraction(counts[focus_index], total)
        tally = "; ".join(f"{label}={count}"
                          for label, count in zip(labels, counts))
        problem = (f"{random.choice(NAMES)} records spinner tallies: {tally}. "
                   f"Focus outcome: {labels[focus_index]}.")
        steps = [step("TALLY", label, count)
                 for label, count in zip(labels, counts)]
        steps.append(step("SUM", " + ".join(map(str, counts)), total))
        steps.append(step("REL_FREQ", labels[focus_index],
                          f"{counts[focus_index]}/{total}", prob_txt(value)))
        return problem, steps, prob_txt(value)

    @staticmethod
    def _sequence():
        length = random.randint(10, 40)
        sequence = tuple(random.choice(("H", "T")) for _ in range(length))
        focus = random.choice(("H", "T"))
        count = sequence.count(focus)
        value = Fraction(count, length)
        problem = (f"Coin trial sequence: {' '.join(sequence)}. Focus face: "
                   f"{focus}.")
        steps = [step("TALLY", focus, count),
                 step("SUM", f"sequence length {length}", length),
                 step("REL_FREQ", focus, f"{count}/{length}", prob_txt(value))]
        return problem, steps, prob_txt(value)

    @staticmethod
    def _predict():
        sectors = random.randint(3, 16)
        favorable = random.randint(1, sectors - 1)
        multiplier = random.randint(5, 100)
        trials = sectors * multiplier
        predicted = favorable * multiplier
        verb = "belongs" if favorable == 1 else "belong"
        problem = (f"A uniform spinner has {sectors} equal sectors, of which "
                   f"{favorable} {verb} to event A. It will be spun {trials} "
                   "times.")
        value = Fraction(favorable, sectors)
        steps = [step("REL_FREQ", "theoretical A",
                      f"{favorable}/{sectors}", prob_txt(value)),
                 step("M", trials, prob_txt(value), predicted),
                 step("CHECK", f"{predicted}/{trials}", prob_txt(value))]
        return problem, steps, str(predicted)

    @staticmethod
    def _compare():
        sides = random.randint(4, 20)
        multiplier = random.randint(5, 200)
        trials = sides * multiplier
        target = random.randint(1, sides)
        relation = random.choice(("higher", "lower", "equal"))
        expected = multiplier
        if relation == "higher":
            observed = random.randint(expected + 1, min(trials, expected + sides * 3))
        elif relation == "lower":
            observed = random.randint(max(0, expected - sides * 3), expected - 1)
        else:
            observed = expected
        experimental = Fraction(observed, trials)
        theoretical = Fraction(1, sides)
        answer = (f"experimental {prob_txt(experimental)}; theoretical "
                  f"{prob_txt(theoretical)}; experimental is {relation}")
        problem = (f"A fair {sides}-sided die was rolled {trials} times; "
                   f"face {target} appeared {observed} times.")
        common = math.lcm(experimental.denominator, theoretical.denominator)
        exp_num = experimental.numerator * (common // experimental.denominator)
        theo_num = theoretical.numerator * (common // theoretical.denominator)
        steps = [step("TALLY", f"face {target}", observed),
                 step("REL_FREQ", "experimental",
                      f"{observed}/{trials}", prob_txt(experimental)),
                 step("REL_FREQ", "theoretical", f"1/{sides}",
                      prob_txt(theoretical)),
                 step("L", experimental.denominator,
                      theoretical.denominator, common),
                 step("C", prob_txt(experimental), common,
                      f"{exp_num}/{common}"),
                 step("C", prob_txt(theoretical), common,
                      f"{theo_num}/{common}"),
                 step("CMP", exp_num, theo_num, relation),
                 step("CHECK", answer)]
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "relative_frequency":
            prefix, steps, answer = self._relative()
        elif variant == "from_sequence":
            prefix, steps, answer = self._sequence()
        elif variant == "predict_count":
            prefix, steps, answer = self._predict()
        else:
            prefix, steps, answer = self._compare()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_experimental_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

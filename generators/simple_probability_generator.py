"""Single-event probability across concrete uniform experiments.

Variants: ``bare``, ``spinner``, ``bag``, ``numbered_cards``, ``die``,
``letter_tiles``, ``as_percent``, and ``as_decimal``. The original
``probability_simple`` operation is preserved for ``bare``. Op-codes:
``EVENT``, ``PROB_SETUP``, ``F``, ``FRAC_TO_DEC``, ``DEC_TO_PERCENT``,
``CHECK``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import dec, pct, prob_txt, roster


PROBABILITY = True
PLACES = (
    "classroom", "game club", "science lab", "school fair", "library",
    "museum activity", "math club", "community center", "study hall",
    "robotics lab", "design studio", "field station", "learning center",
    "survey office", "training center", "workshop",
)
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal")
WORDS = (
    "ALGEBRA", "ANGLE", "AVERAGE", "CHANCE", "CIRCLE", "COUNTING",
    "DECIMAL", "EQUATION", "EVENT", "EXPERIMENT", "FACTOR", "FORMULA",
    "FRACTION", "FUNCTION", "GEOMETRY", "GRAPH", "INTEGER", "LIKELIHOOD",
    "MATRIX", "MEASURE", "MEDIAN", "MULTIPLE", "NUMBER", "OUTCOME",
    "PATTERN", "PERCENT", "POLYGON", "PRIME", "PROBABILITY", "PRODUCT",
    "RANDOMNESS", "RATIO", "SAMPLE", "SEQUENCE", "SPINNER", "STATISTICS",
    "SUM", "TABLE", "TRIANGLE", "VARIABLE", "VECTOR", "VOLUME",
)
QUERIES = (
    "Compute the requested single-event probability.",
    "Count the event outcomes and give P(A) in the required form.",
    "Use favorable outcomes over total equally likely outcomes.",
    "Determine the exact chance of event A.",
    "Find P(A) from the displayed finite experiment.",
)


class SimpleProbabilityGenerator(ProblemGenerator):
    """Generate exact probability from favorable and total outcome counts."""

    VARIANTS = ("bare", "spinner", "bag", "numbered_cards", "die",
                "letter_tiles", "as_percent", "as_decimal")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _number_experiment(kind, output="fraction"):
        total = random.randint(6, 30)
        start = 1 if kind == "die" else random.randint(-10000, 10000)
        outcomes = list(range(start, start + total))
        event_kind = random.choice(("even", "multiple", "greater"))
        if event_kind == "even":
            event = [value for value in outcomes if value % 2 == 0]
            description = "an even number"
        elif event_kind == "multiple":
            divisor = random.randint(2, min(6, total - 1))
            event = [value for value in outcomes if value % divisor == 0]
            description = f"a multiple of {divisor}"
        else:
            cutoff = random.choice(outcomes[1:-1])
            event = [value for value in outcomes if value > cutoff]
            description = f"a number greater than {cutoff}"
        noun = {"spinner": "Equal spinner sectors",
                "numbered_cards": "Numbered cards",
                "die": f"A fair {total}-sided die has faces"}[kind]
        problem = (f"{noun}: S = {roster(outcomes)}. Event A is obtaining "
                   f"{description}; A = {roster(event)}. Report P(A) as a "
                   f"{output}.")
        return problem, event, outcomes

    def _build(self, variant):
        place = random.choice(PLACES)
        output = "fraction"
        if variant == "bare":
            total = random.randint(3, 200)
            favorable = random.randint(1, total - 1)
            outcome_word = "outcome" if favorable == 1 else "outcomes"
            problem = (f"At the {place}, a uniform event has {favorable} "
                       f"favorable {outcome_word} among {total} total outcomes. "
                       "Report P(A) as a reduced fraction.")
            event_text = f"{favorable} favorable outcomes"
        elif variant in ("spinner", "numbered_cards", "die"):
            problem, event, outcomes = self._number_experiment(variant)
            favorable, total = len(event), len(outcomes)
            event_text = roster(event)
            problem = f"At the {place}, {problem}"
        elif variant == "bag":
            labels = tuple(sorted(random.sample(COLORS, 3)))
            counts = tuple(random.randint(1, 40) for _ in labels)
            index = random.randrange(3)
            favorable, total = counts[index], sum(counts)
            count_text = "; ".join(
                f"{label}={count}" for label, count in zip(labels, counts))
            problem = (f"At the {place}, bag color counts are {count_text}. "
                       f"Event A is drawing {labels[index]}. Report P(A) as "
                       "a reduced fraction.")
            event_text = labels[index]
        elif variant == "letter_tiles":
            word = random.choice(WORDS)
            vowel_positions = [index for index, letter in enumerate(word, 1)
                               if letter in "AEIOU"]
            favorable, total = len(vowel_positions), len(word)
            problem = (f"At the {place}, letter tiles spell {word}. Event A "
                       f"is drawing a vowel, found at positions "
                       f"{roster(vowel_positions)}. Report P(A) as a reduced "
                       "fraction.")
            event_text = roster(vowel_positions)
        else:
            output = "percent" if variant == "as_percent" else "decimal"
            total = random.choice((8, 10, 16, 20, 25))
            favorable = random.randint(1, total - 1)
            start = random.randint(-10000, 10000)
            outcomes = list(range(start, start + total))
            problem = (f"At the {place}, numbered tickets form S = "
                       f"{roster(outcomes)}. Event A is drawing one of the "
                       f"first {favorable} tickets. Report P(A) as a "
                       f"{output}.")
            event_text = f"first {favorable} tickets"
        return (f"{problem} {random.choice(QUERIES)}", event_text,
                favorable, total, output)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        problem, event_text, favorable, total, output = self._build(variant)
        value = Fraction(favorable, total)
        fraction_text = prob_txt(value)
        answer = (pct(value) if output == "percent" else
                  dec(value) if output == "decimal" else fraction_text)
        steps = [step("EVENT", "A", event_text, favorable),
                 step("PROB_SETUP", favorable, total)]
        if value.denominator != total:
            steps.append(step("F", f"{favorable}/{total}", fraction_text))
        if output in ("decimal", "percent"):
            decimal_text = dec(value)
            steps.append(step("FRAC_TO_DEC", fraction_text, decimal_text))
            if output == "percent":
                steps.append(step("DEC_TO_PERCENT", decimal_text, answer))
        steps.append(step("CHECK", f"0 < {fraction_text} < 1",
                          "valid probability"))
        steps.append(step("Z", answer))
        operation = ("probability_simple" if variant == "bare" else
                     f"probability_simple_{variant}")
        return {"problem_id": jid(), "operation": operation,
                "problem": problem, "steps": steps, "final_answer": answer}

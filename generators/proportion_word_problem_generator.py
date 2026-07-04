import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import money

# A4: phrasing banks. Within each scenario every phrasing keeps the
# three numbers in the SAME textual order (documented per scenario)
# so the arithmetic mapping is unambiguous. `roles` gives that order
# as (numerator, denominator, query) positions into the three numbers
# as they appear in the sentence.
SCENARIOS = {
    # order in text: k1 (miles), k2 (hours), q (hours)
    "speed": {
        "roles": (0, 1, 2),
        "unit": "mi",
        "phrasings": [
            "If a car travels {k1} miles in {k2} hours, how far will "
            "it travel in {q} hours?",
            "A car covers {k1} miles in {k2} hours at a steady speed. "
            "How far does it go in {q} hours?",
        ],
    },
    # order in text: k1 (cups), k2 (servings), q (servings)
    "recipe": {
        "roles": (0, 1, 2),
        "unit": "cups",
        "phrasings": [
            "A recipe uses {k1} cups of flour for {k2} servings. How "
            "many cups are needed for {q} servings?",
            "You need {k1} cups of flour to make {k2} servings. How "
            "many cups are needed for {q} servings?",
        ],
    },
    # order in text: k2 (pounds), k1 (cost), q (pounds)
    "cost": {
        "roles": (1, 0, 2),
        "unit": "money",
        "phrasings": [
            "If {k2} pounds of apples cost ${k1}, how much do {q} "
            "pounds cost?",
            "{k2} pounds of apples cost ${k1}. What is the price of "
            "{q} pounds?",
        ],
    },
    # order in text: k2 (input), k1 (output), q (input)
    "ratio_table": {
        "roles": (1, 0, 2),
        "unit": "plain",
        "phrasings": [
            "In a ratio table, an input of {k2} maps to {k1}. What "
            "does an input of {q} map to?",
            "A ratio table pairs input {k2} with output {k1}. What "
            "output goes with input {q}?",
        ],
    },
}

DISTRACTORS = [
    "The trip started at {} AM.",
    "There are {} people in the car.",
    "The recipe book has {} pages.",
    "The store is {} blocks away.",
    "The table has {} rows already filled in.",
]


class ProportionWordProblemGenerator(ProblemGenerator):
    """
    Proportion word problems (rates like mi/hr, $/lb, cups/serving)
    solved by cross-multiplication. Supports several phrasings per
    scenario (A4) and an optional distractor quantity the scratchpad
    must first filter out (A6). Rates are integers by construction, so
    every answer is exact.

    With distractor=True the problem carries one irrelevant number and
    the first step (SELECT_RELEVANT) names the numbers that matter and
    the one to ignore.

    Op-codes used:
    - SELECT_RELEVANT: relevant data vs. the distractor to ignore
    - PROP_SETUP / M / EQ_SETUP / D (established)
    - Z: the requested quantity, with units
    """

    def __init__(self, distractor: bool = False):
        self.distractor = distractor
        if distractor:
            self.op_symbol = "distractor"

    def generate(self) -> dict:
        kind = random.choice(list(SCENARIOS))
        spec = SCENARIOS[kind]
        prompt = random.choice(spec["phrasings"])

        rate = random.randint(1, 10)
        k2 = random.randint(1, 5)      # denominator quantity
        k1 = rate * k2                 # numerator quantity
        q = random.randint(2, 12)      # query on the denominator side
        # x solves k1/k2 = x/q, i.e. x = k1·q/k2 = rate·q (integer).
        x = rate * q

        problem = prompt.format(k1=k1, k2=k2, q=q)
        steps = []
        if self.distractor:
            d_sentence = random.choice(DISTRACTORS)
            d_val = random.randint(2, 30)
            problem = f"{problem} {d_sentence.format(d_val)}"
            steps.append(step("SELECT_RELEVANT",
                              f"ratio {k1}/{k2}, query {q}",
                              f"ignore {d_val} (irrelevant)"))

        cross = k1 * q
        steps.append(step("PROP_SETUP", f"{k1}/{k2} = x/{q}"))
        steps.append(step("M", k1, q, cross))
        steps.append(step("EQ_SETUP", f"x = {cross}/{k2}"))
        steps.append(step("D", cross, k2, x))

        if spec["unit"] == "money":
            final_answer = money(Fraction(x))
        elif spec["unit"] == "plain":
            final_answer = str(x)
        else:
            final_answer = f"{x} {spec['unit']}"
        steps.append(step("Z", final_answer))

        operation = ("proportion_word_problem_distractor"
                     if self.distractor else "proportion_word_problem")
        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

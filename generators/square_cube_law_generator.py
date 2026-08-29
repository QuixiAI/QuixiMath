"""Area scales with the square, volume with the cube of a linear factor.

Variants: ``scale_model_area_volume``, ``map_area``, ``recipe_pan_scaling``,
``area_unit_conversion``, ``volume_unit_conversion``, ``how_many_small_cubes``,
``giant_or_miniature``. Five context frames and all four applied modifiers
are supported. Every scale factor is 2,5-smooth (or a small clean fraction)
so every squared/cubed conversion terminates exactly. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``SCALE_LAW``, ``CONV_FACTOR``, ``CMP``, ``M``, ``D``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, dec, estimate_first, exact, select_relevant_step
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("scale_model_area_volume", "map_area", "recipe_pan_scaling",
            "area_unit_conversion", "volume_unit_conversion",
            "how_many_small_cubes", "giant_or_miniature")
FRAMES = (
    "At {place}, {name} works out the following scale problem. {facts} {question}",
    "{question} A project for {name} at {place} states: {facts}",
    "For {name}'s project at {place}: {facts} {question}",
    "A note from {place}, checked by {name}, reads: {facts} {question}",
    "Consider the scale model {name} is building at {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("garden", "workshop", "business", "classroom")
               for setting in CONTEXTS[key].settings)

#: Scale denominators whose only prime factors are 2 and 5, so squaring or
#: cubing them and dividing by a smooth unit-conversion factor always
#: terminates exactly.
SMOOTH_SCALES = (2, 4, 5, 8, 10, 16, 20, 25, 40, 50)

MODEL_THINGS = (("model car", "windshield"), ("model plane", "wing"),
               ("model train", "roof panel"), ("dollhouse", "front door"),
               ("model ship", "deck"))

#: (unit1, unit2, linear factor to go from unit1 to unit2).
LINEAR_UNIT_PAIRS = (("m", "cm", 100), ("km", "m", 1000), ("cm", "mm", 10),
                    ("m", "mm", 1000))

CREATURE_SCALES = (Fraction(2), Fraction(3), Fraction(4), Fraction(5),
                   Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5))


def _places(fr):
    """Decimal places in the exact terminating render of ``fr`` (or a large
    number if it does not terminate — callers filter those out)."""
    try:
        s = dec(fr)
    except ValueError:
        return 99
    return len(s.split(".")[1]) if "." in s else 0


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class SquareCubeLawGenerator(ProblemGenerator):
    """Generate seven exact area/volume scaling models without naming the law."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _scale_model_area_volume():
        thing, part = random.choice(MODEL_THINGS)
        k = random.choice(SMOOTH_SCALES)
        area_real = random.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, 3, 4, 5, 6, 8, 10))
        area_cm2_real = area_real * 10000
        model_cm2 = area_cm2_real / (k * k)
        facts = (f"A {thing} is built at a scale of 1 : {k}. The real "
                 f"{thing}'s {part} has an area of {exact(area_real)} m².")
        question = f"What is the model {part}'s area in cm²?"
        model = "model area = (real area in cm²)/k²"
        steps = [step("SCALE_LAW", "area", f"k² = {k * k}"),
                step("CONV_FACTOR", "1 m²", "10,000 cm²"),
                step("M", exact(area_real), 10000, exact(area_cm2_real)),
                step("D", exact(area_cm2_real), k * k, exact(model_cm2))]
        answer = f"{exact(model_cm2)} cm²"
        used = [f"scale 1:{k}", f"real area {exact(area_real)} m²"]
        return facts, question, steps, answer, model_cm2, model, used, exact

    @staticmethod
    def _map_area():
        k = random.choice((100, 200, 250, 500, 1000, 2000, 2500, 5000))
        map_cm2 = random.choice((1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20))
        real_cm2 = map_cm2 * k * k
        real_m2 = Fraction(real_cm2, 10000)
        facts = (f"A map is drawn at a scale of 1 : {k} (1 cm on the map is "
                 f"{k} cm in reality). A park's area on the map measures "
                 f"{map_cm2} cm².")
        question = "What is the real area of the park in m²?"
        model = "real area = (map area × k²)/10,000"
        steps = [step("SCALE_LAW", "area", f"k² = {k * k}"),
                step("M", map_cm2, k * k, real_cm2),
                step("CONV_FACTOR", "10,000 cm²", "1 m²"),
                step("D", real_cm2, 10000, exact(real_m2))]
        answer = f"{exact(real_m2)} m²"
        used = [f"scale 1:{k}", f"map area {map_cm2} cm²"]
        return facts, question, steps, answer, real_m2, model, used, exact

    @staticmethod
    def _recipe_pan_scaling():
        batters = (Fraction(1), Fraction(2), Fraction(3), Fraction(4),
                  Fraction(5), Fraction(6), Fraction(3, 2), Fraction(5, 2))
        for _ in range(100):
            denom = random.choice((2, 5))
            num = denom + random.choice((1, 2, 3))
            ratio = Fraction(num, denom)
            factor = ratio ** 3
            batter = random.choice(batters)
            new_batter = batter * factor
            if _places(new_batter) <= 4:
                break
        else:
            raise AssertionError("no hand-friendly batter amount found")
        d1 = denom * random.randint(2, 4)
        d2 = int(d1 * ratio)
        facts = (f"A recipe scaled for a {d1}-inch round pan uses "
                 f"{exact(batter)} cups of batter. A larger, similarly "
                 f"shaped pan measures {d2} inches.")
        question = "How much batter does the larger pan need?"
        model = "new batter = old batter × (size ratio)³"
        steps = [step("SCALE_LAW", "volume", f"k³ = {exact(factor)}"),
                step("M", exact(batter), exact(factor), exact(new_batter))]
        answer = f"{exact(new_batter)} cups"
        used = [f"pans {d1} in, {d2} in", f"original {exact(batter)} cups"]
        return facts, question, steps, answer, new_batter, model, used, exact

    @staticmethod
    def _area_unit_conversion():
        unit1, unit2, factor = random.choice(LINEAR_UNIT_PAIRS)
        amount = random.choice((1, 2, 3, 4, 5, 6, 8, 10, Fraction(1, 2), Fraction(3, 2)))
        result = amount * factor * factor
        facts = f"Convert {exact(amount)} {unit1}² to {unit2}²."
        question = "What is the equivalent area?"
        model = "area in new units = area × (linear factor)²"
        steps = [step("CONV_FACTOR", f"1 {unit1}", f"{factor} {unit2}"),
                step("SCALE_LAW", "area", f"k² = {factor * factor}"),
                step("M", exact(amount), factor * factor, exact(result))]
        answer = f"{exact(result)} {unit2}²"
        used = [f"{exact(amount)} {unit1}²"]
        return facts, question, steps, answer, result, model, used, exact

    @staticmethod
    def _volume_unit_conversion():
        unit1, unit2, factor = random.choice(LINEAR_UNIT_PAIRS)
        amount = random.choice((1, 2, 3, 4, 5, Fraction(1, 2)))
        result = amount * factor ** 3
        facts = f"Convert {exact(amount)} {unit1}³ to {unit2}³."
        question = "What is the equivalent volume?"
        model = "volume in new units = volume × (linear factor)³"
        steps = [step("CONV_FACTOR", f"1 {unit1}", f"{factor} {unit2}"),
                step("SCALE_LAW", "volume", f"k³ = {factor ** 3}"),
                step("M", exact(amount), factor ** 3, exact(result))]
        answer = f"{exact(result)} {unit2}³"
        used = [f"{exact(amount)} {unit1}³"]
        return facts, question, steps, answer, result, model, used, exact

    @staticmethod
    def _how_many_small_cubes():
        k = random.randint(2, 6)
        facts = f"A cube's edge length is scaled by a factor of {k}."
        question = "How many of the original small cubes fit inside the new larger cube?"
        model = "count = k³"
        steps = [step("SCALE_LAW", "volume", f"k³ = {k ** 3}")]
        answer = f"{k ** 3} cubes"
        used = [f"edge factor {k}"]
        return facts, question, steps, answer, Fraction(k ** 3), model, used, str

    @staticmethod
    def _giant_or_miniature():
        k = random.choice(CREATURE_SCALES)
        area_factor, volume_factor = k * k, k * k * k
        facts = (f"A creature's linear size scales by a factor of {exact(k)}, "
                 "with every body proportion unchanged.")
        question = "By what factor do its cross-sectional area (strength) and its volume (weight) change?"
        model = "area ×k²; volume ×k³"
        steps = [step("SCALE_LAW", "area", f"k² = {exact(area_factor)}"),
                step("SCALE_LAW", "volume", f"k³ = {exact(volume_factor)}"),
                step("CMP", exact(area_factor), exact(volume_factor), "vs")]
        answer = (f"area ×{exact(area_factor)}; volume ×{exact(volume_factor)}; "
                 "volume changes by the larger factor")
        used = [f"scale factor {exact(k)}"]
        return facts, question, steps, answer, volume_factor, model, used, exact

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in range(301, 601) if n not in occupied])
            problem = f"A nearby shelf holds {extra} unrelated parts. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} unrelated parts"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale of the converted quantity",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "area/volume scale relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_square_cube_law_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}

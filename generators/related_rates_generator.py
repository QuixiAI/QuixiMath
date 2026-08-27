import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid

LADDERS = [(5, 12, 13), (12, 5, 13), (3, 4, 5), (4, 3, 5),
           (6, 8, 10), (8, 6, 10), (8, 15, 17), (15, 8, 17)]

UNIT_PAIRS = [
    ("cm", "s"), ("m", "s"), ("ft", "s"), ("in", "s"),
    ("cm", "min"), ("m", "min"), ("ft", "min"), ("in", "min"),
]

PLACES = [
    "design studio", "school laboratory", "robotics lab", "waterworks",
    "science museum", "testing center", "engineering workshop",
    "research station", "training facility", "field laboratory",
    "fabrication shop", "university lab", "prototype bay", "survey site",
    "technical college", "observatory workshop", "quality-control lab",
    "modeling classroom", "materials lab", "instrument room",
]

CONTEXTS = [
    "At the {place}, a measurement is being recorded.",
    "During a test at the {place}, a measurement is being recorded.",
    "A report from the {place} gives the following measurements.",
    "In a model used by the {place}, the following rates apply.",
]


def context_text():
    return random.choice(CONTEXTS).format(place=random.choice(PLACES))


class RelatedRatesGenerator(ProblemGenerator):
    """
    Related rates on the four classic setups, each with the relation
    stated, differentiated through d/dt, values substituted, and the
    target rate isolated - all arithmetic exact (π stays symbolic).

    Variants:
    - circle: dA/dt = 2πr·dr/dt
    - ladder: x² + y² = L², the missing side found first
    - cube:   dV/dt = 3s²·ds/dt
    - cone:   V = πh³/12 (radius = h/2), solve for dh/dt

    Op-codes used:
    - RATE_SETUP: the scenario and the goal (given, goal)
    - REWRITE / E / S / M / D / EVAL (established)
    - IMPLICIT_DIFF: the relation differentiated in t (established)
    - SUBST / EQ_OP_BOTH / FRAC_REDUCE (established)
    - Z: the rate with units
    """

    VARIANTS = ["circle", "ladder", "cube", "cone"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        length_unit, time_unit = random.choice(UNIT_PAIRS)
        context = context_text()

        if variant == "circle":
            r0 = random.randint(2, 40)
            k = random.randint(1, 20)
            val = 2 * r0 * k
            steps = [
                step("RATE_SETUP",
                     f"circle: dr/dt = {k} {length_unit}/{time_unit}; "
                     f"r = {r0} {length_unit}",
                     "dA/dt"),
                step("REWRITE", "A = πr^2"),
                step("IMPLICIT_DIFF", "d/dt of A = πr^2",
                     "dA/dt = 2πr·dr/dt"),
                step("SUBST", "(r, dr/dt)", f"({r0}, {k})",
                     f"dA/dt = 2π({r0})({k})"),
                step("M", 2, r0, 2 * r0),
                step("M", 2 * r0, k, val),
            ]
            answer = (f"dA/dt = {val}π {length_unit}²/{time_unit}")
            problem = (f"{context} The radius of a circle grows at {k} "
                       f"{length_unit}/{time_unit}. How "
                       f"fast is the area increasing when the radius "
                       f"is {r0} {length_unit}? Give an exact answer.")
        elif variant == "ladder":
            x0, y0, L = random.choice(LADDERS)
            scale = random.randint(1, 8)
            x0, y0, L = x0 * scale, y0 * scale, L * scale
            k = random.randint(1, 12)
            rate = Fraction(-x0 * k, y0)
            steps = [
                step("RATE_SETUP",
                     f"{L} {length_unit} ladder; the base slides away at "
                     f"{k} {length_unit}/{time_unit}; base is {x0} "
                     f"{length_unit} from the wall", "dy/dt"),
                step("REWRITE", f"x^2 + y^2 = {L * L}"),
                step("E", x0, 2, x0 * x0),
                step("S", L * L, x0 * x0, y0 * y0),
                step("E", y0, 2, y0 * y0),
                step("EVAL", "y", y0),
                step("IMPLICIT_DIFF", f"d/dt of x^2 + y^2 = {L * L}",
                     "2x·dx/dt + 2y·dy/dt = 0"),
                step("SUBST", "(x, y, dx/dt)",
                     f"({x0}, {y0}, {k})",
                     f"2({x0})({k}) + 2({y0})·dy/dt = 0"),
                step("M", 2 * x0, k, 2 * x0 * k),
                step("M", 2, y0, 2 * y0),
                step("EQ_OP_BOTH", "subtract", 2 * x0 * k,
                     f"{2 * y0}·dy/dt", -2 * x0 * k),
                step("EQ_OP_BOTH", "divide", 2 * y0, "dy/dt",
                     rate),
                step("FRAC_REDUCE", f"{-2 * x0 * k}/{2 * y0}", rate),
            ]
            answer = f"dy/dt = {rate} {length_unit}/{time_unit}"
            problem = (f"{context} A {L} {length_unit} ladder leans against "
                       f"a wall. The base slides away from the wall at {k} "
                       f"{length_unit}/{time_unit}. How fast "
                       f"is the top sliding down when the base is {x0} "
                       f"{length_unit} from the wall?")
        elif variant == "cube":
            s0 = random.randint(2, 25)
            k = random.randint(1, 15)
            val = 3 * s0 * s0 * k
            steps = [
                step("RATE_SETUP",
                     f"cube: ds/dt = {k} {length_unit}/{time_unit}; "
                     f"s = {s0} {length_unit}", "dV/dt"),
                step("REWRITE", "V = s^3"),
                step("IMPLICIT_DIFF", "d/dt of V = s^3",
                     "dV/dt = 3s^2·ds/dt"),
                step("SUBST", "(s, ds/dt)", f"({s0}, {k})",
                     f"dV/dt = 3({s0})^2({k})"),
                step("E", s0, 2, s0 * s0),
                step("M", 3, s0 * s0, 3 * s0 * s0),
                step("M", 3 * s0 * s0, k, val),
            ]
            answer = f"dV/dt = {val} {length_unit}³/{time_unit}"
            problem = (f"{context} Each edge of a cube grows at {k} "
                       f"{length_unit}/{time_unit}. How "
                       f"fast is the volume increasing when the edge "
                       f"is {s0} {length_unit}?")
        else:
            h0 = random.randint(2, 30)
            k = random.randint(2, 20)
            rate = Fraction(4 * k, h0 * h0)
            rtxt = (f"{rate}/π" if rate.denominator == 1
                    else f"{rate.numerator}/({rate.denominator}π)")
            steps = [
                step("RATE_SETUP",
                     f"conical tank, radius = height/2; water in at "
                     f"dV/dt = {k} {length_unit}³/{time_unit}; depth "
                     f"h = {h0} {length_unit}", "dh/dt"),
                step("REWRITE",
                     "V = (1/3)πr^2·h with r = h/2, so V = πh^3/12"),
                step("IMPLICIT_DIFF", "d/dt of V = πh^3/12",
                     "dV/dt = (πh^2/4)·dh/dt"),
                step("SUBST", "(h, dV/dt)", f"({h0}, {k})",
                     f"{k} = (π({h0})^2/4)·dh/dt"),
                step("E", h0, 2, h0 * h0),
                step("EQ_OP_BOTH", "multiply", 4, f"{4 * k}",
                     f"π·{h0 * h0}·dh/dt"),
                step("EQ_OP_BOTH", "divide", f"{h0 * h0}π", "dh/dt",
                     rtxt),
                step("FRAC_REDUCE", f"{4 * k}/{h0 * h0}", rate),
            ]
            answer = f"dh/dt = {rtxt} {length_unit}/{time_unit}"
            problem = (f"{context} Water pours into a conical tank (radius "
                       f"equals half the depth) at {k} {length_unit}³/"
                       f"{time_unit}. How fast is the depth rising when the "
                       f"water is {h0} {length_unit} deep? "
                       f"Give an exact answer.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"related_rates_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

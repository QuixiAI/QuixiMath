import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid

LADDERS = [(5, 12, 13), (12, 5, 13), (3, 4, 5), (4, 3, 5),
           (6, 8, 10), (8, 6, 10), (8, 15, 17), (15, 8, 17)]


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

        if variant == "circle":
            r0 = random.randint(2, 12)
            k = random.randint(1, 5)
            val = 2 * r0 * k
            steps = [
                step("RATE_SETUP",
                     f"circle: dr/dt = {k} cm/s; r = {r0} cm",
                     "dA/dt"),
                step("REWRITE", "A = πr^2"),
                step("IMPLICIT_DIFF", "d/dt of A = πr^2",
                     "dA/dt = 2πr·dr/dt"),
                step("SUBST", "(r, dr/dt)", f"({r0}, {k})",
                     f"dA/dt = 2π({r0})({k})"),
                step("M", 2, r0, 2 * r0),
                step("M", 2 * r0, k, val),
            ]
            answer = f"dA/dt = {val}π cm²/s"
            problem = (f"The radius of a circle grows at {k} cm/s. How "
                       f"fast is the area increasing when the radius "
                       f"is {r0} cm? Give an exact answer.")
        elif variant == "ladder":
            x0, y0, L = random.choice(LADDERS)
            k = random.randint(1, 4)
            rate = Fraction(-x0 * k, y0)
            steps = [
                step("RATE_SETUP",
                     f"{L} ft ladder; the base slides away at {k} ft/s; "
                     f"base is {x0} ft from the wall", "dy/dt"),
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
            answer = f"dy/dt = {rate} ft/s"
            problem = (f"A {L} ft ladder leans against a wall. The base "
                       f"slides away from the wall at {k} ft/s. How fast "
                       f"is the top sliding down when the base is {x0} "
                       f"ft from the wall?")
        elif variant == "cube":
            s0 = random.randint(2, 10)
            k = random.randint(1, 4)
            val = 3 * s0 * s0 * k
            steps = [
                step("RATE_SETUP",
                     f"cube: ds/dt = {k} cm/s; s = {s0} cm", "dV/dt"),
                step("REWRITE", "V = s^3"),
                step("IMPLICIT_DIFF", "d/dt of V = s^3",
                     "dV/dt = 3s^2·ds/dt"),
                step("SUBST", "(s, ds/dt)", f"({s0}, {k})",
                     f"dV/dt = 3({s0})^2({k})"),
                step("E", s0, 2, s0 * s0),
                step("M", 3, s0 * s0, 3 * s0 * s0),
                step("M", 3 * s0 * s0, k, val),
            ]
            answer = f"dV/dt = {val} cm³/s"
            problem = (f"Each edge of a cube grows at {k} cm/s. How "
                       f"fast is the volume increasing when the edge "
                       f"is {s0} cm?")
        else:
            h0 = random.choice([2, 4, 6, 8, 10])
            k = random.randint(2, 9)
            rate = Fraction(4 * k, h0 * h0)
            rtxt = (f"{rate}/π" if rate.denominator == 1
                    else f"{rate.numerator}/({rate.denominator}π)")
            steps = [
                step("RATE_SETUP",
                     f"conical tank, radius = height/2; water in at "
                     f"dV/dt = {k} m³/min; depth h = {h0} m", "dh/dt"),
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
            answer = f"dh/dt = {rtxt} m/min"
            problem = (f"Water pours into a conical tank (radius equals "
                       f"half the depth) at {k} m³/min. How fast is the "
                       f"depth rising when the water is {h0} m deep? "
                       f"Give an exact answer.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"related_rates_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

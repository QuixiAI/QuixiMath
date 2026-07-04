import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class CrossSectionGenerator(ProblemGenerator):
    """
    Collider luminosity and cross-section arithmetic.

    Integrated luminosity in fb^-1 times cross section in fb gives expected
    events. Picobarns are converted with the supplied 1 pb = 1000 fb factor.

    Op-codes used:
    - COLLIDER_SETUP: givens and target
    - CONV_FACTOR: supplied unit conversion
    - M / D (established/shared): exact arithmetic
    - UNIT_ATTACH: attach event/fb/fb^-1 units to the answer
    - Z: requested collider quantity
    """

    VARIANTS = ["events_fb", "events_pb", "cross_section", "luminosity"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "events_fb":
            problem, steps, answer = self._generate_events_fb()
        elif variant == "events_pb":
            problem, steps, answer = self._generate_events_pb()
        elif variant == "cross_section":
            problem, steps, answer = self._generate_cross_section()
        else:
            problem, steps, answer = self._generate_luminosity()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"cross_section_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_events_fb(self):
        luminosity = random.randint(1, 30)
        sigma = random.randint(1, 40)
        events = luminosity * sigma
        answer = f"N = {events} events"
        steps = [
            step("COLLIDER_SETUP", "events_fb",
                 f"L={luminosity} fb^-1", f"sigma={sigma} fb"),
            step("M", luminosity, sigma, events),
            step("UNIT_ATTACH", events, "events", answer),
        ]
        problem = (
            f"At a collider with integrated luminosity L={luminosity} fb^-1 "
            f"and cross section sigma={sigma} fb, compute expected events "
            "N=L*sigma."
        )
        return problem, steps, answer

    def _generate_events_pb(self):
        luminosity = random.randint(1, 30)
        sigma_pb = random.randint(1, 20)
        sigma_fb = sigma_pb * 1000
        events = luminosity * sigma_fb
        answer = f"N = {events} events"
        steps = [
            step("COLLIDER_SETUP", "events_pb",
                 f"L={luminosity} fb^-1", f"sigma={sigma_pb} pb"),
            step("CONV_FACTOR", "1 pb", "1000 fb"),
            step("M", sigma_pb, 1000, sigma_fb),
            step("M", luminosity, sigma_fb, events),
            step("UNIT_ATTACH", events, "events", answer),
        ]
        problem = (
            f"At a collider with integrated luminosity L={luminosity} fb^-1 "
            f"and cross section sigma={sigma_pb} pb, use 1 pb=1000 fb "
            "to compute expected events."
        )
        return problem, steps, answer

    def _generate_cross_section(self):
        events = random.randint(1, 300)
        luminosity = random.randint(1, 30)
        sigma = Fraction(events, luminosity)
        answer = f"sigma = {fraction_text(sigma)} fb"
        steps = [
            step("COLLIDER_SETUP", "cross_section",
                 f"N={events} events", f"L={luminosity} fb^-1"),
            step("D", events, luminosity, fraction_text(sigma)),
            step("UNIT_ATTACH", fraction_text(sigma), "fb", answer),
        ]
        problem = (
            f"Given N={events} events and integrated luminosity "
            f"L={luminosity} fb^-1, compute cross section sigma=N/L in fb."
        )
        return problem, steps, answer

    def _generate_luminosity(self):
        events = random.randint(1, 300)
        sigma = random.randint(1, 40)
        luminosity = Fraction(events, sigma)
        answer = f"L = {fraction_text(luminosity)} fb^-1"
        steps = [
            step("COLLIDER_SETUP", "luminosity",
                 f"N={events} events", f"sigma={sigma} fb"),
            step("D", events, sigma, fraction_text(luminosity)),
            step("UNIT_ATTACH", fraction_text(luminosity), "fb^-1", answer),
        ]
        problem = (
            f"Given target N={events} events and cross section sigma={sigma} "
            "fb, compute required integrated luminosity L=N/sigma in fb^-1."
        )
        return problem, steps, answer

import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.arc_sector_generator import pi_txt


class SolidRevolutionGenerator(ProblemGenerator):
    """
    Volumes with exact π answers: disks, washers, shells, and square
    cross-sections, each with its formula stated, the integrand
    squared/expanded, and the FTC evaluation in exact fractions.

    Variants:
    - disk:   y = kx on [0, a] about the x-axis -> πk²a³/3
    - washer: between y = kx and y = kx² on [0, 1] -> 2k²π/15
    - shell:  y = x(a - x) about the y-axis -> πa³/3
    - cross_section: squares on the base under y = c - x -> c³/3

    Op-codes used:
    - VOLUME_SETUP: the region and the method
    - VOL_FORMULA: the method formula (established)
    - REWRITE / DIST / INTEG_RULE / ANTIDERIV / EVAL / S
      (established, exact fractions)
    - Z: exact volume ('64π/3' or a plain fraction)
    """

    VARIANTS = ["disk", "washer", "shell", "cross_section"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "disk":
            k = random.randint(1, 3)
            a = random.randint(1, 4)
            body = "x" if k == 1 else f"{k}x"
            vol = Fraction(k * k * a ** 3, 3)
            F = lambda x: Fraction(k * k * x ** 3, 3)
            steps = [
                step("VOLUME_SETUP",
                     f"region under y = {body} on [0, {a}], rotated "
                     f"about the x-axis", "disk method"),
                step("VOL_FORMULA", "V = π ∫ [f(x)]^2 dx"),
                step("REWRITE", f"[{body}]^2 = {k * k}x^2"
                     if k > 1 else "[x]^2 = x^2"),
                step("INTEG_RULE", "power rule",
                     "∫ x^2 dx = x^3/3"),
                step("ANTIDERIV", f"{k * k}x^2" if k > 1 else "x^2",
                     f"({Fraction(k * k, 3)})x^3"),
                step("EVAL", f"F({a})", F(a)),
                step("EVAL", "F(0)", 0),
                step("S", F(a), 0, vol),
            ]
            answer = pi_txt(vol)
            problem = (f"Find the volume when the region under "
                       f"y = {body} on [0, {a}] is rotated about the "
                       f"x-axis. Give an exact answer in terms of π.")
        elif variant == "washer":
            k = random.randint(1, 4)
            body_o = "x" if k == 1 else f"{k}x"
            body_i = "x^2" if k == 1 else f"{k}x^2"
            vol = Fraction(2 * k * k, 15)
            steps = [
                step("VOLUME_SETUP",
                     f"region between y = {body_o} (outer) and "
                     f"y = {body_i} (inner) on [0, 1], about the "
                     f"x-axis", "washer method"),
                step("VOL_FORMULA",
                     "V = π ∫ (R^2 - r^2) dx"),
                step("REWRITE",
                     f"R^2 - r^2 = {k * k}x^2 - {k * k}x^4"
                     if k > 1 else "R^2 - r^2 = x^2 - x^4"),
                step("ANTIDERIV", f"{k * k}x^2 - {k * k}x^4",
                     f"F(x) = ({Fraction(k * k, 3)})x^3 - "
                     f"({Fraction(k * k, 5)})x^5"),
                step("EVAL", "F(1)",
                     Fraction(k * k, 3) - Fraction(k * k, 5)),
                step("EVAL", "F(0)", 0),
                step("S", Fraction(k * k, 3) - Fraction(k * k, 5), 0,
                     vol),
            ]
            answer = pi_txt(vol)
            problem = (f"Find the volume when the region between "
                       f"y = {body_o} and y = {body_i} on [0, 1] is "
                       f"rotated about the x-axis. Give an exact "
                       f"answer in terms of π.")
        elif variant == "shell":
            a = random.randint(2, 6)
            steps = [
                step("VOLUME_SETUP",
                     f"region under y = x({a} - x) on [0, {a}], "
                     f"rotated about the y-axis", "shell method"),
                step("VOL_FORMULA", "V = 2π ∫ x·f(x) dx"),
                step("DIST", "x", f"x({a} - x)",
                     f"{a}x^2 - x^3"),
                step("ANTIDERIV", f"{a}x^2 - x^3",
                     f"F(x) = ({Fraction(a, 3)})x^3 - (1/4)x^4"),
                step("EVAL", f"F({a})",
                     Fraction(a ** 4, 3) - Fraction(a ** 4, 4)),
                step("EVAL", "F(0)", 0),
                step("S", Fraction(a ** 4, 3) - Fraction(a ** 4, 4),
                     0, Fraction(a ** 4, 12)),
                step("M", 2, Fraction(a ** 4, 12),
                     Fraction(a ** 4, 6)),
            ]
            vol = Fraction(a ** 4, 6)
            answer = pi_txt(vol)
            problem = (f"Use the shell method to find the volume when "
                       f"the region under y = x({a} - x) on [0, {a}] "
                       f"is rotated about the y-axis. Give an exact "
                       f"answer in terms of π.")
        else:
            c = random.randint(2, 6)
            vol = Fraction(c ** 3, 3)
            steps = [
                step("VOLUME_SETUP",
                     f"base: region under y = {c} - x on [0, {c}]; "
                     f"cross-sections perpendicular to the x-axis are "
                     f"squares", "cross-section method"),
                step("VOL_FORMULA", "V = ∫ [side(x)]^2 dx"),
                step("REWRITE",
                     f"[({c} - x)]^2 = x^2 - {2 * c}x + {c * c}"),
                step("ANTIDERIV", f"x^2 - {2 * c}x + {c * c}",
                     f"F(x) = (1/3)x^3 - {c}x^2 + {c * c}x"),
                step("EVAL", f"F({c})", vol),
                step("EVAL", "F(0)", 0),
                step("S", vol, 0, vol),
            ]
            answer = str(vol)
            problem = (f"The base of a solid is the region under "
                       f"y = {c} - x on [0, {c}]. Cross-sections "
                       f"perpendicular to the x-axis are squares. "
                       f"Find the volume.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"volume_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

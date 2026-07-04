import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class InterferenceGenerator(ProblemGenerator):
    """
    Exact wave-interference arithmetic for slits, gratings, and thin films.

    Variants:
    - double_slit: y=m*lambda*L/d.
    - diffraction_grating: sin(theta)=m*lambda/d.
    - thin_film: t=m*lambda/(2*n).

    Op-codes used:
    - INTERFERENCE_SETUP / INTERFERENCE_FORMULA
    - M / D (established/shared): exact products and divisions
    - Z: fringe position, sine of diffraction angle, or film thickness
    """

    VARIANTS = ["double_slit", "diffraction_grating", "thin_film"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "double_slit":
            problem, steps, answer = self._generate_double_slit()
        elif variant == "diffraction_grating":
            problem, steps, answer = self._generate_grating()
        else:
            problem, steps, answer = self._generate_thin_film()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"interference_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_double_slit(self):
        order = random.randint(1, 8)
        wavelength = random.randint(1, 20)
        screen_distance = random.randint(1, 20)
        slit_spacing = random.randint(1, 30)
        first_product = order * wavelength
        numerator = first_product * screen_distance
        fringe = Fraction(numerator, slit_spacing)
        steps = [
            step("INTERFERENCE_SETUP", "double_slit",
                 f"m={order}, lambda={wavelength}",
                 f"L={screen_distance}, d={slit_spacing}"),
            step("INTERFERENCE_FORMULA", "y=m*lambda*L/d"),
            step("M", order, wavelength, first_product),
            step("M", first_product, screen_distance, numerator),
            step("D", numerator, slit_spacing, fraction_text(fringe)),
        ]
        answer = f"y={fraction_text(fringe)} m"
        problem = (
            f"A double-slit setup has order m={order}, wavelength "
            f"lambda={wavelength} m, screen distance L={screen_distance} m, "
            f"and slit spacing d={slit_spacing} m. Find fringe position y."
        )
        return problem, steps, answer

    def _generate_grating(self):
        order = random.randint(1, 5)
        wavelength = random.randint(1, 20)
        spacing = random.randint(order * wavelength, order * wavelength + 60)
        numerator = order * wavelength
        sine = Fraction(numerator, spacing)
        steps = [
            step("INTERFERENCE_SETUP", "diffraction_grating",
                 f"m={order}, lambda={wavelength}", f"d={spacing}"),
            step("INTERFERENCE_FORMULA", "d*sin(theta)=m*lambda"),
            step("M", order, wavelength, numerator),
            step("D", numerator, spacing, fraction_text(sine)),
        ]
        answer = f"sin(theta)={fraction_text(sine)}"
        problem = (
            f"A diffraction grating has spacing d={spacing} m. For order "
            f"m={order} and wavelength lambda={wavelength} m, find "
            "sin(theta)."
        )
        return problem, steps, answer

    def _generate_thin_film(self):
        order = random.randint(1, 8)
        wavelength = random.randint(1, 40)
        refractive_index = Fraction(random.randint(2, 8), random.randint(1, 5))
        numerator = order * wavelength
        denominator = 2 * refractive_index
        thickness = numerator / denominator
        steps = [
            step("INTERFERENCE_SETUP", "thin_film",
                 f"m={order}, lambda={wavelength}",
                 f"n={fraction_text(refractive_index)}"),
            step("INTERFERENCE_FORMULA", "2*n*t=m*lambda"),
            step("M", order, wavelength, numerator),
            step("M", 2, fraction_text(refractive_index),
                 fraction_text(denominator)),
            step("D", numerator, fraction_text(denominator),
                 fraction_text(thickness)),
        ]
        answer = f"t={fraction_text(thickness)} m"
        problem = (
            f"A thin film has refractive index n={fraction_text(refractive_index)}. "
            f"For order m={order} and wavelength lambda={wavelength} m, "
            "use 2*n*t=m*lambda to find thickness t."
        )
        return problem, steps, answer

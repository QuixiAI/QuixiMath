import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class StandingWaveGenerator(ProblemGenerator):
    """
    Exact standing-wave harmonic arithmetic for strings and pipes.

    Variants:
    - string_harmonic: fixed-fixed string, lambda=2L/n and f=v/lambda.
    - open_pipe: open-open pipe, lambda=2L/n and f=v/lambda.
    - closed_pipe: closed-open pipe, h=2k-1, lambda=4L/h, f=v/lambda.

    Op-codes used:
    - STANDING_SETUP / STANDING_BOUNDARY / STANDING_FORMULA
    - M / S / D (established/shared): exact harmonic arithmetic
    - Z: wavelength and frequency
    """

    VARIANTS = ["string_harmonic", "open_pipe", "closed_pipe"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "string_harmonic":
            problem, steps, answer = self._generate_string()
        elif variant == "open_pipe":
            problem, steps, answer = self._generate_open_pipe()
        else:
            problem, steps, answer = self._generate_closed_pipe()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"standing_wave_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _fixed_fixed_flow(self, setup_variant, boundary_text, length, speed,
                          harmonic):
        double_length = 2 * length
        wavelength = Fraction(double_length, harmonic)
        frequency = Fraction(speed, wavelength)
        steps = [
            step("STANDING_SETUP", setup_variant, f"n={harmonic}",
                 f"L={length}, v={speed}"),
            step("STANDING_BOUNDARY", boundary_text),
            step("STANDING_FORMULA", "lambda=2L/n, f=v/lambda"),
            step("M", 2, length, double_length),
            step("D", double_length, harmonic, fraction_text(wavelength)),
            step("D", speed, fraction_text(wavelength),
                 fraction_text(frequency)),
        ]
        answer = (
            f"lambda={fraction_text(wavelength)} m; "
            f"f={fraction_text(frequency)} Hz"
        )
        return steps, answer

    def _generate_string(self):
        length = random.randint(1, 24)
        speed = random.randint(20, 240)
        harmonic = random.randint(1, 10)
        steps, answer = self._fixed_fixed_flow(
            "string_harmonic",
            "fixed-fixed string allows n=1,2,3,...",
            length,
            speed,
            harmonic,
        )
        problem = (
            f"A string fixed at both ends has length L={length} m and wave "
            f"speed v={speed} m/s. Find wavelength lambda and frequency f "
            f"for harmonic n={harmonic}."
        )
        return problem, steps, answer

    def _generate_open_pipe(self):
        length = random.randint(1, 24)
        speed = random.randint(20, 240)
        harmonic = random.randint(1, 10)
        steps, answer = self._fixed_fixed_flow(
            "open_pipe",
            "open-open pipe allows n=1,2,3,...",
            length,
            speed,
            harmonic,
        )
        problem = (
            f"An open-open pipe has length L={length} m and sound speed "
            f"v={speed} m/s. Find wavelength lambda and frequency f for "
            f"harmonic n={harmonic}."
        )
        return problem, steps, answer

    def _generate_closed_pipe(self):
        length = random.randint(1, 24)
        speed = random.randint(20, 240)
        mode = random.randint(1, 8)
        doubled_mode = 2 * mode
        harmonic = doubled_mode - 1
        four_length = 4 * length
        wavelength = Fraction(four_length, harmonic)
        frequency = Fraction(speed, wavelength)
        steps = [
            step("STANDING_SETUP", "closed_pipe", f"k={mode}",
                 f"L={length}, v={speed}"),
            step("STANDING_BOUNDARY", "closed-open pipe uses h=2k-1"),
            step("STANDING_FORMULA", "lambda=4L/h, f=v/lambda"),
            step("M", 2, mode, doubled_mode),
            step("S", doubled_mode, 1, harmonic),
            step("M", 4, length, four_length),
            step("D", four_length, harmonic, fraction_text(wavelength)),
            step("D", speed, fraction_text(wavelength),
                 fraction_text(frequency)),
        ]
        answer = (
            f"h={harmonic}; lambda={fraction_text(wavelength)} m; "
            f"f={fraction_text(frequency)} Hz"
        )
        problem = (
            f"A closed-open pipe has length L={length} m and sound speed "
            f"v={speed} m/s. For mode k={mode}, find the odd harmonic h, "
            "wavelength lambda, and frequency f."
        )
        return problem, steps, answer

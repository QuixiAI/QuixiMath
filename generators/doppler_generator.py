import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class DopplerGenerator(ProblemGenerator):
    """
    Acoustic and relativistic Doppler shifts with exact arithmetic.

    Variants:
    - acoustic_toward: f_obs=f*(v+v_observer)/(v-v_source).
    - relativistic_approach: f_obs=f*sqrt((1+beta)/(1-beta)).

    Op-codes used:
    - DOPPLER_SETUP / DOPPLER_FORMULA
    - A / S / M / D / E / ROOT (established/shared): exact arithmetic
    - Z: observed frequency
    """

    VARIANTS = ["acoustic_toward", "relativistic_approach"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "acoustic_toward":
            problem, steps, answer = self._generate_acoustic()
        else:
            problem, steps, answer = self._generate_relativistic()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"doppler_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_acoustic(self):
        sound_speed = random.randint(20, 80)
        observer_speed = random.randint(1, sound_speed // 3)
        source_speed = random.randint(1, sound_speed // 3)
        frequency = random.randint(100, 1000)
        top = sound_speed + observer_speed
        bottom = sound_speed - source_speed
        numerator = frequency * top
        observed = Fraction(numerator, bottom)
        steps = [
            step("DOPPLER_SETUP", "acoustic_toward",
                 f"f={frequency}, v={sound_speed}",
                 f"v_observer={observer_speed}, v_source={source_speed}"),
            step("DOPPLER_FORMULA", "f_obs=f*(v+v_observer)/(v-v_source)"),
            step("A", sound_speed, observer_speed, top),
            step("S", sound_speed, source_speed, bottom),
            step("M", frequency, top, numerator),
            step("D", numerator, bottom, fraction_text(observed)),
        ]
        answer = f"f_obs={fraction_text(observed)} Hz"
        problem = (
            f"A sound source emits f={frequency} Hz. Sound speed is "
            f"v={sound_speed} m/s, the observer moves toward the source at "
            f"v_observer={observer_speed} m/s, and the source moves toward "
            f"the observer at v_source={source_speed} m/s. Find f_obs."
        )
        return problem, steps, answer

    def _generate_relativistic(self):
        factor = random.randint(2, 10)
        factor_sq = factor ** 2
        beta_num = factor_sq - 1
        beta_den = factor_sq + 1
        beta = Fraction(beta_num, beta_den)
        frequency = random.randint(100, 1000)
        one_plus = 1 + beta
        one_minus = 1 - beta
        ratio = one_plus / one_minus
        observed = frequency * factor
        steps = [
            step("DOPPLER_SETUP", "relativistic_approach",
                 f"f={frequency}", f"beta={fraction_text(beta)}"),
            step("DOPPLER_FORMULA",
                 "f_obs=f*sqrt((1+beta)/(1-beta))"),
            step("E", factor, 2, factor_sq),
            step("S", factor_sq, 1, beta_num),
            step("A", factor_sq, 1, beta_den),
            step("A", 1, fraction_text(beta), fraction_text(one_plus)),
            step("S", 1, fraction_text(beta), fraction_text(one_minus)),
            step("D", fraction_text(one_plus), fraction_text(one_minus),
                 fraction_text(ratio)),
            step("ROOT", f"sqrt({fraction_text(ratio)})", factor),
            step("M", frequency, factor, observed),
        ]
        answer = f"f_obs={observed} Hz"
        problem = (
            f"A light source approaches with beta={fraction_text(beta)} and "
            f"emits f={frequency} Hz. Use the relativistic Doppler formula "
            "to find f_obs."
        )
        return problem, steps, answer

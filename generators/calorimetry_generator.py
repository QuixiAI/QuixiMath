import random

from base_generator import ProblemGenerator
from helpers import step, jid


class CalorimetryGenerator(ProblemGenerator):
    """
    Calorimetry with sensible heat and phase changes.

    Variants:
    - temperature_change: q = m c DeltaT
    - phase_change: q = m L
    - ice_to_water: warm ice, melt, then warm water

    Op-codes used:
    - CAL_SETUP: material constants and temperatures
    - CAL_FORMULA: calorimetry relation
    - A / S / M (established/shared): exact heat arithmetic
    - Z: heat required or released
    """

    VARIANTS = ["temperature_change", "phase_change", "ice_to_water"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "temperature_change":
            problem, steps, answer = self._generate_temperature_change()
        elif variant == "phase_change":
            problem, steps, answer = self._generate_phase_change()
        else:
            problem, steps, answer = self._generate_ice_to_water()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"calorimetry_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_temperature_change(self):
        mass = random.randint(1, 20)
        specific_heat = random.randint(1, 10)
        t1 = random.randint(-20, 80)
        delta_t = random.choice([value for value in range(-30, 31)
                                 if value != 0])
        t2 = t1 + delta_t
        mc = mass * specific_heat
        heat = mc * delta_t
        steps = [
            step("CAL_SETUP", "temperature_change",
                 f"m={mass}, c={specific_heat}", f"T1={t1}, T2={t2}"),
            step("CAL_FORMULA", "q=m*c*(T2-T1)"),
            step("S", t2, t1, delta_t),
            step("M", mass, specific_heat, mc),
            step("M", mc, delta_t, heat),
        ]
        answer = f"q={heat} J"
        problem = (
            f"A sample has mass m={mass} kg and specific heat c={specific_heat} "
            f"J/(kg*K). Its temperature changes from T1={t1} C to T2={t2} C. "
            "Find heat q."
        )
        return problem, steps, answer

    def _generate_phase_change(self):
        mass = random.randint(1, 30)
        latent_heat = random.randint(10, 400)
        heat = mass * latent_heat
        steps = [
            step("CAL_SETUP", "phase_change", f"m={mass}",
                 f"L={latent_heat}"),
            step("CAL_FORMULA", "q=m*L"),
            step("M", mass, latent_heat, heat),
        ]
        answer = f"q={heat} J"
        problem = (
            f"A substance of mass m={mass} kg undergoes a phase change with "
            f"latent heat L={latent_heat} J/kg. Find heat q."
        )
        return problem, steps, answer

    def _generate_ice_to_water(self):
        mass = random.randint(1, 20)
        c_ice = random.randint(1, 5)
        latent_heat = random.randint(10, 200)
        c_water = random.randint(1, 8)
        start_temp = -random.randint(1, 30)
        final_temp = random.randint(1, 40)
        warm_ice_delta = 0 - start_temp
        warm_ice_mc = mass * c_ice
        warm_ice_heat = warm_ice_mc * warm_ice_delta
        melt_heat = mass * latent_heat
        warm_water_mc = mass * c_water
        warm_water_heat = warm_water_mc * final_temp
        partial = warm_ice_heat + melt_heat
        total = partial + warm_water_heat
        steps = [
            step("CAL_SETUP", "ice_to_water",
                 f"m={mass}, Ti={start_temp}, Tf={final_temp}",
                 f"c_ice={c_ice}, Lf={latent_heat}, c_water={c_water}"),
            step("CAL_FORMULA", "warm ice: q1=m*c_ice*(0-Ti)"),
            step("S", 0, start_temp, warm_ice_delta),
            step("M", mass, c_ice, warm_ice_mc),
            step("M", warm_ice_mc, warm_ice_delta, warm_ice_heat),
            step("CAL_FORMULA", "melt ice: q2=m*Lf"),
            step("M", mass, latent_heat, melt_heat),
            step("CAL_FORMULA", "warm water: q3=m*c_water*Tf"),
            step("M", mass, c_water, warm_water_mc),
            step("M", warm_water_mc, final_temp, warm_water_heat),
            step("A", warm_ice_heat, melt_heat, partial),
            step("A", partial, warm_water_heat, total),
        ]
        answer = f"q_total={total} J"
        problem = (
            f"Ice of mass m={mass} kg starts at Ti={start_temp} C and ends "
            f"as liquid water at Tf={final_temp} C. Use c_ice={c_ice}, "
            f"Lf={latent_heat}, and c_water={c_water}. Find total heat."
        )
        return problem, steps, answer

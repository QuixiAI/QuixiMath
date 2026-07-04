import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class HeatEngineGenerator(ProblemGenerator):
    """
    Heat engines, Carnot limits, and refrigerator coefficients of performance.

    Variants:
    - engine_efficiency: W = Qh - Qc, eta = W/Qh
    - carnot_efficiency: eta_C = 1 - Tc/Th
    - refrigerator_cop: COP_R = Qc/W

    Op-codes used:
    - ENGINE_SETUP: heat-flow givens
    - ENGINE_FORMULA: efficiency or COP relation
    - A / S / D (established/shared): exact arithmetic
    - Z: efficiency, work, or COP
    """

    VARIANTS = ["engine_efficiency", "carnot_efficiency", "refrigerator_cop"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "engine_efficiency":
            problem, steps, answer = self._generate_engine_efficiency()
        elif variant == "carnot_efficiency":
            problem, steps, answer = self._generate_carnot_efficiency()
        else:
            problem, steps, answer = self._generate_refrigerator_cop()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"heat_engine_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_engine_efficiency(self):
        q_hot = random.randint(20, 300)
        q_cold = random.randint(1, q_hot - 1)
        work = q_hot - q_cold
        efficiency = Fraction(work, q_hot)
        steps = [
            step("ENGINE_SETUP", "engine_efficiency",
                 f"Qh={q_hot}", f"Qc={q_cold}"),
            step("ENGINE_FORMULA", "W=Qh-Qc"),
            step("S", q_hot, q_cold, work),
            step("ENGINE_FORMULA", "eta=W/Qh"),
            step("D", work, q_hot, fraction_text(efficiency)),
        ]
        answer = f"W={work} J; efficiency={fraction_text(efficiency)}"
        problem = (
            f"A heat engine absorbs Qh={q_hot} J and rejects Qc={q_cold} J. "
            "Find work output and efficiency."
        )
        return problem, steps, answer

    def _generate_carnot_efficiency(self):
        t_cold = random.randint(100, 500)
        t_hot = random.randint(t_cold + 1, t_cold + 600)
        temp_gap = t_hot - t_cold
        efficiency = Fraction(temp_gap, t_hot)
        steps = [
            step("ENGINE_SETUP", "carnot_efficiency",
                 f"Th={t_hot}", f"Tc={t_cold}"),
            step("ENGINE_FORMULA", "eta_C=1-Tc/Th=(Th-Tc)/Th"),
            step("S", t_hot, t_cold, temp_gap),
            step("D", temp_gap, t_hot, fraction_text(efficiency)),
        ]
        answer = f"Carnot efficiency={fraction_text(efficiency)}"
        problem = (
            f"A reversible engine operates between Th={t_hot} K and "
            f"Tc={t_cold} K. Find the Carnot efficiency."
        )
        return problem, steps, answer

    def _generate_refrigerator_cop(self):
        q_cold = random.randint(10, 200)
        work = random.randint(1, 80)
        q_hot = q_cold + work
        cop = Fraction(q_cold, work)
        steps = [
            step("ENGINE_SETUP", "refrigerator_cop",
                 f"Qc={q_cold}", f"W={work}"),
            step("ENGINE_FORMULA", "Qh=Qc+W"),
            step("A", q_cold, work, q_hot),
            step("ENGINE_FORMULA", "COP_R=Qc/W"),
            step("D", q_cold, work, fraction_text(cop)),
        ]
        answer = f"Qh={q_hot} J; COP_R={fraction_text(cop)}"
        problem = (
            f"A refrigerator removes Qc={q_cold} J from the cold space "
            f"using work W={work} J. Find heat rejected Qh and COP_R."
        )
        return problem, steps, answer

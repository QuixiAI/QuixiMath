import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


GAS_TO_MASS_TEMPLATES = [
    dict(equation="N2 + 3 H2 -> 2 NH3", gas="H2", target="NH3",
         target_mm=17),
    dict(equation="2 CO + O2 -> 2 CO2", gas="CO", target="CO2",
         target_mm=44),
    dict(equation="2 H2 + O2 -> 2 H2O", gas="H2", target="H2O",
         target_mm=18),
]

MASS_TO_GAS_TEMPLATES = [
    dict(equation="CaCO3 -> CaO + CO2", given="CaCO3", gas="CO2",
         given_mm=100),
    dict(equation="2 H2O2 -> 2 H2O + O2", given="H2O2", gas="O2",
         given_mm=34),
    dict(equation="2 KClO3 -> 2 KCl + 3 O2", given="KClO3", gas="O2",
         given_mm=122),
]


def fraction_text(value):
    return str(Fraction(value))


def parse_term(term):
    pieces = term.split(" ", 1)
    if len(pieces) == 2 and pieces[0].isdigit():
        return int(pieces[0]), pieces[1]
    return 1, term


def parse_equation(equation):
    left_text, right_text = equation.split(" -> ")
    left = [parse_term(term) for term in left_text.split(" + ")]
    right = [parse_term(term) for term in right_text.split(" + ")]
    return left, right


def coefficient_for(equation, formula):
    left, right = parse_equation(equation)
    for coefficient, species in left + right:
        if species == formula:
            return coefficient
    raise ValueError(f"{formula} not found in {equation}")


class GasStoichiometryGenerator(ProblemGenerator):
    """
    Stoichiometry chained through PV=nRT with R supplied as 1.

    Variants:
    - gas_to_mass: gas reactant PV/T -> product moles -> product mass.
    - mass_to_gas_volume: reactant mass -> gas moles -> V=nT/P.
    - mass_to_gas_pressure: reactant mass -> gas moles -> P=nT/V.

    Op-codes used:
    - GAS_STOICH_SETUP / GAS_FORMULA
    - STOICH_RATIO / MOLAR_MASS
    - M / D (established/shared): exact gas-law and stoichiometric arithmetic
    - Z: requested mass, gas volume, or gas pressure
    """

    VARIANTS = [
        "gas_to_mass",
        "mass_to_gas_volume",
        "mass_to_gas_pressure",
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "gas_to_mass":
            problem, steps, answer = self._generate_gas_to_mass()
        elif variant == "mass_to_gas_volume":
            problem, steps, answer = self._generate_mass_to_volume()
        else:
            problem, steps, answer = self._generate_mass_to_pressure()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"gas_stoichiometry_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_gas_to_mass(self):
        template = random.choice(GAS_TO_MASS_TEMPLATES)
        pressure = random.randint(1, 12)
        volume = random.randint(1, 30)
        temperature = random.randint(1, 30)
        pv = pressure * volume
        gas_moles = Fraction(pv, temperature)
        gas_coef = coefficient_for(template["equation"], template["gas"])
        target_coef = coefficient_for(template["equation"], template["target"])
        ratio = Fraction(target_coef, gas_coef)
        target_moles = gas_moles * ratio
        target_mass = target_moles * template["target_mm"]
        steps = [
            step("GAS_STOICH_SETUP", "gas_to_mass", template["equation"],
                 f"gas={template['gas']}, target={template['target']}"),
            step("GAS_FORMULA", "PV=nRT so n=PV/T with R=1"),
            step("M", pressure, volume, pv),
            step("D", pv, temperature, fraction_text(gas_moles)),
            step("STOICH_RATIO", f"{template['gas']}->{template['target']}",
                 f"{target_coef}/{gas_coef}={fraction_text(ratio)}"),
            step("M", fraction_text(gas_moles), fraction_text(ratio),
                 fraction_text(target_moles)),
            step("MOLAR_MASS", template["target"],
                 f"{template['target_mm']} g/mol"),
            step("M", fraction_text(target_moles), template["target_mm"],
                 fraction_text(target_mass)),
        ]
        answer = f"mass {template['target']}={fraction_text(target_mass)} g"
        problem = (
            f"Given balanced equation {template['equation']}, "
            f"{template['gas']} gas has P={pressure} atm, V={volume} L, "
            f"T={temperature} K with R=1. How many grams of "
            f"{template['target']} form? Molar mass {template['target']}="
            f"{template['target_mm']} g/mol."
        )
        return problem, steps, answer

    def _mass_to_gas_core(self, template):
        given_mass = template["given_mm"] * random.randint(1, 12)
        given_moles = Fraction(given_mass, template["given_mm"])
        given_coef = coefficient_for(template["equation"], template["given"])
        gas_coef = coefficient_for(template["equation"], template["gas"])
        ratio = Fraction(gas_coef, given_coef)
        gas_moles = given_moles * ratio
        common_steps = [
            step("MOLAR_MASS", template["given"],
                 f"{template['given_mm']} g/mol"),
            step("D", given_mass, template["given_mm"],
                 fraction_text(given_moles)),
            step("STOICH_RATIO", f"{template['given']}->{template['gas']}",
                 f"{gas_coef}/{given_coef}={fraction_text(ratio)}"),
            step("M", fraction_text(given_moles), fraction_text(ratio),
                 fraction_text(gas_moles)),
        ]
        return given_mass, gas_moles, common_steps

    def _generate_mass_to_volume(self):
        template = random.choice(MASS_TO_GAS_TEMPLATES)
        pressure = random.randint(1, 12)
        temperature = random.randint(1, 30)
        given_mass, gas_moles, common_steps = self._mass_to_gas_core(template)
        nt = gas_moles * temperature
        gas_volume = nt / pressure
        steps = [
            step("GAS_STOICH_SETUP", "mass_to_gas_volume",
                 template["equation"],
                 f"given={given_mass} g {template['given']}, gas={template['gas']}"),
        ]
        steps.extend(common_steps)
        steps.extend([
            step("GAS_FORMULA", "PV=nRT so V=nT/P with R=1"),
            step("M", fraction_text(gas_moles), temperature,
                 fraction_text(nt)),
            step("D", fraction_text(nt), pressure, fraction_text(gas_volume)),
        ])
        answer = f"V {template['gas']}={fraction_text(gas_volume)} L"
        problem = (
            f"Given balanced equation {template['equation']}, {given_mass} g "
            f"{template['given']} reacts. At P={pressure} atm and "
            f"T={temperature} K with R=1, what volume V of {template['gas']} "
            f"gas forms? Molar mass {template['given']}={template['given_mm']} "
            "g/mol."
        )
        return problem, steps, answer

    def _generate_mass_to_pressure(self):
        template = random.choice(MASS_TO_GAS_TEMPLATES)
        vessel_volume = random.randint(1, 30)
        temperature = random.randint(1, 30)
        given_mass, gas_moles, common_steps = self._mass_to_gas_core(template)
        nt = gas_moles * temperature
        pressure = nt / vessel_volume
        steps = [
            step("GAS_STOICH_SETUP", "mass_to_gas_pressure",
                 template["equation"],
                 f"given={given_mass} g {template['given']}, gas={template['gas']}"),
        ]
        steps.extend(common_steps)
        steps.extend([
            step("GAS_FORMULA", "PV=nRT so P=nT/V with R=1"),
            step("M", fraction_text(gas_moles), temperature,
                 fraction_text(nt)),
            step("D", fraction_text(nt), vessel_volume,
                 fraction_text(pressure)),
        ])
        answer = f"P {template['gas']}={fraction_text(pressure)} atm"
        problem = (
            f"Given balanced equation {template['equation']}, {given_mass} g "
            f"{template['given']} reacts and {template['gas']} is collected "
            f"in a V={vessel_volume} L vessel at T={temperature} K with R=1. "
            f"Find pressure P of {template['gas']}. Molar mass "
            f"{template['given']}={template['given_mm']} g/mol."
        )
        return problem, steps, answer

import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


ATOMIC_MASS = {
    "H": 1,
    "C": 12,
    "N": 14,
    "O": 16,
    "Mg": 24,
    "Al": 27,
    "K": 39,
    "Ca": 40,
    "Fe": 56,
}


BALANCE_TEMPLATES = [
    dict(left=["CH4", "O2"], right=["CO2", "H2O"],
         left_coeffs=[1, 2], right_coeffs=[1, 2]),
    dict(left=["Fe", "O2"], right=["Fe2O3"],
         left_coeffs=[4, 3], right_coeffs=[2]),
    dict(left=["C3H8", "O2"], right=["CO2", "H2O"],
         left_coeffs=[1, 5], right_coeffs=[3, 4]),
    dict(left=["N2", "H2"], right=["NH3"],
         left_coeffs=[1, 3], right_coeffs=[2]),
    dict(left=["Al", "O2"], right=["Al2O3"],
         left_coeffs=[4, 3], right_coeffs=[2]),
]

MASS_TEMPLATES = [
    dict(left=["H2", "O2"], right=["H2O"],
         left_coeffs=[2, 1], right_coeffs=[2],
         given="H2", target="H2O"),
    dict(left=["N2", "H2"], right=["NH3"],
         left_coeffs=[1, 3], right_coeffs=[2],
         given="H2", target="NH3"),
    dict(left=["CO", "O2"], right=["CO2"],
         left_coeffs=[2, 1], right_coeffs=[2],
         given="CO", target="CO2"),
    dict(left=["Mg", "O2"], right=["MgO"],
         left_coeffs=[2, 1], right_coeffs=[2],
         given="Mg", target="MgO"),
]

VOLUME_TEMPLATES = [
    dict(left=["CaCO3"], right=["CaO", "CO2"],
         left_coeffs=[1], right_coeffs=[1, 1],
         given="CaCO3", target="CO2"),
    dict(left=["KClO3"], right=["KCl", "O2"],
         left_coeffs=[2], right_coeffs=[2, 3],
         given="KClO3", target="O2",
         molar_masses={"KClO3": 122}),
    dict(left=["H2O2"], right=["H2O", "O2"],
         left_coeffs=[2], right_coeffs=[2, 1],
         given="H2O2", target="O2"),
]

LIMITING_TEMPLATES = [
    dict(left=["H2", "O2"], right=["H2O"],
         left_coeffs=[2, 1], right_coeffs=[2],
         target="H2O"),
    dict(left=["N2", "H2"], right=["NH3"],
         left_coeffs=[1, 3], right_coeffs=[2],
         target="NH3"),
    dict(left=["CO", "O2"], right=["CO2"],
         left_coeffs=[2, 1], right_coeffs=[2],
         target="CO2"),
]


def fraction_text(value):
    return str(Fraction(value))


def formula_counts(formula):
    counts = {}
    i = 0
    while i < len(formula):
        element = formula[i]
        i += 1
        if i < len(formula) and formula[i].islower():
            element += formula[i]
            i += 1
        digits = []
        while i < len(formula) and formula[i].isdigit():
            digits.append(formula[i])
            i += 1
        count = int("".join(digits)) if digits else 1
        counts[element] = counts.get(element, 0) + count
    return counts


def molar_mass(formula, overrides=None):
    overrides = overrides or {}
    if formula in overrides:
        return overrides[formula]
    return sum(ATOMIC_MASS[element] * count
               for element, count in formula_counts(formula).items())


def species_text(coefficient, formula):
    return formula if coefficient == 1 else f"{coefficient} {formula}"


def equation_text(template, balanced=True):
    if balanced:
        left = [
            species_text(coef, formula)
            for coef, formula in zip(template["left_coeffs"], template["left"])
        ]
        right = [
            species_text(coef, formula)
            for coef, formula in zip(template["right_coeffs"], template["right"])
        ]
    else:
        left = template["left"]
        right = template["right"]
    return f"{' + '.join(left)} -> {' + '.join(right)}"


def coefficient_for(template, formula):
    if formula in template["left"]:
        idx = template["left"].index(formula)
        return template["left_coeffs"][idx]
    idx = template["right"].index(formula)
    return template["right_coeffs"][idx]


def element_order(left, right):
    order = []
    for formula in left + right:
        for element in formula_counts(formula):
            if element not in order:
                order.append(element)
    return order


def side_counts(formulas, coefficients):
    totals = {}
    for formula, coefficient in zip(formulas, coefficients):
        for element, count in formula_counts(formula).items():
            totals[element] = totals.get(element, 0) + coefficient * count
    return totals


class StoichiometryGenerator(ProblemGenerator):
    """
    Balanced-equation and stoichiometric conversion practice.

    Variants:
    - balance_equation: balance a skeleton reaction and verify atom counts.
    - mass_to_mass: grams reactant -> moles -> moles product -> grams product.
    - mass_to_volume: grams reactant -> moles gas -> liters using supplied
      molar volume.
    - limiting_reagent: compare product capacities from two reactants.

    Op-codes used:
    - STOICH_SETUP / BALANCE_COEFFS / ATOM_CHECK / BALANCED_EQ
    - MOLAR_MASS / STOICH_RATIO / MOLAR_VOLUME / LIMIT_CHECK
    - LIMITING_REAGENT
    - M / D (established/shared): exact stoichiometric arithmetic
    - Z: balanced equation, mass, volume, or limiting reagent result
    """

    VARIANTS = [
        "balance_equation",
        "mass_to_mass",
        "mass_to_volume",
        "limiting_reagent",
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "balance_equation":
            problem, steps, answer = self._generate_balance()
        elif variant == "mass_to_mass":
            problem, steps, answer = self._generate_mass_to_mass()
        elif variant == "mass_to_volume":
            problem, steps, answer = self._generate_mass_to_volume()
        else:
            problem, steps, answer = self._generate_limiting_reagent()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"stoichiometry_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_balance(self):
        template = random.choice(BALANCE_TEMPLATES)
        skeleton = equation_text(template, balanced=False)
        balanced = equation_text(template, balanced=True)
        left_totals = side_counts(template["left"], template["left_coeffs"])
        right_totals = side_counts(template["right"], template["right_coeffs"])
        steps = [
            step("STOICH_SETUP", "balance_equation", skeleton),
            step("BALANCE_COEFFS",
                 f"reactants={','.join(str(c) for c in template['left_coeffs'])}",
                 f"products={','.join(str(c) for c in template['right_coeffs'])}"),
        ]
        for element in element_order(template["left"], template["right"]):
            steps.append(step("ATOM_CHECK", element,
                              f"left={left_totals[element]}",
                              f"right={right_totals[element]}"))
        steps.append(step("BALANCED_EQ", balanced))
        problem = f"Balance the equation: {skeleton}."
        return problem, steps, balanced

    def _generate_mass_to_mass(self):
        template = random.choice(MASS_TEMPLATES)
        equation = equation_text(template, balanced=True)
        given = template["given"]
        target = template["target"]
        given_mm = molar_mass(given, template.get("molar_masses"))
        target_mm = molar_mass(target, template.get("molar_masses"))
        given_mass = given_mm * random.randint(1, 12)
        given_coef = coefficient_for(template, given)
        target_coef = coefficient_for(template, target)
        ratio = Fraction(target_coef, given_coef)
        moles_given = Fraction(given_mass, given_mm)
        moles_target = moles_given * ratio
        target_mass = moles_target * target_mm
        steps = [
            step("STOICH_SETUP", "mass_to_mass", equation,
                 f"given={given_mass} g {given}, target={target}"),
            step("MOLAR_MASS", given, f"{given_mm} g/mol"),
            step("MOLAR_MASS", target, f"{target_mm} g/mol"),
            step("STOICH_RATIO", f"{given}->{target}",
                 f"{target_coef}/{given_coef}={fraction_text(ratio)}"),
            step("D", given_mass, given_mm, fraction_text(moles_given)),
            step("M", fraction_text(moles_given), fraction_text(ratio),
                 fraction_text(moles_target)),
            step("M", fraction_text(moles_target), target_mm,
                 fraction_text(target_mass)),
        ]
        answer = f"mass {target}={fraction_text(target_mass)} g"
        problem = (
            f"Given balanced equation {equation}, how many grams of {target} "
            f"form from {given_mass} g {given}? Molar masses: "
            f"{given}={given_mm} g/mol, {target}={target_mm} g/mol."
        )
        return problem, steps, answer

    def _generate_mass_to_volume(self):
        template = random.choice(VOLUME_TEMPLATES)
        equation = equation_text(template, balanced=True)
        given = template["given"]
        target = template["target"]
        given_mm = molar_mass(given, template.get("molar_masses"))
        given_mass = given_mm * random.randint(1, 10)
        molar_volume = 24
        given_coef = coefficient_for(template, given)
        target_coef = coefficient_for(template, target)
        ratio = Fraction(target_coef, given_coef)
        moles_given = Fraction(given_mass, given_mm)
        moles_target = moles_given * ratio
        volume = moles_target * molar_volume
        steps = [
            step("STOICH_SETUP", "mass_to_volume", equation,
                 f"given={given_mass} g {given}, target={target}"),
            step("MOLAR_MASS", given, f"{given_mm} g/mol"),
            step("STOICH_RATIO", f"{given}->{target}",
                 f"{target_coef}/{given_coef}={fraction_text(ratio)}"),
            step("D", given_mass, given_mm, fraction_text(moles_given)),
            step("M", fraction_text(moles_given), fraction_text(ratio),
                 fraction_text(moles_target)),
            step("MOLAR_VOLUME", "1 mol gas", f"{molar_volume} L"),
            step("M", fraction_text(moles_target), molar_volume,
                 fraction_text(volume)),
        ]
        answer = f"V {target}={fraction_text(volume)} L"
        problem = (
            f"Given balanced equation {equation}, how many liters of {target} "
            f"gas form from {given_mass} g {given}? Use molar mass "
            f"{given}={given_mm} g/mol and molar gas volume {molar_volume} "
            "L/mol."
        )
        return problem, steps, answer

    def _generate_limiting_reagent(self):
        template = random.choice(LIMITING_TEMPLATES)
        equation = equation_text(template, balanced=True)
        r1, r2 = template["left"]
        target = template["target"]
        target_coef = coefficient_for(template, target)
        r1_coef = coefficient_for(template, r1)
        r2_coef = coefficient_for(template, r2)
        ratio1 = Fraction(target_coef, r1_coef)
        ratio2 = Fraction(target_coef, r2_coef)
        while True:
            amount1 = random.randint(1, 12)
            amount2 = random.randint(1, 12)
            product1 = amount1 * ratio1
            product2 = amount2 * ratio2
            if product1 != product2:
                break
        if product1 < product2:
            limiting = r1
            product = product1
        else:
            limiting = r2
            product = product2
        steps = [
            step("STOICH_SETUP", "limiting_reagent", equation,
                 f"given={r1}={amount1} mol, {r2}={amount2} mol"),
            step("STOICH_RATIO", f"{r1}->{target}",
                 f"{target_coef}/{r1_coef}={fraction_text(ratio1)}"),
            step("M", amount1, fraction_text(ratio1),
                 fraction_text(product1)),
            step("STOICH_RATIO", f"{r2}->{target}",
                 f"{target_coef}/{r2_coef}={fraction_text(ratio2)}"),
            step("M", amount2, fraction_text(ratio2),
                 fraction_text(product2)),
            step("LIMIT_CHECK",
                 f"{target} from {r1}={fraction_text(product1)} mol",
                 f"{target} from {r2}={fraction_text(product2)} mol"),
            step("LIMITING_REAGENT", limiting,
                 f"{target}={fraction_text(product)} mol"),
        ]
        answer = f"limiting={limiting}; {target}={fraction_text(product)} mol"
        problem = (
            f"Given balanced equation {equation}, initial amounts are "
            f"{r1}={amount1} mol and {r2}={amount2} mol. Find the limiting "
            f"reactant and maximum {target} produced."
        )
        return problem, steps, answer

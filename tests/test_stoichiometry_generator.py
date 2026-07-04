import itertools
import math
import os
import re
import sys
import unittest
from fractions import Fraction
from functools import reduce

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.stoichiometry_generator import StoichiometryGenerator
from helpers import DELIM


BALANCE_RE = re.compile(r"Balance the equation: (.+)\.")
MASS_RE = re.compile(
    r"Given balanced equation (.+), how many grams of ([A-Za-z0-9]+) form "
    r"from (\d+) g ([A-Za-z0-9]+)\? Molar masses: "
    r"([A-Za-z0-9]+)=(\d+) g/mol, ([A-Za-z0-9]+)=(\d+) g/mol\."
)
VOLUME_RE = re.compile(
    r"Given balanced equation (.+), how many liters of ([A-Za-z0-9]+) gas "
    r"form from (\d+) g ([A-Za-z0-9]+)\? Use molar mass "
    r"([A-Za-z0-9]+)=(\d+) g/mol and molar gas volume (\d+) L/mol\."
)
LIMIT_RE = re.compile(
    r"Given balanced equation (.+), initial amounts are ([A-Za-z0-9]+)="
    r"(\d+) mol and ([A-Za-z0-9]+)=(\d+) mol\. Find the limiting reactant "
    r"and maximum ([A-Za-z0-9]+) produced\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


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


def parse_term(term):
    match = re.fullmatch(r"(?:(\d+) )?([A-Za-z0-9]+)", term)
    if not match:
        raise AssertionError(f"bad term: {term}")
    return int(match.group(1) or 1), match.group(2)


def parse_equation(equation):
    left_text, right_text = equation.split(" -> ")
    left = [parse_term(term) for term in left_text.split(" + ")]
    right = [parse_term(term) for term in right_text.split(" + ")]
    return left, right


def format_species(coefficient, formula):
    return formula if coefficient == 1 else f"{coefficient} {formula}"


def format_equation(left, right, left_coeffs, right_coeffs):
    left_text = [
        format_species(coef, formula)
        for coef, formula in zip(left_coeffs, left)
    ]
    right_text = [
        format_species(coef, formula)
        for coef, formula in zip(right_coeffs, right)
    ]
    return f"{' + '.join(left_text)} -> {' + '.join(right_text)}"


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


def find_balance(left, right):
    formulas = left + right
    elements = sorted(set().union(*(formula_counts(f) for f in formulas)))
    for coeffs in itertools.product(range(1, 11), repeat=len(formulas)):
        common = reduce(math.gcd, coeffs)
        if common != 1:
            continue
        left_coeffs = coeffs[:len(left)]
        right_coeffs = coeffs[len(left):]
        left_counts = side_counts(left, left_coeffs)
        right_counts = side_counts(right, right_coeffs)
        if all(left_counts.get(e, 0) == right_counts.get(e, 0)
               for e in elements):
            return list(left_coeffs), list(right_coeffs)
    raise AssertionError(f"could not balance {left} -> {right}")


def coefficient_for(parsed_equation, formula):
    left, right = parsed_equation
    for coefficient, species in left + right:
        if species == formula:
            return coefficient
    raise AssertionError(f"{formula} not in equation")


def expected_balance(problem):
    skeleton = BALANCE_RE.fullmatch(problem).group(1)
    left_terms, right_terms = parse_equation(skeleton)
    left = [formula for _, formula in left_terms]
    right = [formula for _, formula in right_terms]
    left_coeffs, right_coeffs = find_balance(left, right)
    balanced = format_equation(left, right, left_coeffs, right_coeffs)
    left_totals = side_counts(left, left_coeffs)
    right_totals = side_counts(right, right_coeffs)
    steps = [
        make_step("STOICH_SETUP", "balance_equation", skeleton),
        make_step("BALANCE_COEFFS",
                  f"reactants={','.join(str(c) for c in left_coeffs)}",
                  f"products={','.join(str(c) for c in right_coeffs)}"),
    ]
    for element in element_order(left, right):
        steps.append(make_step("ATOM_CHECK", element,
                               f"left={left_totals[element]}",
                               f"right={right_totals[element]}"))
    steps.append(make_step("BALANCED_EQ", balanced))
    return steps, balanced


def expected_mass(problem):
    (equation, target, given_mass_raw, given, mm_name1, mm1_raw,
     mm_name2, mm2_raw) = MASS_RE.fullmatch(problem).groups()
    self_check = {mm_name1: int(mm1_raw), mm_name2: int(mm2_raw)}
    parsed = parse_equation(equation)
    given_mm = self_check[given]
    target_mm = self_check[target]
    given_mass = int(given_mass_raw)
    given_coef = coefficient_for(parsed, given)
    target_coef = coefficient_for(parsed, target)
    ratio = Fraction(target_coef, given_coef)
    moles_given = Fraction(given_mass, given_mm)
    moles_target = moles_given * ratio
    target_mass = moles_target * target_mm
    steps = [
        make_step("STOICH_SETUP", "mass_to_mass", equation,
                  f"given={given_mass} g {given}, target={target}"),
        make_step("MOLAR_MASS", given, f"{given_mm} g/mol"),
        make_step("MOLAR_MASS", target, f"{target_mm} g/mol"),
        make_step("STOICH_RATIO", f"{given}->{target}",
                  f"{target_coef}/{given_coef}={fraction_text(ratio)}"),
        make_step("D", given_mass, given_mm, fraction_text(moles_given)),
        make_step("M", fraction_text(moles_given), fraction_text(ratio),
                  fraction_text(moles_target)),
        make_step("M", fraction_text(moles_target), target_mm,
                  fraction_text(target_mass)),
    ]
    answer = f"mass {target}={fraction_text(target_mass)} g"
    return steps, answer


def expected_volume(problem):
    (equation, target, given_mass_raw, given, mm_name, mm_raw,
     molar_volume_raw) = VOLUME_RE.fullmatch(problem).groups()
    self_check = {mm_name: int(mm_raw)}
    parsed = parse_equation(equation)
    given_mass = int(given_mass_raw)
    given_mm = self_check[given]
    molar_volume = int(molar_volume_raw)
    given_coef = coefficient_for(parsed, given)
    target_coef = coefficient_for(parsed, target)
    ratio = Fraction(target_coef, given_coef)
    moles_given = Fraction(given_mass, given_mm)
    moles_target = moles_given * ratio
    volume = moles_target * molar_volume
    steps = [
        make_step("STOICH_SETUP", "mass_to_volume", equation,
                  f"given={given_mass} g {given}, target={target}"),
        make_step("MOLAR_MASS", given, f"{given_mm} g/mol"),
        make_step("STOICH_RATIO", f"{given}->{target}",
                  f"{target_coef}/{given_coef}={fraction_text(ratio)}"),
        make_step("D", given_mass, given_mm, fraction_text(moles_given)),
        make_step("M", fraction_text(moles_given), fraction_text(ratio),
                  fraction_text(moles_target)),
        make_step("MOLAR_VOLUME", "1 mol gas", f"{molar_volume} L"),
        make_step("M", fraction_text(moles_target), molar_volume,
                  fraction_text(volume)),
    ]
    answer = f"V {target}={fraction_text(volume)} L"
    return steps, answer


def expected_limiting(problem):
    (equation, r1, amount1_raw, r2, amount2_raw,
     target) = LIMIT_RE.fullmatch(problem).groups()
    parsed = parse_equation(equation)
    amount1 = int(amount1_raw)
    amount2 = int(amount2_raw)
    target_coef = coefficient_for(parsed, target)
    r1_coef = coefficient_for(parsed, r1)
    r2_coef = coefficient_for(parsed, r2)
    ratio1 = Fraction(target_coef, r1_coef)
    ratio2 = Fraction(target_coef, r2_coef)
    product1 = amount1 * ratio1
    product2 = amount2 * ratio2
    limiting, product = ((r1, product1) if product1 < product2
                         else (r2, product2))
    steps = [
        make_step("STOICH_SETUP", "limiting_reagent", equation,
                  f"given={r1}={amount1} mol, {r2}={amount2} mol"),
        make_step("STOICH_RATIO", f"{r1}->{target}",
                  f"{target_coef}/{r1_coef}={fraction_text(ratio1)}"),
        make_step("M", amount1, fraction_text(ratio1),
                  fraction_text(product1)),
        make_step("STOICH_RATIO", f"{r2}->{target}",
                  f"{target_coef}/{r2_coef}={fraction_text(ratio2)}"),
        make_step("M", amount2, fraction_text(ratio2),
                  fraction_text(product2)),
        make_step("LIMIT_CHECK",
                  f"{target} from {r1}={fraction_text(product1)} mol",
                  f"{target} from {r2}={fraction_text(product2)} mol"),
        make_step("LIMITING_REAGENT", limiting,
                  f"{target}={fraction_text(product)} mol"),
    ]
    answer = f"limiting={limiting}; {target}={fraction_text(product)} mol"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if BALANCE_RE.fullmatch(problem):
        steps, answer = expected_balance(problem)
    elif MASS_RE.fullmatch(problem):
        steps, answer = expected_mass(problem)
    elif VOLUME_RE.fullmatch(problem):
        steps, answer = expected_volume(problem)
    elif LIMIT_RE.fullmatch(problem):
        steps, answer = expected_limiting(problem)
    else:
        raise AssertionError(f"unrecognized problem: {problem}")
    steps.append(make_step("Z", answer))
    return steps, answer


class TestStoichiometryGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = StoichiometryGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps_and_atom_checks(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ATOM_CHECK":
                    self.assertEqual(fields[2].replace("left=", ""),
                                     fields[3].replace("right=", ""),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in StoichiometryGenerator.VARIANTS:
            result = StoichiometryGenerator(variant).generate()
            self.assertEqual(result["operation"], f"stoichiometry_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StoichiometryGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

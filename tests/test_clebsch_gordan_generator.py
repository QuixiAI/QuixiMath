import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.clebsch_gordan_generator import ClebschGordanGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For Clebsch-Gordan coupling j1=([^,]+), j2=([^ ]+) with phase=([+-]), "
    r"(find the coupled state|find the coefficient of ([^ ]+)|"
    r"find the probability weight of ([^ ]+)) for total J=([^,]+), M=([^ ]+)\."
)

HALF_HALF = {
    ("1", "1"): [("1", "ket(+,+)")],
    ("1", "0"): [("1/sqrt2", "ket(+,-)"),
                   ("1/sqrt2", "ket(-,+)")],
    ("1", "-1"): [("1", "ket(-,-)")],
    ("0", "0"): [("1/sqrt2", "ket(+,-)"),
                   ("-1/sqrt2", "ket(-,+)")],
}

ONE_HALF = {
    ("3/2", "3/2"): [("1", "ket(1,+)")],
    ("3/2", "1/2"): [("sqrt(2/3)", "ket(0,+)"),
                       ("sqrt(1/3)", "ket(1,-)")],
    ("3/2", "-1/2"): [("sqrt(1/3)", "ket(-1,+)"),
                        ("sqrt(2/3)", "ket(0,-)")],
    ("3/2", "-3/2"): [("1", "ket(-1,-)")],
    ("1/2", "1/2"): [("sqrt(1/3)", "ket(0,+)"),
                       ("-sqrt(2/3)", "ket(1,-)")],
    ("1/2", "-1/2"): [("sqrt(2/3)", "ket(-1,+)"),
                        ("-sqrt(1/3)", "ket(0,-)")],
}

SQUARES = {
    "0": "0",
    "1": "1",
    "-1": "1",
    "1/sqrt2": "1/2",
    "-1/sqrt2": "1/2",
    "sqrt(1/3)": "1/3",
    "-sqrt(1/3)": "1/3",
    "sqrt(2/3)": "2/3",
    "-sqrt(2/3)": "2/3",
}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def neg_coeff(coeff):
    if coeff == "0":
        return "0"
    if coeff.startswith("-"):
        return coeff[1:]
    return f"-{coeff}"


def apply_phase(terms, phase):
    if phase == "+":
        return terms
    return [(neg_coeff(coeff), basis) for coeff, basis in terms]


def coeff_for_basis(terms, basis):
    for coeff, term_basis in terms:
        if term_basis == basis:
            return coeff
    return "0"


def term_text(coeff, basis):
    abs_coeff = coeff[1:] if coeff.startswith("-") else coeff
    body = basis if abs_coeff == "1" else f"{abs_coeff}*{basis}"
    return body, coeff.startswith("-")


def state_text(terms):
    pieces = []
    for coeff, basis in terms:
        body, negative = term_text(coeff, basis)
        if not pieces:
            pieces.append(f"-{body}" if negative else body)
        elif negative:
            pieces.append(f"- {body}")
        else:
            pieces.append(f"+ {body}")
    return " ".join(pieces)


def normalization_text(terms):
    values = [SQUARES[coeff] for coeff, _ in terms]
    if values == ["1"]:
        return "1"
    return " + ".join(values)


def table_for_coupling(j1, j2):
    return HALF_HALF if (j1, j2) == ("1/2", "1/2") else ONE_HALF


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    j1, j2, phase, action, coeff_basis, prob_basis, J, M = match.groups()
    if action == "find the coupled state":
        variant = "state"
        basis = None
    elif coeff_basis is not None:
        variant = "coefficient"
        basis = coeff_basis
    else:
        variant = "probability"
        basis = prob_basis
    return variant, j1, j2, phase, J, M, basis


def common_steps(j1, j2, J, M, phase, terms):
    norm = normalization_text(terms)
    steps = [
        make_step("CG_SETUP", f"j1={j1}", f"j2={j2}", f"phase={phase}"),
        make_step("TARGET_STATE", f"J={J}", f"M={M}"),
        make_step("LADDER_RULE", "J_- = J1_- + J2_-",
                  "lower from highest weights"),
    ]
    if J in ("0", "1/2"):
        steps.append(make_step("ORTHOGONALITY", "lower multiplet",
                               "orthogonal to higher J"))
    steps.extend([
        make_step("NORMALIZE", norm, "1"),
        make_step("CG_STATE", f"J={J}, M={M}", state_text(terms)),
        make_step("CHECK", "normalization", "1", "ok"),
    ])
    return steps


def expected_flow(example):
    variant, j1, j2, phase, J, M, basis = parse_problem(example["problem"])
    terms = apply_phase(table_for_coupling(j1, j2)[(J, M)], phase)
    steps = common_steps(j1, j2, J, M, phase, terms)
    state = state_text(terms)
    if variant == "state":
        answer = f"ket({J},{M}) = {state}"
    elif variant == "coefficient":
        coeff = coeff_for_basis(terms, basis)
        steps.append(make_step("CG_COEFF", basis, coeff))
        answer = f"coefficient of {basis} = {coeff}"
    else:
        coeff = coeff_for_basis(terms, basis)
        probability = SQUARES[coeff]
        steps.extend([
            make_step("CG_COEFF", basis, coeff),
            make_step("PROB_WEIGHT", f"{coeff}^2", probability),
        ])
        answer = f"probability weight of {basis} = {probability}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestClebschGordanGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ClebschGordanGenerator()

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

    def test_probability_weights_are_coefficients_squared(self):
        gen = ClebschGordanGenerator("probability")
        for _ in range(300):
            result = gen.generate()
            coeff_step = next(s for s in result["steps"]
                              if s.startswith("CG_COEFF"))
            prob_step = next(s for s in result["steps"]
                             if s.startswith("PROB_WEIGHT"))
            coeff = coeff_step.split(DELIM)[2]
            self.assertEqual(SQUARES[coeff], prob_step.split(DELIM)[2])

    def test_variants_are_available(self):
        for variant in ClebschGordanGenerator.VARIANTS:
            result = ClebschGordanGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"clebsch_gordan_{variant}")
            self.assertEqual(parse_problem(result["problem"])[0], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ClebschGordanGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])
            self.assertNotIn(DELIM, result["problem"])


if __name__ == "__main__":
    unittest.main()

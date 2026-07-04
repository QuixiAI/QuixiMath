import random

from base_generator import ProblemGenerator
from helpers import step, jid


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

PRODUCT_BASES = {
    ("1/2", "1/2"): ["ket(+,+)", "ket(+,-)", "ket(-,+)", "ket(-,-)"],
    ("1", "1/2"): [
        "ket(1,+)", "ket(1,-)", "ket(0,+)",
        "ket(0,-)", "ket(-1,+)", "ket(-1,-)",
    ],
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


class ClebschGordanGenerator(ProblemGenerator):
    """
    Exact Clebsch-Gordan table entries for 1/2 x 1/2 and 1 x 1/2.

    Variants:
    - state: emit the full coupled state.
    - coefficient: extract one product-basis coefficient.
    - probability: square one coefficient to a probability weight.

    Op-codes used:
    - CG_SETUP / TARGET_STATE / LADDER_RULE / ORTHOGONALITY
    - NORMALIZE / CG_STATE / CG_COEFF / PROB_WEIGHT / CHECK
    - Z: state, coefficient, or probability
    """

    VARIANTS = ["state", "coefficient", "probability"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        j1, j2 = random.choice([("1/2", "1/2"), ("1", "1/2")])
        table = table_for_coupling(j1, j2)
        J, M = random.choice(list(table))
        phase = random.choice(["+", "-"])
        terms = apply_phase(table[(J, M)], phase)
        basis = None
        if variant in ("coefficient", "probability"):
            basis = random.choice(PRODUCT_BASES[(j1, j2)])
        steps = self._steps(j1, j2, J, M, phase, terms)
        state = state_text(terms)
        if variant == "state":
            answer = f"ket({J},{M}) = {state}"
            problem = self._problem(j1, j2, phase, J, M, "find the coupled state")
        elif variant == "coefficient":
            coeff = coeff_for_basis(terms, basis)
            steps.append(step("CG_COEFF", basis, coeff))
            answer = f"coefficient of {basis} = {coeff}"
            problem = self._problem(
                j1, j2, phase, J, M,
                f"find the coefficient of {basis}",
            )
        else:
            coeff = coeff_for_basis(terms, basis)
            probability = SQUARES[coeff]
            steps.extend([
                step("CG_COEFF", basis, coeff),
                step("PROB_WEIGHT", f"{coeff}^2", probability),
            ])
            answer = f"probability weight of {basis} = {probability}"
            problem = self._problem(
                j1, j2, phase, J, M,
                f"find the probability weight of {basis}",
            )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"clebsch_gordan_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _steps(self, j1, j2, J, M, phase, terms):
        norm = normalization_text(terms)
        steps = [
            step("CG_SETUP", f"j1={j1}", f"j2={j2}", f"phase={phase}"),
            step("TARGET_STATE", f"J={J}", f"M={M}"),
            step("LADDER_RULE", "J_- = J1_- + J2_-",
                 "lower from highest weights"),
        ]
        if J in ("0", "1/2"):
            steps.append(step("ORTHOGONALITY", "lower multiplet",
                              "orthogonal to higher J"))
        steps.extend([
            step("NORMALIZE", norm, "1"),
            step("CG_STATE", f"J={J}, M={M}", state_text(terms)),
            step("CHECK", "normalization", "1", "ok"),
        ])
        return steps

    def _problem(self, j1, j2, phase, J, M, action):
        return (
            f"For Clebsch-Gordan coupling j1={j1}, j2={j2} with "
            f"phase={phase}, {action} for total J={J}, M={M}."
        )

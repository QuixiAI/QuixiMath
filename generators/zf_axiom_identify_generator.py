"""Identify ZF axioms that justify exact set constructions.

Variants: ``single_step``, ``construction_sequence``, and
``definition_expansion``. Op-codes: ``FORM``, ``EXPAND``, ``CHECK``, and
``Z``. Indexed set and function symbols give every variant an unbounded
problem space.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True

QUERIES = {
    "single_step": (
        "Name the one ZF axiom that directly guarantees the target set.",
        "Identify the direct existence axiom for this formation.",
        "Which ZF axiom licenses exactly this construction?",
        "Classify the displayed set-forming operation by its ZF axiom.",
        "Give the axiom used in this single construction step.",
    ),
    "construction_sequence": (
        "List the required ZF axioms in construction order.",
        "Name each existence axiom used, preserving the displayed order.",
        "Recover the ordered axiom sequence for the construction.",
        "Trace the set formation and report its axioms in order.",
        "Give the exact ordered list of ZF construction axioms.",
    ),
    "definition_expansion": (
        "Expand the abbreviation and give the required axioms in order.",
        "Replace the notation by its defining set expression, then name the axioms.",
        "State the canonical expansion and its ordered ZF justification.",
        "Unfold the displayed definition and identify its formation axioms.",
        "Give the exact expansion followed by the axiom sequence.",
    ),
}


def indexed_symbol(letter):
    return f"{letter}_{random.randint(0, 999999)}"


def finite_base():
    start = random.randint(-100000, 99990)
    size = random.randint(3, 7)
    values = list(range(start, start + size))
    return "{" + ", ".join(str(value) for value in values) + "}"


class ZFAxiomIdentifyGenerator(ProblemGenerator):
    """Generate exact ZF axiom-identification and expansion exercises."""

    VARIANTS = ("single_step", "construction_sequence",
                "definition_expansion")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _single_step(self):
        left, right = indexed_symbol("A"), indexed_symbol("B")
        function = indexed_symbol("f")
        case = random.choices(
            ("pair", "union", "power", "separation", "replacement",
             "infinity"),
            weights=(20, 20, 20, 20, 19, 1),
            k=1,
        )[0]
        if case == "pair":
            target, axiom = f"{{{left}, {right}}}", "Pairing"
        elif case == "union":
            target, axiom = f"∪{left}", "Union"
        elif case == "power":
            target, axiom = f"P({left})", "Power Set"
        elif case == "separation":
            base = finite_base()
            target = f"{{x ∈ {base} : x is even}}"
            axiom = "Separation"
        elif case == "replacement":
            target = f"{{{function}(x) : x ∈ {finite_base()}}}"
            axiom = "Replacement"
        else:
            target, axiom = "ω", "Infinity"
        problem = (f"ZF formation target: {target}. "
                   f"{random.choice(QUERIES['single_step'])}")
        steps = [step("FORM", target, axiom),
                 step("CHECK", "direct existence axiom", axiom)]
        return problem, steps, axiom

    def _construction_sequence(self):
        left, right = indexed_symbol("A"), indexed_symbol("B")
        case = random.randrange(3)
        if case == 0:
            target = f"{left} ∪ {right}"
            intermediate = f"{{{left}, {right}}}"
            expanded = f"∪{intermediate}"
            forms = ((intermediate, "Pairing"), (expanded, "Union"))
            axioms = ("Pairing", "Union")
            condition = "Assume both named sets exist."
        elif case == 1:
            target = f"{left} × {right}"
            ambient = f"P(P({left} ∪ {right}))"
            expanded = (f"Sep({ambient}; ordered pairs from {left} "
                        f"and {right})")
            forms = (("ordered pairs", "Pairing"),
                     (f"P({left} ∪ {right})", "Power Set"),
                     (ambient, "Power Set"),
                     (expanded, "Separation"))
            axioms = ("Pairing", "Power Set", "Power Set", "Separation")
            condition = (f"Assume {left}, {right}, and {left} ∪ {right} "
                         "already exist.")
        else:
            target = f"{{{left}}}"
            expanded = target
            forms = ((f"{target} from inputs {left}, {left}", "Pairing"),)
            axioms = ("Pairing",)
            condition = f"Use Pairing with both inputs equal to {left}."
        problem = (f"ZF construction target: {target}. {condition} "
                   f"Displayed expansion: {expanded}. "
                   f"{random.choice(QUERIES['construction_sequence'])}")
        steps = [step("FORM", expression, axiom)
                 for expression, axiom in forms]
        steps.append(step("CHECK", target, ", ".join(axioms)))
        return problem, steps, ", ".join(axioms)

    def _definition_expansion(self):
        left, right = indexed_symbol("A"), indexed_symbol("B")
        function = indexed_symbol("f")
        case = random.randrange(5)
        if case == 0:
            abbreviation = f"{left} ∪ {right}"
            expansion = f"∪{{{left}, {right}}}"
            forms = ((f"{{{left}, {right}}}", "Pairing"),
                     (expansion, "Union"))
        elif case == 1:
            abbreviation = f"singleton({left})"
            expansion = f"{{{left}}}"
            forms = ((f"{expansion} from inputs {left}, {left}", "Pairing"),)
        elif case == 2:
            base = finite_base()
            abbreviation = f"{base} ∩ {right}"
            expansion = f"{{x ∈ {base} : x ∈ {right}}}"
            forms = ((expansion, "Separation"),)
        elif case == 3:
            base = finite_base()
            abbreviation = f"{base} − {right}"
            expansion = f"{{x ∈ {base} : x ∉ {right}}}"
            forms = ((expansion, "Separation"),)
        else:
            base = finite_base()
            abbreviation = f"{function}[{base}]"
            expansion = f"{{{function}(x) : x ∈ {base}}}"
            forms = ((expansion, "Replacement"),)
        axioms = tuple(axiom for _, axiom in forms)
        answer = f"{expansion}; {', '.join(axioms)}"
        problem = (f"ZF definition: {abbreviation}. "
                   f"{random.choice(QUERIES['definition_expansion'])}")
        steps = [step("EXPAND", abbreviation, expansion)]
        steps.extend(step("FORM", expression, axiom)
                     for expression, axiom in forms)
        steps.append(step("CHECK", "expansion and axiom order", answer))
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "single_step":
            problem, steps, answer = self._single_step()
        elif variant == "construction_sequence":
            problem, steps, answer = self._construction_sequence()
        else:
            problem, steps, answer = self._definition_expansion()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"zf_axiom_identify_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

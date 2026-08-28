"""Hilbert-style axiom instances, substitutions, and MP derivations.

Variants: ``pm_axioms``, ``lukasiewicz_axioms``, ``instance_identify``,
``substitute``, and ``justify``.  Op-codes: ``AXIOM_MATCH``, ``SUBSTITUTE``,
``MP``, ``CHECK``, and ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import Imp, Not, Or, Var, random_formula, render, substitute


FOUNDATIONS = True


p, q, r = Var("p"), Var("q"), Var("r")

PM_SCHEMAS = (
    ("PM *1.2 Taut", Imp(Or(p, p), p)),
    ("PM *1.3 Add", Imp(q, Or(p, q))),
    ("PM *1.4 Perm", Imp(Or(p, q), Or(q, p))),
    ("PM *1.5 Assoc", Imp(Or(p, Or(q, r)), Or(q, Or(p, r)))),
    ("PM *1.6 Sum", Imp(Imp(q, r), Imp(Or(p, q), Or(p, r)))),
)

LUKASIEWICZ_SCHEMAS = (
    ("L1", Imp(p, Imp(q, p))),
    ("L2", Imp(Imp(p, Imp(q, r)), Imp(Imp(p, q), Imp(p, r)))),
    ("L3", Imp(Imp(Not(p), Not(q)), Imp(q, p))),
)

QUERIES = {
    "pm_axioms": (
        "Instantiate the named Principia Mathematica axiom.",
        "Apply the displayed substitution to the PM schema.",
        "Compute this uniform instance of the named PM axiom.",
        "Replace the PM schema variables simultaneously and give the result.",
        "Determine the exact formula produced from the PM axiom.",
    ),
    "lukasiewicz_axioms": (
        "Instantiate the named Łukasiewicz axiom.",
        "Apply the displayed substitution to the Łukasiewicz schema.",
        "Compute this uniform instance of the named implication axiom.",
        "Replace the Łukasiewicz schema variables simultaneously and give the result.",
        "Determine the exact formula produced from the Łukasiewicz axiom.",
    ),
    "instance_identify": (
        "Identify the unique schema and recover its substitution.",
        "Match the candidate against the displayed axiom system.",
        "Name the axiom instance and list every schema-variable binding.",
        "Determine which schema generated the candidate formula.",
        "Recover the unique axiom label and simultaneous substitution.",
    ),
    "substitute": (
        "Apply the uniform substitution to the formula schema.",
        "Replace every schema variable simultaneously.",
        "Compute the exact substituted formula.",
        "Carry out the displayed formula substitution.",
        "Determine the canonical result of the uniform replacement.",
    ),
    "justify": (
        "Fill every blank Hilbert-style justification.",
        "Recover each axiom instance and modus ponens citation.",
        "Supply the exact labels and substitutions for all lines.",
        "Complete the derivation annotations from the displayed formulas.",
        "Justify every axiom and derived line in order.",
    ),
}


REPLACEMENT_NAMES = tuple("abcdefghjkmn")


def schema_variables(schema):
    found = []

    def visit(node):
        if isinstance(node, Var) and node.name in ("p", "q", "r"):
            if node.name not in found:
                found.append(node.name)
        elif isinstance(node, Not):
            visit(node.arg)
        elif hasattr(node, "left"):
            visit(node.left)
            visit(node.right)

    visit(schema)
    return tuple(name for name in ("p", "q", "r") if name in found)


def random_replacement():
    return random_formula(depth=random.choice((1, 2)),
                          names=REPLACEMENT_NAMES,
                          connectives=("¬", "∨", "→"), exact_depth=True)


def random_mapping(schema):
    return {name: random_replacement() for name in schema_variables(schema)}


def mapping_text(mapping):
    return "; ".join(f"{name} := {render(mapping[name])}"
                     for name in ("p", "q", "r") if name in mapping)


def binding_text(mapping):
    pieces = []
    for name in ("p", "q", "r"):
        if name not in mapping:
            continue
        rendered = render(mapping[name])
        if hasattr(mapping[name], "left"):
            rendered = f"({rendered})"
        pieces.append(f"{name} := {rendered}")
    return ", ".join(pieces)


def schema_table_text(schemas):
    return "; ".join(f"{label} = {render(schema)}"
                     for label, schema in schemas)


def match_schema(schema, formula, bindings=None):
    bindings = {} if bindings is None else dict(bindings)
    if isinstance(schema, Var) and schema.name in ("p", "q", "r"):
        old = bindings.get(schema.name)
        if old is not None and old != formula:
            return None
        bindings[schema.name] = formula
        return bindings
    if type(schema) is not type(formula):
        return None
    if isinstance(schema, Not):
        return match_schema(schema.arg, formula.arg, bindings)
    if hasattr(schema, "left"):
        bindings = match_schema(schema.left, formula.left, bindings)
        return (None if bindings is None else
                match_schema(schema.right, formula.right, bindings))
    return bindings if schema == formula else None


def unique_instance(schemas):
    while True:
        label, schema = random.choice(schemas)
        mapping = random_mapping(schema)
        formula = substitute(schema, mapping)
        matches = [(other_label, found)
                   for other_label, other in schemas
                   for found in [match_schema(other, formula)]
                   if found is not None]
        if len(matches) == 1:
            return label, schema, mapping, formula


class HilbertAxiomDerivationGenerator(ProblemGenerator):
    """Generate exact Hilbert-system instantiation and derivation tasks."""

    VARIANTS = ("pm_axioms", "lukasiewicz_axioms", "instance_identify",
                "substitute", "justify")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _named_instance(self, schemas, variant, system_name):
        label, schema = random.choice(schemas)
        mapping = random_mapping(schema)
        result = substitute(schema, mapping)
        convention = ("PM convention: A → B abbreviates ¬A ∨ B. "
                      if system_name == "PM" else "")
        problem = (f"Named {system_name} axiom: {label} = {render(schema)}. "
                   f"{convention}"
                   f"Substitution: {mapping_text(mapping)}. "
                   f"{random.choice(QUERIES[variant])}")
        steps = [step("SUBSTITUTE", render(schema), mapping_text(mapping),
                      render(result)),
                 step("AXIOM_MATCH", label, binding_text(mapping)),
                 step("CHECK", "uniform replacement", render(result))]
        return problem, steps, render(result)

    def _instance_identify(self):
        if random.choice((True, False)):
            system, schemas = "PM", PM_SCHEMAS
        else:
            system, schemas = "Lukasiewicz", LUKASIEWICZ_SCHEMAS
        label, _, mapping, formula = unique_instance(schemas)
        convention = ("PM convention: A → B abbreviates ¬A ∨ B. "
                      if system == "PM" else "")
        problem = (f"Axiom system: {system}. {convention}Schemas: "
                   f"{schema_table_text(schemas)}. Candidate formula: "
                   f"{render(formula)}. "
                   f"{random.choice(QUERIES['instance_identify'])}")
        answer = f"{label} [{binding_text(mapping)}]"
        steps = [step("AXIOM_MATCH", label, binding_text(mapping)),
                 step("SUBSTITUTE", label, mapping_text(mapping),
                      render(formula)),
                 step("CHECK", "candidate re-derived", render(formula))]
        return problem, steps, answer

    def _substitute(self):
        names = random.sample(("p", "q", "r"), random.randint(2, 3))
        schema = random_formula(depth=2, names=names,
                                connectives=("¬", "∨", "→"),
                                exact_depth=True, use_all=True)
        mapping = {name: random_replacement() for name in names}
        result = substitute(schema, mapping)
        problem = (f"Formula schema: {render(schema)}. Uniform substitution: "
                   f"{mapping_text(mapping)}. "
                   f"{random.choice(QUERIES['substitute'])}")
        steps = [step("SUBSTITUTE", render(schema), mapping_text(mapping),
                      render(result)),
                 step("CHECK", "simultaneous substitution", render(result))]
        return problem, steps, render(result)

    def _justify(self):
        l1_label, l1 = LUKASIEWICZ_SCHEMAS[0]
        base_mapping = random_mapping(l1)
        base = substitute(l1, base_mapping)
        formulas = [base]
        kinds = ["axiom"]
        justifications = [f"{l1_label} [{binding_text(base_mapping)}]"]
        levels = random.choice((1, 2))
        current = base
        current_line = 1
        for _ in range(levels):
            extra = random_replacement()
            lift_mapping = {"p": current, "q": extra}
            implication = substitute(l1, lift_mapping)
            implication_line = len(formulas) + 1
            formulas.append(implication)
            kinds.append("axiom")
            justifications.append(f"{l1_label} [{binding_text(lift_mapping)}]")
            result = implication.right
            formulas.append(result)
            kinds.append("derived")
            justifications.append(f"MP {current_line},{implication_line}")
            current, current_line = result, len(formulas)
        displayed = "; ".join(
            f"{index}. {render(formula)} [{kind} ____]"
            for index, (formula, kind) in enumerate(zip(formulas, kinds), 1))
        problem = (f"Lukasiewicz schema: L1 = {render(l1)}. Lines marked "
                   "axiom are L1 instances; lines marked derived use modus "
                   "ponens from the unique earlier pair. Derivation: "
                   f"{displayed}. {random.choice(QUERIES['justify'])}")
        steps = []
        for index, (formula, kind, justification) in enumerate(
                zip(formulas, kinds, justifications), 1):
            if kind == "axiom":
                binding = justification.split("[", 1)[1][:-1]
                steps.append(step("AXIOM_MATCH", "L1", binding))
                steps.append(step("CHECK", f"line {index} re-derived",
                                  render(formula)))
            else:
                citations = justification.split(" ", 1)[1]
                steps.append(step("MP", f"lines {citations}", render(formula)))
                steps.append(step("CHECK", f"line {index} re-derived",
                                  render(formula)))
        answer = "; ".join(
            f"{index}: {justification}"
            for index, justification in enumerate(justifications, 1))
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "pm_axioms":
            problem, steps, answer = self._named_instance(
                PM_SCHEMAS, variant, "PM")
        elif variant == "lukasiewicz_axioms":
            problem, steps, answer = self._named_instance(
                LUKASIEWICZ_SCHEMAS, variant, "Łukasiewicz")
        elif variant == "instance_identify":
            problem, steps, answer = self._instance_identify()
        elif variant == "substitute":
            problem, steps, answer = self._substitute()
        else:
            problem, steps, answer = self._justify()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"hilbert_axiom_derivation_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

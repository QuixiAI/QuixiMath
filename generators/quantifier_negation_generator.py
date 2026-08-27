"""Negate quantified statements and push every negation to an atom.

Variants:
- ``symbolic`` negates one-quantifier formulas with a binary connective.
- ``english`` translates and negates a quantified English sentence.
- ``nested`` negates formulas with two quantifiers, including restricted forms.
- ``with_counterexample`` negates a universal claim and supplies its least
  counterexample in the stated finite integer domain.

The generator uses a small predicate-logic AST internally.  Predicate and
variable banks, numeric domains, formula shapes, and five phrasings per
variant give well over 100,000 distinct problem texts.

Op-codes:
- ``TRANSLATE``: turn a controlled-English sentence into a formula.
- ``NEG_QUANT``: exchange ``¬∀`` with ``∃¬`` or ``¬∃`` with ``∀¬``.
- ``NEG_CONNECTIVE``: apply De Morgan, implication negation, or double negation.
- ``REWRITE``: show the complete negation-normal-form result.
- ``WITNESS`` / ``CHECK``: exhibit and verify the least counterexample.
- ``Z``: exact NNF formula, optionally followed by its counterexample.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


PREDICATES = tuple("ABCDEFGHJKLMNPQRSTUVWXYZ")
VARIABLES = ("x", "y", "z", "u", "v", "w")
NOUNS = (
    "student", "artist", "athlete", "chemist", "driver", "gardener",
    "musician", "neighbor", "pilot", "reader", "scientist", "teacher",
    "traveler", "volunteer", "writer", "baker", "carpenter", "dancer",
    "engineer", "farmer", "hiker", "inventor", "judge", "librarian",
)
ADJECTIVES = (
    "alert", "careful", "curious", "focused", "friendly", "generous",
    "honest", "patient", "prepared", "punctual", "quiet", "reliable",
    "rested", "skilled", "thorough", "vigilant", "wise", "creative",
    "organized", "resourceful", "attentive", "calm", "diligent", "kind",
)

QUERIES = {
    "symbolic": (
        "Negate the formula and push the negation to the predicates.",
        "Write the logical negation in negation normal form.",
        "Exchange the quantifier and simplify the negated connective.",
        "Give the equivalent NNF formula for the statement's negation.",
        "Move every negation inward until it applies only to an atom.",
    ),
    "english": (
        "Translate the sentence, negate it, and give the NNF formula.",
        "Write the logical negation using the supplied predicate key.",
        "Formalize the denial of the sentence with negation only on atoms.",
        "Give the canonical quantified formula that contradicts the sentence.",
        "Negate the English claim and simplify to NNF.",
    ),
    "nested": (
        "Negate the nested statement and push the negation to the atoms.",
        "Reverse each quantifier and give the resulting NNF formula.",
        "Write the logical denial of this nested quantified formula.",
        "Move the outer negation through every quantifier and connective.",
        "Give the canonical negation-normal-form result.",
    ),
    "with_counterexample": (
        "Negate the claim and report its least counterexample.",
        "Write the NNF denial and identify the first witness in the domain.",
        "Formalize why the universal statement fails and give the least witness.",
        "Give the negated formula together with its smallest counterexample.",
        "Push the negation inward, then verify the earliest failing value.",
    ),
}


def atom(predicate, *arguments):
    return ("atom", predicate, tuple(arguments))


def negate(node):
    return ("not", node)


def binary(kind, left, right):
    return (kind, left, right)


def quantify(kind, variable, body):
    return (kind, variable, body)


def render(node):
    """Render the generator's predicate-logic fragment canonically."""
    kind = node[0]
    if kind == "atom":
        return f"{node[1]}({', '.join(node[2])})"
    if kind == "not":
        child = render(node[1])
        return f"¬{child}" if node[1][0] == "atom" else f"¬({child})"
    if kind in ("forall", "exists"):
        symbol = "∀" if kind == "forall" else "∃"
        return f"{symbol}{node[1]} {render(node[2])}"
    symbol = {"and": "∧", "or": "∨", "imp": "→"}[kind]
    return f"({render(node[1])} {symbol} {render(node[2])})"


def negation_normal_form(node):
    """Return ``¬node`` in NNF."""
    kind = node[0]
    if kind == "atom":
        return negate(node)
    if kind == "not":
        return node[1]
    if kind == "forall":
        return quantify("exists", node[1], negation_normal_form(node[2]))
    if kind == "exists":
        return quantify("forall", node[1], negation_normal_form(node[2]))
    if kind == "and":
        return binary("or", negation_normal_form(node[1]),
                      negation_normal_form(node[2]))
    if kind == "or":
        return binary("and", negation_normal_form(node[1]),
                      negation_normal_form(node[2]))
    if kind == "imp":
        return binary("and", node[1], negation_normal_form(node[2]))
    raise ValueError(f"unsupported predicate formula kind: {kind}")


def transformation_steps(source, target):
    """List each quantifier/connective law present, then the full rewrite."""
    steps = []

    def visit(node, under_negation=True):
        kind = node[0]
        if kind in ("forall", "exists"):
            source_symbol = "∀" if kind == "forall" else "∃"
            target_symbol = "∃" if kind == "forall" else "∀"
            steps.append(step("NEG_QUANT", f"¬{source_symbol}{node[1]}",
                              f"{target_symbol}{node[1]} ¬"))
            visit(node[2], True)
        elif kind in ("and", "or", "imp"):
            left, right = render(node[1]), render(node[2])
            if kind == "and":
                after = f"¬{left} ∨ ¬{right}"
                symbol = "∧"
            elif kind == "or":
                after = f"¬{left} ∧ ¬{right}"
                symbol = "∨"
            else:
                after = f"{left} ∧ ¬{right}"
                symbol = "→"
            steps.append(step("NEG_CONNECTIVE", f"¬({left} {symbol} {right})",
                              after))
            visit(node[1], kind != "imp")
            visit(node[2], True)
        elif kind == "not" and under_negation:
            steps.append(step("NEG_CONNECTIVE", f"¬¬{render(node[1])}",
                              render(node[1])))

    visit(source)
    steps.append(step("REWRITE", render(target)))
    return steps


class QuantifierNegationGenerator(ProblemGenerator):
    """Generate independently checkable predicate-negation traces."""

    VARIANTS = ("symbolic", "english", "nested", "with_counterexample")
    WEIGHTS = (0.15, 0.15, 0.20, 0.50)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _symbols(count):
        return random.sample(PREDICATES, count)

    def _symbolic(self):
        variable = random.choice(VARIABLES)
        first_name, second_name = self._symbols(2)
        first = atom(first_name, variable)
        second = atom(second_name, variable)
        shapes = (
            quantify("forall", variable, binary("imp", first, second)),
            quantify("exists", variable, binary("and", first, second)),
            quantify("forall", variable, binary("or", first, second)),
            quantify("exists", variable, binary("imp", first, second)),
            quantify("forall", variable, negate(first)),
            quantify("exists", variable, negate(first)),
        )
        source = random.choice(shapes)
        problem = (f"Formula: {render(source)}. "
                   f"{random.choice(QUERIES['symbolic'])}")
        return source, problem, []

    def _english(self):
        variable = random.choice(VARIABLES)
        noun, adjective = random.choice(NOUNS), random.choice(ADJECTIVES)
        first_name, second_name = self._symbols(2)
        first = atom(first_name, variable)
        second = atom(second_name, variable)
        form = random.choice(("every", "no", "some", "some_not"))
        if form == "every":
            sentence = f"Every {noun} is {adjective}"
            source = quantify("forall", variable, binary("imp", first, second))
        elif form == "no":
            sentence = f"No {noun} is {adjective}"
            source = quantify("forall", variable,
                              binary("imp", first, negate(second)))
        elif form == "some":
            sentence = f"Some {noun} is {adjective}"
            source = quantify("exists", variable, binary("and", first, second))
        else:
            sentence = f"Some {noun} is not {adjective}"
            source = quantify("exists", variable,
                              binary("and", first, negate(second)))
        article = "an" if noun[0] in "aeiou" else "a"
        key = (f"{first_name}({variable}): {variable} is {article} {noun}; "
               f"{second_name}({variable}): {variable} is {adjective}")
        problem = (f"Sentence: {sentence}. Predicate key: {key}. "
                   f"{random.choice(QUERIES['english'])}")
        return source, problem, [step("TRANSLATE", sentence, render(source))]

    def _nested(self):
        first_variable, second_variable = random.sample(VARIABLES, 2)
        unary_name, relation_name = self._symbols(2)
        unary_first = atom(unary_name, first_variable)
        unary_second = atom(unary_name, second_variable)
        relation = atom(relation_name, first_variable, second_variable)
        shapes = (
            quantify("exists", first_variable,
                     quantify("forall", second_variable, relation)),
            quantify("forall", first_variable,
                     quantify("exists", second_variable, relation)),
            quantify("forall", first_variable,
                     binary("imp", unary_first,
                            quantify("exists", second_variable, relation))),
            quantify("exists", first_variable,
                     binary("and", unary_first,
                            quantify("forall", second_variable, relation))),
            quantify("forall", first_variable,
                     quantify("exists", second_variable,
                              binary("or", relation, unary_second))),
        )
        source = random.choice(shapes)
        problem = (f"Formula: {render(source)}. "
                   f"{random.choice(QUERIES['nested'])}")
        return source, problem, []

    def _with_counterexample(self):
        upper = random.randint(100, 10000000)
        variable = "n"
        source = quantify(
            "forall", variable,
            binary("imp", atom("Prime", variable), atom("Odd", variable)),
        )
        problem = (
            f"Domain: integers n with 2 ≤ n ≤ {upper}. "
            "Claim: every prime n in the domain is odd. "
            f"{random.choice(QUERIES['with_counterexample'])}"
        )
        return source, problem, []

    def generate(self):
        variant = self.variant or random.choices(
            self.VARIANTS, weights=self.WEIGHTS, k=1)[0]
        if variant == "symbolic":
            source, problem, prefix_steps = self._symbolic()
        elif variant == "english":
            source, problem, prefix_steps = self._english()
        elif variant == "nested":
            source, problem, prefix_steps = self._nested()
        else:
            source, problem, prefix_steps = self._with_counterexample()

        target = negation_normal_form(source)
        steps = prefix_steps + transformation_steps(source, target)
        answer = render(target)
        if variant == "with_counterexample":
            steps.extend([
                step("WITNESS", "n=2", "Prime(2)=T", "Odd(2)=F"),
                step("CHECK", "2 is in the domain", "claim fails at n=2"),
            ])
            answer += "; n = 2"
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"quantifier_negation_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

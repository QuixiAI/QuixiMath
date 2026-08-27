"""Translate controlled quantified English into canonical predicate logic.

Variants:
- ``universal`` covers every/all/no unary class-property statements.
- ``existential`` covers positive and negative existential statements.
- ``restricted_quantifier`` distinguishes implication from conjunction when a
  noun phrase has a relative-clause restriction.
- ``two_place`` translates subject/object quantifier scope for binary verbs.

Large noun, property, verb, and predicate-symbol banks combine with five
question phrasings and multiple sentence grammars for well over 100,000
problem texts.

Op-codes:
- ``PREDICATES``: repeat the supplied predicate key.
- ``QUANT_CHOICE``: map the controlling English determiner to a quantifier.
- ``SHAPE``: state why a restriction becomes implication or conjunction.
- ``REWRITE``: give the complete canonical formula.
- ``Z``: exact formula.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


PREDICATES = tuple("ABCDEFGHJKLMNPQRSTUVWXYZ")
NOUNS = (
    "artist", "athlete", "baker", "carpenter", "chemist", "dancer",
    "driver", "engineer", "farmer", "gardener", "hiker", "inventor",
    "judge", "librarian", "musician", "neighbor", "pilot", "reader",
    "scientist", "student", "teacher", "traveler", "volunteer", "writer",
)
PROPERTIES = (
    "alert", "attentive", "calm", "careful", "creative", "curious",
    "diligent", "focused", "friendly", "generous", "honest", "kind",
    "organized", "patient", "prepared", "punctual", "quiet", "reliable",
    "resourceful", "rested", "skilled", "thorough", "vigilant", "wise",
)
VERBS = (
    "admires", "assists", "calls", "follows", "greets", "helps",
    "mentors", "observes", "questions", "thanks", "trusts", "visits",
)

QUERIES = {
    "universal": (
        "Translate the sentence into predicate logic.",
        "Write its canonical universal formula.",
        "Use the predicate key to formalize the universal statement.",
        "Give the symbolic form with the correct universal restriction.",
        "Express the universal sentence exactly in the supplied notation.",
    ),
    "existential": (
        "Translate the existential sentence into predicate logic.",
        "Write its canonical existential formula.",
        "Use the predicate key to formalize the existential statement.",
        "Give the symbolic form with the correct existential conjunction.",
        "Express the existential sentence exactly in the supplied notation.",
    ),
    "restricted_quantifier": (
        "Translate the restricted-quantifier sentence.",
        "Formalize both the noun class and its relative-clause restriction.",
        "Write the canonical formula using the supplied predicates.",
        "Choose implication or conjunction from the controlling quantifier.",
        "Express the complete restricted statement symbolically.",
    ),
    "two_place": (
        "Translate the two-place predicate sentence with the stated scope.",
        "Write the canonical nested-quantifier formula.",
        "Formalize the subject and object noun restrictions.",
        "Preserve the English quantifier scope in predicate logic.",
        "Express the binary-relation statement in the supplied notation.",
    ),
}


def predicate(symbol, variable):
    return f"{symbol}({variable})"


def relation(symbol, first, second):
    return f"{symbol}({first}, {second})"


def article(word):
    return "an" if word[0] in "aeiou" else "a"


class EnglishToLogicGenerator(ProblemGenerator):
    """Generate template-invertible English-to-predicate-logic records."""

    VARIANTS = ("universal", "existential", "restricted_quantifier",
                "two_place")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _symbols(count):
        return random.sample(PREDICATES, count)

    def _unary_words(self):
        noun = random.choice(NOUNS)
        first_property, second_property = random.sample(PROPERTIES, 2)
        return noun, first_property, second_property

    def _universal(self):
        noun, prop, _ = self._unary_words()
        noun_symbol, property_symbol = self._symbols(2)
        form = random.choice(("every", "all", "each", "any", "no"))
        if form == "every":
            sentence = f"Every {noun} is {prop}"
            choice = "every → ∀"
            consequent = predicate(property_symbol, "x")
        elif form == "all":
            sentence = f"All {noun}s are {prop}"
            choice = "all → ∀"
            consequent = predicate(property_symbol, "x")
        elif form == "each":
            sentence = f"Each {noun} is {prop}"
            choice = "each → ∀"
            consequent = predicate(property_symbol, "x")
        elif form == "any":
            sentence = f"Any {noun} is {prop}"
            choice = "any → ∀"
            consequent = predicate(property_symbol, "x")
        else:
            sentence = f"No {noun} is {prop}"
            choice = "no → ∀ with negated property"
            consequent = f"¬{predicate(property_symbol, 'x')}"
        formula = (f"∀x ({predicate(noun_symbol, 'x')} → {consequent})")
        key = (f"{noun_symbol}(x): x is {article(noun)} {noun}; "
               f"{property_symbol}(x): x is {prop}")
        return sentence, key, choice, "universal restriction → implication", formula

    def _existential(self):
        noun, prop, _ = self._unary_words()
        noun_symbol, property_symbol = self._symbols(2)
        form = random.choice(("some", "at_least_one", "there_is",
                              "some_not", "there_is_not"))
        negative = form in ("some_not", "there_is_not")
        if form == "some":
            sentence = f"Some {noun} is {prop}"
        elif form == "at_least_one":
            sentence = f"At least one {noun} is {prop}"
        elif form == "there_is":
            sentence = f"There is {article(noun)} {noun} that is {prop}"
        elif form == "some_not":
            sentence = f"Some {noun} is not {prop}"
        else:
            sentence = f"There is {article(noun)} {noun} that is not {prop}"
        second = predicate(property_symbol, "x")
        if negative:
            second = "¬" + second
        formula = f"∃x ({predicate(noun_symbol, 'x')} ∧ {second})"
        key = (f"{noun_symbol}(x): x is {article(noun)} {noun}; "
               f"{property_symbol}(x): x is {prop}")
        return sentence, key, "some/there is → ∃", "existential restriction → conjunction", formula

    def _restricted(self):
        noun, first_property, second_property = self._unary_words()
        noun_symbol, first_symbol, second_symbol = self._symbols(3)
        form = random.choice(("every", "all", "some", "no"))
        restriction = (f"({predicate(noun_symbol, 'x')} ∧ "
                       f"{predicate(first_symbol, 'x')})")
        if form == "every":
            sentence = (f"Every {noun} who is {first_property} is "
                        f"{second_property}")
            formula = f"∀x ({restriction} → {predicate(second_symbol, 'x')})"
            choice, shape = "every → ∀", "universal restriction → implication"
        elif form == "all":
            sentence = (f"All {noun}s who are {first_property} are "
                        f"{second_property}")
            formula = f"∀x ({restriction} → {predicate(second_symbol, 'x')})"
            choice, shape = "all → ∀", "universal restriction → implication"
        elif form == "some":
            sentence = (f"Some {noun} who is {first_property} is "
                        f"{second_property}")
            formula = f"∃x ({restriction} ∧ {predicate(second_symbol, 'x')})"
            choice, shape = "some → ∃", "existential restriction → conjunction"
        else:
            sentence = (f"No {noun} who is {first_property} is "
                        f"{second_property}")
            formula = (f"∀x ({restriction} → "
                       f"¬{predicate(second_symbol, 'x')})")
            choice, shape = "no → ∀ with negated property", "universal restriction → implication"
        key = (f"{noun_symbol}(x): x is {article(noun)} {noun}; "
               f"{first_symbol}(x): x is {first_property}; "
               f"{second_symbol}(x): x is {second_property}")
        return sentence, key, choice, shape, formula

    def _two_place(self):
        subject, object_noun = random.sample(NOUNS, 2)
        verb = random.choice(VERBS)
        subject_symbol, object_symbol, relation_symbol = self._symbols(3)
        form = random.choice(("every_some", "some_every", "every_every",
                              "some_some"))
        subject_atom = predicate(subject_symbol, "x")
        object_atom = predicate(object_symbol, "y")
        relation_atom = relation(relation_symbol, "x", "y")
        if form == "every_some":
            sentence = f"Every {subject} {verb} some {object_noun}"
            formula = (f"∀x ({subject_atom} → "
                       f"∃y ({object_atom} ∧ {relation_atom}))")
            choice = "every → ∀; some → ∃"
        elif form == "some_every":
            sentence = f"Some {subject} {verb} every {object_noun}"
            formula = (f"∃x ({subject_atom} ∧ "
                       f"∀y ({object_atom} → {relation_atom}))")
            choice = "some → ∃; every → ∀"
        elif form == "every_every":
            sentence = f"Every {subject} {verb} every {object_noun}"
            formula = (f"∀x ({subject_atom} → "
                       f"∀y ({object_atom} → {relation_atom}))")
            choice = "every → ∀; every → ∀"
        else:
            sentence = f"Some {subject} {verb} some {object_noun}"
            formula = (f"∃x ({subject_atom} ∧ "
                       f"∃y ({object_atom} ∧ {relation_atom}))")
            choice = "some → ∃; some → ∃"
        key = (f"{subject_symbol}(x): x is {article(subject)} {subject}; "
               f"{object_symbol}(y): y is {article(object_noun)} {object_noun}; "
               f"{relation_symbol}(x, y): x {verb} y")
        return sentence, key, choice, "subject/object noun phrases restrict their quantifiers", formula

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "universal":
            sentence, key, choice, shape, answer = self._universal()
        elif variant == "existential":
            sentence, key, choice, shape, answer = self._existential()
        elif variant == "restricted_quantifier":
            sentence, key, choice, shape, answer = self._restricted()
        else:
            sentence, key, choice, shape, answer = self._two_place()
        problem = (f"Sentence: {sentence}. Predicate key: {key}. "
                   f"{random.choice(QUERIES[variant])}")
        steps = [step("PREDICATES", key), step("QUANT_CHOICE", choice),
                 step("SHAPE", shape), step("REWRITE", answer),
                 step("Z", answer)]
        return {
            "problem_id": jid(),
            "operation": f"english_to_logic_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

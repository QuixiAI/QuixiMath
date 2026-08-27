"""Parse well-formed formulas and convert infix/Polish notation.

Variants:
- ``is_wff`` classifies a canonical formula or a localized near-miss.
- ``main_connective`` identifies the root connective.
- ``depth_and_subformulas`` reports connective depth and distinct subformulas.
- ``polish_to_infix`` decodes Łukasiewicz ``N K A C E`` notation.
- ``infix_to_polish`` encodes a canonical infix formula.

Near-misses cover dropped/unmatched parentheses, dangling connectives, and
doubled operators.  Exact-depth random formulas and five phrasings yield more
than 100,000 problem texts.

Op-codes:
- ``SCAN``: scan one token while tracking parenthesis/Polish stack depth.
- ``PARSE``: record one parsed subformula and node kind.
- ``MAIN_CONNECTIVE`` / ``DEPTH``: report syntax-tree properties.
- ``POLISH``: record the canonical Łukasiewicz spelling.
- ``Z``: exact parse verdict or conversion.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import (depth, from_polish, main_connective, random_formula,
                          render, size, subformulas, to_polish)


FOUNDATIONS = True


BINARY_SYMBOLS = ("∧", "∨", "→", "↔")

QUERIES = {
    "is_wff": ("Decide whether the expression is a well-formed formula.",
               "Parse the expression or identify its first syntax defect.",
               "Classify the string as a WFF or a localized near-miss.",
               "Check the formula grammar and report the structural result.",
               "Determine whether the displayed string parses correctly."),
    "main_connective": ("Identify the main connective.",
                        "Parse the formula and report its outermost operation.",
                        "Which connective is at the root of the syntax tree?",
                        "Find the main connective and include the formula depth.",
                        "Give the outer connective of the canonical formula."),
    "depth_and_subformulas": ("Find the connective depth and number of distinct subformulas.",
                              "Parse the tree and report its depth and subformula count.",
                              "Count the distinct subformulas and deepest connective level.",
                              "Give both structural measures of the formula.",
                              "Determine the formula's depth and distinct-node count."),
    "polish_to_infix": ("Convert the Polish formula to canonical infix notation.",
                         "Decode the Łukasiewicz string.",
                         "Parse the prefix operators and write the infix formula.",
                         "Translate this Polish notation to the canonical formula.",
                         "Recover the infix syntax tree from the prefix spelling."),
    "infix_to_polish": ("Convert the infix formula to Polish notation.",
                         "Encode the formula with Łukasiewicz operator letters.",
                         "Write the prefix spelling using N, K, A, C, and E.",
                         "Translate the canonical formula to Polish form.",
                         "Give the operator-first encoding of the infix expression."),
}


def node_kind(formula):
    connective = main_connective(formula)
    return "atom" if connective is None else (
        "negation" if connective == "¬" else f"binary {connective}"
    )


class WFFParsingGenerator(ProblemGenerator):
    """Generate syntax-tree walks and deliberately localized invalid strings."""

    VARIANTS = ("is_wff", "main_connective", "depth_and_subformulas",
                "polish_to_infix", "infix_to_polish")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _formula():
        return random_formula(depth=3, names=("p", "q", "r"),
                              connectives=("¬", "∧", "∨", "→", "↔"),
                              exact_depth=True, use_all=True)

    @staticmethod
    def _scan_infix(text):
        steps = []
        level = 0
        for token in text:
            if token.isspace():
                continue
            if token == "(":
                level += 1
            elif token == ")":
                level -= 1
            steps.append(step("SCAN", token, f"parenthesis depth {level}"))
        return steps

    @staticmethod
    def _parse_steps(formula):
        return [step("PARSE", render(item), node_kind(item))
                for item in subformulas(formula)]

    @staticmethod
    def _near_miss(valid):
        kind = random.choice(("unmatched_closing", "dropped_parenthesis",
                              "dangling_connective", "doubled_connective"))
        if kind == "unmatched_closing":
            return ") " + valid, "unmatched parenthesis", 1
        if kind == "dropped_parenthesis" and ")" in valid:
            index = random.choice([i for i, char in enumerate(valid) if char == ")"])
            invalid = valid[:index] + valid[index + 1:]
            return invalid, "unmatched parenthesis", len(invalid) + 1
        if kind == "dangling_connective" or not any(symbol in valid
                                                     for symbol in BINARY_SYMBOLS):
            invalid = valid + " ∧"
            return invalid, "dangling connective", len(invalid)
        indexes = [index for index, char in enumerate(valid)
                   if char in BINARY_SYMBOLS]
        index = random.choice(indexes)
        invalid = valid[:index + 1] + " ∨" + valid[index + 1:]
        position = index + 3
        return invalid, "unexpected connective", position

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        formula = self._formula()
        infix = render(formula)
        if variant == "is_wff":
            valid = random.choice((True, False))
            if valid:
                expression = infix
                answer = (f"wff; main connective {main_connective(formula)}; "
                          f"depth {depth(formula)}; {len(subformulas(formula))} subformulas")
                steps = self._scan_infix(expression) + self._parse_steps(formula)
                steps.extend((step("MAIN_CONNECTIVE", main_connective(formula)),
                              step("DEPTH", depth(formula))))
            else:
                expression, error, position = self._near_miss(infix)
                answer = f"not a wff ({error} at position {position})"
                steps = self._scan_infix(expression)
                steps.append(step("PARSE", "error", error, f"position {position}"))
            problem = (
                f"Expression: {expression}. Positions are 1-based; the end-of-input "
                f"position is one past the last character. "
                f"{random.choice(QUERIES[variant])}"
            )
        elif variant == "main_connective":
            problem = f"Formula: {infix}. {random.choice(QUERIES[variant])}"
            steps = self._scan_infix(infix) + self._parse_steps(formula)
            steps.extend((step("MAIN_CONNECTIVE", main_connective(formula)),
                          step("DEPTH", depth(formula))))
            answer = (f"main connective = {main_connective(formula)}; "
                      f"depth = {depth(formula)}")
        elif variant == "depth_and_subformulas":
            problem = f"Formula: {infix}. {random.choice(QUERIES[variant])}"
            steps = self._scan_infix(infix) + self._parse_steps(formula)
            steps.append(step("DEPTH", depth(formula),
                              f"{len(subformulas(formula))} distinct subformulas"))
            answer = (f"depth = {depth(formula)}; subformulas = "
                      f"{len(subformulas(formula))}")
        elif variant == "polish_to_infix":
            polish = to_polish(formula)
            problem = f"Polish formula: {polish}. {random.choice(QUERIES[variant])}"
            steps = []
            needed = 1
            for token in polish:
                needed -= 1
                if token == "N":
                    needed += 1
                elif token in "KACE":
                    needed += 2
                steps.append(step("SCAN", token, f"open operand slots {needed}"))
            steps.extend(self._parse_steps(from_polish(polish)))
            answer = infix
        else:
            polish = to_polish(formula)
            problem = f"Infix formula: {infix}. {random.choice(QUERIES[variant])}"
            steps = self._scan_infix(infix) + self._parse_steps(formula)
            steps.append(step("POLISH", polish))
            answer = polish
        steps.append(step("Z", answer))
        return {"problem_id": jid(), "operation": f"wff_parsing_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

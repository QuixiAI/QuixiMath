"""Evaluate quantified sentences over explicit finite domains.

Variants:
- ``arithmetic_predicate`` uses ``x < y``, ``x ∣ y``, ``x + y = c``, or
  ``x² > y`` over a displayed positive-integer domain.
- ``relation_table`` evaluates a two-variable sentence from a pair roster.
- ``function_table`` evaluates quantified equalities from a displayed table.
- ``nested_three`` checks a three-quantifier relation sentence exhaustively.

Domains, predicates, quantifier shapes, pair rosters, function tables, and five
phrasings give an effectively unbounded problem space.

Op-codes:
- ``DOMAIN``: state the exact finite carrier.
- ``QUANT_CASE``: open one quantified case or report one matrix assignment.
- ``WITNESS``: give the first witness in domain order.
- ``NO_WITNESS``: show the first failed universal/existential case.
- ``CHECK``: evaluate a predicate or a complete function-table condition.
- ``QUANT_RESULT``: state the truth value of the quantified prefix.
- ``Z``: composite truth value with witnesses, counterexample, or truth column.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import relation_text, roster


FOUNDATIONS = True


QUERIES = {
    "arithmetic_predicate": (
        "Decide the quantified sentence by checking the finite domain.",
        "Evaluate the statement and give first witnesses or a counterexample.",
        "Model-check the formula in increasing domain order.",
        "Determine its truth value with an explicit finite-domain certificate.",
        "Check each required case and report the canonical result.",
    ),
    "relation_table": (
        "Decide the quantified sentence from the relation roster.",
        "Model-check the formula and report first witnesses or a counterexample.",
        "Evaluate the quantifiers in the displayed domain order.",
        "Determine whether the finite relation satisfies the sentence.",
        "Check the relation table exhaustively and give the canonical result.",
    ),
    "function_table": (
        "Decide the quantified equality statement from the function table.",
        "Evaluate the formula using only the displayed function values.",
        "Model-check the equality sentence in increasing domain order.",
        "Determine its truth value and provide the first certificate.",
        "Check every required table entry and give the canonical result.",
    ),
    "nested_three": (
        "Decide the three-quantifier sentence by exhaustive model checking.",
        "Evaluate the nested formula over the displayed relation.",
        "Check the quantifiers in increasing domain order and report the result.",
        "Determine the truth value and include the atomic truth column.",
        "Model-check every ordered triple in the finite domain.",
    ),
}


TWO_PREFIXES = ("forall_exists", "exists_forall", "restricted_forall")


def domain_values(low_size=3, high_size=7):
    size = random.randint(low_size, high_size)
    return tuple(sorted(random.sample(range(1, 41), size)))


def truth_text(value):
    return "true" if value else "false"


def first_two_quantifier_result(domain, prefix, predicate, predicate_text,
                                restriction=None, restriction_text=None):
    """Evaluate a two-variable prefix and produce a forced trace/answer."""
    steps = []
    if prefix == "forall_exists":
        witnesses = []
        for first in domain:
            steps.append(step("QUANT_CASE", f"x={first}"))
            witness = next((second for second in domain
                            if predicate(first, second)), None)
            if witness is None:
                steps.append(step("NO_WITNESS", f"x={first}",
                                  f"tried y in {roster(domain)}"))
                answer = f"false; counterexample x = {first}"
                steps.append(step("QUANT_RESULT", "∀x ∃y", "false"))
                return steps, answer
            witnesses.append(witness)
            steps.append(step("WITNESS", f"x={first}", f"y={witness}",
                              predicate_text(first, witness)))
        answer = "true; witnesses y = " + ", ".join(map(str, witnesses))
        steps.append(step("QUANT_RESULT", "∀x ∃y", "true"))
        return steps, answer

    if prefix == "exists_forall":
        for first in domain:
            steps.append(step("QUANT_CASE", f"x={first}"))
            failure = next((second for second in domain
                            if not predicate(first, second)), None)
            if failure is None:
                steps.append(step("WITNESS", f"x={first}",
                                  f"all y={domain[0]}..{domain[-1]}",
                                  "predicate true"))
                steps.append(step("QUANT_RESULT", "∃x ∀y", "true"))
                return steps, f"true; witness x = {first}"
            steps.append(step("NO_WITNESS", f"x={first}", f"fails y={failure}",
                              predicate_text(first, failure)))
        steps.append(step("QUANT_RESULT", "∃x ∀y", "false"))
        return steps, "false; no x works"

    witnesses = []
    for first in domain:
        applies = restriction(first)
        steps.append(step("QUANT_CASE", f"x={first}",
                          f"{restriction_text(first)}={truth_text(applies)}"))
        if not applies:
            continue
        witness = next((second for second in domain
                        if predicate(first, second)), None)
        if witness is None:
            steps.append(step("NO_WITNESS", f"x={first}",
                              f"tried y in {roster(domain)}"))
            steps.append(step("QUANT_RESULT", "∀x (P(x) → ∃y)", "false"))
            return steps, f"false; counterexample x = {first}"
        witnesses.append((first, witness))
        steps.append(step("WITNESS", f"x={first}", f"y={witness}",
                          predicate_text(first, witness)))
    pairs = ", ".join(f"{first}→{second}" for first, second in witnesses)
    answer = f"true; witnesses x→y = {pairs}" if pairs else "true; no P-cases"
    steps.append(step("QUANT_RESULT", "∀x (P(x) → ∃y)", "true"))
    return steps, answer


def two_formula(prefix, condition, restriction=None):
    if prefix == "forall_exists":
        return f"∀x ∃y ({condition})"
    if prefix == "exists_forall":
        return f"∃x ∀y ({condition})"
    return f"∀x ({restriction} → ∃y ({condition}))"


class QuantifierFiniteDomainGenerator(ProblemGenerator):
    """Generate exact finite-model-checking records."""

    VARIANTS = ("arithmetic_predicate", "relation_table", "function_table",
                "nested_three")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _restriction(domain):
        choice = random.choice(("even", "odd", "at_least"))
        if choice == "even":
            return (lambda value: value % 2 == 0,
                    lambda value: f"Even({value})",
                    "Even(x)")
        if choice == "odd":
            return (lambda value: value % 2 == 1,
                    lambda value: f"Odd({value})",
                    "Odd(x)")
        cutoff = random.choice(domain)
        return (lambda value: value >= cutoff,
                lambda value: f"{value} ≥ {cutoff}",
                f"x ≥ {cutoff}")

    def _arithmetic(self):
        domain = domain_values()
        prefix = random.choice(TWO_PREFIXES)
        kind = random.choice(("less", "divides", "sum", "square"))
        if kind == "less":
            condition = "x < y"
            predicate = lambda first, second: first < second
            text = lambda first, second: f"{first} < {second}"
        elif kind == "divides":
            condition = "x ∣ y"
            predicate = lambda first, second: second % first == 0
            text = lambda first, second: f"{first} ∣ {second}"
        elif kind == "sum":
            target = random.randint(domain[0] * 2, domain[-1] * 2)
            condition = f"x + y = {target}"
            predicate = lambda first, second: first + second == target
            text = lambda first, second: f"{first} + {second} = {target}"
        else:
            condition = "x² > y"
            predicate = lambda first, second: first * first > second
            text = lambda first, second: f"{first}² > {second}"
        restriction, restriction_text, restriction_formula = self._restriction(domain)
        formula = two_formula(prefix, condition, restriction_formula)
        problem = (f"Domain D = {roster(domain)}. Formula: {formula}. "
                   f"{random.choice(QUERIES['arithmetic_predicate'])}")
        steps = [step("DOMAIN", roster(domain))]
        trace, answer = first_two_quantifier_result(
            domain, prefix, predicate, text, restriction, restriction_text)
        return problem, steps + trace, answer

    def _relation(self):
        domain = domain_values()
        all_pairs = list(itertools.product(domain, repeat=2))
        count = random.randint(0, min(14, len(all_pairs)))
        relation = frozenset(random.sample(all_pairs, count))
        prefix = random.choice(TWO_PREFIXES)
        restriction, restriction_text, restriction_formula = self._restriction(domain)
        predicate = lambda first, second: (first, second) in relation
        text = lambda first, second: (
            f"({first}, {second}) ∈ R" if (first, second) in relation
            else f"({first}, {second}) ∉ R")
        formula = two_formula(prefix, "R(x, y)", restriction_formula)
        problem = (f"Domain D = {roster(domain)}. R = {relation_text(relation)}. "
                   f"Formula: {formula}. "
                   f"{random.choice(QUERIES['relation_table'])}")
        steps = [step("DOMAIN", roster(domain))]
        trace, answer = first_two_quantifier_result(
            domain, prefix, predicate, text, restriction, restriction_text)
        return problem, steps + trace, answer

    def _function(self):
        domain = domain_values()
        mode = random.choice(("total", "constant", "onto", "omitted"))
        if mode == "constant" and random.choice((True, False)):
            value = random.choice(domain)
            mapping = {item: value for item in domain}
        elif mode == "onto" and random.choice((True, False)):
            outputs = list(domain)
            random.shuffle(outputs)
            mapping = dict(zip(domain, outputs))
        elif mode == "omitted" and random.choice((True, False)):
            omitted = random.choice(domain)
            choices = [item for item in domain if item != omitted]
            mapping = {item: random.choice(choices) for item in domain}
        else:
            mapping = {item: random.choice(domain) for item in domain}
        table = ", ".join(f"f({item})={mapping[item]}" for item in domain)
        if mode == "total":
            prefix, condition = "forall_exists", "f(x) = y"
            predicate = lambda first, second: mapping[first] == second
            text = lambda first, second: f"f({first}) = {second}"
        elif mode == "constant":
            prefix, condition = "exists_forall", "f(y) = x"
            predicate = lambda first, second: mapping[second] == first
            text = lambda first, second: f"f({second}) = {mapping[second]}"
        elif mode == "onto":
            prefix, condition = "forall_exists", "f(y) = x"
            predicate = lambda first, second: mapping[second] == first
            text = lambda first, second: f"f({second}) = {mapping[second]}"
        else:
            prefix, condition = "exists_forall", "f(y) ≠ x"
            predicate = lambda first, second: mapping[second] != first
            text = lambda first, second: f"f({second}) = {mapping[second]}"
        formula = two_formula(prefix, condition)
        problem = (f"Domain D = {roster(domain)}. Function table: {table}. "
                   f"Formula: {formula}. "
                   f"{random.choice(QUERIES['function_table'])}")
        steps = [step("DOMAIN", roster(domain))]
        trace, answer = first_two_quantifier_result(
            domain, prefix, predicate, text)
        return problem, steps + trace, answer

    def _nested(self):
        domain = domain_values(3, 4)
        all_pairs = list(itertools.product(domain, repeat=2))
        count = random.randint(0, len(all_pairs))
        relation = frozenset(random.sample(all_pairs, count))
        shape = random.choice(("chain", "two_step", "bridge", "shared_row"))
        if shape == "chain":
            prefix = (("forall", "x"), ("exists", "y"), ("forall", "z"))
            matrix_text = "(R(x, y) ∧ R(y, z)) → R(x, z)"
            matrix = lambda x, y, z: not (
                (x, y) in relation and (y, z) in relation) or (x, z) in relation
        elif shape == "two_step":
            prefix = (("exists", "x"), ("forall", "y"), ("exists", "z"))
            matrix_text = "R(x, y) ∧ R(y, z)"
            matrix = lambda x, y, z: ((x, y) in relation
                                      and (y, z) in relation)
        elif shape == "bridge":
            prefix = (("forall", "x"), ("forall", "y"), ("exists", "z"))
            matrix_text = "R(x, z) ∨ R(z, y)"
            matrix = lambda x, y, z: ((x, z) in relation
                                      or (z, y) in relation)
        else:
            prefix = (("exists", "x"), ("exists", "y"), ("forall", "z"))
            matrix_text = "R(x, z) ∧ R(y, z)"
            matrix = lambda x, y, z: ((x, z) in relation
                                      and (y, z) in relation)

        def quantify(index, environment):
            if index == len(prefix):
                return matrix(environment["x"], environment["y"],
                              environment["z"])
            kind, variable = prefix[index]
            values = []
            for value in domain:
                extended = dict(environment)
                extended[variable] = value
                values.append(quantify(index + 1, extended))
            return all(values) if kind == "forall" else any(values)

        prefix_text = " ".join(
            ("∀" if kind == "forall" else "∃") + variable
            for kind, variable in prefix)
        formula = f"{prefix_text} ({matrix_text})"
        column = "".join(
            "T" if matrix(*values) else "F"
            for values in itertools.product(domain, repeat=3))
        result = quantify(0, {})
        problem = (f"Domain D = {roster(domain)}. R = {relation_text(relation)}. "
                   f"Formula: {formula}. Triple order: x, then y, then z. "
                   f"{random.choice(QUERIES['nested_three'])}")
        steps = [step("DOMAIN", roster(domain))]
        for values, value in zip(itertools.product(domain, repeat=3), column):
            x_value, y_value, z_value = values
            steps.append(step("QUANT_CASE",
                              f"x={x_value}, y={y_value}, z={z_value}",
                              f"matrix={value}"))
        steps.append(step("QUANT_RESULT", prefix_text, truth_text(result),
                          f"atomic column={column}"))
        answer = f"{truth_text(result)}; atomic column = {column}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "arithmetic_predicate":
            problem, steps, answer = self._arithmetic()
        elif variant == "relation_table":
            problem, steps, answer = self._relation()
        elif variant == "function_table":
            problem, steps, answer = self._function()
        else:
            problem, steps, answer = self._nested()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"quantifier_finite_domain_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

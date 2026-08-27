"""Convert predicate formulas to capture-free prenex normal form.

Variants:
- ``pull_out`` moves two or three non-clashing quantifiers left-to-right.
- ``rename_then_pull`` alpha-renames a repeated/clashing binder before pulling.
- ``negation_then_prenex`` first pushes an outer negation through quantifiers
  and a connective, then pulls the resulting prefix.

Every source is built as two quantified branches joined by ``∧`` or ``∨``.
The implementation standardizes bound variables apart, records the prescribed
``v→v1`` renaming, and constructs the prefix structurally.  Predicate, variable,
prefix, connective, and phrasing choices exceed 100,000 problem texts.

Op-codes:
- ``NEG_QUANT`` / ``NEG_CONNECTIVE``: push an outer negation to atoms.
- ``RENAME``: alpha-rename one binder and its bound occurrences.
- ``PULL``: move one quantifier past the root connective in forced order.
- ``REWRITE``: show the current complete formula after each structural stage.
- ``CHECK``: confirm that the final matrix contains no quantifier.
- ``Z``: exact canonical prenex formula.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


PREDICATES = tuple("ABCDEFGHJKLMNPQRSTUVWXYZ")
VARIABLES = ("x", "y", "z", "u", "v", "w")

QUERIES = {
    "pull_out": (
        "Convert the formula to prenex normal form.",
        "Pull the quantifiers in the stated order and give the prenex result.",
        "Move every quantifier to the front without changing the matrix.",
        "Write the equivalent formula with one left-to-right prefix.",
        "Give the canonical prenex normal form.",
    ),
    "rename_then_pull": (
        "Apply the required alpha-renaming, then convert to prenex form.",
        "Avoid variable capture and pull the quantifiers left-to-right.",
        "Standardize the binders apart before forming the prefix.",
        "Rename the clashing binder as stated and give the prenex result.",
        "Perform capture-free prenex conversion in the prescribed order.",
    ),
    "negation_then_prenex": (
        "Push the negation to atoms, then convert to prenex normal form.",
        "Negate the quantifiers and form the left-to-right prenex prefix.",
        "Find the equivalent NNF first and then pull every quantifier forward.",
        "Move the negation inward before producing the prenex result.",
        "Give the capture-free prenex form after negation normalization.",
    ),
}


def atom(predicate, *arguments):
    return ("atom", predicate, tuple(arguments))


def quantify(kind, variable, body):
    return (kind, variable, body)


def render(node):
    kind = node[0]
    if kind == "atom":
        return f"{node[1]}({', '.join(node[2])})"
    if kind == "not":
        child = render(node[1])
        return f"¬{child}" if node[1][0] == "atom" else f"¬{child}"
    if kind in ("forall", "exists"):
        return f"{'∀' if kind == 'forall' else '∃'}{node[1]} {render(node[2])}"
    symbol = {"and": "∧", "or": "∨"}[kind]
    return f"({render(node[1])} {symbol} {render(node[2])})"


def wrap(prefix, matrix):
    result = matrix
    for kind, variable in reversed(prefix):
        result = quantify(kind, variable, result)
    return result


def free_variables(node, bound=frozenset()):
    kind = node[0]
    if kind == "atom":
        return set(node[2]) - set(bound)
    if kind == "not":
        return free_variables(node[1], bound)
    if kind in ("forall", "exists"):
        return free_variables(node[2], bound | {node[1]})
    return (free_variables(node[1], bound)
            | free_variables(node[2], bound))


def rename_bound(body, old, new):
    kind = body[0]
    if kind == "atom":
        arguments = tuple(new if value == old else value for value in body[2])
        return ("atom", body[1], arguments)
    if kind == "not":
        return ("not", rename_bound(body[1], old, new))
    if kind in ("forall", "exists"):
        if body[1] == old:
            return body
        return (kind, body[1], rename_bound(body[2], old, new))
    return (kind, rename_bound(body[1], old, new),
            rename_bound(body[2], old, new))


def standardize_apart(node):
    """Rename binders that repeat or would capture a globally free variable."""
    global_free = free_variables(node)
    used = set()
    renamings = []

    def visit(item):
        kind = item[0]
        if kind == "atom":
            return item
        if kind == "not":
            return ("not", visit(item[1]))
        if kind in ("forall", "exists"):
            variable, body = item[1], item[2]
            if variable in used or variable in global_free:
                index = 1
                fresh = f"{variable}{index}"
                unavailable = used | global_free | free_variables(body)
                while fresh in unavailable:
                    index += 1
                    fresh = f"{variable}{index}"
                body = rename_bound(body, variable, fresh)
                renamings.append((kind, variable, fresh))
                variable = fresh
            used.add(variable)
            return (kind, variable, visit(body))
        return (kind, visit(item[1]), visit(item[2]))

    return visit(node), renamings


def to_nnf(node, positive=True):
    kind = node[0]
    if kind == "atom":
        return node if positive else ("not", node)
    if kind == "not":
        return to_nnf(node[1], not positive)
    if kind in ("forall", "exists"):
        if positive:
            return (kind, node[1], to_nnf(node[2], True))
        dual = "exists" if kind == "forall" else "forall"
        return (dual, node[1], to_nnf(node[2], False))
    if positive:
        return (kind, to_nnf(node[1], True), to_nnf(node[2], True))
    dual = "or" if kind == "and" else "and"
    return (dual, to_nnf(node[1], False), to_nnf(node[2], False))


def split_prefix(node):
    prefix = []
    while node[0] in ("forall", "exists"):
        prefix.append((node[0], node[1]))
        node = node[2]
    return prefix, node


def quantifier_text(item):
    return ("∀" if item[0] == "forall" else "∃") + item[1]


class PrenexNormalFormGenerator(ProblemGenerator):
    """Generate forced, capture-free prenex conversions."""

    VARIANTS = ("pull_out", "rename_then_pull", "negation_then_prenex")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _branch(prefix, predicate, arguments):
        return wrap(prefix, atom(predicate, *arguments))

    def _source(self, variant):
        connector = random.choice(("and", "or"))
        first_predicate, second_predicate = random.sample(PREDICATES, 2)
        first_variable, second_variable, third_variable = random.sample(VARIABLES, 3)
        total = random.choice((2, 3))
        left_count = random.randint(1, total - 1)
        right_count = total - left_count
        kinds = [random.choice(("forall", "exists")) for _ in range(total)]

        if variant == "rename_then_pull":
            shared = first_variable
            left_vars = [shared]
            right_vars = [shared]
            if left_count == 2:
                left_vars.append(third_variable)
            if right_count == 2:
                right_vars.append(third_variable)
        else:
            ordered = [first_variable, second_variable, third_variable]
            left_vars = ordered[:left_count]
            right_vars = ordered[left_count:total]

        left_prefix = list(zip(kinds[:left_count], left_vars))
        right_prefix = list(zip(kinds[left_count:], right_vars))
        free_name = random.choice([name for name in VARIABLES
                                   if name not in set(left_vars + right_vars)])
        left_args = tuple(left_vars + ([free_name] if random.choice((True, False)) else []))
        right_args = tuple(right_vars + ([free_name] if random.choice((True, False)) else []))
        left = self._branch(left_prefix, first_predicate, left_args)
        right = self._branch(right_prefix, second_predicate, right_args)
        joined = (connector, left, right)
        return ("not", joined) if variant == "negation_then_prenex" else joined

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        source = self._source(variant)
        nnf = to_nnf(source)
        standardized, renamings = standardize_apart(nnf)
        assert standardized[0] in ("and", "or")
        connector = standardized[0]
        left_prefix, left_matrix = split_prefix(standardized[1])
        right_prefix, right_matrix = split_prefix(standardized[2])
        prefix = left_prefix + right_prefix
        matrix = (connector, left_matrix, right_matrix)
        target = wrap(prefix, matrix)

        if variant == "negation_then_prenex":
            policy = "first push negation to atoms, then pull left-to-right"
        else:
            policy = "pull quantifiers left-to-right"
        rename_text = (", ".join(f"{old}→{new}" for _, old, new in renamings)
                       if renamings else "none")
        problem = (f"Formula: {render(source)}. Policy: {policy}. "
                   f"Required renaming: {rename_text}. "
                   f"{random.choice(QUERIES[variant])}")
        steps = []
        if variant == "negation_then_prenex":
            original = source[1]
            original_left, original_right = original[1], original[2]
            for branch in (original_left, original_right):
                branch_prefix, _ = split_prefix(branch)
                for kind, variable in branch_prefix:
                    symbol = "∀" if kind == "forall" else "∃"
                    dual = "∃" if kind == "forall" else "∀"
                    steps.append(step("NEG_QUANT", f"¬{symbol}{variable}",
                                      f"{dual}{variable} ¬"))
            source_symbol = "∧" if original[0] == "and" else "∨"
            target_symbol = "∨" if original[0] == "and" else "∧"
            steps.append(step("NEG_CONNECTIVE", f"¬(A {source_symbol} B)",
                              f"¬A {target_symbol} ¬B"))
            steps.append(step("REWRITE", render(nnf)))
        for kind, old, new in renamings:
            symbol = "∀" if kind == "forall" else "∃"
            steps.append(step("RENAME", f"{symbol}{old}", f"{symbol}{new}"))
        if renamings:
            steps.append(step("REWRITE", render(standardized)))

        accumulated = []
        for side, side_prefix in (("left", left_prefix), ("right", right_prefix)):
            for index, item in enumerate(side_prefix):
                accumulated.append(item)
                remaining_left = (left_prefix[len(accumulated):]
                                  if side == "left" else [])
                if side == "left":
                    remaining_right = right_prefix
                else:
                    right_done = len(accumulated) - len(left_prefix)
                    remaining_right = right_prefix[right_done:]
                current_matrix = (
                    connector,
                    wrap(remaining_left, left_matrix),
                    wrap(remaining_right, right_matrix),
                )
                current = wrap(accumulated, current_matrix)
                symbol = "∧" if connector == "and" else "∨"
                steps.append(step("PULL", quantifier_text(item),
                                  f"from {side} past {symbol}"))
                steps.append(step("REWRITE", render(current)))
        steps.append(step("CHECK", "matrix quantifier-free", render(matrix)))
        answer = render(target)
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"prenex_normal_form_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

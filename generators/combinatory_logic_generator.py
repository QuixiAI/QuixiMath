"""Deterministic SKI and BCK combinatory-logic reductions.

Variants: ``ski_reduce``, ``bck``, ``define_by_ski``, and
``normal_form_count``.  Terms are fully parenthesized applications and are
built backward from known normal forms.  Op-codes: ``COMB_RULE``, ``REWRITE``,
``CHECK``, and ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True
VARIABLES = tuple("abcdefghjkmnpqrstuvwxyz")

QUERIES = {
    "ski_reduce": (
        "Reduce the SKI term to normal form.",
        "Apply the leftmost-outermost SKI rules.",
        "Determine the combinator term's normal form.",
        "Contract each earliest SKI redex.",
        "Normalize the displayed SKI application.",
    ),
    "bck": (
        "Reduce the BCK term to normal form.",
        "Apply the leftmost-outermost BCK rules.",
        "Determine the BCK combinator term's normal form.",
        "Contract each earliest BCK redex.",
        "Normalize the displayed BCK application.",
    ),
    "define_by_ski": (
        "Verify that S K K acts as I on the argument.",
        "Reduce the displayed SKI definition of I.",
        "Show by normalization that S K K returns its argument.",
        "Apply the S and K rules to verify the identity combinator.",
        "Determine the normal form of the proposed I application.",
    ),
    "normal_form_count": (
        "Give both the normal form and contraction count.",
        "Normalize the term and count the rule applications.",
        "Determine the final term and number of reductions.",
        "Count each leftmost-outermost contraction through normal form.",
        "Report the normal form together with its exact step count.",
    ),
}


def atom(name):
    return ("atom", name)


def app(left, right):
    return ("app", left, right)


def term_text(term):
    if term[0] == "atom":
        return term[1]
    return f"({term_text(term[1])} {term_text(term[2])})"


def random_normal(depth=None):
    depth = random.randint(2, 3) if depth is None else depth
    if depth <= 0 or (depth > 1 and random.random() < 0.05):
        return atom(random.choice(VARIABLES))
    return app(random_normal(depth - 1), random_normal(depth - 1))


RULE_TEXT = {
    "I": ("I x", "x"),
    "K": ("K x y", "x"),
    "S": ("S x y z", "x z (y z)"),
    "B": ("B x y z", "x (y z)"),
    "C": ("C x y z", "x z y"),
}


def root_contract(term, allowed):
    head = term
    args = []
    while head[0] == "app":
        args.append(head[2])
        head = head[1]
    args.reverse()
    if head[0] != "atom" or head[1] not in allowed:
        return None
    name = head[1]
    arity = 1 if name == "I" else 2 if name == "K" else 3
    if len(args) < arity:
        return None
    if name == "I":
        result = args[0]
    elif name == "K":
        result = args[0]
    elif name == "S":
        first, second, third = args[:3]
        result = app(app(first, third), app(second, third))
    elif name == "B":
        first, second, third = args[:3]
        result = app(first, app(second, third))
    else:
        first, second, third = args[:3]
        result = app(app(first, third), second)
    for extra in args[arity:]:
        result = app(result, extra)
    return result, name


def reduce_once(term, allowed):
    contracted = root_contract(term, allowed)
    if contracted is not None:
        return contracted
    if term[0] == "app":
        left = reduce_once(term[1], allowed)
        if left is not None:
            return app(left[0], term[2]), left[1]
        right = reduce_once(term[2], allowed)
        if right is not None:
            return app(term[1], right[0]), right[1]
    return None


def normalize(term, allowed, limit=8):
    trace = []
    current = term
    for _ in range(limit + 1):
        outcome = reduce_once(current, allowed)
        if outcome is None:
            return trace, current
        if len(trace) == limit:
            return None
        new, rule = outcome
        trace.append((current, new, rule))
        current = new
    return None


def ski_wrap(target):
    choice = random.randrange(3)
    if choice == 0:
        return app(atom("I"), target)
    if choice == 1:
        return app(app(atom("K"), target), random_normal())
    return app(app(app(atom("S"), atom("K")), atom("K")), target)


def bck_wrap(target):
    choice = random.randrange(3)
    if choice == 0:
        return app(app(atom("K"), target), random_normal())
    if choice == 1:
        return app(app(app(atom("C"), atom("K")), random_normal()), target)
    # B (K target) f x -> K target (f x) -> target.
    return app(app(app(atom("B"), app(atom("K"), target)), random_normal()),
               random_normal())


def wrapped_term(system):
    allowed = frozenset(system)
    while True:
        target = random_normal()
        term = target
        wrapper = ski_wrap if system == "SKI" else bck_wrap
        for _ in range(random.randint(1, 4)):
            term = wrapper(term)
        outcome = normalize(term, allowed)
        if outcome is not None and 1 <= len(outcome[0]) <= 8:
            return term, target, outcome[0]


def trace_steps(term, trace, normal):
    steps = [step("REWRITE", term_text(term))]
    for _, after, rule in trace:
        left, right = RULE_TEXT[rule]
        steps.append(step("COMB_RULE", left, right))
        steps.append(step("REWRITE", term_text(after)))
    steps.append(step("CHECK", "normal form", term_text(normal),
                      f"steps {len(trace)}"))
    return steps


class CombinatoryLogicGenerator(ProblemGenerator):
    """Generate terminating leftmost-outermost combinator reductions."""

    VARIANTS = ("ski_reduce", "bck", "define_by_ski", "normal_form_count")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _reduce(self, system, variant):
        term, _, trace = wrapped_term(system)
        allowed = frozenset(system)
        _, normal = normalize(term, allowed)
        rules = ("I x → x; K x y → x; S x y z → x z (y z)"
                 if system == "SKI" else
                 "B x y z → x (y z); C x y z → x z y; K x y → x")
        problem = (f"Rule system {system}: {rules}. Term: {term_text(term)}. "
                   "Policy: contract the leftmost-outermost redex first. "
                   f"{random.choice(QUERIES[variant])}")
        return problem, trace_steps(term, trace, normal), \
            f"normal form = {term_text(normal)}"

    def _define_by_ski(self):
        argument = random_normal()
        term = app(app(app(atom("S"), atom("K")), atom("K")), argument)
        trace, normal = normalize(term, frozenset("SKI"))
        problem = ("Definition proposal: I = S K K. Rules: "
                   "S x y z → x z (y z); K x y → x. "
                   f"Argument: {term_text(argument)}. Application term: "
                   f"{term_text(term)}. Policy: contract leftmost-outermost. "
                   f"{random.choice(QUERIES['define_by_ski'])}")
        answer = (f"S K K acts as I; normal form = {term_text(normal)}")
        return problem, trace_steps(term, trace, normal), answer

    def _normal_form_count(self):
        system = random.choice(("SKI", "BCK"))
        term, _, trace = wrapped_term(system)
        _, normal = normalize(term, frozenset(system))
        rules = ("I x → x; K x y → x; S x y z → x z (y z)"
                 if system == "SKI" else
                 "B x y z → x (y z); C x y z → x z y; K x y → x")
        problem = (f"Rule system {system}: {rules}. Term: {term_text(term)}. "
                   "Policy: contract the leftmost-outermost redex first. "
                   f"{random.choice(QUERIES['normal_form_count'])}")
        answer = (f"normal form = {term_text(normal)}; "
                  f"steps = {len(trace)}")
        return problem, trace_steps(term, trace, normal), answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "ski_reduce":
            problem, steps, answer = self._reduce("SKI", variant)
        elif variant == "bck":
            problem, steps, answer = self._reduce("BCK", variant)
        elif variant == "define_by_ski":
            problem, steps, answer = self._define_by_ski()
        else:
            problem, steps, answer = self._normal_form_count()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"combinatory_logic_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

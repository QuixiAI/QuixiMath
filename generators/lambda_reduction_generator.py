import random

from base_generator import ProblemGenerator
from helpers import step, jid


VAR_POOL = "abcdefghkmnpqrst"
FRESH_ORDER = ["z", "w", "v", "u"]

MAX_BETA = 5
MAX_TERM_TEXT = 84
MAX_NF_TEXT = 64

RENAME_RULE = ("Rename a captured bound variable to the first unused name "
               "from z, w, v, u.")

NAMES = [
    "Ana", "Bo", "Cleo", "Devi", "Emil", "Farid", "Greta", "Hana",
    "Ivan", "Jun", "Kira", "Liam", "Mira", "Noor", "Omar", "Pia",
]

PROBLEM_TEMPLATES = [
    "Reduce the lambda term {term} by leftmost-outermost beta reduction. {rule}",
    ("Normalize {term} using leftmost-outermost beta reduction; alpha-rename "
     "when needed. {rule}"),
    ("Find the normal form of {term}, using capture-avoiding substitution and "
     "leftmost-outermost order. {rule}"),
    ("{who} is reducing {term} by hand, always contracting the "
     "leftmost-outermost redex. What normal form does {who} reach? {rule}"),
    ("Apply beta reduction repeatedly to {term}, contracting the "
     "leftmost-outermost redex each time, and state the normal form. {rule}"),
]


def text(term):
    """Fully parenthesised rendering: every abstraction and every application
    carries its own parentheses, so the string parses only one way."""
    if term[0] == "var":
        return term[1]
    if term[0] == "abs":
        return f"(lambda {term[1]}. {text(term[2])})"
    return f"({text(term[1])} {text(term[2])})"


def top(term):
    """Rendering at the root, where an outer abstraction needs no parens."""
    if term[0] == "abs":
        return f"lambda {term[1]}. {text(term[2])}"
    return text(term)


def free_vars(term):
    if term[0] == "var":
        return {term[1]}
    if term[0] == "app":
        return free_vars(term[1]) | free_vars(term[2])
    return free_vars(term[2]) - {term[1]}


def rename_bound(term, old, new):
    if term[0] == "var":
        return ("var", new) if term[1] == old else term
    if term[0] == "app":
        return ("app", rename_bound(term[1], old, new),
                rename_bound(term[2], old, new))
    if term[1] == old:
        return term
    return ("abs", term[1], rename_bound(term[2], old, new))


def fresh_name(used):
    for name in FRESH_ORDER:
        if name not in used:
            return name
    raise ValueError(f"no fresh name available for {sorted(used)}")


def substitute(term, var, value, log):
    """Capture-avoiding substitution; appends (before, after) rename texts."""
    if term[0] == "var":
        return value if term[1] == var else term
    if term[0] == "app":
        return ("app", substitute(term[1], var, value, log),
                substitute(term[2], var, value, log))
    param, body = term[1], term[2]
    if param == var:
        return term
    if param in free_vars(value) and var in free_vars(body):
        used = free_vars(body) | free_vars(value) | {var}
        new_param = fresh_name(used)
        renamed = rename_bound(body, param, new_param)
        log.append((top(("abs", param, body)),
                    top(("abs", new_param, renamed))))
        body, param = renamed, new_param
    return ("abs", param, substitute(body, var, value, log))


def count_var(term, var):
    if term[0] == "var":
        return 1 if term[1] == var else 0
    if term[0] == "app":
        return count_var(term[1], var) + count_var(term[2], var)
    if term[1] == var:
        return 0
    return count_var(term[2], var)


def reduce_once(term):
    """One leftmost-outermost beta step; returns (whole, info) or None."""
    if term[0] == "app":
        if term[1][0] == "abs":
            log = []
            local = substitute(term[1][2], term[1][1], term[2], log)
            info = {
                "fn": term[1],
                "arg": term[2],
                "local": local,
                "renames": log,
                "uses": count_var(term[1][2], term[1][1]),
            }
            return local, info
        left = reduce_once(term[1])
        if left is not None:
            return ("app", left[0], term[2]), left[1]
        right = reduce_once(term[2])
        if right is not None:
            return ("app", term[1], right[0]), right[1]
        return None
    if term[0] == "abs":
        inner = reduce_once(term[2])
        if inner is not None:
            return ("abs", term[1], inner[0]), inner[1]
    return None


def reduce_once_inner(term):
    """One applicative-order (innermost) beta step; used only to confirm the
    term is strongly normalizing before it is handed to a student."""
    if term[0] == "app":
        left = reduce_once_inner(term[1])
        if left is not None:
            return ("app", left, term[2])
        right = reduce_once_inner(term[2])
        if right is not None:
            return ("app", term[1], right)
        if term[1][0] == "abs":
            return substitute(term[1][2], term[1][1], term[2], [])
        return None
    if term[0] == "abs":
        inner = reduce_once_inner(term[2])
        if inner is not None:
            return ("abs", term[1], inner)
    return None


def normalize(term, limit=MAX_BETA + 1):
    """Leftmost-outermost normalization trace, or None if it is too long."""
    trace = []
    current = term
    for _ in range(limit):
        outcome = reduce_once(current)
        if outcome is None:
            return trace, current
        current, info = outcome
        info["after"] = current
        trace.append(info)
    return None


def inner_terminates(term, limit=18):
    current = term
    for _ in range(limit):
        nxt = reduce_once_inner(current)
        if nxt is None:
            return True
        current = nxt
    return False


def random_subterm(size, scope, frees, binders):
    pool = scope + frees
    if size <= 1 or random.random() < 0.22:
        return ("var", random.choice(pool))
    roll = random.random()
    if roll < 0.38:
        name = random.choice(binders)
        return ("abs", name, random_subterm(size - 1, scope + [name], frees,
                                            binders))
    left_size = random.randint(1, max(1, size - 2))
    right_size = max(1, size - 1 - left_size)
    return ("app", random_subterm(left_size, scope, frees, binders),
            random_subterm(right_size, scope, frees, binders))


def random_redex_term():
    names = random.sample(VAR_POOL, random.randint(3, 6))
    frees = names[:random.randint(1, 2)]
    binders = names
    binder = random.choice(binders)
    body = random_subterm(random.randint(2, 6), [binder], frees, binders)
    arg = random_subterm(random.randint(1, 4), [], frees, binders)
    if random.random() < 0.3:
        inner = random.choice(binders)
        arg = ("abs", inner, random_subterm(random.randint(1, 2),
                                            [inner], frees, binders))
    term = ("app", ("abs", binder, body), arg)
    if random.random() < 0.4:
        term = ("app", term, random_subterm(random.randint(1, 2), [], frees,
                                            binders))
    return term


def classify(trace):
    if any(info["renames"] for info in trace):
        return "alpha"
    if any(info["uses"] >= 2 for info in trace):
        return "duplicate"
    if any(info["uses"] == 0 for info in trace):
        return "constant"
    return "identity"


def sample_term(variant):
    """A random term whose leftmost-outermost trace lands in `variant`."""
    while True:
        term = random_redex_term()
        if len(text(term)) > MAX_TERM_TEXT:
            continue
        outcome = normalize(term)
        if outcome is None:
            continue
        trace, normal = outcome
        if not 1 <= len(trace) <= MAX_BETA:
            continue
        if len(text(normal)) > MAX_NF_TEXT:
            continue
        if not inner_terminates(term):
            continue
        if classify(trace) != variant:
            continue
        return term, trace, normal


class LambdaReductionGenerator(ProblemGenerator):
    """
    Lambda-calculus beta-reduction traces on randomly built terms, reduced in
    leftmost-outermost order with capture-avoiding substitution.

    Variants name the phenomenon the trace exhibits: `identity` (each bound
    variable used exactly once), `constant` (an argument is discarded),
    `duplicate` (an argument is copied), `alpha` (capture forces a rename).

    Op-codes used:
    - LAMBDA_SETUP / BETA / ALPHA_RENAME / SUBSTITUTE / REWRITE / NO_REDEX
    - Z: normal form under the stated strategy
    """

    VARIANTS = ["identity", "constant", "alpha", "duplicate"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        term, trace, normal = sample_term(variant)
        steps = [step("LAMBDA_SETUP", text(term), "leftmost-outermost")]
        for info in trace:
            steps.append(step("BETA", f"{text(info['fn'])} applied to "
                                      f"{text(info['arg'])}"))
            for before, after in info["renames"]:
                steps.append(step("ALPHA_RENAME", before, after))
            steps.append(step("SUBSTITUTE",
                              f"{info['fn'][1]}:={text(info['arg'])} in "
                              f"{top(info['fn'][2])}",
                              top(info["local"])))
            steps.append(step("REWRITE", top(info["after"])))
        steps.append(step("NO_REDEX", top(normal), "no beta redex remains"))
        answer = f"normal form = {top(normal)}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            term=text(term), rule=RENAME_RULE, who=random.choice(NAMES))
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"lambda_reduction_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

import random

from base_generator import ProblemGenerator
from helpers import step, jid


CASES = {
    "simple": ("f(X,a)", "f(b,Y)"),
    "nested": ("g(X,h(Y))", "g(h(a),h(b))"),
    "occurs": ("X", "f(X)"),
}


PROBLEM_TEMPLATES = [
    "Unify terms {left} and {right} with occurs-check. Report the MGU or failure.",
    "Find the most general unifier of {left} and {right}; use occurs-check.",
    "Run first-order unification on {left} = {right}, including occurs-check.",
]


class Var:
    def __init__(self, name):
        self.name = name


class Func:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []


def split_args(text):
    out = []
    depth = 0
    start = 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(text[start:i])
            start = i + 1
    out.append(text[start:])
    return out


def parse_term(text):
    text = text.strip()
    if "(" not in text:
        return Var(text) if text and text[0].isupper() else Func(text)
    name, rest = text.split("(", 1)
    body = rest[:-1]
    return Func(name, [parse_term(part) for part in split_args(body)])


def term_text(term):
    if isinstance(term, Var):
        return term.name
    if not term.args:
        return term.name
    return f"{term.name}(" + ",".join(term_text(arg) for arg in term.args) + ")"


def apply_subst(term, subst):
    if isinstance(term, Var):
        if term.name in subst:
            return apply_subst(subst[term.name], subst)
        return term
    return Func(term.name, [apply_subst(arg, subst) for arg in term.args])


def occurs(var, term, subst):
    term = apply_subst(term, subst)
    if isinstance(term, Var):
        return term.name == var
    return any(occurs(var, arg, subst) for arg in term.args)


def subst_text(subst):
    if not subst:
        return "{}"
    return "{" + ", ".join(f"{name}={term_text(apply_subst(term, subst))}"
                           for name, term in sorted(subst.items())) + "}"


class UnificationGenerator(ProblemGenerator):
    """
    First-order term unification with occurs-check.

    Op-codes used:
    - UNIFY_SETUP / UNIFY_PAIR / UNIFY_DECOMPOSE / UNIFY_BIND
    - OCCURS_CHECK / APPLY_SUBST / UNIFY_FAIL
    - Z: MGU or occurs-check failure
    """

    VARIANTS = ["simple", "nested", "occurs"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        left, right = CASES[variant]
        steps = [step("UNIFY_SETUP", left, right, "occurs-check")]
        ok, subst, reason = self._unify(parse_term(left), parse_term(right),
                                        steps)
        if ok:
            answer = f"MGU = {subst_text(subst)}"
        else:
            answer = f"failure; {reason}"
        problem = random.choice(PROBLEM_TEMPLATES).format(left=left,
                                                          right=right)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"unification_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _unify(self, left, right, steps):
        subst = {}
        work = [(left, right)]
        while work:
            a, b = work.pop(0)
            a = apply_subst(a, subst)
            b = apply_subst(b, subst)
            steps.append(step("UNIFY_PAIR", term_text(a), term_text(b)))
            if term_text(a) == term_text(b):
                steps.append(step("APPLY_SUBST", subst_text(subst)))
                continue
            if isinstance(a, Var):
                if occurs(a.name, b, subst):
                    reason = f"occurs-check {a.name} in {term_text(b)}"
                    steps.append(step("OCCURS_CHECK", a.name, term_text(b),
                                      "fail"))
                    steps.append(step("UNIFY_FAIL", reason))
                    return False, subst, reason
                subst[a.name] = b
                steps.append(step("UNIFY_BIND", a.name, term_text(b),
                                  subst_text(subst)))
            elif isinstance(b, Var):
                work.insert(0, (b, a))
            elif a.name == b.name and len(a.args) == len(b.args):
                steps.append(step("UNIFY_DECOMPOSE", a.name,
                                  f"{len(a.args)} arguments"))
                work = list(zip(a.args, b.args)) + work
            else:
                reason = f"clash {term_text(a)} vs {term_text(b)}"
                steps.append(step("UNIFY_FAIL", reason))
                return False, subst, reason
        return True, subst, ""

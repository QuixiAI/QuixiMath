"""Simple-type inference, application checks, and PM type levels.

Variants: ``simple_type_inference``, ``typing_check``, and ``pm_levels``.
Op-codes: ``TYPE_ASSIGN``, ``TYPE_ABS``, ``TYPE_APP``, ``LEVEL``,
``MEMBERSHIP_OK``, ``MEMBERSHIP_BAD``, ``CHECK``, and ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True
TERM_NAMES = tuple("abcdefghjkmnpqrstuvwxyz")
TYPE_NAMES = tuple("ABCDEFGHJKLMN")

QUERIES = {
    "simple_type_inference": (
        "Infer the principal simple type.",
        "Determine the term's most general simple type.",
        "Assign fresh type variables and solve the application constraints.",
        "Compute the canonical right-associative arrow type.",
        "Find the principal type of the lambda term.",
    ),
    "typing_check": (
        "Decide whether the application type-checks and give its type when valid.",
        "Check every application against the declarations.",
        "Determine whether the term is well-typed.",
        "Unify the declared input and output types through the term.",
        "Report the typing verdict with its type or first mismatch.",
    ),
    "pm_levels": (
        "Apply the PM type-level rule to the expression.",
        "Determine whether the membership or class formation is well-typed.",
        "Check the displayed levels and report the exact verdict.",
        "Use type(y) = type(x) + 1 for membership.",
        "Evaluate the type-level constraint in the stated expression.",
    ),
}


def var(name):
    return ("var", name)


def abs_term(name, body):
    return ("abs", name, body)


def app_term(left, right):
    return ("app", left, right)


def term_text(term):
    if term[0] == "var":
        return term[1]
    if term[0] == "abs":
        return f"(lambda {term[1]}. {term_text(term[2])})"
    return f"({term_text(term[1])} {term_text(term[2])})"


def arrow(left, right):
    return ("arrow", left, right)


class Inferencer:
    def __init__(self):
        self.next_id = 0
        self.substitution = {}
        self.events = []

    def fresh(self):
        value = ("typevar", self.next_id)
        self.next_id += 1
        return value

    def prune(self, value):
        if value[0] == "typevar" and value[1] in self.substitution:
            self.substitution[value[1]] = self.prune(self.substitution[value[1]])
            return self.substitution[value[1]]
        if value[0] == "arrow":
            return arrow(self.prune(value[1]), self.prune(value[2]))
        return value

    def occurs(self, identifier, value):
        value = self.prune(value)
        if value[0] == "typevar":
            return value[1] == identifier
        return value[0] == "arrow" and (
            self.occurs(identifier, value[1]) or
            self.occurs(identifier, value[2]))

    def unify(self, left, right):
        left, right = self.prune(left), self.prune(right)
        if left == right:
            return
        if left[0] == "typevar":
            if self.occurs(left[1], right):
                raise ValueError("recursive type")
            self.substitution[left[1]] = right
            return
        if right[0] == "typevar":
            self.unify(right, left)
            return
        if left[0] == right[0] == "arrow":
            self.unify(left[1], right[1])
            self.unify(left[2], right[2])
            return
        raise ValueError("types do not unify")

    def infer(self, term, environment=None):
        environment = {} if environment is None else dict(environment)
        kind = term[0]
        if kind == "var":
            return environment[term[1]]
        if kind == "abs":
            argument_type = self.fresh()
            environment[term[1]] = argument_type
            self.events.append(("assign", term[1], argument_type))
            body_type = self.infer(term[2], environment)
            result = arrow(argument_type, body_type)
            self.events.append(("abs", f"lambda {term[1]}", result))
            return result
        function_type = self.infer(term[1], environment)
        argument_type = self.infer(term[2], environment)
        result_type = self.fresh()
        self.unify(function_type, arrow(argument_type, result_type))
        self.events.append(("app", term_text(term), result_type))
        return result_type


def type_variables(value, inferencer, found=None):
    found = [] if found is None else found
    value = inferencer.prune(value)
    if value[0] == "typevar" and value[1] not in found:
        found.append(value[1])
    elif value[0] == "arrow":
        type_variables(value[1], inferencer, found)
        type_variables(value[2], inferencer, found)
    return found


def type_text(value, inferencer, names=None, top=True):
    value = inferencer.prune(value)
    names = names or {}
    if value[0] == "typevar":
        return names[value[1]]
    left = type_text(value[1], inferencer, names, False)
    right = type_text(value[2], inferencer, names, True)
    if inferencer.prune(value[1])[0] == "arrow":
        left = f"({left})"
    rendered = f"{left} → {right}"
    return rendered


def principal_type(term):
    inferencer = Inferencer()
    result = inferencer.infer(term)
    identifiers = type_variables(result, inferencer)
    names = {identifier: chr(ord("a") + index)
             for index, identifier in enumerate(identifiers)}
    rendered = type_text(result, inferencer, names)
    steps = []
    for kind, label, value in inferencer.events:
        event_type = type_text(value, inferencer, names)
        if kind == "assign":
            steps.append(step("TYPE_ASSIGN", label, event_type))
        elif kind == "abs":
            steps.append(step("TYPE_ABS", label, event_type))
        else:
            steps.append(step("TYPE_APP", label, "unify", event_type))
    return rendered, steps


def lambda_template():
    names = random.sample(TERM_NAMES, 8)
    x, y, f, g = names[:4]
    identity = abs_term(x, var(x))
    constant = abs_term(x, abs_term(y, var(x)))
    apply = abs_term(f, abs_term(x, app_term(var(f), var(x))))
    twice = abs_term(
        f,
        abs_term(x, app_term(var(f), app_term(var(f), var(x)))),
    )
    compose = abs_term(
        f,
        abs_term(
            g,
            abs_term(x, app_term(var(f), app_term(var(g), var(x)))),
        ),
    )
    flip = abs_term(
        f,
        abs_term(
            x,
            abs_term(y, app_term(app_term(var(f), var(y)), var(x))),
        ),
    )
    substitute = abs_term(
        f,
        abs_term(
            g,
            abs_term(
                x,
                app_term(
                    app_term(var(f), var(x)),
                    app_term(var(g), var(x)),
                ),
            ),
        ),
    )
    templates = (
        identity,
        constant,
        apply,
        twice,
        compose,
        flip,
        substitute,
    )
    term = random.choice(templates)
    wrapper_count = random.randrange(5)
    for name in names[4:4 + wrapper_count]:
        term = abs_term(name, term)
    return term


def declared_type_text(value, top=True):
    if isinstance(value, str):
        return value
    left = declared_type_text(value[0], False)
    right = declared_type_text(value[1], True)
    if not isinstance(value[0], str):
        left = f"({left})"
    return f"{left} → {right}"


class TypeTheoryGenerator(ProblemGenerator):
    """Generate simple-type and PM-level exercises."""

    VARIANTS = ("simple_type_inference", "typing_check", "pm_levels")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _simple_type_inference(self):
        term = lambda_template()
        answer, steps = principal_type(term)
        problem = (f"Lambda term: {term_text(term)}. Arrow types associate "
                   "to the right; name principal type variables a,b,c,... "
                   "in first-occurrence order. "
                   f"{random.choice(QUERIES['simple_type_inference'])}")
        steps.append(step("CHECK", "principal type", answer))
        return problem, steps, answer

    def _typing_check(self):
        term_names = random.sample(TERM_NAMES, 4)
        type_names = random.sample(TYPE_NAMES, 4)
        f, g, x, h = term_names
        a, b, c, d = type_names
        case = random.randrange(5)
        if case == 0:
            declarations = [(f, (a, b)), (x, a)]
            term, answer = app_term(var(f), var(x)), f"well-typed; type {b}"
            applications = [(term, "unify", b)]
        elif case == 1:
            declarations = [(f, (a, b)), (x, c)]
            term = app_term(var(f), var(x))
            answer = f"ill-typed (expected {a}, got {c})"
            applications = [(term, f"expected {a}", f"got {c}")]
        elif case == 2:
            declarations = [(f, (a, b)), (g, (b, c)), (x, a)]
            inner = app_term(var(f), var(x))
            term = app_term(var(g), inner)
            answer = f"well-typed; type {c}"
            applications = [(inner, "unify", b), (term, "unify", c)]
        elif case == 3:
            declarations = [(h, ((a, b), c)), (f, (a, b))]
            term = app_term(var(h), var(f))
            answer = f"well-typed; type {c}"
            applications = [(term, "unify", c)]
        else:
            declarations = [(x, a), (f, (a, b))]
            inner = app_term(var(f), var(x))
            term = app_term(inner, var(x))
            answer = f"ill-typed ({b} is not a function type)"
            applications = [(inner, "unify", b),
                            (term, f"function required", f"got {b}")]
        declarations_text = "; ".join(
            f"{name} : {declared_type_text(value)}"
            for name, value in declarations)
        problem = (f"Declarations: {declarations_text}. Term: "
                   f"{term_text(term)}. "
                   f"{random.choice(QUERIES['typing_check'])}")
        steps = [step("TYPE_ASSIGN", name, declared_type_text(value))
                 for name, value in declarations]
        for application, action, result in applications:
            steps.append(step("TYPE_APP", term_text(application), action, result))
        steps.append(step("CHECK", answer))
        return problem, steps, answer

    def _pm_levels(self):
        x, y = random.sample(TERM_NAMES, 2)
        level = random.randint(0, 100000)
        case = random.randrange(4)
        if case == 0:
            upper = level + 1
            problem = (f"PM type levels: type({x}) = {level}; type({y}) = "
                       f"{upper}. Expression: {x} ∈ {y}. "
                       f"{random.choice(QUERIES['pm_levels'])}")
            steps = [step("LEVEL", x, level), step("LEVEL", y, upper),
                     step("MEMBERSHIP_OK",
                          f"type({y}) = type({x}) + 1")]
            answer = (f"well-typed (type({y}) = type({x}) + 1)")
        elif case == 1:
            upper = level + random.choice((0, 2, 3))
            problem = (f"PM type levels: type({x}) = {level}; type({y}) = "
                       f"{upper}. Expression: {x} ∈ {y}. "
                       f"{random.choice(QUERIES['pm_levels'])}")
            steps = [step("LEVEL", x, level), step("LEVEL", y, upper),
                     step("MEMBERSHIP_BAD",
                          f"need {level + 1}", f"got {upper}")]
            answer = (f"ill-typed (type({y}) must be {level + 1}, "
                      f"not {upper})")
        elif case == 2:
            problem = (f"PM type levels: type({x}) = {level}. Expression: "
                       f"{x} ∈ {x}. {random.choice(QUERIES['pm_levels'])}")
            steps = [step("LEVEL", x, level),
                     step("MEMBERSHIP_BAD", f"type({x}) = type({x}) + 1",
                          "impossible")]
            answer = (f"ill-typed ({x} ∈ {x} needs type({x}) = "
                      f"type({x}) + 1)")
        else:
            class_level = level + 1
            problem = (f"PM type levels: type({x}) = {level}. Class "
                       f"expression: class({x} : φ({x})). "
                       f"{random.choice(QUERIES['pm_levels'])}")
            steps = [step("LEVEL", x, level),
                     step("LEVEL", f"class of {x}", class_level),
                     step("CHECK", f"class level = {level} + 1",
                          class_level)]
            answer = f"well-typed; type {class_level}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "simple_type_inference":
            problem, steps, answer = self._simple_type_inference()
        elif variant == "typing_check":
            problem, steps, answer = self._typing_check()
        else:
            problem, steps, answer = self._pm_levels()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"type_theory_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

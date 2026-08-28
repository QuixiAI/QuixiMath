"""Independent type inference and PM-level oracle for TypeTheoryGenerator."""
import random
import re
import unittest

from generators.type_theory_generator import TypeTheoryGenerator, QUERIES
from helpers import DELIM


def tokenize_term(text):
    return re.findall(r"lambda|[a-z]+|[().]", text)


def parse_term_at(tokens, position=0):
    if tokens[position] != "(":
        return ("var", tokens[position]), position + 1
    if tokens[position + 1] == "lambda":
        name = tokens[position + 2]
        assert tokens[position + 3] == "."
        body, position = parse_term_at(tokens, position + 4)
        assert tokens[position] == ")"
        return ("abs", name, body), position + 1
    left, position = parse_term_at(tokens, position + 1)
    right, position = parse_term_at(tokens, position)
    assert tokens[position] == ")"
    return ("app", left, right), position + 1


def parse_term(text):
    tokens = tokenize_term(text)
    term, position = parse_term_at(tokens)
    assert position == len(tokens), text
    return term


class IndependentInferencer:
    def __init__(self):
        self.counter = 0
        self.subst = {}

    def fresh(self):
        value = ("v", self.counter)
        self.counter += 1
        return value

    def resolve(self, value):
        if value[0] == "v" and value[1] in self.subst:
            self.subst[value[1]] = self.resolve(self.subst[value[1]])
            return self.subst[value[1]]
        if value[0] == "arr":
            return ("arr", self.resolve(value[1]), self.resolve(value[2]))
        return value

    def occurs(self, identifier, value):
        value = self.resolve(value)
        return (value == ("v", identifier) or
                value[0] == "arr" and
                (self.occurs(identifier, value[1]) or
                 self.occurs(identifier, value[2])))

    def unify(self, left, right):
        left, right = self.resolve(left), self.resolve(right)
        if left == right:
            return
        if left[0] == "v":
            if self.occurs(left[1], right):
                raise TypeError("recursive")
            self.subst[left[1]] = right
            return
        if right[0] == "v":
            self.unify(right, left)
            return
        if left[0] == right[0] == "arr":
            self.unify(left[1], right[1])
            self.unify(left[2], right[2])
            return
        raise TypeError((left, right))

    def infer(self, term, environment=None):
        environment = {} if environment is None else dict(environment)
        if term[0] == "var":
            return environment[term[1]]
        if term[0] == "abs":
            parameter = self.fresh()
            environment[term[1]] = parameter
            return ("arr", parameter, self.infer(term[2], environment))
        function = self.infer(term[1], environment)
        argument = self.infer(term[2], environment)
        result = self.fresh()
        self.unify(function, ("arr", argument, result))
        return result


def principal_text(term):
    inferencer = IndependentInferencer()
    inferred = inferencer.resolve(inferencer.infer(term))
    names = {}

    def render(value, left_side=False):
        value = inferencer.resolve(value)
        if value[0] == "v":
            if value[1] not in names:
                names[value[1]] = chr(ord("a") + len(names))
            return names[value[1]]
        left = render(value[1], True)
        right = render(value[2])
        if inferencer.resolve(value[1])[0] == "arr":
            left = f"({left})"
        return f"{left} → {right}"

    return render(inferred)


def tokenize_type(text):
    return re.findall(r"[A-Z]+|→|[()]", text)


def parse_type(text):
    tokens = tokenize_type(text)

    def parse(position=0):
        if tokens[position] == "(":
            left, position = parse(position + 1)
            assert tokens[position] == ")"
            position += 1
        else:
            left, position = ("atom", tokens[position]), position + 1
        if position < len(tokens) and tokens[position] == "→":
            right, position = parse(position + 1)
            return ("arr", left, right), position
        return left, position

    value, position = parse()
    assert position == len(tokens), text
    return value


def typed_check(term, environment):
    if term[0] == "var":
        return environment[term[1]]
    function = typed_check(term[1], environment)
    argument = typed_check(term[2], environment)
    if function[0] != "arr":
        raise TypeError(f"{type_render(function)} is not a function type")
    if function[1] != argument:
        raise ValueError((type_render(function[1]), type_render(argument)))
    return function[2]


def type_render(value):
    if value[0] == "atom":
        return value[1]
    left = type_render(value[1])
    if value[1][0] == "arr":
        left = f"({left})"
    return f"{left} → {type_render(value[2])}"


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "simple_type_inference":
        match = re.fullmatch(
            r"Lambda term: (.+)\. Arrow types associate to the right; name "
            r"principal type variables a,b,c,\.\.\. in first-occurrence order\.",
            body)
        assert match is not None, body
        term = parse_term(match.group(1))
        answer = principal_text(term)
        case = "inference"
    elif variant == "typing_check":
        match = re.fullmatch(r"Declarations: (.+)\. Term: (.+)\.", body)
        assert match is not None, body
        environment = {}
        for declaration in match.group(1).split("; "):
            name, type_string = declaration.split(" : ", 1)
            environment[name] = parse_type(type_string)
        term = parse_term(match.group(2))
        try:
            result = typed_check(term, environment)
            answer = f"well-typed; type {type_render(result)}"
            case = "valid"
        except ValueError as error:
            expected, got = error.args[0]
            answer = f"ill-typed (expected {expected}, got {got})"
            case = "mismatch"
        except TypeError as error:
            answer = f"ill-typed ({error})"
            case = "nonfunction"
    else:
        class_match = re.fullmatch(
            r"PM type levels: type\(([a-z]+)\) = (\d+)\. Class expression: "
            r"class\(\1 : φ\(\1\)\)\.", body)
        membership = re.fullmatch(
            r"PM type levels: type\(([a-z]+)\) = (\d+)(?:; type\(([a-z]+)\) "
            r"= (\d+))?\. Expression: ([a-z]+) ∈ ([a-z]+)\.", body)
        assert class_match or membership, body
        term = None
        if class_match:
            level = int(class_match.group(2))
            answer, case = f"well-typed; type {level + 1}", "class"
        else:
            first, first_level = membership.group(1), int(membership.group(2))
            second = membership.group(3) or first
            second_level = (int(membership.group(4))
                            if membership.group(4) else first_level)
            if first == second:
                answer = (f"ill-typed ({first} ∈ {first} needs type({first}) = "
                          f"type({first}) + 1)")
                case = "self"
            elif second_level == first_level + 1:
                answer = (f"well-typed (type({second}) = type({first}) + 1)")
                case = "valid_membership"
            else:
                answer = (f"ill-typed (type({second}) must be {first_level + 1}, "
                          f"not {second_level})")
                case = "invalid_membership"
    return {"variant": variant, "query": query, "answer": answer,
            "case": case, "term": term}


class TypeTheoryGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(316228)

    def test_output_contract(self):
        example = TypeTheoryGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = TypeTheoryGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_all_typing_and_level_cases_are_reachable(self):
        typing = TypeTheoryGenerator("typing_check")
        typing_cases = {oracle_parts(typing.generate())["case"]
                        for _ in range(300)}
        self.assertEqual(typing_cases, {"valid", "mismatch", "nonfunction"})
        levels = TypeTheoryGenerator("pm_levels")
        level_cases = {oracle_parts(levels.generate())["case"]
                       for _ in range(300)}
        self.assertEqual(level_cases,
                         {"class", "self", "valid_membership",
                          "invalid_membership"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in TypeTheoryGenerator.VARIANTS:
            generator = TypeTheoryGenerator(variant)
            seen_queries = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"type_theory_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TypeTheoryGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = TypeTheoryGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

"""Independent parsing, NNF conversion, and model checks for quantifier negation."""
import itertools
import random
import re
import unittest

from generators.quantifier_negation_generator import (
    QUERIES, QuantifierNegationGenerator,
)
from helpers import DELIM


TOKEN = re.compile(r"\s*(∀|∃|¬|∧|∨|→|\(|\)|,|[A-Za-z][A-Za-z0-9]*)")


class PredicateParser:
    """Independent parser for the generator's printed predicate fragment."""

    def __init__(self, text):
        self.text = text
        self.tokens = []
        position = 0
        while position < len(text):
            match = TOKEN.match(text, position)
            if match is None:
                raise AssertionError(f"bad token at {text[position:]!r}")
            self.tokens.append(match.group(1))
            position = match.end()
        self.index = 0

    def take(self, expected=None):
        if self.index >= len(self.tokens):
            raise AssertionError(f"unexpected end of {self.text!r}")
        token = self.tokens[self.index]
        self.index += 1
        if expected is not None:
            assert token == expected, (token, expected, self.text)
        return token

    def node(self):
        token = self.take()
        if token in ("∀", "∃"):
            variable = self.take()
            return (("forall" if token == "∀" else "exists"), variable,
                    self.node())
        if token == "¬":
            return ("not", self.node())
        if token == "(":
            left = self.node()
            operator = self.take()
            assert operator in ("∧", "∨", "→"), operator
            right = self.node()
            self.take(")")
            return ({"∧": "and", "∨": "or", "→": "imp"}[operator],
                    left, right)
        predicate = token
        self.take("(")
        arguments = [self.take()]
        while self.tokens[self.index] == ",":
            self.take(",")
            arguments.append(self.take())
        self.take(")")
        return ("atom", predicate, tuple(arguments))

    def parse(self):
        result = self.node()
        assert self.index == len(self.tokens), (self.tokens[self.index:], self.text)
        return result


def parse_formula(text):
    return PredicateParser(text).parse()


def render(node):
    kind = node[0]
    if kind == "atom":
        return f"{node[1]}({', '.join(node[2])})"
    if kind == "not":
        child = render(node[1])
        return f"¬{child}" if node[1][0] == "atom" else f"¬({child})"
    if kind in ("forall", "exists"):
        return f"{'∀' if kind == 'forall' else '∃'}{node[1]} {render(node[2])}"
    symbol = {"and": "∧", "or": "∨", "imp": "→"}[kind]
    return (f"({render(node[1])} "
            f"{symbol} "
            f"{render(node[2])})")


def negate_to_nnf(node):
    kind = node[0]
    if kind == "atom":
        return ("not", node)
    if kind == "not":
        return node[1]
    if kind == "forall":
        return ("exists", node[1], negate_to_nnf(node[2]))
    if kind == "exists":
        return ("forall", node[1], negate_to_nnf(node[2]))
    if kind == "and":
        return ("or", negate_to_nnf(node[1]), negate_to_nnf(node[2]))
    if kind == "or":
        return ("and", negate_to_nnf(node[1]), negate_to_nnf(node[2]))
    assert kind == "imp", node
    return ("and", node[1], negate_to_nnf(node[2]))


def predicate_arities(node):
    found = {}

    def visit(item):
        if item[0] == "atom":
            arity = len(item[2])
            assert found.setdefault(item[1], arity) == arity
        elif item[0] == "not":
            visit(item[1])
        elif item[0] in ("forall", "exists"):
            visit(item[2])
        else:
            visit(item[1])
            visit(item[2])

    visit(node)
    return found


def evaluate(node, domain, model, environment=None):
    environment = {} if environment is None else environment
    kind = node[0]
    if kind == "atom":
        values = tuple(environment[name] for name in node[2])
        return values in model[node[1]]
    if kind == "not":
        return not evaluate(node[1], domain, model, environment)
    if kind in ("forall", "exists"):
        results = []
        for value in domain:
            extended = dict(environment)
            extended[node[1]] = value
            results.append(evaluate(node[2], domain, model, extended))
        return all(results) if kind == "forall" else any(results)
    left = evaluate(node[1], domain, model, environment)
    right = evaluate(node[2], domain, model, environment)
    if kind == "and":
        return left and right
    if kind == "or":
        return left or right
    assert kind == "imp", node
    return (not left) or right


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def english_source(body):
    match = re.fullmatch(
        r"Sentence: (.+)\. Predicate key: ([A-Z])\((\w)\): \3 is "
        r"(?:a|an) (\w+); ([A-Z])\(\3\): \3 is (\w+)\.", body)
    assert match is not None, body
    sentence, first_name, variable, noun, second_name, adjective = match.groups()
    first = ("atom", first_name, (variable,))
    second = ("atom", second_name, (variable,))
    if sentence == f"Every {noun} is {adjective}":
        matrix = ("imp", first, second)
        return ("forall", variable, matrix)
    if sentence == f"No {noun} is {adjective}":
        matrix = ("imp", first, ("not", second))
        return ("forall", variable, matrix)
    if sentence == f"Some {noun} is {adjective}":
        return ("exists", variable, ("and", first, second))
    assert sentence == f"Some {noun} is not {adjective}", sentence
    return ("exists", variable, ("and", first, ("not", second)))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("symbolic", "nested"):
        match = re.fullmatch(r"Formula: (.+)\.", body)
        assert match is not None, body
        source = parse_formula(match.group(1))
    elif variant == "english":
        source = english_source(body)
    else:
        match = re.fullmatch(
            r"Domain: integers n with 2 ≤ n ≤ (\d+)\. "
            r"Claim: every prime n in the domain is odd\.", body)
        assert match is not None, body
        assert int(match.group(1)) >= 2
        source = ("forall", "n",
                  ("imp", ("atom", "Prime", ("n",)),
                   ("atom", "Odd", ("n",))))
    target = negate_to_nnf(source)
    answer = render(target)
    if variant == "with_counterexample":
        answer += "; n = 2"
    return {"variant": variant, "query": query, "source": source,
            "target": target, "answer": answer}


class QuantifierNegationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(140921)

    def test_output_contract(self):
        example = QuantifierNegationGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = QuantifierNegationGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_nnf_is_semantic_complement_in_random_finite_models(self):
        generator = QuantifierNegationGenerator()
        for _ in range(300):
            parts = oracle_parts(generator.generate())
            source, target = parts["source"], parts["target"]
            arities = predicate_arities(source)
            domain = tuple(range(random.randint(1, 3)))
            for _ in range(8):
                model = {}
                for name, arity in arities.items():
                    tuples = itertools.product(domain, repeat=arity)
                    model[name] = {values for values in tuples
                                   if random.choice((True, False))}
                self.assertEqual(evaluate(target, domain, model),
                                 not evaluate(source, domain, model))

    def test_trace_finishes_at_oracle_target(self):
        generator = QuantifierNegationGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            rewrites = [raw.split(DELIM)[1] for raw in example["steps"]
                        if raw.startswith(f"REWRITE{DELIM}")]
            self.assertEqual(rewrites, [render(parts["target"])])
            self.assertTrue(any(raw.startswith(f"NEG_QUANT{DELIM}")
                                for raw in example["steps"]))
            if parts["variant"] == "english":
                translated = next(raw.split(DELIM)[2]
                                  for raw in example["steps"]
                                  if raw.startswith(f"TRANSLATE{DELIM}"))
                self.assertEqual(parse_formula(translated), parts["source"])

    def test_counterexample_is_least_and_verified(self):
        generator = QuantifierNegationGenerator("with_counterexample")
        for _ in range(200):
            example = generator.generate()
            upper = int(re.search(r"≤ n ≤ (\d+)", example["problem"]).group(1))
            self.assertGreaterEqual(upper, 2)
            def is_prime(value):
                return (value >= 2 and all(value % divisor
                                           for divisor in range(
                                               2, int(value ** 0.5) + 1)))
            least = next(value for value in range(2, upper + 1)
                         if is_prime(value) and value % 2 == 0)
            self.assertEqual(least, 2)
            witness = next(raw.split(DELIM) for raw in example["steps"]
                           if raw.startswith(f"WITNESS{DELIM}"))
            self.assertEqual(witness, ["WITNESS", "n=2",
                                       "Prime(2)=T", "Odd(2)=F"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in QuantifierNegationGenerator.VARIANTS:
            generator = QuantifierNegationGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"quantifier_negation_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            QuantifierNegationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = QuantifierNegationGenerator()
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

"""Independent parser and reducer for CombinatoryLogicGenerator."""
import random
import re
import unittest

from generators.combinatory_logic_generator import CombinatoryLogicGenerator, QUERIES
from helpers import DELIM


def tokenize(text):
    return re.findall(r"[A-Za-z]+|[()]", text)


def parse_at(tokens, position=0):
    token = tokens[position]
    if token != "(":
        return ("atom", token), position + 1
    left, position = parse_at(tokens, position + 1)
    right, position = parse_at(tokens, position)
    assert tokens[position] == ")"
    return ("app", left, right), position + 1


def parse_term(text):
    tokens = tokenize(text)
    term, position = parse_at(tokens)
    assert position == len(tokens), text
    return term


def render(term):
    return term[1] if term[0] == "atom" else f"({render(term[1])} {render(term[2])})"


def independent_root(term, allowed):
    head, args = term, []
    while head[0] == "app":
        args.append(head[2])
        head = head[1]
    args.reverse()
    if head[0] != "atom" or head[1] not in allowed:
        return None
    rule = head[1]
    arity = 1 if rule == "I" else 2 if rule == "K" else 3
    if len(args) < arity:
        return None
    app = lambda x, y: ("app", x, y)
    if rule in ("I", "K"):
        result = args[0]
    elif rule == "S":
        result = app(app(args[0], args[2]), app(args[1], args[2]))
    elif rule == "B":
        result = app(args[0], app(args[1], args[2]))
    else:
        result = app(app(args[0], args[2]), args[1])
    for extra in args[arity:]:
        result = app(result, extra)
    return result, rule


def independent_step(term, allowed):
    root = independent_root(term, allowed)
    if root:
        return root
    if term[0] == "app":
        left = independent_step(term[1], allowed)
        if left:
            return ("app", left[0], term[2]), left[1]
        right = independent_step(term[2], allowed)
        if right:
            return ("app", term[1], right[0]), right[1]
    return None


def normalize(term, allowed):
    count = 0
    while True:
        outcome = independent_step(term, allowed)
        if outcome is None:
            return term, count
        term = outcome[0]
        count += 1
        assert count <= 8


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("ski_reduce", "bck", "normal_form_count"):
        match = re.fullmatch(
            r"Rule system (SKI|BCK): .+\. Term: (.+)\. Policy: contract "
            r"the leftmost-outermost redex first\.", body)
        assert match is not None, body
        system, term = match.group(1), parse_term(match.group(2))
        normal, count = normalize(term, frozenset(system))
        if variant == "normal_form_count":
            answer = f"normal form = {render(normal)}; steps = {count}"
        else:
            answer = f"normal form = {render(normal)}"
        argument = None
    else:
        match = re.fullmatch(
            r"Definition proposal: I = S K K\. Rules: .+\. Argument: "
            r"(.+)\. Application term: (.+)\. Policy: contract "
            r"leftmost-outermost\.", body)
        assert match is not None, body
        argument, term = parse_term(match.group(1)), parse_term(match.group(2))
        normal, count = normalize(term, frozenset("SKI"))
        assert normal == argument
        system = "SKI"
        answer = f"S K K acts as I; normal form = {render(normal)}"
    return {"variant": variant, "query": query, "system": system,
            "term": term, "normal": normal, "count": count,
            "argument": argument, "answer": answer}


class CombinatoryLogicGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(244949)

    def test_output_contract(self):
        example = CombinatoryLogicGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CombinatoryLogicGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_each_rewrite_is_one_leftmost_outermost_contraction(self):
        generator = CombinatoryLogicGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            current = parts["term"]
            pending_rule = None
            rewrites = 0
            for fields in (raw.split(DELIM) for raw in example["steps"][:-1]):
                if fields[0] == "COMB_RULE":
                    pending_rule = fields[1][0]
                elif fields[0] == "REWRITE":
                    rendered = parse_term(fields[1])
                    if rewrites == 0:
                        self.assertEqual(rendered, current)
                    else:
                        outcome = independent_step(current, frozenset(parts["system"]))
                        self.assertIsNotNone(outcome)
                        self.assertEqual(outcome[1], pending_rule)
                        self.assertEqual(rendered, outcome[0])
                        current = rendered
                    rewrites += 1
            self.assertEqual(current, parts["normal"])
            self.assertEqual(rewrites - 1, parts["count"])

    def test_all_terms_normalize_within_eight_steps(self):
        generator = CombinatoryLogicGenerator()
        for _ in range(500):
            parts = oracle_parts(generator.generate())
            self.assertLessEqual(parts["count"], 8)
            self.assertIsNone(independent_step(parts["normal"],
                                               frozenset(parts["system"])))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CombinatoryLogicGenerator.VARIANTS:
            generator = CombinatoryLogicGenerator(variant)
            seen_queries = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"combinatory_logic_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CombinatoryLogicGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CombinatoryLogicGenerator()
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

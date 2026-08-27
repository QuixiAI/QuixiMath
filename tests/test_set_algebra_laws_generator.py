"""Independent membership-table oracle for SetAlgebraLawsGenerator."""
import random
import re
import unittest

from generators.set_algebra_laws_generator import QUERIES, SetAlgebraLawsGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def logic_to_set(node, mapping):
    kind = node[0]
    if kind == "var":
        return ("name", mapping[node[1]])
    if kind == "const":
        return ("universe",) if node[1] else ("literal", frozenset())
    if kind == "not":
        return ("comp", logic_to_set(node[1], mapping))
    translated = {"and": "inter", "or": "union"}[kind]
    return (translated, logic_to_set(node[1], mapping),
            logic_to_set(node[2], mapping))


def render_set(node, top=True):
    kind = node[0]
    if kind == "name":
        return node[1]
    if kind == "universe":
        return "U"
    if kind == "literal":
        return "∅"
    if kind == "comp":
        return render_set(node[1], False) + "ᶜ"
    symbol = {"inter": "∩", "union": "∪"}[kind]
    text = f"{render_set(node[1], False)} {symbol} {render_set(node[2], False)}"
    return text if top else f"({text})"


def forced_distribution(source):
    assert source[0] == "inter"
    left, right = source[1], source[2]
    if left[0] == "union":
        return ("union", ("inter", left[1], right),
                ("inter", left[2], right))
    assert right[0] == "union"
    return ("union", ("inter", left, right[1]),
            ("inter", left, right[2]))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    names_match = re.match(
        r"Set names: (\w+), (\w+), (\w+) are arbitrary subsets of U\. ", body)
    assert names_match is not None, body
    names = list(names_match.group(1, 2, 3))
    rest = body[names_match.end():]
    if variant == "simplify":
        match = re.fullmatch(r"Expression: (.+)\. Target family: (.+)\.", rest)
        assert match is not None, rest
        source = oracle.parse_set_expression(match.group(1))
        family = [oracle.parse_set_expression(item)
                  for item in match.group(2).split("; ")]
        source_column = oracle.membership_column(source, names)
        matches = [item for item in family
                   if oracle.membership_column(item, names) == source_column]
        assert len(matches) == 1, matches
        target = matches[0]
    elif variant == "dual_of_logic":
        match = re.fullmatch(
            r"Correspondence: p↦(\w+), q↦(\w+)\. Logic identity: (.+) ≡ (.+)\. "
            r"Set expression: (.+)\.", rest)
        assert match is not None, rest
        mapping = {"p": match.group(1), "q": match.group(2)}
        logic_source = oracle.parse_formula(match.group(3))
        logic_target = oracle.parse_formula(match.group(4))
        source = oracle.parse_set_expression(match.group(5))
        self_source = logic_to_set(logic_source, mapping)
        assert source == self_source, (source, self_source)
        target = logic_to_set(logic_target, mapping)
    else:
        match = re.fullmatch(r"Expression: (.+)\.", rest)
        assert match is not None, rest
        source = oracle.parse_set_expression(match.group(1))
        target = forced_distribution(source)
    return {"variant": variant, "query": query, "names": names,
            "source": source, "target": target, "answer": render_set(target)}


class SetAlgebraLawsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(361091)

    def test_output_contract(self):
        example = SetAlgebraLawsGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SetAlgebraLawsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_law_rewrites_and_membership_columns_are_exact(self):
        generator = SetAlgebraLawsGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            rewrites = []
            checks = []
            for index, raw_step in enumerate(example["steps"]):
                fields = raw_step.split(DELIM)
                if fields[0] == "LAW":
                    before = oracle.parse_set_expression(fields[2])
                    after = oracle.parse_set_expression(fields[3])
                    self.assertEqual(oracle.membership_column(before, parts["names"]),
                                     oracle.membership_column(after, parts["names"]))
                    self.assertEqual(example["steps"][index + 1].split(DELIM)[0],
                                     "REWRITE")
                elif fields[0] == "REWRITE":
                    rewritten = oracle.parse_set_expression(fields[1])
                    self.assertEqual(
                        oracle.membership_column(rewritten, parts["names"]),
                        oracle.membership_column(parts["source"], parts["names"]),
                    )
                    rewrites.append(rewritten)
                elif fields[0] == "CHECK":
                    checks.append(fields)
            self.assertEqual(rewrites[-1], parts["target"])
            expected = "".join("1" if value else "0"
                               for value in oracle.membership_column(
                                   parts["source"], parts["names"]))
            self.assertEqual(checks,
                             [["CHECK", "membership columns", expected, expected]])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in SetAlgebraLawsGenerator.VARIANTS:
            generator = SetAlgebraLawsGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"set_algebra_laws_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SetAlgebraLawsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SetAlgebraLawsGenerator()
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

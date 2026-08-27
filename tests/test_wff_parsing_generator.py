"""Independent parser and conversion oracle for WFFParsingGenerator."""
import random
import re
import unittest

from generators.wff_parsing_generator import QUERIES, WFFParsingGenerator
from helpers import DELIM
from tests import foundations_oracle as logic_oracle


OP_TO_KIND = {"N": "not", "K": "and", "A": "or", "C": "imp", "E": "iff"}


def polish_parse(text, index=0):
    if index >= len(text):
        raise ValueError("ended early")
    token = text[index]
    if token.islower():
        return ("var", token), index + 1
    if token == "N":
        child, next_index = polish_parse(text, index + 1)
        return ("not", child), next_index
    if token in "KACE":
        left, next_index = polish_parse(text, index + 1)
        right, final_index = polish_parse(text, next_index)
        return (OP_TO_KIND[token], left, right), final_index
    raise ValueError(token)


def polish_text(node):
    if node[0] == "var":
        return node[1]
    if node[0] == "not":
        return "N" + polish_text(node[1])
    letter = {value: key for key, value in OP_TO_KIND.items()}[node[0]]
    return letter + polish_text(node[1]) + polish_text(node[2])


def formula_depth(node):
    if node[0] in ("var", "const"):
        return 0
    if node[0] == "not":
        return 1 + formula_depth(node[1])
    return 1 + max(formula_depth(node[1]), formula_depth(node[2]))


def formula_nodes(node):
    output = {node}
    if node[0] == "not":
        output |= formula_nodes(node[1])
    elif node[0] not in ("var", "const"):
        output |= formula_nodes(node[1]) | formula_nodes(node[2])
    return output


def main_symbol(node):
    return {"not": "¬", "and": "∧", "or": "∨", "imp": "→", "iff": "↔"}.get(
        node[0]
    )


def invalid_error(text):
    level = 0
    for index, char in enumerate(text, 1):
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
            if level < 0:
                return "unmatched parenthesis", index
    if level > 0:
        return "unmatched parenthesis", len(text) + 1
    doubled = re.search(r"[∧∨→↔]\s+([∧∨→↔])", text)
    if doubled:
        return "unexpected connective", doubled.start(1) + 1
    stripped = text.rstrip()
    if stripped and stripped[-1] in "∧∨→↔":
        return "dangling connective", len(stripped)
    return None


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            if problem.endswith(f" {query}"):
                return problem[:-(len(query) + 1)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "is_wff":
        match = re.fullmatch(
            r"Expression: (.+)\. Positions are 1-based; the end-of-input "
            r"position is one past the last character\.", body
        )
        assert match is not None, body
        expression = match.group(1)
        error = invalid_error(expression)
        if error:
            answer = f"not a wff ({error[0]} at position {error[1]})"
            node = None
        else:
            node = logic_oracle.parse_formula(expression)
            answer = (f"wff; main connective {main_symbol(node)}; "
                      f"depth {formula_depth(node)}; {len(formula_nodes(node))} subformulas")
        return {"variant": variant, "answer": answer, "node": node,
                "error": error, "query": query}
    if variant in ("main_connective", "depth_and_subformulas"):
        match = re.fullmatch(r"Formula: (.+)\.", body)
        assert match is not None, body
        node = logic_oracle.parse_formula(match.group(1))
        if variant == "main_connective":
            answer = f"main connective = {main_symbol(node)}; depth = {formula_depth(node)}"
        else:
            answer = (f"depth = {formula_depth(node)}; subformulas = "
                      f"{len(formula_nodes(node))}")
        return {"variant": variant, "answer": answer, "node": node,
                "query": query}
    if variant == "polish_to_infix":
        match = re.fullmatch(r"Polish formula: ([N KACEpqr]+)\.", body)
        assert match is not None, body
        polish = match.group(1).replace(" ", "")
        node, index = polish_parse(polish)
        assert index == len(polish)
        return {"variant": variant, "answer": logic_oracle.render(node),
                "node": node, "polish": polish, "query": query}
    match = re.fullmatch(r"Infix formula: (.+)\.", body)
    assert match is not None, body
    node = logic_oracle.parse_formula(match.group(1))
    return {"variant": variant, "answer": polish_text(node), "node": node,
            "polish": polish_text(node), "query": query}


class WFFParsingGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(425623)

    def test_output_contract(self):
        example = WFFParsingGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = WFFParsingGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_parse_metrics_errors_and_polish_steps(self):
        generator = WFFParsingGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            parse_errors = []
            polish_steps = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "PARSE" and fields[1] == "error":
                    parse_errors.append((fields[2], int(fields[3].split()[1])))
                elif fields[0] == "POLISH":
                    polish_steps.append(fields[1])
                elif fields[0] == "DEPTH" and parts["node"] is not None:
                    self.assertEqual(int(fields[1]), formula_depth(parts["node"]))
            if parts.get("error"):
                self.assertEqual(parse_errors, [parts["error"]])
            if parts["variant"] == "infix_to_polish":
                self.assertEqual(polish_steps, [parts["polish"]])

    def test_all_variants_five_phrasings_and_wff_outcomes_are_reachable(self):
        for variant in WFFParsingGenerator.VARIANTS:
            generator = WFFParsingGenerator(variant)
            seen_queries = set()
            wff_outcomes = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"wff_parsing_{variant}")
                seen_queries.add(parts["query"])
                if variant == "is_wff":
                    wff_outcomes.add(parts["node"] is not None)
            self.assertEqual(seen_queries, set(QUERIES[variant]))
            if variant == "is_wff":
                self.assertEqual(wff_outcomes, {False, True})

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            WFFParsingGenerator("bogus")

    def test_pipe_safety_and_canonical_valid_formulas(self):
        generator = WFFParsingGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            if parts["node"] is not None and parts["variant"] != "polish_to_infix":
                rendered = logic_oracle.render(parts["node"])
                self.assertTrue(logic_oracle.is_canonical_formula(rendered))
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

"""Independent tuple-AST tableau engine and truth-table oracle."""
import random
import re
import unittest

from generators.semantic_tableau_generator import QUERIES, SemanticTableauGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def nnf(node, negated=False):
    kind = node[0]
    if kind == "var":
        return ("not", node) if negated else node
    if kind == "const":
        return ("const", node[1] != negated)
    if kind == "not":
        return nnf(node[1], not negated)
    if kind == "imp":
        expanded = ("or", ("not", node[1]), node[2])
        return nnf(expanded, negated)
    if kind == "and":
        output = "or" if negated else "and"
    else:
        assert kind == "or", node
        output = "and" if negated else "or"
    return (output, nnf(node[1], negated), nnf(node[2], negated))


def literal(node):
    if node[0] == "var":
        return node[1], True
    if node[0] == "not" and node[1][0] == "var":
        return node[1][1], False
    return None


def contradiction(branch):
    seen = {}
    for item in branch["formulas"]:
        value = literal(item["formula"])
        if value is None:
            continue
        if value[0] in seen and seen[value[0]] != value[1]:
            return value[0]
        seen[value[0]] = value[1]
    return None


def assignment_text(assignment):
    return ", ".join(f"{name}={'T' if assignment[name] else 'F'}"
                     for name in sorted(assignment))


def branch_assignment(branch, names):
    result = {name: False for name in names}
    for item in branch["formulas"]:
        value = literal(item["formula"])
        if value:
            result[value[0]] = value[1]
    return result


def independent_tableau(root, names):
    line_number = 2
    branches = [{"id": "1", "closed": False,
                 "formulas": [{"line": 1, "formula": root,
                               "expanded": False}]}]
    trace = [["TABLEAU_ROOT", oracle.render(root)]]

    def close_new():
        for branch in branches:
            if branch["closed"]:
                continue
            name = contradiction(branch)
            if name:
                branch["closed"] = True
                trace.append(["BRANCH_CLOSE", branch["id"], f"{name}, ¬{name}"])

    close_new()
    while True:
        selected = None
        for rule, kind in (("ALPHA", "and"), ("BETA", "or")):
            candidates = []
            for branch_index, branch in enumerate(branches):
                if branch["closed"]:
                    continue
                for item_index, item in enumerate(branch["formulas"]):
                    if not item["expanded"] and item["formula"][0] == kind:
                        candidates.append((item["line"], branch_index,
                                           item_index, rule))
            if candidates:
                selected = min(candidates, key=lambda value: (value[0], value[1]))
                break
        if selected is None:
            break
        _, branch_index, item_index, rule = selected
        branch = branches[branch_index]
        item = branch["formulas"][item_index]
        item["expanded"] = True
        formula = item["formula"]
        if rule == "ALPHA":
            first_line, second_line = line_number, line_number + 1
            line_number += 2
            branch["formulas"].extend([
                {"line": first_line, "formula": formula[1], "expanded": False},
                {"line": second_line, "formula": formula[2], "expanded": False},
            ])
            trace.append(["ALPHA", f"line {item['line']}",
                          f"{first_line}: {oracle.render(formula[1])}; "
                          f"{second_line}: {oracle.render(formula[2])}"])
        else:
            left_line, right_line = line_number, line_number + 1
            line_number += 2
            common = [dict(value) for value in branch["formulas"]]
            left = {"id": branch["id"] + "L", "closed": False,
                    "formulas": [dict(value) for value in common] + [
                        {"line": left_line, "formula": formula[1],
                         "expanded": False}]}
            right = {"id": branch["id"] + "R", "closed": False,
                     "formulas": [dict(value) for value in common] + [
                         {"line": right_line, "formula": formula[2],
                          "expanded": False}]}
            branches[branch_index:branch_index + 1] = [left, right]
            trace.append(["BETA", f"line {item['line']}",
                          f"{left['id']}: {left_line}: {oracle.render(formula[1])}",
                          f"{right['id']}: {right_line}: {oracle.render(formula[2])}"])
        close_new()
    for branch in branches:
        if not branch["closed"]:
            trace.append(["BRANCH_OPEN", branch["id"],
                          assignment_text(branch_assignment(branch, names))])
    return trace, branches


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"Formula: (.+)\. Task: (.+)\. Policy: expand α before β; within a "
        r"rule class use the oldest line first and the leftmost branch first\.",
        body)
    assert match is not None, body
    source = oracle.parse_formula(match.group(1))
    names = oracle.formula_variables(source)
    root = nnf(source, negated=(variant in ("validity", "countermodel")))
    trace, branches = independent_tableau(root, names)
    open_branches = [branch for branch in branches if not branch["closed"]]
    if not open_branches:
        answer = ("closed; valid" if variant in ("validity", "countermodel")
                  else "closed; unsatisfiable")
        assignment = None
    else:
        assignment = branch_assignment(open_branches[0], names)
        if variant == "satisfiability":
            answer = f"open; satisfiable; model {assignment_text(assignment)}"
        else:
            answer = f"open; countermodel {assignment_text(assignment)}"
    return {"variant": variant, "query": query, "source": source,
            "root": root, "names": names, "trace": trace,
            "branches": branches, "assignment": assignment, "answer": answer}


class SemanticTableauGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(476219)

    def test_output_contract(self):
        example = SemanticTableauGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SemanticTableauGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_trace_exactly_matches_independent_expansion_policy(self):
        generator = SemanticTableauGenerator()
        structural = {"TABLEAU_ROOT", "ALPHA", "BETA", "BRANCH_CLOSE",
                      "BRANCH_OPEN"}
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            emitted = [raw.split(DELIM) for raw in example["steps"]
                       if raw.split(DELIM)[0] in structural]
            self.assertEqual(emitted, parts["trace"])

    def test_open_assignment_has_required_source_truth_value(self):
        generator = SemanticTableauGenerator()
        for _ in range(300):
            parts = oracle_parts(generator.generate())
            if parts["assignment"] is None:
                rows = oracle.all_assignments(parts["names"])
                values = [oracle.eval_formula(parts["source"], row) for row in rows]
                if parts["variant"] == "satisfiability":
                    self.assertFalse(any(values))
                else:
                    self.assertTrue(all(values))
            else:
                value = oracle.eval_formula(parts["source"], parts["assignment"])
                self.assertEqual(value, parts["variant"] == "satisfiability")

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in SemanticTableauGenerator.VARIANTS:
            generator = SemanticTableauGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"semantic_tableau_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SemanticTableauGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SemanticTableauGenerator()
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

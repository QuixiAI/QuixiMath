"""Independent eight-row oracle for set identity membership tables."""
import random
import re
import unittest

from generators.set_identity_membership_table_generator import (
    QUERIES, SetIdentityMembershipTableGenerator,
)
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def row_text(row, spaced=False):
    if spaced:
        return ", ".join(
            f"x {'∈' if row[name] else '∉'} {name}" for name in sorted(row))
    return ", ".join(
        f"x{'∈' if row[name] else '∉'}{name}" for name in sorted(row))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"Set names: (\w+), (\w+), (\w+) are arbitrary subsets of U\. "
        r"Claim: (.+) = (.+)\.", body,
    )
    assert match is not None, body
    names = sorted(match.group(1, 2, 3))
    left = oracle.parse_set_expression(match.group(4))
    right = oracle.parse_set_expression(match.group(5))
    left_column = oracle.membership_column(left, names)
    right_column = oracle.membership_column(right, names)
    first = None
    for row, left_value, right_value in zip(
            oracle.membership_rows(names), left_column, right_column):
        if left_value != right_value:
            first = row
            break
    answer = ("identity; columns match" if first is None else
              f"not an identity; fails at {row_text(first, spaced=True)}")
    return {"variant": variant, "query": query, "names": names,
            "left": left, "right": right, "left_column": left_column,
            "right_column": right_column, "first": first, "answer": answer}


def parse_compact_row(text):
    row = {}
    for field in text.split(", "):
        match = re.fullmatch(r"x([∈∉])(\w+)", field)
        assert match is not None, field
        row[match.group(2)] = match.group(1) == "∈"
    return row


def eval_membership(expression, row):
    env = {name: ({"x"} if included else set())
           for name, included in row.items()}
    return "x" in oracle.eval_set_expression(expression, env, {"x"})


class SetIdentityMembershipTableGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(887201)

    def test_output_contract(self):
        example = SetIdentityMembershipTableGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SetIdentityMembershipTableGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_all_eight_rows_subexpressions_and_sides_are_exact(self):
        generator = SetIdentityMembershipTableGenerator()
        for _ in range(180):
            example = generator.generate()
            parts = oracle_parts(example)
            rows = []
            side_values = []
            active_row = None
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "MEMBER_ROW":
                    active_row = parse_compact_row(fields[1])
                    rows.append(active_row)
                elif fields[0] == "EVAL_SUB":
                    self.assertEqual(parse_compact_row(fields[1]), active_row)
                    expression = oracle.parse_set_expression(fields[2])
                    expected = eval_membership(expression, active_row)
                    self.assertEqual(fields[3], "∈" if expected else "∉")
                elif fields[0] == "SIDE":
                    expression = parts[fields[1]]
                    expected = eval_membership(expression, active_row)
                    self.assertEqual(fields[2], "∈" if expected else "∉")
                    side_values.append((fields[1], expected))
            self.assertEqual(rows, oracle.membership_rows(parts["names"]))
            self.assertEqual(len(side_values), 16)
            compare = next(item.split(DELIM) for item in example["steps"]
                           if item.startswith("TABLE_COMPARE" + DELIM))
            if parts["first"] is None:
                self.assertEqual(compare, ["TABLE_COMPARE", "match"])
            else:
                self.assertEqual(compare, ["TABLE_COMPARE", "differ",
                                           row_text(parts["first"], spaced=True)])

    def test_all_variants_phrasings_and_expected_outcomes(self):
        for variant in SetIdentityMembershipTableGenerator.VARIANTS:
            generator = SetIdentityMembershipTableGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(
                    example["operation"],
                    f"set_identity_membership_table_{variant}",
                )
                seen_queries.add(parts["query"])
                if variant == "refute_identity":
                    self.assertIsNotNone(parts["first"])
                else:
                    self.assertIsNone(parts["first"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SetIdentityMembershipTableGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SetIdentityMembershipTableGenerator()
        for _ in range(200):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()

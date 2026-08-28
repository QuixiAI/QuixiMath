"""Independent count-table oracle for TwoWayTableProbabilityGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.two_way_table_probability_generator import (
    QUERIES, TwoWayTableProbabilityGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"A table records (\d+) ([a-z]+)\. Cells: (.+)\. One ([a-z]+) is "
        r"chosen uniformly\. Target row: ([a-z]+)=([a-z]+)\. Target column: "
        r"([a-z]+)=([a-z]+)\.", body)
    assert match is not None, body
    stated_total = int(match.group(1))
    cells = {}
    row_key = col_key = None
    row_values, col_values = [], []
    for item in match.group(3).split("; "):
        cell_match = re.fullmatch(
            r"([a-z]+)=([a-z]+) and ([a-z]+)=([a-z]+): (\d+)", item)
        assert cell_match is not None, item
        rkey, row, ckey, col, count = cell_match.groups()
        row_key = row_key or rkey
        col_key = col_key or ckey
        assert (rkey, ckey) == (row_key, col_key)
        if row not in row_values:
            row_values.append(row)
        if col not in col_values:
            col_values.append(col)
        cells[row, col] = int(count)
    assert len(cells) == len(row_values) * len(col_values)
    assert sum(cells.values()) == stated_total
    assert match.group(5) == row_key and match.group(7) == col_key
    target_row, target_col = match.group(6), match.group(8)
    cell = cells[target_row, target_col]
    row_total = sum(cells[target_row, col] for col in col_values)
    col_total = sum(cells[row, target_col] for row in row_values)
    if variant == "joint":
        value = Fraction(cell, stated_total)
        answer = ptext(value)
    elif variant == "marginal":
        value = Fraction(row_total, stated_total)
        answer = ptext(value)
    elif variant == "conditional_row":
        value = Fraction(cell, row_total)
        answer = ptext(value)
    elif variant == "conditional_column":
        value = Fraction(cell, col_total)
        answer = ptext(value)
    elif variant == "union":
        value = Fraction(row_total + col_total - cell, stated_total)
        answer = ptext(value)
    else:
        marginal = Fraction(col_total, stated_total)
        conditional = Fraction(cell, col_total)
        value = marginal
        answer = (f"P({col_key}={target_col}) = {ptext(marginal)}; "
                  f"P({row_key}={target_row} given {col_key}={target_col}) = "
                  f"{ptext(conditional)}")
    return {"variant": variant, "query": query, "answer": answer,
            "value": value, "cells": cells, "total": stated_total,
            "row_total": row_total, "col_total": col_total, "cell": cell,
            "shape": (len(row_values), len(col_values))}


class TwoWayTableProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(223607)

    def test_output_contract(self):
        example = TwoWayTableProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = TwoWayTableProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_table_and_arithmetic_steps_are_exact(self):
        generator = TwoWayTableProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            table_cells = [int(raw.split(DELIM)[2]) for raw in example["steps"]
                           if raw.startswith("TABLE_CELL" + DELIM)]
            self.assertEqual(table_cells, list(parts["cells"].values()))
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "TABLE_TOTAL":
                    expression = fields[2]
                    left, right = expression.split(" = ")
                    self.assertEqual(sum(map(int, left.split(" + "))), int(right))
                elif fields[0] == "PROB_SETUP":
                    self.assertGreaterEqual(int(fields[1]), 0)
                    self.assertGreater(int(fields[2]), 0)
                elif fields[0] in ("F", "FRAC_BUILD"):
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
                    self.assertEqual(fields[2], ptext(Fraction(fields[2])))
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]), int(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]), int(fields[3]))

    def test_two_by_three_variant_has_six_cells(self):
        generator = TwoWayTableProbabilityGenerator("two_by_three")
        for _ in range(100):
            self.assertEqual(oracle_parts(generator.generate())["shape"], (2, 3))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in TwoWayTableProbabilityGenerator.VARIANTS:
            generator = TwoWayTableProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_two_way_table_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TwoWayTableProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = TwoWayTableProbabilityGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

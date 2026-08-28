"""Independent rendered-table oracle for TwoWayTableGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.two_way_table_generator import QUERIES, TwoWayTableGenerator
from helpers import DELIM
from tests.stats_oracle import find_displays, parse_two_way


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def percent_text(numerator, denominator):
    value = Fraction(100 * numerator, denominator)
    if value.denominator == 1:
        return f"{value.numerator}%"
    tenths = value * 10
    assert tenths.denominator == 1
    raw = abs(tenths.numerator)
    sign = "-" if tenths < 0 else ""
    return f"{sign}{raw // 10}.{raw % 10}%"


def parsed_table(body):
    displays = [text for kind, text in find_displays(body)
                if kind == "two_way"]
    assert len(displays) == 1, displays
    rows, cols, cells = parse_two_way(displays[0])
    return rows, cols, cells


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    rows, cols, cells = parsed_table(body)
    body_rows, body_cols = rows[:-1], cols[:-1]
    assert rows[-1] == cols[-1] == "Total"
    grand_total = int(cells[-1][-1])
    row_totals = [int(cells[i][-1]) for i in range(len(body_rows))]
    col_totals = [int(cells[-1][j]) for j in range(len(body_cols))]
    if variant == "association_check":
        target_col = re.search(r"Compared column: (.+?)\.", body).group(1)
        j = body_cols.index(target_col)
        percents = [percent_text(int(cells[i][j]), row_totals[i])
                    for i in range(2)]
        associated = percents[0] != percents[1]
        symbol = "≠" if associated else "="
        label = "associated" if associated else "not associated"
        answer = f"{label}; {percents[0]} {symbol} {percents[1]}"
        target = None
    else:
        target_row, target_col = re.search(
            r"Target row: (.+?)\. Target column: (.+?)\.", body
        ).groups()
        i, j = body_rows.index(target_row), body_cols.index(target_col)
        if variant == "fill_missing_cell":
            known = sum(int(value) for value in cells[i][:-1]
                        if value != "?")
            value = row_totals[i] - known
        else:
            value = int(cells[i][j])
        if variant == "marginal":
            answer = str(row_totals[i])
        elif variant == "joint_relative":
            answer = percent_text(value, grand_total)
        elif variant == "conditional_row":
            answer = percent_text(value, row_totals[i])
        elif variant == "conditional_col":
            answer = percent_text(value, col_totals[j])
        else:
            answer = str(value)
        target = (i, j)
    return {"variant": variant, "query": query, "answer": answer,
            "rows": body_rows, "cols": body_cols, "cells": cells,
            "row_totals": row_totals, "col_totals": col_totals,
            "grand_total": grand_total, "target": target}


class TwoWayTableGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310016)

    def test_output_contract(self):
        example = TwoWayTableGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_700_answers_from_rendered_table(self):
        generator = TwoWayTableGenerator()
        for _ in range(700):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_margins_and_grand_total_are_exact(self):
        generator = TwoWayTableGenerator()
        for _ in range(400):
            parts = oracle_parts(generator.generate())
            cells = parts["cells"]
            for i, total in enumerate(parts["row_totals"]):
                known = [int(value) for value in cells[i][:-1]
                         if value != "?"]
                if "?" not in cells[i][:-1]:
                    self.assertEqual(sum(known), total)
            for j, total in enumerate(parts["col_totals"]):
                known = [cells[i][j] for i in range(len(parts["rows"]))]
                if "?" not in known:
                    self.assertEqual(sum(map(int, known)), total)
            self.assertEqual(sum(parts["row_totals"]), parts["grand_total"])
            self.assertEqual(sum(parts["col_totals"]), parts["grand_total"])

    def test_arithmetic_and_margin_steps_are_exact(self):
        generator = TwoWayTableGenerator()
        for _ in range(450):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] in ("MARGIN_ROW", "MARGIN_COL"):
                    if "?" not in fields[2]:
                        self.assertEqual(sum(map(int, fields[2].split(" + "))),
                                         int(fields[3]), raw)

    def test_all_four_table_shapes_are_reachable(self):
        generator = TwoWayTableGenerator("marginal")
        seen = set()
        for _ in range(500):
            parts = oracle_parts(generator.generate())
            seen.add((len(parts["rows"]), len(parts["cols"])))
        self.assertEqual(seen, {(2, 2), (2, 3), (3, 2), (3, 3)})

    def test_percent_answers_have_at_most_one_decimal(self):
        for variant in ("joint_relative", "conditional_row",
                        "conditional_col", "association_check"):
            generator = TwoWayTableGenerator(variant)
            for _ in range(250):
                answer = generator.generate()["final_answer"]
                for number in re.findall(r"\d+(?:\.\d+)?%", answer):
                    decimals = number.rstrip("%").partition(".")[2]
                    self.assertLessEqual(len(decimals), 1)

    def test_missing_cell_is_unique_and_not_leaked_before_subtraction(self):
        generator = TwoWayTableGenerator("fill_missing_cell")
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertEqual(sum(value == "?" for row in parts["cells"]
                                 for value in row), 1)
            cell_steps = [raw for raw in example["steps"]
                          if raw.startswith(f"TABLE_CELL{DELIM}")]
            self.assertEqual(len(cell_steps),
                             len(parts["rows"]) * len(parts["cols"]))
            self.assertEqual(cell_steps[-1].split(DELIM)[2],
                             example["final_answer"])
            grand = next(raw.split(DELIM)[2] for raw in example["steps"]
                         if raw.startswith(f"TABLE_TOTAL{DELIM}grand{DELIM}"))
            terms = list(map(int, grand.split(" = ")[0].split(" + ")))
            self.assertEqual(terms, parts["row_totals"])

    def test_association_rule_and_both_verdicts(self):
        generator = TwoWayTableGenerator("association_check")
        seen = set()
        for _ in range(300):
            example = generator.generate()
            self.assertIn("Association rule:", example["problem"])
            seen.add(example["final_answer"].split(";", 1)[0])
        self.assertEqual(seen, {"associated", "not associated"})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in TwoWayTableGenerator.VARIANTS:
            generator = TwoWayTableGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_two_way_table_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TwoWayTableGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = TwoWayTableGenerator()
        for _ in range(350):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                    example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()

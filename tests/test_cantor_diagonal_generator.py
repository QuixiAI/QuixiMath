"""Independent string oracle for CantorDiagonalGenerator."""
import random
import re
import unittest

from generators.cantor_diagonal_generator import CantorDiagonalGenerator, QUERIES
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_rows(text, prefix):
    rows = []
    for index, item in enumerate(text.split("; ")):
        match = re.fullmatch(fr"{prefix}{index + (1 if prefix == 'row ' else 0)} = (\d+)", item)
        assert match is not None, item
        rows.append(match.group(1))
    return rows


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "binary_strings":
        match = re.fullmatch(
            r"Binary rows of length (\d+), indexed 1 through \1: (.+)\. "
            r"Replace each diagonal bit by its opposite\.", body)
        assert match is not None, body
        size, rows = int(match.group(1)), parse_rows(match.group(2), "row ")
        old = "".join(rows[index][index] for index in range(size))
        new = "".join("1" if value == "0" else "0" for value in old)
        answer = f"diagonal {old}; new string {new}"
    elif variant == "decimal_digits":
        match = re.fullmatch(
            r"Decimal rows of length (\d+), indexed 1 through \1: (.+)\. "
            r"Replace a diagonal digit d by 1 unless d = 1, in which case "
            r"replace it by 2\.", body)
        assert match is not None, body
        size, rows = int(match.group(1)), parse_rows(match.group(2), "row ")
        old = "".join(rows[index][index] for index in range(size))
        new = "".join("2" if value == "1" else "1" for value in old)
        answer = f"diagonal {old}; new string {new}"
    else:
        match = re.fullmatch(
            r"For functions f0 through f(\d+) from ℕ to \{0, 1\}, the "
            r"columns shown are inputs 0 through \1: (.+)\. Define "
            r"g\(k\) = 1 − f_k\(k\) on the shown inputs\.", body)
        assert match is not None, body
        size = int(match.group(1)) + 1
        rows = parse_rows(match.group(2), "f")
        old = "".join(rows[index][index] for index in range(size))
        new = "".join("1" if value == "0" else "0" for value in old)
        answer = f"diagonal {old}; new function prefix {new}"
    assert len(rows) == size
    assert all(len(row) == size for row in rows)
    return {"variant": variant, "query": query, "rows": rows,
            "diagonal": old, "new": new, "answer": answer}


class CantorDiagonalGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(314159)

    def test_output_contract(self):
        example = CantorDiagonalGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CantorDiagonalGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_new_object_differs_from_every_row_at_its_index(self):
        generator = CantorDiagonalGenerator()
        for _ in range(350):
            parts = oracle_parts(generator.generate())
            for index, row in enumerate(parts["rows"]):
                self.assertNotEqual(parts["new"][index], row[index])
            self.assertNotIn(parts["new"], parts["rows"])

    def test_trace_records_each_diagonal_flip_and_check(self):
        generator = CantorDiagonalGenerator()
        for _ in range(180):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [raw.split(DELIM) for raw in example["steps"]]
            diag = [fields for fields in steps if fields[0] == "DIAG"]
            flips = [fields for fields in steps if fields[0] == "FLIP"]
            checks = [fields for fields in steps if fields[0] == "CHECK"]
            self.assertEqual("".join(fields[2] for fields in diag),
                             parts["diagonal"])
            self.assertEqual("".join(fields[2].split(" → ")[1]
                                     for fields in flips), parts["new"])
            self.assertEqual(len(checks), len(parts["rows"]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CantorDiagonalGenerator.VARIANTS:
            generator = CantorDiagonalGenerator(variant)
            seen_queries = set()
            for _ in range(220):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"cantor_diagonal_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CantorDiagonalGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CantorDiagonalGenerator()
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

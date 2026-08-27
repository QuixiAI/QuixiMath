"""Independent truth-table oracle for TruthTableGenerator."""
import random
import re
import unittest

from generators.truth_table_generator import QUERIES, TruthTableGenerator
from helpers import DELIM
from tests import foundations_oracle as logic_oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            if problem.endswith(f" {query}"):
                return problem[:-(len(query) + 1)], variant, query
    raise AssertionError(problem)


def row_text(assignment, names):
    return ", ".join(f"{name}={'T' if assignment[name] else 'F'}" for name in names)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "equivalence":
        match = re.fullmatch(
            r"Formula 1: (.+)\. Formula 2: (.+)\. Variables: ([pqr, ]+)\. "
            r"Row order: ([TF, ]+)\.", body
        )
        assert match is not None, body
        first, second = map(logic_oracle.parse_formula, match.groups()[:2])
        names = tuple(match.group(3).split(", "))
        first_column = logic_oracle.truth_column(first, names)
        second_column = logic_oracle.truth_column(second, names)
        if first_column == second_column:
            answer = f"equivalent; column {first_column}"
            witness = None
        else:
            witness_assignment = logic_oracle.first_difference(first, second)
            witness = row_text(witness_assignment, names)
            answer = f"not equivalent; differ at {witness}"
        formulas = {"formula 1": first, "formula 2": second}
        columns = {"formula 1": first_column, "formula 2": second_column}
    else:
        match = re.fullmatch(
            r"Formula: (.+)\. Variables: ([pqr, ]+)\. Row order: ([TF, ]+)\.",
            body,
        )
        assert match is not None, body
        formula = logic_oracle.parse_formula(match.group(1))
        names = tuple(match.group(2).split(", "))
        result = logic_oracle.truth_column(formula, names)
        formulas, columns, witness = {"formula": formula}, {"formula": result}, None
        if variant == "classify":
            classification = logic_oracle.classify(formula)
            answer = f"{classification}; {result}"
        else:
            answer = result
    expected_order = ", ".join(
        "".join("T" if assignment[name] else "F" for name in names)
        for assignment in logic_oracle.all_assignments(names)
    )
    self_order = match.group(4) if variant == "equivalence" else match.group(3)
    assert self_order == expected_order
    return {"variant": variant, "names": names, "formulas": formulas,
            "columns": columns, "answer": answer, "witness": witness,
            "query": query}


class TruthTableGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(399389)

    def test_output_contract(self):
        example = TruthTableGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = TruthTableGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_subformula_values_columns_and_counterexamples(self):
        generator = TruthTableGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            columns = {}
            counterexamples = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "EVAL_SUB":
                    assignment = {}
                    for item in fields[1].split(", "):
                        name, value = item.split("=")
                        assignment[name] = value == "T"
                    label, formula_text = fields[2].split(": ", 1)
                    actual = logic_oracle.eval_formula(
                        logic_oracle.parse_formula(formula_text), assignment
                    )
                    self.assertEqual(fields[3], "T" if actual else "F")
                    self.assertIn(label, parts["formulas"])
                elif fields[0] == "TT_COLUMN":
                    columns[fields[1]] = fields[2]
                elif fields[0] == "COUNTEREXAMPLE":
                    counterexamples.append(fields[1])
            self.assertEqual(columns, parts["columns"])
            if parts["witness"] is not None:
                self.assertEqual(counterexamples, [parts["witness"]])
            else:
                self.assertEqual(counterexamples, [])

    def test_all_variants_phrasings_and_classifications_are_reachable(self):
        for variant in TruthTableGenerator.VARIANTS:
            generator = TruthTableGenerator(variant)
            seen_queries = set()
            classifications = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"truth_table_{variant}")
                seen_queries.add(parts["query"])
                if variant == "classify":
                    classifications.add(parts["answer"].split(";", 1)[0])
            self.assertEqual(seen_queries, set(QUERIES[variant]))
            if variant == "classify":
                self.assertEqual(classifications,
                                 {"tautology", "contradiction", "contingency"})

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TruthTableGenerator("bogus")

    def test_pipe_safety_and_formula_canonicality(self):
        generator = TruthTableGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for formula in parts["formulas"].values():
                self.assertTrue(logic_oracle.is_canonical_formula(
                    logic_oracle.render(formula)))
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

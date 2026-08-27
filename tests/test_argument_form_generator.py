"""Independent schema matcher and truth-table oracle for ArgumentFormGenerator."""
import random
import re
import unittest

from generators.argument_form_generator import QUERIES, ArgumentFormGenerator
from helpers import DELIM
from tests import foundations_oracle as logic_oracle


X, Y, Z, W = (("meta", name) for name in "xyzw")

SCHEMAS = {
    "modus ponens": ((('imp', X, Y), X), Y, True),
    "modus tollens": ((('imp', X, Y), ('not', Y)), ('not', X), True),
    "hypothetical syllogism": ((('imp', X, Y), ('imp', Y, Z)), ('imp', X, Z), True),
    "disjunctive syllogism": ((('or', X, Y), ('not', X)), Y, True),
    "simplification": ((('and', X, Y),), X, True),
    "conjunction": ((X, Y), ('and', X, Y), True),
    "addition": ((X,), ('or', X, Y), True),
    "constructive dilemma": ((('and', ('imp', X, Y), ('imp', Z, W)),
                               ('or', X, Z)), ('or', Y, W), True),
    "affirming the consequent": ((('imp', X, Y), Y), X, False),
    "denying the antecedent": ((('imp', X, Y), ('not', X)), ('not', Y), False),
}


def match(pattern, actual, bindings):
    if pattern[0] == "meta":
        name = pattern[1]
        if name in bindings:
            return bindings[name] == actual
        bindings[name] = actual
        return True
    if pattern[0] != actual[0] or len(pattern) != len(actual):
        return False
    return all(match(p_child, a_child, bindings)
               for p_child, a_child in zip(pattern[1:], actual[1:]))


def schema_label(premises, conclusion):
    labels = []
    for label, (patterns, conclusion_pattern, _) in SCHEMAS.items():
        if len(patterns) != len(premises):
            continue
        bindings = {}
        if (all(match(pattern, actual, bindings)
                for pattern, actual in zip(patterns, premises))
                and match(conclusion_pattern, conclusion, bindings)):
            labels.append(label)
    assert len(labels) == 1, labels
    return labels[0]


def parse_english_clause(clause, first, second):
    if clause == first:
        return ("var", "p")
    if clause == second:
        return ("var", "q")
    if clause == f"it is not the case that {first}":
        return ("not", ("var", "p"))
    if clause == f"it is not the case that {second}":
        return ("not", ("var", "q"))
    if clause == f"if {first}, then {second}":
        return ("imp", ("var", "p"), ("var", "q"))
    raise AssertionError(clause)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            if problem.endswith(f" {query}"):
                return problem[:-(len(query) + 1)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "english":
        match_obj = re.fullmatch(
            r'Vocabulary: p means "(.+)"; q means "(.+)"\. Argument clauses: '
            r'(.+); therefore (.+)\.', body
        )
        assert match_obj is not None, body
        first, second, premise_text, conclusion_text = match_obj.groups()
        premises = tuple(parse_english_clause(item, first, second)
                         for item in premise_text.split("; "))
        conclusion = parse_english_clause(conclusion_text, first, second)
    else:
        match_obj = re.fullmatch(r"Premises: (.+)\. Conclusion: (.+)\.", body)
        assert match_obj is not None, body
        premises = tuple(logic_oracle.parse_formula(item)
                         for item in match_obj.group(1).split("; "))
        conclusion = logic_oracle.parse_formula(match_obj.group(2))
    label = schema_label(premises, conclusion)
    names = sorted(set().union(*(set(logic_oracle.formula_variables(item))
                                for item in premises),
                               set(logic_oracle.formula_variables(conclusion))))
    counterexample = None
    for assignment in logic_oracle.all_assignments(names):
        if (all(logic_oracle.eval_formula(item, assignment) for item in premises)
                and not logic_oracle.eval_formula(conclusion, assignment)):
            counterexample = assignment
            break
    if counterexample is None:
        answer = f"valid; {label}"
    else:
        answer = (f"invalid; {label}; counterexample "
                  f"{logic_oracle.row_text(counterexample)}")
    return {"variant": variant, "premises": premises, "conclusion": conclusion,
            "label": label, "counterexample": counterexample, "answer": answer,
            "names": names, "query": query}


class ArgumentFormGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(449107)

    def test_output_contract(self):
        example = ArgumentFormGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ArgumentFormGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_truth_rows_premise_filters_and_counterexample(self):
        generator = ArgumentFormGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            premise_rows = {}
            conclusion_rows = {}
            counterexample_rows = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] in ("PREMISES_ALL_T", "CONCLUSION_AT"):
                    assignment = {item.split("=")[0]: item.endswith("=T")
                                  for item in fields[1].split(", ")}
                    key = fields[1]
                    if fields[0] == "PREMISES_ALL_T":
                        expected = all(logic_oracle.eval_formula(item, assignment)
                                       for item in parts["premises"])
                        self.assertEqual(fields[2], "yes" if expected else "no")
                        premise_rows[key] = expected
                    else:
                        expected = logic_oracle.eval_formula(parts["conclusion"], assignment)
                        self.assertEqual(fields[2], "T" if expected else "F")
                        conclusion_rows[key] = expected
                elif fields[0] == "COUNTEREXAMPLE":
                    counterexample_rows.append(fields[1])
            self.assertEqual(len(premise_rows), 2 ** len(parts["names"]))
            if parts["counterexample"] is None:
                self.assertEqual(counterexample_rows, [])
            else:
                self.assertEqual(counterexample_rows,
                                 [logic_oracle.row_text(parts["counterexample"])])

    def test_all_variants_phrasings_and_validity_outcomes(self):
        for variant in ArgumentFormGenerator.VARIANTS:
            generator = ArgumentFormGenerator(variant)
            seen_queries = set()
            outcomes = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"argument_form_{variant}")
                seen_queries.add(parts["query"])
                outcomes.add(parts["counterexample"] is None)
            self.assertEqual(seen_queries, set(QUERIES[variant]))
            if variant == "named_rule":
                self.assertEqual(outcomes, {True})
            elif variant == "fallacy":
                self.assertEqual(outcomes, {False})
            else:
                self.assertEqual(outcomes, {False, True})

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ArgumentFormGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ArgumentFormGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()

"""Independent prompt-only oracle for GraphInterpretGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.graph_interpret_generator import (
    BAR_QUERIES,
    CONSTRUCT_BAR_QUERIES,
    DOUBLE_BAR_QUERIES,
    GraphInterpretGenerator,
    LINE_QUERIES,
    PICTOGRAPH_QUERIES,
)
from helpers import DELIM


LEGACY_OPERATIONS = {
    "bar": {
        "bar_chart_read", "bar_chart_compare", "bar_chart_total",
        "bar_chart_difference", "bar_chart_max", "bar_chart_min",
    },
    "line": {
        "line_graph_read", "line_graph_increase", "line_graph_decrease",
        "line_graph_max", "line_graph_min", "line_graph_range",
    },
    "pictograph": {
        "pictograph_read", "pictograph_compare", "pictograph_total",
        "pictograph_difference", "pictograph_max",
    },
}
NEW_OPERATIONS = {
    "double_bar": {
        "double_bar_compare", "double_bar_total", "double_bar_largest_gap",
    },
    "construct_bar": {"construct_bar"},
}


def _rows(lines):
    result = {}
    for line in lines:
        label, value = line.strip().rsplit(": ", 1)
        result[label] = int(value)
    return result


def _single_chart(problem):
    body = problem.split("\n\nQuestion:", 1)[0]
    lines = body.splitlines()
    if lines[0] == "Bar Chart Data:":
        return "bar", _rows(lines[1:])
    if lines[0] == "Line Graph Data:":
        return "line", _rows(lines[1:])
    match = re.fullmatch(r"Pictograph \(each (.) = (\d+)\):", lines[0])
    if match:
        symbol, scale = match.group(1), int(match.group(2))
        values = {}
        for line in lines[1:]:
            label, marks = line.strip().split(": ", 1)
            values[label] = len(marks) * scale
        return "pictograph", values
    raise AssertionError(problem)


def _double_chart(problem):
    body = problem.split("\n\nQuestion:", 1)[0]
    lines = body.splitlines()
    assert lines[0] == "Double Bar Chart Data:"
    series = {}
    current = None
    for line in lines[1:]:
        if line.startswith("Series "):
            current = line[len("Series "):-1]
            series[current] = {}
        else:
            label, value = line.strip().rsplit(": ", 1)
            series[current][label] = int(value)
    return series


def _labels_in_question(question, labels):
    # Word-boundary match: some line-graph label sets aren't prefix-free
    # (e.g. "2pm" is a substring of "12pm", "Mon" of "Mon2"), so plain
    # substring search would misfire.
    return [label for label in labels
            if re.search(rf"\b{re.escape(label)}\b", question)]


def _target_in_question(question, labels):
    found = _labels_in_question(question, labels)
    assert len(found) == 1, (question, found)
    return found[0]


def _two_targets_in_question(question, labels):
    found = _labels_in_question(question, labels)
    assert len(found) == 2, (question, found)
    return found


def _construct_oracle(problem):
    match = re.fullmatch(
        r"Raw category observations: (.+)\.\nCategory order: (.+)\.\n"
        r"Question: .+",
        problem,
    )
    observations = match.group(1).split(", ")
    categories = match.group(2).split(", ")
    return "; ".join(f"{category}: {observations.count(category)}"
                     for category in categories)


def oracle_answer(example):
    """Recompute solely from the display and question, never from steps."""
    operation = example["operation"]
    problem = example["problem"]
    question = problem.rsplit("\n", 1)[-1]
    if operation == "construct_bar":
        return _construct_oracle(problem)
    if operation.startswith("double_bar_"):
        series = _double_chart(problem)
        names = list(series)
        categories = list(series[names[0]])
        if operation == "double_bar_total":
            return str(sum(sum(values.values()) for values in series.values()))
        if operation == "double_bar_largest_gap":
            gaps = {category: abs(series[names[0]][category]
                                  - series[names[1]][category])
                    for category in categories}
            category = max(gaps, key=gaps.get)
            return (f"{category}; gap {gaps[category]} ({names[0]} "
                    f"{series[names[0]][category]}, {names[1]} "
                    f"{series[names[1]][category]})")
        category_question = question.replace(names[0], "").replace(names[1], "")
        category = _target_in_question(category_question, categories)
        value1, value2 = (series[names[0]][category],
                          series[names[1]][category])
        if value1 > value2:
            winner, high, low = names[0], value1, value2
        else:
            winner, high, low = names[1], value2, value1
        return f"{winner}; {category} {high} > {low} by {high - low}"

    kind, values = _single_chart(problem)
    labels = list(values)
    if operation.endswith("_read"):
        target = _target_in_question(question, labels)
        return str(values[target])
    if operation.endswith("_compare"):
        first, second = _two_targets_in_question(question, labels)
        value1, value2 = values[first], values[second]
        winner, high, low = ((first, value1, value2) if value1 > value2
                             else (second, value2, value1))
        if kind == "pictograph":
            return f"{winner} has {high - low} more"
        return f"{winner} is greater by {high - low}"
    if operation.endswith("_total"):
        return str(sum(values.values()))
    if operation.endswith("_difference"):
        first, second = _two_targets_in_question(question, labels)
        return str(abs(values[first] - values[second]))
    if operation.endswith("_max"):
        target = max(values, key=values.get)
        return f"{target} ({values[target]})"
    if operation.endswith("_min"):
        target = min(values, key=values.get)
        return f"{target} ({values[target]})"
    if operation == "line_graph_range":
        return str(max(values.values()) - min(values.values()))
    ordered = list(values.items())
    if operation == "line_graph_increase":
        changes = [(ordered[index][1] - ordered[index - 1][1],
                    ordered[index - 1][0], ordered[index][0])
                   for index in range(1, len(ordered))]
        amount, first, second = max(changes)
        return f"{first} to {second} (increase of {amount})"
    if operation == "line_graph_decrease":
        changes = [(ordered[index - 1][1] - ordered[index][1],
                    ordered[index - 1][0], ordered[index][0])
                   for index in range(1, len(ordered))]
        amount, first, second = max(changes)
        return f"{first} to {second} (decrease of {amount})"
    raise AssertionError((operation, problem))


def _query_template(example):
    query = example["problem"].rsplit("\n", 1)[-1]
    op = example["operation"]
    if op == "construct_bar":
        return next(template for template in CONSTRUCT_BAR_QUERIES
                    if query == template)
    if op.startswith("double_bar_"):
        bank = DOUBLE_BAR_QUERIES
        question_type = op.removeprefix("double_bar_")
        fields = ("category", "series1", "series2")
    else:
        for prefix, candidate_bank in (("bar_chart_", BAR_QUERIES),
                                       ("line_graph_", LINE_QUERIES),
                                       ("pictograph_", PICTOGRAPH_QUERIES)):
            if op.startswith(prefix):
                bank = candidate_bank
                question_type = op.removeprefix(prefix)
                if question_type == "read":
                    question_type = "read_value"
                break
        else:
            raise AssertionError(op)
        fields = ("target", "a", "b")
    for template in bank[question_type]:
        pattern = re.escape(template)
        for field in fields:
            pattern = pattern.replace(r"\{" + field + r"\}", r".+?")
        if re.fullmatch(pattern, query):
            return template
    raise AssertionError(query)


class TestGraphInterpretGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(310008)

    def test_output_contract(self):
        for graph_type in (*LEGACY_OPERATIONS, *NEW_OPERATIONS):
            result = GraphInterpretGenerator(graph_type).generate()
            for key in ("problem_id", "operation", "problem", "steps",
                        "final_answer"):
                self.assertIn(key, result)
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = GraphInterpretGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_answer(example),
                             example["problem"])

    def test_every_legacy_and_new_operation_has_prompt_oracle_coverage(self):
        for graph_type, expected in {**LEGACY_OPERATIONS,
                                     **NEW_OPERATIONS}.items():
            generator = GraphInterpretGenerator(graph_type)
            seen = set()
            for _ in range(500):
                example = generator.generate()
                self.assertEqual(example["final_answer"], oracle_answer(example))
                seen.add(example["operation"])
            self.assertEqual(seen, expected)

    def test_arithmetic_steps_are_exact(self):
        generator = GraphInterpretGenerator()
        for _ in range(600):
            example = generator.generate()
            oracle_answer(example)
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

    def test_double_bar_has_exactly_two_graph_data_steps(self):
        generator = GraphInterpretGenerator("double_bar")
        for _ in range(250):
            example = generator.generate()
            rows = [raw for raw in example["steps"]
                    if raw.startswith(f"GRAPH_DATA{DELIM}")]
            self.assertEqual(len(rows), 2)
            self.assertTrue(all("double_bar" in row for row in rows))

    def test_construct_bar_counts_each_raw_observation(self):
        generator = GraphInterpretGenerator("construct_bar")
        for _ in range(250):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             _construct_oracle(example["problem"]))
            observations = re.search(
                r"Raw category observations: (.+)\.", example["problem"]
            ).group(1).split(", ")
            count_steps = [raw for raw in example["steps"]
                           if raw.startswith(f"COUNT{DELIM}")]
            self.assertEqual(sum(int(raw.split(DELIM)[2])
                                 for raw in count_steps), len(observations))

    def test_new_variants_have_four_phrasings_per_question(self):
        construct = GraphInterpretGenerator("construct_bar")
        seen = {_query_template(construct.generate()) for _ in range(300)}
        self.assertEqual(seen, set(CONSTRUCT_BAR_QUERIES))

        double = GraphInterpretGenerator("double_bar")
        seen = {question_type: set() for question_type in DOUBLE_BAR_QUERIES}
        for _ in range(1200):
            example = double.generate()
            question_type = example["operation"].removeprefix("double_bar_")
            seen[question_type].add(_query_template(example))
        for question_type, templates in DOUBLE_BAR_QUERIES.items():
            self.assertEqual(seen[question_type], set(templates))

    def test_legacy_variants_have_four_phrasings_per_question(self):
        for graph_type, prefix, bank in (
            ("bar", "bar_chart_", BAR_QUERIES),
            ("line", "line_graph_", LINE_QUERIES),
            ("pictograph", "pictograph_", PICTOGRAPH_QUERIES),
        ):
            generator = GraphInterpretGenerator(graph_type)
            seen = {question_type: set() for question_type in bank}
            for _ in range(1500):
                example = generator.generate()
                question_type = example["operation"].removeprefix(prefix)
                if question_type == "read":
                    question_type = "read_value"
                seen[question_type].add(_query_template(example))
            for question_type, templates in bank.items():
                self.assertEqual(seen[question_type], set(templates),
                                 (graph_type, question_type))

    def test_all_new_verdict_outcomes_occur(self):
        generator = GraphInterpretGenerator("double_bar")
        winners = set()
        for _ in range(500):
            example = generator.generate()
            if example["operation"] == "double_bar_compare":
                winners.add(example["final_answer"].split(";", 1)[0])
        self.assertGreaterEqual(len(winners), 4)

    def test_invalid_graph_type_rejected(self):
        with self.assertRaises(ValueError):
            GraphInterpretGenerator("bogus")

    def test_deterministic_with_seed(self):
        random.seed(100)
        first = GraphInterpretGenerator().generate()
        random.seed(100)
        second = GraphInterpretGenerator().generate()
        self.assertEqual(first["problem"], second["problem"])
        self.assertEqual(first["final_answer"], second["final_answer"])
        self.assertEqual(first["steps"], second["steps"])

    def test_pipe_safety_and_render_sanity(self):
        generator = GraphInterpretGenerator()
        for _ in range(500):
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

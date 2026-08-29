"""Read and construct text bar, line, pictograph, and double-bar displays.

Legacy variants remain ``bar`` (six operations), ``line`` (six), and
``pictograph`` (five); every question type in all three now draws from
3-5 phrasing templates (``BAR_QUERIES``, ``LINE_QUERIES``,
``PICTOGRAPH_QUERIES``). The statistics extension adds ``double_bar`` with
compare, total, and largest-gap questions, plus ``construct_bar`` from raw
categorical observations. Op-codes include ``GRAPH_DATA``, ``GRAPH_READ``,
``COUNT``, ``CMP``, ``GRAPH_MIN``, ``GRAPH_MAX``, ``GRAPH_CHANGE``,
``GRAPH_MAX_CHANGE``, ``PICTO_KEY``, ``PICTO_COUNT``, ``SORT``, ``A``, ``S``,
``M``, ``CHECK``, and ``Z``. All values and arithmetic are integers; distinct
extrema and gaps are enforced when a question needs a unique answer. Random
data, category sets, series labels, raw-data order, and per-question
phrasings give unbounded capacity.
"""
import hashlib
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from stats_common import running_sum_steps, text_list


STATISTICS = True
GRAPH_TYPES = ("bar", "line", "pictograph", "double_bar", "construct_bar")
SERIES_PAIRS = (
    ("Class A", "Class B"), ("Morning", "Afternoon"),
    ("North", "South"), ("Team Blue", "Team Gold"),
    ("Week 1", "Week 2"), ("Year 1", "Year 2"),
)
DOUBLE_BAR_QUERIES = {
    "compare": (
        "Question: At {category}, which series is greater and by how much?",
        "Question: Compare {series1} and {series2} for {category}.",
        "Question: Which group has the larger {category} bar, and what is the difference?",
        "Question: For {category}, name the higher series and calculate its lead.",
    ),
    "total": (
        "Question: What is the total of every bar in both series?",
        "Question: Add all values across the two series.",
        "Question: What combined total is represented by the double-bar chart?",
        "Question: Find the sum of all bars from {series1} and {series2}.",
    ),
    "largest_gap": (
        "Question: Which category has the largest gap between the two series?",
        "Question: Find the category where the series differ most.",
        "Question: Compare each pair of bars and report the unique largest difference.",
        "Question: At which category is the absolute gap greatest?",
    ),
}
CONSTRUCT_BAR_QUERIES = (
    "Question: Construct the bar-chart data list in the stated category order.",
    "Question: Count each category and report the complete bar data.",
    "Question: Turn the raw observations into a category-to-count bar list.",
    "Question: Build the text bar chart by tallying every observation.",
)
BAR_QUERIES = {
    "read_value": (
        "Question: What is the value for {target}?",
        "Question: How many does {target} have?",
        "Question: Read the bar chart value for {target}.",
        "Question: What does the {target} bar show?",
    ),
    "compare": (
        "Question: Compare {a} and {b}. Which is greater and by how much?",
        "Question: Between {a} and {b}, which is greater and by how much?",
        "Question: Which bar is taller, {a} or {b}, and by how much?",
        "Question: How much greater is the larger of {a} and {b}?",
    ),
    "total": (
        "Question: What is the total of all values?",
        "Question: Add up every bar's value.",
        "Question: What do all the bars sum to?",
        "Question: Find the combined total across all categories.",
    ),
    "difference": (
        "Question: What is the difference between {a} and {b}?",
        "Question: By how much do {a} and {b} differ?",
        "Question: Find the gap between {a} and {b}.",
        "Question: How far apart are {a} and {b}?",
    ),
    "max": (
        "Question: Which category has the highest value?",
        "Question: Which bar is tallest?",
        "Question: Name the category with the largest value.",
        "Question: Which category peaks the highest?",
    ),
    "min": (
        "Question: Which category has the lowest value?",
        "Question: Which bar is shortest?",
        "Question: Name the category with the smallest value.",
        "Question: Which category dips the lowest?",
    ),
}
LINE_QUERIES = {
    "read_value": (
        "Question: What is the value at {target}?",
        "Question: What does the line show at {target}?",
        "Question: Read the value plotted at {target}.",
        "Question: What is recorded at {target}?",
    ),
    "increase": (
        "Question: Between which two consecutive time periods was there "
        "the largest increase?",
        "Question: Find the consecutive pair with the biggest rise.",
        "Question: Where did the value climb the most from one period to "
        "the next?",
        "Question: Identify the two consecutive points with the largest "
        "increase.",
    ),
    "decrease": (
        "Question: Between which two consecutive time periods was there "
        "the largest decrease?",
        "Question: Find the consecutive pair with the biggest drop.",
        "Question: Where did the value fall the most from one period to "
        "the next?",
        "Question: Identify the two consecutive points with the largest "
        "decrease.",
    ),
    "max": (
        "Question: At which time was the value highest?",
        "Question: When did the line peak?",
        "Question: Identify the time with the maximum value.",
        "Question: Which point on the line is highest?",
    ),
    "min": (
        "Question: At which time was the value lowest?",
        "Question: When did the line bottom out?",
        "Question: Identify the time with the minimum value.",
        "Question: Which point on the line is lowest?",
    ),
    "range": (
        "Question: What is the range (difference between highest and "
        "lowest values)?",
        "Question: Find the spread between the highest and lowest values.",
        "Question: By how much do the maximum and minimum values differ?",
        "Question: Compute the range of the plotted values.",
    ),
}
PICTOGRAPH_QUERIES = {
    "read_value": (
        "Question: How many does {target} represent?",
        "Question: What value does {target} show?",
        "Question: Read the pictograph value for {target}.",
        "Question: How many symbols' worth does {target} have?",
    ),
    "compare": (
        "Question: Compare {a} and {b}. Which has more and by how much?",
        "Question: Between {a} and {b}, which has more and by how much?",
        "Question: Which has more symbols, {a} or {b}, and by how much?",
        "Question: How many more does the larger of {a} and {b} have?",
    ),
    "total": (
        "Question: What is the total represented by all categories?",
        "Question: Add up the values shown for every category.",
        "Question: What do all the pictograph rows sum to?",
        "Question: Find the combined total across all categories.",
    ),
    "difference": (
        "Question: What is the difference between {a} and {b}?",
        "Question: By how much do {a} and {b} differ?",
        "Question: Find the gap between {a} and {b}.",
        "Question: How far apart are {a} and {b}?",
    ),
    "max": (
        "Question: Which category has the highest value?",
        "Question: Which category has the most symbols?",
        "Question: Name the category with the largest value.",
        "Question: Which category is represented the most?",
    ),
}


class GraphInterpretGenerator(ProblemGenerator):
    """
    Generate bar, line, pictograph, double-bar, and bar-construction problems.

    Read values, comparisons, totals, differences, extrema, changes, and gaps,
    or tally raw categorical observations into a complete bar-data list.
    """

    def __init__(self, graph_type: str = None):
        """
        Initialize with optional graph type.

        Args:
            graph_type: One of ``GRAPH_TYPES``, or None for random.
        """
        if graph_type is not None and graph_type not in GRAPH_TYPES:
            raise ValueError(f"graph_type must be one of {GRAPH_TYPES} or None")
        self.graph_type = graph_type

    def generate(self) -> dict:
        if self.graph_type is not None:
            return self._generate_type(self.graph_type)

        # Preserve the exact global-RNG advancement of the legacy three-way
        # wrapper. This class sits mid-registry, so changing its consumption
        # would churn seeded examples for hundreds of unrelated generators.
        legacy_type = random.choice(("bar", "line", "pictograph"))
        legacy_result = self._generate_type(legacy_type)
        post_legacy_state = random.getstate()
        digest = hashlib.sha256(
            legacy_result["problem"].encode("utf-8")
        ).digest()
        extension = digest[0] % 5
        if extension not in (0, 1):
            return legacy_result
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            graph_type = "double_bar" if extension == 0 else "construct_bar"
            return self._generate_type(graph_type)
        finally:
            random.setstate(post_legacy_state)

    def _generate_type(self, graph_type) -> dict:

        if graph_type == "bar":
            return self._generate_bar_chart()
        elif graph_type == "line":
            return self._generate_line_graph()
        elif graph_type == "pictograph":
            return self._generate_pictograph()
        elif graph_type == "double_bar":
            return self._generate_double_bar()
        return self._generate_construct_bar()

    def _generate_double_bar(self) -> dict:
        """Generate one of the three planned double-bar interpretations."""
        categories = random.sample(self._get_categories("bar"),
                                   random.randint(4, 6))
        series1, series2 = random.choice(SERIES_PAIRS)
        question_type = random.choice(("compare", "total", "largest_gap"))
        while True:
            first = dict(zip(categories,
                             random.sample(range(5, 51), len(categories))))
            second = dict(zip(categories,
                              random.sample(range(5, 51), len(categories))))
            gaps = [abs(first[category] - second[category])
                    for category in categories]
            if question_type == "compare":
                target = random.choice(categories)
                if first[target] == second[target]:
                    continue
            elif question_type == "largest_gap":
                if max(gaps) == 0 or gaps.count(max(gaps)) != 1:
                    continue
            break
        return self._create_double_bar_problem(
            categories, series1, series2, first, second, question_type)

    def _generate_construct_bar(self) -> dict:
        """Construct a bar-data text list from raw category observations."""
        categories = sorted(random.sample(self._get_categories("bar"),
                                          random.randint(4, 6)))
        counts = {category: random.randint(1, 7) for category in categories}
        observations = [category for category in categories
                        for _ in range(counts[category])]
        random.shuffle(observations)
        chart = text_list(counts)
        problem = (
            f"Raw category observations: {', '.join(observations)}.\n"
            f"Category order: {', '.join(categories)}.\n"
            f"{random.choice(CONSTRUCT_BAR_QUERIES)}"
        )
        steps = [step("SORT", ", ".join(sorted(observations)))]
        for category, count in counts.items():
            steps.append(step("COUNT", category, count))
        additions, total = running_sum_steps(counts.values())
        steps.extend(additions)
        steps.extend([
            step("GRAPH_DATA", "bar_chart",
                 ",".join(f"{category}:{count}"
                          for category, count in counts.items())),
            step("CHECK", "category counts sum",
                 " + ".join(map(str, counts.values())), len(observations)),
            step("Z", chart),
        ])
        return dict(
            problem_id=jid(), operation="construct_bar", problem=problem,
            steps=steps, final_answer=chart,
        )

    def _generate_bar_chart(self) -> dict:
        """Generate a bar chart interpretation problem."""
        # Create random categorical data
        categories = self._get_categories("bar")
        num_categories = random.randint(4, 6)
        selected = random.sample(categories, num_categories)
        # distinct values: max/min/compare questions stay unambiguous
        drawn = random.sample(range(5, 51), num_categories)
        values = dict(zip(selected, drawn))

        # Choose question type
        question_type = random.choice([
            "read_value", "compare", "total", "difference", "max", "min"
        ])

        return self._create_bar_problem(values, question_type)

    def _generate_line_graph(self) -> dict:
        """Generate a line graph interpretation problem."""
        # Create time-series data
        time_labels = self._get_time_labels()
        num_points = random.randint(5, 8)
        selected_times = time_labels[:num_points]

        # Choose question type first, then draw a walk that keeps its
        # answer unambiguous (unique extremum / unique largest change)
        question_type = random.choice([
            "read_value", "increase", "decrease", "max", "min", "range"
        ])

        while True:
            start_val = random.randint(10, 30)
            values = {}
            current = start_val
            for t in selected_times:
                values[t] = current
                change = random.randint(-5, 8)
                current = max(5, current + change)
            vals = [values[t] for t in selected_times]
            diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
            if question_type == "max" and vals.count(max(vals)) != 1:
                continue
            if question_type == "min" and vals.count(min(vals)) != 1:
                continue
            if question_type == "increase":
                top = max(diffs)
                if top <= 0 or diffs.count(top) != 1:
                    continue
            if question_type == "decrease":
                bottom = min(diffs)
                if bottom >= 0 or diffs.count(bottom) != 1:
                    continue
            break

        return self._create_line_problem(values, selected_times, question_type)

    def _generate_pictograph(self) -> dict:
        """Generate a pictograph interpretation problem."""
        categories = self._get_categories("pictograph")
        num_categories = random.randint(3, 5)
        selected = random.sample(categories, num_categories)

        # Each symbol represents a value
        symbol_value = random.choice([2, 5, 10])
        symbols = ["★", "●", "■", "▲", "♦"]
        symbol = random.choice(symbols)

        # Generate distinct symbol counts (1-8 symbols per category) so
        # max/compare questions stay unambiguous
        drawn = random.sample(range(1, 9), num_categories)
        symbol_counts = dict(zip(selected, drawn))
        actual_values = {cat: count * symbol_value for cat, count in symbol_counts.items()}

        # Choose question type
        question_type = random.choice([
            "read_value", "compare", "total", "difference", "max"
        ])

        return self._create_pictograph_problem(
            symbol_counts, actual_values, symbol, symbol_value, question_type
        )

    def _get_categories(self, context: str) -> list:
        """Return appropriate category names based on context."""
        if context == "bar":
            category_sets = [
                ["Apples", "Oranges", "Bananas", "Grapes", "Strawberries", "Peaches"],
                ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"],
                ["Math", "Science", "English", "History", "Art", "Music"],
                ["Soccer", "Basketball", "Baseball", "Tennis", "Swimming", "Football"],
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            ]
        else:  # pictograph
            category_sets = [
                ["Dogs", "Cats", "Birds", "Fish", "Hamsters"],
                ["Pizza", "Burgers", "Tacos", "Pasta", "Salad"],
                ["Bikes", "Cars", "Buses", "Trains", "Planes"],
                ["Lions", "Tigers", "Bears", "Elephants", "Giraffes"],
            ]
        return random.choice(category_sets)

    def _get_time_labels(self) -> list:
        """Return time-based labels for line graphs."""
        label_sets = [
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
            ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8"],
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon2"],
            ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
            ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"],
        ]
        return random.choice(label_sets)

    def _format_bar_chart(self, values: dict) -> str:
        """Format bar chart data as text representation."""
        lines = ["Bar Chart Data:"]
        for cat, val in values.items():
            lines.append(f"  {cat}: {val}")
        return "\n".join(lines)

    def _format_line_graph(self, values: dict, times: list) -> str:
        """Format line graph data as text representation."""
        lines = ["Line Graph Data:"]
        for t in times:
            lines.append(f"  {t}: {values[t]}")
        return "\n".join(lines)

    def _format_pictograph(self, symbol_counts: dict, symbol: str, symbol_value: int) -> str:
        """Format pictograph data as text representation."""
        lines = [f"Pictograph (each {symbol} = {symbol_value}):"]
        for cat, count in symbol_counts.items():
            symbols_str = symbol * count
            lines.append(f"  {cat}: {symbols_str}")
        return "\n".join(lines)

    @staticmethod
    def _format_double_bar(categories, series1, series2, first, second):
        lines = ["Double Bar Chart Data:", f"Series {series1}:"]
        lines.extend(f"  {category}: {first[category]}"
                     for category in categories)
        lines.append(f"Series {series2}:")
        lines.extend(f"  {category}: {second[category]}"
                     for category in categories)
        return "\n".join(lines)

    def _create_double_bar_problem(
        self, categories, series1, series2, first, second, question_type
    ) -> dict:
        """Create a double-bar problem with two explicit data-series steps."""
        chart = self._format_double_bar(
            categories, series1, series2, first, second)
        steps = [
            step("GRAPH_DATA", f"double_bar {series1}",
                 ",".join(f"{category}:{first[category]}"
                          for category in categories)),
            step("GRAPH_DATA", f"double_bar {series2}",
                 ",".join(f"{category}:{second[category]}"
                          for category in categories)),
        ]
        fields = {"series1": series1, "series2": series2}
        if question_type == "compare":
            category = random.choice(categories)
            value1, value2 = first[category], second[category]
            steps.extend([step("GRAPH_READ", f"{series1} {category}", value1),
                          step("GRAPH_READ", f"{series2} {category}", value2)])
            if value1 > value2:
                winner, high, low = series1, value1, value2
            else:
                winner, high, low = series2, value2, value1
            difference = high - low
            steps.extend([step("S", high, low, difference),
                          step("CMP", series1, series2, winner)])
            answer = (f"{winner}; {category} {high} > {low} by "
                      f"{difference}")
            operation = "double_bar_compare"
            fields["category"] = category
        elif question_type == "total":
            values = ([first[category] for category in categories]
                      + [second[category] for category in categories])
            for category in categories:
                steps.append(step("GRAPH_READ", f"{series1} {category}",
                                  first[category]))
            for category in categories:
                steps.append(step("GRAPH_READ", f"{series2} {category}",
                                  second[category]))
            additions, total = running_sum_steps(values)
            steps.extend(additions)
            steps.append(step("CHECK", "all bars included",
                              " + ".join(map(str, values)), total))
            answer = str(total)
            operation = "double_bar_total"
        else:
            gaps = {}
            for category in categories:
                value1, value2 = first[category], second[category]
                high, low = max(value1, value2), min(value1, value2)
                gap = high - low
                gaps[category] = gap
                steps.extend([
                    step("GRAPH_READ", f"{series1} {category}", value1),
                    step("GRAPH_READ", f"{series2} {category}", value2),
                    step("S", high, low, gap),
                ])
            category = max(gaps, key=gaps.get)
            answer = (f"{category}; gap {gaps[category]} ({series1} "
                      f"{first[category]}, {series2} {second[category]})")
            steps.append(step("CHECK", "unique largest gap",
                              category, gaps[category]))
            operation = "double_bar_largest_gap"
        query = random.choice(DOUBLE_BAR_QUERIES[question_type]).format(**fields)
        problem = f"{chart}\n\n{query}"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(), operation=operation, problem=problem,
            steps=steps, final_answer=answer,
        )

    def _create_bar_problem(self, values: dict, question_type: str) -> dict:
        """Create a bar chart problem with steps."""
        steps = []
        categories = list(values.keys())
        chart_repr = self._format_bar_chart(values)

        # Record the graph data
        steps.append(step("GRAPH_DATA", "bar_chart", ",".join(f"{k}:{v}" for k, v in values.items())))

        if question_type == "read_value":
            target = random.choice(categories)
            value = values[target]
            steps.append(step("GRAPH_READ", target, value))
            final_answer = str(value)
            query = random.choice(BAR_QUERIES["read_value"]).format(target=target)
            problem = f"{chart_repr}\n\n{query}"
            operation = "bar_chart_read"

        elif question_type == "compare":
            cat1, cat2 = random.sample(categories, 2)
            v1, v2 = values[cat1], values[cat2]
            steps.append(step("GRAPH_READ", cat1, v1))
            steps.append(step("GRAPH_READ", cat2, v2))
            if v1 > v2:
                relation = "greater"
                diff = v1 - v2
                steps.append(step("S", v1, v2, diff))
                final_answer = f"{cat1} is greater by {diff}"
            elif v1 < v2:
                relation = "less"
                diff = v2 - v1
                steps.append(step("S", v2, v1, diff))
                final_answer = f"{cat2} is greater by {diff}"
            else:
                relation = "equal"
                final_answer = f"{cat1} and {cat2} are equal"
            steps.append(step("CMP", cat1, cat2, relation))
            query = random.choice(BAR_QUERIES["compare"]).format(a=cat1, b=cat2)
            problem = f"{chart_repr}\n\n{query}"
            operation = "bar_chart_compare"

        elif question_type == "total":
            total = 0
            for cat in categories:
                v = values[cat]
                steps.append(step("GRAPH_READ", cat, v))
                new_total = total + v
                steps.append(step("A", total, v, new_total))
                total = new_total
            final_answer = str(total)
            query = random.choice(BAR_QUERIES["total"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "bar_chart_total"

        elif question_type == "difference":
            cat1, cat2 = random.sample(categories, 2)
            v1, v2 = values[cat1], values[cat2]
            steps.append(step("GRAPH_READ", cat1, v1))
            steps.append(step("GRAPH_READ", cat2, v2))
            diff = abs(v1 - v2)
            if v1 >= v2:
                steps.append(step("S", v1, v2, diff))
            else:
                steps.append(step("S", v2, v1, diff))
            final_answer = str(diff)
            query = random.choice(BAR_QUERIES["difference"]).format(a=cat1, b=cat2)
            problem = f"{chart_repr}\n\n{query}"
            operation = "bar_chart_difference"

        elif question_type == "max":
            max_val = max(values.values())
            max_cat = [k for k, v in values.items() if v == max_val][0]
            for cat in categories:
                steps.append(step("GRAPH_READ", cat, values[cat]))
            steps.append(step("GRAPH_MAX", max_cat, max_val))
            final_answer = f"{max_cat} ({max_val})"
            query = random.choice(BAR_QUERIES["max"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "bar_chart_max"

        else:  # min
            min_val = min(values.values())
            min_cat = [k for k, v in values.items() if v == min_val][0]
            for cat in categories:
                steps.append(step("GRAPH_READ", cat, values[cat]))
            steps.append(step("GRAPH_MIN", min_cat, min_val))
            final_answer = f"{min_cat} ({min_val})"
            query = random.choice(BAR_QUERIES["min"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "bar_chart_min"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

    def _create_line_problem(self, values: dict, times: list, question_type: str) -> dict:
        """Create a line graph problem with steps."""
        steps = []
        chart_repr = self._format_line_graph(values, times)

        # Record the graph data
        steps.append(step("GRAPH_DATA", "line_graph", ",".join(f"{k}:{v}" for k, v in values.items())))

        if question_type == "read_value":
            target = random.choice(times)
            value = values[target]
            steps.append(step("GRAPH_READ", target, value))
            final_answer = str(value)
            query = random.choice(LINE_QUERIES["read_value"]).format(target=target)
            problem = f"{chart_repr}\n\n{query}"
            operation = "line_graph_read"

        elif question_type == "increase":
            # Find largest increase between consecutive points
            max_increase = 0
            max_pair = (times[0], times[1])
            for i in range(len(times) - 1):
                t1, t2 = times[i], times[i + 1]
                increase = values[t2] - values[t1]
                steps.append(step("GRAPH_READ", t1, values[t1]))
                steps.append(step("GRAPH_READ", t2, values[t2]))
                steps.append(step("S", values[t2], values[t1], increase))
                steps.append(step("GRAPH_CHANGE", t1, t2, increase))
                if increase > max_increase:
                    max_increase = increase
                    max_pair = (t1, t2)
            steps.append(step("GRAPH_MAX_CHANGE", max_pair[0], max_pair[1], max_increase))
            final_answer = f"{max_pair[0]} to {max_pair[1]} (increase of {max_increase})"
            query = random.choice(LINE_QUERIES["increase"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "line_graph_increase"

        elif question_type == "decrease":
            # Find largest decrease between consecutive points
            max_decrease = 0
            max_pair = (times[0], times[1])
            for i in range(len(times) - 1):
                t1, t2 = times[i], times[i + 1]
                decrease = values[t1] - values[t2]
                steps.append(step("GRAPH_READ", t1, values[t1]))
                steps.append(step("GRAPH_READ", t2, values[t2]))
                steps.append(step("S", values[t1], values[t2], decrease))
                steps.append(step("GRAPH_CHANGE", t1, t2, -decrease))
                if decrease > max_decrease:
                    max_decrease = decrease
                    max_pair = (t1, t2)
            if max_decrease > 0:
                steps.append(step("GRAPH_MAX_CHANGE", max_pair[0], max_pair[1], -max_decrease))
                final_answer = f"{max_pair[0]} to {max_pair[1]} (decrease of {max_decrease})"
            else:
                final_answer = "No decrease occurred"
            query = random.choice(LINE_QUERIES["decrease"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "line_graph_decrease"

        elif question_type == "max":
            max_val = max(values.values())
            max_time = [t for t in times if values[t] == max_val][0]
            for t in times:
                steps.append(step("GRAPH_READ", t, values[t]))
            steps.append(step("GRAPH_MAX", max_time, max_val))
            final_answer = f"{max_time} ({max_val})"
            query = random.choice(LINE_QUERIES["max"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "line_graph_max"

        elif question_type == "min":
            min_val = min(values.values())
            min_time = [t for t in times if values[t] == min_val][0]
            for t in times:
                steps.append(step("GRAPH_READ", t, values[t]))
            steps.append(step("GRAPH_MIN", min_time, min_val))
            final_answer = f"{min_time} ({min_val})"
            query = random.choice(LINE_QUERIES["min"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "line_graph_min"

        else:  # range
            max_val = max(values.values())
            min_val = min(values.values())
            for t in times:
                steps.append(step("GRAPH_READ", t, values[t]))
            steps.append(step("GRAPH_MAX", "max", max_val))
            steps.append(step("GRAPH_MIN", "min", min_val))
            range_val = max_val - min_val
            steps.append(step("S", max_val, min_val, range_val))
            final_answer = str(range_val)
            query = random.choice(LINE_QUERIES["range"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "line_graph_range"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

    def _create_pictograph_problem(
        self, symbol_counts: dict, actual_values: dict, symbol: str,
        symbol_value: int, question_type: str
    ) -> dict:
        """Create a pictograph problem with steps."""
        steps = []
        categories = list(symbol_counts.keys())
        chart_repr = self._format_pictograph(symbol_counts, symbol, symbol_value)

        # Record the graph data and key
        steps.append(step("GRAPH_DATA", "pictograph", f"key:{symbol}={symbol_value}"))
        steps.append(step("PICTO_KEY", symbol, symbol_value))

        if question_type == "read_value":
            target = random.choice(categories)
            count = symbol_counts[target]
            value = actual_values[target]
            steps.append(step("PICTO_COUNT", target, count))
            steps.append(step("M", count, symbol_value, value))
            final_answer = str(value)
            query = random.choice(PICTOGRAPH_QUERIES["read_value"]).format(target=target)
            problem = f"{chart_repr}\n\n{query}"
            operation = "pictograph_read"

        elif question_type == "compare":
            cat1, cat2 = random.sample(categories, 2)
            c1, c2 = symbol_counts[cat1], symbol_counts[cat2]
            v1, v2 = actual_values[cat1], actual_values[cat2]
            steps.append(step("PICTO_COUNT", cat1, c1))
            steps.append(step("M", c1, symbol_value, v1))
            steps.append(step("PICTO_COUNT", cat2, c2))
            steps.append(step("M", c2, symbol_value, v2))
            if v1 > v2:
                diff = v1 - v2
                steps.append(step("S", v1, v2, diff))
                final_answer = f"{cat1} has {diff} more"
            elif v1 < v2:
                diff = v2 - v1
                steps.append(step("S", v2, v1, diff))
                final_answer = f"{cat2} has {diff} more"
            else:
                final_answer = f"{cat1} and {cat2} are equal"
            steps.append(step("CMP", cat1, cat2, "v1>v2" if v1 > v2 else ("v1<v2" if v1 < v2 else "equal")))
            query = random.choice(PICTOGRAPH_QUERIES["compare"]).format(a=cat1, b=cat2)
            problem = f"{chart_repr}\n\n{query}"
            operation = "pictograph_compare"

        elif question_type == "total":
            total = 0
            for cat in categories:
                count = symbol_counts[cat]
                value = actual_values[cat]
                steps.append(step("PICTO_COUNT", cat, count))
                steps.append(step("M", count, symbol_value, value))
                new_total = total + value
                steps.append(step("A", total, value, new_total))
                total = new_total
            final_answer = str(total)
            query = random.choice(PICTOGRAPH_QUERIES["total"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "pictograph_total"

        elif question_type == "difference":
            cat1, cat2 = random.sample(categories, 2)
            c1, c2 = symbol_counts[cat1], symbol_counts[cat2]
            v1, v2 = actual_values[cat1], actual_values[cat2]
            steps.append(step("PICTO_COUNT", cat1, c1))
            steps.append(step("M", c1, symbol_value, v1))
            steps.append(step("PICTO_COUNT", cat2, c2))
            steps.append(step("M", c2, symbol_value, v2))
            diff = abs(v1 - v2)
            if v1 >= v2:
                steps.append(step("S", v1, v2, diff))
            else:
                steps.append(step("S", v2, v1, diff))
            final_answer = str(diff)
            query = random.choice(PICTOGRAPH_QUERIES["difference"]).format(a=cat1, b=cat2)
            problem = f"{chart_repr}\n\n{query}"
            operation = "pictograph_difference"

        else:  # max
            max_val = max(actual_values.values())
            max_cat = [k for k, v in actual_values.items() if v == max_val][0]
            for cat in categories:
                count = symbol_counts[cat]
                value = actual_values[cat]
                steps.append(step("PICTO_COUNT", cat, count))
                steps.append(step("M", count, symbol_value, value))
            steps.append(step("GRAPH_MAX", max_cat, max_val))
            final_answer = f"{max_cat} ({max_val})"
            query = random.choice(PICTOGRAPH_QUERIES["max"])
            problem = f"{chart_repr}\n\n{query}"
            operation = "pictograph_max"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

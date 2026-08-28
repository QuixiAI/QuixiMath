"""Read, compare, and interpret fixed-column text box plots.

Variants: ``read_summary``, ``iqr_from_plot``, ``percent_region``, ``shape``,
``compare_two``, ``outliers_marked``, and ``from_description``. Op-codes:
``STAT_SETUP``, ``RULE``, ``PLOT_READ``, ``S``, ``CHECK``, and ``Z``.
Summaries are strictly ordered integers on scales at most 40 units wide;
shape uses the stated whisker-then-box-half rule, and marked outliers lie
outside the whiskers. Random summaries, contexts, settings, targets, and four
phrasings give unbounded capacity.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from stats_common import RULES, render_box_plot, render_box_plots


STATISTICS = True
CONTEXTS = ("ages", "battery lifetimes", "commute times", "daily sales",
            "package weights", "plant heights", "points per game",
            "quiz scores", "rainfall readings", "shoe sizes")
SETTINGS = ("amber study", "birch survey", "cedar trial", "delta project",
            "ember lab", "forest audit", "granite program", "harbor test",
            "indigo review", "jade pilot", "kestrel study", "lunar trial")
QUERIES = {
    "read_summary": (
        "Read the complete five-number summary.",
        "Use the symbol columns to report min, Q1, median, Q3, and max.",
        "Decode all five landmarks from the box plot.",
        "Give the exact five-number summary shown by the display.",
    ),
    "iqr_from_plot": (
        "Find the interquartile range from the plot.",
        "Read Q1 and Q3, then compute IQR.",
        "Subtract the first quartile from the third quartile.",
        "Use the box endpoints to determine the exact IQR.",
    ),
    "percent_region": (
        "What percent of observations lie in the stated quartile region?",
        "Use quartile areas to find the percentage in the target region.",
        "Determine the fixed box-plot percentage for the named interval.",
        "Count the quartile sections in the target region and report a percent.",
    ),
    "shape": (
        "Apply the stated rule to classify the plot's shape.",
        "Compare whiskers first, then box halves, and give a numerical witness.",
        "Determine left-skewed, right-skewed, or symmetric from the exact lengths.",
        "Use the supplied shape rule and report the decisive comparison.",
    ),
    "compare_two": (
        "Choose the plot with the larger stated feature and show both values.",
        "Compare A and B using the named target.",
        "Which display has the greater requested statistic?",
        "Read both plots and give the winning label with a numerical comparison.",
    ),
    "outliers_marked": (
        "List every marked outlier in ascending order.",
        "Read the o symbols and report the outlier values.",
        "Which values are explicitly marked outside the whiskers?",
        "Use the scale columns to identify all plotted outliers.",
    ),
    "from_description": (
        "Compute both the IQR and the full range from the description.",
        "Use the five stated landmarks to find IQR and range.",
        "Subtract the quartiles and endpoints to report both spreads.",
        "Find the two exact spreads without drawing the box plot.",
    ),
}


def _summary(base=None, shape=None):
    base = random.randint(8, 75) if base is None else base
    if shape == "symmetric":
        whisker = random.randint(2, 5)
        half = random.randint(2, 5)
        widths = (whisker, half, half, whisker)
    elif shape == "right-skewed":
        left_whisker = random.randint(2, 4)
        right_whisker = random.randint(left_whisker + 1, 7)
        widths = (left_whisker, random.randint(2, 5),
                  random.randint(2, 5), right_whisker)
    elif shape == "left-skewed":
        right_whisker = random.randint(2, 4)
        left_whisker = random.randint(right_whisker + 1, 7)
        widths = (left_whisker, random.randint(2, 5),
                  random.randint(2, 5), right_whisker)
    else:
        widths = tuple(random.randint(2, 6) for _ in range(4))
    values = [base]
    for width in widths:
        values.append(values[-1] + width)
    return tuple(values)


def _summary_answer(summary):
    minimum, q1, median, q3, maximum = summary
    return (f"min = {minimum}, Q1 = {q1}, median = {median}, "
            f"Q3 = {q3}, max = {maximum}")


def _read_summary_steps(summary, label="Plot"):
    names = ("min", "Q1", "median", "Q3", "max")
    return [step("PLOT_READ", f"{label} {name}", f"column value {value}", value)
            for name, value in zip(names, summary)]


def _shape(summary):
    minimum, q1, median, q3, maximum = summary
    left_whisker, right_whisker = q1 - minimum, maximum - q3
    if left_whisker != right_whisker:
        if right_whisker > left_whisker:
            return ("right-skewed",
                    f"right whisker {right_whisker} > left whisker {left_whisker}")
        return ("left-skewed",
                f"left whisker {left_whisker} > right whisker {right_whisker}")
    left_box, right_box = median - q1, q3 - median
    if right_box > left_box:
        return ("right-skewed",
                f"right box half {right_box} > left box half {left_box}")
    if left_box > right_box:
        return ("left-skewed",
                f"left box half {left_box} > right box half {right_box}")
    return ("symmetric",
            f"whiskers {left_whisker} = {right_whisker}; box halves "
            f"{left_box} = {right_box}")


class BoxPlotGenerator(ProblemGenerator):
    """Generate exact text box-plot reading and comparison exercises."""

    VARIANTS = ("read_summary", "iqr_from_plot", "percent_region", "shape",
                "compare_two", "outliers_marked", "from_description")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _single(variant):
        wanted_shape = (random.choice(("left-skewed", "right-skewed", "symmetric"))
                        if variant == "shape" else None)
        summary = _summary(shape=wanted_shape)
        outliers = ()
        if variant == "outliers_marked":
            gaps = random.sample((2, 3, 4), random.randint(1, 2))
            choices = [summary[0] - gaps[0]]
            if len(gaps) == 2:
                choices.append(summary[-1] + gaps[1])
            elif random.choice((True, False)):
                choices[0] = summary[-1] + gaps[0]
            outliers = tuple(sorted(choices))
        context = random.choice(CONTEXTS)
        reading = RULES["box plot"]
        plot = render_box_plot(summary, outliers=outliers)
        prefix = (f"At the {random.choice(SETTINGS)}, the box plot shows "
                  f"{context}. Reading rule: {reading}.\n{plot}")
        steps = [step("STAT_SETUP", f"box plot of {context}", variant),
                 step("RULE", "box plot", reading)]
        steps.extend(_read_summary_steps(summary))
        if variant == "read_summary":
            answer = _summary_answer(summary)
        elif variant == "iqr_from_plot":
            iqr = summary[3] - summary[1]
            steps.extend([step("S", summary[3], summary[1], iqr),
                          step("CHECK", "IQR", iqr)])
            answer = str(iqr)
        elif variant == "percent_region":
            regions = (("Q1 to max", 75), ("min to median", 50),
                       ("median to max", 50), ("Q1 to Q3", 50),
                       ("min to Q3", 75))
            region, percent = random.choice(regions)
            prefix += (f"\nQuartile rule: each of the four sections contains "
                       f"25% of the observations. Target region: {region}.")
            steps.extend([step("RULE", "quartile sections", "25% each"),
                          step("PLOT_READ", "target region", region),
                          step("CHECK", "25% per quartile section",
                               f"{percent}%")])
            answer = f"{percent}%"
        elif variant == "shape":
            shape_rule = ("compare whisker lengths first; if tied, compare box "
                          "halves; longer right means right-skewed, longer left "
                          "means left-skewed, and a second tie means symmetric")
            prefix += f"\nShape rule: {shape_rule}."
            label, witness = _shape(summary)
            steps.extend([step("RULE", "shape", shape_rule),
                          step("CHECK", "shape comparison", witness, label)])
            answer = f"{label}; {witness}"
        else:
            for value in outliers:
                steps.append(step("PLOT_READ", "outlier o", f"column value {value}",
                                  value))
            steps.append(step("CHECK", "outside whiskers",
                              ", ".join(map(str, outliers))))
            answer = "outliers: " + ", ".join(map(str, outliers))
        return prefix, steps, answer

    @staticmethod
    def _compare():
        base = random.randint(8, 65)
        while True:
            first, second = _summary(base), _summary(base + random.randint(0, 3))
            target = random.choice(("median", "IQR"))
            first_value = first[2] if target == "median" else first[3] - first[1]
            second_value = second[2] if target == "median" else second[3] - second[1]
            if first_value != second_value and max(first[-1], second[-1]) - min(
                    first[0], second[0]) <= 35:
                break
        context = random.choice(CONTEXTS)
        reading = RULES["box plot"]
        plot = render_box_plots((("A", first), ("B", second)))
        prefix = (f"At the {random.choice(SETTINGS)}, two box plots show "
                  f"{context}. Reading rule: {reading}. Compare target: "
                  f"{target}.\n{plot}")
        steps = [step("STAT_SETUP", f"compare box plots of {context}", target),
                 step("RULE", "box plot", reading)]
        steps.extend(_read_summary_steps(first, "A"))
        steps.extend(_read_summary_steps(second, "B"))
        winner = "A" if first_value > second_value else "B"
        high, low = max(first_value, second_value), min(first_value, second_value)
        steps.append(step("CHECK", f"larger {target}", f"{high} > {low}", winner))
        answer = f"{winner}; {target} {high} > {low}"
        return prefix, steps, answer

    @staticmethod
    def _description():
        summary = _summary()
        minimum, q1, median, q3, maximum = summary
        context = random.choice(CONTEXTS)
        prefix = (f"At the {random.choice(SETTINGS)}, a box plot of {context} "
                  f"is described by min={minimum}, Q1={q1}, median={median}, "
                  f"Q3={q3}, max={maximum}.")
        iqr, data_range = q3 - q1, maximum - minimum
        steps = [
            step("STAT_SETUP", f"described box plot of {context}",
                 _summary_answer(summary)),
            step("PLOT_READ", "Q1 and Q3", f"{q1}, {q3}"),
            step("S", q3, q1, iqr),
            step("PLOT_READ", "min and max", f"{minimum}, {maximum}"),
            step("S", maximum, minimum, data_range),
            step("CHECK", "spreads", f"IQR {iqr}, range {data_range}"),
        ]
        answer = f"IQR = {iqr}; range = {data_range}"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "compare_two":
            prefix, steps, answer = self._compare()
        elif variant == "from_description":
            prefix, steps, answer = self._description()
        else:
            prefix, steps, answer = self._single(variant)
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_box_plot_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

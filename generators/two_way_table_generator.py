"""Read and complete aligned two-way frequency tables.

Variants: ``marginal``, ``joint_relative``, ``conditional_row``,
``conditional_col``, ``fill_missing_cell``, and ``association_check``.
Tables may be 2x2, 2x3, 3x2, or 3x3 and always show row, column, and grand
totals. Requested percents are constructed to be integers or one-decimal
values. Association uses the stated rule that differing row-conditional
percents in a 2x2 table indicate association. Random shapes, counts, labels,
targets, sites, and four phrasings give unbounded capacity.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import pct
from stats_common import num_txt, render_two_way, running_sum_steps


STATISTICS = True
TOTALS = (20, 25, 40, 50, 100, 200)
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
CONTEXTS = (
    ("Grade", ("Grade 9", "Grade 10", "Grade 11"),
     "Response", ("Yes", "No", "Maybe")),
    ("Shift", ("Day", "Evening", "Night"),
     "Travel", ("Car", "Bus", "Walk")),
    ("Program", ("Program A", "Program B", "Program C"),
     "Result", ("Pass", "Review", "Retry")),
    ("Region", ("North", "Central", "South"),
     "Choice", ("Option A", "Option B", "Option C")),
    ("Team", ("Team Red", "Team Blue", "Team Gold"),
     "Outcome", ("Win", "Draw", "Loss")),
    ("Group", ("Group 1", "Group 2", "Group 3"),
     "Method", ("Online", "Hybrid", "In person")),
)
QUERIES = {
    "marginal": (
        "Find the target row's marginal total.",
        "Add across the named row and report its count.",
        "What is the row margin for the target category?",
        "Use the displayed cells to calculate the requested marginal count.",
    ),
    "joint_relative": (
        "Find the target cell's joint relative frequency as a percent.",
        "What percent of the full table lies in the named intersection?",
        "Divide the target joint count by the grand total and convert to percent.",
        "Report the intersection's relative frequency for all observations.",
    ),
    "conditional_row": (
        "What percent of the target row lies in the target column?",
        "Compute the target-column percent conditional on the named row.",
        "Use the row margin as denominator for the requested percent.",
        "Find the within-row relative frequency of the target cell.",
    ),
    "conditional_col": (
        "What percent of the target column lies in the target row?",
        "Compute the target-row percent conditional on the named column.",
        "Use the column margin as denominator for the requested percent.",
        "Find the within-column relative frequency of the target cell.",
    ),
    "fill_missing_cell": (
        "Use the margins to fill the ? cell.",
        "Find the missing target count from its displayed row total.",
        "Subtract the known row cells to recover the hidden frequency.",
        "What integer belongs in the target table cell?",
    ),
    "association_check": (
        "Use the stated rule to decide whether the two variables are associated.",
        "Compare the target-column percents across the two rows.",
        "Do the row-conditional percentages provide evidence of association?",
        "Report the association label with both conditional-percent witnesses.",
    ),
}


def _site():
    return f"{random.choice(LOCATIONS)} during the {random.choice(SETTINGS)}"


def _composition(total, parts):
    cuts = sorted(random.sample(range(1, total), parts - 1))
    points = [0, *cuts, total]
    return [right - left for left, right in zip(points, points[1:])]


def _percent_is_short(numerator, denominator):
    return (Fraction(1000 * numerator, denominator)).denominator == 1


def _context(rows, cols):
    row_key, row_bank, col_key, col_bank = random.choice(CONTEXTS)
    return row_key, row_bank[:rows], col_key, col_bank[:cols]


def _generic_table(variant):
    while True:
        rows, cols = random.choice(((2, 2), (2, 3), (3, 2), (3, 3)))
        total = random.choice([value for value in TOTALS
                               if value >= rows * cols + 4])
        flat = _composition(total, rows * cols)
        cells = [flat[index * cols:(index + 1) * cols]
                 for index in range(rows)]
        row_totals = [sum(row) for row in cells]
        col_totals = [sum(cells[i][j] for i in range(rows))
                      for j in range(cols)]
        if variant == "conditional_row":
            valid = [(i, j) for i in range(rows) for j in range(cols)
                     if _percent_is_short(cells[i][j], row_totals[i])]
        elif variant == "conditional_col":
            valid = [(i, j) for i in range(rows) for j in range(cols)
                     if _percent_is_short(cells[i][j], col_totals[j])]
        else:
            valid = [(i, j) for i in range(rows) for j in range(cols)]
        if valid:
            break
    target = random.choice(valid)
    row_key, row_labels, col_key, col_labels = _context(rows, cols)
    return (row_key, row_labels, col_key, col_labels, cells, row_totals,
            col_totals, total, target)


def _association_table():
    row_key, row_labels, col_key, col_labels = _context(2, 2)
    total = random.choice((100, 200))
    if total == 100:
        first_total = random.choice((40, 50, 60))
    else:
        first_total = random.choice((80, 100, 120))
    row_totals = [first_total, total - first_total]
    first_pct = random.choice((30, 40, 50, 60, 70))
    associated = random.choice((True, False))
    if associated:
        second_pct = random.choice([value for value in (30, 40, 50, 60, 70)
                                    if value != first_pct])
    else:
        second_pct = first_pct
    first_col = [row_totals[0] * first_pct // 100,
                 row_totals[1] * second_pct // 100]
    cells = [[first_col[i], row_totals[i] - first_col[i]] for i in range(2)]
    col_totals = [sum(first_col), total - sum(first_col)]
    return (row_key, row_labels, col_key, col_labels, cells, row_totals,
            col_totals, total, (0, 0), associated)


def _table_steps(row_labels, col_labels, cells, total, missing=None):
    steps = [step("STAT_SETUP", "two-way frequency table",
                  f"{len(row_labels)}x{len(col_labels)}, n={total}")]
    for i, row in enumerate(row_labels):
        for j, col in enumerate(col_labels):
            if missing != (i, j):
                steps.append(step("TABLE_CELL", f"{row}, {col}",
                                  cells[i][j]))
    if missing is None:
        terms = [value for row in cells for value in row]
    else:
        terms = [sum(row) for row in cells]
    steps.append(step("TABLE_TOTAL", "grand",
                      " + ".join(map(str, terms)) + f" = {total}"))
    return steps


def _margin_row_step(label, values, total):
    return step("MARGIN_ROW", label, " + ".join(map(str, values)), total)


def _margin_col_step(label, values, total):
    return step("MARGIN_COL", label, " + ".join(map(str, values)), total)


class TwoWayTableGenerator(ProblemGenerator):
    """Generate exact two-way-table reading and completion exercises."""

    VARIANTS = ("marginal", "joint_relative", "conditional_row",
                "conditional_col", "fill_missing_cell", "association_check")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _ordinary(variant):
        (row_key, row_labels, col_key, col_labels, cells, row_totals,
         col_totals, total, target) = _generic_table(variant)
        i, j = target
        shown = [row[:] for row in cells]
        missing = target if variant == "fill_missing_cell" else None
        if missing is not None:
            shown[i][j] = None
        table = render_two_way(row_labels, col_labels, shown, totals=True,
                               row_totals=row_totals, col_totals=col_totals,
                               grand_total=total)
        prefix = (f"At the {_site()}, a two-way table crosses {row_key} "
                  f"(rows) with {col_key} (columns).\n{table}\nTarget row: "
                  f"{row_labels[i]}. Target column: {col_labels[j]}.")
        steps = _table_steps(row_labels, col_labels, cells, total, missing)
        cell = cells[i][j]
        if variant == "marginal":
            steps.append(_margin_row_step(row_labels[i], cells[i],
                                          row_totals[i]))
            answer = str(row_totals[i])
        elif variant == "joint_relative":
            numerator = 100 * cell
            percent = pct(Fraction(cell, total))
            steps.extend([
                step("M", cell, 100, numerator),
                step("D", numerator, total, percent.removesuffix("%")),
                step("JOINT_REL", f"{row_labels[i]} and {col_labels[j]}",
                     f"{cell}/{total}", percent),
            ])
            answer = percent
        elif variant == "conditional_row":
            numerator = 100 * cell
            percent = pct(Fraction(cell, row_totals[i]))
            steps.extend([
                _margin_row_step(row_labels[i], cells[i], row_totals[i]),
                step("M", cell, 100, numerator),
                step("D", numerator, row_totals[i],
                     percent.removesuffix("%")),
                step("COND_ROW", f"{col_labels[j]} given {row_labels[i]}",
                     f"{cell}/{row_totals[i]}", percent),
            ])
            answer = percent
        elif variant == "conditional_col":
            column = [row[j] for row in cells]
            numerator = 100 * cell
            percent = pct(Fraction(cell, col_totals[j]))
            steps.extend([
                _margin_col_step(col_labels[j], column, col_totals[j]),
                step("M", cell, 100, numerator),
                step("D", numerator, col_totals[j],
                     percent.removesuffix("%")),
                step("COND_COL", f"{row_labels[i]} given {col_labels[j]}",
                     f"{cell}/{col_totals[j]}", percent),
            ])
            answer = percent
        else:
            known = [value for index, value in enumerate(cells[i]) if index != j]
            additions, known_total = running_sum_steps(known)
            steps.extend([_margin_row_step(row_labels[i],
                                           ["?" if index == j else value
                                            for index, value in enumerate(cells[i])],
                                           row_totals[i]),
                          *additions,
                          step("S", row_totals[i], known_total, cell),
                          step("TABLE_CELL", f"{row_labels[i]}, {col_labels[j]}",
                               cell)])
            answer = str(cell)
        steps.append(step("CHECK", variant.replace("_", " "), answer))
        return prefix, steps, answer

    @staticmethod
    def _association():
        (row_key, row_labels, col_key, col_labels, cells, row_totals,
         col_totals, total, target, associated) = _association_table()
        table = render_two_way(row_labels, col_labels, cells, totals=True)
        prefix = (f"At the {_site()}, a two-way table crosses {row_key} "
                  f"(rows) with {col_key} (columns).\n{table}\nCompared "
                  f"column: {col_labels[0]}. Association rule: the variables "
                  f"are associated when this column's row-conditional "
                  f"percents differ.")
        steps = _table_steps(row_labels, col_labels, cells, total)
        steps.append(step("RULE", "association",
                          "different row-conditional percents means associated"))
        percents = []
        for i, label in enumerate(row_labels):
            cell = cells[i][0]
            numerator = 100 * cell
            percent = pct(Fraction(cell, row_totals[i]))
            percents.append(percent)
            steps.extend([
                _margin_row_step(label, cells[i], row_totals[i]),
                step("M", cell, 100, numerator),
                step("D", numerator, row_totals[i],
                     percent.removesuffix("%")),
                step("COND_ROW", f"{col_labels[0]} given {label}",
                     f"{cell}/{row_totals[i]}", percent),
            ])
        symbol = "≠" if associated else "="
        label = "associated" if associated else "not associated"
        answer = f"{label}; {percents[0]} {symbol} {percents[1]}"
        steps.extend([step("COMPARE", "row-conditional percents",
                           percents[0], percents[1]),
                      step("CHECK", "association verdict", answer)])
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "association_check":
            prefix, steps, answer = self._association()
        else:
            prefix, steps, answer = self._ordinary(variant)
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_two_way_table_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

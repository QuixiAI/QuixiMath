"""Compute exact event probabilities from generic two-way count tables.

Variants: ``joint``, ``marginal``, ``conditional_row``,
``conditional_column``, ``union``, and ``two_by_three``. Op-codes:
``TABLE_CELL``, ``TABLE_TOTAL``, ``PROB_SETUP``, ``F``, ``COND_FORMULA``,
``FRAC_BUILD``, ``IE_FORMULA``, ``A``, ``S``, and ``Z``. Random contexts,
labels, cell counts, targets, and five phrasings give an unbounded space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
TWO_BY_TWO_CONTEXTS = (
    ("students", "student", "sport", ("yes", "no"), "pet", ("yes", "no")),
    ("commuters", "commuter", "route", ("bus", "rail"), "shift", ("day", "night")),
    ("customers", "customer", "plan", ("basic", "plus"), "renewal", ("yes", "no")),
    ("plants", "plant", "light", ("sun", "shade"), "flower", ("yes", "no")),
    ("devices", "device", "system", ("ios", "android"), "status", ("online", "offline")),
    ("books", "book", "format", ("print", "digital"), "genre", ("fiction", "history")),
    ("players", "player", "team", ("red", "blue"), "result", ("win", "loss")),
    ("orders", "order", "size", ("small", "large"), "delivery", ("pickup", "ship")),
)
TWO_BY_THREE_CONTEXTS = (
    ("students", "student", "grade", ("junior", "senior"), "club", ("art", "music", "robotics")),
    ("orders", "order", "channel", ("store", "web"), "size", ("small", "medium", "large")),
    ("travelers", "traveler", "fare", ("standard", "flex"), "route", ("north", "south", "west")),
    ("readers", "reader", "format", ("print", "digital"), "topic", ("fiction", "history", "science")),
    ("athletes", "athlete", "level", ("junior", "senior"), "event", ("run", "swim", "cycle")),
    ("workers", "worker", "shift", ("day", "night"), "site", ("east", "central", "west")),
)
QUERIES = {
    "joint": (
        "Find the probability that both target conditions hold.",
        "Use the target cell to compute the joint probability.",
        "What is the exact chance of the target row and target column together?",
        "Divide the target intersection count by the grand total.",
        "Determine the joint measure of the two displayed targets.",
    ),
    "marginal": (
        "Find the marginal probability of the target row.",
        "Add across the target row and divide by the grand total.",
        "What is the exact chance that the row target holds?",
        "Compute the target-row total and its marginal probability.",
        "Determine the row event probability without conditioning.",
    ),
    "conditional_row": (
        "Find the target-column probability given the target row.",
        "Restrict to the target row and compute the conditional chance.",
        "What fraction of the target row also meets the column target?",
        "Use the row total as the denominator for the requested probability.",
        "Determine the exact column event chance given the row condition.",
    ),
    "conditional_column": (
        "Find the target-row probability given the target column.",
        "Restrict to the target column and compute the conditional chance.",
        "What fraction of the target column also meets the row target?",
        "Use the column total as the denominator for the requested probability.",
        "Determine the exact row event chance given the column condition.",
    ),
    "union": (
        "Find the probability that the target row or target column holds.",
        "Use inclusion-exclusion to compute the union of the target events.",
        "Add both target totals and subtract their shared cell.",
        "What is the exact chance of meeting at least one target condition?",
        "Determine the measure of the row-target union column-target event.",
    ),
    "two_by_three": (
        "Find the target-column marginal and the target-row probability given that column.",
        "Report the column event chance and the conditional row chance within it.",
        "Compute both the target-column measure and the requested conditional probability.",
        "Use the three-column table for a marginal-and-conditional pair.",
        "Give the exact column marginal followed by the row probability given that column.",
    ),
}


def _fraction_steps(numerator, denominator, setup_code="PROB_SETUP"):
    value = Fraction(numerator, denominator)
    raw = f"{numerator}/{denominator}"
    steps = [step(setup_code, numerator, denominator)]
    if raw != prob_txt(value):
        steps.append(step("F", raw, prob_txt(value)))
    return steps, value


class TwoWayTableProbabilityGenerator(ProblemGenerator):
    """Generate joint, marginal, conditional, and union table questions."""

    VARIANTS = ("joint", "marginal", "conditional_row",
                "conditional_column", "union", "two_by_three")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _table(variant):
        contexts = (TWO_BY_THREE_CONTEXTS if variant == "two_by_three"
                    else TWO_BY_TWO_CONTEXTS)
        plural, singular, row_key, row_values, col_key, col_values = random.choice(contexts)
        counts = {(row, col): random.randint(2, 80)
                  for row in row_values for col in col_values}
        target_row = random.choice(row_values)
        target_col = random.choice(col_values)
        total = sum(counts.values())
        cell = counts[target_row, target_col]
        row_total = sum(counts[target_row, col] for col in col_values)
        col_total = sum(counts[row, target_col] for row in row_values)

        cells = "; ".join(
            f"{row_key}={row} and {col_key}={col}: {counts[row, col]}"
            for row in row_values for col in col_values)
        prefix = (f"A table records {total} {plural}. Cells: {cells}. One "
                  f"{singular} is chosen uniformly. Target row: "
                  f"{row_key}={target_row}. Target column: "
                  f"{col_key}={target_col}.")
        steps = [step("TABLE_CELL", f"{row_key}={row}, {col_key}={col}",
                      counts[row, col])
                 for row in row_values for col in col_values]
        steps.append(step("TABLE_TOTAL", "grand",
                          " + ".join(str(counts[row, col])
                                     for row in row_values for col in col_values)
                          + f" = {total}"))

        if variant == "joint":
            extra, value = _fraction_steps(cell, total)
            steps.extend(extra)
            answer = prob_txt(value)
        elif variant == "marginal":
            steps.append(step("TABLE_TOTAL", f"{row_key}={target_row}",
                              " + ".join(str(counts[target_row, col])
                                         for col in col_values)
                              + f" = {row_total}"))
            extra, value = _fraction_steps(row_total, total)
            steps.extend(extra)
            answer = prob_txt(value)
        elif variant == "conditional_row":
            steps.append(step("TABLE_TOTAL", f"{row_key}={target_row}",
                              " + ".join(str(counts[target_row, col])
                                         for col in col_values)
                              + f" = {row_total}"))
            expression = (f"P({col_key}={target_col} given {row_key}={target_row}) "
                          f"= count(both)/count({row_key}={target_row})")
            value = Fraction(cell, row_total)
            steps.extend([step("COND_FORMULA", expression),
                          step("FRAC_BUILD", f"{cell}/{row_total}", prob_txt(value))])
            answer = prob_txt(value)
        elif variant == "conditional_column":
            steps.append(step("TABLE_TOTAL", f"{col_key}={target_col}",
                              " + ".join(str(counts[row, target_col])
                                         for row in row_values)
                              + f" = {col_total}"))
            expression = (f"P({row_key}={target_row} given {col_key}={target_col}) "
                          f"= count(both)/count({col_key}={target_col})")
            value = Fraction(cell, col_total)
            steps.extend([step("COND_FORMULA", expression),
                          step("FRAC_BUILD", f"{cell}/{col_total}", prob_txt(value))])
            answer = prob_txt(value)
        elif variant == "union":
            union_count = row_total + col_total - cell
            steps.extend([
                step("TABLE_TOTAL", f"{row_key}={target_row}",
                     " + ".join(str(counts[target_row, col]) for col in col_values)
                     + f" = {row_total}"),
                step("TABLE_TOTAL", f"{col_key}={target_col}",
                     " + ".join(str(counts[row, target_col]) for row in row_values)
                     + f" = {col_total}"),
                step("IE_FORMULA", "count(R or C) = count(R) + count(C) − count(R and C)"),
                step("A", row_total, col_total, row_total + col_total),
                step("S", row_total + col_total, cell, union_count),
            ])
            extra, value = _fraction_steps(union_count, total)
            steps.extend(extra)
            answer = prob_txt(value)
        else:
            marginal = Fraction(col_total, total)
            conditional = Fraction(cell, col_total)
            steps.append(step("TABLE_TOTAL", f"{col_key}={target_col}",
                              " + ".join(str(counts[row, target_col])
                                         for row in row_values)
                              + f" = {col_total}"))
            extra, _ = _fraction_steps(col_total, total)
            steps.extend(extra)
            expression = (f"P({row_key}={target_row} given {col_key}={target_col}) "
                          f"= count(both)/count({col_key}={target_col})")
            steps.extend([step("COND_FORMULA", expression),
                          step("FRAC_BUILD", f"{cell}/{col_total}",
                               prob_txt(conditional))])
            answer = (f"P({col_key}={target_col}) = {prob_txt(marginal)}; "
                      f"P({row_key}={target_row} given {col_key}={target_col}) = "
                      f"{prob_txt(conditional)}")
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        prefix, steps, answer = self._table(variant)
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_two_way_table_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

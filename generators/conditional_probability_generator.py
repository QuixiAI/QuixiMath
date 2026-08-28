"""Compute exact conditional probabilities from tables, tests, and formulas.

Variants: ``table``, ``bayes_positive``, ``bayes_negative``,
``given_probabilities``, ``chain_rule``, and ``reverse_conditioning``.
Op-codes: ``COND_SETUP``, ``COND_TOTAL``, ``COND_COUNT``, ``COND_FORMULA``,
``BAYES_SETUP``, ``BAYES_CELL``, ``BAYES_FORMULA``, ``A``, ``M``, ``D``,
``FRAC_BUILD``, ``CHECK``, and ``Z``. Six table contexts, random exact rates,
inventories, and five phrasings give an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, prob_txt


PROBABILITY = True
TABLE_CONTEXTS = (
    ("students", "student", "club", ("yes", "no"), "commute", ("bike", "bus")),
    ("employees", "employee", "shift", ("day", "night"), "travel", ("car", "train")),
    ("customers", "customer", "member", ("yes", "no"), "channel", ("store", "web")),
    ("patients", "patient", "exercise", ("yes", "no"), "sleep", ("good", "poor")),
    ("voters", "voter", "region", ("east", "west"), "choice", ("alpha", "beta")),
    ("devices", "device", "status", ("online", "offline"), "type", ("mobile", "desktop")),
)
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal",
          "white", "yellow")
QUERIES = {
    "table": (
        "Find the displayed conditional probability from the table.",
        "Restrict to the conditioning category and compute the exact fraction.",
        "Use the target cell over the stated marginal total.",
        "What is the exact value of the conditional probability shown?",
        "Read the numerator and denominator from the two-way table.",
    ),
    "bayes_positive": (
        "Find the probability of disease given a positive test.",
        "Use the diagnostic cells to compute the positive-test posterior.",
        "Among positive tests, find the exact fraction that are true positives.",
        "Apply Bayes through population counts for the requested positive result.",
        "Compute the disease posterior after observing a positive test.",
    ),
    "bayes_negative": (
        "Find the probability of no disease given a negative test.",
        "Use the diagnostic cells to compute the negative-test posterior.",
        "Among negative tests, find the exact fraction that are true negatives.",
        "Apply Bayes through population counts for the requested negative result.",
        "Compute the no-disease posterior after observing a negative test.",
    ),
    "given_probabilities": (
        "Find P(A given B) from the stated probabilities.",
        "Divide the intersection probability by P(B).",
        "Use the definition of conditional probability to compute the exact answer.",
        "What is the exact value of P(A given B)?",
        "Apply P(A given B) = P(A ∩ B)/P(B).",
    ),
    "chain_rule": (
        "Find the probability of the displayed ordered color sequence.",
        "Use the three-factor conditional chain rule for the draws.",
        "Multiply the successive without-replacement probabilities.",
        "What is the exact chance of drawing the colors in that order?",
        "Apply P(A)·P(B given A)·P(C given A ∩ B).",
    ),
    "reverse_conditioning": (
        "Find P(B given A) from P(A given B), P(A), and P(B).",
        "Recover the intersection, then reverse the conditioning direction.",
        "Use Bayes' rearrangement to compute the exact reverse conditional.",
        "What is the exact value of P(B given A)?",
        "Multiply P(A given B) by P(B), then divide by P(A).",
    ),
}


class ConditionalProbabilityGenerator(ProblemGenerator):
    """Generate conditional-probability calculations in six exact forms."""

    VARIANTS = ("table", "bayes_positive", "bayes_negative",
                "given_probabilities", "chain_rule", "reverse_conditioning")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _frac_step(num, den):
        value = Fraction(num, den)
        return step("FRAC_BUILD", f"{num}/{den}", exact(value)), exact(value)

    @staticmethod
    def _table():
        plural, singular, row_key, row_values, col_key, col_values = random.choice(
            TABLE_CONTEXTS)
        cells = {(row, col): random.randint(4, 80)
                 for row in row_values for col in col_values}
        target_kind = random.choice(("row_given_col", "col_given_row"))
        target_row, target_col = random.choice(row_values), random.choice(col_values)
        if target_kind == "row_given_col":
            target, given = f"{row_key}={target_row}", f"{col_key}={target_col}"
            numerator = cells[target_row, target_col]
            denominator = sum(cells[row, target_col] for row in row_values)
            total_label = f"{col_key}={target_col} total"
            total_parts = [cells[row, target_col] for row in row_values]
        else:
            target, given = f"{col_key}={target_col}", f"{row_key}={target_row}"
            numerator = cells[target_row, target_col]
            denominator = sum(cells[target_row, col] for col in col_values)
            total_label = f"{row_key}={target_row} total"
            total_parts = [cells[target_row, col] for col in col_values]
        cell_text = "; ".join(
            f"{row_key}={row} and {col_key}={col}: {cells[row, col]}"
            for row in row_values for col in col_values)
        problem = (f"A two-way table for {plural} has counts: {cell_text}. One "
                   f"{singular} is selected uniformly. Target: P({target} given {given}).")
        frac_step, answer = ConditionalProbabilityGenerator._frac_step(
            numerator, denominator)
        steps = [
            step("COND_SETUP", cell_text, f"P({target} given {given})"),
            step("COND_TOTAL", total_label,
                 " + ".join(map(str, total_parts)) + f" = {denominator}"),
            step("COND_COUNT", f"{target} and {given}", numerator),
            step("COND_FORMULA", "P(A given B) = count(A and B)/count(B)"),
            frac_step,
            step("CHECK", f"{numerator} ≤ {denominator}",
                 "valid conditional probability"),
        ]
        return problem, steps, answer

    @staticmethod
    def _bayes(variant):
        sensitivity_den = random.randint(4, 30)
        specificity_den = random.randint(4, 30)
        sensitivity = Fraction(random.randint(1, sensitivity_den - 1), sensitivity_den)
        specificity = Fraction(random.randint(1, specificity_den - 1), specificity_den)
        disease = sensitivity.denominator * random.randint(5, 80)
        no_disease = specificity.denominator * random.randint(5, 80)
        total = disease + no_disease
        true_positive = int(disease * sensitivity)
        false_negative = disease - true_positive
        true_negative = int(no_disease * specificity)
        false_positive = no_disease - true_negative
        if variant == "bayes_positive":
            target = "P(disease=yes given test positive)"
            numerator, denominator = true_positive, true_positive + false_positive
            split_label = "positive tests"
            formula = "P(disease=yes given positive) = TP/(TP + FP)"
            add_step = step("A", true_positive, false_positive, denominator)
        else:
            target = "P(disease=no given test negative)"
            numerator, denominator = true_negative, true_negative + false_negative
            split_label = "negative tests"
            formula = "P(disease=no given negative) = TN/(TN + FN)"
            add_step = step("A", true_negative, false_negative, denominator)
        frac_step, answer = ConditionalProbabilityGenerator._frac_step(
            numerator, denominator)
        problem = (f"A screening test is used for {total} people. Disease=yes "
                   f"count is {disease} and disease=no count is {no_disease}. "
                   "Sensitivity P(test positive given disease=yes) = "
                   f"{prob_txt(sensitivity)}. Specificity P(test negative given "
                   f"disease=no) = {prob_txt(specificity)}. Target: {target}.")
        steps = [
            step("BAYES_SETUP",
                 f"disease=yes {disease}, disease=no {no_disease}",
                 f"sensitivity {prob_txt(sensitivity)}, specificity {prob_txt(specificity)}",
                 target),
            step("BAYES_CELL", "true positive",
                 f"{disease} × {prob_txt(sensitivity)}", true_positive),
            step("BAYES_CELL", "false negative",
                 f"{disease} − {true_positive}", false_negative),
            step("BAYES_CELL", "true negative",
                 f"{no_disease} × {prob_txt(specificity)}", true_negative),
            step("BAYES_CELL", "false positive",
                 f"{no_disease} − {true_negative}", false_positive),
            add_step, step("BAYES_FORMULA", formula), frac_step,
            step("CHECK", split_label, f"posterior denominator = {denominator}"),
        ]
        return problem, steps, answer

    @staticmethod
    def _given_probabilities():
        denominator_b = random.randint(3, 60)
        p_b = Fraction(random.randint(1, denominator_b - 1), denominator_b)
        denominator_cond = random.randint(3, 60)
        conditional = Fraction(random.randint(1, denominator_cond - 1),
                               denominator_cond)
        intersection = p_b * conditional
        problem = (f"Events A and B have P(A ∩ B) = {prob_txt(intersection)} "
                   f"and P(B) = {prob_txt(p_b)}.")
        steps = [step("COND_SETUP", f"P(A ∩ B) = {prob_txt(intersection)}",
                      f"P(B) = {prob_txt(p_b)}", "P(A given B)"),
                 step("COND_FORMULA", "P(A given B) = P(A ∩ B)/P(B)"),
                 step("D", prob_txt(intersection), prob_txt(p_b),
                      prob_txt(conditional)),
                 step("CHECK", "intersection ≤ conditioning event",
                      f"{prob_txt(intersection)} ≤ {prob_txt(p_b)}")]
        return problem, steps, prob_txt(conditional)

    @staticmethod
    def _chain_rule():
        colors = tuple(random.sample(COLORS, 3))
        counts = tuple(random.randint(2, 10) for _ in colors)
        order = tuple(random.sample(colors, 3))
        inventory = dict(zip(colors, counts))
        total = sum(counts)
        factors = (Fraction(inventory[order[0]], total),
                   Fraction(inventory[order[1]], total - 1),
                   Fraction(inventory[order[2]], total - 2))
        first_two = factors[0] * factors[1]
        value = first_two * factors[2]
        inventory_text = ", ".join(f"{count} {color}"
                                   for color, count in zip(colors, counts))
        problem = (f"A bag has {inventory_text} balls. Three balls are drawn "
                   f"without replacement in this order: {', '.join(order)}.")
        steps = [step("COND_SETUP", f"draw order {', '.join(order)}",
                      f"counts {inventory_text}"),
                 step("COND_FORMULA",
                      "P(A then B then C) = P(A)·P(B given A)·P(C given A ∩ B)"),
                 step("M", prob_txt(factors[0]), prob_txt(factors[1]),
                      prob_txt(first_two)),
                 step("M", prob_txt(first_two), prob_txt(factors[2]),
                      prob_txt(value)),
                 step("CHECK", "ordered draw factors",
                      " × ".join(prob_txt(factor) for factor in factors),
                      prob_txt(value))]
        return problem, steps, prob_txt(value)

    @staticmethod
    def _reverse():
        only_a, intersection, only_b, neither = (random.randint(1, 100)
                                                  for _ in range(4))
        total = only_a + intersection + only_b + neither
        p_a = Fraction(only_a + intersection, total)
        p_b = Fraction(only_b + intersection, total)
        p_a_given_b = Fraction(intersection, only_b + intersection)
        p_b_given_a = Fraction(intersection, only_a + intersection)
        recovered = p_a_given_b * p_b
        problem = (f"Events A and B have P(A given B) = {prob_txt(p_a_given_b)}, "
                   f"P(A) = {prob_txt(p_a)}, and P(B) = {prob_txt(p_b)}.")
        steps = [step("COND_SETUP", f"P(A given B) = {prob_txt(p_a_given_b)}",
                      f"P(A) = {prob_txt(p_a)}, P(B) = {prob_txt(p_b)}",
                      "P(B given A)"),
                 step("COND_FORMULA",
                      "P(B given A) = P(A given B)·P(B)/P(A)"),
                 step("M", prob_txt(p_a_given_b), prob_txt(p_b),
                      prob_txt(recovered)),
                 step("D", prob_txt(recovered), prob_txt(p_a),
                      prob_txt(p_b_given_a)),
                 step("CHECK", "recovered intersection", prob_txt(recovered))]
        return problem, steps, prob_txt(p_b_given_a)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "table":
            prefix, steps, answer = self._table()
        elif variant in ("bayes_positive", "bayes_negative"):
            prefix, steps, answer = self._bayes(variant)
        elif variant == "given_probabilities":
            prefix, steps, answer = self._given_probabilities()
        elif variant == "chain_rule":
            prefix, steps, answer = self._chain_rule()
        else:
            prefix, steps, answer = self._reverse()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"conditional_probability_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

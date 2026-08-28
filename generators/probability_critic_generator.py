"""Audit seeded errors and blanks in probability-strand solutions.

Variants: ``tree_error``, ``bayes_error``, ``complement_forgotten``, and
``missing_step``. Op-codes: ``VERIFY``, ``FLAG``, ``TREE_BRANCH``,
``BRANCH_SUM``, ``BAYES_TERM``, ``BAYES_EVIDENCE``, ``POSTERIOR``,
``COMPLEMENT``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``. Source
problems come from the strand's tree, multi-hypothesis Bayes, and complement
generators; displayed errors propagate consistently from one seeded mistake.
"""
import random
import re
from fractions import Fraction

from base_generator import ProblemGenerator
from generators.bayes_multiple_hypotheses_generator import (
    BayesMultipleHypothesesGenerator,
)
from generators.complement_probability_generator import ComplementProbabilityGenerator
from generators.tree_diagram_probability_generator import TreeDiagramProbabilityGenerator
from helpers import DELIM, jid, step
from prob_common import prob_txt


PROBABILITY = True
QUERIES = {
    "tree_error": (
        "Find the first wrong branch product and repair the propagated sum.",
        "Audit the tree calculation in order and correct its final probability.",
        "Identify the seeded path-product error, then redo the branch sum.",
        "Check each favorable branch and report the exact first bad step.",
        "Correct the one erroneous tree branch and the answer based on it.",
    ),
    "bayes_error": (
        "Find the first wrong Bayes term and repair the posterior.",
        "Audit the prior-times-likelihood products before renormalizing.",
        "Identify the seeded Bayes multiplication error and redo the update.",
        "Check each hypothesis weight and report the exact first bad step.",
        "Correct the erroneous Bayes term, evidence, and target posterior.",
    ),
    "complement_forgotten": (
        "Find the omitted complement operation and repair the answer.",
        "Audit the none-event calculation and restore the missing one-minus step.",
        "Identify where the work confuses none with at least one.",
        "Check the failure product, then correct the first bad conclusion.",
        "Supply the forgotten complement and report the exact probability.",
    ),
    "missing_step": (
        "Reconstruct the blank branch calculation and complete the solution.",
        "Use the source experiment and surrounding lines to fill the blank.",
        "Recover the exact missing path product and verify the branch sum.",
        "Check the shown branch, then supply the unique omitted branch.",
        "Report the blank step, its corrected value, and the final probability.",
    ),
}


def _wrong(value):
    value = Fraction(value)
    return Fraction(value.numerator + 1, value.denominator)


def _tree_source():
    source = TreeDiagramProbabilityGenerator("exactly_one").generate()
    branches = []
    for raw in source["steps"]:
        fields = raw.split(DELIM)
        if fields[0] == "TREE_BRANCH":
            branches.append((fields[1], fields[2], Fraction(fields[3])))
    if len(branches) != 2:
        raise RuntimeError("expected two favorable exactly-one branches")
    return source, branches


def _render(header, source_problem, shown, query):
    numbered = "\n".join(f"{index}) {line}"
                           for index, line in enumerate(shown, 1))
    return (f"{header}\nSource problem: {source_problem}\n{numbered}\n{query}")


def _sum_steps(values):
    steps = []
    running = values[0]
    for value in values[1:]:
        total = running + value
        steps.append(step("A", prob_txt(running), prob_txt(value), prob_txt(total)))
        running = total
    return steps, running


class ProbabilityCriticGenerator(ProblemGenerator):
    """Generate probability calculations with one seeded error or blank."""

    VARIANTS = ("tree_error", "bayes_error", "complement_forgotten",
                "missing_step")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _tree_error():
        source, branches = _tree_source()
        bad_index = random.randrange(2)
        shown_values = [value for _, _, value in branches]
        shown_values[bad_index] = _wrong(shown_values[bad_index])
        shown_total = sum(shown_values, Fraction())
        shown = [f"Branch {label}: {expression} = {prob_txt(shown_values[index])}"
                 for index, (label, expression, _) in enumerate(branches)]
        shown.extend([
            "Add favorable branches: "
            + " + ".join(prob_txt(value) for value in shown_values)
            + f" = {prob_txt(shown_total)}",
            f"Answer: {prob_txt(shown_total)}",
        ])
        line = bad_index + 1
        label, expression, true_value = branches[bad_index]
        correct = sum((value for _, _, value in branches), Fraction())
        problem = _render(
            "A worked probability-tree solution contains one arithmetic mistake; "
            "later lines consistently use that mistaken value.",
            source["problem"], shown, random.choice(QUERIES["tree_error"]))
        steps = [step("VERIFY", index, "ok") for index in range(1, line)]
        steps.extend([
            step("FLAG", line, f"{expression} = {prob_txt(true_value)}"),
            step("TREE_BRANCH", label, expression, prob_txt(true_value)),
            step("BRANCH_SUM", " + ".join(label for label, _, _ in branches),
                 " + ".join(prob_txt(value) for _, _, value in branches),
                 prob_txt(correct)),
            step("CHECK", "favorable branches recomputed", prob_txt(correct)),
        ])
        return problem, steps, f"step {line}; {prob_txt(correct)}"

    @staticmethod
    def _bayes_error():
        source = BayesMultipleHypothesesGenerator("three_hypotheses").generate()
        terms = []
        for raw in source["steps"]:
            fields = raw.split(DELIM)
            if fields[0] == "BAYES_TERM":
                terms.append((fields[1], fields[2], Fraction(fields[3])))
        if len(terms) != 3:
            raise RuntimeError("expected three Bayes terms")
        target_match = re.search(r"Target: P\((U\d+) given [a-z]+\)",
                                 source["problem"])
        if target_match is None:
            raise RuntimeError("could not find Bayes target")
        target = target_match.group(1)
        bad_index = random.randrange(3)
        shown_values = [value for _, _, value in terms]
        shown_values[bad_index] = _wrong(shown_values[bad_index])
        shown_evidence = sum(shown_values, Fraction())
        shown_target = shown_values[[label for label, _, _ in terms].index(target)]
        shown_posterior = shown_target / shown_evidence
        shown = [f"Bayes term {label}: {expression} = {prob_txt(shown_values[index])}"
                 for index, (label, expression, _) in enumerate(terms)]
        shown.extend([
            "Evidence: " + " + ".join(prob_txt(value) for value in shown_values)
            + f" = {prob_txt(shown_evidence)}",
            f"Posterior {target}: {prob_txt(shown_target)} ÷ "
            f"{prob_txt(shown_evidence)} = {prob_txt(shown_posterior)}",
            f"Answer: {prob_txt(shown_posterior)}",
        ])
        line = bad_index + 1
        bad_label, expression, true_value = terms[bad_index]
        true_values = [value for _, _, value in terms]
        evidence = sum(true_values, Fraction())
        target_term = true_values[[label for label, _, _ in terms].index(target)]
        posterior = target_term / evidence
        first_factor, second_factor = map(Fraction, expression.split(" × "))
        problem = _render(
            "A worked Bayes solution contains one arithmetic mistake; the "
            "evidence and posterior consistently propagate it.",
            source["problem"], shown, random.choice(QUERIES["bayes_error"]))
        steps = [step("VERIFY", index, "ok") for index in range(1, line)]
        steps.extend([
            step("FLAG", line, f"{expression} = {prob_txt(true_value)}"),
            step("M", prob_txt(first_factor), prob_txt(second_factor),
                 prob_txt(true_value)),
            step("BAYES_TERM", bad_label, expression, prob_txt(true_value)),
        ])
        addition, total = _sum_steps(true_values)
        steps.extend(addition)
        steps.extend([
            step("BAYES_EVIDENCE", "sum of corrected terms", prob_txt(total)),
            step("D", prob_txt(target_term), prob_txt(evidence),
                 prob_txt(posterior)),
            step("POSTERIOR", target, "target term ÷ evidence",
                 prob_txt(posterior)),
            step("CHECK", "posterior uses corrected evidence", prob_txt(posterior)),
        ])
        return problem, steps, f"step {line}; {prob_txt(posterior)}"

    @staticmethod
    def _complement_forgotten():
        source = ComplementProbabilityGenerator("at_least_one_two_stage").generate()
        complement_rows = []
        none = None
        for raw in source["steps"]:
            fields = raw.split(DELIM)
            if fields[0] == "COMPLEMENT" and "failure" in fields[1]:
                complement_rows.append((fields[1], fields[2], Fraction(fields[3])))
            elif fields[0] == "M":
                none = Fraction(fields[3])
        if len(complement_rows) != 2 or none is None:
            raise RuntimeError("unexpected complement source flow")
        correct = 1 - none
        shown = [f"{label.capitalize()}: {expression} = {prob_txt(value)}"
                 for label, expression, value in complement_rows]
        shown.extend([
            f"Neither succeeds: {prob_txt(complement_rows[0][2])} × "
            f"{prob_txt(complement_rows[1][2])} = {prob_txt(none)}",
            f"Answer for at least one success: {prob_txt(none)}",
        ])
        line = 4
        problem = _render(
            "A worked complement solution has omitted one required operation.",
            source["problem"], shown,
            random.choice(QUERIES["complement_forgotten"]))
        steps = [step("VERIFY", index, "ok") for index in range(1, line)]
        steps.extend([
            step("FLAG", line, f"1 − {prob_txt(none)} = {prob_txt(correct)}"),
            step("S", 1, prob_txt(none), prob_txt(correct)),
            step("COMPLEMENT", "at least one success",
                 f"1 − {prob_txt(none)}", prob_txt(correct)),
            step("CHECK", "none + at least one",
                 f"{prob_txt(none)} + {prob_txt(correct)}", "1"),
        ])
        return problem, steps, f"step {line}; {prob_txt(correct)}"

    @staticmethod
    def _missing_step():
        source, branches = _tree_source()
        blank_index = random.randrange(2)
        correct = sum((value for _, _, value in branches), Fraction())
        shown = []
        for index, (label, expression, value) in enumerate(branches):
            if index == blank_index:
                shown.append("____")
            else:
                shown.append(f"Branch {label}: {expression} = {prob_txt(value)}")
        shown.extend([
            "Add favorable branches: "
            + " + ".join(prob_txt(value) for _, _, value in branches)
            + f" = {prob_txt(correct)}",
            f"Answer: {prob_txt(correct)}",
        ])
        line = blank_index + 1
        label, expression, value = branches[blank_index]
        problem = _render(
            "One line of a correct probability-tree solution is blank.",
            source["problem"], shown, random.choice(QUERIES["missing_step"]))
        steps = [step("VERIFY", index, "ok") for index in range(1, line)]
        steps.extend([
            step("FLAG", line, f"Branch {label}: {expression} = {prob_txt(value)}"),
            step("TREE_BRANCH", label, expression, prob_txt(value)),
            step("CHECK", "branch sum", prob_txt(correct)),
        ])
        answer = (f"step {line}; branch {label} = {prob_txt(value)}; "
                  f"answer {prob_txt(correct)}")
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "tree_error":
            problem, steps, answer = self._tree_error()
        elif variant == "bayes_error":
            problem, steps, answer = self._bayes_error()
        elif variant == "complement_forgotten":
            problem, steps, answer = self._complement_forgotten()
        else:
            problem, steps, answer = self._missing_step()
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_critic_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

"""Generate forced natural-deduction and Fitch-style derivations.

Variants:
- ``forward_chain`` applies ``∧E`` and ``→E`` under a stated earliest-line
  policy and reports every newly derived formula in order.
- ``justify`` blanks rule names in a complete derivation.
- ``missing_line`` removes one formula while leaving its determining rule.
- ``conditional_proof`` opens an assumption subproof and closes it with ``→I``.

Random atom selections, implication chains, derivation templates, missing-line
positions, and five phrasings yield more than 100,000 problem texts.

Op-codes:
- ``PREMISE``: number and state a premise line.
- ``APPLY``: give a rule, cited lines, and derived formula.
- ``SUBPROOF_OPEN`` / ``SUBPROOF_CLOSE``: delimit an assumption and ``→I``.
- ``CHECK``: confirm the requested conclusion or forced-chain exhaustion.
- ``Z``: exact sequence, justification list, or missing formula.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import And, Imp, Or, Var, render


FOUNDATIONS = True


ATOM_NAMES = tuple("abcdefghijklmnopqrstuvwx")

QUERIES = {
    "forward_chain": (
        "Derive every new formula in the forced order.",
        "Apply the policy until no additional line can be appended.",
        "List the complete sequence produced by forward chaining.",
        "Carry out each earliest applicable elimination step.",
        "Give all derived lines in their deterministic order.",
    ),
    "justify": (
        "Fill every blank rule justification.",
        "Name the rule and cited lines for each blank.",
        "Complete the missing Fitch-style annotations.",
        "Supply the exact justifications for the derived lines.",
        "Recover every omitted natural-deduction rule label.",
    ),
    "missing_line": (
        "Recover the missing formula from its displayed justification.",
        "Fill the blank derivation line exactly.",
        "Use the cited rule to reconstruct the omitted formula.",
        "Determine the unique formula that belongs on the blank line.",
        "Complete the proof by restoring the missing line.",
    ),
    "conditional_proof": (
        "Complete the subproof justifications and close it with →I.",
        "Fill the assumption, derived line, and conditional-proof labels.",
        "Justify each subproof line and discharge the stated assumption.",
        "Supply the exact Fitch annotations for the conditional proof.",
        "Complete the derivation through implication introduction.",
    ),
}


def rule_text(rule, citations):
    return f"{rule} {citations}" if citations else rule


def forced_chain(premises):
    """Apply the stated restart-on-first-new-line policy."""
    lines = list(premises)
    derived = []
    while True:
        candidate = None
        for source_index, formula in enumerate(lines, 1):
            if isinstance(formula, And):
                for rule, child in (("∧E₁", formula.left),
                                    ("∧E₂", formula.right)):
                    if child not in lines:
                        candidate = (child, rule, str(source_index))
                        break
                if candidate is not None:
                    break
            if isinstance(formula, Imp):
                for antecedent_index, antecedent in enumerate(lines, 1):
                    if antecedent == formula.left and formula.right not in lines:
                        candidate = (formula.right, "→E",
                                     f"{source_index},{antecedent_index}")
                        break
                if candidate is not None:
                    break
        if candidate is None:
            return lines, derived
        formula, rule, citations = candidate
        lines.append(formula)
        derived.append((len(lines), formula, rule, citations))


class NaturalDeductionGenerator(ProblemGenerator):
    """Generate line-by-line deductions with independently checkable rules."""

    VARIANTS = ("forward_chain", "justify", "missing_line",
                "conditional_proof")
    WEIGHTS = (0.35, 0.30, 0.30, 0.05)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _atoms(count):
        return [Var(name) for name in random.sample(ATOM_NAMES, count)]

    def _forward(self):
        length = random.randint(2, 5)
        atoms = self._atoms(length + 2)
        premises = [And(atoms[0], atoms[1])]
        premises.append(Imp(atoms[0], atoms[2]))
        premises.append(Imp(atoms[1], atoms[3]))
        current = atoms[2]
        for target in atoms[4:length + 2]:
            premises.append(Imp(current, target))
            current = target
        lines, derived = forced_chain(premises)
        premise_text = "; ".join(
            f"{index}. {render(formula)}"
            for index, formula in enumerate(premises, 1))
        policy = ("repeatedly scan lines from 1 upward, trying ∧E₁, then ∧E₂, "
                  "then →E with the earliest antecedent; append the first new "
                  "formula and restart")
        problem = (f"Premises in line order: {premise_text}. Policy: {policy}. "
                   f"{random.choice(QUERIES['forward_chain'])}")
        steps = [step("PREMISE", index, render(formula))
                 for index, formula in enumerate(premises, 1)]
        for line, formula, rule, citations in derived:
            steps.append(step("APPLY", rule, citations, render(formula)))
        steps.append(step("CHECK", "no new formula remains",
                          f"{len(lines)} total lines"))
        answer = "; ".join(f"{line}: {render(formula)}"
                           for line, formula, _, _ in derived)
        return problem, steps, answer

    def _base_derivation(self):
        first, second, extra, conclusion = self._atoms(4)
        conjunction = And(first, second)
        disjunction = Or(conjunction, extra)
        implication = Imp(disjunction, conclusion)
        return [
            (first, "premise", ""),
            (second, "premise", ""),
            (conjunction, "∧I", "1,2"),
            (disjunction, "∨I", "3"),
            (implication, "premise", ""),
            (conclusion, "→E", "5,4"),
        ]

    @staticmethod
    def _derivation_text(lines, blank_rules=(), blank_formula=None):
        rendered = []
        for index, (formula, rule, citations) in enumerate(lines, 1):
            formula_text = "____" if index == blank_formula else render(formula)
            justification = ("____" if index in blank_rules
                             else rule_text(rule, citations))
            rendered.append(f"{index}. {formula_text} [{justification}]")
        return "; ".join(rendered)

    def _justify(self):
        lines = self._base_derivation()
        blanks = (3, 4, 6)
        displayed = self._derivation_text(lines, blank_rules=blanks)
        problem = (f"Derivation: {displayed}. "
                   f"{random.choice(QUERIES['justify'])}")
        steps = []
        for index, (formula, rule, citations) in enumerate(lines, 1):
            if rule == "premise":
                steps.append(step("PREMISE", index, render(formula)))
            else:
                steps.append(step("APPLY", rule, citations, render(formula)))
        steps.append(step("CHECK", "all cited schemas match"))
        answer = "; ".join(
            f"{index}: {rule_text(lines[index - 1][1], lines[index - 1][2])}"
            for index in blanks)
        return problem, steps, answer

    def _missing(self):
        lines = self._base_derivation()
        missing = random.choice((3, 6))
        displayed = self._derivation_text(lines, blank_formula=missing)
        problem = (f"Derivation: {displayed}. "
                   f"{random.choice(QUERIES['missing_line'])}")
        steps = [step("PREMISE", index, render(formula))
                 if rule == "premise"
                 else step("APPLY", rule, citations, render(formula))
                 for index, (formula, rule, citations) in enumerate(lines, 1)]
        answer = f"line {missing}: {render(lines[missing - 1][0])}"
        steps.append(step("CHECK", answer, "rule schema satisfied"))
        return problem, steps, answer

    def _conditional(self):
        first, second = self._atoms(2)
        if random.choice((True, False)):
            joined = And(first, second)
            lines = [
                (first, "premise", ""),
                (second, "assumption", ""),
                (joined, "∧I", "1,2"),
                (Imp(second, joined), "→I", "2–3"),
            ]
        else:
            implication = Imp(first, second)
            lines = [
                (implication, "premise", ""),
                (first, "assumption", ""),
                (second, "→E", "1,2"),
                (implication, "→I", "2–3"),
            ]
        displayed = self._derivation_text(lines, blank_rules=(2, 3, 4))
        problem = (f"Fitch derivation: {displayed}. Lines 2–3 form one subproof. "
                   f"{random.choice(QUERIES['conditional_proof'])}")
        steps = [step("PREMISE", 1, render(lines[0][0])),
                 step("SUBPROOF_OPEN", "assume", render(lines[1][0])),
                 step("APPLY", lines[2][1], lines[2][2], render(lines[2][0])),
                 step("SUBPROOF_CLOSE", "→I", "lines 2–3",
                      render(lines[3][0])),
                 step("CHECK", "conclusion reached", render(lines[3][0]))]
        answer = "; ".join(
            f"{index}: {rule_text(lines[index - 1][1], lines[index - 1][2])}"
            for index in (2, 3, 4))
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choices(
            self.VARIANTS, weights=self.WEIGHTS, k=1)[0]
        if variant == "forward_chain":
            problem, steps, answer = self._forward()
        elif variant == "justify":
            problem, steps, answer = self._justify()
        elif variant == "missing_line":
            problem, steps, answer = self._missing()
        else:
            problem, steps, answer = self._conditional()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"natural_deduction_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

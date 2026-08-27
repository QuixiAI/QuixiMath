"""Form converses, inverses, contrapositives, and biconditional halves.

Variants:
- ``symbolic`` transforms a randomized symbolic conditional.
- ``english`` transforms a parameterized mathematical conditional.
- ``truth_with_counterexample`` tests a converse and finds its first witness.
- ``biconditional_split`` writes an iff statement as two implications.

The symbolic formula builder and bounded divisibility families give a problem
space above 100,000.  Each variant has five phrasings.

Op-codes:
- ``COND_PARTS``: identify hypothesis and conclusion.
- ``FORM``: construct the requested conditional form.
- ``DIV_CHECK`` / ``TRY`` / ``REJECT`` / ``ACCEPT``: verify a false converse.
- ``COUNTEREXAMPLE``: record the first witness.
- ``Z``: exact transformed sentence/formula or composite verdict.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import And, Iff, Imp, Not, Or, random_formula, render


FOUNDATIONS = True


QUERIES = {
    "symbolic": (
        "Write the requested conditional form.",
        "Transform the hypothesis and conclusion as requested.",
        "Give the canonical symbolic result.",
        "Identify the two parts, then construct the named form.",
        "Rewrite the conditional without changing the requested form's meaning.",
    ),
    "english": (
        "Write the requested form as a complete mathematical sentence.",
        "Transform the hypothesis and conclusion in words.",
        "State the named conditional form.",
        "Identify the two clauses, then rewrite them as requested.",
        "Give the corresponding conditional sentence.",
    ),
    "truth_with_counterexample": (
        "Decide whether the converse is true and give its first counterexample.",
        "Scan eligible values in order to test the converse.",
        "Refute the converse with the smallest witness in the stated domain.",
        "Determine the converse's truth and report the earliest failure.",
        "Test the reversed implication and give its first counterexample.",
    ),
    "biconditional_split": (
        "Split the biconditional into its two conditional directions.",
        "Write the forward and reverse implications.",
        "Replace the iff statement by two conditionals.",
        "Identify both directions of the biconditional.",
        "Give the pair of implications equivalent to the displayed iff.",
    ),
}


class ConditionalFormsGenerator(ProblemGenerator):
    """Generate canonical conditional transformations and bounded truth scans."""

    VARIANTS = ("symbolic", "english", "truth_with_counterexample",
                "biconditional_split")
    FORMS = ("converse", "inverse", "contrapositive")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _formula_pair():
        while True:
            left = random_formula(depth=random.randint(1, 3), names=("p", "q", "r"),
                                  connectives=("¬", "∧", "∨"))
            right = random_formula(depth=random.randint(1, 3), names=("p", "q", "r"),
                                   connectives=("¬", "∧", "∨"))
            if left != right:
                return left, right

    @staticmethod
    def _symbolic_form(hypothesis, conclusion, form):
        if form == "converse":
            return Imp(conclusion, hypothesis)
        if form == "inverse":
            return Imp(Not(hypothesis), Not(conclusion))
        return Imp(Not(conclusion), Not(hypothesis))

    def _symbolic(self):
        hypothesis, conclusion = self._formula_pair()
        form = random.choice(self.FORMS)
        conditional = render(Imp(hypothesis, conclusion))
        result = render(self._symbolic_form(hypothesis, conclusion, form))
        problem = (
            f"Conditional: {conditional}. Requested form: {form}. "
            f"{random.choice(QUERIES['symbolic'])}"
        )
        steps = [step("COND_PARTS", render(hypothesis), render(conclusion)),
                 step("FORM", form, result)]
        return problem, steps, result

    @staticmethod
    def _english_pair():
        kind = random.choice(("divisibility", "threshold", "even"))
        if kind == "divisibility":
            base = random.randint(2, 500)
            stronger = base * random.randint(2, 20)
            return (f"n is divisible by {stronger}",
                    f"n is divisible by {base}",
                    f"n is not divisible by {stronger}",
                    f"n is not divisible by {base}")
        if kind == "threshold":
            lower = random.randint(-500, 500)
            upper = lower + random.randint(1, 100)
            return (f"n > {upper}", f"n > {lower}",
                    f"n ≤ {upper}", f"n ≤ {lower}")
        factor = random.randint(2, 1000)
        if factor % 2:
            factor += 1
        return (f"n is divisible by {factor}", "n is even",
                f"n is not divisible by {factor}", "n is odd")

    @staticmethod
    def _english_result(hypothesis, conclusion, neg_h, neg_c, form):
        if form == "converse":
            return f"If {conclusion}, then {hypothesis}."
        if form == "inverse":
            return f"If {neg_h}, then {neg_c}."
        return f"If {neg_c}, then {neg_h}."

    def _english(self):
        hypothesis, conclusion, neg_h, neg_c = self._english_pair()
        form = random.choice(self.FORMS)
        conditional = f"If {hypothesis}, then {conclusion}."
        result = self._english_result(hypothesis, conclusion, neg_h, neg_c, form)
        problem = (
            f"Conditional: {conditional} Requested form: {form}. "
            f"{random.choice(QUERIES['english'])}"
        )
        steps = [step("COND_PARTS", hypothesis, conclusion),
                 step("FORM", form, result)]
        return problem, steps, result

    def _truth(self):
        base = random.randint(2, 100)
        stronger = base * random.randint(2, 12)
        lower = random.randint(1, 2000)
        first = ((lower + base - 1) // base) * base
        candidates = [first + index * base for index in range(12)]
        counterexample = next(value for value in candidates
                              if value % stronger != 0)
        problem = (
            f"Conditional: If n is divisible by {stronger}, then n is divisible "
            f"by {base}, for integers n ≥ {lower}. Consider its converse and scan "
            f"multiples of {base} in increasing order. "
            f"{random.choice(QUERIES['truth_with_counterexample'])}"
        )
        converse = (f"If n is divisible by {base}, then n is divisible by "
                    f"{stronger}.")
        steps = [step("COND_PARTS", f"n divisible by {stronger}",
                      f"n divisible by {base}"),
                 step("FORM", "converse", converse)]
        for value in candidates:
            remainder = value % stronger
            steps.append(step("DIV_CHECK", value, stronger,
                              f"quotient {value // stronger}, remainder {remainder}"))
            failed = remainder != 0
            steps.append(step("TRY", f"n = {value}",
                              "converse fails" if failed else "converse holds"))
            if failed:
                steps.append(step("ACCEPT", f"n = {value}", "counterexample"))
                break
            steps.append(step("REJECT", f"n = {value}", "not a counterexample"))
        witness = (f"{counterexample} is divisible by {base} but not by "
                   f"{stronger}")
        steps.append(step("COUNTEREXAMPLE", f"n = {counterexample}", witness))
        answer = f"converse: false; counterexample n = {counterexample} ({witness})"
        return problem, steps, answer

    def _biconditional(self):
        left, right = self._formula_pair()
        biconditional = render(Iff(left, right))
        forward, reverse = render(Imp(left, right)), render(Imp(right, left))
        problem = (
            f"Biconditional: {biconditional}. "
            f"{random.choice(QUERIES['biconditional_split'])}"
        )
        steps = [step("COND_PARTS", render(left), render(right)),
                 step("FORM", "forward", forward),
                 step("FORM", "reverse", reverse)]
        answer = f"{forward}; {reverse}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        builders = {"symbolic": self._symbolic, "english": self._english,
                    "truth_with_counterexample": self._truth,
                    "biconditional_split": self._biconditional}
        problem, steps, answer = builders[variant]()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"conditional_forms_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

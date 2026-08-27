"""Write canonical algebra for elementary direct-proof patterns.

Variants:
- ``parity_sum`` and ``parity_product`` prove parity from integer witnesses.
- ``consecutive_product_even`` handles both parity cases for ``n(n+1)``.
- ``divisibility_transitive`` substitutes divisibility witnesses.
- ``contrapositive_setup`` states the negated conclusion and negated premise.
- ``contradiction_setup`` states a canonical contradictory assumption.

Op-codes:
- ``REPRESENT``: introduce an integer/parity/divisibility witness.
- ``EXPAND``: multiply or add the represented forms.
- ``FACTOR``: expose the parity or divisibility factor.
- ``ASSUME`` / ``GOAL`` / ``SETUP``: establish an indirect-proof framework.
- ``CONCLUDE``: state the property established by the algebra.
- ``Z``: exact factored form or canonical setup sentence.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


SYMBOLS = tuple("abcdefghjkmnpqrstuvwxyz")

QUERIES = {
    "parity_sum": (
        "Write the direct algebraic proof.",
        "Add the witness forms, factor 2, and conclude the parity.",
        "Show the required parity using the displayed integer witnesses.",
        "Expand and refactor the sum into canonical parity form.",
        "Complete the direct parity argument without skipping algebra.",
    ),
    "parity_product": (
        "Write the direct algebraic proof for the product.",
        "Multiply the witness forms and refactor into parity form.",
        "Use the displayed integer witnesses to establish the product's parity.",
        "Expand, factor 2 when needed, and conclude.",
        "Complete the product-parity argument algebraically.",
    ),
    "consecutive_product_even": (
        "Prove the product is even by covering both parity cases.",
        "Write the factored product when n is even and when n is odd.",
        "Use the two parity representations to establish a factor of 2.",
        "Complete the cases proof for two consecutive integers.",
        "Show algebraically that one of n and n+1 contributes a factor 2.",
    ),
    "divisibility_transitive": (
        "Substitute the witnesses to prove the divisibility conclusion.",
        "Write the direct algebra showing that the first integer divides the third.",
        "Use the two divisibility equations and combine their integer factors.",
        "Complete the transitivity proof from the stated witnesses.",
        "Express the third integer as the first times an integer.",
    ),
    "contrapositive_setup": (
        "State the canonical assumption and goal for a proof by contraposition.",
        "Rewrite the implication as its contrapositive proof setup.",
        "Give exactly what to assume and what to prove.",
        "Set up the indirect direction by negating conclusion then premise.",
        "Identify the contrapositive hypothesis and target.",
    ),
    "contradiction_setup": (
        "State the canonical first assumption for a proof by contradiction.",
        "Negate the claim and give the algebraic contradiction setup.",
        "Write the assumption that begins the contradiction argument.",
        "Set up the proof by assuming the claim is false.",
        "Give the canonical contradictory assumption and first consequence.",
    ),
}


def choose_symbols(count):
    return random.sample(SYMBOLS, count)


def parity_form(number, witness, parity):
    return f"{number} = 2{witness}" + (" + 1" if parity == "odd" else "")


class DirectProofAlgebraGenerator(ProblemGenerator):
    """Generate symbolic direct-proof records with exact canonical targets."""

    VARIANTS = ("parity_sum", "parity_product", "consecutive_product_even",
                "divisibility_transitive", "contrapositive_setup",
                "contradiction_setup")
    WEIGHTS = (0.24, 0.24, 0.01, 0.27, 0.02, 0.22)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _parity_sum(self):
        first, second, first_witness, second_witness = choose_symbols(4)
        first_parity, second_parity = random.choice(
            (("odd", "odd"), ("even", "even"), ("odd", "even"),
             ("even", "odd")))
        first_bit = 1 if first_parity == "odd" else 0
        second_bit = 1 if second_parity == "odd" else 0
        total_bit = (first_bit + second_bit) % 2
        conclusion = "odd" if total_bit else "even"
        first_form = parity_form(first, first_witness, first_parity)
        second_form = parity_form(second, second_witness, second_parity)
        constant = first_bit + second_bit
        expanded = (f"2{first_witness} + 2{second_witness}"
                    + (f" + {constant}" if constant else ""))
        inside = f"{first_witness} + {second_witness}"
        if constant == 2:
            inside += " + 1"
        factored = f"2({inside})" + (" + 1" if total_bit else "")
        problem = (f"Let {first_form} and {second_form}, where the witnesses "
                   f"are integers. Prove {first} + {second} is {conclusion}. "
                   f"{random.choice(QUERIES['parity_sum'])}")
        steps = [step("REPRESENT", f"{first_parity} {first}", first_form),
                 step("REPRESENT", f"{second_parity} {second}", second_form),
                 step("EXPAND", f"{first} + {second}", expanded),
                 step("FACTOR", factored), step("CONCLUDE", conclusion)]
        return problem, steps, factored

    def _parity_product(self):
        first, second, first_witness, second_witness = choose_symbols(4)
        first_parity, second_parity = random.choice(
            (("odd", "odd"), ("even", "even"), ("odd", "even"),
             ("even", "odd")))
        first_form = parity_form(first, first_witness, first_parity)
        second_form = parity_form(second, second_witness, second_parity)
        if first_parity == second_parity == "odd":
            expanded = (f"4{first_witness}{second_witness} + 2{first_witness} "
                        f"+ 2{second_witness} + 1")
            factored = (f"2(2{first_witness}{second_witness} + {first_witness} "
                        f"+ {second_witness}) + 1")
            conclusion = "odd"
        elif first_parity == "even" and second_parity == "even":
            expanded = f"4{first_witness}{second_witness}"
            factored = f"2(2{first_witness}{second_witness})"
            conclusion = "even"
        elif first_parity == "even":
            expanded = (f"4{first_witness}{second_witness} "
                        f"+ 2{first_witness}")
            factored = f"2{first_witness}(2{second_witness} + 1)"
            conclusion = "even"
        else:
            expanded = (f"4{first_witness}{second_witness} "
                        f"+ 2{second_witness}")
            factored = f"2{second_witness}(2{first_witness} + 1)"
            conclusion = "even"
        problem = (f"Let {first_form} and {second_form}, where the witnesses "
                   f"are integers. Prove {first}{second} is {conclusion}. "
                   f"{random.choice(QUERIES['parity_product'])}")
        steps = [step("REPRESENT", f"{first_parity} {first}", first_form),
                 step("REPRESENT", f"{second_parity} {second}", second_form),
                 step("EXPAND", f"{first}{second}", expanded),
                 step("FACTOR", factored), step("CONCLUDE", conclusion)]
        return problem, steps, factored

    def _consecutive(self):
        number, witness = choose_symbols(2)
        even_factor = f"2{witness}(2{witness} + 1)"
        odd_factor = f"2({witness} + 1)(2{witness} + 1)"
        problem = (f"Let {number} be an integer and use integer witness {witness} "
                   f"in the parity cases. Prove {number}({number} + 1) is even. "
                   f"{random.choice(QUERIES['consecutive_product_even'])}")
        steps = [step("REPRESENT", f"case {number} even",
                      f"{number} = 2{witness}"),
                 step("EXPAND", f"{number}({number} + 1)", even_factor),
                 step("FACTOR", even_factor),
                 step("REPRESENT", f"case {number} odd",
                      f"{number} = 2{witness} + 1"),
                 step("EXPAND", f"{number}({number} + 1)", odd_factor),
                 step("FACTOR", odd_factor), step("CONCLUDE", "even in both cases")]
        return problem, steps, f"{even_factor}; {odd_factor}"

    def _divisibility(self):
        first, second, third, first_witness, second_witness = choose_symbols(5)
        first_equation = f"{second} = {first}{first_witness}"
        second_equation = f"{third} = {second}{second_witness}"
        factored = f"{third} = {first}({first_witness}{second_witness})"
        problem = (f"Let {first}, {second}, {third} be integers. Suppose "
                   f"{first} ∣ {second} and {second} ∣ {third}, with "
                   f"{first_equation} and {second_equation}. Prove "
                   f"{first} ∣ {third}. "
                   f"{random.choice(QUERIES['divisibility_transitive'])}")
        steps = [step("REPRESENT", f"{first} ∣ {second}", first_equation),
                 step("REPRESENT", f"{second} ∣ {third}", second_equation),
                 step("EXPAND", second_equation,
                      f"{third} = ({first}{first_witness}){second_witness}"),
                 step("FACTOR", factored), step("CONCLUDE", f"{first} ∣ {third}")]
        return problem, steps, factored

    def _contrapositive(self):
        names = choose_symbols(2)
        number, other = names
        templates = (
            (f"If {number}² is odd, then {number} is odd",
             f"assume {number} is even; show {number}² is even"),
            (f"If {number}² is even, then {number} is even",
             f"assume {number} is odd; show {number}² is odd"),
            (f"If {number} + 1 is odd, then {number} is even",
             f"assume {number} is odd; show {number} + 1 is even"),
            (f"If {number}{other} is odd, then {number} and {other} are odd",
             f"assume {number} is even or {other} is even; "
             f"show {number}{other} is even"),
        )
        theorem, answer = random.choice(templates)
        assumption, goal = answer.split("; ")
        problem = (f"Theorem: {theorem}. "
                   f"{random.choice(QUERIES['contrapositive_setup'])}")
        steps = [step("ASSUME", assumption), step("GOAL", goal),
                 step("SETUP", answer)]
        return problem, steps, answer

    def _contradiction(self):
        number, first_witness, second_witness = choose_symbols(3)
        prime = random.choice((2, 3, 5, 7, 11, 13, 17, 19))
        templates = (
            (f"No integer {number} is both even and odd",
             f"assume {number} is both even and odd; write {number} = "
             f"2{first_witness} = 2{second_witness} + 1"),
            ("There is no greatest integer",
             f"assume {number} is the greatest integer; consider {number} + 1"),
            (f"The sum of rational {first_witness} and irrational {number} is irrational",
             f"assume {first_witness} + {number} is rational; then {number} = "
             f"({first_witness} + {number}) − {first_witness} would be rational"),
            (f"√{prime} is irrational",
             f"assume √{prime} = {first_witness}/{second_witness} in lowest terms; "
             f"derive {prime}{second_witness}² = {first_witness}²"),
        )
        theorem, answer = random.choice(templates)
        problem = (f"Claim: {theorem}. Setup symbols: {number}, "
                   f"{first_witness}, {second_witness}. "
                   f"{random.choice(QUERIES['contradiction_setup'])}")
        steps = [step("ASSUME", answer.split("; ")[0]),
                 step("SETUP", answer)]
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choices(self.VARIANTS,
                                                 weights=self.WEIGHTS, k=1)[0]
        if variant == "parity_sum":
            problem, steps, answer = self._parity_sum()
        elif variant == "parity_product":
            problem, steps, answer = self._parity_product()
        elif variant == "consecutive_product_even":
            problem, steps, answer = self._consecutive()
        elif variant == "divisibility_transitive":
            problem, steps, answer = self._divisibility()
        elif variant == "contrapositive_setup":
            problem, steps, answer = self._contrapositive()
        else:
            problem, steps, answer = self._contradiction()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"direct_proof_algebra_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

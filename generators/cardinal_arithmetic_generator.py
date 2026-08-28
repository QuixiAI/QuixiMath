"""Infinite-cardinal arithmetic and standard set cardinalities.

Variants are ``add_multiply``, ``exponent``, and ``set_cardinality``.  The
trace vocabulary is ``CARD_RULE`` plus ``REWRITE`` and exact finite ``A``/``M``
steps when a prefix contains only finite cardinals.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "add_multiply": (
        "Evaluate the expression as a cardinal.",
        "Apply the infinite-cardinal maximum rule from left to right.",
        "Determine the resulting cardinal.",
        "Simplify the cardinal sum or product.",
        "Compute the expression using exact cardinal arithmetic.",
    ),
    "exponent": (
        "Evaluate the cardinal exponentiation.",
        "Apply the stated exponentiation identity.",
        "Determine the resulting cardinal power.",
        "Simplify the cardinal exponential expression.",
        "Compute the power in canonical cardinal notation.",
    ),
    "set_cardinality": (
        "Determine the cardinality of the described set.",
        "Classify the set as countable or continuum-sized.",
        "Compute the set cardinality using the supplied construction.",
        "Apply the relevant finite-product, sequence, or power-set rule.",
        "Give the exact infinite cardinal of the set.",
    ),
}


INFINITE_RANK = {"ℵ0": 1, "c": 2, "2^c": 3}


def cardinal_text(value):
    return str(value)


def combine_cardinals(left, right, operator):
    left_infinite = isinstance(left, str)
    right_infinite = isinstance(right, str)
    if not left_infinite and not right_infinite:
        return left + right if operator == "+" else left * right
    if operator == "·" and ((left == 0) or (right == 0)):
        return 0
    if not left_infinite:
        return right
    if not right_infinite:
        return left
    return left if INFINITE_RANK[left] >= INFINITE_RANK[right] else right


def expression_result(operands, operator):
    result = operands[0]
    for operand in operands[1:]:
        result = combine_cardinals(result, operand, operator)
    return result


class CardinalArithmeticGenerator(ProblemGenerator):
    """Generate exact cardinal arithmetic with ℵ0 and c."""

    VARIANTS = ("add_multiply", "exponent", "set_cardinality")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _add_multiply(self):
        operator = random.choice(("+", "·"))
        count = random.randint(2, 4)
        operands = [random.randint(1, 1000) for _ in range(count)]
        infinite_indices = random.sample(range(count), random.randint(1, count - 1))
        for index in infinite_indices:
            operands[index] = random.choice(("ℵ0", "c"))
        expression = f" {operator} ".join(map(cardinal_text, operands))
        rule = ("For positive cardinals, if at least one operand is infinite, "
                "both addition and multiplication equal the larger infinite "
                "cardinal.")
        problem = (f"Evaluate cardinal expression: {expression}. {rule} "
                   f"{random.choice(QUERIES['add_multiply'])}")
        steps = [step("CARD_RULE", "infinite addition and multiplication",
                      "κ + λ = κ · λ = max(κ, λ)")]
        current = operands[0]
        prefix = cardinal_text(current)
        for operand in operands[1:]:
            result = combine_cardinals(current, operand, operator)
            if isinstance(current, int) and isinstance(operand, int):
                steps.append(step("A" if operator == "+" else "M",
                                  current, operand, result))
            else:
                steps.append(step("CARD_RULE", "maximum infinite cardinal",
                                  f"{cardinal_text(current)} {operator} "
                                  f"{cardinal_text(operand)} = "
                                  f"{cardinal_text(result)}"))
            prefix = f"{prefix} {operator} {cardinal_text(operand)}"
            steps.append(step("REWRITE", prefix, cardinal_text(result)))
            current = result
        answer = cardinal_text(current)
        steps.append(step("CHECK", expression, answer))
        return problem, steps, answer

    def _exponent(self):
        case = random.randrange(6)
        if case == 0:
            base, exponent, result = random.randint(2, 100000), "ℵ0", "c"
            rule = "n^ℵ0 = c for every finite integer n ≥ 2"
            label = "finite base"
        elif case == 1:
            base, exponent, result = "ℵ0", "ℵ0", "c"
            rule = "ℵ0^ℵ0 = c"
            label = "countable sequences"
        elif case == 2:
            base, exponent, result = "ℵ0", random.randint(1, 100000), "ℵ0"
            rule = "ℵ0^n = ℵ0 for every positive finite n"
            label = "finite exponent"
        elif case == 3:
            base, exponent, result = "c", "ℵ0", "c"
            rule = "c^ℵ0 = c"
            label = "continuum to countable power"
        elif case == 4:
            base, exponent, result = "c", "c", "2^c"
            rule = "c^c = 2^c"
            label = "continuum self-power"
        else:
            base, exponent, result = 2, "ℵ0", "c"
            rule = "2^ℵ0 = c"
            label = "continuum definition"
        power = f"{base}^{exponent}"
        adjustment = random.randint(1, 100000)
        outer_operator = random.choice(("+", "·"))
        expression = f"{adjustment} {outer_operator} ({power})"
        problem = (f"Evaluate cardinal exponentiation inside expression: "
                   f"{expression}. "
                   f"Identity to use: {rule}. "
                   f"{random.choice(QUERIES['exponent'])}")
        steps = [step("CARD_RULE", label, rule),
                 step("REWRITE", power, result),
                 step("CARD_RULE", "positive finite with infinite",
                      f"{adjustment} {outer_operator} {result} = {result}"),
                 step("REWRITE", expression, result),
                 step("CHECK", expression, result)]
        answer = f"c ({expression})" if result == "c" else result
        return problem, steps, answer

    def _set_cardinality(self):
        case = random.randrange(7)
        parameter = random.randint(2, 100000)
        if case == 0:
            object_text = f"ℕ^{parameter}"
            result, rule = "ℵ0", "a positive finite power of ℵ0 is ℵ0"
            answer = f"card({object_text}) = ℵ0"
        elif case == 1:
            object_text = f"ℤ^{parameter}"
            result, rule = "ℵ0", "a finite product of countable sets is countable"
            answer = f"card({object_text}) = ℵ0"
        elif case == 2:
            object_text = f"ℚ^{parameter}"
            result, rule = "ℵ0", "a finite product of countable sets is countable"
            answer = f"card({object_text}) = ℵ0"
        elif case == 3:
            object_text = f"(ℝ − ℚ)^{parameter}"
            result = "c"
            rule = ("removing a countable subset from ℝ leaves cardinal c, "
                    "and a positive finite power of c is c")
            answer = f"card({object_text}) = c"
        elif case == 4:
            object_text = f"P(ℕ × F_{parameter}), where card(F_{parameter}) = {parameter}"
            result = "c"
            rule = "ℕ times a nonempty finite set has size ℵ0, and 2^ℵ0 = c"
            answer = f"card(P(ℕ × F_{parameter})) = c (2^ℵ0)"
        elif case == 5:
            object_text = f"finite sequences over ℕ of length at most {parameter}"
            result, rule = "ℵ0", "a finite union of finite powers of ℵ0 is ℵ0"
            answer = f"card({object_text}) = ℵ0"
        else:
            object_text = (f"functions ℕ → D_{parameter}, where "
                           f"card(D_{parameter}) = {parameter}")
            result = "c"
            rule = "m^ℵ0 = c for every finite m ≥ 2"
            answer = f"card(functions ℕ → D_{parameter}) = c (2^ℵ0)"
        problem = (f"Set description: {object_text}. Cardinality rule: {rule}. "
                   f"{random.choice(QUERIES['set_cardinality'])}")
        steps = [step("CARD_RULE", "set construction", rule),
                 step("REWRITE", f"card({object_text})", result),
                 step("CHECK", answer)]
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "add_multiply":
            problem, steps, answer = self._add_multiply()
        elif variant == "exponent":
            problem, steps, answer = self._exponent()
        else:
            problem, steps, answer = self._set_cardinality()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"cardinal_arithmetic_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

import math
import random
import string

from base_generator import ProblemGenerator
from helpers import step, jid


PLACES = [
    "combinatorics class", "math club", "technical college", "study hall",
    "training center", "university seminar", "problem-solving workshop",
    "computer lab", "science classroom", "learning center", "tutoring center",
    "research group", "exam review", "lecture room", "statistics class",
    "engineering classroom", "algebra workshop", "design studio",
    "research station", "graduate seminar",
]

CONTEXTS = [
    "A worksheet from the {place} gives the following counting problem.",
    "During a session at the {place}, this arrangement is analyzed.",
    "An exercise used by the {place} asks for this count.",
    "The {place} is checking the following combinatorial model.",
    "A review prepared at the {place} includes this problem.",
    "In a lesson at the {place}, the following count is studied.",
]


def context_text():
    return random.choice(CONTEXTS).format(place=random.choice(PLACES))


def product_steps(factors):
    if not factors:
        return [], 1
    run = factors[0]
    steps = []
    for factor in factors[1:]:
        steps.append(step("M", run, factor, run * factor))
        run *= factor
    return steps, run


def combination_steps(n, r):
    numer_factors = list(range(n, n - r, -1))
    denom_factors = list(range(1, r + 1))
    steps = [
        step("COMB_SETUP", f"C({n}, {r})", "n!/(r!(n-r)!)"),
        step("REWRITE", "numerator", " * ".join(str(v) for v in numer_factors)),
    ]
    numer_steps, numer = product_steps(numer_factors)
    steps += numer_steps
    steps.append(step("REWRITE", "denominator",
                      " * ".join(str(v) for v in denom_factors)))
    denom_steps, denom = product_steps(denom_factors)
    steps += denom_steps
    value = numer // denom
    steps.append(step("D", numer, denom, value))
    return steps, value


def factorial_value(n):
    return math.factorial(n)


def item_text(count, letter):
    return f"{count} {letter}" if count == 1 else f"{count} {letter}'s"


class StarsAndBarsGenerator(ProblemGenerator):
    """
    Stars and bars counts and multinomial coefficients.

    Variants:
    - nonnegative: x1+...+xk=n with xi >= 0
    - positive: x1+...+xk=n with xi >= 1
    - multinomial: n!/(a!b!c!...)

    Op-codes used:
    - SB_SETUP / SB_FORMULA: stars-and-bars setup and formula
    - SHIFT: positive-variable substitution
    - MULTI_SETUP / MULTI_FORMULA: multinomial setup and formula
    - FACT_VALUE: factorial values used in the denominator
    - A / S / M / D (established): arithmetic
    - Z: exact count
    """

    VARIANTS = ["nonnegative", "positive", "multinomial"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "nonnegative":
            n = random.randint(4, 50)
            k = random.randint(2, 10)
            n_plus_k = n + k
            top = n_plus_k - 1
            bottom = k - 1
            steps = [
                step("SB_SETUP", f"x1+...+x{k} = {n}", "xi >= 0"),
                step("SB_FORMULA", "C(n+k-1, k-1)"),
                step("A", n, k, n_plus_k),
                step("S", n_plus_k, 1, top),
                step("S", k, 1, bottom),
            ]
            combo_steps, value = combination_steps(top, bottom)
            steps += combo_steps
            problem = (
                f"How many nonnegative integer solutions are there to "
                f"x1 + ... + x{k} = {n}?"
            )
            answer = f"solutions = {value}"
        elif variant == "positive":
            k = random.randint(2, 10)
            n = random.randint(k + 2, k + 50)
            remaining = n - k
            top = n - 1
            bottom = k - 1
            steps = [
                step("SB_SETUP", f"x1+...+x{k} = {n}", "xi >= 1"),
                step("SHIFT", "yi = xi - 1", f"y1+...+y{k} = {remaining}"),
                step("SB_FORMULA", "C(n-1, k-1)"),
                step("S", n, k, remaining),
                step("S", n, 1, top),
                step("S", k, 1, bottom),
            ]
            combo_steps, value = combination_steps(top, bottom)
            steps += combo_steps
            problem = (
                f"How many positive integer solutions are there to "
                f"x1 + ... + x{k} = {n}?"
            )
            answer = f"solutions = {value}"
        else:
            count_len = random.choice([3, 4])
            letters = random.sample(string.ascii_uppercase, count_len)
            counts = [random.randint(1, 5) for _ in range(count_len)]
            total = sum(counts)
            denom_facts = [factorial_value(count) for count in counts]
            denom_steps, denom = product_steps(denom_facts)
            numer = factorial_value(total)
            value = numer // denom
            count_text = ", ".join(item_text(counts[i], letters[i])
                                   for i in range(count_len))
            steps = [
                step("MULTI_SETUP", count_text, f"total {total}"),
                step("MULTI_FORMULA", "n!/(a!b!c!...)", f"{total}! / repeats"),
                step("FACT_VALUE", f"{total}!", numer),
            ]
            for count, fact in zip(counts, denom_facts):
                steps.append(step("FACT_VALUE", f"{count}!", fact))
            steps += denom_steps
            steps.append(step("D", numer, denom, value))
            problem = (
                f"How many distinct strings can be made from {count_text}?"
            )
            answer = f"multinomial = {value}"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"stars_and_bars_{variant}",
            problem=f"{context_text()} {problem}",
            steps=steps,
            final_answer=answer,
        )

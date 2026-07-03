import random
from base_generator import ProblemGenerator
from helpers import step, jid


def ordinal(n):
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }"


class ArithmeticSequenceGenerator(ProblemGenerator):
    """
    Arithmetic sequences from four shown terms: the nth term, which term
    equals a given value, and the partial sum.

    The common difference is computed from the first pair and verified
    against a second pair (A1) before any formula is used.

    Op-codes used:
    - SEQ_SETUP: the shown terms and the goal (terms, goal)
    - COMMON_DIFF: difference of consecutive terms (work, value)
    - CHECK: verify d on another consecutive pair (established)
    - SEQ_FORMULA: state the formula (established *_FORMULA shape)
    - SEQ_APPLY: the formula with values substituted (instantiation)
    - S / M / A / D: the arithmetic (established meanings)
    - Z: final answer
    """

    VARIANTS = ["nth_term", "which_term", "partial_sum"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a1 = random.randint(-9, 9)
        d = random.choice([v for v in range(-9, 10) if v != 0])
        n = random.randint(10, 30)
        terms = [a1 + i * d for i in range(4)]
        shown = ", ".join(str(t) for t in terms)

        steps = []
        an = a1 + (n - 1) * d

        def wrap(v):
            return f"({v})" if v < 0 else str(v)

        def diff_steps(goal):
            steps.append(step("SEQ_SETUP", f"{shown}, ...", goal))
            steps.append(step("COMMON_DIFF",
                              f"{terms[1]} - {wrap(terms[0])}", d))
            steps.append(step("CHECK", "difference",
                              f"{terms[2]} - {wrap(terms[1])} = {d}", d))

        def nth_chain():
            steps.append(step("SEQ_FORMULA", "a_n = a_1 + (n - 1)d"))
            steps.append(step("SEQ_APPLY",
                              f"a_{n} = {a1} + ({n} - 1)·{d}"))
            steps.append(step("S", n, 1, n - 1))
            steps.append(step("M", n - 1, d, (n - 1) * d))
            steps.append(step("A", a1, (n - 1) * d, an))

        if variant == "nth_term":
            diff_steps(f"{ordinal(n)} term")
            nth_chain()
            steps.append(step("Z", an))
            problem = (f"The arithmetic sequence {shown}, ... continues. "
                       f"Find the {ordinal(n)} term.")
            answer = str(an)
        elif variant == "which_term":
            diff_steps(f"which term equals {an}")
            steps.append(step("SEQ_FORMULA", "a_n = a_1 + (n - 1)d"))
            steps.append(step("SEQ_APPLY",
                              f"{an} = {a1} + (n - 1)·{d}"))
            steps.append(step("S", an, a1, an - a1))
            steps.append(step("D", an - a1, d, n - 1))
            steps.append(step("A", n - 1, 1, n))
            steps.append(step("Z", n))
            problem = (f"The arithmetic sequence {shown}, ... continues. "
                       f"Which term of the sequence equals {an}?")
            answer = str(n)
        else:
            total = n * (a1 + an) // 2
            diff_steps(f"sum of first {n} terms")
            nth_chain()
            steps.append(step("SEQ_FORMULA", "S_n = n(a_1 + a_n)/2"))
            steps.append(step("SEQ_APPLY",
                              f"S_{n} = {n}·({a1} + {an})/2"))
            steps.append(step("A", a1, an, a1 + an))
            steps.append(step("M", n, a1 + an, n * (a1 + an)))
            steps.append(step("D", n * (a1 + an), 2, total))
            steps.append(step("Z", total))
            problem = (f"The arithmetic sequence {shown}, ... continues. "
                       f"Find the sum of the first {n} terms.")
            answer = str(total)

        return dict(
            problem_id=jid(),
            operation=f"arithmetic_sequence_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

"""Check exact one-step martingale identities and optional stopping.

Variants: ``drift_corrected``, ``quadratic``, ``exponential``,
``not_martingale``, ``optional_stopping_ruin``, and ``doob_product``.
Op-codes: ``MARTINGALE_SETUP``, ``MARTINGALE_STEP``, ``OST_EQUATION``,
``POW``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``. Every
conditional expectation is evaluated by enumerating a two-point next step;
the optional-stopping variant uses bounded gambler's-ruin stopping times.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
P_BANK = (Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2),
          Fraction(3, 5), Fraction(2, 3), Fraction(3, 4))
BIASED_P_BANK = tuple(p for p in P_BANK if p != Fraction(1, 2))
BASE_BANK = (Fraction(2), Fraction(3), Fraction(1, 2), Fraction(1, 3))
PRODUCT_BANK = (
    (Fraction(1, 2), Fraction(1, 2), Fraction(3, 2)),
    (Fraction(1, 3), Fraction(2), Fraction(1, 2)),
    (Fraction(2, 3), Fraction(1, 2), Fraction(2)),
    (Fraction(1, 4), Fraction(2), Fraction(2, 3)),
    (Fraction(3, 4), Fraction(2, 3), Fraction(2)),
)
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
QUERIES = {
    "drift_corrected": (
        "Check the one-step martingale identity exactly.",
        "Evaluate the conditional mean and compare it with the current value.",
        "Verify whether subtracting the drift produces a martingale.",
        "Enumerate the next increment to test the martingale property.",
        "Decide the martingale question by direct conditioning.",
    ),
    "quadratic": (
        "Check the quadratic martingale identity in one step.",
        "Condition on the current position and compare the two values.",
        "Verify the compensation of the squared walk exactly.",
        "Enumerate both next positions to test this martingale.",
        "Evaluate the conditional mean of the quadratic process.",
    ),
    "exponential": (
        "Check the normalized exponential martingale exactly.",
        "Enumerate the next step and verify the exponential identity.",
        "Compare the next conditional mean with the current process value.",
        "Test whether the stated normalization removes the drift.",
        "Verify this multiplicative one-step martingale equation.",
    ),
    "not_martingale": (
        "Classify the uncorrected walk as a submartingale or supermartingale.",
        "Compare its next conditional mean with its current value.",
        "Show exactly why the biased walk is not a martingale.",
        "Use one-step conditioning to classify this process.",
        "Determine the direction of the walk's conditional drift.",
    ),
    "optional_stopping_ruin": (
        "Use optional stopping to find the upper-boundary hitting probability.",
        "Apply the exponential martingale at the absorption time.",
        "Derive the exact gambler's-ruin probability from the stopped process.",
        "Solve the bounded stopping equation for the chance of reaching N.",
        "Use the stopped martingale rather than a memorized ruin formula.",
    ),
    "doob_product": (
        "Check the mean-one product martingale exactly.",
        "Condition on the current product and enumerate the next factor.",
        "Verify that multiplying by the next independent factor preserves mean.",
        "Evaluate the product process's one-step conditional expectation.",
        "Test the multiplicative martingale identity from the factor law.",
    ),
}


def _context(subject):
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} studies {subject}.")


def _reachable_state(n):
    up = random.randint(0, n)
    return 2 * up - n


def _walk_problem(n, state, p, process):
    q = 1 - p
    return (f"{_context('a nearest-neighbor random walk')} The walk starts at "
            f"S_0=0 and has independent increments +1 with probability "
            f"p={prob_txt(p)} and -1 with probability q={prob_txt(q)}. "
            f"At time n={n}, condition on S_{n}={state}. The process is "
            f"{process}.")


def _pow(base, exponent):
    value = base ** exponent
    return step("POW", f"base {prob_txt(base)}, exponent {exponent}",
                prob_txt(value)), value


class MartingaleCheckGenerator(ProblemGenerator):
    """Generate exact finite-state martingale checks and stopped-walk tasks."""

    VARIANTS = ("drift_corrected", "quadratic", "exponential",
                "not_martingale", "optional_stopping_ruin", "doob_product")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _drift_corrected():
        n = random.randint(1, 12)
        state = _reachable_state(n)
        p = random.choice(P_BANK)
        q = 1 - p
        drift = p - q
        expected_position = state + drift
        compensation_next = (n + 1) * drift
        conditional = expected_position - compensation_next
        current = state - n * drift
        process = f"M_k=S_k-k({prob_txt(drift)})"
        problem = _walk_problem(n, state, p, process)
        steps = [
            step("MARTINGALE_SETUP", process, f"condition S_{n}={state}"),
            step("MARTINGALE_STEP", f"E[S_{n + 1} given S_{n}={state}]",
                 f"{state} + ({prob_txt(p)})(1) + ({prob_txt(q)})(−1)",
                 prob_txt(expected_position)),
            step("S", prob_txt(expected_position), prob_txt(compensation_next),
                 prob_txt(conditional)),
            step("CHECK", f"M_{n}", f"{state} − {n}({prob_txt(drift)})",
                 prob_txt(current)),
        ]
        answer = (f"martingale; E[M_{n + 1} given S_{n} = {state}] = "
                  f"{prob_txt(conditional)} = M_{n}")
        return problem, steps, answer

    @staticmethod
    def _quadratic():
        n = random.randint(1, 12)
        state = _reachable_state(n)
        p = Fraction(1, 2)
        plus_square = (state + 1) ** 2
        minus_square = (state - 1) ** 2
        weighted_plus = p * plus_square
        weighted_minus = p * minus_square
        expected_square = weighted_plus + weighted_minus
        conditional = expected_square - (n + 1)
        current = state ** 2 - n
        process = "M_k=S_k^2-k"
        problem = _walk_problem(n, state, p, process)
        steps = [
            step("MARTINGALE_SETUP", process, f"condition S_{n}={state}"),
            step("POW", f"base {state + 1}, exponent 2", plus_square),
            step("POW", f"base {state - 1}, exponent 2", minus_square),
            step("M", prob_txt(p), plus_square, prob_txt(weighted_plus)),
            step("M", prob_txt(p), minus_square, prob_txt(weighted_minus)),
            step("A", prob_txt(weighted_plus), prob_txt(weighted_minus),
                 prob_txt(expected_square)),
            step("MARTINGALE_STEP", f"E[S_{n + 1}^2 given S_{n}={state}]",
                 f"(1/2)({plus_square}) + (1/2)({minus_square})",
                 prob_txt(expected_square)),
            step("S", prob_txt(expected_square), n + 1, prob_txt(conditional)),
            step("CHECK", f"M_{n}", f"{state}^2 − {n}", prob_txt(current)),
        ]
        answer = (f"martingale; E[M_{n + 1} given S_{n} = {state}] = "
                  f"{prob_txt(conditional)} = M_{n}")
        return problem, steps, answer

    @staticmethod
    def _exponential():
        n = random.randint(1, 8)
        state = _reachable_state(n)
        p = random.choice(P_BANK)
        q = 1 - p
        base = random.choice(BASE_BANK)
        normalizer = p * base + q / base
        process = (f"M_k=({prob_txt(base)})^S_k/({prob_txt(normalizer)})^k")
        problem = _walk_problem(n, state, p, process)
        plus_step, plus_power = _pow(base, state + 1)
        minus_step, minus_power = _pow(base, state - 1)
        next_den_step, next_denominator = _pow(normalizer, n + 1)
        first_weight = p * plus_power
        second_weight = q * minus_power
        numerator = first_weight + second_weight
        conditional = numerator / next_denominator
        current_num_step, current_numerator = _pow(base, state)
        current_den_step, current_denominator = _pow(normalizer, n)
        current = current_numerator / current_denominator
        steps = [
            step("MARTINGALE_SETUP", process,
                 f"c=p·a+q/a={prob_txt(normalizer)}"),
            plus_step, minus_step,
            step("M", prob_txt(p), prob_txt(plus_power), prob_txt(first_weight)),
            step("M", prob_txt(q), prob_txt(minus_power), prob_txt(second_weight)),
            step("A", prob_txt(first_weight), prob_txt(second_weight),
                 prob_txt(numerator)),
            next_den_step,
            step("D", prob_txt(numerator), prob_txt(next_denominator),
                 prob_txt(conditional)),
            step("MARTINGALE_STEP", f"E[M_{n + 1} given S_{n}={state}]",
                 "weighted two-point next value", prob_txt(conditional)),
            current_num_step, current_den_step,
            step("D", prob_txt(current_numerator), prob_txt(current_denominator),
                 prob_txt(current)),
            step("CHECK", f"M_{n}", prob_txt(current)),
        ]
        answer = (f"martingale; E[M_{n + 1} given S_{n} = {state}] = "
                  f"{prob_txt(conditional)} = M_{n}")
        return problem, steps, answer

    @staticmethod
    def _not_martingale():
        n = random.randint(1, 12)
        state = _reachable_state(n)
        p = random.choice(BIASED_P_BANK)
        q = 1 - p
        expected = state + p - q
        kind = "submartingale" if p > q else "supermartingale"
        relation = ">" if p > q else "<"
        problem = _walk_problem(n, state, p, "X_k=S_k")
        steps = [
            step("MARTINGALE_SETUP", "X_k=S_k", f"condition S_{n}={state}"),
            step("MARTINGALE_STEP", f"E[S_{n + 1} given S_{n}={state}]",
                 f"{state} + ({prob_txt(p)})(1) + ({prob_txt(q)})(−1)",
                 prob_txt(expected)),
            step("CHECK", prob_txt(expected), relation, state),
        ]
        answer = f"{kind}; {prob_txt(expected)} {relation} {state}"
        return problem, steps, answer

    @staticmethod
    def _optional_stopping():
        boundary = random.randint(3, 9)
        initial = random.randint(1, boundary - 1)
        p = random.choice(BIASED_P_BANK)
        q = 1 - p
        ratio = q / p
        initial_step, initial_power = _pow(ratio, initial)
        boundary_step, boundary_power = _pow(ratio, boundary)
        numerator = 1 - initial_power
        denominator = 1 - boundary_power
        probability = numerator / denominator
        problem = (f"{_context('a stopped random walk')} A gambler starts at "
                   f"S_0=i={initial} and stops at tau upon reaching 0 or N="
                   f"{boundary}. Each round adds 1 with probability p="
                   f"{prob_txt(p)} and subtracts 1 with probability q="
                   f"{prob_txt(q)}. Use the bounded stopped martingale "
                   f"M_k=({prob_txt(ratio)})^S_k. Target: P(S_tau=N).")
        steps = [
            step("MARTINGALE_SETUP", f"M_k=({prob_txt(ratio)})^S_k",
                 f"p·r+q/r={prob_txt(p * ratio + q / ratio)}"),
            initial_step, boundary_step,
            step("OST_EQUATION", "E[M_tau]=M_0",
                 f"x({prob_txt(boundary_power)})+(1−x)={prob_txt(initial_power)}"),
            step("S", 1, prob_txt(initial_power), prob_txt(numerator)),
            step("S", 1, prob_txt(boundary_power), prob_txt(denominator)),
            step("D", prob_txt(numerator), prob_txt(denominator),
                 prob_txt(probability)),
            step("CHECK", "bounded absorption", "optional stopping applies"),
        ]
        answer = (f"P(S_tau=N) = {prob_txt(probability)}; exponential "
                  f"martingale M_k=({prob_txt(ratio)})^S_k")
        return problem, steps, answer

    @staticmethod
    def _doob_product():
        n = random.randint(1, 10)
        p, first, second = random.choice(PRODUCT_BANK)
        q = 1 - p
        first_count = random.randint(0, n)
        current = first ** first_count * second ** (n - first_count)
        next_first = current * first
        next_second = current * second
        first_weight = p * next_first
        second_weight = q * next_second
        conditional = first_weight + second_weight
        problem = (f"{_context('a product process')} Independent factors Y_j "
                   f"equal a={prob_txt(first)} with probability p={prob_txt(p)} "
                   f"and b={prob_txt(second)} with probability q={prob_txt(q)}. "
                   f"Let M_k=Y_1Y_2...Y_k. At time n={n}, condition on "
                   f"M_{n}={prob_txt(current)}.")
        steps = [
            step("MARTINGALE_SETUP", "M_k=Y_1Y_2...Y_k",
                 f"E[Y]={prob_txt(p)}({prob_txt(first)})+"
                 f"{prob_txt(q)}({prob_txt(second)})=1"),
            step("M", prob_txt(current), prob_txt(first), prob_txt(next_first)),
            step("M", prob_txt(current), prob_txt(second), prob_txt(next_second)),
            step("M", prob_txt(p), prob_txt(next_first), prob_txt(first_weight)),
            step("M", prob_txt(q), prob_txt(next_second), prob_txt(second_weight)),
            step("A", prob_txt(first_weight), prob_txt(second_weight),
                 prob_txt(conditional)),
            step("MARTINGALE_STEP", f"E[M_{n + 1} given M_{n}={prob_txt(current)}]",
                 "weighted two-point next product", prob_txt(conditional)),
            step("CHECK", f"M_{n}", prob_txt(current)),
        ]
        answer = (f"martingale; E[M_{n + 1} given M_{n} = {prob_txt(current)}] "
                  f"= {prob_txt(conditional)} = M_{n}")
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "drift_corrected":
            problem, steps, answer = self._drift_corrected()
        elif variant == "quadratic":
            problem, steps, answer = self._quadratic()
        elif variant == "exponential":
            problem, steps, answer = self._exponential()
        elif variant == "not_martingale":
            problem, steps, answer = self._not_martingale()
        elif variant == "optional_stopping_ruin":
            problem, steps, answer = self._optional_stopping()
        else:
            problem, steps, answer = self._doob_product()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_martingale_check_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

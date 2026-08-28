"""Compute finite random-walk positions, moments, and ruin quantities.

Variants: ``position_prob``, ``biased_position``, ``return_to_origin``,
``mean_var``, ``ruin_fair``, ``ruin_biased``, and ``duration_fair``.
Op-codes: ``RW_SETUP``, ``RW_PATHS``, ``RW_MOMENTS``, ``RUIN_SETUP``,
``RUIN_FORMULA``, ``NCR``, ``POW``, ``A``, ``S``, ``M``, ``D``, ``CHECK``,
and ``Z``. Position problems use at most 12 steps, allowing the tests to
enumerate every path; ruin tests solve the first-step system independently.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
P_BANK = (Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2),
          Fraction(3, 5), Fraction(2, 3), Fraction(3, 4))
BIASED_P_BANK = tuple(p for p in P_BANK if p != Fraction(1, 2))
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
    "position_prob": (
        "Find this exact position probability.",
        "Count the up-step paths that end at the target.",
        "Compute P(S_n=k) for this symmetric walk.",
        "Solve for the required up and down counts, then evaluate the probability.",
        "Find the exact mass at the stated position.",
    ),
    "biased_position": (
        "Find this exact biased-walk position probability.",
        "Weight every path ending at the target position.",
        "Compute P(S_n=k) for the stated up-step probability.",
        "Count the matching paths and multiply by their common weight.",
        "Evaluate the exact mass at the target position.",
    ),
    "return_to_origin": (
        "Find the exact probability of returning to the origin at that time.",
        "Count paths with equal numbers of up and down steps.",
        "Compute P(S_n=0) for this symmetric walk.",
        "Evaluate the central-binomial return probability.",
        "Find the exact mass back at the starting point.",
    ),
    "mean_var": (
        "Find E[S_n] and Var(S_n) exactly.",
        "Use independent increment moments for the walk.",
        "Compute the position mean and variance after n steps.",
        "Report the exact center and spread of S_n.",
        "Add the means and variances of the increments.",
    ),
    "ruin_fair": (
        "Find the fair-walk probability of reaching N before ruin.",
        "Use the fair gambler's-ruin formula.",
        "Compute the exact fair upper-boundary hitting probability.",
        "What is the fair-game chance of winning before reaching zero?",
        "Evaluate the fair first-step boundary problem.",
    ),
    "ruin_biased": (
        "Find the biased-walk probability of reaching N before ruin.",
        "Use the biased gambler's-ruin formula.",
        "Compute the exact biased upper-boundary hitting probability.",
        "What is the biased-game chance of winning before reaching zero?",
        "Evaluate the biased first-step boundary problem.",
    ),
    "duration_fair": (
        "Find the expected number of rounds until absorption.",
        "Use the fair gambler's-ruin duration formula.",
        "Compute the exact expected stopping time.",
        "How many rounds are expected before reaching 0 or N?",
        "Evaluate the fair first-step duration problem.",
    ),
}


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} studies a random walk.")


def _power(base, exponent):
    value = base ** exponent
    return step("POW", f"base {prob_txt(base)}, exponent {exponent}",
                prob_txt(value)), value


def _walk_problem(n, p, target):
    q = 1 - p
    return (f"{_context()} A nearest-neighbor walk starts at S_0=0 and takes "
            f"n={n} independent steps. Each step is +1 with probability "
            f"p={prob_txt(p)} and -1 with probability q={prob_txt(q)}. "
            f"Target: {target}.")


def _position_steps(n, position, p, symmetric_shortcut=False):
    up = (n + position) // 2
    down = n - up
    coefficient = math.comb(n, up)
    steps = [
        step("RW_SETUP", f"p={prob_txt(p)}, n={n}", f"P(S_{n}={position})"),
        step("RW_PATHS", f"u-d={position}, u+d={n}", "solve",
             f"u={up}, d={down}"),
        step("NCR", f"C({n}, {up})", coefficient),
    ]
    if symmetric_shortcut:
        power_step, path_weight = _power(Fraction(1, 2), n)
        steps.append(power_step)
    else:
        p_step, p_power = _power(p, up)
        q_step, q_power = _power(1 - p, down)
        path_weight = p_power * q_power
        steps.extend([
            p_step, q_step,
            step("M", prob_txt(p_power), prob_txt(q_power),
                 prob_txt(path_weight)),
        ])
    probability = coefficient * path_weight
    steps.extend([
        step("M", coefficient, prob_txt(path_weight), prob_txt(probability)),
        step("CHECK", "u+d", f"{up}+{down}", n),
    ])
    return steps, probability


def _ruin_problem(initial, boundary, p, target):
    q = 1 - p
    return (f"{_context()} A gambler starts with i={initial} units and stops upon "
            f"reaching 0 or N={boundary}. Each round adds 1 unit with probability "
            f"p={prob_txt(p)} and subtracts 1 unit with probability q="
            f"{prob_txt(q)}. Target: {target}.")


class RandomWalkGenerator(ProblemGenerator):
    """Generate exact walk-position and gambler's-ruin exercises."""

    VARIANTS = ("position_prob", "biased_position", "return_to_origin",
                "mean_var", "ruin_fair", "ruin_biased", "duration_fair")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _position(biased):
        n = random.randint(2, 12 if not biased else 10)
        up = random.randint(0, n)
        position = 2 * up - n
        p = random.choice(BIASED_P_BANK) if biased else Fraction(1, 2)
        problem = _walk_problem(n, p, f"P(S_{n}={position})")
        steps, probability = _position_steps(n, position, p, not biased)
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _return():
        half_steps = random.randint(1, 6)
        n = 2 * half_steps
        p = Fraction(1, 2)
        problem = _walk_problem(n, p, f"P(S_{n}=0)")
        steps, probability = _position_steps(n, 0, p, True)
        steps.append(step("CHECK", "return requires equal up and down counts",
                          f"{half_steps} and {half_steps}"))
        return problem, steps, prob_txt(probability)

    @staticmethod
    def _moments():
        n = random.randint(2, 12)
        p = random.choice(P_BANK)
        q = 1 - p
        drift = p - q
        mean = n * drift
        pq = p * q
        four_n = 4 * n
        variance = four_n * pq
        problem = _walk_problem(n, p, f"E[S_{n}] and Var(S_{n})")
        steps = [
            step("RW_SETUP", f"p={prob_txt(p)}, q={prob_txt(q)}, n={n}",
                 "position moments"),
            step("RW_MOMENTS", "E[S_n]=n(p-q)", "Var(S_n)=4npq"),
            step("S", prob_txt(p), prob_txt(q), prob_txt(drift)),
            step("M", n, prob_txt(drift), prob_txt(mean)),
            step("M", prob_txt(p), prob_txt(q), prob_txt(pq)),
            step("M", 4, n, four_n),
            step("M", four_n, prob_txt(pq), prob_txt(variance)),
            step("CHECK", "independent increments", "means and variances add"),
        ]
        answer = f"E[S_{n}] = {prob_txt(mean)}; Var(S_{n}) = {prob_txt(variance)}"
        return problem, steps, answer

    @staticmethod
    def _fair_ruin(duration):
        boundary = random.randint(3, 10)
        initial = random.randint(1, boundary - 1)
        p = Fraction(1, 2)
        if duration:
            target = "the expected rounds until hitting 0 or N"
            distance = boundary - initial
            value = initial * distance
            steps = [
                step("RUIN_SETUP", f"fair, i={initial}, N={boundary}",
                     "expected duration"),
                step("RUIN_FORMULA", "E_i=i(N-i)"),
                step("S", boundary, initial, distance),
                step("M", initial, distance, value),
                step("CHECK", "duration is zero at boundaries", "E_0=E_N=0"),
            ]
        else:
            target = "P(reach N before 0)"
            value = Fraction(initial, boundary)
            steps = [
                step("RUIN_SETUP", f"fair, i={initial}, N={boundary}", target),
                step("RUIN_FORMULA", "fair", "P_i=i/N"),
                step("D", initial, boundary, prob_txt(value)),
                step("CHECK", "boundary values", "P_0=0, P_N=1"),
            ]
        return _ruin_problem(initial, boundary, p, target), steps, prob_txt(value)

    @staticmethod
    def _biased_ruin():
        boundary = random.randint(3, 9)
        initial = random.randint(1, boundary - 1)
        p = random.choice(BIASED_P_BANK)
        q = 1 - p
        ratio = q / p
        i_step, i_power = _power(ratio, initial)
        n_step, n_power = _power(ratio, boundary)
        numerator = 1 - i_power
        denominator = 1 - n_power
        value = numerator / denominator
        target = "P(reach N before 0)"
        problem = _ruin_problem(initial, boundary, p, target)
        steps = [
            step("RUIN_SETUP", f"biased, i={initial}, N={boundary}",
                 f"p={prob_txt(p)}, q={prob_txt(q)}"),
            step("RUIN_FORMULA", "(1-r^i)/(1-r^N)", "r=q/p"),
            step("D", prob_txt(q), prob_txt(p), prob_txt(ratio)),
            i_step, n_step,
            step("S", 1, prob_txt(i_power), prob_txt(numerator)),
            step("S", 1, prob_txt(n_power), prob_txt(denominator)),
            step("D", prob_txt(numerator), prob_txt(denominator), prob_txt(value)),
            step("CHECK", "boundary values", "P_0=0, P_N=1"),
        ]
        return problem, steps, prob_txt(value)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "position_prob":
            problem, steps, answer = self._position(False)
        elif variant == "biased_position":
            problem, steps, answer = self._position(True)
        elif variant == "return_to_origin":
            problem, steps, answer = self._return()
        elif variant == "mean_var":
            problem, steps, answer = self._moments()
        elif variant == "ruin_fair":
            problem, steps, answer = self._fair_ruin(False)
        elif variant == "ruin_biased":
            problem, steps, answer = self._biased_ruin()
        else:
            problem, steps, answer = self._fair_ruin(True)
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_random_walk_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

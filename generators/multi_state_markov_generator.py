"""Compute exact three-state Markov-chain probabilities and summaries.

Variants: ``two_step``, ``path_probability``, ``hitting_prob_3state``,
``expected_hitting_time``, ``stationary_3state``, and
``distribution_after_one_step``. Op-codes: ``MARKOV_SETUP``, ``WALK_GOAL``,
``WALK_TERM``, ``PATH_EDGE``, ``FIRST_STEP``, ``LINEAR_SYSTEM``,
``STEADY_EQUATION``, ``DIST_ENTRY``, ``A``, ``S``, ``M``, ``D``, ``CHECK``,
and ``Z``. All transition arithmetic uses ``Fraction`` values.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
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
    "two_step": (
        "Find this exact two-step transition probability.",
        "Sum the three intermediate-state path weights.",
        "Compute the requested entry of P squared.",
        "Evaluate the two-step state-to-state probability.",
        "Condition on the state after the first transition.",
    ),
    "path_probability": (
        "Find the exact probability of the specified state path.",
        "Multiply the transition probabilities along this path.",
        "Compute the likelihood of the stated trajectory.",
        "Evaluate this ordered Markov path probability.",
        "Use the Markov property at each path edge.",
    ),
    "hitting_prob_3state": (
        "Find the probability of hitting state 3 before state 1.",
        "Solve the exact first-step boundary equation.",
        "Compute the upper-state hitting probability from state 2.",
        "Evaluate this three-state boundary-hitting chance.",
        "Use h_1=0 and h_3=1 in the first-step recursion.",
    ),
    "expected_hitting_time": (
        "Find the expected time to hit state 3 from states 1 and 2.",
        "Solve the two first-step equations for the hitting times.",
        "Compute both exact expected absorption times.",
        "Evaluate E_1[T_3] and E_2[T_3].",
        "Use the transient-state linear system for the target-state wait.",
    ),
    "stationary_3state": (
        "Find the exact stationary distribution.",
        "Solve pi P=pi with components summing to one.",
        "Use detailed balance to identify the invariant probabilities.",
        "Compute the three-state steady-state vector.",
        "Find and verify the invariant distribution.",
    ),
    "distribution_after_one_step": (
        "Find the state distribution after one transition.",
        "Multiply the initial row distribution by P.",
        "Compute all three next-state probabilities.",
        "Evaluate the one-step distribution vector exactly.",
        "Sum incoming probability flow into each state.",
    ),
}


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} studies a Markov chain.")


def _positive_row():
    denominator = random.randint(3, 9)
    first, second = sorted(random.sample(range(1, denominator), 2))
    counts = (first, second - first, denominator - second)
    return tuple(Fraction(value, denominator) for value in counts)


def _general_matrix():
    return tuple(_positive_row() for _ in range(3))


def _absorbing_matrix():
    return _positive_row(), _positive_row(), (Fraction(0), Fraction(0), Fraction(1))


def _row_text(row):
    return "(" + ", ".join(prob_txt(value) for value in row) + ")"


def _matrix_text(matrix):
    return "; ".join(f"P{index + 1}={_row_text(row)}"
                     for index, row in enumerate(matrix))


def _problem(matrix, target, initial=None):
    extra = "" if initial is None else f" Initial distribution v={_row_text(initial)}."
    return (f"{_context()} The states are {{1, 2, 3}}. Transition rows, with "
            f"columns in state order 1, 2, 3, are {_matrix_text(matrix)}.{extra} "
            f"Target: {target}.")


def _setup(matrix, target):
    return step("MARKOV_SETUP", "three_state", _matrix_text(matrix), target)


def _sum_three(steps, values):
    first = values[0] + values[1]
    total = first + values[2]
    steps.extend([
        step("A", prob_txt(values[0]), prob_txt(values[1]), prob_txt(first)),
        step("A", prob_txt(first), prob_txt(values[2]), prob_txt(total)),
    ])
    return total


def _solve_two(a, b, c, d, first_rhs=Fraction(1), second_rhs=Fraction(1)):
    determinant = a * d - b * c
    first_numerator = first_rhs * d - b * second_rhs
    second_numerator = a * second_rhs - first_rhs * c
    return (determinant, first_numerator, second_numerator,
            first_numerator / determinant, second_numerator / determinant)


class MultiStateMarkovGenerator(ProblemGenerator):
    """Generate exact three-state transition and hitting-time exercises."""

    VARIANTS = ("two_step", "path_probability", "hitting_prob_3state",
                "expected_hitting_time", "stationary_3state",
                "distribution_after_one_step")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _two_step():
        matrix = _general_matrix()
        start = random.randrange(3)
        end = random.randrange(3)
        terms = [matrix[start][middle] * matrix[middle][end]
                 for middle in range(3)]
        target = f"P(X_2={end + 1} given X_0={start + 1})"
        steps = [_setup(matrix, target),
                 step("WALK_GOAL", "2 steps", f"{start + 1} to {end + 1}")]
        for middle, value in enumerate(terms):
            steps.append(step("WALK_TERM", f"via {middle + 1}",
                              (f"{prob_txt(matrix[start][middle])} times "
                               f"{prob_txt(matrix[middle][end])}"),
                              prob_txt(value)))
        total = _sum_three(steps, terms)
        steps.append(step("CHECK", "sum over every intermediate state",
                          prob_txt(total)))
        return _problem(matrix, target), steps, prob_txt(total)

    @staticmethod
    def _path_probability():
        matrix = _general_matrix()
        transitions = random.randint(2, 4)
        path = [random.randrange(3) for _ in range(transitions + 1)]
        factors = [matrix[left][right] for left, right in zip(path, path[1:])]
        path_text = "→".join(str(state + 1) for state in path)
        target = f"P(path {path_text})"
        steps = [_setup(matrix, target)]
        for left, right, value in zip(path, path[1:], factors):
            steps.append(step("PATH_EDGE", f"{left + 1}→{right + 1}",
                              prob_txt(value)))
        running = factors[0]
        for value in factors[1:]:
            steps.append(step("M", prob_txt(running), prob_txt(value),
                              prob_txt(running * value)))
            running *= value
        steps.append(step("CHECK", "ordered path uses one factor per edge",
                          len(factors)))
        return _problem(matrix, target), steps, prob_txt(running)

    @staticmethod
    def _hitting_probability():
        matrix = _general_matrix()
        p21, p22, p23 = matrix[1]
        denominator = 1 - p22
        probability = p23 / denominator
        target = "P_2(hit state 3 before state 1)"
        self_term = p22 * probability
        reconstructed = self_term + p23
        steps = [
            _setup(matrix, target),
            step("FIRST_STEP", "h_1=0, h_3=1",
                 "h_2=P21*h_1+P22*h_2+P23*h_3"),
            step("S", 1, prob_txt(p22), prob_txt(denominator)),
            step("D", prob_txt(p23), prob_txt(denominator),
                 prob_txt(probability)),
            step("M", prob_txt(p22), prob_txt(probability),
                 prob_txt(self_term)),
            step("A", prob_txt(self_term), prob_txt(p23),
                 prob_txt(reconstructed)),
            step("CHECK", "first-step equation reconstructs h_2",
                 prob_txt(reconstructed)),
        ]
        return _problem(matrix, target), steps, prob_txt(probability)

    @staticmethod
    def _hitting_time():
        matrix = _absorbing_matrix()
        p11, p12, _ = matrix[0]
        p21, p22, _ = matrix[1]
        a, b = 1 - p11, -p12
        c, d = -p21, 1 - p22
        determinant, num1, num2, time1, time2 = _solve_two(a, b, c, d)
        target = "E_1[T_3] and E_2[T_3]"
        ad, bc = a * d, b * c
        steps = [
            _setup(matrix, target),
            step("FIRST_STEP", "t_1=1+P11*t_1+P12*t_2",
                 "t_2=1+P21*t_1+P22*t_2"),
            step("S", 1, prob_txt(p11), prob_txt(a)),
            step("M", prob_txt(p12), -1, prob_txt(b)),
            step("M", prob_txt(p21), -1, prob_txt(c)),
            step("S", 1, prob_txt(p22), prob_txt(d)),
            step("LINEAR_SYSTEM",
                 f"({prob_txt(a)})t_1 - ({prob_txt(-b)})t_2 = 1",
                 f"-({prob_txt(-c)})t_1 + ({prob_txt(d)})t_2 = 1"),
            step("M", prob_txt(a), prob_txt(d), prob_txt(ad)),
            step("M", prob_txt(b), prob_txt(c), prob_txt(bc)),
            step("S", prob_txt(ad), prob_txt(bc), prob_txt(determinant)),
            step("S", prob_txt(d), prob_txt(b), prob_txt(num1)),
            step("D", prob_txt(num1), prob_txt(determinant), prob_txt(time1)),
            step("S", prob_txt(a), prob_txt(c), prob_txt(num2)),
            step("D", prob_txt(num2), prob_txt(determinant), prob_txt(time2)),
            step("CHECK", "target state", "E_3[T_3]=0"),
        ]
        answer = f"E_1[T_3] = {prob_txt(time1)}; E_2[T_3] = {prob_txt(time2)}"
        return _problem(matrix, target), steps, answer

    @staticmethod
    def _stationary():
        weights = tuple(random.randint(3, 9) for _ in range(3))
        matrix = tuple(
            tuple(Fraction(weights[row] - 2, weights[row]) if row == column
                  else Fraction(1, weights[row]) for column in range(3))
            for row in range(3)
        )
        total_weight = sum(weights)
        stationary = tuple(Fraction(value, total_weight) for value in weights)
        target = "stationary distribution pi"
        steps = [
            _setup(matrix, target),
            step("STEADY_EQUATION", "pi P=pi", "pi_1+pi_2+pi_3=1"),
            step("A", weights[0], weights[1], weights[0] + weights[1]),
            step("A", weights[0] + weights[1], weights[2], total_weight),
        ]
        for weight, value in zip(weights, stationary):
            steps.append(step("D", weight, total_weight, prob_txt(value)))
        for left, right in ((0, 1), (0, 2), (1, 2)):
            forward = stationary[left] * matrix[left][right]
            backward = stationary[right] * matrix[right][left]
            steps.extend([
                step("M", prob_txt(stationary[left]),
                     prob_txt(matrix[left][right]), prob_txt(forward)),
                step("M", prob_txt(stationary[right]),
                     prob_txt(matrix[right][left]), prob_txt(backward)),
                step("CHECK", f"detailed balance {left + 1}↔{right + 1}",
                     prob_txt(forward), prob_txt(backward)),
            ])
        answer = "pi = " + _row_text(stationary)
        return _problem(matrix, target), steps, answer

    @staticmethod
    def _distribution():
        matrix = _general_matrix()
        initial = _positive_row()
        target = "distribution after one step"
        steps = [_setup(matrix, target)]
        output = []
        for end in range(3):
            terms = [initial[start] * matrix[start][end] for start in range(3)]
            for start, term in enumerate(terms):
                steps.append(step("M", prob_txt(initial[start]),
                                  prob_txt(matrix[start][end]), prob_txt(term)))
            total = _sum_three(steps, terms)
            steps.append(step("DIST_ENTRY", f"state {end + 1}",
                              "sum incoming flow", prob_txt(total)))
            output.append(total)
        steps.append(step("CHECK", "next-state probabilities sum to 1",
                          "+".join(prob_txt(value) for value in output), 1))
        answer = "after one step = " + _row_text(output)
        return _problem(matrix, target, initial), steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "two_step":
            problem, steps, answer = self._two_step()
        elif variant == "path_probability":
            problem, steps, answer = self._path_probability()
        elif variant == "hitting_prob_3state":
            problem, steps, answer = self._hitting_probability()
        elif variant == "expected_hitting_time":
            problem, steps, answer = self._hitting_time()
        elif variant == "stationary_3state":
            problem, steps, answer = self._stationary()
        else:
            problem, steps, answer = self._distribution()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_multi_state_markov_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

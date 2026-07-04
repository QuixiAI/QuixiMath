import ast
import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.permutation_group_generator import PermutationGroupGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"In S_(\d+), let sigma=(\[[\d, ]+\]) and tau=(\[[\d, ]+\]), "
    r"where each list gives images of 1\.\.(\d+)\. Compute sigma after "
    r"tau, then give cycle notation, order, and parity\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def list_text(values):
    return ", ".join(str(value) for value in values)


def perm_text(perm):
    return "[" + list_text(perm) + "]"


def compose(sigma, tau):
    return [sigma[tau[i] - 1] for i in range(len(sigma))]


def cycles_of(perm):
    n = len(perm)
    seen = [False] * n
    cycles = []
    for start in range(1, n + 1):
        if seen[start - 1]:
            continue
        current = start
        cycle = []
        while not seen[current - 1]:
            seen[current - 1] = True
            cycle.append(current)
            current = perm[current - 1]
        if len(cycle) > 1:
            cycles.append(cycle)
    return cycles


def cycle_text(cycles):
    if not cycles:
        return "identity"
    return "".join("(" + " ".join(str(value) for value in cycle) + ")"
                   for cycle in cycles)


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    n1, sigma_text, tau_text, n2 = match.groups()
    n = int(n1)
    assert n == int(n2)
    sigma = ast.literal_eval(sigma_text)
    tau = ast.literal_eval(tau_text)
    return n, sigma, tau


def expected_flow(n, sigma, tau):
    composed = compose(sigma, tau)
    cycles = cycles_of(composed)
    steps = [
        make_step("PERM_SETUP", f"n={n}", f"sigma={perm_text(sigma)}",
                  f"tau={perm_text(tau)}"),
    ]
    for idx, tau_value in enumerate(tau, start=1):
        image = sigma[tau_value - 1]
        steps.append(make_step("PERM_COMPOSE", f"i={idx}",
                               f"tau(i)={tau_value}",
                               f"sigma(tau(i))={image}"))
    steps.append(make_step("PERM_RESULT", perm_text(composed)))

    for cycle in cycles:
        trace = "->".join(str(value) for value in cycle + [cycle[0]])
        steps.append(make_step("CYCLE_TRACE", f"start {cycle[0]}", trace))
        steps.append(make_step("CYCLE", cycle_text([cycle])))
    lengths = [len(cycle) for cycle in cycles]
    steps.append(make_step("CYCLE_LENGTHS", list_text(lengths) or "none"))

    order = 1
    for length in lengths:
        g = gcd(order, length)
        new_order = lcm(order, length)
        steps.append(make_step("GCD_RESULT", f"gcd({order},{length})", g))
        steps.append(make_step("LCM_STEP", order, length, new_order))
        order = new_order

    transpositions = 0
    for length in lengths:
        contribution = length - 1
        steps.append(make_step("S", length, 1, contribution))
        new_total = transpositions + contribution
        steps.append(make_step("A", transpositions, contribution, new_total))
        transpositions = new_total
    parity = "even" if transpositions % 2 == 0 else "odd"
    steps.append(make_step("PARITY", f"transpositions {transpositions}",
                           parity))

    answer = (
        f"composition = {perm_text(composed)}; cycles = {cycle_text(cycles)}; "
        f"order = {order}; parity = {parity}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPermutationGroupGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PermutationGroupGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "permutation_group")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            n, sigma, tau = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(n, sigma, tau)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_permutation_conditions_and_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            n, sigma, tau = parse_problem(result["problem"])
            self.assertEqual(sorted(sigma), list(range(1, n + 1)))
            self.assertEqual(sorted(tau), list(range(1, n + 1)))
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

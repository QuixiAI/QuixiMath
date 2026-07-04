import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.index_gymnastics_generator import IndexGymnasticsGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Evaluate c \* sum_i eps_i(\d)(\d) eps_i(\d)(\d) with c=(-?\d+) "
    r"for j=(\d), k=(\d), l=(\d), m=(\d) in 3D, and verify the "
    r"Kronecker-delta identity\."
)
INDICES = [1, 2, 3]


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def epsilon(a, b, c):
    values = [a, b, c]
    if len(set(values)) < 3:
        return 0
    inversions = sum(
        1
        for i in range(3)
        for j in range(i + 1, 3)
        if values[i] > values[j]
    )
    return -1 if inversions % 2 else 1


def delta(a, b):
    return 1 if a == b else 0


def scaled_target_text(coeff, j, k, l, m):
    body = f"sum_i eps_i{j}{k} eps_i{l}{m}"
    if coeff == 1:
        return body
    if coeff == -1:
        return f"-{body}"
    return f"{coeff}*{body}"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    p_j, p_k, p_l, p_m, coeff, j, k, l, m = map(int, match.groups())
    assert (p_j, p_k, p_l, p_m) == (j, k, l, m)
    return coeff, j, k, l, m


def expected_flow(example):
    coeff, j, k, l, m = parse_problem(example["problem"])
    eps_products = []
    steps = [
        make_step("INDEX_SETUP", f"c={coeff}", f"j={j}, k={k}",
                  f"l={l}, m={m}"),
        make_step("IDENTITY", "sum_i eps_ijk eps_ilm",
                  "delta_jl delta_km - delta_jm delta_kl"),
    ]
    for i in INDICES:
        left = epsilon(i, j, k)
        right = epsilon(i, l, m)
        product = left * right
        eps_products.append(product)
        steps.extend([
            make_step("EPSILON_VALUE", f"eps_{i}{j}{k}", left),
            make_step("EPSILON_VALUE", f"eps_{i}{l}{m}", right),
            make_step("M", left, right, product),
        ])
    partial = eps_products[0] + eps_products[1]
    lhs = partial + eps_products[2]
    d_jl = delta(j, l)
    d_km = delta(k, m)
    d_jm = delta(j, m)
    d_kl = delta(k, l)
    rhs_left = d_jl * d_km
    rhs_right = d_jm * d_kl
    rhs = rhs_left - rhs_right
    scaled = coeff * lhs
    steps.extend([
        make_step("A", eps_products[0], eps_products[1], partial),
        make_step("A", partial, eps_products[2], lhs),
        make_step("DELTA_VALUE", f"delta_{j}{l}", d_jl),
        make_step("DELTA_VALUE", f"delta_{k}{m}", d_km),
        make_step("DELTA_VALUE", f"delta_{j}{m}", d_jm),
        make_step("DELTA_VALUE", f"delta_{k}{l}", d_kl),
        make_step("M", d_jl, d_km, rhs_left),
        make_step("M", d_jm, d_kl, rhs_right),
        make_step("S", rhs_left, rhs_right, rhs),
        make_step("CHECK", "epsilon contraction", rhs, "identity"),
        make_step("M", coeff, lhs, scaled),
    ])
    target = scaled_target_text(coeff, j, k, l, m)
    answer = f"{target} = {scaled}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestIndexGymnasticsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = IndexGymnasticsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_both_nonzero_signs_occur(self):
        random.seed(7)
        values = set()
        gen = IndexGymnasticsGenerator()
        for _ in range(500):
            coeff, j, k, l, m = parse_problem(gen.generate()["problem"])
            contraction = sum(epsilon(i, j, k) * epsilon(i, l, m)
                              for i in INDICES)
            values.add(contraction)
        self.assertIn(1, values)
        self.assertIn(-1, values)
        self.assertIn(0, values)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.casimir_generator import CasimirGenerator
from helpers import DELIM


SPIN_RE = re.compile(r"spin-(\d+(?:/\d+)?)")
HBAR_RE = re.compile(r"hbar=(\d+(?:/\d+)?)")
ELEMENT_RE = re.compile(r"(\S+) entry at m=(-?\d+(?:/\d+)?)")
JP_RE = re.compile(r"Jplus=hbar\*(\[\[.*?\]\])")
JM_RE = re.compile(r"Jminus=hbar\*(\[\[.*?\]\])")
JZ_RE = re.compile(r"Jz=hbar\*(\[\[.*?\]\])")


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def diag(values):
    return [
        [values[i] if i == j else Fraction(0) for j in range(len(values))]
        for i in range(len(values))
    ]


def mat_add(A, B):
    return [
        [A[i][j] + B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def mat_scale(A, scalar):
    return [[scalar * value for value in row] for row in A]


def m_values(j):
    return [j - k for k in range(int(2 * j) + 1)]


def parse_problem(problem):
    spin = SPIN_RE.search(problem)
    assert spin is not None, problem
    hbar = HBAR_RE.search(problem)
    assert hbar is not None, problem
    parts = {
        "j": Fraction(spin.group(1)),
        "hbar": Fraction(hbar.group(1)),
    }
    element = ELEMENT_RE.search(problem)
    if element is not None:
        parts["variant"] = "element"
        parts["operator"] = element.group(1)
        parts["m"] = Fraction(element.group(2))
    elif "eigenvalue" in problem or "multiplet" in problem:
        parts["variant"] = "eigenvalue"
    else:
        parts["variant"] = "verify"
    return parts


def parse_symbol_matrix(text):
    """[[0, sqrt3, 0], ...] -> float matrix."""
    rows = re.findall(r"\[([^\[\]]+)\]", text)
    out = []
    for row in rows:
        values = []
        for token in row.split(", "):
            token = token.strip()
            if token.startswith("sqrt"):
                values.append(math.sqrt(float(token[4:])))
            else:
                values.append(float(Fraction(token)))
        out.append(values)
    return out


def ladder_matrices(j):
    """Numeric Jz, Jplus, Jminus in units of hbar, built from scratch."""
    ms = m_values(j)
    size = len(ms)
    jz = [[float(ms[i]) if i == k else 0.0 for k in range(size)]
          for i in range(size)]
    jp = [[0.0] * size for _ in range(size)]
    jm = [[0.0] * size for _ in range(size)]
    for index, m in enumerate(ms):
        if index > 0:
            jp[index - 1][index] = math.sqrt(float((j - m) * (j + m + 1)))
        if index < size - 1:
            jm[index + 1][index] = math.sqrt(float((j + m) * (j - m + 1)))
    return jz, jp, jm


def matmul(A, B):
    size = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(size))
             for j in range(size)] for i in range(size)]


def casimir_numeric(problem, parts):
    """J^2 by honest matrix multiplication, using the problem's matrices."""
    jp_text = JP_RE.search(problem)
    if jp_text is not None:
        jp = parse_symbol_matrix(jp_text.group(1))
        jm = parse_symbol_matrix(JM_RE.search(problem).group(1))
        jz = parse_symbol_matrix(JZ_RE.search(problem).group(1))
    else:
        jz, jp, jm = ladder_matrices(parts["j"])
    jz_sq = matmul(jz, jz)
    plus_minus = matmul(jp, jm)
    minus_plus = matmul(jm, jp)
    size = len(jz)
    scale = float(parts["hbar"]) ** 2
    return [[scale * (jz_sq[i][k]
                      + 0.5 * (plus_minus[i][k] + minus_plus[i][k]))
             for k in range(size)] for i in range(size)]


def element_value(operator, j, m, hbar_sq):
    if operator == "JplusJminus":
        return (j + m) * (j - m + 1) * hbar_sq
    if operator == "JminusJplus":
        return (j - m) * (j + m + 1) * hbar_sq
    if operator == "Jz^2":
        return m * m * hbar_sq
    assert operator == "J^2", operator
    return j * (j + 1) * hbar_sq


def oracle(example):
    parts = parse_problem(example["problem"])
    j = parts["j"]
    hbar_sq = parts["hbar"] ** 2
    if parts["variant"] == "element":
        value = element_value(parts["operator"], j, parts["m"], hbar_sq)
        return (f"{parts['operator']} at m={fraction_text(parts['m'])} = "
                f"{fraction_text(value)}")
    ms = m_values(j)
    dim = len(ms)
    # Independent route: average the diagonal of J^2 built entry by entry.
    trace = sum(
        m * m + Fraction((j + m) * (j - m + 1) + (j - m) * (j + m + 1), 2)
        for m in ms
    ) * hbar_sq
    eigen = trace / dim
    if parts["variant"] == "eigenvalue":
        return f"J^2 = {fraction_text(eigen)}; dim = {dim}"
    return (f"J^2 = {fraction_text(eigen)}I = "
            f"{matrix_text(diag([eigen] * dim))}")


class TestCasimirGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CasimirGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle(result),
                             result["problem"])

    def test_matrix_product_route_agrees(self):
        """Multiply the ladder matrices out and compare with the answer."""
        for _ in range(200):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            if parts["variant"] == "element":
                continue
            product = casimir_numeric(result["problem"], parts)
            eigen = float(Fraction(
                result["final_answer"].split("=")[1].split(";")[0]
                .replace("I", "").strip()))
            size = len(product)
            for i in range(size):
                for k in range(size):
                    target = eigen if i == k else 0.0
                    self.assertAlmostEqual(product[i][k], target,
                                           delta=1e-6 * max(1.0, abs(eigen)),
                                           msg=result["problem"])

    def test_step_arithmetic_and_matrices(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            j = parts["j"]
            hbar_sq = parts["hbar"] ** 2
            ms = m_values(j)
            seen = set()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                op = fields[0]
                seen.add(op)
                if op == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif op == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif op == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif op == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif op == "MATRIX_PRODUCT":
                    if fields[1] == "Jz^2":
                        expected = diag([m * m * hbar_sq for m in ms])
                    elif fields[1] == "J+J-":
                        expected = diag([(j + m) * (j - m + 1) * hbar_sq
                                         for m in ms])
                    else:
                        self.assertEqual(fields[1], "J-J+", raw_step)
                        expected = diag([(j - m) * (j + m + 1) * hbar_sq
                                         for m in ms])
                    self.assertEqual(fields[2], matrix_text(expected),
                                     raw_step)
                elif op == "MATRIX_ADD" and fields[1] == "J+J- + J-J+":
                    expected = diag([
                        ((j + m) * (j - m + 1) + (j - m) * (j + m + 1))
                        * hbar_sq for m in ms])
                    self.assertEqual(fields[2], matrix_text(expected),
                                     raw_step)
                elif op == "MATRIX_SCALE":
                    expected = diag([
                        Fraction((j + m) * (j - m + 1)
                                 + (j - m) * (j + m + 1), 2) * hbar_sq
                        for m in ms])
                    self.assertEqual(fields[2], matrix_text(expected),
                                     raw_step)
                elif op == "MATRIX_ADD":
                    self.assertEqual(fields[1], "Jz^2 + ladder half", raw_step)
                    eigen = j * (j + 1) * hbar_sq
                    self.assertEqual(fields[2],
                                     matrix_text(diag([eigen] * len(ms))),
                                     raw_step)
                elif op == "DIM":
                    self.assertEqual(fields[1],
                                     f"2*{fraction_text(j)}+1", raw_step)
                    self.assertEqual(int(fields[2]), len(ms), raw_step)
                elif op == "CHECK" and fields[1] == "sum_rule":
                    left = Fraction(fields[2].split("=")[1])
                    right = Fraction(fields[3].split("=")[1])
                    self.assertEqual(left, right, raw_step)
                elif op == "CHECK" and fields[1] == "trace":
                    left = Fraction(fields[2].split("=")[1])
                    right = Fraction(fields[3].split("=")[1])
                    self.assertEqual(left, right, raw_step)
                elif op == "CHECK":
                    self.assertEqual(fields[1], "J^2", raw_step)
                    self.assertEqual(fields[3], "verified", raw_step)
                elif op == "Z":
                    self.assertEqual(fields[1:], [result["final_answer"]])
                else:
                    self.assertEqual(op, "CASIMIR_SETUP", raw_step)
                    self.assertEqual(fields[1], f"spin={fraction_text(j)}")
                    self.assertEqual(
                        fields[2], f"hbar={fraction_text(parts['hbar'])}")
            self.assertIn("CASIMIR_SETUP", seen)
            self.assertIn("Z", seen)

    def test_variants_and_spread(self):
        variants = set()
        spins = set()
        hbars = set()
        operators = set()
        openings = set()
        for _ in range(600):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            variants.add(parts["variant"])
            spins.add(parts["j"])
            hbars.add(parts["hbar"])
            operators.add(parts.get("operator"))
            openings.add(result["problem"].split(" ", 2)[0])
        self.assertEqual(variants, {"verify", "eigenvalue", "element"})
        self.assertGreaterEqual(len(spins), 8)
        self.assertGreaterEqual(len(hbars), 100)
        self.assertGreaterEqual(len(operators), 5)
        self.assertGreaterEqual(len(openings), 6)

    def test_fixed_variant_constructor(self):
        for variant in CasimirGenerator.VARIANTS:
            result = CasimirGenerator(variant).generate()
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)
        with self.assertRaises(ValueError):
            CasimirGenerator("bogus")

    def test_spin1_operation_preserved(self):
        gen = CasimirGenerator("verify")
        operations = {gen.generate()["operation"] for _ in range(200)}
        self.assertIn("casimir_spin1", operations)

    def test_deterministic_under_seed(self):
        random.seed(11)
        first = [self.gen.generate() for _ in range(20)]
        random.seed(11)
        second = [self.gen.generate() for _ in range(20)]
        self.assertEqual([ex["steps"] for ex in first],
                         [ex["steps"] for ex in second])

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

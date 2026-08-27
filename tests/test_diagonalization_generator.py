import ast
import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.diagonalization_generator import DiagonalizationGenerator
from helpers import DELIM


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


# --------------------------------------------------------------- phrasings

MATRIX = r"\[\[-?\d+, -?\d+\], \[-?\d+, -?\d+\]\]"
VECTOR = r"\[-?\d+, -?\d+\]"

PHRASINGS = [
    # power
    (r"Diagonalize A = (?P<A>{M}) and compute A\^(?P<k>\d+)\.", "power"),
    (r"Let A = (?P<A>{M})\. Write A = P·D·P\^-1 with D diagonal, then use "
     r"that form to find A\^(?P<k>\d+)\.", "power"),
    (r"Find an eigenvector matrix P and a diagonal matrix D with "
     r"A = P·D·P\^-1 for A = (?P<A>{M}), and evaluate A\^(?P<k>\d+)\.",
     "power"),
    (r"Use diagonalization to raise A = (?P<A>{M}) to the power "
     r"(?P<k>\d+)\.", "power"),
    (r"For A = (?P<A>{M}), give the diagonalization P, D, P\^-1 and the "
     r"matrix A\^(?P<k>\d+)\.", "power"),
    # decompose
    (r"Diagonalize A = (?P<A>{M})\.", "decompose"),
    (r"Let A = (?P<A>{M})\. Find P, D, and P\^-1 with A = P·D·P\^-1 and D "
     r"diagonal\.", "decompose"),
    (r"Find the eigenvalues and eigenvectors of A = (?P<A>{M}) and use them "
     r"to write A = P·D·P\^-1\.", "decompose"),
    (r"Write A = (?P<A>{M}) in the form P·D·P\^-1 with D diagonal\.",
     "decompose"),
    (r"Give an eigendecomposition A = P·D·P\^-1 for A = (?P<A>{M})\.",
     "decompose"),
    # vector_power
    (r"Let A = (?P<A>{M}) and x = (?P<x>{V})\. Use the diagonalization of A "
     r"to compute A\^(?P<k>\d+)x\.", "vector_power"),
    (r"Diagonalize A = (?P<A>{M}), expand x = (?P<x>{V}) in the eigenbasis, "
     r"and find A\^(?P<k>\d+)x\.", "vector_power"),
    (r"For A = (?P<A>{M}), write x = (?P<x>{V}) as a combination of "
     r"eigenvectors and compute A\^(?P<k>\d+)x\.", "vector_power"),
    (r"A state vector x = (?P<x>{V}) is advanced (?P<k>\d+) steps by "
     r"A = (?P<A>{M})\. Using eigenvectors, find A\^\d+x\.", "vector_power"),
    (r"Given A = (?P<A>{M}) and x = (?P<x>{V}), use A\^(?P<k>\d+) = "
     r"P·D\^\d+·P\^-1 to evaluate A\^\d+x\.", "vector_power"),
]

COMPILED = [
    (re.compile(body.replace("{M}", MATRIX).replace("{V}", VECTOR)), kind)
    for body, kind in PHRASINGS
]


def parse_problem(problem):
    """Returns (kind, A, k, x, phrasing_index) for any phrasing."""
    for index, (pattern, kind) in enumerate(COMPILED):
        match = pattern.fullmatch(problem)
        if match is None:
            continue
        groups = match.groupdict()
        A = ast.literal_eval(groups["A"])
        k = int(groups["k"]) if groups.get("k") else None
        x = ast.literal_eval(groups["x"]) if groups.get("x") else None
        return kind, A, k, x, index
    raise AssertionError(f"unparsed problem: {problem}")


# ----------------------------------------------------- independent linear alg

def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B)))
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def matrix_power(A, k):
    """Repeated multiplication -- independent of any diagonalization."""
    result = [[1, 0], [0, 1]]
    for _ in range(k):
        result = matmul(result, A)
    return result


def inverse_2x2(A):
    a, b = A[0]
    c, d = A[1]
    det = a * d - b * c
    return [[d // det, -b // det], [-c // det, a // det]]


def eigenvalues(A):
    trace = A[0][0] + A[1][1]
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = trace * trace - 4 * det
    root = math.isqrt(disc)
    assert root * root == disc
    return sorted([(trace - root) // 2, (trace + root) // 2])


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def rref(M):
    work = [[Fraction(v) for v in row] for row in M]
    rows, cols = len(work), len(work[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows)
                      if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [v / scale for v in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [
                work[r][j] - factor * work[pivot_row][j]
                for j in range(cols)
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivot_cols


def primitive_int_vector(vec):
    scale = 1
    for value in vec:
        scale = lcm(scale, value.denominator)
    ints = [value.numerator * (scale // value.denominator) for value in vec]
    common = 0
    for value in ints:
        common = gcd(common, abs(value))
    ints = [value // common for value in ints]
    first = next(value for value in ints if value != 0)
    if first < 0:
        ints = [-value for value in ints]
    return ints


def subtract_lambda(A, lam):
    return [
        [A[i][j] - (lam if i == j else 0) for j in range(2)]
        for i in range(2)
    ]


def null_vector(M):
    R, pivot_cols = rref(M)
    free_cols = [j for j in range(2) if j not in pivot_cols]
    vec = [Fraction(0), Fraction(0)]
    vec[free_cols[0]] = Fraction(1)
    for row, pivot in enumerate(pivot_cols):
        vec[pivot] = -R[row][free_cols[0]]
    return primitive_int_vector(vec)


def columns_to_matrix(cols):
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


def poly_text(lambdas):
    trace = sum(lambdas)
    det = lambdas[0] * lambdas[1]
    coeffs = [1, -trace, det]
    pieces = ["λ^2"]
    if coeffs[1] > 0:
        body = "λ" if coeffs[1] == 1 else f"{coeffs[1]}λ"
        pieces.append(f"+ {body}")
    elif coeffs[1] < 0:
        body = "λ" if coeffs[1] == -1 else f"{abs(coeffs[1])}λ"
        pieces.append(f"- {body}")
    if coeffs[2] > 0:
        pieces.append(f"+ {coeffs[2]}")
    elif coeffs[2] < 0:
        pieces.append(f"- {abs(coeffs[2])}")
    return " ".join(pieces)


def factor_text(root):
    if root > 0:
        return f"(λ - {root})"
    return f"(λ + {-root})"


def oracle_parts(A, k):
    lambdas = eigenvalues(A)
    vectors = [null_vector(subtract_lambda(A, lam)) for lam in lambdas]
    P = columns_to_matrix(vectors)
    P_inv = inverse_2x2(P)
    D = [[lambdas[0], 0], [0, lambdas[1]]]
    Dk = None if k is None else [[lambdas[0] ** k, 0], [0, lambdas[1] ** k]]
    Ak = None if k is None else matrix_power(A, k)
    return lambdas, vectors, P, P_inv, D, Dk, Ak


def oracle_answer(example):
    """Recompute the answer from the problem text with repeated products."""
    kind, A, k, x, _ = parse_problem(example["problem"])
    lambdas, vectors, P, P_inv, D, Dk, Ak = oracle_parts(A, k)
    if kind == "decompose":
        return (f"P={fmt_matrix(P)}, D={fmt_matrix(D)}, "
                f"P^-1={fmt_matrix(P_inv)}")
    if kind == "power":
        return (f"P={fmt_matrix(P)}, D={fmt_matrix(D)}, "
                f"P^-1={fmt_matrix(P_inv)}, A^{k}={fmt_matrix(Ak)}")
    c = matvec(P_inv, x)
    y = matvec(Ak, x)
    return f"c={c}, A^{k}x={y}"


def eval_integer_expr(expr):
    expr = re.sub(r"-?\d+", lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def parse_scalar_vector(text):
    if text.startswith("v = "):
        return 1, ast.literal_eval(text.removeprefix("v = "))
    if text.startswith("-v = "):
        return -1, ast.literal_eval(text.removeprefix("-v = "))
    lam_txt, lv_txt = text.split("*v = ")
    return int(lam_txt), ast.literal_eval(lv_txt)


def check_step_arithmetic(example):
    kind, A, k, x, _ = parse_problem(example["problem"])
    lambdas, vectors, P, P_inv, D, Dk, Ak = oracle_parts(A, k)
    factored = "*".join(factor_text(lam) for lam in lambdas)
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "CHAR_POLY":
            if parts[1] != f"p(λ) = {poly_text(lambdas)}":
                return False
            if parts[2] != factored:
                return False
        elif parts[0] == "E":
            if int(parts[1]) ** int(parts[2]) != int(parts[3]):
                return False
        elif parts[0] == "EIGENVECTOR":
            lam = int(parts[1].split(" = ")[1])
            vec = ast.literal_eval(parts[2])
            if matvec(subtract_lambda(A, lam), vec) != [0, 0]:
                return False
        elif parts[0] == "CHECK" and parts[1].startswith("A*"):
            vec = ast.literal_eval(parts[1][2:])
            Av = ast.literal_eval(parts[2])
            lam, lv = parse_scalar_vector(parts[3])
            if Av != matvec(A, vec):
                return False
            if lv != [lam * value for value in vec]:
                return False
        elif parts[0] == "DIAG_FORM":
            if parts[1] != f"P = {fmt_matrix(P)}":
                return False
            if parts[2] != f"D = {fmt_matrix(D)}":
                return False
            if parts[3] != f"P^-1 = {fmt_matrix(P_inv)}":
                return False
        elif parts[0] == "D_POWER":
            if parts[1] != f"D^{k}" or parts[2] != fmt_matrix(Dk):
                return False
        elif parts[0] == "POWER_ENTRY":
            if eval_integer_expr(parts[2]) != Fraction(parts[3]):
                return False
            i, j = ast.literal_eval(parts[1])
            if Ak[i - 1][j - 1] != int(parts[3]):
                return False
        elif parts[0] == "COORDS":
            if ast.literal_eval(parts[2]) != matvec(P_inv, x):
                return False
        elif parts[0] == "COMBO":
            if ast.literal_eval(parts[2]) != x:
                return False
        elif parts[0] == "SCALE_MODE":
            if eval_integer_expr(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "VEC_ENTRY":
            if eval_integer_expr(parts[2]) != Fraction(parts[3]):
                return False
            row = int(parts[1].strip("()"))
            if matvec(Ak, x)[row - 1] != int(parts[3]):
                return False
        elif parts[0] == "CHECK" and parts[1].startswith("P*["):
            coords = ast.literal_eval(parts[1][2:])
            if ast.literal_eval(parts[2]) != matvec(P, coords):
                return False
        elif parts[0] == "CHECK" and parts[1] == f"direct A^{k}":
            if ast.literal_eval(parts[2]) != matrix_power(A, k):
                return False
        elif parts[0] == "CHECK" and parts[1] == f"direct A^{k}x":
            if ast.literal_eval(parts[2]) != matvec(matrix_power(A, k), x):
                return False
    return True


class TestDiagonalizationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DiagonalizationGenerator()

    def test_output_contract(self):
        for _ in range(60):
            result = self.gen.generate()
            for key in ("problem_id", "operation", "problem", "steps",
                        "final_answer"):
                self.assertIn(key, result)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                             result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_p_is_unimodular_and_matches_eigenvectors(self):
        for _ in range(300):
            result = self.gen.generate()
            _, A, _, _, _ = parse_problem(result["problem"])
            lambdas, vectors, P, _, _, _, _ = oracle_parts(A, None)
            det = P[0][0] * P[1][1] - P[0][1] * P[1][0]
            self.assertIn(det, (1, -1), (A, P))
            self.assertNotEqual(lambdas[0], lambdas[1])
            for lam, vec in zip(lambdas, vectors):
                self.assertEqual(matvec(A, vec),
                                 [lam * v for v in vec])

    def test_power_entries_cover_matrix(self):
        gen = DiagonalizationGenerator("power")
        for _ in range(100):
            result = gen.generate()
            entries = [s for s in result["steps"]
                       if s.startswith(f"POWER_ENTRY{DELIM}")]
            self.assertEqual(len(entries), 4)

    def test_vector_power_entries_cover_vector(self):
        gen = DiagonalizationGenerator("vector_power")
        for _ in range(100):
            result = gen.generate()
            entries = [s for s in result["steps"]
                       if s.startswith(f"VEC_ENTRY{DELIM}")]
            self.assertEqual(len(entries), 2)
            self.assertTrue(any(s.startswith(f"COORDS{DELIM}")
                                for s in result["steps"]))

    def test_all_variants_and_operations(self):
        expected = {
            "power": "diagonalization_power",
            "decompose": "diagonalization_decompose",
            "vector_power": "diagonalization_vector_power",
        }
        for variant, operation in expected.items():
            gen = DiagonalizationGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["operation"], operation)
                kind, _, _, _, _ = parse_problem(result["problem"])
                self.assertEqual(kind, variant)
        seen = {self.gen.generate()["operation"] for _ in range(300)}
        self.assertEqual(seen, set(expected.values()))

    def test_all_phrasings_parse(self):
        seen = set()
        for _ in range(1500):
            _, _, _, _, index = parse_problem(self.gen.generate()["problem"])
            seen.add(index)
        self.assertEqual(seen, set(range(len(COMPILED))))

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"--|\+ -|- -|\^1\b|(?<!\d)1λ|(?<!\d)1\*")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))
            for raw_step in result["steps"]:
                self.assertIsNone(bad.search(raw_step), raw_step)

    def test_operands_stay_hand_sized(self):
        for _ in range(300):
            result = self.gen.generate()
            values = [abs(int(v))
                      for v in re.findall(r"-?\d+", result["final_answer"])]
            self.assertLessEqual(max(values), 20000, result["final_answer"])

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)

    def test_capacity_is_wide(self):
        texts = {self.gen.generate()["problem"] for _ in range(800)}
        self.assertGreaterEqual(len(texts), 790)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DiagonalizationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

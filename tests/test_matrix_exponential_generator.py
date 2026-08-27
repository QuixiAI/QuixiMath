import ast
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

from generators.matrix_exponential_generator import MatrixExponentialGenerator
from helpers import DELIM


MATRIX_RE = r"(\[\[-?\d+, -?\d+\], \[-?\d+, -?\d+\]\])"
VECTOR_RE = r"(\[-?\d+, -?\d+\])"

# Independent copy of the phrasing templates: drift between the generator and
# this list makes test_every_phrasing_is_parsed fail loudly.
EXP_TEMPLATES = [
    "Find e^(At) for A = {matrix} by diagonalization.",
    "Compute the matrix exponential e^(At) for A = {matrix} using "
    "diagonalization.",
    "Diagonalize A = {matrix} and use P e^(Dt) P^-1 to write e^(At).",
    "The matrix A = {matrix} has two distinct integer eigenvalues. "
    "Find e^(At).",
    "For the system x' = Ax with A = {matrix}, find the fundamental "
    "matrix e^(At).",
    "Use the factorization A = P D P^-1 to compute e^(At) when "
    "A = {matrix}.",
]

IVP_TEMPLATES = [
    "Solve the initial value problem x' = Ax with A = {matrix} and "
    "x(0) = {vector}.",
    "For A = {matrix}, find x(t) satisfying x' = Ax with x(0) = {vector}.",
    "A linear system x' = Ax has A = {matrix}. Find the solution with "
    "initial state x(0) = {vector}.",
    "Use e^(At) to solve x' = Ax where A = {matrix} and x(0) = {vector}.",
    "Find the vector x(t) = e^(At)x(0) for A = {matrix} and "
    "x(0) = {vector}.",
    "The system x' = Ax with A = {matrix} starts at x(0) = {vector}. "
    "Give x(t).",
]


def to_pattern(template):
    parts = re.split(r"(\{matrix\}|\{vector\})", template)
    lookup = {"{matrix}": MATRIX_RE, "{vector}": VECTOR_RE}
    return "".join(lookup.get(part, re.escape(part)) for part in parts)


EXP_PATTERNS = [re.compile(to_pattern(t)) for t in EXP_TEMPLATES]
IVP_PATTERNS = [re.compile(to_pattern(t)) for t in IVP_TEMPLATES]


def parse_problem(problem):
    """Return (index, kind, A, x0) for whichever phrasing matched."""
    for idx, pattern in enumerate(EXP_PATTERNS):
        m = pattern.fullmatch(problem)
        if m:
            return idx, "exponential", ast.literal_eval(m.group(1)), None
    for idx, pattern in enumerate(IVP_PATTERNS):
        m = pattern.fullmatch(problem)
        if m:
            return (idx, "ivp", ast.literal_eval(m.group(1)),
                    ast.literal_eval(m.group(2)))
    raise AssertionError(f"unparsed phrasing: {problem!r}")


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B)))
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def inverse_2x2(A):
    a, b = A[0]
    c, d = A[1]
    det = a * d - b * c
    return [[d // det, -b // det], [-c // det, a // det]]


def eigenvalues(A):
    trace = A[0][0] + A[1][1]
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = trace * trace - 4 * det
    assert disc > 0, A
    root = math.isqrt(disc)
    assert root * root == disc, A
    return sorted([(trace - root) // 2, (trace + root) // 2])


def spectral_projectors(A, lambdas):
    """Sylvester's formula: C_k = prod_{j != k} (A - lambda_j I)/(l_k - l_j).

    This is an eigenvector-free route to e^(At) = C_1 e^(l1 t) + C_2 e^(l2 t),
    completely independent of the generator's P D P^-1 construction.
    """
    lam1, lam2 = lambdas
    proj = []
    for lam_k, lam_other in ((lam1, lam2), (lam2, lam1)):
        denom = Fraction(lam_k - lam_other)
        block = [
            [Fraction(A[i][j] - (lam_other if i == j else 0)) / denom
             for j in range(2)]
            for i in range(2)
        ]
        for row in block:
            for value in row:
                assert value.denominator == 1, (A, lambdas)
        proj.append([[int(v) for v in row] for row in block])
    return proj


def exp_text(lam):
    if lam == 1:
        return "e^t"
    if lam == -1:
        return "e^(-t)"
    return f"e^({lam}t)"


def combo_text(terms):
    pieces = []
    for coeff, lam in terms:
        if coeff == 0:
            continue
        body = exp_text(lam) if abs(coeff) == 1 else (
            f"{abs(coeff)}*{exp_text(lam)}"
        )
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def symbolic_matrix(entries):
    return "[" + ", ".join(
        "[" + ", ".join(row) + "]" for row in entries
    ) + "]"


def oracle_parts(problem):
    """Recompute everything the answer needs straight from the problem text."""
    _, kind, A, x0 = parse_problem(problem)
    lambdas = eigenvalues(A)
    C1, C2 = spectral_projectors(A, lambdas)
    records = [
        [[(C1[i][j], lambdas[0]), (C2[i][j], lambdas[1])] for j in range(2)]
        for i in range(2)
    ]
    entries = [[combo_text(records[i][j]) for j in range(2)] for i in range(2)]
    return kind, A, x0, lambdas, C1, C2, records, entries


def oracle_answer(example):
    kind, A, x0, lambdas, C1, C2, records, entries = oracle_parts(
        example["problem"])
    if kind == "ivp":
        v1 = matvec(C1, x0)
        v2 = matvec(C2, x0)
        comps = [combo_text([(v1[i], lambdas[0]), (v2[i], lambdas[1])])
                 for i in range(2)]
        return "x(t)=[" + ", ".join(comps) + "]"
    return f"e^(At)={symbolic_matrix(entries)}"


def parse_scalar_vector(text):
    if text.startswith("v = "):
        return 1, ast.literal_eval(text.removeprefix("v = "))
    if text.startswith("-v = "):
        return -1, ast.literal_eval(text.removeprefix("-v = "))
    lam_txt, lv_txt = text.split("*v = ")
    return int(lam_txt), ast.literal_eval(lv_txt)


def subtract_lambda(A, lam):
    return [[A[i][j] - (lam if i == j else 0) for j in range(2)]
            for i in range(2)]


def value_at_zero(records):
    return [[sum(coeff for coeff, _ in row[j]) for j in range(2)]
            for row in records]


def derivative_at_zero(records):
    return [[sum(coeff * lam for coeff, lam in row[j]) for j in range(2)]
            for row in records]


def check_step_arithmetic(test, example):
    kind, A, x0, lambdas, C1, C2, records, entries = oracle_parts(
        example["problem"])
    expD = [[exp_text(lambdas[0]), "0"], ["0", exp_text(lambdas[1])]]
    seen = set()
    P = None
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        seen.add(code)
        if code == "MAT_SETUP":
            test.assertEqual(parts[1], f"A = {fmt_matrix(A)}")
            if kind == "ivp":
                test.assertIn(str(x0), parts[2])
        elif code == "EIGENVALUE":
            test.assertIn(int(parts[1].split(" = ")[1]), lambdas)
        elif code == "EIGENVECTOR":
            lam = int(parts[1].split(" = ")[1])
            vec = ast.literal_eval(parts[2])
            test.assertNotEqual(vec, [0, 0])
            test.assertEqual(matvec(subtract_lambda(A, lam), vec), [0, 0])
        elif code == "CHECK" and parts[1].startswith("A*"):
            vec = ast.literal_eval(parts[1][2:])
            Av = ast.literal_eval(parts[2])
            lam, lv = parse_scalar_vector(parts[3])
            test.assertEqual(Av, matvec(A, vec))
            test.assertEqual(lv, [lam * value for value in vec])
        elif code == "DIAG_FORM":
            P = ast.literal_eval(parts[1].removeprefix("P = "))
            D = ast.literal_eval(parts[2].removeprefix("D = "))
            P_inv = ast.literal_eval(parts[3].removeprefix("P^-1 = "))
            test.assertEqual(D, [[lambdas[0], 0], [0, lambdas[1]]])
            test.assertEqual(matmul(P, P_inv), [[1, 0], [0, 1]])
            test.assertEqual(matmul(matmul(P, D), P_inv), A)
        elif code == "EXP_DIAG":
            test.assertEqual(parts[2], symbolic_matrix(expD))
        elif code == "EXP_ENTRY":
            i, j = ast.literal_eval(parts[1])
            test.assertEqual(parts[2], entries[i - 1][j - 1])
            test.assertEqual(parts[3], entries[i - 1][j - 1])
        elif code == "EXP_APPLY":
            test.assertEqual(parts[2], f"x(0) = {x0}")
        elif code == "SOL_ENTRY":
            i = int(parts[1][1]) - 1
            test.assertIn(f"({entries[i][0]})*", parts[2])
            test.assertIn(f"({entries[i][1]})*", parts[2])
            expect = combo_text([
                (matvec(C1, x0)[i], lambdas[0]),
                (matvec(C2, x0)[i], lambdas[1]),
            ])
            test.assertEqual(parts[3], expect)
        elif code == "CHECK" and parts[1] == "t = 0":
            got = ast.literal_eval(parts[2])
            if kind == "ivp":
                test.assertEqual(got, x0)
            else:
                test.assertEqual(got, value_at_zero(records))
    # e^(A*0) = I and d/dt e^(At) at 0 = A pin the coefficient matrices down.
    test.assertEqual(value_at_zero(records), [[1, 0], [0, 1]])
    test.assertEqual(derivative_at_zero(records), A)
    test.assertIn("EXP_FORM", seen)
    if kind == "ivp":
        test.assertIn("SOL_ENTRY", seen)


class TestMatrixExponentialGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MatrixExponentialGenerator()

    def test_output_contract(self):
        for _ in range(50):
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

    def test_step_arithmetic_and_symbolic_checks(self):
        for _ in range(400):
            result = self.gen.generate()
            check_step_arithmetic(self, result)

    def test_every_phrasing_and_variant_is_parsed(self):
        exp_seen, ivp_seen, ops = set(), set(), set()
        for _ in range(600):
            result = self.gen.generate()
            idx, kind, _, _ = parse_problem(result["problem"])
            ops.add(result["operation"])
            (exp_seen if kind == "exponential" else ivp_seen).add(idx)
        self.assertEqual(exp_seen, set(range(len(EXP_TEMPLATES))))
        self.assertEqual(ivp_seen, set(range(len(IVP_TEMPLATES))))
        self.assertEqual(
            ops,
            {"matrix_exponential_diagonalizable", "matrix_exponential_ivp"})

    def test_eigenvalues_distinct_and_matrix_nondiagonal(self):
        for _ in range(400):
            result = self.gen.generate()
            _, _, A, _ = parse_problem(result["problem"])
            lam1, lam2 = eigenvalues(A)
            self.assertNotEqual(lam1, lam2)
            self.assertNotEqual(0, lam1)
            self.assertNotEqual(0, lam2)
            self.assertFalse(A[0][1] == 0 and A[1][0] == 0)
            self.assertLessEqual(max(abs(v) for row in A for v in row), 48)

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<![\d)])1\*|\+ -|--|\^1(?![\dt])")
        for _ in range(400):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]), result["problem"])
            self.assertIsNone(bad.search(result["final_answer"]),
                              result["final_answer"])
            for raw_step in result["steps"]:
                self.assertIsNone(bad.search(raw_step), raw_step)

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, str(result["final_answer"]))
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)

    def test_deterministic_under_seed(self):
        random.seed(11)
        first = [self.gen.generate() for _ in range(20)]
        random.seed(11)
        second = [self.gen.generate() for _ in range(20)]
        self.assertEqual([e["problem"] for e in first],
                         [e["problem"] for e in second])
        self.assertEqual([e["steps"] for e in first],
                         [e["steps"] for e in second])


if __name__ == "__main__":
    unittest.main()

import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.diagonalization_generator import (
    columns_to_matrix,
    inverse_2x2,
    matmul,
    scalar_vector_text,
)
from generators.eigenvalue_generator import matvec, null_vector, subtract_lambda
from generators.matrix_ops_generator import mat


COLUMN_BOUND = 8
ENTRY_BOUND = 48
LAMBDAS = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
X0_BOUND = 6

EXP_PHRASINGS = [
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

IVP_PHRASINGS = [
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


def symbolic_vector(entries):
    return "[" + ", ".join(entries) + "]"


def signed(value):
    return f"({value})" if value < 0 else str(value)


def exp_entries(P, P_inv, lambdas):
    entries = []
    term_records = []
    for i in range(2):
        row = []
        record_row = []
        for j in range(2):
            terms = [
                (P[i][0] * P_inv[0][j], lambdas[0]),
                (P[i][1] * P_inv[1][j], lambdas[1]),
            ]
            row.append(combo_text(terms))
            record_row.append(terms)
        entries.append(row)
        term_records.append(record_row)
    return entries, term_records


def primitive_columns(bound):
    return [
        (p, q)
        for p in range(-bound, bound + 1)
        for q in range(-bound, bound + 1)
        if gcd(abs(p), abs(q)) == 1
    ]


def unimodular_matrices(bound):
    """Every integer 2x2 matrix with determinant +-1 and entries <= bound."""
    cols = primitive_columns(bound)
    return [
        [[p, r], [q, s]]
        for (p, q) in cols
        for (r, s) in cols
        if p * s - q * r in (1, -1)
    ]


UNIMODULAR = unimodular_matrices(COLUMN_BOUND)


def random_system():
    """Random integral A with two distinct integer eigenvalues.

    Built backward: A = P D P^-1 for a random unimodular P and a random pair
    of distinct integer eigenvalues, so A, its eigenvectors and P^-1 are all
    integral and the whole diagonalization stays hand-checkable.
    """
    while True:
        raw_p = random.choice(UNIMODULAR)
        lambdas = sorted(random.sample(LAMBDAS, 2))
        D = [[lambdas[0], 0], [0, lambdas[1]]]
        A = matmul(matmul(raw_p, D), inverse_2x2(raw_p))
        if A[0][1] == 0 and A[1][0] == 0:
            continue  # already diagonal: no work to do
        if max(abs(v) for row in A for v in row) > ENTRY_BOUND:
            continue
        return A, lambdas, D


class MatrixExponentialGenerator(ProblemGenerator):
    """
    Matrix exponential for diagonalizable 2x2 matrices:
    e^(At) = P*e^(Dt)*P^-1. Eigenvalues are distinct integers in [-6, 6] and
    P is unimodular, so every symbolic entry is an exact integer combination
    of e^(lambda t) terms. A second variant applies e^(At) to an integer
    initial vector to solve x' = Ax, x(0) = x0.

    Op-codes used:
    - MAT_SETUP (established): matrix and goal
    - EIGENVALUE / EIGENVECTOR (established): eigenpairs
    - CHECK (established): Av = lambda v, e^(A0) = I, x(0) recovered
    - DIAG_FORM (established): P, D, and P^-1
    - EXP_DIAG: e^(Dt)
    - EXP_FORM: e^(At) = P*e^(Dt)*P^-1
    - EXP_ENTRY: one symbolic entry of e^(At)
    - EXP_APPLY: form x(t) = e^(At)x(0)
    - SOL_ENTRY: one component of the solution vector x(t)
    - Z: e^(At) or x(t)
    """

    def generate(self) -> dict:
        A, lambdas, D = random_system()
        vectors = [null_vector(subtract_lambda(A, lam)) for lam in lambdas]
        P = columns_to_matrix(vectors)
        P_inv = inverse_2x2(P)
        entries, term_records = exp_entries(P, P_inv, lambdas)
        expD = [[exp_text(lambdas[0]), "0"], ["0", exp_text(lambdas[1])]]
        variant = random.choice(["exponential", "ivp"])

        if variant == "ivp":
            while True:
                x0 = [random.randint(-X0_BOUND, X0_BOUND) for _ in range(2)]
                if x0 != [0, 0]:
                    break
            phrasing = random.choice(IVP_PHRASINGS)
            problem = phrasing.format(matrix=mat(A), vector=str(x0))
            goal = f"solve x' = Ax with x(0) = {x0}"
            operation = "matrix_exponential_ivp"
        else:
            x0 = None
            phrasing = random.choice(EXP_PHRASINGS)
            problem = phrasing.format(matrix=mat(A))
            goal = "compute e^(At)"
            operation = "matrix_exponential_diagonalizable"

        steps = [step("MAT_SETUP", f"A = {mat(A)}", goal)]
        for lam, vec in zip(lambdas, vectors):
            Av = matvec(A, vec)
            lv = [lam * value for value in vec]
            steps.extend([
                step("EIGENVALUE", f"λ = {lam}", "diagonal entry of D"),
                step("EIGENVECTOR", f"λ = {lam}", str(vec)),
                step("CHECK", f"A*{vec}", str(Av),
                     scalar_vector_text(lam, lv)),
            ])
        steps.extend([
            step("DIAG_FORM", f"P = {mat(P)}", f"D = {mat(D)}",
                 f"P^-1 = {mat(P_inv)}"),
            step("EXP_DIAG", "e^(Dt)", symbolic_matrix(expD)),
            step("EXP_FORM", "e^(At) = P*e^(Dt)*P^-1"),
        ])
        for i in range(2):
            for j in range(2):
                raw_terms = combo_text(term_records[i][j])
                steps.append(step("EXP_ENTRY", f"({i + 1},{j + 1})",
                                  raw_terms, entries[i][j]))

        if variant == "ivp":
            steps.append(step("EXP_APPLY", "x(t) = e^(At)x(0)",
                              f"x(0) = {x0}"))
            components = []
            start = []
            for i in range(2):
                terms = [
                    (sum(P[i][0] * P_inv[0][j] * x0[j] for j in range(2)),
                     lambdas[0]),
                    (sum(P[i][1] * P_inv[1][j] * x0[j] for j in range(2)),
                     lambdas[1]),
                ]
                body = combo_text(terms)
                components.append(body)
                start.append(sum(coeff for coeff, _ in terms))
                work = (f"({entries[i][0]})*{signed(x0[0])} + "
                        f"({entries[i][1]})*{signed(x0[1])}")
                steps.append(step("SOL_ENTRY", f"x{i + 1}(t)", work, body))
            steps.append(step("CHECK", "t = 0", str(start),
                              f"matches x(0) = {x0}"))
            answer = f"x(t)={symbolic_vector(components)}"
        else:
            steps.append(step("CHECK", "t = 0", mat([[1, 0], [0, 1]]),
                              "identity"))
            answer = f"e^(At)={symbolic_matrix(entries)}"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

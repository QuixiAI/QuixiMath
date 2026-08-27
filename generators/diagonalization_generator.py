import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.eigenvalue_generator import (
    factored_text,
    matvec,
    null_vector,
    poly_coeffs_from_roots,
    poly_text,
    subtract_lambda,
)
from generators.matrix_ops_generator import mat


# Largest entry allowed in an eigenvector column of P.
VEC_BOUND = 12
# Largest absolute entry allowed in A itself (keeps the row reduction hand-
# friendly even though P may be wide).
ENTRY_CAP = 60
# Eigenvalues are drawn from +-1..EIG_BOUND (0 is excluded so A stays
# invertible and every factor (lambda - r) renders with a visible root).
EIG_BOUND = 9
# Largest absolute entry allowed in the reported A^k / A^k x, so the final
# products stay pencil-and-paper sized.
RESULT_CAP = 20000


def _primitive_vectors(bound):
    """Primitive integer 2-vectors, sign-normalised to a positive lead."""
    out = []
    for p in range(0, bound + 1):
        for q in range(-bound, bound + 1):
            if p == 0 and q <= 0:
                continue
            if gcd(abs(p), abs(q)) != 1:
                continue
            out.append((p, q))
    return out


def _unimodular_pairs(bound):
    """Ordered eigenvector pairs (v0, v1) whose matrix has determinant +-1."""
    vecs = _primitive_vectors(bound)
    pairs = []
    for p, q in vecs:
        for r, s in vecs:
            if (p, q) == (r, s):
                continue
            if abs(p * s - q * r) == 1:
                pairs.append(((p, q), (r, s)))
    return pairs


EIGENVECTOR_PAIRS = _unimodular_pairs(VEC_BOUND)


def fmt_num(n):
    return f"({n})" if n < 0 else str(n)


def product_expr(a, b):
    if a == 0 or b == 0:
        return "0"
    if a == 1:
        return fmt_num(b)
    if b == 1:
        return fmt_num(a)
    if a == -1:
        return fmt_num(-b)
    if b == -1:
        return fmt_num(-a)
    return f"{fmt_num(a)}*{fmt_num(b)}"


def product_sum_expr(*pairs):
    terms = [product_expr(a, b) for a, b in pairs if a * b != 0]
    if not terms:
        return "0"
    return " + ".join(terms)


def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B)))
         for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def inverse_2x2(A):
    a, b = A[0]
    c, d = A[1]
    det = a * d - b * c
    return [[d // det, -b // det], [-c // det, a // det]]


def matrix_power(A, k):
    result = [[1, 0], [0, 1]]
    for _ in range(k):
        result = matmul(result, A)
    return result


def columns_to_matrix(cols):
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


def scalar_vector_text(lam, lv):
    if lam == 1:
        return f"v = {lv}"
    if lam == -1:
        return f"-v = {lv}"
    return f"{lam}*v = {lv}"


def combo_text(c0, c1):
    """c0*v0 + c1*v1 with unit and zero coefficients rendered honestly."""
    pieces = []
    for coeff, name in ((c0, "v1"), (c1, "v2")):
        if coeff == 0:
            continue
        if coeff == 1:
            body = name
        elif coeff == -1:
            body = f"-{name}"
        else:
            body = f"{coeff}*{name}"
        if pieces and not body.startswith("-"):
            pieces.append(f"+ {body}")
        elif pieces:
            pieces.append(f"- {body[1:]}")
        else:
            pieces.append(body)
    return " ".join(pieces) if pieces else "0"


class DiagonalizationGenerator(ProblemGenerator):
    """
    Diagonalize a 2x2 matrix with two distinct integer eigenvalues.  The
    matrix is built backward from a unimodular eigenvector matrix P and an
    integer diagonal D, so P, D, and P^-1 are all integral and every
    displayed number is exact.

    Variants:
    - power (default): diagonalize and use A^k = P*D^k*P^-1
    - decompose: diagonalize only, reporting P, D, and P^-1
    - vector_power: expand a vector in the eigenbasis and push it k steps

    Op-codes used:
    - MAT_SETUP (established): matrix, exponent, and goal
    - CHAR_POLY (established): characteristic polynomial
    - EIGENVALUE / EIGENVECTOR (established): eigenpairs
    - CHECK (established): Av = lambda v and P*D*P^-1 = A
    - DIAG_FORM: P, D, and P^-1
    - E / D_POWER: diagonal power computation
    - POWER_FORM: A^k = P*D^k*P^-1
    - POWER_ENTRY: each entry of A^k from the matrix product
    - COORDS: eigenbasis coordinates of the given vector, c = P^-1 x
    - COMBO: x rewritten as a combination of the eigenvectors
    - SCALE_MODE: one eigen-component after k steps, lambda^k times c
    - VEC_ENTRY: each entry of A^k x from the scaled components
    - Z: the requested decomposition or power
    """

    VARIANTS = ["power", "decompose", "vector_power"]
    VARIANT_WEIGHTS = [0.30, 0.25, 0.45]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    # ------------------------------------------------------------- sampling

    @staticmethod
    def _sample_instance():
        """Random (A, lambdas, vectors) with hand-friendly entries."""
        while True:
            v0, v1 = random.choice(EIGENVECTOR_PAIRS)
            lam0, lam1 = sorted(random.sample(
                [v for v in range(-EIG_BOUND, EIG_BOUND + 1) if v != 0], 2))
            P = columns_to_matrix([list(v0), list(v1)])
            P_inv = inverse_2x2(P)
            D = [[lam0, 0], [0, lam1]]
            A = matmul(matmul(P, D), P_inv)
            if max(abs(v) for row in A for v in row) > ENTRY_CAP:
                continue
            return A, [lam0, lam1], [list(v0), list(v1)]

    @staticmethod
    def _sample_exponent(lambdas):
        top = max(abs(lam) for lam in lambdas)
        choices = [2, 3]
        if top <= 6:
            choices.append(4)
        if top <= 4:
            choices.append(5)
        return random.choice(choices)

    # ------------------------------------------------------------ phrasings

    @staticmethod
    def _phrase_power(A, k):
        idx = random.randrange(5)
        if idx == 0:
            return f"Diagonalize A = {mat(A)} and compute A^{k}."
        if idx == 1:
            return (f"Let A = {mat(A)}. Write A = P·D·P^-1 with D diagonal, "
                    f"then use that form to find A^{k}.")
        if idx == 2:
            return (f"Find an eigenvector matrix P and a diagonal matrix D "
                    f"with A = P·D·P^-1 for A = {mat(A)}, and evaluate "
                    f"A^{k}.")
        if idx == 3:
            return (f"Use diagonalization to raise A = {mat(A)} to the "
                    f"power {k}.")
        return (f"For A = {mat(A)}, give the diagonalization P, D, P^-1 "
                f"and the matrix A^{k}.")

    @staticmethod
    def _phrase_decompose(A):
        idx = random.randrange(5)
        if idx == 0:
            return f"Diagonalize A = {mat(A)}."
        if idx == 1:
            return (f"Let A = {mat(A)}. Find P, D, and P^-1 with "
                    f"A = P·D·P^-1 and D diagonal.")
        if idx == 2:
            return (f"Find the eigenvalues and eigenvectors of "
                    f"A = {mat(A)} and use them to write A = P·D·P^-1.")
        if idx == 3:
            return f"Write A = {mat(A)} in the form P·D·P^-1 with D diagonal."
        return f"Give an eigendecomposition A = P·D·P^-1 for A = {mat(A)}."

    @staticmethod
    def _phrase_vector(A, k, x):
        idx = random.randrange(5)
        vec = mat([x])[1:-1]
        if idx == 0:
            return (f"Let A = {mat(A)} and x = {vec}. Use the "
                    f"diagonalization of A to compute A^{k}x.")
        if idx == 1:
            return (f"Diagonalize A = {mat(A)}, expand x = {vec} in the "
                    f"eigenbasis, and find A^{k}x.")
        if idx == 2:
            return (f"For A = {mat(A)}, write x = {vec} as a combination of "
                    f"eigenvectors and compute A^{k}x.")
        if idx == 3:
            return (f"A state vector x = {vec} is advanced {k} steps by "
                    f"A = {mat(A)}. Using eigenvectors, find A^{k}x.")
        return (f"Given A = {mat(A)} and x = {vec}, use "
                f"A^{k} = P·D^{k}·P^-1 to evaluate A^{k}x.")

    # ------------------------------------------------------------ shared

    def _diagonalize_steps(self, A, lambdas, vectors, P, P_inv, D):
        coeffs = poly_coeffs_from_roots(lambdas)
        steps = [step("CHAR_POLY", f"p(λ) = {poly_text(coeffs)}",
                      factored_text(lambdas))]
        for lam, vec in zip(lambdas, vectors):
            Av = matvec(A, vec)
            lv = [lam * value for value in vec]
            steps.extend([
                step("EIGENVALUE", f"λ = {lam}", f"p({lam}) = 0"),
                step("EIGENVECTOR", f"λ = {lam}", str(vec)),
                step("CHECK", f"A*{vec}", str(Av),
                     scalar_vector_text(lam, lv)),
            ])
        steps.extend([
            step("DIAG_FORM", f"P = {mat(P)}", f"D = {mat(D)}",
                 f"P^-1 = {mat(P_inv)}"),
            step("CHECK", "P*D*P^-1", mat(A), "matches A"),
        ])
        return steps

    # ------------------------------------------------------------ generate

    def _draw(self, variant):
        """Rejection-sample an instance whose reported result stays small."""
        fallback = None
        for _ in range(400):
            A, lambdas, vectors = self._sample_instance()
            P = columns_to_matrix(vectors)
            P_inv = inverse_2x2(P)
            D = [[lambdas[0], 0], [0, lambdas[1]]]
            base = (A, lambdas, vectors, P, P_inv, D)
            if variant == "decompose":
                return base + (None, None, None)
            k = self._sample_exponent(lambdas)
            Dk = [[lambdas[0] ** k, 0], [0, lambdas[1] ** k]]
            if variant == "power":
                Ak = matmul(matmul(P, Dk), P_inv)
                size = max(abs(v) for row in Ak for v in row)
                candidate = base + (k, Dk, None)
            else:
                x = [0, 0]
                while x == [0, 0]:
                    x = [random.randint(-9, 9), random.randint(-9, 9)]
                c = matvec(P_inv, x)
                scaled = [c[0] * Dk[0][0], c[1] * Dk[1][1]]
                y = [scaled[0] * vectors[0][0] + scaled[1] * vectors[1][0],
                     scaled[0] * vectors[0][1] + scaled[1] * vectors[1][1]]
                size = max(abs(v) for v in y)
                candidate = base + (k, Dk, x)
            if size <= RESULT_CAP:
                return candidate
            if fallback is None:
                fallback = candidate
        return fallback

    def generate(self) -> dict:
        variant = self.variant
        if variant is None:
            variant = random.choices(self.VARIANTS,
                                     weights=self.VARIANT_WEIGHTS)[0]
        A, lambdas, vectors, P, P_inv, D, k, Dk, x = self._draw(variant)
        assert [null_vector(subtract_lambda(A, lam)) for lam in lambdas] \
            == vectors

        if variant == "decompose":
            problem = self._phrase_decompose(A)
            steps = [step("MAT_SETUP", f"A = {mat(A)}",
                          "diagonalize A = P*D*P^-1")]
            steps += self._diagonalize_steps(A, lambdas, vectors,
                                             P, P_inv, D)
            answer = f"P={mat(P)}, D={mat(D)}, P^-1={mat(P_inv)}"
            steps.append(step("Z", answer))
            return dict(
                problem_id=jid(),
                operation="diagonalization_decompose",
                problem=problem,
                steps=steps,
                final_answer=answer,
            )

        if variant == "vector_power":
            problem = self._phrase_vector(A, k, x)
            c = matvec(P_inv, x)
            scaled = [c[0] * Dk[0][0], c[1] * Dk[1][1]]
            y = [scaled[0] * vectors[0][0] + scaled[1] * vectors[1][0],
                 scaled[0] * vectors[0][1] + scaled[1] * vectors[1][1]]
            assert y == matvec(matrix_power(A, k), x)

            steps = [step("MAT_SETUP", f"A = {mat(A)}, x = {x}, k = {k}",
                          "compute A^k x by diagonalization")]
            steps += self._diagonalize_steps(A, lambdas, vectors,
                                             P, P_inv, D)
            steps.append(step("COORDS", "c = P^-1 x", str(c)))
            steps.append(step("COMBO", f"x = {combo_text(c[0], c[1])}",
                              str(x)))
            steps.append(step("CHECK", f"P*{c}", str(matvec(P, c)),
                              "matches x"))
            for index in range(2):
                steps.append(step("E", lambdas[index], k,
                                  Dk[index][index]))
                steps.append(step("SCALE_MODE", f"λ = {lambdas[index]}",
                                  product_expr(Dk[index][index], c[index]),
                                  scaled[index]))
            for row in range(2):
                expr = product_sum_expr(
                    (scaled[0], vectors[0][row]),
                    (scaled[1], vectors[1][row]),
                )
                steps.append(step("VEC_ENTRY", f"({row + 1})", expr, y[row]))
            steps.append(step("CHECK", f"direct A^{k}x",
                              str(matvec(matrix_power(A, k), x)),
                              "matches eigenbasis result"))
            answer = f"c={c}, A^{k}x={y}"
            steps.append(step("Z", answer))
            return dict(
                problem_id=jid(),
                operation="diagonalization_vector_power",
                problem=problem,
                steps=steps,
                final_answer=answer,
            )

        # variant == "power"
        B = matmul(P, Dk)
        Ak = matmul(B, P_inv)
        direct = matrix_power(A, k)
        assert direct == Ak
        problem = self._phrase_power(A, k)

        steps = [step("MAT_SETUP", f"A = {mat(A)}, k = {k}",
                      "diagonalize and compute A^k")]
        steps += self._diagonalize_steps(A, lambdas, vectors, P, P_inv, D)
        steps.extend([
            step("E", lambdas[0], k, Dk[0][0]),
            step("E", lambdas[1], k, Dk[1][1]),
            step("D_POWER", f"D^{k}", mat(Dk)),
            step("POWER_FORM", f"A^{k} = P*D^{k}*P^-1"),
        ])
        for i in range(2):
            for j in range(2):
                expr = product_sum_expr(
                    (B[i][0], P_inv[0][j]),
                    (B[i][1], P_inv[1][j]),
                )
                steps.append(step("POWER_ENTRY", f"({i + 1},{j + 1})",
                                  expr, Ak[i][j]))
        steps.append(step("CHECK", f"direct A^{k}", mat(direct),
                          "matches diagonalization"))

        answer = (f"P={mat(P)}, D={mat(D)}, P^-1={mat(P_inv)}, "
                  f"A^{k}={mat(Ak)}")
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="diagonalization_power",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

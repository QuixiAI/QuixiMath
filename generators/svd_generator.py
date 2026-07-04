import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


ROOT2 = "√2"
S = f"1/{ROOT2}"
VEC_PLUS = f"[{S}, {S}]"
VEC_MINUS = f"[{S}, -{S}]"
ORTHO_MATRIX = f"[[{S}, {S}], [{S}, -{S}]]"


def over_root2(n):
    if n == 1:
        return S
    if n == -1:
        return f"-{S}"
    if n < 0:
        return f"-{-n}/{ROOT2}"
    return f"{n}/{ROOT2}"


def scaled_vec(n, signs):
    return "[" + ", ".join(over_root2(n * sign) for sign in signs) + "]"


def ata_for(A):
    return [
        [sum(A[k][i] * A[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


class SVDGenerator(ProblemGenerator):
    """
    Singular value decomposition of symmetric 2x2 matrices via A^T A.
    Matrices have the form [[a, b], [b, a]], so A^T A has exact eigenvectors
    [1/sqrt(2), +/-1/sqrt(2)] and integer singular values.

    Op-codes used:
    - MAT_SETUP (established): matrix and goal
    - ATA: compute A^T A
    - EIGENVALUE / EIGENVECTOR (established): eigendata of A^T A
    - ROOT (established): singular values from eigenvalues
    - AV_VECTOR: A*v_i
    - U_VECTOR: u_i = A*v_i/sigma_i
    - CHECK (established): U*Sigma*V^T reconstructs A
    - Z: U, Sigma, and V^T
    """

    def generate(self) -> dict:
        a = random.randint(3, 30)
        b = random.randint(1, a - 1)
        A = [[a, b], [b, a]]
        ata = ata_for(A)
        sigma1 = a + b
        sigma2 = a - b
        lambda1 = sigma1 * sigma1
        lambda2 = sigma2 * sigma2
        Sigma = [[sigma1, 0], [0, sigma2]]

        steps = [
            step("MAT_SETUP", f"A = {mat(A)}", "SVD via A^T A"),
            step("ATA", "A^T A", mat(ata)),
            step("EIGENVALUE", f"λ1 = {lambda1}",
                 f"from ({a} + {b})^2"),
            step("EIGENVECTOR", f"λ1 = {lambda1}", VEC_PLUS),
            step("ROOT", f"√{lambda1}", sigma1),
            step("AV_VECTOR", "A*v1", scaled_vec(sigma1, [1, 1])),
            step("U_VECTOR", "u1 = A*v1/σ1", VEC_PLUS),
            step("EIGENVALUE", f"λ2 = {lambda2}",
                 f"from ({a} - {b})^2"),
            step("EIGENVECTOR", f"λ2 = {lambda2}", VEC_MINUS),
            step("ROOT", f"√{lambda2}", sigma2),
            step("AV_VECTOR", "A*v2", scaled_vec(sigma2, [1, -1])),
            step("U_VECTOR", "u2 = A*v2/σ2", VEC_MINUS),
            step("CHECK", "U*Sigma*V^T", mat(A), "matches A"),
        ]
        answer = (f"U={ORTHO_MATRIX}; Sigma={mat(Sigma)}; "
                  f"V^T={ORTHO_MATRIX}")
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="svd_symmetric_2x2",
            problem=(f"Find an SVD A = U*Sigma*V^T for A = {mat(A)} "
                     f"using A^T A."),
            steps=steps,
            final_answer=answer,
        )

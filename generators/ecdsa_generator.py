import random

from base_generator import ProblemGenerator
from helpers import step, jid


P, A, N = 17, 2, 19
G = (5, 1)


def inv_mod(value, modulus):
    return pow(value % modulus, -1, modulus)


def point_text(point):
    return "O" if point is None else f"({point[0]},{point[1]})"


def add(Pt, Qt):
    if Pt is None:
        return Qt
    if Qt is None:
        return Pt
    x1, y1 = Pt
    x2, y2 = Qt
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if Pt == Qt:
        lam = ((3 * x1 * x1 + A) * inv_mod(2 * y1, P)) % P
    else:
        lam = ((y2 - y1) * inv_mod(x2 - x1, P)) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return x3, y3


def scalar(k, point):
    acc = None
    for _ in range(k):
        acc = add(acc, point)
    return acc


class ECDSAGenerator(ProblemGenerator):
    """
    Toy ECDSA signing and verification on a small curve.

    Uses E: y^2=x^3+2x+2 over F_17, base point G=(5,1), and order n=19.

    Op-codes used:
    - ECDSA_SETUP / ECDSA_PUBLIC / ECDSA_NONCE / MOD_INVERSE
    - ECDSA_SIGN / ECDSA_VERIFY / EC_SCALAR / EC_ADD / CHECK
    - Z: signature and verification verdict
    """

    def generate(self) -> dict:
        d = random.randint(2, 9)
        z = random.randint(1, 9)
        k = random.randint(2, 17)
        Q = scalar(d, G)
        R = scalar(k, G)
        r = R[0] % N
        s = (inv_mod(k, N) * (z + r * d)) % N
        if r == 0 or s == 0:
            return self.generate()
        w = inv_mod(s, N)
        u1 = (z * w) % N
        u2 = (r * w) % N
        X = add(scalar(u1, G), scalar(u2, Q))
        verdict = "valid" if X is not None and X[0] % N == r else "invalid"
        steps = [
            step("ECDSA_SETUP", "E/F_17, G=(5,1), n=19",
                 f"d={d}", f"z={z}", f"k={k}"),
            step("ECDSA_PUBLIC", f"Q=dG={point_text(Q)}"),
            step("ECDSA_NONCE", f"kG={point_text(R)}", f"r={r}"),
            step("MOD_INVERSE", f"{k} mod 19", inv_mod(k, N)),
            step("ECDSA_SIGN", "s=k^-1(z+rd) mod n", f"s={s}"),
            step("MOD_INVERSE", f"{s} mod 19", w),
            step("ECDSA_VERIFY", f"u1={u1}", f"u2={u2}"),
            step("EC_SCALAR", f"u1G={point_text(scalar(u1, G))}",
                 f"u2Q={point_text(scalar(u2, Q))}"),
            step("EC_ADD", point_text(X)),
            step("CHECK", f"x(X) mod n = {X[0] % N}", f"r={r}", verdict),
        ]
        answer = f"signature = (r={r}, s={s}); verification = {verdict}"
        problem = (
            "On E: y^2=x^3+2x+2 over F_17 with G=(5,1) of order n=19, "
            f"private key d={d}, message hash z={z}, and nonce k={k}. "
            "Compute the ECDSA signature and verify it."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="ecdsa_sign_verify",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

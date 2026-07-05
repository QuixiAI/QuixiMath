import random

from base_generator import ProblemGenerator
from helpers import step, jid


P, A, B = 17, 2, 2
G = (5, 1)


def inv_mod(value, modulus=P):
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
        lam = ((3 * x1 * x1 + A) * inv_mod(2 * y1)) % P
    else:
        lam = ((y2 - y1) * inv_mod(x2 - x1)) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return x3, y3


def scalar(k, point):
    acc = None
    for _ in range(k):
        acc = add(acc, point)
    return acc


class ECDHGenerator(ProblemGenerator):
    """
    Toy elliptic-curve Diffie-Hellman over F_17.

    Op-codes used:
    - ECDH_SETUP / EC_SCALAR / EC_PUBLIC / EC_SHARED / CHECK
    - Z: public keys and shared secret
    """

    def generate(self) -> dict:
        alice = random.randint(2, 9)
        bob = random.randint(2, 9)
        A_pub = scalar(alice, G)
        B_pub = scalar(bob, G)
        shared_a = scalar(alice, B_pub)
        shared_b = scalar(bob, A_pub)
        steps = [
            step("ECDH_SETUP", "E:y^2=x^3+2x+2 over F_17",
                 f"G={point_text(G)}"),
            step("EC_SCALAR", f"a={alice}", f"aG={point_text(A_pub)}"),
            step("EC_SCALAR", f"b={bob}", f"bG={point_text(B_pub)}"),
            step("EC_PUBLIC", f"A={point_text(A_pub)}",
                 f"B={point_text(B_pub)}"),
            step("EC_SHARED", f"aB={point_text(shared_a)}",
                 f"bA={point_text(shared_b)}"),
            step("CHECK", point_text(shared_a), point_text(shared_b)),
        ]
        answer = (
            f"A={point_text(A_pub)}; B={point_text(B_pub)}; "
            f"shared={point_text(shared_a)}"
        )
        problem = (
            "On E: y^2=x^3+2x+2 over F_17 with base point G=(5,1), "
            f"Alice secret a={alice} and Bob secret b={bob}. Compute both "
            "public keys and the shared ECDH point."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="ecdh_key_exchange",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

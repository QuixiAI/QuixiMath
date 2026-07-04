import random

from base_generator import ProblemGenerator
from helpers import step, jid


def vector_text(vector):
    return "(" + ",".join(str(value) for value in vector) + ")"


class FeatureMapGenerator(ProblemGenerator):
    """
    Verify a polynomial kernel by expanding an explicit feature-map dot product.

    Uses the exact one-dimensional degree-2 map:
      phi(t) = (t^2, 2t, 2)
      phi(x) dot phi(z) = x^2 z^2 + 4xz + 4 = (xz + 2)^2

    Op-codes used:
    - FEATURE_MAP_SETUP / FEATURE_VECTOR / DOT / KERNEL_BASE / KERNEL_VALUE
    - CHECK (established): equality of expanded feature dot and kernel value
    - M / A / E (established/shared): feature coordinates and kernel arithmetic
    - Z: both feature vectors, dot product, kernel value, verification flag
    """

    def generate(self) -> dict:
        x = random.randint(-20, 20)
        z = random.choice([value for value in range(-20, 21)
                           if value != x])
        phi_x = (x ** 2, 2 * x, 2)
        phi_z = (z ** 2, 2 * z, 2)
        term1 = phi_x[0] * phi_z[0]
        term2 = phi_x[1] * phi_z[1]
        term3 = phi_x[2] * phi_z[2]
        partial = term1 + term2
        dot_value = partial + term3
        xz = x * z
        base = xz + 2
        kernel_value = base ** 2

        steps = [
            step("FEATURE_MAP_SETUP", "K(x,z)=(xz+2)^2",
                 "phi(t)=(t^2,2t,2)", f"x={x},z={z}"),
            step("E", x, 2, phi_x[0]),
            step("M", 2, x, phi_x[1]),
            step("FEATURE_VECTOR", "phi(x)", vector_text(phi_x)),
            step("E", z, 2, phi_z[0]),
            step("M", 2, z, phi_z[1]),
            step("FEATURE_VECTOR", "phi(z)", vector_text(phi_z)),
            step("M", phi_x[0], phi_z[0], term1),
            step("M", phi_x[1], phi_z[1], term2),
            step("M", phi_x[2], phi_z[2], term3),
            step("A", term1, term2, partial),
            step("A", partial, term3, dot_value),
            step("DOT", "phi(x),phi(z)", dot_value),
            step("M", x, z, xz),
            step("A", xz, 2, base),
            step("KERNEL_BASE", "x,z", f"xz+2={xz}+2", base),
            step("E", base, 2, kernel_value),
            step("KERNEL_VALUE", "x,z", kernel_value),
            step("CHECK", "feature dot equals kernel",
                 f"{dot_value}={kernel_value}", "verified=true"),
        ]
        answer = (
            f"phi_x={vector_text(phi_x)}; phi_z={vector_text(phi_z)}; "
            f"dot={dot_value}; K={kernel_value}; verified=true"
        )
        steps.append(step("Z", answer))
        problem = (
            "For the polynomial kernel K(x,z)=(xz + 2)^2 with feature map "
            f"phi(t)=(t^2, 2t, 2), verify K(x,z) for x={x} and z={z} "
            "by expanding phi(x) dot phi(z)."
        )
        return dict(
            problem_id=jid(),
            operation="feature_map_polynomial_verify",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

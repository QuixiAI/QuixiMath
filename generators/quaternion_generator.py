import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def number_text(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return str(value)


def quat_text(q):
    return "(" + ",".join(number_text(value) for value in q) + ")"


def vector_text(v):
    return "(" + ",".join(str(value) for value in v) + ")"


def conjugate(q):
    a, b, c, d = q
    return (a, -b, -c, -d)


def norm_squared(q):
    return sum(value * value for value in q)


def multiply(q, r):
    a, b, c, d = q
    e, f, g, h = r
    return (
        a * e - b * f - c * g - d * h,
        a * f + b * e + c * h - d * g,
        a * g - b * h + c * e + d * f,
        a * h + b * g - c * f + d * e,
    )


def inverse(q):
    n = norm_squared(q)
    return tuple(Fraction(value, n) for value in conjugate(q))


def random_quaternion():
    while True:
        q = tuple(random.randint(-3, 3) for _ in range(4))
        if q != (0, 0, 0, 0):
            return q


class QuaternionGenerator(ProblemGenerator):
    """
    Quaternion multiplication, conjugates, norms, inverses, and rotations.

    Variants:
    - arithmetic: multiply p*q and q*p, then compute conjugate/norm/inverse
    - rotation: rotate a pure vector by q*v*q^-1 for a unit basis quaternion

    Op-codes used:
    - QUAT_SETUP / HAMILTON: operands and Hamilton multiplication facts
    - QUAT_MUL_START / QUAT_COMPONENT / QUAT_RESULT: multiplication trace
    - CONJUGATE / NORM_SQUARED / QUAT_INVERSE / ROTATED_VECTOR: summaries
    - M / A / S / F (established/shared): exact coefficient arithmetic
    - CHECK: noncommutativity or unit norm verification
    - Z: final quaternion result
    """

    VARIANTS = ["arithmetic", "rotation"]

    COMPONENTS = ["real", "i", "j", "k"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "arithmetic":
            problem, steps, answer = self._generate_arithmetic()
        else:
            problem, steps, answer = self._generate_rotation()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"quaternion_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _hamilton_steps(self):
        return [
            step("HAMILTON", "i*i", "-1"),
            step("HAMILTON", "j*j", "-1"),
            step("HAMILTON", "k*k", "-1"),
            step("HAMILTON", "i*j", "k"),
            step("HAMILTON", "j*i", "-k"),
        ]

    def _generate_arithmetic(self):
        while True:
            p = random_quaternion()
            q = random_quaternion()
            pq = multiply(p, q)
            qp = multiply(q, p)
            if pq != qp:
                break
        steps = [
            step("QUAT_SETUP", f"p={quat_text(p)}", f"q={quat_text(q)}"),
        ]
        steps.extend(self._hamilton_steps())
        self._trace_multiply(steps, "p", p, "q", q, "p*q")
        self._trace_multiply(steps, "q", q, "p", p, "q*p")
        p_conj = conjugate(p)
        p_norm = self._trace_norm(steps, "p", p)
        p_inv = self._trace_inverse(steps, "p", p_conj, p_norm)
        steps.append(step("CHECK", "p*q differs from q*p", "yes"))
        answer = (
            f"p*q = {quat_text(pq)}; q*p = {quat_text(qp)}; "
            f"conjugate(p) = {quat_text(p_conj)}; "
            f"norm^2(p) = {p_norm}; p^-1 = {quat_text(p_inv)}"
        )
        problem = (
            f"Let p={quat_text(p)} and q={quat_text(q)} represent "
            "coefficients of 1,i,j,k. With i^2=j^2=k^2=ijk=-1, "
            "compute p*q, q*p, conjugate(p), norm^2(p), and p^-1."
        )
        return problem, steps, answer

    def _generate_rotation(self):
        q = random.choice([
            (0, 1, 0, 0),
            (0, -1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, -1, 0),
            (0, 0, 0, 1),
            (0, 0, 0, -1),
        ])
        while True:
            vector = tuple(random.randint(-4, 4) for _ in range(3))
            if vector != (0, 0, 0):
                break
        v = (0,) + vector
        q_conj = conjugate(q)
        q_norm = norm_squared(q)
        q_inv = inverse(q)
        first = multiply(q, v)
        rotated = multiply(first, q_inv)
        rotated_int = tuple(int(value) for value in rotated)
        steps = [
            step("QUAT_SETUP", f"q={quat_text(q)}", f"v={quat_text(v)}"),
        ]
        steps.extend(self._hamilton_steps())
        traced_norm = self._trace_norm(steps, "q", q)
        steps.append(step("CHECK", "unit norm", "yes" if traced_norm == 1
                          else "no"))
        steps.append(step("CONJUGATE", "q", quat_text(q_conj)))
        for value in q_conj:
            steps.append(step("F", value, q_norm,
                              number_text(Fraction(value, q_norm))))
        steps.append(step("QUAT_INVERSE", "q", quat_text(q_inv)))
        self._trace_multiply(steps, "q", q, "v", v, "q*v")
        self._trace_multiply(steps, "q*v", first, "q^-1", q_inv,
                             "q*v*q^-1")
        steps.append(step("ROTATED_VECTOR", vector_text(rotated_int[1:])))
        answer = (
            f"qvq^-1 = {quat_text(rotated_int)}; "
            f"vector = {vector_text(rotated_int[1:])}"
        )
        problem = (
            f"Let q={quat_text(q)} and v={quat_text(v)} represent a unit "
            "quaternion and a pure-vector quaternion. Rotate v by q*v*q^-1."
        )
        return problem, steps, answer

    def _trace_multiply(self, steps, left_name, left, right_name, right,
                        result_name):
        steps.append(step("QUAT_MUL_START", result_name, left_name,
                          right_name))
        a, b, c, d = left
        e, f, g, h = right
        terms = [
            [(1, a, e), (-1, b, f), (-1, c, g), (-1, d, h)],
            [(1, a, f), (1, b, e), (1, c, h), (-1, d, g)],
            [(1, a, g), (-1, b, h), (1, c, e), (1, d, f)],
            [(1, a, h), (1, b, g), (-1, c, f), (1, d, e)],
        ]
        result = []
        for component, component_terms in zip(self.COMPONENTS, terms):
            running = 0
            for sign, left_value, right_value in component_terms:
                product = left_value * right_value
                steps.append(step("M", left_value, right_value, product))
                signed = product
                if sign < 0:
                    signed = -product
                    steps.append(step("S", 0, product, signed))
                total = running + signed
                steps.append(step("A", running, signed, total))
                running = total
            steps.append(step("QUAT_COMPONENT", result_name, component,
                              running))
            result.append(running)
        steps.append(step("QUAT_RESULT", result_name, quat_text(result)))
        return tuple(result)

    def _trace_norm(self, steps, name, q):
        running = 0
        for value in q:
            square = value * value
            steps.append(step("M", value, value, square))
            total = running + square
            steps.append(step("A", running, square, total))
            running = total
        steps.append(step("NORM_SQUARED", name, running))
        return running

    def _trace_inverse(self, steps, name, q_conj, q_norm):
        steps.append(step("CONJUGATE", name, quat_text(q_conj)))
        fractions = []
        for value in q_conj:
            fraction = Fraction(value, q_norm)
            steps.append(step("F", value, q_norm, number_text(fraction)))
            fractions.append(fraction)
        steps.append(step("QUAT_INVERSE", name, quat_text(fractions)))
        return tuple(fractions)

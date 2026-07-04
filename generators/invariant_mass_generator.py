import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


MASS_TRIPLES = [
    (8, 15, 17),
    (9, 12, 15),
    (12, 5, 13),
    (15, 8, 17),
    (16, 12, 20),
    (20, 21, 29),
    (21, 20, 29),
]
CM_TRIPLES = [
    (12, 5, 13),
    (15, 8, 17),
    (16, 12, 20),
    (20, 21, 29),
    (21, 20, 29),
]
TWO_BODY_CASES = [
    (10, 3),
    (17, 4),
    (20, 6),
    (26, 5),
    (29, 10),
    (30, 9),
    (34, 8),
    (50, 7),
]


def fraction_text(value):
    return str(Fraction(value))


class InvariantMassGenerator(ProblemGenerator):
    """
    Relativistic kinematics with exact invariant quantities.

    Variants cover invariant mass, center-of-mass energy, threshold beam
    energy, and two-body decay momentum. Root cases are chosen from
    Pythagorean data so every answer is exact.

    Op-codes used:
    - KIN_SETUP: givens and target
    - KIN_FORMULA: relativistic formula being applied
    - A / S / M / D / E / ROOT (established/shared): exact arithmetic
    - Z: requested kinematic quantity
    """

    VARIANTS = ["invariant_mass", "cm_energy", "threshold",
                "two_body_momentum"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "invariant_mass":
            problem, steps, answer = self._generate_invariant_mass()
        elif variant == "cm_energy":
            problem, steps, answer = self._generate_cm_energy()
        elif variant == "threshold":
            problem, steps, answer = self._generate_threshold()
        else:
            problem, steps, answer = self._generate_two_body_momentum()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"invariant_mass_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _split_same_direction(self, total_e, total_p):
        p1 = random.randint(0, total_p)
        p2 = total_p - p1
        e1 = random.randint(p1 + 1, total_e - p2 - 1)
        e2 = total_e - e1
        return e1, p1, e2, p2

    def _split_incoming(self, total_e, total_p):
        q_min = total_p + 1
        q_max = (total_e + total_p - 2) // 2
        p1 = random.randint(q_min, q_max)
        p2 = total_p - p1
        e1 = random.randint(p1 + 1, total_e - abs(p2) - 1)
        e2 = total_e - e1
        return e1, p1, e2, p2

    def _mass_from_total(self, e1, p1, e2, p2):
        total_e = e1 + e2
        total_p = p1 + p2
        e_sq = total_e ** 2
        p_sq = total_p ** 2
        mass_sq = e_sq - p_sq
        mass = int(mass_sq ** 0.5)
        return total_e, total_p, e_sq, p_sq, mass_sq, mass

    def _generate_invariant_mass(self):
        mass, total_p, total_e = random.choice(MASS_TRIPLES)
        e1, p1, e2, p2 = self._split_same_direction(total_e, total_p)
        total_e, total_p, e_sq, p_sq, mass_sq, mass = self._mass_from_total(
            e1, p1, e2, p2
        )
        steps = [
            step("KIN_SETUP", "invariant_mass",
                 f"(E1,p1)=({e1},{p1})", f"(E2,p2)=({e2},{p2})", "M"),
            step("KIN_FORMULA", "M=sqrt((E1+E2)^2-(p1+p2)^2)"),
            step("A", e1, e2, total_e),
            step("A", p1, p2, total_p),
            step("E", total_e, 2, e_sq),
            step("E", total_p, 2, p_sq),
            step("S", e_sq, p_sq, mass_sq),
            step("ROOT", f"sqrt({mass_sq})", mass),
        ]
        answer = f"M = {mass}"
        problem = (
            f"Two decay products in one dimension have (E,p)=({e1},{p1}) "
            f"and (E,p)=({e2},{p2}). Compute the invariant mass "
            "M=sqrt((E1+E2)^2-(p1+p2)^2)."
        )
        return problem, steps, answer

    def _generate_cm_energy(self):
        cm_energy, total_p, total_e = random.choice(CM_TRIPLES)
        e1, p1, e2, p2 = self._split_incoming(total_e, total_p)
        total_e, total_p, e_sq, p_sq, s_value, cm_energy = (
            self._mass_from_total(e1, p1, e2, p2)
        )
        steps = [
            step("KIN_SETUP", "cm_energy",
                 f"(E1,p1)=({e1},{p1})", f"(E2,p2)=({e2},{p2})",
                 "sqrt(s)"),
            step("KIN_FORMULA", "sqrt(s)=sqrt((E1+E2)^2-(p1+p2)^2)"),
            step("A", e1, e2, total_e),
            step("A", p1, p2, total_p),
            step("E", total_e, 2, e_sq),
            step("E", total_p, 2, p_sq),
            step("S", e_sq, p_sq, s_value),
            step("ROOT", f"sqrt({s_value})", cm_energy),
        ]
        answer = f"sqrt(s) = {cm_energy}"
        problem = (
            f"Two incoming particles in one dimension have (E,p)=({e1},{p1}) "
            f"and (E,p)=({e2},{p2}). Compute the center-of-mass energy "
            "sqrt(s)=sqrt((E1+E2)^2-(p1+p2)^2)."
        )
        return problem, steps, answer

    def _generate_threshold(self):
        m_a = random.randint(1, 8)
        m_b = random.randint(1, 8)
        final_mass = m_a + m_b + random.randint(1, 12)
        final_sq = final_mass ** 2
        m_a_sq = m_a ** 2
        m_b_sq = m_b ** 2
        after_a = final_sq - m_a_sq
        numerator = after_a - m_b_sq
        denominator = 2 * m_b
        threshold = Fraction(numerator, denominator)
        steps = [
            step("KIN_SETUP", "threshold",
                 f"m_a={m_a},m_b={m_b}", f"M_f={final_mass}", "E_thr"),
            step("KIN_FORMULA", "E_thr=(M_f^2-m_a^2-m_b^2)/(2*m_b)"),
            step("E", final_mass, 2, final_sq),
            step("E", m_a, 2, m_a_sq),
            step("E", m_b, 2, m_b_sq),
            step("S", final_sq, m_a_sq, after_a),
            step("S", after_a, m_b_sq, numerator),
            step("M", 2, m_b, denominator),
            step("D", numerator, denominator, fraction_text(threshold)),
        ]
        answer = f"E_thr = {fraction_text(threshold)}"
        problem = (
            f"A beam particle of mass m_a={m_a} hits a stationary target "
            f"of mass m_b={m_b}. The final particles have total rest mass "
            f"M_f={final_mass}. Compute "
            "E_thr=(M_f^2-m_a^2-m_b^2)/(2*m_b)."
        )
        return problem, steps, answer

    def _generate_two_body_momentum(self):
        parent, daughter = random.choice(TWO_BODY_CASES)
        m1 = daughter
        m2 = daughter
        mass_sum = m1 + m2
        mass_diff = m1 - m2
        parent_sq = parent ** 2
        sum_sq = mass_sum ** 2
        diff_sq = mass_diff ** 2
        left = parent_sq - sum_sq
        right = parent_sq - diff_sq
        radicand = left * right
        root = int(radicand ** 0.5)
        denominator = 2 * parent
        momentum = Fraction(root, denominator)
        steps = [
            step("KIN_SETUP", "two_body_momentum",
                 f"M={parent}", f"m1={m1},m2={m2}", "p"),
            step("KIN_FORMULA",
                 "p=sqrt((M^2-(m1+m2)^2)*(M^2-(m1-m2)^2))/(2*M)"),
            step("A", m1, m2, mass_sum),
            step("S", m1, m2, mass_diff),
            step("E", parent, 2, parent_sq),
            step("E", mass_sum, 2, sum_sq),
            step("E", mass_diff, 2, diff_sq),
            step("S", parent_sq, sum_sq, left),
            step("S", parent_sq, diff_sq, right),
            step("M", left, right, radicand),
            step("ROOT", f"sqrt({radicand})", root),
            step("M", 2, parent, denominator),
            step("D", root, denominator, fraction_text(momentum)),
        ]
        answer = f"p = {fraction_text(momentum)}"
        problem = (
            f"A parent of mass M={parent} decays into two equal daughters "
            f"m1=m2={daughter}. Compute the two-body momentum "
            "p=sqrt((M^2-(m1+m2)^2)*(M^2-(m1-m2)^2))/(2*M)."
        )
        return problem, steps, answer

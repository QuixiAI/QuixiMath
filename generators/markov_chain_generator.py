import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def random_probability():
    den = random.randint(3, 14)
    num = random.randint(1, den - 1)
    return Fraction(num, den)


def random_absorbing_row():
    den = random.randint(5, 16)
    counts = [0, 0, 1, 1]
    for _ in range(den - 2):
        counts[random.randrange(4)] += 1
    return tuple(Fraction(count, den) for count in counts)


def solve_two_by_two(a, b, c, d, r0, r1):
    det = a * d - b * c
    x0_num = r0 * d - b * r1
    x1_num = a * r1 - r0 * c
    return det, x0_num, x1_num, x0_num / det, x1_num / det


class MarkovChainGenerator(ProblemGenerator):
    """
    Markov chain transition, steady-state, and absorbing-chain calculations.

    Variants:
    - n_step: a two-step transition probability in a two-state chain
    - steady_state: stationary distribution for a two-state chain
    - absorbing: absorption probabilities and expected hitting times

    Op-codes used:
    - MARKOV_SETUP: transition matrix or absorbing-chain rows
    - MATRIX_ENTRY: target matrix product entry
    - STEADY_EQUATION: stationary balance equations
    - ABSORB_EQ / HIT_EQ: linear systems for absorption and hitting time
    - LINEAR_SYSTEM: coefficient matrix summary
    - A / S / M / D (established/shared): exact arithmetic
    - CHECK: stochastic or balance verification
    - Z: requested probability, stationary distribution, or absorbing result
    """

    VARIANTS = ["n_step", "steady_state", "absorbing"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "n_step":
            problem, steps, answer = self._generate_n_step()
        elif variant == "steady_state":
            problem, steps, answer = self._generate_steady_state()
        else:
            problem, steps, answer = self._generate_absorbing()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"markov_chain_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_n_step(self):
        p01 = random_probability()
        p00 = 1 - p01
        p10 = random_probability()
        p11 = 1 - p10
        term0 = p00 * p01
        term1 = p01 * p11
        prob = term0 + term1
        steps = [
            step("MARKOV_SETUP", "two_state",
                 f"P00={fraction_text(p00)}, P01={fraction_text(p01)}",
                 f"P10={fraction_text(p10)}, P11={fraction_text(p11)}"),
            step("MATRIX_ENTRY", "P2_01=P00*P01 + P01*P11"),
            step("M", fraction_text(p00), fraction_text(p01),
                 fraction_text(term0)),
            step("M", fraction_text(p01), fraction_text(p11),
                 fraction_text(term1)),
            step("A", fraction_text(term0), fraction_text(term1),
                 fraction_text(prob)),
        ]
        answer = f"P(X2=1 given X0=0)={fraction_text(prob)}"
        problem = (
            "For a two-state Markov chain with "
            f"P00={fraction_text(p00)}, P01={fraction_text(p01)}, "
            f"P10={fraction_text(p10)}, P11={fraction_text(p11)}, compute "
            "the two-step probability P(X2=1 given X0=0)."
        )
        return problem, steps, answer

    def _generate_steady_state(self):
        p01 = random_probability()
        p10 = random_probability()
        p00 = 1 - p01
        p11 = 1 - p10
        denom = p01 + p10
        pi0 = p10 / denom
        pi1 = p01 / denom
        flow01 = pi0 * p01
        flow10 = pi1 * p10
        steps = [
            step("MARKOV_SETUP", "two_state",
                 f"P00={fraction_text(p00)}, P01={fraction_text(p01)}",
                 f"P10={fraction_text(p10)}, P11={fraction_text(p11)}"),
            step("STEADY_EQUATION", "pi0*pi01=pi1*pi10",
                 "pi0+pi1=1"),
            step("A", fraction_text(p01), fraction_text(p10),
                 fraction_text(denom)),
            step("D", fraction_text(p10), fraction_text(denom),
                 fraction_text(pi0)),
            step("D", fraction_text(p01), fraction_text(denom),
                 fraction_text(pi1)),
            step("M", fraction_text(pi0), fraction_text(p01),
                 fraction_text(flow01)),
            step("M", fraction_text(pi1), fraction_text(p10),
                 fraction_text(flow10)),
            step("CHECK", f"flow01={fraction_text(flow01)}",
                 f"flow10={fraction_text(flow10)}"),
        ]
        answer = f"pi0={fraction_text(pi0)}, pi1={fraction_text(pi1)}"
        problem = (
            "For a two-state Markov chain with "
            f"P01={fraction_text(p01)} and P10={fraction_text(p10)}, "
            "find the steady-state distribution."
        )
        return problem, steps, answer

    def _generate_absorbing(self):
        p00, p01, p0a, p0b = random_absorbing_row()
        p10, p11, p1a, p1b = random_absorbing_row()
        a = 1 - p00
        b = -p01
        c = -p10
        d = 1 - p11
        det, u0_num, u1_num, u0, u1 = solve_two_by_two(
            a, b, c, d, p0a, p1a
        )
        _, t0_num, t1_num, t0, t1 = solve_two_by_two(
            a, b, c, d, Fraction(1), Fraction(1)
        )
        steps = [
            step("MARKOV_SETUP", "absorbing",
                 (f"row0 to0={fraction_text(p00)}, to1={fraction_text(p01)}, "
                  f"toA={fraction_text(p0a)}, toB={fraction_text(p0b)}"),
                 (f"row1 to0={fraction_text(p10)}, to1={fraction_text(p11)}, "
                  f"toA={fraction_text(p1a)}, toB={fraction_text(p1b)}")),
            step("ABSORB_EQ", "u0=p0A+p00*u0+p01*u1",
                 "u1=p1A+p10*u0+p11*u1"),
            step("S", 1, fraction_text(p00), fraction_text(a)),
            step("S", 0, fraction_text(p01), fraction_text(b)),
            step("S", 0, fraction_text(p10), fraction_text(c)),
            step("S", 1, fraction_text(p11), fraction_text(d)),
            step("LINEAR_SYSTEM", f"a={fraction_text(a)}, b={fraction_text(b)}",
                 f"c={fraction_text(c)}, d={fraction_text(d)}"),
            step("M", fraction_text(a), fraction_text(d), fraction_text(a * d)),
            step("M", fraction_text(b), fraction_text(c), fraction_text(b * c)),
            step("S", fraction_text(a * d), fraction_text(b * c),
                 fraction_text(det)),
            step("M", fraction_text(p0a), fraction_text(d),
                 fraction_text(p0a * d)),
            step("M", fraction_text(b), fraction_text(p1a),
                 fraction_text(b * p1a)),
            step("S", fraction_text(p0a * d), fraction_text(b * p1a),
                 fraction_text(u0_num)),
            step("D", fraction_text(u0_num), fraction_text(det),
                 fraction_text(u0)),
            step("M", fraction_text(a), fraction_text(p1a),
                 fraction_text(a * p1a)),
            step("M", fraction_text(p0a), fraction_text(c),
                 fraction_text(p0a * c)),
            step("S", fraction_text(a * p1a), fraction_text(p0a * c),
                 fraction_text(u1_num)),
            step("D", fraction_text(u1_num), fraction_text(det),
                 fraction_text(u1)),
            step("HIT_EQ", "t0=1+p00*t0+p01*t1",
                 "t1=1+p10*t0+p11*t1"),
            step("S", fraction_text(d), fraction_text(b),
                 fraction_text(t0_num)),
            step("D", fraction_text(t0_num), fraction_text(det),
                 fraction_text(t0)),
            step("S", fraction_text(a), fraction_text(c),
                 fraction_text(t1_num)),
            step("D", fraction_text(t1_num), fraction_text(det),
                 fraction_text(t1)),
        ]
        answer = (
            f"P(absorb A from 0)={fraction_text(u0)}, "
            f"P(absorb A from 1)={fraction_text(u1)}; "
            f"E[T from 0]={fraction_text(t0)}, "
            f"E[T from 1]={fraction_text(t1)}"
        )
        problem = (
            "For an absorbing Markov chain with transient transitions "
            f"from 0: to0={fraction_text(p00)}, to1={fraction_text(p01)}, "
            f"toA={fraction_text(p0a)}, toB={fraction_text(p0b)}; "
            f"from 1: to0={fraction_text(p10)}, to1={fraction_text(p11)}, "
            f"toA={fraction_text(p1a)}, toB={fraction_text(p1b)}, compute "
            "the absorption probabilities into A and expected hitting times."
        )
        return problem, steps, answer

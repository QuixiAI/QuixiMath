import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.markov_chain_generator import MarkovChainGenerator, solve_two_by_two
from helpers import DELIM


NSTEP_RE = re.compile(
    r"For a two-state Markov chain with P00=([^,]+), P01=([^,]+), "
    r"P10=([^,]+), P11=([^,]+), compute the two-step probability "
    r"P\(X2=1 given X0=0\)\."
)
STEADY_RE = re.compile(
    r"For a two-state Markov chain with P01=([^ ]+) and P10=([^,]+), "
    r"find the steady-state distribution\."
)
ABS_RE = re.compile(
    r"For an absorbing Markov chain with transient transitions from 0: "
    r"to0=([^,]+), to1=([^,]+), toA=([^,]+), toB=([^;]+); from 1: "
    r"to0=([^,]+), to1=([^,]+), toA=([^,]+), toB=([^,]+), compute "
    r"the absorption probabilities into A and expected hitting times\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_nstep(problem):
    p00, p01, p10, p11 = (
        Fraction(value) for value in NSTEP_RE.fullmatch(problem).groups()
    )
    term0 = p00 * p01
    term1 = p01 * p11
    prob = term0 + term1
    steps = [
        make_step("MARKOV_SETUP", "two_state",
                  f"P00={fraction_text(p00)}, P01={fraction_text(p01)}",
                  f"P10={fraction_text(p10)}, P11={fraction_text(p11)}"),
        make_step("MATRIX_ENTRY", "P2_01=P00*P01 + P01*P11"),
        make_step("M", fraction_text(p00), fraction_text(p01),
                  fraction_text(term0)),
        make_step("M", fraction_text(p01), fraction_text(p11),
                  fraction_text(term1)),
        make_step("A", fraction_text(term0), fraction_text(term1),
                  fraction_text(prob)),
    ]
    answer = f"P(X2=1 given X0=0)={fraction_text(prob)}"
    return steps, answer


def expected_steady(problem):
    p01, p10 = (Fraction(value)
                for value in STEADY_RE.fullmatch(problem).groups())
    p00 = 1 - p01
    p11 = 1 - p10
    denom = p01 + p10
    pi0 = p10 / denom
    pi1 = p01 / denom
    flow01 = pi0 * p01
    flow10 = pi1 * p10
    steps = [
        make_step("MARKOV_SETUP", "two_state",
                  f"P00={fraction_text(p00)}, P01={fraction_text(p01)}",
                  f"P10={fraction_text(p10)}, P11={fraction_text(p11)}"),
        make_step("STEADY_EQUATION", "pi0*pi01=pi1*pi10",
                  "pi0+pi1=1"),
        make_step("A", fraction_text(p01), fraction_text(p10),
                  fraction_text(denom)),
        make_step("D", fraction_text(p10), fraction_text(denom),
                  fraction_text(pi0)),
        make_step("D", fraction_text(p01), fraction_text(denom),
                  fraction_text(pi1)),
        make_step("M", fraction_text(pi0), fraction_text(p01),
                  fraction_text(flow01)),
        make_step("M", fraction_text(pi1), fraction_text(p10),
                  fraction_text(flow10)),
        make_step("CHECK", f"flow01={fraction_text(flow01)}",
                  f"flow10={fraction_text(flow10)}"),
    ]
    answer = f"pi0={fraction_text(pi0)}, pi1={fraction_text(pi1)}"
    return steps, answer


def expected_absorbing(problem):
    values = [Fraction(value) for value in ABS_RE.fullmatch(problem).groups()]
    p00, p01, p0a, p0b, p10, p11, p1a, p1b = values
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
        make_step("MARKOV_SETUP", "absorbing",
                  (f"row0 to0={fraction_text(p00)}, "
                   f"to1={fraction_text(p01)}, toA={fraction_text(p0a)}, "
                   f"toB={fraction_text(p0b)}"),
                  (f"row1 to0={fraction_text(p10)}, "
                   f"to1={fraction_text(p11)}, toA={fraction_text(p1a)}, "
                   f"toB={fraction_text(p1b)}")),
        make_step("ABSORB_EQ", "u0=p0A+p00*u0+p01*u1",
                  "u1=p1A+p10*u0+p11*u1"),
        make_step("S", 1, fraction_text(p00), fraction_text(a)),
        make_step("S", 0, fraction_text(p01), fraction_text(b)),
        make_step("S", 0, fraction_text(p10), fraction_text(c)),
        make_step("S", 1, fraction_text(p11), fraction_text(d)),
        make_step("LINEAR_SYSTEM", f"a={fraction_text(a)}, b={fraction_text(b)}",
                  f"c={fraction_text(c)}, d={fraction_text(d)}"),
        make_step("M", fraction_text(a), fraction_text(d),
                  fraction_text(a * d)),
        make_step("M", fraction_text(b), fraction_text(c),
                  fraction_text(b * c)),
        make_step("S", fraction_text(a * d), fraction_text(b * c),
                  fraction_text(det)),
        make_step("M", fraction_text(p0a), fraction_text(d),
                  fraction_text(p0a * d)),
        make_step("M", fraction_text(b), fraction_text(p1a),
                  fraction_text(b * p1a)),
        make_step("S", fraction_text(p0a * d), fraction_text(b * p1a),
                  fraction_text(u0_num)),
        make_step("D", fraction_text(u0_num), fraction_text(det),
                  fraction_text(u0)),
        make_step("M", fraction_text(a), fraction_text(p1a),
                  fraction_text(a * p1a)),
        make_step("M", fraction_text(p0a), fraction_text(c),
                  fraction_text(p0a * c)),
        make_step("S", fraction_text(a * p1a), fraction_text(p0a * c),
                  fraction_text(u1_num)),
        make_step("D", fraction_text(u1_num), fraction_text(det),
                  fraction_text(u1)),
        make_step("HIT_EQ", "t0=1+p00*t0+p01*t1",
                  "t1=1+p10*t0+p11*t1"),
        make_step("S", fraction_text(d), fraction_text(b),
                  fraction_text(t0_num)),
        make_step("D", fraction_text(t0_num), fraction_text(det),
                  fraction_text(t0)),
        make_step("S", fraction_text(a), fraction_text(c),
                  fraction_text(t1_num)),
        make_step("D", fraction_text(t1_num), fraction_text(det),
                  fraction_text(t1)),
    ]
    answer = (
        f"P(absorb A from 0)={fraction_text(u0)}, "
        f"P(absorb A from 1)={fraction_text(u1)}; "
        f"E[T from 0]={fraction_text(t0)}, "
        f"E[T from 1]={fraction_text(t1)}"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if NSTEP_RE.fullmatch(problem):
        steps, answer = expected_nstep(problem)
    elif STEADY_RE.fullmatch(problem):
        steps, answer = expected_steady(problem)
    else:
        steps, answer = expected_absorbing(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMarkovChainGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MarkovChainGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in MarkovChainGenerator.VARIANTS:
            result = MarkovChainGenerator(variant).generate()
            self.assertEqual(result["operation"], f"markov_chain_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MarkovChainGenerator("bogus")

    def test_probabilities_are_valid(self):
        for _ in range(300):
            result = self.gen.generate()
            if result["operation"] == "markov_chain_absorbing":
                values = [Fraction(v) for v in ABS_RE.fullmatch(
                    result["problem"]
                ).groups()]
                self.assertEqual(sum(values[:4], Fraction(0)), 1)
                self.assertEqual(sum(values[4:], Fraction(0)), 1)
            elif result["operation"] == "markov_chain_n_step":
                p00, p01, p10, p11 = (
                    Fraction(v) for v in NSTEP_RE.fullmatch(
                        result["problem"]
                    ).groups()
                )
                self.assertEqual(p00 + p01, 1)
                self.assertEqual(p10 + p11, 1)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

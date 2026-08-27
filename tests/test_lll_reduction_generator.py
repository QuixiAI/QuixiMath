import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lll_reduction_generator import LLLReductionGenerator
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe

BASIS_RE = re.compile(r"\[\((-?\d+),(-?\d+)\),\((-?\d+),(-?\d+)\)\]")
PAIR_RE = re.compile(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def norm2(v):
    return dot(v, v)


def det2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def parse_basis(problem):
    m = BASIS_RE.search(problem)
    a, b, c, d = map(int, m.groups())
    return (a, b), (c, d)


def round_half_away(fr):
    """Round-half-away-from-zero, the rule the problem text states."""
    if fr >= 0:
        return (fr.numerator + fr.denominator // 2) // fr.denominator
    return -round_half_away(-fr)


def lagrange_reduce(b1, b2):
    """Independent (swap-first, floor-rounding) Lagrange reduction.

    Different control flow from the generator's loop; used only to obtain a
    frame in which brute force over small coefficients is provably complete.
    """
    if norm2(b1) > norm2(b2):
        b1, b2 = b2, b1
    for _ in range(200):
        mu = Fraction(dot(b1, b2), norm2(b1))
        k = (mu + Fraction(1, 2)).__floor__()
        b2 = (b2[0] - k * b1[0], b2[1] - k * b1[1])
        if norm2(b2) >= norm2(b1):
            return b1, b2
        b1, b2 = b2, b1
    raise AssertionError("lagrange reduction did not terminate")


def brute_shortest(b1, b2):
    """Shortest nonzero lattice vector, by exhaustive search in a reduced
    frame (all short vectors have coefficients in {-2..2} there)."""
    r1, r2 = lagrange_reduce(b1, b2)
    best = None
    ties = []
    for a in range(-3, 4):
        for b in range(-3, 4):
            v = (a * r1[0] + b * r2[0], a * r1[1] + b * r2[1])
            if v == (0, 0):
                continue
            n = norm2(v)
            if best is None or n < best:
                best, ties = n, [v]
            elif n == best:
                ties.append(v)
    return best, {canonical_sign(v) for v in ties}


def canonical_sign(v):
    if v[0] < 0 or (v[0] == 0 and v[1] < 0):
        return (-v[0], -v[1])
    return v


def gauss_replay(b1, b2):
    """Replay of the stated hand procedure: mu, round, size-reduce, swap."""
    for _ in range(60):
        mu = Fraction(dot(b2, b1), norm2(b1))
        k = round_half_away(mu)
        if k:
            b2 = (b2[0] - k * b1[0], b2[1] - k * b1[1])
            continue
        if norm2(b2) < norm2(b1):
            b1, b2 = b2, b1
            continue
        return b1, b2
    raise AssertionError("gauss reduction did not terminate")


def basis_text(b1, b2):
    return f"[({b1[0]},{b1[1]}),({b2[0]},{b2[1]})]"


def lll_oracle(problem):
    b1, b2 = parse_basis(problem)
    r1, r2 = gauss_replay(b1, b2)
    best, shortest_set = brute_shortest(b1, b2)
    assert len(shortest_set) == 1, problem
    shortest = next(iter(shortest_set))
    # Independent facts: the reduced basis spans the same lattice, its first
    # vector is the (unique up to sign) shortest vector, and it is reduced.
    assert abs(det2(r1, r2)) == abs(det2(b1, b2)), problem
    assert norm2(r1) == best, problem
    assert canonical_sign(r1) == shortest, problem
    assert norm2(r1) <= norm2(r2), problem
    assert 2 * abs(dot(r1, r2)) <= norm2(r1), problem
    if "shortest" in problem:
        return f"shortest vector = ({shortest[0]},{shortest[1]}); norm^2 = {best}"
    return f"reduced basis = {basis_text(r1, r2)}"


def walk_steps(case, result):
    """Re-derive every emitted number from the problem's basis."""
    steps = result["steps"]
    case.assertTrue(steps[0].startswith("LLL_SETUP|"))
    b1, b2 = parse_basis(steps[0].split("|", 1)[1])
    case.assertEqual((b1, b2), parse_basis(result["problem"]))
    i = 1
    while steps[i].startswith("DOT|"):
        _, label, value = steps[i].split("|")
        case.assertEqual(label, "b2.b1")
        case.assertEqual(int(value), dot(b2, b1))
        _, label, den = steps[i + 1].split("|")
        case.assertTrue(steps[i + 1].startswith("NORM2|"))
        case.assertEqual(int(den), norm2(b1))
        code, mu_text, round_text = steps[i + 2].split("|")
        case.assertEqual(code, "MU")
        mu = Fraction(mu_text)
        case.assertEqual(mu, Fraction(dot(b2, b1), norm2(b1)))
        k = int(round_text.split("=")[1])
        case.assertEqual(k, round_half_away(mu))
        i += 3
        if steps[i].startswith("SIZE_REDUCE|"):
            _, old_text, new_text = steps[i].split("|")
            old = tuple(map(int, PAIR_RE.search(old_text).groups()))
            new = tuple(map(int, PAIR_RE.search(new_text).groups()))
            case.assertEqual(old, b2)
            case.assertEqual(new, (b2[0] - k * b1[0], b2[1] - k * b1[1]))
            b2 = new
            i += 1
        elif steps[i].startswith("SWAP|"):
            case.assertEqual(k, 0)
            _, n2_text, n1_text = steps[i].split("|")
            case.assertEqual(int(n2_text.split("=")[1]), norm2(b2))
            case.assertEqual(int(n1_text.split("=")[1]), norm2(b1))
            case.assertLess(norm2(b2), norm2(b1))
            b1, b2 = b2, b1
            i += 1
    case.assertTrue(steps[i].startswith("LLL_DONE|"), steps[i])
    case.assertEqual(parse_basis(steps[i]), (b1, b2))
    i += 1
    code, method, lhs, rhs = steps[i].split("|")
    case.assertEqual((code, method), ("CHECK", "det_invariant"))
    case.assertEqual(lhs.split("=")[1].strip(),
                     str(abs(det2(*parse_basis(result["problem"])))))
    case.assertEqual(lhs.split("=")[1], rhs.split("=")[1])
    i += 1
    if steps[i].startswith("NORMALIZE_SIGN|"):
        _, before, after = steps[i].split("|")
        v = tuple(map(int, PAIR_RE.search(before).groups()))
        w = tuple(map(int, PAIR_RE.search(after).groups()))
        case.assertEqual(w, canonical_sign(v))
        case.assertEqual(v, b1)
        i += 1
    if steps[i].startswith("SHORTEST|"):
        _, vec_text, norm_text = steps[i].split("|")
        v = tuple(map(int, PAIR_RE.search(vec_text).groups()))
        case.assertEqual(v, canonical_sign(b1))
        case.assertEqual(int(norm_text.split("=")[1]), norm2(v))
        i += 1
    case.assertEqual(i, len(steps) - 1)
    case.assertTrue(steps[-1].startswith("Z|"))


class TestLLLReductionGenerator(unittest.TestCase):
    def test_contract_oracle_and_formatting(self):
        random.seed(123)
        gen = LLLReductionGenerator()
        bases = set()
        problems = set()
        operations = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             lll_oracle(result["problem"]), result["problem"])
            self.assertFalse(any("--" in s for s in result["steps"]))
            self.assertTrue(any(s.startswith("LLL_DONE|")
                                for s in result["steps"]))
            walk_steps(self, result)
            bases.add(parse_basis(result["problem"]))
            problems.add(result["problem"])
            operations.add(result["operation"])
        self.assertGreaterEqual(len(bases), 250)
        self.assertGreaterEqual(len(problems), 280)
        self.assertEqual(operations,
                         {"lll_reduction_2d", "lll_reduction_2d_shortest"})

    def test_fixed_variants(self):
        random.seed(5)
        for variant, operation in (("basis", "lll_reduction_2d"),
                                   ("shortest", "lll_reduction_2d_shortest")):
            gen = LLLReductionGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"], operation)
                self.assertEqual(result["final_answer"],
                                 lll_oracle(result["problem"]))
        with self.assertRaises(ValueError):
            LLLReductionGenerator("bogus")

    def test_phrasings_all_parse(self):
        random.seed(9)
        gen = LLLReductionGenerator()
        openings = set()
        for _ in range(200):
            result = gen.generate()
            openings.add(result["problem"][:24])
            self.assertRegex(result["problem"], BASIS_RE)
        self.assertGreaterEqual(len(openings), 5)


if __name__ == "__main__":
    unittest.main()

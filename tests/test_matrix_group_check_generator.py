import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.matrix_group_check_generator import MatrixGroupCheckGenerator
from helpers import DELIM


NUM = r"-?\d+(?:/\d+)?"
MATRIX_RE = rf"(\[\[{NUM},{NUM}\],\[{NUM},{NUM}\]\])"
GROUP_RE = r"(SO2|SU2|O2|SL2Z|GL2Z)"

# Independent copy of the phrasings: drift makes the coverage test fail.
TEMPLATES = [
    "Check whether M={matrix} is a member of {group}.",
    "Does M={matrix} belong to {group}? Verify the defining conditions.",
    "Decide whether the matrix M={matrix} lies in the group {group}.",
    "Test M={matrix} for membership in {group}.",
    "Is M={matrix} an element of {group}? Check the group conditions.",
]

LABELS = {
    "so2": ("R", "R^T R"),
    "o2": ("R", "R^T R"),
    "su2": ("U", "U^dagger U"),
    "sl2z": ("M", "M^T M"),
    "gl2z": ("M", "M^T M"),
}
CIRCLE = ("so2", "su2", "o2")


def to_pattern(template):
    parts = re.split(r"(\{matrix\}|\{group\})", template)
    lookup = {"{matrix}": MATRIX_RE, "{group}": GROUP_RE}
    return "".join(lookup.get(part, re.escape(part)) for part in parts)


PATTERNS = [re.compile(to_pattern(t)) for t in TEMPLATES]
ENTRY_RE = re.compile(rf"\[\[({NUM}),({NUM})\],\[({NUM}),({NUM})\]\]")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    """Return (phrasing index, group, 2x2 Fraction matrix)."""
    for idx, pattern in enumerate(PATTERNS):
        m = pattern.fullmatch(problem)
        if m:
            group = m.group(2).lower()
            a, b, c, d = ENTRY_RE.fullmatch(m.group(1)).groups()
            M = [[Fraction(a), Fraction(b)], [Fraction(c), Fraction(d)]]
            return idx, group, M
    raise AssertionError(f"unparsed phrasing: {problem!r}")


def transpose(M):
    return [[M[j][i] for j in range(2)] for i in range(2)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def determinant(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def is_integral(M):
    return all(v.denominator == 1 for row in M for v in row)


def oracle_answer(problem):
    """Membership decided from the problem text by an independent route.

    Orthogonality is tested by actually forming M^T M (four dot products),
    not by the a^2 + b^2 shortcut the generator's steps take.
    """
    _, group, M = parse_problem(problem)
    gram = matmul(transpose(M), M)
    det = determinant(M)
    scale = gram[0][0]
    if group in CIRCLE:
        # rotation/reflection shapes always give M^T M = (a^2 + b^2) I
        assert gram[0][1] == 0 and gram[1][0] == 0, gram
        assert gram[1][1] == scale, gram
        orthogonal = gram == [[1, 0], [0, 1]]
        member = orthogonal if group == "o2" else (orthogonal and det == 1)
        product_label = LABELS[group][1]
        norm_text = "I" if scale == 1 else f"({fraction_text(scale)})I"
        detail = f"{product_label} = {norm_text}, det = {fraction_text(det)}"
    else:
        assert is_integral(M), M
        member = det == 1 if group == "sl2z" else det in (1, -1)
        detail = f"integer entries, det = {fraction_text(det)}"
    return (f"{group.upper()} member {'yes' if member else 'no'}; {detail}")


def expected_flow(example):
    """Rebuild the whole scratchpad from the problem text alone."""
    _, group, M = parse_problem(example["problem"])
    matrix = ("[[" + ",".join(fraction_text(v) for v in M[0]) + "],["
              + ",".join(fraction_text(v) for v in M[1]) + "]]")
    symbol, product_label = LABELS[group]
    left = M[0][0] * M[1][1]
    right = M[0][1] * M[1][0]
    det = left - right
    answer = oracle_answer(example["problem"])
    if group in CIRCLE:
        a_sq = M[0][0] ** 2
        b_sq = M[1][0] ** 2
        norm = a_sq + b_sq
        norm_text = "I" if norm == 1 else f"({fraction_text(norm)})I"
        steps = [
            make_step("MATRIX_GROUP_SETUP", group.upper(), f"M={matrix}"),
            make_step("E", fraction_text(M[0][0]), 2, fraction_text(a_sq)),
            make_step("E", fraction_text(M[1][0]), 2, fraction_text(b_sq)),
            make_step("A", fraction_text(a_sq), fraction_text(b_sq),
                      fraction_text(norm)),
            make_step("CHECK", product_label, norm_text,
                      "metric preserved" if norm == 1 else "columns not unit"),
            make_step("M", fraction_text(M[0][0]), fraction_text(M[1][1]),
                      fraction_text(left)),
            make_step("M", fraction_text(M[0][1]), fraction_text(M[1][0]),
                      fraction_text(right)),
            make_step("S", fraction_text(left), fraction_text(right),
                      fraction_text(det)),
            make_step("CHECK", f"det {symbol}", fraction_text(det),
                      "special" if det == 1 else "not special"),
            make_step("Z", answer),
        ]
    else:
        steps = [
            make_step("MATRIX_GROUP_SETUP", group.upper(), f"M={matrix}"),
            make_step("CHECK", "entries", "all integers", "lattice condition"),
            make_step("M", fraction_text(M[0][0]), fraction_text(M[1][1]),
                      fraction_text(left)),
            make_step("M", fraction_text(M[0][1]), fraction_text(M[1][0]),
                      fraction_text(right)),
            make_step("S", fraction_text(left), fraction_text(right),
                      fraction_text(det)),
            make_step("CHECK", f"det {symbol}", fraction_text(det),
                      "unimodular" if det in (1, -1) else "not unimodular"),
            make_step("Z", answer),
        ]
    return steps, answer


class TestMatrixGroupCheckGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MatrixGroupCheckGenerator()

    def test_output_contract(self):
        for _ in range(50):
            result = self.gen.generate()
            for key in ("problem_id", "operation", "problem", "steps",
                        "final_answer"):
                self.assertIn(key, result)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                             result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(600):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_membership_matches_group_definition(self):
        for _ in range(600):
            result = self.gen.generate()
            _, group, M = parse_problem(result["problem"])
            gram = matmul(transpose(M), M)
            det = determinant(M)
            verdict = result["final_answer"].split(" member ")[1].split(";")[0]
            if group == "so2" or group == "su2":
                want = gram == [[1, 0], [0, 1]] and det == 1
            elif group == "o2":
                want = gram == [[1, 0], [0, 1]]
            elif group == "sl2z":
                want = is_integral(M) and det == 1
            else:
                want = is_integral(M) and det in (1, -1)
            self.assertEqual(verdict, "yes" if want else "no",
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(400):
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_every_phrasing_group_and_verdict_appears(self):
        phrasings, groups, verdicts = set(), set(), set()
        for _ in range(1200):
            result = self.gen.generate()
            idx, group, _ = parse_problem(result["problem"])
            phrasings.add(idx)
            groups.add(group)
            verdicts.add((group,
                          result["final_answer"].split(" member ")[1][:3]))
        self.assertEqual(phrasings, set(range(len(TEMPLATES))))
        self.assertEqual(groups, set(MatrixGroupCheckGenerator.VARIANTS))
        for group in MatrixGroupCheckGenerator.VARIANTS:
            self.assertIn((group, "yes"), verdicts)
            self.assertIn((group, "no;"), verdicts)

    def test_variants_are_available(self):
        for variant in MatrixGroupCheckGenerator.VARIANTS:
            for _ in range(20):
                result = MatrixGroupCheckGenerator(variant).generate()
                self.assertEqual(result["operation"],
                                 f"matrix_group_check_{variant}")
                self.assertEqual(parse_problem(result["problem"])[1], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MatrixGroupCheckGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)

    def test_deterministic_under_seed(self):
        random.seed(19)
        first = [self.gen.generate() for _ in range(25)]
        random.seed(19)
        second = [self.gen.generate() for _ in range(25)]
        self.assertEqual([e["steps"] for e in first],
                         [e["steps"] for e in second])


if __name__ == "__main__":
    unittest.main()

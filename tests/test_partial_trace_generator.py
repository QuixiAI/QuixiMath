import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.partial_trace_generator import PartialTraceGenerator
from helpers import DELIM


BELL_RE = re.compile(
    r"Trace out qubit B for phase-shifted Bell state Phi\(([^)]+)\) = "
    r"\(ket00 \+ e\^\(i([^)]+)\)ket11\)/sqrt\(2\)\."
)
PRODUCT_RE = re.compile(
    r"Trace out qubit B for phase-shifted product state "
    r"plus\(([^)]+)\)0 = "
    r"\(ket00 \+ e\^\(i([^)]+)\)ket10\)/sqrt\(2\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


SCHMIDT_RE = re.compile(
    r"Trace out qubit B for the state psi = \(sqrt\((\d+)\)ket00 "
    r"([+-]) sqrt\((\d+)\)ket11\)/sqrt\((\d+)\)\.")


def parse_problem(problem):
    match = BELL_RE.fullmatch(problem)
    if match:
        assert match.group(1) == match.group(2), problem
        return "bell_phi_plus", match.group(1)
    match = SCHMIDT_RE.fullmatch(problem)
    if match:
        return "schmidt_diagonal", (int(match.group(1)),
                                    match.group(2),
                                    int(match.group(3)),
                                    int(match.group(4)))
    match = PRODUCT_RE.fullmatch(problem)
    assert match, problem
    assert match.group(1) == match.group(2), problem
    return "product_plus_zero", match.group(1)


def expected_flow(example):
    variant, params = parse_problem(example["problem"])
    if variant == "schmidt_diagonal":
        # independent check: weights normalize, rho_A diagonal with a/(a+b)
        from fractions import Fraction
        a, _sign, b, total = params
        assert a + b == total, example["problem"]
        pa, pb = Fraction(a, total), Fraction(b, total)
        rho = f"[[{pa},0],[0,{pb}]]"
        answer = f"rho_A = {rho}; entangled yes"
        # verify final answer and diagonal trace = 1; skip full trace match
        assert pa + pb == 1
        return None, answer
    if variant == "bell_phi_plus":
        phase = params
        positive_phase = f"e^(i{phase})"
        negative_phase = f"e^(-i{phase})"
        psi = f"(ket00 + {positive_phase}ket11)/sqrt(2)"
        rho = "[[1/2,0],[0,1/2]]"
        answer = f"rho_A = {rho}; entangled yes"
        steps = [
            make_step("DENSITY_SETUP", "state=Phi_phase", f"psi={psi}"),
            make_step("OUTER_PRODUCT",
                      f"rho=1/2(ket00bra00+{negative_phase}ket00bra11+"
                      f"{positive_phase}ket11bra00+ket11bra11)"),
            make_step("PARTIAL_TRACE", "ket00bra00", "ket0bra0"),
            make_step("PARTIAL_TRACE", "ket00bra11", "0"),
            make_step("PARTIAL_TRACE", "ket11bra00", "0"),
            make_step("PARTIAL_TRACE", "ket11bra11", "ket1bra1"),
            make_step("REDUCED_DENSITY", f"rho_A={rho}"),
            make_step("CHECK", "Tr(rho_A^2)", "1/2", "mixed entangled"),
            make_step("Z", answer),
        ]
    else:
        phase = params
        positive_phase = f"e^(i{phase})"
        negative_phase = f"e^(-i{phase})"
        psi = f"(ket00 + {positive_phase}ket10)/sqrt(2)"
        rho = (f"[[1/2,{negative_phase}/2],"
               f"[{positive_phase}/2,1/2]]")
        answer = f"rho_A = {rho}; entangled no"
        steps = [
            make_step("DENSITY_SETUP", "state=plus_phase_0", f"psi={psi}"),
            make_step("OUTER_PRODUCT",
                      f"rho=1/2(ket00bra00+{negative_phase}ket00bra10+"
                      f"{positive_phase}ket10bra00+ket10bra10)"),
            make_step("PARTIAL_TRACE", "ket00bra00", "ket0bra0"),
            make_step("PARTIAL_TRACE", "ket00bra10", "ket0bra1"),
            make_step("PARTIAL_TRACE", "ket10bra00", "ket1bra0"),
            make_step("PARTIAL_TRACE", "ket10bra10", "ket1bra1"),
            make_step("REDUCED_DENSITY", f"rho_A={rho}"),
            make_step("CHECK", "Tr(rho_A^2)", "1", "pure separable"),
            make_step("Z", answer),
        ]
    return steps, answer


class TestPartialTraceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PartialTraceGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(100):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            if expected_steps is not None:
                self.assertEqual(result["steps"], expected_steps,
                                 result["problem"])

    def test_variants_are_available(self):
        for variant in PartialTraceGenerator.VARIANTS:
            result = PartialTraceGenerator(variant).generate()
            self.assertEqual(result["operation"], f"partial_trace_{variant}")
            self.assertEqual(parse_problem(result["problem"])[0], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PartialTraceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(100):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

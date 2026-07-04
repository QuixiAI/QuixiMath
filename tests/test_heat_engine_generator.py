import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.heat_engine_generator import HeatEngineGenerator
from helpers import DELIM


ENGINE_RE = re.compile(
    r"A heat engine absorbs Qh=(\d+) J and rejects Qc=(\d+) J\. Find work "
    r"output and efficiency\."
)
CARNOT_RE = re.compile(
    r"A reversible engine operates between Th=(\d+) K and Tc=(\d+) K\. "
    r"Find the Carnot efficiency\."
)
FRIDGE_RE = re.compile(
    r"A refrigerator removes Qc=(\d+) J from the cold space using work "
    r"W=(\d+) J\. Find heat rejected Qh and COP_R\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_engine(problem):
    q_hot, q_cold = (int(value) for value in ENGINE_RE.fullmatch(problem).groups())
    work = q_hot - q_cold
    efficiency = Fraction(work, q_hot)
    steps = [
        make_step("ENGINE_SETUP", "engine_efficiency",
                  f"Qh={q_hot}", f"Qc={q_cold}"),
        make_step("ENGINE_FORMULA", "W=Qh-Qc"),
        make_step("S", q_hot, q_cold, work),
        make_step("ENGINE_FORMULA", "eta=W/Qh"),
        make_step("D", work, q_hot, fraction_text(efficiency)),
    ]
    answer = f"W={work} J; efficiency={fraction_text(efficiency)}"
    return steps, answer


def expected_carnot(problem):
    t_hot, t_cold = (
        int(value) for value in CARNOT_RE.fullmatch(problem).groups()
    )
    temp_gap = t_hot - t_cold
    efficiency = Fraction(temp_gap, t_hot)
    steps = [
        make_step("ENGINE_SETUP", "carnot_efficiency",
                  f"Th={t_hot}", f"Tc={t_cold}"),
        make_step("ENGINE_FORMULA", "eta_C=1-Tc/Th=(Th-Tc)/Th"),
        make_step("S", t_hot, t_cold, temp_gap),
        make_step("D", temp_gap, t_hot, fraction_text(efficiency)),
    ]
    answer = f"Carnot efficiency={fraction_text(efficiency)}"
    return steps, answer


def expected_fridge(problem):
    q_cold, work = (int(value) for value in FRIDGE_RE.fullmatch(problem).groups())
    q_hot = q_cold + work
    cop = Fraction(q_cold, work)
    steps = [
        make_step("ENGINE_SETUP", "refrigerator_cop",
                  f"Qc={q_cold}", f"W={work}"),
        make_step("ENGINE_FORMULA", "Qh=Qc+W"),
        make_step("A", q_cold, work, q_hot),
        make_step("ENGINE_FORMULA", "COP_R=Qc/W"),
        make_step("D", q_cold, work, fraction_text(cop)),
    ]
    answer = f"Qh={q_hot} J; COP_R={fraction_text(cop)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ENGINE_RE.fullmatch(problem):
        steps, answer = expected_engine(problem)
    elif CARNOT_RE.fullmatch(problem):
        steps, answer = expected_carnot(problem)
    else:
        steps, answer = expected_fridge(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestHeatEngineGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = HeatEngineGenerator()

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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in HeatEngineGenerator.VARIANTS:
            result = HeatEngineGenerator(variant).generate()
            self.assertEqual(result["operation"], f"heat_engine_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HeatEngineGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

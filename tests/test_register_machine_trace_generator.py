"""Prompt-only oracle for RegisterMachineTraceGenerator (depth strand)."""
import random
import re
import unittest

from generators.register_machine_trace_generator import (
    RegisterMachineTraceGenerator)
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_INIT = re.compile(r"\(((?:r\d+=\d+(?:, )?)+)\)")
_LINE = re.compile(r"L\d+: (?:HALT|(?:INC|DEC) r\d+ -> L\d+"
                   r"(?: else L\d+)?)")


def _parse_regs(txt):
    return {name: int(value) for name, value in
            (pair.split("=") for pair in txt.split(", "))}


def _interpret(lines, regs):
    """An independent interpreter, written against the printed grammar."""
    table = {}
    for line in lines:
        label, body = line.split(": ", 1)
        table[label] = body
    pc = lines[0].split(":", 1)[0]
    regs = dict(regs)
    executed = 0
    while True:
        body = table[pc]
        if body == "HALT":
            return executed, regs
        executed += 1
        match = re.fullmatch(r"(INC|DEC) (r\d+) -> (L\d+)(?: else (L\d+))?",
                             body)
        op, reg, goto, other = match.groups()
        if op == "INC":
            regs[reg] += 1
            pc = goto
        elif regs[reg] > 0:
            regs[reg] -= 1
            pc = goto
        else:
            pc = other
        assert executed <= 3000


def _parse_problem(problem):
    lines = _LINE.findall(problem)
    regs = _parse_regs(_INIT.search(problem).group(1))
    return lines, regs


def _reg_txt(regs):
    return "(" + ", ".join(f"{k}={regs[k]}" for k in sorted(regs)) + ")"


def oracle_answer(example):
    problem = example["problem"]
    lines, regs0 = _parse_problem(problem)
    executed, final = _interpret(lines, regs0)
    op = example["operation"]
    if op.startswith("register_machine_trace_halting_step"):
        return str(executed)
    if op.startswith("register_machine_trace_final_registers"):
        return _reg_txt(final)
    invariant = re.search(r"(?:quantity |conserved )([^;.]+?(?:\)))[;. ]",
                          problem).group(1).strip()
    conserved = int(example["final_answer"].rsplit("= ", 1)[1]
                    .split(" ")[0])
    return f"{_reg_txt(final)}; {invariant} = {conserved} conserved"


class TestRegisterMachineTraceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RegisterMachineTraceGenerator()

    def test_output_contract_and_depth(self):
        for _ in range(20):
            result = self.gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            tier = result["operation"].rsplit("_", 1)[1]
            self.assertGreaterEqual(chain_depth(result["steps"]),
                                    TIER_FLOORS[tier])
            self.assertFalse(milestone_violations(result["steps"]))
            self.assertLessEqual(record_chars(result), 16_000)
            self.assertIsNotNone(parse_count(result["problem"]))

    def test_oracle_recomputes_from_problem_text(self):
        for variant in ("final_registers", "halting_step"):
            gen = RegisterMachineTraceGenerator(variant)
            for _ in range(25):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:170])

    def test_invariant_variant_registers_and_value(self):
        gen = RegisterMachineTraceGenerator("trace_invariant")
        for _ in range(25):
            result = gen.generate()
            lines, regs0 = _parse_problem(result["problem"])
            executed, final = _interpret(lines, regs0)
            self.assertTrue(result["final_answer"]
                            .startswith(_reg_txt(final) + ";"))
            # milestones all carry one identical conserved value, and the
            # trace really executed to the same halt
            milestone_values = {s.split(DELIM)[3]
                                for s in result["steps"]
                                if s.startswith(f"MILESTONE{DELIM}")}
            self.assertEqual(len(milestone_values), 1, milestone_values)
            conserved = result["final_answer"].rsplit("= ", 1)[1]
            self.assertTrue(conserved.startswith(
                milestone_values.pop()))

    def test_every_rm_step_matches_the_program(self):
        gen = RegisterMachineTraceGenerator("final_registers", tier="d100")
        for _ in range(8):
            result = gen.generate()
            lines, regs0 = _parse_problem(result["problem"])
            names = sorted(regs0)
            bodies = {line.split(": ", 1)[0]: line.split(": ", 1)[1]
                      for line in lines}

            def state(field):
                values = re.match(r"\((.*);L\d+\)", field).group(1)
                return dict(zip(names, map(int, values.split(","))))

            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "RM_STEP":
                    continue
                before = state(fields[1])
                note_label = fields[2].split(":", 1)[0]
                after = state(fields[3])
                body = bodies[note_label]
                match = re.fullmatch(
                    r"(INC|DEC) (r\d+) -> (L\d+)(?: else (L\d+))?", body)
                op, reg, goto, other = match.groups()
                expected = dict(before)
                if op == "INC":
                    expected[reg] += 1
                elif before[reg] > 0:
                    expected[reg] -= 1
                self.assertEqual(after, expected, raw)

    def test_halting_trace_length_matches_answer(self):
        gen = RegisterMachineTraceGenerator("halting_step", tier="d50")
        for _ in range(10):
            result = gen.generate()
            rm_steps = sum(1 for s in result["steps"]
                           if s.startswith(f"RM_STEP{DELIM}"))
            self.assertEqual(rm_steps, int(result["final_answer"]))

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = RegisterMachineTraceGenerator("halting_step",
                                                   tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            RegisterMachineTraceGenerator("bogus")
        with self.assertRaises(ValueError):
            RegisterMachineTraceGenerator(tier="d1000")


if __name__ == "__main__":
    unittest.main()

import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.dfa_minimization_generator import DFAMinimizationGenerator
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


ALPHABET = ["0", "1"]


def block_text(block):
    return "{" + ",".join(sorted(block)) + "}"


def partition_text(partition):
    return ", ".join(block_text(block) for block in partition)


def normalize(blocks):
    return sorted([tuple(sorted(block)) for block in blocks if block],
                  key=lambda block: block[0])


def block_index(partition, state):
    for i, block in enumerate(partition):
        if state in block:
            return i
    raise AssertionError(state)


def parse_problem(problem):
    match = re.search(
        r"states ([^;]+); alphabet ([^;]+); start ([^;]+); accepting states "
        r"([^;]+); transitions (.+?)(?:\. Give|\.|, find|$)",
        problem,
    )
    assert match is not None, problem
    states, _, start, accept, trans_text = match.groups()
    states = states.split(", ")
    accept = accept.split(", ") if accept != "none" else []
    transitions = {}
    for clause in trans_text.split("; "):
        state, entries = clause.split(":")
        for entry in entries.split(","):
            symbol, target = entry.split("->")
            transitions[(state, symbol)] = target
    return states, start, accept, transitions


def refine(states, transitions, partition):
    groups = {}
    for state in states:
        signature = tuple(block_index(partition, transitions[(state, sym)])
                          for sym in ALPHABET)
        groups.setdefault((block_index(partition, state), signature),
                          []).append(state)
    return normalize(groups.values())


def oracle(problem):
    states, start, accept, transitions = parse_problem(problem)
    non_accept = [s for s in states if s not in accept]
    partition = normalize([non_accept, accept])
    while True:
        new_partition = refine(states, transitions, partition)
        if new_partition == partition:
            break
        partition = new_partition
    names = {block: block_text(block) for block in partition}
    start_block = partition[block_index(partition, start)]
    accepting = [block for block in partition if set(block) & set(accept)]
    min_trans = []
    for block in partition:
        rep = block[0]
        pieces = []
        for sym in ALPHABET:
            target_block = partition[block_index(partition,
                                                 transitions[(rep, sym)])]
            pieces.append(f"{sym}->{names[target_block]}")
        min_trans.append(f"{names[block]}:{','.join(pieces)}")
    return (
        f"blocks = {partition_text(partition)}; "
        f"start = {names[start_block]}; "
        f"accepting = {partition_text(accepting)}; "
        f"transitions = {'; '.join(min_trans)}"
    )


class TestDFAMinimizationGenerator(unittest.TestCase):
    def test_contract_oracle_and_variants(self):
        random.seed(123)
        gen = DFAMinimizationGenerator()
        saw = set()
        openings = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(";", 1)[0])
        self.assertEqual(saw, {f"dfa_minimization_{v}"
                               for v in DFAMinimizationGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            DFAMinimizationGenerator("bad")


if __name__ == "__main__":
    unittest.main()

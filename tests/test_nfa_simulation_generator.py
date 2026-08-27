import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.nfa_simulation_generator import NFASimulationGenerator
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


PROBLEM_RE = re.compile(
    r"states ([^;:]+); alphabet ([^;]+); start ([^;]+); accepting states "
    r"([^;]+); transitions (.+); input ([a-z]+)"
)
ENTRY_RE = re.compile(r"([a-z]+)->(\{[^}]*\})")

# Independent copy of the six phrasings' distinctive openings.
OPENINGS = [
    "Run the NFA with states ",
    "Trace active states for this NFA: states ",
    "For the NFA described by states ",
    "A nondeterministic machine has states ",
    "Simulate the subset construction on the fly: states ",
    "Given states ",
]


def parse_set(text):
    body = text.strip()[1:-1]
    return set() if not body else set(body.split(","))


def set_text(values):
    values = sorted(values)
    return "{" + ",".join(values) + "}" if values else "{}"


def parse_problem(problem):
    match = PROBLEM_RE.search(problem)
    assert match is not None, problem
    states, alphabet, start, accept, trans_text, input_text = match.groups()
    alphabet = alphabet.split(", ")
    transitions = {}
    epsilons = {}
    for clause in trans_text.split("; "):
        state, entries = clause.split(":", 1)
        for symbol, target_text in ENTRY_RE.findall(entries):
            targets = parse_set(target_text)
            if symbol == "epsilon":
                epsilons[state] = targets
            else:
                assert symbol in alphabet, (symbol, alphabet)
                transitions[(state, symbol)] = targets
    return {
        "states": states.split(", "),
        "alphabet": alphabet,
        "start": start,
        "accept": set(accept.split(", ")) if accept != "none" else set(),
        "transitions": transitions,
        "epsilons": epsilons,
        "input": input_text,
    }


def path_reachable_sets(parts):
    """Active sets by product-graph reachability, not frontier iteration.

    Nodes are (state, symbols consumed); epsilon edges keep the counter and
    symbol edges advance it. Depth-first search collects every node reachable
    from (start, 0), then the active set after k symbols is read off by
    counter. This is a different algorithm from the generator's step-by-step
    move-then-close loop, so agreement is a real cross-check.
    """
    word = parts["input"]
    seen = set()
    stack = [(parts["start"], 0)]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        state, index = node
        for target in parts["epsilons"].get(state, set()):
            stack.append((target, index))
        if index < len(word):
            for target in parts["transitions"].get((state, word[index]),
                                                   set()):
                stack.append((target, index + 1))
    return [{state for state, index in seen if index == k}
            for k in range(len(word) + 1)]


def oracle(problem):
    parts = parse_problem(problem)
    sets = path_reachable_sets(parts)
    status = "accepted" if sets[-1] & parts["accept"] else "rejected"
    return f"{status}; sets = {' -> '.join(set_text(s) for s in sets)}"


def check_steps(case, result):
    parts = parse_problem(result["problem"])
    sets = path_reachable_sets(parts)
    word = parts["input"]
    seen_codes = set()
    active_seen = []
    for raw_step in result["steps"]:
        fields = raw_step.split(DELIM)
        code = fields[0]
        seen_codes.add(code)
        if code == "NFA_SETUP":
            case.assertEqual(fields[1],
                             "states " + ", ".join(parts["states"]))
            case.assertEqual(fields[3], f"start {parts['start']}")
        elif code == "NFA_ACCEPT":
            case.assertEqual(set(fields[1].split(", ")), parts["accept"])
        elif code == "NFA_TRANSITION":
            state, symbol, targets = fields[1], fields[2], parse_set(fields[3])
            case.assertEqual(targets,
                             parts["transitions"].get((state, symbol), set()))
        elif code == "NFA_EPSILON":
            case.assertEqual(parse_set(fields[2]),
                             parts["epsilons"].get(fields[1], set()))
        elif code == "NFA_INPUT":
            case.assertEqual(fields[1], word)
        elif code == "NFA_READ":
            pos = int(fields[1].split()[1])
            case.assertEqual(fields[2], word[pos - 1])
        elif code == "NFA_MOVE":
            before = parse_set(fields[1])
            symbol = fields[2]
            moved = parse_set(fields[4])
            union = set()
            if fields[3] != "none":
                for piece in fields[3].split("; "):
                    src, dst = piece.split("->")
                    case.assertIn(src, before)
                    case.assertEqual(
                        parse_set(dst),
                        parts["transitions"].get((src, symbol), set()))
                    union |= parse_set(dst)
            case.assertEqual(union, moved, raw_step)
        elif code == "NFA_ACTIVE":
            active_seen.append(parse_set(fields[2]))
        elif code == "CHECK":
            listed = fields[1].split(" = ")[1]
            expected = sorted(sets[-1] & parts["accept"])
            case.assertEqual(listed,
                             ", ".join(expected) if expected else "none")
    case.assertEqual(active_seen, sets)
    case.assertIn("EPS_CLOSURE", seen_codes)
    case.assertIn("NFA_MOVE", seen_codes)


class TestNFASimulationGenerator(unittest.TestCase):
    def test_contract_oracle_and_pipe_safety(self):
        random.seed(123)
        gen = NFASimulationGenerator()
        saw = set()
        openings = set()
        verdicts = set()
        for _ in range(600):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertNotIn(DELIM, result["final_answer"])
            self.assertNotIn(DELIM, result["problem"])
            self.assertEqual(result["final_answer"], oracle(result["problem"]),
                             result["problem"])
            check_steps(self, result)
            saw.add(result["operation"])
            verdicts.add(result["final_answer"].split(";")[0])
            for index, opening in enumerate(OPENINGS):
                if result["problem"].startswith(opening):
                    openings.add(index)
        self.assertEqual(saw, {f"nfa_simulation_{v}"
                               for v in NFASimulationGenerator.VARIANTS})
        self.assertEqual(openings, set(range(len(OPENINGS))))
        self.assertEqual(verdicts, {"accepted", "rejected"})

    def test_explicit_variants(self):
        random.seed(7)
        for variant in NFASimulationGenerator.VARIANTS:
            gen = NFASimulationGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"nfa_simulation_{variant}")
                self.assertEqual(result["final_answer"],
                                 oracle(result["problem"]),
                                 result["problem"])
                check_steps(self, result)

    def test_alphabets_and_state_labels_vary(self):
        random.seed(5)
        gen = NFASimulationGenerator()
        alphabets, labels = set(), set()
        for _ in range(300):
            parts = parse_problem(gen.generate()["problem"])
            alphabets.add(tuple(parts["alphabet"]))
            labels.add(tuple(parts["states"]))
        self.assertIn(("a", "b"), alphabets)
        self.assertIn(("a", "b", "c"), alphabets)
        self.assertGreater(len(labels), 50)

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            NFASimulationGenerator("bad")

    def test_deterministic_under_seed(self):
        gen = NFASimulationGenerator()
        random.seed(31)
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(31)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

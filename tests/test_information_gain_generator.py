import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.information_gain_generator import InformationGainGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"A dataset has 16 examples with pos=(\d+) and neg=(\d+)\. "
    r"Candidate splits are (\w+): left pos=(\d+), neg=(\d+); "
    r"right pos=(\d+), neg=(\d+) and (\w+): left pos=(\d+), neg=(\d+); "
    r"right pos=(\d+), neg=(\d+)\. Use self-info values "
    r"I\(p\)=-log2\(p\): (.+)\. Compute information gain for each split "
    r"and choose the better split\."
)

TOTAL = 16


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def decimal_text(value):
    value = Fraction(value)
    num, den = value.numerator, value.denominator
    places = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        places += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        places += 1
    if den != 1:
        raise AssertionError(value)
    if places == 0:
        return str(num)
    sign = "-" if num < 0 else ""
    digits = str(abs(num)).rjust(places + 1, "0")
    return sign + f"{digits[:-places]}.{digits[-places:]}".rstrip("0").rstrip(".")


def parse_info_table(raw):
    table = {}
    for piece in raw.split(", "):
        probability, value = piece.split("=")
        table[Fraction(probability)] = Fraction(value)
    return table


def info_table_text(info_table):
    return ", ".join(
        f"{fraction_text(probability)}={decimal_text(value)}"
        for probability, value in sorted(info_table.items())
    )


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    groups = match.groups()
    parent = [int(groups[0]), int(groups[1])]
    first = groups[2]
    second = groups[7]
    splits = {
        first: {
            "left": {"pos": int(groups[3]), "neg": int(groups[4])},
            "right": {"pos": int(groups[5]), "neg": int(groups[6])},
        },
        second: {
            "left": {"pos": int(groups[8]), "neg": int(groups[9])},
            "right": {"pos": int(groups[10]), "neg": int(groups[11])},
        },
    }
    info_table = parse_info_table(groups[12])
    return parent, [first, second], splits, info_table


def entropy_from_counts(counts, total, info_table):
    entropy = Fraction(0)
    for count in counts:
        if count == 0:
            continue
        probability = Fraction(count, total)
        entropy += probability * info_table[probability]
    return entropy


def append_entropy_steps(steps, label, counts, total, info_table):
    steps.append(make_step("ENTROPY_SETUP", label,
                           f"counts={counts[0]},{counts[1]}",
                           f"total={total}"))
    running = Fraction(0)
    for count in counts:
        if count == 0:
            steps.append(make_step("ENTROPY_ZERO", label, "count=0"))
            continue
        probability = Fraction(count, total)
        info = info_table[probability]
        term = probability * info
        new_running = running + term
        steps.extend([
            make_step("D", count, total, fraction_text(probability)),
            make_step("INFO_VALUE", f"p={fraction_text(probability)}",
                      f"I={decimal_text(info)}"),
            make_step("M", fraction_text(probability), decimal_text(info),
                      decimal_text(term)),
            make_step("A", decimal_text(running), decimal_text(term),
                      decimal_text(new_running)),
        ])
        running = new_running
    steps.append(make_step("ENTROPY_VALUE", label, decimal_text(running)))
    return running


def expected_flow(example):
    parent, features, splits, info_table = parse_problem(example["problem"])
    steps = [
        make_step("IG_SETUP", f"parent pos={parent[0]}, neg={parent[1]}",
                  f"total={TOTAL}", f"splits={features[0]},{features[1]}"),
        make_step("INFO_TABLE", info_table_text(info_table)),
    ]
    parent_entropy = append_entropy_steps(
        steps, "parent", parent, TOTAL, info_table
    )

    gains = {}
    for feature in features:
        split = splits[feature]
        steps.append(make_step("SPLIT_SETUP", feature,
                               f"left pos={split['left']['pos']}, "
                               f"neg={split['left']['neg']}",
                               f"right pos={split['right']['pos']}, "
                               f"neg={split['right']['neg']}"))
        weighted_terms = []
        for branch in ("left", "right"):
            branch_counts = [split[branch]["pos"], split[branch]["neg"]]
            entropy = append_entropy_steps(
                steps, f"{feature}_{branch}", branch_counts, 8, info_table
            )
            weight = Fraction(8, TOTAL)
            weighted = weight * entropy
            steps.extend([
                make_step("D", 8, TOTAL, fraction_text(weight)),
                make_step("M", fraction_text(weight), decimal_text(entropy),
                          decimal_text(weighted)),
            ])
            weighted_terms.append(weighted)
        child_entropy = weighted_terms[0] + weighted_terms[1]
        gain = parent_entropy - child_entropy
        steps.extend([
            make_step("A", decimal_text(weighted_terms[0]),
                      decimal_text(weighted_terms[1]),
                      decimal_text(child_entropy)),
            make_step("S", decimal_text(parent_entropy),
                      decimal_text(child_entropy), decimal_text(gain)),
            make_step("INFO_GAIN", feature, decimal_text(gain)),
        ])
        gains[feature] = gain

    first, second = features
    best = first if gains[first] > gains[second] else second
    relation = ">" if best == first else "<"
    steps.append(make_step("CHECK", f"{first} vs {second}",
                           f"{decimal_text(gains[first])} {relation} "
                           f"{decimal_text(gains[second])}",
                           f"choose={best}"))
    answer = (
        f"best={best}; gain_{first}={decimal_text(gains[first])}; "
        f"gain_{second}={decimal_text(gains[second])}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestInformationGainGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = InformationGainGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "information_gain_best_split")
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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

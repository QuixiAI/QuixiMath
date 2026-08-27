import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction
from itertools import permutations

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.derangement_generator import DerangementGenerator
from helpers import DELIM


def derangements(n):
    """Recurrence route (mirrors the generator; used only for step checks)."""
    values = [1, 0]
    for m in range(2, n + 1):
        values.append((m - 1) * (values[m - 1] + values[m - 2]))
    return values[:max(2, n + 1)]


def derangement_inclusion_exclusion(n):
    """Independent route: D_n = sum_i (-1)^i n!/i! (exact integers)."""
    total = 0
    for i in range(n + 1):
        total += (-1) ** i * math.factorial(n) // math.factorial(i)
    return total


def brute_force_fixed_point_counts(n):
    """Brute force: counts[k] = permutations of n with exactly k fixed pts."""
    counts = [0] * (n + 1)
    for perm in permutations(range(n)):
        fixed = sum(1 for i, v in enumerate(perm) if i == v)
        counts[fixed] += 1
    return counts


# ---------------------------------------------------------------- parsing

_LEAD = r"[A-Za-z]+ [a-z\- ]+ at the [a-z\- ]+\. "

_PATTERNS = [
    # recurrence
    (r"How many derangements are there of (?P<n>\d+) distinct [a-z]+\?",
     "recurrence"),
    (r"Tonight (?P<n>\d+) visitors each left one of their [a-z]+, and the "
     r"[a-z]+ are handed back in a random order\. In how many of the orders "
     r"does every visitor get someone else's item\?", "recurrence"),
    (r"Count the permutations of (?P<n>\d+) labelled [a-z]+ in which no item "
     r"stays in its own position\.", "recurrence"),
    (r"A shuffle of the (?P<n>\d+) numbered [a-z]+ is called a derangement "
     r"when no item returns to the slot it came from\. How many derangements "
     r"of the \d+ [a-z]+ are there\?", "recurrence"),
    (r"There are (?P<n>\d+) owners and \d+ matching [a-z]+\. In how many ways "
     r"can the [a-z]+ be returned so that nobody receives their own\?",
     "recurrence"),
    # exactly_k
    (r"The (?P<n>\d+) [a-z]+ are handed back at random\. In how many of the "
     r"orders do exactly (?P<k>\d+) owners get their own item\?", "exactly_k"),
    (r"How many permutations of (?P<n>\d+) labelled [a-z]+ have exactly "
     r"(?P<k>\d+) fixed points\?", "exactly_k"),
    (r"Of all the ways to return (?P<n>\d+) [a-z]+ to their \d+ owners, count "
     r"those in which exactly (?P<k>\d+) of the [a-z]+ reach the right "
     r"owner\.", "exactly_k"),
    (r"A random shuffle of (?P<n>\d+) numbered [a-z]+ is recorded\. How many "
     r"shuffles leave exactly (?P<k>\d+) of the [a-z]+ in their original "
     r"positions\?", "exactly_k"),
    (r"Among the arrangements of (?P<n>\d+) [a-z]+ across \d+ labelled slots, "
     r"how many put exactly (?P<k>\d+) items in their matching slot\?",
     "exactly_k"),
    # at_least_one
    (r"The (?P<n>\d+) [a-z]+ are handed back at random\. In how many of the "
     r"orders does at least one owner get their own item\?", "at_least_one"),
    (r"How many permutations of (?P<n>\d+) labelled [a-z]+ have at least one "
     r"fixed point\?", "at_least_one"),
    (r"Count the ways to return (?P<n>\d+) [a-z]+ to their \d+ owners so that "
     r"the return is not a complete mismatch, that is, at least one owner is "
     r"matched correctly\.", "at_least_one"),
    (r"A shuffle of (?P<n>\d+) numbered [a-z]+ is called lucky when some item "
     r"lands back in its own slot\. How many of the shuffles of the \d+ "
     r"[a-z]+ are lucky\?", "at_least_one"),
    (r"Out of every arrangement of (?P<n>\d+) [a-z]+ in \d+ labelled slots, "
     r"how many have one or more items sitting in their matching slot\?",
     "at_least_one"),
    # probability
    (r"The (?P<n>\d+) [a-z]+ are handed back in a uniformly random order\. "
     r"What is the probability that no owner gets their own item\? Give the "
     r"answer as a fraction in lowest terms\.", "probability"),
    (r"A permutation of (?P<n>\d+) labelled [a-z]+ is chosen uniformly at "
     r"random\. What is the probability that it has no fixed point\? Give the "
     r"answer as a fraction in lowest terms\.", "probability"),
    (r"All arrangements of (?P<n>\d+) [a-z]+ in \d+ labelled slots are "
     r"equally likely\. Find the probability that the arrangement is a "
     r"derangement\. Give the answer as a fraction in lowest terms\.",
     "probability"),
    (r"If the (?P<n>\d+) numbered [a-z]+ are shuffled at random, how likely "
     r"is it that not a single item returns to its own slot\? Give the answer "
     r"as a fraction in lowest terms\.", "probability"),
    (r"A random matching sends the (?P<n>\d+) [a-z]+ back to the \d+ owners\. "
     r"What is the probability that every owner receives the wrong item\? "
     r"Give the answer as a fraction in lowest terms\.", "probability"),
]

_COMPILED = [(re.compile(_LEAD + body), kind) for body, kind in _PATTERNS]


def parse_problem(problem):
    """Parse any phrasing back to (kind, n, k)."""
    for pattern, kind in _COMPILED:
        match = pattern.fullmatch(problem)
        if match is not None:
            groups = match.groupdict()
            k = int(groups["k"]) if groups.get("k") is not None else None
            return kind, int(groups["n"]), k
    raise AssertionError(f"unparsed problem: {problem}")


def oracle_answer(example):
    """Recompute the answer from the problem text by an independent route."""
    kind, n, k = parse_problem(example["problem"])
    if n <= 8:
        counts = brute_force_fixed_point_counts(n)
        deranged = counts[0]
    else:
        counts = None
        deranged = derangement_inclusion_exclusion(n)
    total = math.factorial(n)
    if kind == "recurrence":
        return f"D_{n} = {deranged}"
    if kind == "exactly_k":
        if counts is not None:
            return str(counts[k])
        return str(math.comb(n, k) * derangement_inclusion_exclusion(n - k))
    if kind == "at_least_one":
        if counts is not None:
            return str(total - counts[0])
        return str(total - deranged)
    frac = Fraction(deranged, total)
    return f"{frac.numerator}/{frac.denominator}"


def check_step_arithmetic(example):
    kind, n, k = parse_problem(example["problem"])
    seen_values = {}
    setups = []
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "DERANGE_SETUP":
            setups.append((fields[1], fields[2]))
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "NCR":
            match = re.fullmatch(r"C\((\d+),(\d+)\)", fields[1])
            if match is None:
                return False
            if math.comb(int(match.group(1)), int(match.group(2))) != int(
                    fields[2]):
                return False
        elif op == "FACT":
            if math.factorial(int(fields[1])) != int(fields[2]):
                return False
        elif op == "FACT_FORMULA":
            match = re.fullmatch(r"(\d+)! = ([\d·]+)", fields[1])
            if match is None:
                return False
            product = 1
            for token in match.group(2).split("·"):
                product *= int(token)
            if product != math.factorial(int(match.group(1))):
                return False
        elif op == "GCD":
            match = re.fullmatch(r"gcd\((\d+),(\d+)\)", fields[1])
            if match is None:
                return False
            if math.gcd(int(match.group(1)), int(match.group(2))) != int(
                    fields[2]):
                return False
        elif op == "F":
            num, den = (int(part) for part in fields[1].split("/"))
            frac = Fraction(num, den)
            if fields[2] != f"{frac.numerator}/{frac.denominator}":
                return False
        elif op == "DERANGE_PROB":
            num, den = (int(part) for part in fields[2].split("/"))
            if den != math.factorial(n):
                return False
            if num != derangement_inclusion_exclusion(n):
                return False
        elif op == "COMPLEMENT":
            if fields[2] != f"{n}! - D_{n}":
                return False
        elif op == "DERANGE_VALUE":
            m = int(fields[1][2:])
            seen_values[m] = int(fields[2])
        elif op == "Z":
            if fields[1:] != [example["final_answer"]]:
                return False
    # the recurrence table must be complete and correct for the sub-problem
    target = n - k if kind == "exactly_k" else n
    for m in range(2, target + 1):
        if seen_values.get(m) != derangement_inclusion_exclusion(m):
            return False
    if not setups:
        return False
    if setups[0][0] != f"n = {n}":
        return False
    return True


class TestDerangementGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DerangementGenerator()

    def test_output_contract(self):
        for _ in range(50):
            result = self.gen.generate()
            for key in ("problem_id", "operation", "problem", "steps",
                        "final_answer"):
                self.assertIn(key, result)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                             result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(250):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_brute_force_cross_check_small_n(self):
        """Exhaustive permutation check of every variant for small n."""
        for variant in DerangementGenerator.VARIANTS:
            gen = DerangementGenerator(variant)
            for _ in range(60):
                result = gen.generate()
                kind, n, k = parse_problem(result["problem"])
                self.assertEqual(kind, variant)
                if n > 8:
                    continue
                counts = brute_force_fixed_point_counts(n)
                total = math.factorial(n)
                if variant == "recurrence":
                    expected = f"D_{n} = {counts[0]}"
                elif variant == "exactly_k":
                    expected = str(counts[k])
                elif variant == "at_least_one":
                    expected = str(total - counts[0])
                else:
                    frac = Fraction(counts[0], total)
                    expected = f"{frac.numerator}/{frac.denominator}"
                self.assertEqual(result["final_answer"], expected,
                                 result["problem"])

    def test_recurrence_matches_inclusion_exclusion(self):
        for n in range(2, 16):
            self.assertEqual(derangements(n)[n],
                             derangement_inclusion_exclusion(n))

    def test_all_variants_and_operations(self):
        expected_ops = {
            "recurrence": "derangement_recurrence",
            "exactly_k": "derangement_exactly_k",
            "at_least_one": "derangement_at_least_one",
            "probability": "derangement_probability",
        }
        for variant, operation in expected_ops.items():
            gen = DerangementGenerator(variant)
            for _ in range(20):
                result = gen.generate()
                self.assertEqual(result["operation"], operation)
        seen = set()
        for _ in range(400):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(seen, set(expected_ops.values()))

    def test_fixed_variant_constructor(self):
        gen = DerangementGenerator("recurrence")
        result = gen.generate()
        self.assertEqual(result["operation"], "derangement_recurrence")
        with self.assertRaises(ValueError):
            DerangementGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
                for field in raw_step.split(DELIM)[1:]:
                    self.assertNotIn(DELIM, field)

    def test_all_phrasings_parse(self):
        seen = set()
        for _ in range(1200):
            result = self.gen.generate()
            problem = result["problem"]
            for index, (pattern, kind) in enumerate(_COMPILED):
                if pattern.fullmatch(problem):
                    seen.add((kind, index))
                    break
            else:
                self.fail(f"unparsed problem: {problem}")
        self.assertEqual(len(seen), len(_COMPILED))

    def test_capacity_is_wide(self):
        texts = {self.gen.generate()["problem"] for _ in range(800)}
        self.assertGreaterEqual(len(texts), 790)


if __name__ == "__main__":
    unittest.main()

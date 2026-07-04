import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.algorithm_trace_generator import AlgorithmTraceGenerator
from helpers import DELIM


BINARY_RE = re.compile(
    r"Trace binary search on sorted values ([\d, ]+) for target (\d+) for "
    r"(\d+) iterations using 0-based indices\. What is the state after "
    r"those iterations\?"
)
INSERTION_RE = re.compile(
    r"Trace insertion sort on values ([\d, ]+) for (\d+) passes\. "
    r"What is the array after those passes\?"
)
MERGE_RE = re.compile(
    r"Trace top-down merge sort on values ([\d, ]+) for (\d+) merge "
    r"operations\. What is the array after those merges\?"
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def list_text(values):
    return ", ".join(str(value) for value in values)


def array_answer(values):
    return "[" + list_text(values) + "]"


def parse_values(text):
    return [int(value) for value in text.split(", ")]


def parse_problem(problem):
    match = BINARY_RE.fullmatch(problem)
    if match:
        values_text, target, iterations = match.groups()
        return {"variant": "binary_search", "values": parse_values(values_text),
                "target": int(target), "iterations": int(iterations)}

    match = INSERTION_RE.fullmatch(problem)
    if match:
        values_text, passes = match.groups()
        return {"variant": "insertion_sort",
                "values": parse_values(values_text), "passes": int(passes)}

    match = MERGE_RE.fullmatch(problem)
    assert match is not None, problem
    values_text, merges = match.groups()
    return {"variant": "merge_sort", "values": parse_values(values_text),
            "merges": int(merges)}


def binary_expected(parts):
    values = parts["values"]
    target = parts["target"]
    iterations = parts["iterations"]
    steps = [
        make_step("ALG_SETUP", "binary search", f"target {target}",
                  f"values {list_text(values)}"),
    ]
    lo = 0
    hi = len(values) - 1
    found_index = None
    for iteration in range(1, iterations + 1):
        if lo > hi or found_index is not None:
            break
        steps.append(make_step("SEARCH_BOUNDS", f"iter {iteration}",
                               f"lo={lo}", f"hi={hi}"))
        total = lo + hi
        mid = total // 2
        steps.append(make_step("A", lo, hi, total))
        steps.append(make_step("FLOOR_DIV", total, 2, mid))
        steps.append(make_step("MIDPOINT", f"iter {iteration}", mid))
        if values[mid] == target:
            found_index = mid
            steps.append(make_step("COMPARE", f"values[{mid}]={values[mid]}",
                                   f"target {target}", "equal"))
            steps.append(make_step("SEARCH_STATE", "found", f"index {mid}"))
        elif values[mid] < target:
            steps.append(make_step("COMPARE", f"values[{mid}]={values[mid]}",
                                   f"target {target}", "less"))
            lo = mid + 1
            steps.append(make_step("SEARCH_STATE", f"lo={lo}", f"hi={hi}"))
        else:
            steps.append(make_step("COMPARE", f"values[{mid}]={values[mid]}",
                                   f"target {target}", "greater"))
            hi = mid - 1
            steps.append(make_step("SEARCH_STATE", f"lo={lo}", f"hi={hi}"))

    if found_index is not None:
        answer = f"found {target} at index {found_index}"
    elif lo > hi:
        answer = f"not found; insertion point = {lo}"
    else:
        answer = f"lo={lo}, hi={hi}, status=searching"
    return steps, answer


def insertion_expected(parts):
    values = parts["values"]
    passes = parts["passes"]
    arr = list(values)
    steps = [
        make_step("ALG_SETUP", "insertion sort", f"passes {passes}",
                  f"values {list_text(values)}"),
    ]
    for pass_num in range(1, passes + 1):
        key = arr[pass_num]
        j = pass_num - 1
        steps.append(make_step("INSERT_KEY", f"pass {pass_num}", key,
                               f"index {pass_num}"))
        while j >= 0 and arr[j] > key:
            steps.append(make_step("COMPARE", f"arr[{j}]={arr[j]}",
                                   f"key {key}", "shift"))
            arr[j + 1] = arr[j]
            steps.append(make_step("SHIFT", f"{j}->{j + 1}", list_text(arr)))
            j -= 1
        if j >= 0:
            steps.append(make_step("COMPARE", f"arr[{j}]={arr[j]}",
                                   f"key {key}", "stop"))
        arr[j + 1] = key
        steps.append(make_step("INSERT_PLACE", f"index {j + 1}",
                               list_text(arr)))
        steps.append(make_step("ARRAY_STATE", f"pass {pass_num}",
                               list_text(arr)))
    return steps, f"array = {array_answer(arr)}"


def merge_expected(parts):
    values = parts["values"]
    merges = parts["merges"]
    arr = list(values)
    steps = [
        make_step("ALG_SETUP", "merge sort", f"merges {merges}",
                  f"values {list_text(values)}"),
    ]
    merge_count = 0

    def sort_range(lo, hi):
        nonlocal merge_count
        if hi - lo <= 1 or merge_count >= merges:
            return
        mid = (lo + hi) // 2
        sort_range(lo, mid)
        if merge_count >= merges:
            return
        sort_range(mid, hi)
        if merge_count >= merges:
            return

        left = arr[lo:mid]
        right = arr[mid:hi]
        merge_no = merge_count + 1
        steps.append(make_step("MERGE_BEGIN", f"merge {merge_no}",
                               f"lo={lo},mid={mid},hi={hi}",
                               f"left {list_text(left)}; right {list_text(right)}"))
        i = 0
        j = 0
        merged = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                steps.append(make_step("MERGE_COMPARE", left[i], right[j],
                                       "take left"))
                merged.append(left[i])
                steps.append(make_step("MERGE_TAKE", left[i],
                                       f"merged {list_text(merged)}"))
                i += 1
            else:
                steps.append(make_step("MERGE_COMPARE", left[i], right[j],
                                       "take right"))
                merged.append(right[j])
                steps.append(make_step("MERGE_TAKE", right[j],
                                       f"merged {list_text(merged)}"))
                j += 1
        while i < len(left):
            merged.append(left[i])
            steps.append(make_step("MERGE_TAKE", left[i],
                                   f"merged {list_text(merged)}"))
            i += 1
        while j < len(right):
            merged.append(right[j])
            steps.append(make_step("MERGE_TAKE", right[j],
                                   f"merged {list_text(merged)}"))
            j += 1
        arr[lo:hi] = merged
        merge_count += 1
        steps.append(make_step("MERGE_DONE", f"merge {merge_count}",
                               f"range {lo}-{hi - 1}",
                               f"array {list_text(arr)}"))

    sort_range(0, len(arr))
    return steps, f"array = {array_answer(arr)}"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "binary_search":
        steps, answer = binary_expected(parts)
    elif parts["variant"] == "insertion_sort":
        steps, answer = insertion_expected(parts)
    else:
        steps, answer = merge_expected(parts)
    return steps + [make_step("Z", answer)], answer


class TestAlgorithmTraceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = AlgorithmTraceGenerator()

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
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "FLOOR_DIV":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("binary_search", "insertion_sort", "merge_sort"):
            gen = AlgorithmTraceGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"algorithm_trace_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            AlgorithmTraceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()

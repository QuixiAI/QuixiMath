import random

from base_generator import ProblemGenerator
from helpers import step, jid


def list_text(values):
    return ", ".join(str(value) for value in values)


def array_answer(values):
    return "[" + list_text(values) + "]"


class AlgorithmTraceGenerator(ProblemGenerator):
    """
    Deterministic algorithm state traces after a fixed number of steps.

    Variants:
    - binary_search: state after k iterations
    - insertion_sort: array after k outer passes
    - merge_sort: array after k top-down merge operations

    Op-codes used:
    - ALG_SETUP: algorithm, input, and stop condition
    - SEARCH_BOUNDS / MIDPOINT / SEARCH_STATE: binary-search trace
    - INSERT_KEY / SHIFT / INSERT_PLACE / ARRAY_STATE: insertion-sort trace
    - MERGE_BEGIN / MERGE_COMPARE / MERGE_TAKE / MERGE_DONE: merge-sort trace
    - COMPARE / A / FLOOR_DIV (established or descriptive arithmetic)
    - Z: requested state after the trace
    """

    VARIANTS = ["binary_search", "insertion_sort", "merge_sort"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "binary_search":
            problem, steps, answer = self._generate_binary_search()
        elif variant == "insertion_sort":
            problem, steps, answer = self._generate_insertion_sort()
        else:
            problem, steps, answer = self._generate_merge_sort()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"algorithm_trace_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_binary_search(self):
        size = random.randint(6, 8)
        values = sorted(random.sample(range(2, 50), size))
        if random.random() < 0.7:
            target = random.choice(values)
        else:
            candidates = [value for value in range(2, 50) if value not in values]
            target = random.choice(candidates)
        iterations = random.randint(1, 4)
        steps = [
            step("ALG_SETUP", "binary search", f"target {target}",
                 f"values {list_text(values)}"),
        ]

        lo = 0
        hi = len(values) - 1
        found_index = None
        for iteration in range(1, iterations + 1):
            if lo > hi or found_index is not None:
                break
            steps.append(step("SEARCH_BOUNDS", f"iter {iteration}",
                              f"lo={lo}", f"hi={hi}"))
            total = lo + hi
            mid = total // 2
            steps.append(step("A", lo, hi, total))
            steps.append(step("FLOOR_DIV", total, 2, mid))
            steps.append(step("MIDPOINT", f"iter {iteration}", mid))
            if values[mid] == target:
                found_index = mid
                steps.append(step("COMPARE", f"values[{mid}]={values[mid]}",
                                  f"target {target}", "equal"))
                steps.append(step("SEARCH_STATE", "found", f"index {mid}"))
            elif values[mid] < target:
                steps.append(step("COMPARE", f"values[{mid}]={values[mid]}",
                                  f"target {target}", "less"))
                lo = mid + 1
                steps.append(step("SEARCH_STATE", f"lo={lo}", f"hi={hi}"))
            else:
                steps.append(step("COMPARE", f"values[{mid}]={values[mid]}",
                                  f"target {target}", "greater"))
                hi = mid - 1
                steps.append(step("SEARCH_STATE", f"lo={lo}", f"hi={hi}"))

        if found_index is not None:
            answer = f"found {target} at index {found_index}"
        elif lo > hi:
            answer = f"not found; insertion point = {lo}"
        else:
            answer = f"lo={lo}, hi={hi}, status=searching"
        problem = (
            f"Trace binary search on sorted values {list_text(values)} for "
            f"target {target} for {iterations} iterations using 0-based "
            f"indices. What is the state after those iterations?"
        )
        return problem, steps, answer

    def _generate_insertion_sort(self):
        size = random.randint(5, 7)
        values = random.sample(range(1, 40), size)
        passes = random.randint(1, size - 1)
        arr = list(values)
        steps = [
            step("ALG_SETUP", "insertion sort", f"passes {passes}",
                 f"values {list_text(values)}"),
        ]

        for pass_num in range(1, passes + 1):
            key = arr[pass_num]
            j = pass_num - 1
            steps.append(step("INSERT_KEY", f"pass {pass_num}", key,
                              f"index {pass_num}"))
            while j >= 0 and arr[j] > key:
                steps.append(step("COMPARE", f"arr[{j}]={arr[j]}",
                                  f"key {key}", "shift"))
                arr[j + 1] = arr[j]
                steps.append(step("SHIFT", f"{j}->{j + 1}", list_text(arr)))
                j -= 1
            if j >= 0:
                steps.append(step("COMPARE", f"arr[{j}]={arr[j]}",
                                  f"key {key}", "stop"))
            arr[j + 1] = key
            steps.append(step("INSERT_PLACE", f"index {j + 1}", list_text(arr)))
            steps.append(step("ARRAY_STATE", f"pass {pass_num}",
                              list_text(arr)))

        answer = f"array = {array_answer(arr)}"
        problem = (
            f"Trace insertion sort on values {list_text(values)} for {passes} "
            f"passes. What is the array after those passes?"
        )
        return problem, steps, answer

    def _generate_merge_sort(self):
        size = random.randint(5, 7)
        values = random.sample(range(1, 50), size)
        merges = random.randint(1, size - 1)
        arr = list(values)
        steps = [
            step("ALG_SETUP", "merge sort", f"merges {merges}",
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
            steps.append(step("MERGE_BEGIN", f"merge {merge_no}",
                              f"lo={lo},mid={mid},hi={hi}",
                              f"left {list_text(left)}; right {list_text(right)}"))
            i = 0
            j = 0
            merged = []
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    steps.append(step("MERGE_COMPARE", left[i], right[j],
                                      "take left"))
                    merged.append(left[i])
                    steps.append(step("MERGE_TAKE", left[i],
                                      f"merged {list_text(merged)}"))
                    i += 1
                else:
                    steps.append(step("MERGE_COMPARE", left[i], right[j],
                                      "take right"))
                    merged.append(right[j])
                    steps.append(step("MERGE_TAKE", right[j],
                                      f"merged {list_text(merged)}"))
                    j += 1
            while i < len(left):
                merged.append(left[i])
                steps.append(step("MERGE_TAKE", left[i],
                                  f"merged {list_text(merged)}"))
                i += 1
            while j < len(right):
                merged.append(right[j])
                steps.append(step("MERGE_TAKE", right[j],
                                  f"merged {list_text(merged)}"))
                j += 1
            arr[lo:hi] = merged
            merge_count += 1
            steps.append(step("MERGE_DONE", f"merge {merge_count}",
                              f"range {lo}-{hi - 1}",
                              f"array {list_text(arr)}"))

        sort_range(0, len(arr))
        answer = f"array = {array_answer(arr)}"
        problem = (
            f"Trace top-down merge sort on values {list_text(values)} for "
            f"{merges} merge operations. What is the array after those "
            f"merges?"
        )
        return problem, steps, answer

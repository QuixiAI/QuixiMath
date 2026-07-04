import random
from base_generator import ProblemGenerator
from helpers import step, jid


class SimpleStatsGenerator(ProblemGenerator):
    """Computes mean, median, and mode for small integer datasets.

    Mean datasets are constructed with the sum divisible by the count so
    the answer is an exact integer (hand-friendly); an even-count median
    is an integer or ends in .5 — never a rounded float.
    """

    def generate(self) -> dict:
        target = random.choice(["mean", "median", "mode"])
        size = random.randint(5, 9)
        data = [random.randint(1, 20) for _ in range(size)]
        if target == "mean":
            # Redraw until the sum divides evenly: exact integer mean
            while sum(data) % size:
                data = [random.randint(1, 20) for _ in range(size)]
        steps = []

        # Sort for median/mode clarity
        sorted_data = sorted(data)
        steps.append(step("SORT", ",".join(map(str, data)), ",".join(map(str, sorted_data))))

        if target == "mean":
            total = 0
            for val in sorted_data:
                new_total = total + val
                steps.append(step("A", total, val, new_total))
                total = new_total
            mean_value = total // len(sorted_data)
            steps.append(step("MEAN_DIV", total, len(sorted_data), mean_value))
            final_answer = str(mean_value)
            operation = "mean"
            problem = f"Find mean of {sorted_data}"

        elif target == "median":
            n = len(sorted_data)
            mid = n // 2
            if n % 2 == 1:
                median = sorted_data[mid]
                steps.append(step("MEDIAN_PICK", sorted_data[mid], "", median))
            else:
                pair = (sorted_data[mid - 1], sorted_data[mid])
                steps.append(step("MEDIAN_PAIR", pair[0], pair[1]))
                pair_sum = pair[0] + pair[1]
                # Exact: integer when the sum is even, else n.5
                median = pair_sum // 2 if pair_sum % 2 == 0 else f"{pair_sum // 2}.5"
                steps.append(step("MEAN_DIV", pair_sum, 2, median))
            final_answer = str(median)
            operation = "median"
            problem = f"Find median of {sorted_data}"

        else:  # mode
            freq = {}
            for val in sorted_data:
                freq[val] = freq.get(val, 0) + 1
                steps.append(step("MODE_COUNT", val, freq[val]))
            max_freq = max(freq.values())
            modes = [k for k, v in freq.items() if v == max_freq]
            final_answer = ", ".join(map(str, modes))
            steps.append(step("MODE", max_freq, final_answer))
            operation = "mode"
            problem = f"Find mode of {sorted_data}"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

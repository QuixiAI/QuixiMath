import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kmeans_step_generator import KMeansStepGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Run one k-means iteration with points (.+) and starting centroids "
    r"(.+)\. Use squared Euclidean distance for assignment, then update "
    r"each centroid to its cluster mean\."
)
POINT_RE = re.compile(r"P(\d+)=\(([^,]+),([^)]+)\)")
CENTROID_RE = re.compile(r"C(\d+)=\(([^,]+),([^)]+)\)")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def point_text(point):
    return f"({fraction_text(point[0])},{fraction_text(point[1])})"


def points_text(points):
    return ", ".join(
        f"P{index}={point_text(point)}"
        for index, point in enumerate(points, start=1)
    )


def centroids_text(centroids):
    return ", ".join(
        f"C{index}={point_text(point)}"
        for index, point in enumerate(centroids, start=1)
    )


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    points = [
        (Fraction(x), Fraction(y))
        for _, x, y in POINT_RE.findall(match.group(1))
    ]
    centroids = [
        (Fraction(x), Fraction(y))
        for _, x, y in CENTROID_RE.findall(match.group(2))
    ]
    return points, centroids


def squared_distance(point, centroid):
    dx = point[0] - centroid[0]
    dy = point[1] - centroid[1]
    return dx * dx + dy * dy


def expected_flow(example):
    points, centroids = parse_problem(example["problem"])
    steps = [
        make_step("KMEANS_SETUP", f"points={points_text(points)}",
                  f"centroids={centroids_text(centroids)}"),
    ]
    assignments = []
    for index, point in enumerate(points, start=1):
        distances = []
        for centroid_index, centroid in enumerate(centroids, start=1):
            dx = point[0] - centroid[0]
            dy = point[1] - centroid[1]
            dx2 = dx ** 2
            dy2 = dy ** 2
            dist2 = dx2 + dy2
            steps.extend([
                make_step("S", fraction_text(point[0]),
                          fraction_text(centroid[0]), fraction_text(dx)),
                make_step("E", fraction_text(dx), 2, fraction_text(dx2)),
                make_step("S", fraction_text(point[1]),
                          fraction_text(centroid[1]), fraction_text(dy)),
                make_step("E", fraction_text(dy), 2, fraction_text(dy2)),
                make_step("A", fraction_text(dx2), fraction_text(dy2),
                          fraction_text(dist2)),
                make_step("DIST2", f"P{index}", f"C{centroid_index}",
                          fraction_text(dist2)),
            ])
            distances.append(dist2)
        assigned = 0 if distances[0] < distances[1] else 1
        assignments.append(assigned)
        relation = "<" if assigned == 0 else ">"
        steps.extend([
            make_step("CHECK", f"P{index}",
                      f"d2(C1)={fraction_text(distances[0])} {relation} "
                      f"d2(C2)={fraction_text(distances[1])}",
                      f"assign=C{assigned + 1}"),
            make_step("ASSIGN", f"P{index}", f"C{assigned + 1}"),
        ])

    new_centroids = []
    for cluster_index in (0, 1):
        member_indices = [
            idx for idx, assignment in enumerate(assignments)
            if assignment == cluster_index
        ]
        members = [points[idx] for idx in member_indices]
        member_names = ",".join(f"P{idx + 1}" for idx in member_indices)
        steps.append(make_step("CLUSTER_MEMBERS", f"C{cluster_index + 1}",
                               member_names))
        sum_x = Fraction(0)
        sum_y = Fraction(0)
        for point in members:
            new_sum_x = sum_x + point[0]
            new_sum_y = sum_y + point[1]
            steps.append(make_step("A", fraction_text(sum_x),
                                   fraction_text(point[0]),
                                   fraction_text(new_sum_x)))
            steps.append(make_step("A", fraction_text(sum_y),
                                   fraction_text(point[1]),
                                   fraction_text(new_sum_y)))
            sum_x, sum_y = new_sum_x, new_sum_y
        count = len(members)
        mean_x = sum_x / count
        mean_y = sum_y / count
        steps.extend([
            make_step("D", fraction_text(sum_x), count, fraction_text(mean_x)),
            make_step("D", fraction_text(sum_y), count, fraction_text(mean_y)),
            make_step("CENTROID_UPDATE", f"C{cluster_index + 1}",
                      point_text((mean_x, mean_y))),
        ])
        new_centroids.append((mean_x, mean_y))

    assignment_text = ",".join(
        f"P{index}:C{assignment + 1}"
        for index, assignment in enumerate(assignments, start=1)
    )
    answer = (
        f"assignments={assignment_text}; "
        f"C1_new={point_text(new_centroids[0])}; "
        f"C2_new={point_text(new_centroids[1])}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestKMeansStepGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KMeansStepGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "kmeans_one_iteration")
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
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

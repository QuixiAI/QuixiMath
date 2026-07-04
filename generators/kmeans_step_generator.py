import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


POINT_COUNT = 4


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


def squared_distance(point, centroid):
    dx = point[0] - centroid[0]
    dy = point[1] - centroid[1]
    return dx * dx + dy * dy


def assign_points(points, centroids):
    assignments = []
    for point in points:
        distances = [squared_distance(point, centroid) for centroid in centroids]
        if distances[0] == distances[1]:
            return None
        assignments.append(0 if distances[0] < distances[1] else 1)
    if 0 not in assignments or 1 not in assignments:
        return None
    return assignments


def mean_point(points):
    count = len(points)
    return (
        sum(point[0] for point in points) / count,
        sum(point[1] for point in points) / count,
    )


class KMeansStepGenerator(ProblemGenerator):
    """
    One complete k-means assignment/update iteration for two 2D centroids.

    Four points are assigned by squared Euclidean distance, then each centroid
    is updated to the exact mean of its assigned cluster.

    Op-codes used:
    - KMEANS_SETUP / DIST2 / ASSIGN / CLUSTER_MEMBERS / CENTROID_UPDATE
    - CHECK (established): compare squared distances
    - S / E / A / D (established/shared): distance and mean arithmetic
    - Z: assignments and updated centroids
    """

    def generate(self) -> dict:
        grid = [(x, y) for x in range(-5, 6) for y in range(-5, 6)]
        for _ in range(100):
            points = random.sample(grid, POINT_COUNT)
            centroids = random.sample(grid, 2)
            assignments = assign_points(points, centroids)
            if assignments is not None:
                break
        else:
            points = [(-4, -3), (-3, -2), (3, 2), (4, 3)]
            centroids = [(-5, -5), (5, 5)]
            assignments = assign_points(points, centroids)

        steps = [
            step("KMEANS_SETUP", f"points={points_text(points)}",
                 f"centroids={centroids_text(centroids)}"),
        ]

        for index, point in enumerate(points, start=1):
            distances = []
            for centroid_index, centroid in enumerate(centroids, start=1):
                dx = point[0] - centroid[0]
                dy = point[1] - centroid[1]
                dx2 = dx ** 2
                dy2 = dy ** 2
                dist2 = dx2 + dy2
                steps.extend([
                    step("S", point[0], centroid[0], dx),
                    step("E", dx, 2, dx2),
                    step("S", point[1], centroid[1], dy),
                    step("E", dy, 2, dy2),
                    step("A", dx2, dy2, dist2),
                    step("DIST2", f"P{index}", f"C{centroid_index}",
                         dist2),
                ])
                distances.append(dist2)
            assigned = assignments[index - 1] + 1
            relation = "<" if assigned == 1 else ">"
            steps.extend([
                step("CHECK", f"P{index}",
                     f"d2(C1)={distances[0]} {relation} d2(C2)={distances[1]}",
                     f"assign=C{assigned}"),
                step("ASSIGN", f"P{index}", f"C{assigned}"),
            ])

        new_centroids = []
        for cluster_index in (0, 1):
            member_indices = [
                idx for idx, assignment in enumerate(assignments)
                if assignment == cluster_index
            ]
            members = [points[idx] for idx in member_indices]
            member_names = ",".join(f"P{idx + 1}" for idx in member_indices)
            steps.append(step("CLUSTER_MEMBERS", f"C{cluster_index + 1}",
                              member_names))
            sum_x = Fraction(0)
            sum_y = Fraction(0)
            for point in members:
                new_sum_x = sum_x + point[0]
                new_sum_y = sum_y + point[1]
                steps.append(step("A", fraction_text(sum_x), point[0],
                                  fraction_text(new_sum_x)))
                steps.append(step("A", fraction_text(sum_y), point[1],
                                  fraction_text(new_sum_y)))
                sum_x, sum_y = new_sum_x, new_sum_y
            count = len(members)
            mean_x = sum_x / count
            mean_y = sum_y / count
            steps.extend([
                step("D", fraction_text(sum_x), count, fraction_text(mean_x)),
                step("D", fraction_text(sum_y), count, fraction_text(mean_y)),
                step("CENTROID_UPDATE", f"C{cluster_index + 1}",
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
        steps.append(step("Z", answer))
        problem = (
            f"Run one k-means iteration with points {points_text(points)} and "
            f"starting centroids {centroids_text(centroids)}. Use squared "
            "Euclidean distance for assignment, then update each centroid to "
            "its cluster mean."
        )
        return dict(
            problem_id=jid(),
            operation="kmeans_one_iteration",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

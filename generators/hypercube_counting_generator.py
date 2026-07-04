import math
import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.geometric_mean_generator import sqrt_txt


def wrap(n):
    return f"({n})" if n < 0 else str(n)


class HypercubeCountingGenerator(ProblemGenerator):
    """
    Counting the pieces of an n-cube and measuring in R^4.

    Variants:
    - count:      k-faces of the n-cube via C(n,k)·2^(n-k)
                  (vertices, edges, square faces, cubic cells)
    - distance4d: distance between two integer points in R^4 - four
                  squared differences instead of two
    - diagonal:   main diagonal of an n-cube with side s is s√n; for
                  n = 4 it is exactly 2s, a genuinely 4-dimensional
                  surprise with integer arithmetic

    Op-codes used:
    - HYPERCUBE_SETUP: the object and the goal (object, goal)
    - HYPERCUBE_FORMULA: the counting or diagonal formula
    - NCR: a binomial coefficient (expression, value)
    - E / M / S / A: the arithmetic (established)
    - DIST_FORMULA: extended to four coordinates (established)
    - ROOT_SIMPLIFY: for radical answers (established)
    - Z: final answer
    """

    VARIANTS = ["count", "distance4d", "diagonal"]
    PIECES = {0: "vertices", 1: "edges", 2: "square faces",
              3: "cubic cells"}

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "count":
            n = random.randint(3, 6)
            k = random.randint(0, min(3, n - 1))
            count = math.comb(n, k) * 2 ** (n - k)
            steps = [
                step("HYPERCUBE_SETUP", f"{n}-cube",
                     f"number of {self.PIECES[k]} (k = {k})"),
                step("HYPERCUBE_FORMULA",
                     "k-faces of the n-cube: C(n,k) · 2^(n-k)"),
                step("NCR", f"C({n},{k})", math.comb(n, k)),
                step("E", 2, n - k, 2 ** (n - k)),
                step("M", math.comb(n, k), 2 ** (n - k), count),
                step("Z", count),
            ]
            problem = (f"How many {self.PIECES[k]} does a "
                       f"{n}-dimensional hypercube have?")
            answer = str(count)
        elif variant == "distance4d":
            p = [random.randint(-5, 5) for _ in range(4)]
            q = [random.randint(-5, 5) for _ in range(4)]
            if p == q:
                return self.generate()
            ds = [q[i] - p[i] for i in range(4)]
            sqs = [d * d for d in ds]
            total = sum(sqs)
            steps = [
                step("HYPERCUBE_SETUP",
                     f"points P({', '.join(map(str, p))}) and "
                     f"Q({', '.join(map(str, q))}) in R^4", "distance"),
                step("DIST_FORMULA",
                     "d = √(Σ (q_i - p_i)^2), four coordinates"),
            ]
            for i in range(4):
                steps.append(step("S", q[i], p[i], ds[i]))
                steps.append(step("E", wrap(ds[i]), 2, sqs[i]))
            acc = sqs[0]
            for v in sqs[1:]:
                steps.append(step("A", acc, v, acc + v))
                acc += v
            val = sqrt_txt(total)
            if "√" in val:
                steps.append(step("ROOT_SIMPLIFY", f"√{total} = {val}"))
            else:
                steps.append(step("E", val, 2, total))
            answer = f"d = {val}"
            steps.append(step("Z", answer))
            problem = (f"Find the distance between "
                       f"P({', '.join(map(str, p))}) and "
                       f"Q({', '.join(map(str, q))}) in 4-dimensional "
                       f"space.")
        else:
            n = random.choice([2, 3, 4, 4, 5])
            s = random.randint(2, 9)
            steps = [
                step("HYPERCUBE_SETUP", f"{n}-cube with side {s}",
                     "main diagonal"),
                step("HYPERCUBE_FORMULA", "diagonal = s·√n"),
            ]
            root = sqrt_txt(n)
            if "√" not in root:
                steps.append(step("E", root, 2, n))
                steps.append(step("M", s, int(root), s * int(root)))
                answer = str(s * int(root))
            else:
                answer = f"{s}√{n}"
            steps.append(step("Z", answer))
            problem = (f"Find the length of the main diagonal of a "
                       f"{n}-dimensional cube with side length {s}. "
                       f"Give an exact answer.")

        return dict(
            problem_id=jid(),
            operation=f"hypercube_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

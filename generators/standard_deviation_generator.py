import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.geometric_mean_generator import sqrt_txt

# Deviation patterns (sum 0) whose population variance is an integer,
# for the standard-deviation variant.
STD_PATTERNS = {
    4: [(-3, -1, 1, 3), (-2, -2, 2, 2), (-1, -1, 1, 1),
        (-4, -2, 2, 4), (-3, -3, 3, 3)],
    5: [(-3, -1, 0, 1, 3), (-4, -2, 0, 2, 4)],
    6: [(-2, -2, -2, 2, 2, 2), (-4, -1, -1, 1, 1, 4),
        (-3, -3, -3, 3, 3, 3)],
}


class StandardDeviationGenerator(ProblemGenerator):
    """
    Variance and standard deviation by hand with the classic
    deviation table: mean first, one DEV_ROW per value with x,
    x - mean, and (x - mean)^2, then the sum of squares divided by
    n (population) or n - 1 (sample). Data are built from integer
    deviations that sum to zero, so the mean is always an integer.

    Variants:
    - population_variance: SS/n
    - sample_variance: SS/(n - 1), exact fraction if it does not
      divide evenly
    - population_std: patterns with integer variance; exact radical
      via sqrt_txt when the variance is not a perfect square

    Op-codes used:
    - A / MEAN_DIV (established, simple_stats) for the mean
    - DEV_ROW: x, x - mean, (x - mean)^2 — one table row
    - EVAL / D (established)
    - Z: the exact variance or standard deviation
    """

    VARIANTS = ["population_variance", "sample_variance",
                "population_std"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        n = random.choice([4, 5, 6])
        if variant == "population_std":
            devs = list(random.choice(STD_PATTERNS[n]))
        else:
            while True:
                devs = [random.randint(-6, 6) for _ in range(n - 1)]
                last = -sum(devs)
                if abs(last) <= 8 and (any(devs) or last != 0):
                    devs.append(last)
                    break
        mean = random.randint(10, 30)
        data = [mean + d for d in devs]
        random.shuffle(data)
        ss = sum(d * d for d in devs)
        raw = ", ".join(map(str, data))

        steps = []
        total = data[0]
        for v in data[1:]:
            steps.append(step("A", total, v, total + v))
            total += v
        steps.append(step("MEAN_DIV", total, n, mean))
        for v in data:
            steps.append(step("DEV_ROW", v, v - mean,
                              (v - mean) ** 2))
        sq = [(v - mean) ** 2 for v in data]
        run = sq[0]
        for v in sq[1:]:
            steps.append(step("A", run, v, run + v))
            run += v

        if variant == "population_variance":
            var = Fraction(ss, n)
            steps.append(step("D", ss, n, str(var)))
            answer = str(var)
            problem = (f"Find the population variance of the data "
                       f"set: {raw}. Give an exact answer.")
        elif variant == "sample_variance":
            var = Fraction(ss, n - 1)
            steps.append(step("EVAL", "n - 1", n - 1))
            steps.append(step("D", ss, n - 1, str(var)))
            answer = str(var)
            problem = (f"Find the sample variance of the data set: "
                       f"{raw}. Give an exact answer.")
        else:
            var = ss // n
            steps.append(step("D", ss, n, var))
            answer = sqrt_txt(var)
            steps.append(step("EVAL", f"σ = √{var}", answer))
            problem = (f"Find the population standard deviation of "
                       f"the data set: {raw}. Give an exact answer.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"standard_deviation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

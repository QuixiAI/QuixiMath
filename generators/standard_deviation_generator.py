import hashlib
import random
from collections import Counter
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.geometric_mean_generator import sqrt_txt
from stats_common import (num_txt, patterns, running_sum_steps,
                          sample_from_pattern, sqrt_fraction)


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
NEW_QUERIES = {
    "sample_std": (
        "Find the exact sample standard deviation.",
        "Use divisor n - 1 and report the sample sd.",
        "Build the deviation table and calculate s exactly.",
        "What sample standard deviation does this data set have?",
    ),
    "shortcut_formula": (
        "Use the stated shortcut formula to find the population variance.",
        "Calculate σ² from Σx²/n - x̄² and verify it by deviations.",
        "Find the exact population variance by the computational formula.",
        "Apply the shortcut identity, then check the deviation route.",
    ),
    "from_frequency_table": (
        "Find the exact population standard deviation from the frequency table.",
        "Use the frequencies as weights to calculate σ.",
        "Expand the weighted deviation calculation and report the population sd.",
        "What population standard deviation is represented by this table?",
    ),
    "coefficient_of_variation": (
        "Find the coefficient of variation.",
        "Divide σ by μ and convert the result to a percent.",
        "Use the stated CV rule to report relative spread.",
        "What percent coefficient of variation do these summaries give?",
    ),
}
LEGACY_VARIANTS = ("population_variance", "sample_variance", "population_std")
EXTENSION_VARIANTS = tuple(NEW_QUERIES)

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
    - sample_std: sample-square patterns, so s is exact
    - shortcut_formula: σ² = Σx²/n - x̄², checked by deviations
    - from_frequency_table: weighted population standard deviation
    - coefficient_of_variation: CV = σ/μ × 100%

    Op-codes used:
    - A / MEAN_DIV (established, simple_stats) for the mean
    - DEV_ROW: x, x - mean, (x - mean)^2 — one table row
    - EVAL / D (established)
    - FREQ_SETUP / WEIGHT_ROW / CV_FORMULA / DEC_TO_PERCENT (established)
    - Z: the exact variance or standard deviation
    """

    VARIANTS = ["population_variance", "sample_variance",
                "population_std", "sample_std", "shortcut_formula",
                "from_frequency_table", "coefficient_of_variation"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _site():
        return (f"{random.choice(LOCATIONS)} during the "
                f"{random.choice(SETTINGS)}")

    @staticmethod
    def _new_result(variant, prefix, steps, answer):
        problem = f"{prefix}\n{random.choice(NEW_QUERIES[variant])}"
        steps.append(step("Z", answer))
        return dict(problem_id=jid(),
                    operation=f"standard_deviation_{variant}",
                    problem=problem, steps=steps, final_answer=answer)

    @staticmethod
    def _deviation_steps(data, mean, setup):
        total_steps, total = running_sum_steps(data)
        steps = [step("STAT_SETUP", setup, f"n={len(data)}"), *total_steps,
                 step("MEAN_DIV", total, len(data), num_txt(mean))]
        squares = []
        for value in data:
            deviation = Fraction(value) - mean
            square = deviation * deviation
            squares.append(square)
            steps.append(step("DEV_ROW", num_txt(value), num_txt(deviation),
                              num_txt(square)))
        square_steps, ss = running_sum_steps(squares)
        steps.extend(square_steps)
        steps.append(step("SUM", "squared deviations", num_txt(ss)))
        return steps, ss

    @classmethod
    def _sample_std(cls):
        n = random.randint(4, 8)
        pattern = random.choice(patterns(n, sample_square=True, max_abs=8))
        scale = random.randint(1, 4)
        pattern = tuple(scale * value for value in pattern)
        mean = random.randint(30, 100)
        data = sample_from_pattern(mean, pattern)
        prefix = (f"At the {cls._site()}, sample data are: "
                  f"{', '.join(map(str, data))}.")
        steps, ss = cls._deviation_steps(data, Fraction(mean),
                                         "sample standard deviation")
        divisor = n - 1
        variance = Fraction(ss, divisor)
        standard_deviation = sqrt_fraction(variance)
        answer = num_txt(standard_deviation)
        steps.extend([
            step("EVAL", "n - 1", divisor),
            step("D", num_txt(ss), divisor, num_txt(variance)),
            step("EVAL", f"s = √{num_txt(variance)}", answer),
            step("CHECK", "square s", f"{answer}²", num_txt(variance)),
        ])
        return cls._new_result("sample_std", prefix, steps, answer)

    @classmethod
    def _shortcut(cls):
        n = random.randint(4, 8)
        pattern = random.choice(patterns(n, max_abs=6))
        scale = random.randint(1, 4)
        pattern = tuple(scale * value for value in pattern)
        mean = random.randint(30, 100)
        data = sample_from_pattern(mean, pattern)
        prefix = (f"At the {cls._site()}, population data are: "
                  f"{', '.join(map(str, data))}. Shortcut formula: "
                  f"σ² = Σx²/n - x̄².")
        total_steps, total = running_sum_steps(data)
        steps = [step("STAT_SETUP", "population variance shortcut", f"n={n}"),
                 *total_steps, step("MEAN_DIV", total, n, mean)]
        squares = []
        for value in data:
            square = value * value
            squares.append(square)
            steps.append(step("E", value, 2, square))
        square_steps, square_total = running_sum_steps(squares)
        steps.extend(square_steps)
        mean_square_x = Fraction(square_total, n)
        mean_squared = mean * mean
        variance = mean_square_x - mean_squared
        steps.extend([
            step("D", square_total, n, num_txt(mean_square_x)),
            step("E", mean, 2, mean_squared),
            step("S", num_txt(mean_square_x), mean_squared,
                 num_txt(variance)),
        ])
        deviations = [(value - mean) ** 2 for value in data]
        for value, square in zip(data, deviations):
            steps.append(step("DEV_ROW", value, value - mean, square))
        deviation_steps, ss = running_sum_steps(deviations)
        steps.extend(deviation_steps)
        checked = Fraction(ss, n)
        steps.extend([step("D", ss, n, num_txt(checked)),
                      step("CHECK", "shortcut = deviation route",
                           num_txt(variance), num_txt(checked))])
        assert variance == checked
        return cls._new_result("shortcut_formula", prefix, steps,
                               num_txt(variance))

    @classmethod
    def _frequency_std(cls):
        n = random.randint(4, 8)
        pattern = random.choice(patterns(n, pop_square=True, max_abs=8))
        scale = random.randint(1, 4)
        pattern = tuple(scale * value for value in pattern)
        mean = random.randint(30, 100)
        data = sample_from_pattern(mean, pattern, shuffle=False)
        counts = sorted(Counter(data).items())
        table = "; ".join(f"{value}: {frequency}"
                          for value, frequency in counts)
        prefix = (f"At the {cls._site()}, frequency table (value: frequency): "
                  f"{table}.")
        steps = [step("FREQ_SETUP", "population standard deviation", f"n={n}")]
        weighted = []
        for value, frequency in counts:
            product = value * frequency
            weighted.append(product)
            steps.append(step("WEIGHT_ROW", value, frequency, product))
        total_steps, total = running_sum_steps(weighted)
        steps.extend(total_steps)
        steps.append(step("MEAN_DIV", total, n, mean))
        contributions = []
        for value, frequency in counts:
            deviation = value - mean
            square = deviation * deviation
            contribution = frequency * square
            contributions.append(contribution)
            steps.extend([step("DEV_ROW", value, deviation, square),
                          step("WEIGHT_ROW", square, frequency, contribution)])
        contribution_steps, ss = running_sum_steps(contributions)
        steps.extend(contribution_steps)
        variance = Fraction(ss, n)
        standard_deviation = sqrt_fraction(variance)
        answer = num_txt(standard_deviation)
        steps.extend([step("D", ss, n, num_txt(variance)),
                      step("EVAL", f"σ = √{num_txt(variance)}", answer),
                      step("CHECK", "weighted squared deviations", ss,
                           answer)])
        return cls._new_result("from_frequency_table", prefix, steps, answer)

    @classmethod
    def _cv(cls):
        percent = random.choice((Fraction(5), Fraction(10), Fraction(25, 2),
                                 Fraction(20), Fraction(25), Fraction(40),
                                 Fraction(50)))
        sigma = random.randint(1, 20)
        mean = Fraction(100 * sigma, percent)
        ratio = Fraction(sigma, mean)
        answer = f"{num_txt(percent)}%"
        prefix = (f"At the {cls._site()}, a population has mean μ = "
                  f"{num_txt(mean)} and standard deviation σ = {sigma}. "
                  f"CV rule: σ/μ × 100%.")
        steps = [
            step("STAT_SETUP", "coefficient of variation",
                 f"μ={num_txt(mean)}, σ={sigma}"),
            step("CV_FORMULA", "σ/μ × 100%"),
            step("D", sigma, num_txt(mean), num_txt(ratio)),
            step("DEC_TO_PERCENT", num_txt(ratio), answer),
            step("CHECK", "relative spread", answer),
        ]
        return cls._new_result("coefficient_of_variation", prefix, steps,
                               answer)

    def generate(self) -> dict:
        if self.variant in EXTENSION_VARIANTS:
            return self._generate_extension(self.variant)
        if self.variant is not None:
            return self._generate_legacy(self.variant)

        # Preserve the legacy wrapper's exact global-RNG advancement. This
        # class sits mid-registry, so consuming a different random sequence
        # would churn seeded examples for hundreds of unrelated generators.
        legacy = self._generate_legacy(random.choice(LEGACY_VARIANTS))
        post_legacy_state = random.getstate()
        digest = hashlib.sha256(
            legacy["problem"].encode("utf-8")
            + repr(post_legacy_state).encode("ascii")
        ).digest()
        if digest[0] >= 224:  # retain a 1/8 legacy share
            return legacy
        extension_index = digest[0] % len(EXTENSION_VARIANTS)
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            return self._generate_extension(
                EXTENSION_VARIANTS[extension_index])
        finally:
            random.setstate(post_legacy_state)

    def _generate_extension(self, variant):
        if variant == "sample_std":
            return self._sample_std()
        if variant == "shortcut_formula":
            return self._shortcut()
        if variant == "from_frequency_table":
            return self._frequency_std()
        return self._cv()

    @staticmethod
    def _generate_legacy(variant):
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

"""Carry out exact pseudo-random and Monte Carlo arithmetic by hand.

Variants: ``lcg_sequence``, ``lcg_period``, ``inverse_transform_discrete``,
``inverse_transform_linear``, ``hit_or_miss_pi``, and
``estimate_from_samples``. Op-codes: ``LCG_SETUP``, ``LCG_STEP``,
``REPEAT``, ``CDF_TABLE``, ``INV_TRANSFORM``, ``ROOT``, ``POINT_SET``,
``HIT``, ``SAMPLE_VALUE``, ``POW``, ``A``, ``M``, ``D``, ``CHECK``, and
``Z``. No logarithm or other unstated calculator value is required.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact, prob_txt


PROBABILITY = True
LCG_BANK = ((5, 1, 8), (5, 3, 16), (4, 1, 9), (1, 3, 10),
            (1, 5, 12), (1, 4, 15), (1, 5, 16), (9, 5, 16))
ROOT_BANK = (Fraction(1, 4), Fraction(1, 3), Fraction(2, 5),
             Fraction(1, 2), Fraction(3, 5), Fraction(2, 3),
             Fraction(3, 4), Fraction(4, 5))
INSIDE_POINTS = ((Fraction(0), Fraction(0)), (Fraction(1, 2), Fraction(1, 2)),
                 (Fraction(3, 5), Fraction(4, 5)),
                 (Fraction(1, 5), Fraction(4, 5)),
                 (Fraction(2, 3), Fraction(1, 3)),
                 (Fraction(3, 4), Fraction(1, 4)),
                 (Fraction(1), Fraction(0)),
                 (Fraction(4, 5), Fraction(3, 5)))
OUTSIDE_POINTS = ((Fraction(4, 5), Fraction(4, 5)),
                  (Fraction(3, 4), Fraction(3, 4)),
                  (Fraction(1), Fraction(1)),
                  (Fraction(2, 3), Fraction(4, 5)),
                  (Fraction(9, 10), Fraction(1, 2)),
                  (Fraction(1, 2), Fraction(9, 10)))
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
QUERIES = {
    "lcg_sequence": (
        "Compute the requested states and normalized uniforms.",
        "Iterate the congruence and divide each state by the modulus.",
        "Find the exact LCG output sequence and its uniform scaling.",
        "Evaluate every stated pseudo-random update.",
        "Generate the next states and reduce all x_i/m fractions.",
    ),
    "lcg_period": (
        "Iterate until the initial state repeats and report the cycle.",
        "Find the exact period and ordered cycle of this LCG.",
        "Track states until the first repeat.",
        "Determine the pseudo-random orbit length and entries.",
        "Compute the full cycle beginning at x_0.",
    ),
    "inverse_transform_discrete": (
        "Use inverse transform sampling to select the outcome.",
        "Find the first cdf value at least as large as u.",
        "Map the supplied uniform value through this discrete cdf.",
        "Identify the cdf interval containing u.",
        "Compute the exact inverse-cdf sample.",
    ),
    "inverse_transform_linear": (
        "Invert the cdf and find the exact sample x.",
        "Use x=B*sqrt(u) with the supplied perfect-square fraction.",
        "Map u through this continuous inverse cdf exactly.",
        "Solve F(x)=u on the stated support.",
        "Compute the inverse-transform sample without a calculator.",
    ),
    "hit_or_miss_pi": (
        "Classify every point and compute the hit-or-miss pi estimate.",
        "Count points in the quarter unit disk, then evaluate 4*hits/n.",
        "Find the exact rational Monte Carlo estimate of pi.",
        "Test x squared plus y squared against one for every sample.",
        "Compute the quarter-circle hit count and resulting estimate.",
    ),
    "estimate_from_samples": (
        "Compute the Monte Carlo estimate as the sample average.",
        "Add the supplied outputs and divide by their count.",
        "Find the exact empirical mean of these simulated values.",
        "Evaluate the estimator from the listed samples.",
        "Use equal weight for every sampled output.",
    ),
}


def _context():
    return (f"At the {random.choice(VENUES)} in {random.choice(CITIES)}, "
            f"{random.choice(NAMES)} performs a simulation calculation.")


def _lcg_next(value, multiplier, increment, modulus):
    return (multiplier * value + increment) % modulus


def _point_text(point):
    return f"({prob_txt(point[0])},{prob_txt(point[1])})"


def _power(base, exponent):
    value = base ** exponent
    return step("POW", f"base {prob_txt(base)}, exponent {exponent}",
                prob_txt(value)), value


class MonteCarloArithmeticGenerator(ProblemGenerator):
    """Generate exact LCG, inverse-transform, and sample-average exercises."""

    VARIANTS = ("lcg_sequence", "lcg_period", "inverse_transform_discrete",
                "inverse_transform_linear", "hit_or_miss_pi",
                "estimate_from_samples")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _lcg_sequence():
        multiplier, increment, modulus = random.choice(LCG_BANK)
        initial = random.randrange(modulus)
        count = random.randint(4, 7)
        problem = (f"{_context()} Method: LCG with x_(n+1)=({multiplier}*x_n+"
                   f"{increment}) mod {modulus}, x_0={initial}. Target: x_1 "
                   f"through x_{count} and u_i=x_i/{modulus}.")
        steps = [step("LCG_SETUP", f"a={multiplier}, c={increment}, m={modulus}",
                      f"x_0={initial}")]
        values, uniforms = [], []
        current = initial
        for index in range(1, count + 1):
            following = _lcg_next(current, multiplier, increment, modulus)
            steps.append(step("LCG_STEP", index,
                              f"({multiplier}*{current}+{increment}) mod {modulus}",
                              following))
            uniform = Fraction(following, modulus)
            steps.append(step("D", following, modulus, prob_txt(uniform)))
            values.append(following)
            uniforms.append(uniform)
            current = following
        answer = ("x = " + ", ".join(map(str, values)) + "; u = "
                  + ", ".join(prob_txt(value) for value in uniforms))
        return problem, steps, answer

    @staticmethod
    def _lcg_period():
        multiplier, increment, modulus = random.choice(LCG_BANK)
        initial = random.randrange(modulus)
        problem = (f"{_context()} Method: LCG with x_(n+1)=({multiplier}*x_n+"
                   f"{increment}) mod {modulus}, x_0={initial}. Target: the "
                   f"period and cycle beginning at x_0.")
        steps = [step("LCG_SETUP", f"a={multiplier}, c={increment}, m={modulus}",
                      f"x_0={initial}")]
        seen, cycle = {}, []
        current = initial
        while current not in seen:
            seen[current] = len(cycle)
            cycle.append(current)
            following = _lcg_next(current, multiplier, increment, modulus)
            steps.append(step("LCG_STEP", len(cycle),
                              f"({multiplier}*{current}+{increment}) mod {modulus}",
                              following))
            current = following
        start = seen[current]
        orbit = cycle[start:]
        steps.extend([
            step("REPEAT", f"state {current}", f"first seen at index {start}"),
            step("CHECK", "cycle closes", f"period {len(orbit)}"),
        ])
        answer = f"period {len(orbit)}; cycle " + ", ".join(map(str, orbit))
        return problem, steps, answer

    @staticmethod
    def _inverse_discrete():
        denominator = random.choice((8, 10, 12, 16, 20))
        cuts = sorted(random.sample(range(1, denominator), 3))
        probabilities = (cuts[0], cuts[1] - cuts[0],
                         cuts[2] - cuts[1], denominator - cuts[2])
        probabilities = tuple(Fraction(value, denominator) for value in probabilities)
        cdf = []
        running = Fraction()
        for probability in probabilities:
            running += probability
            cdf.append(running)
        blocked = {int(value * 100) for value in cdf if (value * 100).denominator == 1}
        choices = [value for value in range(1, 100) if value not in blocked]
        u = Fraction(random.choice(choices), 100)
        outcome = next(index + 1 for index, value in enumerate(cdf) if u <= value)
        lower = Fraction() if outcome == 1 else cdf[outcome - 2]
        table = ", ".join(f"F({index + 1})={prob_txt(value)}"
                          for index, value in enumerate(cdf))
        problem = (f"{_context()} Method: inverse transform for outcomes "
                   f"1, 2, 3, 4 with cdf {table}. Uniform input u={exact(u)}. "
                   f"Target: the sampled outcome.")
        steps = [
            step("CDF_TABLE", "outcomes 1,2,3,4", table),
            step("INV_TRANSFORM", exact(u),
                 (f"{prob_txt(lower)} < u ≤ F({outcome})="
                  f"{prob_txt(cdf[outcome - 1])}"), outcome),
            step("CHECK", "first cdf threshold at least u", outcome),
        ]
        return problem, steps, f"sampled outcome = {outcome}"

    @staticmethod
    def _inverse_linear():
        bound = random.randint(2, 10)
        root = random.choice(ROOT_BANK)
        u = root ** 2
        sample = bound * root
        problem = (f"{_context()} Method: inverse transform on 0≤x≤{bound} "
                   f"with cdf F(x)=x^2/{bound ** 2}. Uniform input u="
                   f"{prob_txt(u)}. Target: the exact sampled x.")
        steps = [
            step("INV_TRANSFORM", f"F(x)=x^2/{bound ** 2}",
                 f"x={bound}*sqrt(u)"),
            step("ROOT", prob_txt(u), prob_txt(root)),
            step("M", bound, prob_txt(root), prob_txt(sample)),
            step("CHECK", "F(sample)=u", prob_txt(u)),
        ]
        return problem, steps, f"sample x = {prob_txt(sample)}"

    @staticmethod
    def _hit_or_miss():
        count = random.randint(6, 10)
        points = [random.choice(INSIDE_POINTS), random.choice(OUTSIDE_POINTS)]
        points.extend(random.choice(INSIDE_POINTS + OUTSIDE_POINTS)
                      for _ in range(count - 2))
        random.shuffle(points)
        point_list = ", ".join(_point_text(point) for point in points)
        problem = (f"{_context()} Method: quarter-square hit-or-miss pi with "
                   f"sample points {point_list}. A hit satisfies x^2+y^2≤1. "
                   f"Target: the hit count and estimate 4*hits/n.")
        steps = [step("POINT_SET", f"n={count}", point_list)]
        hits = 0
        for point in points:
            x_step, x_square = _power(point[0], 2)
            y_step, y_square = _power(point[1], 2)
            radius_square = x_square + y_square
            inside = radius_square <= 1
            hits += int(inside)
            steps.extend([
                x_step, y_step,
                step("A", prob_txt(x_square), prob_txt(y_square),
                     prob_txt(radius_square)),
                step("HIT", _point_text(point),
                     f"{prob_txt(radius_square)} {'≤' if inside else '>'} 1",
                     "in" if inside else "out"),
            ])
        four_hits = 4 * hits
        estimate = Fraction(four_hits, count)
        steps.extend([
            step("M", 4, hits, four_hits),
            step("D", four_hits, count, prob_txt(estimate)),
            step("CHECK", "at least one hit and one miss", "yes"),
        ])
        answer = f"hits = {hits} of {count}; pi estimate = {prob_txt(estimate)}"
        return problem, steps, answer

    @staticmethod
    def _estimate():
        count = random.randint(5, 10)
        denominator = random.choice((2, 3, 4, 5))
        samples = [Fraction(random.randint(0, 4 * denominator), denominator)
                   for _ in range(count)]
        sample_text = ", ".join(prob_txt(value) for value in samples)
        problem = (f"{_context()} Method: equal-weight Monte Carlo average. "
                   f"The sampled outputs are {sample_text}. Target: the exact "
                   f"estimate of E[g(X)].")
        steps = [step("SAMPLE_VALUE", 1, prob_txt(samples[0]))]
        running = samples[0]
        for index, value in enumerate(samples[1:], 2):
            steps.append(step("SAMPLE_VALUE", index, prob_txt(value)))
            steps.append(step("A", prob_txt(running), prob_txt(value),
                              prob_txt(running + value)))
            running += value
        estimate = running / count
        steps.extend([
            step("D", prob_txt(running), count, prob_txt(estimate)),
            step("CHECK", "equal sample weights", f"1/{count} each"),
        ])
        return problem, steps, f"estimate = {prob_txt(estimate)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "lcg_sequence":
            problem, steps, answer = self._lcg_sequence()
        elif variant == "lcg_period":
            problem, steps, answer = self._lcg_period()
        elif variant == "inverse_transform_discrete":
            problem, steps, answer = self._inverse_discrete()
        elif variant == "inverse_transform_linear":
            problem, steps, answer = self._inverse_linear()
        elif variant == "hit_or_miss_pi":
            problem, steps, answer = self._hit_or_miss()
        else:
            problem, steps, answer = self._estimate()
        problem = f"{problem} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_monte_carlo_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

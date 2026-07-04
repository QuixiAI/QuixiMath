import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Standard deviations are 2^a·5^b so every z = (x - μ)/σ is an exact
# terminating decimal.
SIGMAS = [2, 4, 5, 8, 10, 20, 25]


class ZScoreGenerator(ProblemGenerator):
    """
    Z-scores and standardization: convert a raw value to its z-score,
    recover a raw value from a z-score, compare standings across two
    distributions, and flag unusual values with the |z| > 2 rule. All
    z-scores are exact terminating decimals by construction.

    Variants:
    - standardize: z = (x - μ)/σ
    - raw_from_z:  x = μ + z·σ
    - compare:     two distributions, higher z wins
    - unusual:     |z| > 2 flags an unusual value

    Op-codes used:
    - NORM_SETUP / ZSCORE (established, normal_table)
    - ZSCORE_FORMULA / RAW_FORMULA: the formula being applied
    - S / D / M / A / CHECK (established)
    - Z: the z-score, raw value, winner, or usual/unusual verdict
    """

    VARIANTS = ["standardize", "raw_from_z", "compare", "unusual"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _pick(self, unusual=None):
        """Return (mu, sigma, x, z) with z an exact decimal."""
        sigma = random.choice(SIGMAS)
        mu = random.randint(40, 120)
        while True:
            k = random.randint(-3 * sigma, 3 * sigma)
            z = Fraction(k, sigma)
            if k == 0 or mu + k < 0:
                continue
            if unusual is True and abs(z) <= 2:
                continue
            if unusual is False and abs(z) >= 2:
                continue
            return mu, sigma, mu + k, z

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "standardize":
            mu, sigma, x, z = self._pick()
            steps = [
                step("NORM_SETUP", f"X ~ N({mu}, {sigma})",
                     f"z-score of x = {x}"),
                step("ZSCORE_FORMULA", "z = (x - μ)/σ"),
                step("S", x, mu, x - mu),
                step("D", x - mu, sigma, dec(z)),
            ]
            answer = dec(z)
            problem = (f"A distribution has mean {mu} and standard "
                       f"deviation {sigma}. Find the z-score of the "
                       f"value {x}.")
        elif variant == "raw_from_z":
            mu, sigma, x, z = self._pick()
            zs = z * sigma
            steps = [
                step("NORM_SETUP", f"X ~ N({mu}, {sigma})",
                     f"raw value for z = {dec(z)}"),
                step("RAW_FORMULA", "x = μ + z·σ"),
                step("M", dec(z), sigma, dec(zs)),
                step("A", mu, dec(zs), x),
            ]
            answer = str(x)
            problem = (f"A distribution has mean {mu} and standard "
                       f"deviation {sigma}. What value has a z-score "
                       f"of {dec(z)}?")
        elif variant == "compare":
            while True:
                m1, s1, v1, z1 = self._pick()
                m2, s2, v2, z2 = self._pick()
                if z1 != z2:
                    break
            winner = "A" if z1 > z2 else "B"
            steps = [
                step("NORM_SETUP", f"A: {v1} in N({m1}, {s1})",
                     "compare relative standing"),
                step("ZSCORE", f"({v1} - {m1})/{s1}", dec(z1)),
                step("NORM_SETUP", f"B: {v2} in N({m2}, {s2})",
                     "compare relative standing"),
                step("ZSCORE", f"({v2} - {m2})/{s2}", dec(z2)),
                step("CHECK", "higher z-score",
                     f"{dec(z1)} vs {dec(z2)}",
                     f"{winner} is relatively higher"),
            ]
            answer = winner
            problem = (f"Student A scored {v1} on a test with mean "
                       f"{m1} and standard deviation {s1}. Student B "
                       f"scored {v2} on a test with mean {m2} and "
                       f"standard deviation {s2}. Who has the higher "
                       f"relative standing (answer A or B)?")
        else:
            unusual = random.random() < 0.5
            mu, sigma, x, z = self._pick(unusual=unusual)
            verdict = "unusual" if abs(z) > 2 else "usual"
            steps = [
                step("NORM_SETUP", f"X ~ N({mu}, {sigma})",
                     f"is x = {x} unusual?"),
                step("ZSCORE_FORMULA", "z = (x - μ)/σ"),
                step("S", x, mu, x - mu),
                step("D", x - mu, sigma, dec(z)),
                step("CHECK", "abs(z) > 2 rule",
                     f"abs({dec(z)}) {'>' if abs(z) > 2 else '≤'} 2",
                     verdict),
            ]
            answer = verdict
            problem = (f"A distribution has mean {mu} and standard "
                       f"deviation {sigma}. Using the |z| > 2 rule, "
                       f"is the value {x} unusual? (answer usual or "
                       f"unusual)")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"z_score_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

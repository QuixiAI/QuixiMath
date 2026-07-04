import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec, money

# Common denominators that divide 100, so every expected value and
# variance is an exact terminating decimal (and dollar amounts land on
# whole cents).
DENOMS = [4, 5, 10, 20]


def signed_money(fr):
    """Fraction dollars -> '$3.50' or '-$3.50'."""
    return ("-" if fr < 0 else "") + money(abs(fr))


def prob_txt(fr):
    """Probability as a reduced fraction string."""
    return str(fr)


def dist_txt(xs, ps):
    return "; ".join(f"P(X={x}) = {prob_txt(p)}"
                     for x, p in zip(xs, ps))


class ExpectedValueGenerator(ProblemGenerator):
    """
    Expected value and variance of small discrete distributions, and
    the expected value of simple games. Probabilities share a
    denominator dividing 100, so E[X], Var(X) and dollar payoffs are
    all exact.

    Variants:
    - expected_value: E[X] = Σ x·P(x)
    - variance:       Var(X) = Σ P(x)·(x - μ)²
    - winnings:       expected net dollar value of a game
    - fair_game:      classify a paid game as fair / favorable /
                      unfavorable to the player

    Op-codes used:
    - EV_SETUP: the distribution (or game) and the goal
    - EV_FORMULA / VAR_FORMULA: the formula being applied
    - M / A / S / E (established): the weighted products and sums
    - VAR_ROW: one variance term (x-μ, (x-μ)², P·(x-μ)²)
    - CHECK (established): the fair/favorable/unfavorable verdict
    - Z: the expected value, variance, dollar value, or verdict
    """

    VARIANTS = ["expected_value", "variance", "winnings", "fair_game"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _distribution(self, m, x_lo, x_hi, no_zero=False):
        """m outcomes: distinct x in [x_lo, x_hi] and probs summing to 1."""
        den = random.choice(DENOMS)
        while True:
            nums = [random.randint(1, den - m + 1) for _ in range(m - 1)]
            last = den - sum(nums)
            if last >= 1:
                nums.append(last)
                break
        pool = [v for v in range(x_lo, x_hi + 1)
                if not (no_zero and v == 0)]
        xs = random.sample(pool, m)
        ps = [Fraction(n, den) for n in nums]
        return xs, ps

    def _ev_steps(self, xs, ps):
        """Weighted-product + running-sum steps; returns (steps, E)."""
        steps = [step("EV_FORMULA", "E[X] = Σ x·P(x)")]
        terms = []
        for x, p in zip(xs, ps):
            prod = x * p
            terms.append(prod)
            steps.append(step("M", x, prob_txt(p), dec(prod)))
        run = terms[0]
        for t in terms[1:]:
            steps.append(step("A", dec(run), dec(t), dec(run + t)))
            run += t
        return steps, run

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "expected_value":
            m = random.randint(3, 4)
            xs, ps = self._distribution(m, 0, 9)
            steps = [step("EV_SETUP", dist_txt(xs, ps), "E[X]")]
            ev_steps, E = self._ev_steps(xs, ps)
            steps += ev_steps
            answer = dec(E)
            problem = (f"A discrete random variable has distribution "
                       f"{dist_txt(xs, ps)}. Find E[X].")
        elif variant == "variance":
            m = random.randint(3, 4)
            xs, ps = self._distribution(m, 0, 8)
            steps = [step("EV_SETUP", dist_txt(xs, ps), "Var(X)")]
            ev_steps, mu = self._ev_steps(xs, ps)
            steps += ev_steps
            steps.append(step("VAR_FORMULA", "Var(X) = Σ P(x)·(x - μ)^2"))
            terms = []
            for x, p in zip(xs, ps):
                dev = x - mu
                sq = dev * dev
                weighted = p * sq
                terms.append(weighted)
                steps.append(step("VAR_ROW", f"{x} - {dec(mu)} = {dec(dev)}",
                                  f"({dec(dev)})^2 = {dec(sq)}",
                                  f"{prob_txt(p)}·{dec(sq)} = {dec(weighted)}"))
            run = terms[0]
            for t in terms[1:]:
                steps.append(step("A", dec(run), dec(t), dec(run + t)))
                run += t
            answer = dec(run)
            problem = (f"A discrete random variable has distribution "
                       f"{dist_txt(xs, ps)} with mean μ = {dec(mu)}. "
                       f"Find Var(X).")
        elif variant == "winnings":
            m = random.randint(3, 4)
            payoffs, ps = self._distribution(m, -8, 12, no_zero=True)
            steps = [step("EV_SETUP",
                          "; ".join(f"P(${p}) = {prob_txt(pr)}"
                                    for p, pr in zip(payoffs, ps)),
                          "expected value of the game"),
                     step("EV_FORMULA", "E = Σ (payoff)·P")]
            terms = []
            for pay, pr in zip(payoffs, ps):
                prod = pay * pr
                terms.append(prod)
                steps.append(step("M", pay, prob_txt(pr), dec(prod)))
            run = terms[0]
            for t in terms[1:]:
                steps.append(step("A", dec(run), dec(t), dec(run + t)))
                run += t
            answer = signed_money(run)
            outcomes = ", ".join(
                f"{'win' if p > 0 else 'lose'} ${abs(p)} with "
                f"probability {prob_txt(pr)}"
                for p, pr in zip(payoffs, ps))
            problem = (f"In a game you {outcomes}. What is the "
                       f"expected value of the game?")
        else:
            m = random.randint(2, 3)
            payoffs, ps = self._distribution(m, 1, 12)
            cost = random.randint(2, 10)
            steps = [step("EV_SETUP",
                          "; ".join(f"P(win ${p}) = {prob_txt(pr)}"
                                    for p, pr in zip(payoffs, ps)),
                          f"fair? cost = ${cost}")]
            terms = []
            for pay, pr in zip(payoffs, ps):
                prod = pay * pr
                terms.append(prod)
                steps.append(step("M", pay, prob_txt(pr), dec(prod)))
            run = terms[0]
            for t in terms[1:]:
                steps.append(step("A", dec(run), dec(t), dec(run + t)))
                run += t
            net = run - cost
            steps.append(step("S", dec(run), cost, dec(net)))
            verdict = ("fair" if net == 0 else
                       "favorable" if net > 0 else "unfavorable")
            steps.append(step("CHECK", "net vs 0",
                              f"{dec(net)} {'=' if net == 0 else '>' if net > 0 else '<'} 0",
                              verdict))
            answer = verdict
            outcomes = ", ".join(f"win ${p} with probability "
                                 f"{prob_txt(pr)}"
                                 for p, pr in zip(payoffs, ps))
            problem = (f"A game costs ${cost} to play. You {outcomes}. "
                       f"Is the game fair, favorable, or unfavorable "
                       f"to the player?")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"expected_value_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

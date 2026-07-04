import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Carrying capacities are 2^a·5^b so every derived rate is an exact
# terminating decimal.
CAPS = [40, 50, 80, 100, 200, 250, 400, 500]
KS = ["0.2", "0.3", "0.4", "0.5", "0.6", "0.8"]


class LogisticGrowthGenerator(ProblemGenerator):
    """
    Logistic differential equations dP/dt = kP(1 - P/L) worked with
    the standard facts: the carrying capacity is the limit, growth is
    fastest at L/2 with maximum rate kL/4, and the solution is
    P = L/(1 + Ae^(-kt)) with A = (L - P(0))/P(0). All numbers are
    exact terminating decimals or integers by construction.

    Variants:
    - limit: factor aP - bP^2 into logistic form, read off L
    - half_capacity: population of fastest growth, L/2
    - max_rate: maximum of dP/dt, computed as k·L/4
    - rate_at: evaluate kP(1 - P/L) at a clean P
    - solution: build the particular solution from L, P(0), k

    Op-codes used:
    - ODE_SETUP / REWRITE / THEOREM / DOMAIN_NOTE (established)
    - SUBST / EVAL / M / S / D (established) for the arithmetic
    - Z: the requested exact value or the particular solution
    """

    VARIANTS = ["limit", "half_capacity", "max_rate", "rate_at",
                "solution"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        L = random.choice(CAPS)
        k = Fraction(random.choice(KS))
        kt = f"{dec(k)}t"
        factored = f"dP/dt = {dec(k)}P(1 - P/{L})"

        if variant == "limit":
            b = k / L
            P0 = random.choice([v for v in (5, 10, 20, 25, 50)
                                if v < L])
            expanded = f"dP/dt = {dec(k)}P - {dec(b)}P^2"
            steps = [
                step("ODE_SETUP", f"{expanded}, P(0) = {P0}",
                     "find lim t→∞ P"),
                step("D", dec(b), dec(k), f"1/{L}"),
                step("REWRITE", factored),
                step("THEOREM", "logistic carrying capacity",
                     f"solutions with 0 < P(0) < L approach L = {L}"),
                step("DOMAIN_NOTE", f"0 < {P0} < {L}",
                     f"P → {L}"),
            ]
            answer = str(L)
            problem = (f"A population satisfies {expanded} with "
                       f"P(0) = {P0}. Find lim t→∞ P.")
        elif variant == "half_capacity":
            steps = [
                step("ODE_SETUP", factored,
                     "find P where growth is fastest"),
                step("THEOREM", "logistic growth",
                     "dP/dt is greatest at P = L/2"),
                step("D", L, 2, L // 2),
            ]
            answer = str(L // 2)
            problem = (f"A population satisfies {factored}. At what "
                       f"value of P is the population growing fastest?")
        elif variant == "max_rate":
            kL = k * L
            top = kL / 4
            steps = [
                step("ODE_SETUP", factored, "find the maximum of dP/dt"),
                step("THEOREM", "logistic growth",
                     "the maximum rate is k·L/4, at P = L/2"),
                step("M", dec(k), L, dec(kL)),
                step("D", dec(kL), 4, dec(top)),
            ]
            answer = dec(top)
            problem = (f"A population satisfies {factored}. What is "
                       f"the maximum value of dP/dt?")
        elif variant == "rate_at":
            r = random.choice([f for f in
                               (Fraction(1, 4), Fraction(1, 2),
                                Fraction(3, 4), Fraction(1, 5),
                                Fraction(2, 5), Fraction(3, 5),
                                Fraction(4, 5), Fraction(1, 10))
                               if L % f.denominator == 0])
            P = int(L * r)
            rem = 1 - r
            kP = k * P
            rate = kP * rem
            steps = [
                step("ODE_SETUP", factored, f"evaluate dP/dt at P = {P}"),
                step("SUBST", "P", P,
                     f"{dec(k)}({P})(1 - {P}/{L})"),
                step("D", P, L, dec(r)),
                step("S", 1, dec(r), dec(rem)),
                step("M", dec(k), P, dec(kP)),
                step("M", dec(kP), dec(rem), dec(rate)),
            ]
            answer = dec(rate)
            problem = (f"A population satisfies {factored}. Compute "
                       f"dP/dt when P = {P}.")
        else:
            A = random.randint(1, 9)
            P0 = random.choice([5, 10, 20, 25, 50])
            L = P0 * (A + 1)
            diff = L - P0
            answer = f"P = {L}/(1 + {A}e^(-{kt}))" if A > 1 else \
                f"P = {L}/(1 + e^(-{kt}))"
            steps = [
                step("ODE_SETUP",
                     f"logistic: L = {L}, P(0) = {P0}, k = {dec(k)}",
                     "write the particular solution"),
                step("THEOREM", "logistic solution",
                     "P = L/(1 + Ae^(-kt)), A = (L - P(0))/P(0)"),
                step("S", L, P0, diff),
                step("D", diff, P0, A),
                step("REWRITE", answer),
            ]
            problem = (f"A logistic population has carrying capacity "
                       f"{L}, P(0) = {P0}, and growth constant "
                       f"k = {dec(k)}. Write the particular solution "
                       f"P = L/(1 + Ae^(-kt)).")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"logistic_growth_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

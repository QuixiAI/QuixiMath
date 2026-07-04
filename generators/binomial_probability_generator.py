import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# Success probabilities as small fractions; p^k(1-p)^(n-k) stays exact
# (a terminating decimal when the denominator is 2^a·5^b, else a
# reduced fraction).
PS = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5),
      Fraction(1, 10), Fraction(2, 5), Fraction(3, 10), Fraction(2, 3),
      Fraction(3, 4), Fraction(7, 10)]


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


def pow_step(base, e):
    """A POW step for base^e; returns (step, value)."""
    val = base ** e
    return step("POW", f"({base})^{e}", exact(val)), val


class BinomialProbabilityGenerator(ProblemGenerator):
    """
    Binomial probabilities for small n, built the by-hand way:
    P(X = k) = C(n,k)·p^k·(1-p)^(n-k), with the combination and each
    power shown explicitly. Probabilities are small fractions, so
    every answer is exact.

    Variants:
    - exact_k:       P(X = k)
    - at_most:       P(X ≤ k) summed term by term
    - at_least_one:  P(X ≥ 1) = 1 - (1-p)^n (the complement shortcut)
    - mean:          expected successes E[X] = n·p
    - variance:      Var(X) = n·p·(1-p)

    Op-codes used:
    - BINOM_SETUP: n, k, p and the goal
    - BINOM_FORMULA: the pmf (or the moment / complement rule)
    - NCR: the combination C(n, k)
    - POW: a power p^k or (1-p)^(n-k)
    - TERM: one term of a cumulative sum (factors → value)
    - M / A / S (established): products, sums, complement
    - Z: the exact probability, mean, or variance
    """

    VARIANTS = ["exact_k", "at_most", "at_least_one", "mean",
                "variance"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _term_value(self, n, i, p):
        return Fraction(math.comb(n, i)) * p ** i * (1 - p) ** (n - i)

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        p = random.choice(PS)
        q = 1 - p

        if variant == "exact_k":
            n = random.randint(3, 8)
            k = random.randint(1, n - 1)
            C = math.comb(n, k)
            pk = p ** k
            qnk = q ** (n - k)
            partial = C * pk
            prob = partial * qnk
            steps = [
                step("BINOM_SETUP", f"n = {n}, k = {k}, p = {p}",
                     "P(X = k)"),
                step("BINOM_FORMULA",
                     "P(X=k) = C(n,k)·p^k·(1-p)^(n-k)"),
                step("NCR", f"C({n}, {k})", C),
                pow_step(p, k)[0],
                pow_step(q, n - k)[0],
                step("M", C, exact(pk), exact(partial)),
                step("M", exact(partial), exact(qnk), exact(prob)),
            ]
            answer = exact(prob)
            problem = (f"A binomial experiment has n = {n} trials with "
                       f"success probability p = {p}. Find P(X = {k}). "
                       f"Give an exact answer.")
        elif variant == "at_most":
            n = random.randint(3, 6)
            k = random.randint(1, 2)
            steps = [
                step("BINOM_SETUP", f"n = {n}, p = {p}",
                     f"P(X ≤ {k})"),
                step("BINOM_FORMULA",
                     "P(X ≤ k) = Σ C(n,i)·p^i·(1-p)^(n-i)"),
            ]
            terms = []
            for i in range(k + 1):
                C = math.comb(n, i)
                val = self._term_value(n, i, p)
                terms.append(val)
                steps.append(step("TERM",
                                  f"i={i}: {C}·({p})^{i}·({q})^{n - i}",
                                  exact(val)))
            run = terms[0]
            for t in terms[1:]:
                steps.append(step("A", exact(run), exact(t),
                                  exact(run + t)))
                run += t
            answer = exact(run)
            problem = (f"A binomial experiment has n = {n} trials with "
                       f"success probability p = {p}. Find P(X ≤ {k}). "
                       f"Give an exact answer.")
        elif variant == "at_least_one":
            n = random.randint(2, 8)
            qn = q ** n
            prob = 1 - qn
            steps = [
                step("BINOM_SETUP", f"n = {n}, p = {p}", "P(X ≥ 1)"),
                step("BINOM_FORMULA", "P(X ≥ 1) = 1 - (1-p)^n"),
                pow_step(q, n)[0],
                step("S", 1, exact(qn), exact(prob)),
            ]
            answer = exact(prob)
            problem = (f"A binomial experiment has n = {n} trials with "
                       f"success probability p = {p}. Find the "
                       f"probability of at least one success. Give an "
                       f"exact answer.")
        elif variant == "mean":
            n = random.randint(4, 20)
            mean = n * p
            steps = [
                step("BINOM_SETUP", f"n = {n}, p = {p}", "E[X]"),
                step("BINOM_FORMULA", "E[X] = n·p"),
                step("M", n, p, exact(mean)),
            ]
            answer = exact(mean)
            problem = (f"A binomial experiment has n = {n} trials with "
                       f"success probability p = {p}. Find the "
                       f"expected number of successes.")
        else:
            n = random.randint(4, 20)
            np_ = n * p
            var = np_ * q
            steps = [
                step("BINOM_SETUP", f"n = {n}, p = {p}", "Var(X)"),
                step("BINOM_FORMULA", "Var(X) = n·p·(1-p)"),
                step("M", n, p, exact(np_)),
                step("M", exact(np_), exact(q), exact(var)),
            ]
            answer = exact(var)
            problem = (f"A binomial experiment has n = {n} trials with "
                       f"success probability p = {p}. Find the "
                       f"variance of the number of successes. Give an "
                       f"exact answer.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"binomial_probability_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

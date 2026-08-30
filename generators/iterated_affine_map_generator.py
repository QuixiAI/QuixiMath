"""Long orbits of affine maps mod m (depth strand).

Strand I of ``plans/depth_plan.md``: iterate ``x -> (a*x + b) mod m``
for tier-many dependent steps, all state bounded below ``m <= 997``.

Variants:

- ``final_state``: report ``x_N`` after exactly N stated iterations.
- ``orbit_period``: iterate until a value repeats; answer
  ``period L; enters cycle at n=M`` (parameters screened so the rho
  shape ``M + L`` lands in the tier window).
- ``first_return``: ``a`` coprime to ``m`` makes the map a bijection,
  so the orbit is a pure cycle; answer the first ``n > 0`` with
  ``x_n = x_0``.
- ``backward``: given the map and ``x_N``, run the inverse map
  ``x -> a_inv*(x - b) mod m`` for N steps to recover ``x_0``.

Op-codes: ``ITER`` / ``ITER_INV`` (new; previous value first, new value
last per the strand convention), ``MILESTONE`` (state mod 9) at
``d100``+, ``Z``.
"""
import math
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, find_cycle, pick_tier,
                          tier_difficulty, tier_target)

DEPTH = True

PROMPTS = {
    "final_state": (
        "Let x = {x0}. Apply the rule x -> ({a}x + {b}) mod {m} exactly "
        "{n} times. What is the final value?",
        "Starting from x = {x0}, iterate x -> ({a}x + {b}) mod {m} for "
        "{n} iterations. Report the final value.",
        "The rule x -> ({a}x + {b}) mod {m} is applied {n} times starting "
        "at {x0}. Find the resulting value.",
        "Iterate the map x -> ({a}x + {b}) mod {m} a total of {n} times "
        "from x = {x0}. Give the final value.",
    ),
    "orbit_period": (
        "Let x = {x0}. Iterate x -> ({a}x + {b}) mod {m} until a value "
        "repeats (at most {cap} steps). Where does the orbit enter its "
        "cycle, and what is the cycle length?",
        "Starting from x = {x0}, apply x -> ({a}x + {b}) mod {m} until "
        "some value appears twice (at most {cap} steps). Report the cycle "
        "entry point and the period.",
        "Iterate the map x -> ({a}x + {b}) mod {m} from {x0} until a "
        "repeat occurs (at most {cap} steps). Give the period and where "
        "the cycle begins.",
        "The orbit of {x0} under x -> ({a}x + {b}) mod {m} eventually "
        "repeats; trace it (at most {cap} steps) and report the period "
        "and the entry index.",
    ),
    "first_return": (
        "Let x = {x0}. Iterate x -> ({a}x + {b}) mod {m} until the value "
        "returns to {x0} (at most {cap} steps). After how many steps does "
        "it first return?",
        "Starting from x = {x0}, apply x -> ({a}x + {b}) mod {m} until "
        "{x0} appears again (at most {cap} steps). Report the first "
        "return time.",
        "Iterate the map x -> ({a}x + {b}) mod {m} from {x0} until it "
        "comes back to its start (at most {cap} steps). How many steps "
        "does that take?",
        "The orbit of {x0} under x -> ({a}x + {b}) mod {m} returns to "
        "{x0}; trace it (at most {cap} steps) and report the first "
        "return time.",
    ),
    "backward": (
        "The rule x -> ({a}x + {b}) mod {m} was applied exactly {n} "
        "times and produced {xn}. Undo it step by step using the inverse "
        "rule x -> {ainv}(x - {b}) mod {m}. What was the starting value?",
        "After {n} applications of x -> ({a}x + {b}) mod {m}, the value "
        "is {xn}. Run the inverse rule x -> {ainv}(x - {b}) mod {m} the "
        "same number of times to recover the start.",
        "Applying x -> ({a}x + {b}) mod {m} exactly {n} times turned an "
        "unknown start into {xn}. Invert it with x -> {ainv}(x - {b}) "
        "mod {m}, one step at a time. Find the start.",
        "A value was pushed through x -> ({a}x + {b}) mod {m} for {n} "
        "iterations, ending at {xn}. Use the inverse rule x -> "
        "{ainv}(x - {b}) mod {m} to walk back to the starting value.",
    ),
}


def _milestoned_chain(x0, tier):
    chain = Chain(x0, milestone_spacing=(True if tier != "d50" else None))
    chain.set_invariant("state mod 9", lambda v, k: v % 9)
    return chain


class IteratedAffineMapGenerator(ProblemGenerator):
    """Long affine orbits mod m (depth strand)."""

    VARIANTS = ("final_state", "orbit_period", "first_return", "backward")
    BASE_DIFFICULTY = 2

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and tier not in ("d50", "d100", "d200"):
            raise ValueError("tier must be d50, d100, d200, or None")
        self.variant = variant
        self.tier = tier

    @staticmethod
    def _params(rng, coprime):
        m = rng.randint(50, 997)
        a = rng.randint(2, m - 1)
        if coprime:
            while math.gcd(a, m) != 1:
                a = rng.randint(2, m - 1)
        b = rng.randint(0, m - 1)
        x0 = rng.randint(0, m - 1)
        return a, b, m, x0

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        tier = self.tier or pick_tier()
        n = tier_target(tier)

        if variant in ("final_state", "backward"):
            a, b, m, x0 = self._params(random, coprime=(variant == "backward"))
            if variant == "final_state":
                chain = _milestoned_chain(x0, tier)
                for k in range(1, n + 1):
                    chain.apply("ITER", f"n={k}", (a * chain.value + b) % m)
                answer = str(chain.value)
                problem = random.choice(PROMPTS[variant]).format(
                    a=a, b=b, m=m, x0=x0, n=n)
            else:
                ainv = pow(a, -1, m)
                xn = x0
                for _ in range(n):
                    xn = (a * xn + b) % m
                chain = _milestoned_chain(xn, tier)
                for k in range(1, n + 1):
                    chain.apply("ITER_INV", f"n={k}",
                                (ainv * (chain.value - b)) % m)
                answer = str(x0)
                problem = random.choice(PROMPTS[variant]).format(
                    a=a, b=b, m=m, xn=xn, n=n, ainv=ainv)
        else:
            # Screen parameters until the rho shape fits the tier window.
            lo, hi = max(n - 15, TIER_FLOORS[tier]), n + 15
            for _ in range(5000):
                a, b, m, x0 = self._params(
                    random, coprime=(variant == "first_return"))
                f = lambda x: (a * x + b) % m
                mu, lam = find_cycle(f, x0)
                # first_return traces the full cycle back to x0; the rho
                # variant stops at step mu+lam, whose value equals x_mu —
                # the first visible repeat.
                length = lam if variant == "first_return" else mu + lam
                if lo <= length <= hi:
                    break
            else:  # pragma: no cover - the parameter space is vast
                raise ValueError("no orbit shape found for the tier")
            chain = _milestoned_chain(x0, tier)
            for k in range(1, length + 1):
                chain.apply("ITER", f"n={k}", (a * chain.value + b) % m)
            cap = ((length + 24) // 25) * 25  # a stated honest ceiling
            if variant == "first_return":
                answer = str(lam)
            else:
                answer = f"period {lam}; enters cycle at n={mu}"
            problem = random.choice(PROMPTS[variant]).format(
                a=a, b=b, m=m, x0=x0, cap=cap)

        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"iterated_affine_map_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )

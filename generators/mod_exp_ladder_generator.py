"""Square-and-multiply ladders mod small m (depth strand).

Strand E of ``plans/depth_plan.md``. The accumulator never leaves
``Z_m`` (m <= 499), while the exponent is huge: the ladder walks its
binary expansion bit by bit, one ``LADDER`` step per square and one per
multiply, so the chain length is ``bits + popcount - 1``.

Variants:

- ``final_residue``: a^E mod m after the full ladder.
- ``ladder_audit``: the same ladder with MILESTONE rows whose invariant
  is the number of exponent bits consumed so far — a positional
  drift-check the oracle re-derives from the exponent's expansion; the
  answer states the residue and the bit count.
- ``fermat_route``: m prime; first reduce the tier-many-DIGIT exponent
  mod ord_m(a) with a digit-by-digit ``DIV_STEP`` chain (that reduction
  is the marathon), then finish with a short ladder on the reduced
  exponent. Composite answer ``E = r (mod ord); a^E = x (mod m)``.

Op-codes: ``LADDER`` (new), ``DIV_STEP`` / ``RULE`` (established),
``MILESTONE``, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

PROMPTS = {
    "final_residue": (
        "Compute {a}^{e} mod {m} by square-and-multiply, walking the "
        "exponent's {bits} bits one at a time. What is the residue?",
        "Use the binary ladder ({bits} bits) to evaluate {a}^{e} mod {m} "
        "step by step. Report the residue.",
        "Walk the {bits} bits of the exponent to compute {a}^{e} mod {m} "
        "by repeated squaring. Give the result.",
        "Evaluate {a}^{e} mod {m} with the square-and-multiply ladder "
        "over all {bits} bits. What value results?",
    ),
    "ladder_audit": (
        "Compute {a}^{e} mod {m} by square-and-multiply, walking the "
        "exponent's {bits} bits one at a time. Report the residue and "
        "confirm how many bits were consumed.",
        "Use the binary ladder ({bits} bits) to evaluate {a}^{e} mod {m} "
        "step by step. Give the residue and the bit count.",
        "Walk the {bits} bits of the exponent to compute {a}^{e} mod {m} "
        "by repeated squaring. State the result and the bits consumed.",
        "Evaluate {a}^{e} mod {m} with the square-and-multiply ladder "
        "over all {bits} bits. Report the residue and the count of bits.",
    ),
    "fermat_route": (
        "Compute {a}^{e} mod {m} (the exponent has {L} digits). First "
        "reduce the exponent mod {order} — the order of {a} — digit by "
        "digit, then finish with a short ladder. State the reduced "
        "exponent and the residue.",
        "Evaluate {a}^{e} mod {m}, where the exponent has {L} digits: "
        "reduce it mod the order {order} of {a} one digit at a time, "
        "then square-and-multiply. Give both the reduction and the "
        "result.",
        "The exponent of {a}^{e} mod {m} has {L} digits. Take it mod "
        "{order} (the order of {a}) digit by digit, then run the short "
        "ladder. Report the reduced exponent and the final residue.",
        "Work out {a}^{e} mod {m} by first collapsing the exponent of "
        "{L} digits mod {order}, the order of {a}, digit by digit, then "
        "finishing the ladder. State the reduction and the residue.",
    ),
}


def _ladder_links(e):
    return e.bit_length() + bin(e).count("1") - 1


def _emit_ladder(a, e, m, chain, consumed):
    """Walk the ladder, appending to ``consumed`` BEFORE each apply so a
    milestone firing inside the apply reads live positional state."""
    bits = bin(e)[2:]
    consumed.append(1)
    chain.apply("LADDER", f"start acc = a (bit 1 of {len(bits)})", a % m)
    for index, bit in enumerate(bits[1:], start=2):
        consumed.append(index)
        chain.apply("LADDER", f"square (bit {index} of {len(bits)})",
                    (chain.value * chain.value) % m)
        if bit == "1":
            consumed.append(index)
            chain.apply("LADDER", f"multiply by {a} (bit {index})",
                        (chain.value * a) % m)


def _order(a, m):
    order, power = 1, a % m
    while power != 1:
        power = (power * a) % m
        order += 1
    return order


def _small_primes():
    out = []
    for q in range(11, 500):
        if all(q % d for d in range(2, int(q ** 0.5) + 1)):
            out.append(q)
    return out


PRIMES = _small_primes()


class ModExpLadderGenerator(ProblemGenerator):
    """Modular exponentiation marathons (depth strand)."""

    VARIANTS = ("final_residue", "ladder_audit", "fermat_route")
    BASE_DIFFICULTY = 3

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and tier not in ("d50", "d100", "d200"):
            raise ValueError("tier must be d50, d100, d200, or None")
        self.variant = variant
        self.tier = tier

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        tier = self.tier or pick_tier()
        target = tier_target(tier)
        lo, hi = TIER_FLOORS[tier], target + 15

        if variant == "fermat_route":
            m = random.choice(PRIMES)
            a = random.randint(2, m - 1)
            order = _order(a, m)
            length = target  # digit-reduction chain carries the tier
            digits = ([random.randint(1, 9)]
                      + [random.randint(0, 9) for _ in range(length - 1)])
            e = int("".join(str(d) for d in digits))
            chain = Chain(0, milestone_spacing=(True if tier != "d50"
                                                else None))
            chain.set_invariant("remainder mod 9", lambda v, k: v % 9)
            for d in digits:
                widened = chain.value * 10 + d
                chain.apply("DIV_STEP", f"d={d}, q={widened // order}",
                            widened % order)
            reduced = chain.value
            chain.steps.append(step(
                "RULE", f"a^E = a^(E mod ord) since ord({a}) = {order}",
                f"exponent becomes {reduced}"))
            residue = pow(a, reduced, m) if reduced else 1
            if reduced:
                ladder = Chain(1)
                _emit_ladder(a, reduced, m, ladder, [])
                chain.steps.extend(ladder.steps)
            answer = f"E = {reduced} (mod {order}); {a}^E = {residue} (mod {m})"
            problem = random.choice(PROMPTS[variant]).format(
                a=a, e=e, m=m, L=length, order=order)
        else:
            m = random.randint(5, 499)
            a = random.randint(2, m - 1)
            # links ~ 1.5x bits on average, so draw bit-lengths near
            # two-thirds of the window and screen the exact link count.
            b_lo = max(2, (2 * lo) // 3 - 6)
            b_hi = (2 * hi) // 3 + 6
            for _ in range(5000):
                e = random.getrandbits(random.randint(b_lo, b_hi)) | 1
                if lo <= _ladder_links(e) <= hi:
                    break
            else:  # pragma: no cover
                raise ValueError("no exponent found for the tier")
            chain = Chain(1, milestone_spacing=(True if tier != "d50"
                                                else None))
            bits = e.bit_length()
            consumed_schedule = []
            if variant == "ladder_audit":
                chain.set_invariant(
                    "exponent bits consumed",
                    lambda v, k: consumed_schedule[k - 1])
            else:
                chain.set_invariant("acc mod 9", lambda v, k: v % 9)
            _emit_ladder(a, e, m, chain, consumed_schedule)
            residue = chain.value
            if variant == "ladder_audit":
                answer = f"{residue}; {bits} bits consumed"
            else:
                answer = str(residue)
            problem = random.choice(PROMPTS[variant]).format(
                a=a, e=e, m=m, bits=bits)

        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"mod_exp_ladder_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )

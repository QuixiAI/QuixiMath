"""Compare options by expected cost, worst case, and simple ruin risk.

Variants: ``expected_cost_two_plans``, ``insurance_premium_vs_expected_loss``,
``fair_price``, ``minimax_vs_expected``, ``risk_of_ruin_simple``,
``wait_or_buy``. Five context frames and all four applied modifiers are
supported. Probabilities are always tenths or clean fractions, and dollar
amounts are chosen backward so every expectation lands on the cent. Ties are
excluded by construction. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``EXPECTED_COST``, ``DECIDE``,
``EXPECTED_LOSS``, ``CMP``, ``FAIR_PRICE``, ``WORST_CASE``, ``MINIMAX``,
``SURVIVE_PROB``, ``RUIN_PROB``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, dec, estimate_first, exact,
                            frac_percent, money, select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("expected_cost_two_plans", "insurance_premium_vs_expected_loss",
            "fair_price", "minimax_vs_expected", "risk_of_ruin_simple",
            "wait_or_buy")
FRAMES = (
    "At {place}, {name} weighs the following choice. {facts} {question}",
    "{question} A decision faced by {name} at {place}: {facts}",
    "For {name}'s decision at {place}: {facts} {question}",
    "A memo from {place}, reviewed by {name}, reads: {facts} {question}",
    "Consider the choice {name} faces at {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)

TENTHS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
INSURANCE_PERCENTS = (1, 2, 4, 5, 10, 20, 25, 50)


def _places(fr):
    """Decimal places in the exact terminating render of ``fr``."""
    s = dec(fr)
    return len(s.split(".")[1]) if "." in s else 0


#: (per-round ruin probability, rounds) pairs whose survival probability
#: still terminates within four decimal places by hand.
RUIN_OPTIONS = [(p, n) for p in (Fraction(1, 20), Fraction(1, 10),
                                 Fraction(1, 8), Fraction(1, 5), Fraction(1, 4))
                for n in range(2, 6) if _places((1 - p) ** n) <= 4]


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class DecisionUnderUncertaintyGenerator(ProblemGenerator):
    """Generate six exact expected-cost decision models without naming a method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _expected_cost_two_plans():
        flat = 10 * random.randint(5, 30)
        base = 10 * random.randint(2, flat // 10)
        fee = 10 * random.randint(5, 40)
        prob = Fraction(random.choice(TENTHS), 10)
        cost_b = base + fee * prob
        while cost_b == flat:
            prob = Fraction(random.choice(TENTHS), 10)
            cost_b = base + fee * prob
        winner, w_cost, l_cost = ("A", flat, cost_b) if flat < cost_b else ("B", cost_b, flat)
        facts = (f"Plan A costs ${flat} flat. Plan B costs ${base} plus a "
                 f"${fee} repair fee that is needed with probability {dec(prob)}.")
        question = "Which has the lower expected cost?"
        model = "expected(B) = base + probability × fee"
        steps = [step("EXPECTED_COST", "A", flat, flat),
                step("EXPECTED_COST", "B", f"{base} + {dec(prob)}·{fee}", dec(cost_b)),
                step("DECIDE", winner, f"{dec(w_cost)} < {dec(l_cost)}")]
        answer = f"plan {winner}; ${dec(w_cost)} vs ${dec(l_cost)}"
        used = [f"plan A ${flat}", f"plan B base ${base}, fee ${fee} at {dec(prob)}"]
        return facts, question, steps, answer, cost_b, model, used, money

    @staticmethod
    def _insurance_premium_vs_expected_loss():
        pct = random.choice(INSURANCE_PERCENTS)
        loss = 100 * random.randint(2, 100)
        expected_loss = pct * loss // 100
        premium = expected_loss + random.choice([n for n in range(-80, 81, 5) if n != 0])
        premium = max(1, premium)
        diff = premium - expected_loss
        while diff == 0:
            premium += 5
            diff = premium - expected_loss
        verb = "exceeds it by" if diff > 0 else "is below it by"
        facts = (f"An insurance premium is ${premium}. There is a {pct}% "
                 f"chance of a ${loss} loss.")
        question = "How does the premium compare to the expected loss?"
        model = "expected loss = probability × loss"
        steps = [step("EXPECTED_LOSS", f"{pct}% × {loss}", expected_loss),
                step("CMP", premium, expected_loss, ">" if diff > 0 else "<")]
        answer = f"expected loss ${expected_loss}; premium {verb} ${abs(diff)}"
        used = [f"premium ${premium}", f"{pct}% chance of ${loss}"]
        return facts, question, steps, answer, Fraction(expected_loss), model, used, money

    @staticmethod
    def _fair_price():
        prob = Fraction(random.choice(TENTHS), 10)
        x = 10 * random.randint(2, 60)
        y = 10 * random.randint(0, 40)
        fair = prob * x + (1 - prob) * y
        facts = f"A game pays ${x} with probability {dec(prob)} and ${y} otherwise."
        question = "What is the fair price to play?"
        model = "fair price = p × payout1 + (1 − p) × payout2"
        steps = [step("FAIR_PRICE", f"{dec(prob)}·{x} + {dec(1 - prob)}·{y}", money(fair))]
        answer = money(fair)
        used = [f"payout ${x} at {dec(prob)}", f"payout ${y} otherwise"]
        return facts, question, steps, answer, fair, model, used, money

    @staticmethod
    def _minimax_vs_expected():
        guaranteed = 10 * random.randint(3, 30)
        high = 10 * random.randint(guaranteed // 10, guaranteed * 3 // 10 + 10)
        prob = Fraction(random.choice(TENTHS), 10)
        expected_b = high * prob
        while expected_b == guaranteed:
            prob = Fraction(random.choice(TENTHS), 10)
            expected_b = high * prob
        ev_winner = "A" if guaranteed > expected_b else "B"
        hi_ev, lo_ev = (guaranteed, expected_b) if guaranteed > expected_b else (expected_b, guaranteed)
        facts = (f"Option A guarantees ${guaranteed}. Option B pays ${high} "
                 f"with probability {dec(prob)} and $0 otherwise.")
        question = "Which option does the worst-case rule choose, and which option is better once each outcome's probability is accounted for?"
        model = "worst case = smallest possible payout; expected = probability-weighted average"
        steps = [step("WORST_CASE", "A", guaranteed), step("WORST_CASE", "B", 0),
                step("MINIMAX", "A", f"{guaranteed} > 0"),
                step("EXPECTED_COST", "B", f"{dec(prob)}·{high}", dec(expected_b)),
                step("CMP", dec(guaranteed), dec(expected_b), ">" if guaranteed > expected_b else "<")]
        answer = f"worst-case: A; expected value: {ev_winner} (${dec(hi_ev)} vs ${dec(lo_ev)})"
        used = [f"A guarantees ${guaranteed}", f"B pays ${high} at {dec(prob)}"]
        return facts, question, steps, answer, expected_b, model, used, money

    @staticmethod
    def _risk_of_ruin_simple():
        p, n = random.choice(RUIN_OPTIONS)
        survive = (1 - p) ** n
        ruin = 1 - survive
        facts = (f"On each of {n} independent rounds, there is a "
                 f"{frac_percent(p)} chance of ruin.")
        question = f"What is the probability of ruin over all {n} rounds combined?"
        model = "P(ruin) = 1 − (1 − p)^rounds"
        steps = [step("SURVIVE_PROB", f"(1 − {exact(p)})^{n}", exact(survive)),
                step("RUIN_PROB", f"1 − {exact(survive)}", exact(ruin))]
        answer = frac_percent(ruin)
        used = [f"per-round ruin chance {frac_percent(p)}", f"rounds {n}"]
        return facts, question, steps, answer, ruin, model, used, frac_percent

    @staticmethod
    def _wait_or_buy():
        price_now = 10 * random.randint(5, 50)
        new_price = 10 * random.randint(0, 70)
        while new_price == price_now:
            new_price = 10 * random.randint(0, 70)
        prob = Fraction(random.choice(TENTHS), 10)
        expected_wait = prob * new_price + (1 - prob) * price_now
        while expected_wait == price_now:
            prob = Fraction(random.choice(TENTHS), 10)
            expected_wait = prob * new_price + (1 - prob) * price_now
        winner = "buy now" if price_now < expected_wait else "wait"
        w_cost, l_cost = (price_now, expected_wait) if price_now < expected_wait else (expected_wait, price_now)
        facts = (f"A price is ${price_now} now. There is a {dec(prob)} "
                 f"probability it changes to ${new_price} next week; "
                 f"otherwise it stays at ${price_now}.")
        question = "Is it better to buy now or wait, based on expected cost?"
        model = "expected(wait) = p × new price + (1 − p) × current price"
        steps = [step("EXPECTED_COST", "buy now", price_now, price_now),
                step("EXPECTED_COST", "wait",
                     f"{dec(prob)}·{new_price} + {dec(1 - prob)}·{price_now}", dec(expected_wait)),
                step("DECIDE", winner, f"{dec(w_cost)} < {dec(l_cost)}")]
        answer = f"{winner}; ${dec(w_cost)} vs ${dec(l_cost)}"
        used = [f"now ${price_now}", f"next week ${new_price} at {dec(prob)}"]
        return facts, question, steps, answer, expected_wait, model, used, money

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in range(501, 801) if n not in occupied])
            problem = f"An unrelated memo lists {extra} archived files. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} archived files"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale of the deciding cost",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "decision-under-uncertainty relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_decision_under_uncertainty_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}

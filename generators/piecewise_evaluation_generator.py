import random
from base_generator import ProblemGenerator
from helpers import step, jid


def money(cents):
    """Formats integer cents as a dollars string with two decimals."""
    return f"{cents // 100}.{cents % 100:02d}"


def sub(n):
    """A substituted input is always parenthesized: 2(3) + 5, (-2)^2."""
    return f"({n})"


def halves(n2):
    """Renders a count of half-units: 7 halves -> 3.5, 6 halves -> 3."""
    return str(n2 // 2) if n2 % 2 == 0 else f"{n2 // 2}.5"


class PiecewiseEvaluationGenerator(ProblemGenerator):
    """
    Evaluates piecewise and step functions: pick the branch, then compute.

    Variants:
    - abstract: three-piece f(x) with strict/inclusive boundaries; the
      input sometimes lands exactly on a boundary
    - shipping: flat-rate weight bands (a pure step function)
    - billing:  base fee with included units plus a per-unit overage rate
    - tax:      two marginal brackets - tax each slice at its own rate

    The scratchpad always tests the branch conditions in order against the
    actual input before any arithmetic, the way a person traces a piecewise
    definition by hand.

    Op-codes used:
    - FUNC_SETUP: the definition and the evaluation target (established)
    - BRANCH_TEST: test one branch condition with the input substituted
      (condition, yes/no)
    - BRANCH_USE: the selected branch needs no further arithmetic; read
      off its value (value)
    - SUBST / E / M / A / S: the arithmetic (established meanings)
    - PERCENT_TO_DEC: rate conversion for tax brackets (established)
    - Z: final answer
    """

    VARIANTS = ["abstract", "shipping", "billing", "tax"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _abstract(self):
        fname = random.choice(["f", "g", "h"])
        var = random.choice(["x", "x", "t"])
        c1 = random.randint(-3, 1)
        c2 = c1 + random.randint(2, 4)

        a1 = random.choice([v for v in range(-4, 5) if v not in (-1, 0, 1)])
        b1 = random.choice([v for v in range(-5, 6) if v != 0])
        b1_txt = f"+ {b1}" if b1 > 0 else f"- {-b1}"
        p1 = f"{a1}{var} {b1_txt}"
        p2 = f"{var}^2"
        p3 = str(random.choice([v for v in range(-9, 10)]))

        region = random.randint(1, 3)
        if region == 1:
            k = c1 - random.randint(1, 4)
        elif region == 2:
            k = random.randint(c1, c2)  # boundaries included on purpose
        else:
            k = c2 + random.randint(1, 4)

        defn = (f"{fname}({var}) = {{ {p1} if {var} < {c1}; "
                f"{p2} if {c1} <= {var} <= {c2}; {p3} if {var} > {c2} }}")
        steps = [step("FUNC_SETUP", defn, f"{fname}({k})")]

        steps.append(step("BRANCH_TEST", f"{k} < {c1}",
                          "yes" if k < c1 else "no"))
        if k >= c1:
            steps.append(step("BRANCH_TEST", f"{c1} <= {k} <= {c2}",
                              "yes" if k <= c2 else "no"))
        if k >= c1 and k > c2:
            steps.append(step("BRANCH_TEST", f"{k} > {c2}", "yes"))

        if region == 1:
            value = a1 * k + b1
            steps.append(step("SUBST", var, k, f"{a1}{sub(k)} {b1_txt}"))
            steps.append(step("M", a1, k, a1 * k))
            steps.append(step("A", a1 * k, b1, value))
        elif region == 2:
            value = k * k
            steps.append(step("SUBST", var, k, f"{sub(k)}^2"))
            steps.append(step("E", sub(k), 2, value))
        else:
            value = int(p3)
            steps.append(step("BRANCH_USE", p3))

        steps.append(step("Z", value))
        problem = f"Given {defn}, find {fname}({k})."
        return self._pack("piecewise_evaluation", problem, steps, str(value))

    def _shipping(self):
        cut1 = random.choice([1, 2, 3])
        cut2 = random.choice([5, 6, 8])
        p1 = 25 * random.randint(10, 24)
        p2 = p1 + 25 * random.randint(4, 12)
        p3 = p2 + 25 * random.randint(4, 12)
        w2 = random.randint(1, 2 * cut2 + 6)  # weight in half-pounds
        w = halves(w2)

        if w2 <= 2 * cut1:
            price = p1
        elif w2 <= 2 * cut2:
            price = p2
        else:
            price = p3

        bands = (f"up to {cut1} lb: ${money(p1)}; "
                 f"over {cut1} lb up to {cut2} lb: ${money(p2)}; "
                 f"over {cut2} lb: ${money(p3)}")
        steps = [step("FUNC_SETUP", bands, f"weight {w} lb")]
        steps.append(step("BRANCH_TEST", f"{w} <= {cut1}",
                          "yes" if w2 <= 2 * cut1 else "no"))
        if w2 > 2 * cut1:
            steps.append(step("BRANCH_TEST", f"{cut1} < {w} <= {cut2}",
                              "yes" if w2 <= 2 * cut2 else "no"))
        if w2 > 2 * cut2:
            steps.append(step("BRANCH_TEST", f"{w} > {cut2}", "yes"))
        steps.append(step("BRANCH_USE", f"${money(price)}"))
        steps.append(step("Z", f"${money(price)}"))

        problem = (f"Shipping costs ${money(p1)} for packages up to {cut1} lb, "
                   f"${money(p2)} for over {cut1} lb up to {cut2} lb, and "
                   f"${money(p3)} for over {cut2} lb. Find the cost to ship a "
                   f"{w} lb package.")
        return self._pack("piecewise_shipping", problem, steps,
                          f"${money(price)}")

    def _billing(self):
        base = random.choice([1500, 2000, 2500, 3000, 4000])
        included = random.choice([100, 200, 300, 500])
        rate = random.choice([5, 10, 15, 20, 25])  # cents per extra minute
        if random.random() < 0.6:
            used = included + random.randint(5, 120)
        else:
            used = random.randint(included // 2, included)

        setup = (f"${money(base)} base for first {included} min, "
                 f"${money(rate)} per extra min")
        steps = [step("FUNC_SETUP", setup, f"{used} minutes")]
        steps.append(step("BRANCH_TEST", f"{used} <= {included}",
                          "yes" if used <= included else "no"))
        if used <= included:
            total = base
            steps.append(step("BRANCH_USE", f"${money(base)}"))
        else:
            extra = used - included
            over = extra * rate
            total = base + over
            steps.append(step("S", used, included, extra))
            steps.append(step("M", extra, money(rate), money(over)))
            steps.append(step("A", money(base), money(over), money(total)))
        steps.append(step("Z", f"${money(total)}"))

        problem = (f"A phone plan costs ${money(base)} per month including "
                   f"{included} minutes, plus ${money(rate)} for each "
                   f"additional minute. Find the bill for {used} minutes.")
        return self._pack("piecewise_billing", problem, steps,
                          f"${money(total)}")

    def _tax(self):
        bracket = random.choice([8000, 10000, 12000, 15000, 20000])
        r1 = random.choice([5, 8, 10, 12])
        r2 = random.choice([15, 18, 20, 22, 25])
        if random.random() < 0.65:
            income = bracket + 500 * random.randint(2, 30)
        else:
            income = 500 * random.randint(4, bracket // 500)

        setup = (f"{r1}% on first ${bracket} of income, "
                 f"{r2}% on income above ${bracket}")
        steps = [step("FUNC_SETUP", setup, f"income ${income}")]
        steps.append(step("BRANCH_TEST", f"{income} <= {bracket}",
                          "yes" if income <= bracket else "no"))
        if income <= bracket:
            tax = income * r1 // 100
            steps.append(step("PERCENT_TO_DEC", f"{r1}%", f"0.{r1:02d}"))
            steps.append(step("M", income, f"0.{r1:02d}", tax))
        else:
            t1 = bracket * r1 // 100
            above = income - bracket
            t2 = above * r2 // 100
            tax = t1 + t2
            steps.append(step("PERCENT_TO_DEC", f"{r1}%", f"0.{r1:02d}"))
            steps.append(step("M", bracket, f"0.{r1:02d}", t1))
            steps.append(step("S", income, bracket, above))
            steps.append(step("PERCENT_TO_DEC", f"{r2}%", f"0.{r2:02d}"))
            steps.append(step("M", above, f"0.{r2:02d}", t2))
            steps.append(step("A", t1, t2, tax))
        steps.append(step("Z", f"${tax}"))

        problem = (f"A tax is {r1}% on the first ${bracket} of income and "
                   f"{r2}% on income above ${bracket}. Find the tax on an "
                   f"income of ${income}.")
        return self._pack("piecewise_tax", problem, steps, f"${tax}")

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

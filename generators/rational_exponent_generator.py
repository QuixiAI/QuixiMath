import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid

ROOT_SYM = {2: "√", 3: "∛", 4: "∜"}


def radical_txt(n, var, m):
    """'∛(x^2)', '∛x', '√(x^3)'."""
    inner = var if m == 1 else f"{var}^{m}"
    if m == 1:
        return f"{ROOT_SYM[n]}{var}"
    return f"{ROOT_SYM[n]}({inner})"


class RationalExponentGenerator(ProblemGenerator):
    """
    Rational exponents ↔ radicals.

    Variants:
    - to_radical:   x^(m/n) → ⁿ√(x^m), with m/n already in lowest terms
    - from_radical: ⁿ√(x^m) → x^(m/n), REDUCING the exponent fraction
      (∜(x²) → x^(2/4) → x^(1/2); ∛(x⁶) → x²)
    - evaluate:     k^n raised to (m/n) — root first, then power; negative
      exponents flip to a reciprocal

    Op-codes used:
    - EXP_RULE_SETUP / EXP_RULE_IDENTIFY (established exponent vocabulary)
    - FORM_IDENTIFY: the conversion rule (name, formula)
    - ROOT / CBRT: take the root (value, root)
    - E: raise to the power (base, exponent, result)
    - F: reduce the exponent fraction (from, to)
    - REWRITE: current form (string)
    - Z: final answer
    """

    VARIANTS = ["to_radical", "from_radical", "evaluate"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _to_radical(self):
        # 40% numeric base: 7^(2/3) -> ∛(7^2) -> ∛49
        if random.random() < 0.4:
            b = random.choice([2, 3, 5, 6, 7, 10])
            while True:
                n = random.choice([2, 3, 4])
                m = random.randint(2, 5)
                if gcd(m, n) == 1 and b ** m <= 1000:
                    break
            original = f"{b}^({m}/{n})"
            answer = f"{ROOT_SYM[n]}{b ** m}"
            steps = [
                step("EXP_RULE_SETUP", original),
                step("FORM_IDENTIFY", "rational_exponent",
                     "a^(m/n) = ⁿ√(a^m)"),
                step("E", b, m, b ** m),
                step("REWRITE", answer),
                step("Z", answer),
            ]
            return self._pack("rational_exponent_to_radical",
                              f"Write as a radical: {original}", steps,
                              answer)
        var = random.choice(["x", "y", "n", "t"])
        while True:
            n = random.choice([2, 3, 4])
            m = random.randint(1, 9)
            if gcd(m, n) == 1:
                break
        original = f"{var}^({m}/{n})"
        answer = radical_txt(n, var, m)
        steps = [
            step("EXP_RULE_SETUP", original),
            step("FORM_IDENTIFY", "rational_exponent",
                 "a^(m/n) = ⁿ√(a^m)"),
            step("REWRITE", answer),
            step("Z", answer),
        ]
        return self._pack("rational_exponent_to_radical",
                          f"Write as a radical: {original}", steps, answer)

    def _from_radical(self):
        var = random.choice(["x", "y", "n", "t"])
        while True:
            n = random.choice([2, 3, 4])
            m = random.randint(1, 9)
            if gcd(m, n) > 1 or m > n:   # make reduction/integer cases common
                break
        original = radical_txt(n, var, m)
        g = gcd(m, n)
        mr, nr = m // g, n // g
        raw = f"{var}^({m}/{n})"
        if nr == 1:
            answer = var if mr == 1 else f"{var}^{mr}"
        else:
            answer = f"{var}^({mr}/{nr})"
        steps = [
            step("EXP_RULE_SETUP", original),
            step("FORM_IDENTIFY", "rational_exponent",
                 "ⁿ√(a^m) = a^(m/n)"),
            step("REWRITE", raw),
        ]
        if g > 1:
            steps.append(step("F", f"{m}/{n}",
                              f"{mr}/{nr}" if nr > 1 else str(mr)))
            steps.append(step("REWRITE", answer))
        steps.append(step("Z", answer))
        return self._pack("rational_exponent_from_radical",
                          f"Write with a rational exponent: {original}",
                          steps, answer)

    def _evaluate(self):
        n = random.choice([2, 3])
        k = random.randint(2, 6 if n == 3 else 12)
        while True:
            m = random.randint(1, 3)
            if gcd(m, n) == 1:
                break
        base = k ** n
        negative = random.random() < 0.3
        exp_txt = f"(-{m}/{n})" if negative else f"({m}/{n})"
        original = f"{base}^{exp_txt}"
        value = k ** m

        steps = [
            step("EXP_RULE_SETUP", original),
            step("FORM_IDENTIFY", "rational_exponent",
                 "a^(m/n) = (ⁿ√a)^m"),
        ]
        if n == 2:
            steps.append(step("ROOT", base, k))
        else:
            steps.append(step("CBRT", base, k))
        if m > 1:
            steps.append(step("E", k, m, value))
        if negative:
            steps.append(step("EXP_RULE_IDENTIFY", "negative_exponent",
                              "x^(-n) = 1/x^n"))
            answer = f"1/{value}"
        else:
            answer = str(value)
        steps.append(step("Z", answer))
        return self._pack("rational_exponent_evaluate",
                          f"Evaluate: {original}", steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

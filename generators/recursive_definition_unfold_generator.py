"""Evaluate recursive definitions by unfolding to bases and folding back.

Variants:
- ``one_arg``: factorial or ``f(n)=f(n−1)+cn``.
- ``two_arg``: Ackermann ``A(1,n)``/``A(2,n)`` or Euclidean gcd recursion.
- ``on_strings``: length, reversal, or character count by head/tail recursion.
- ``mutual``: mutually recursive even/odd predicates.

Op-codes:
- ``UNFOLD``: replace one recursive call by its defining right-hand side.
- ``BASE``: evaluate a base case.
- ``FOLD``: substitute known recursive values on the way back out.
- ``A`` / ``M``: expose numeric fold arithmetic.
- ``DIVMOD``: expose one Euclidean quotient and remainder.
- ``Z``: exact integer, string, or Boolean result.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "one_arg": (
        "Evaluate the requested value by unfolding to the base case.",
        "Expand every recursive call, then fold the values back.",
        "Use the definition alone to compute the target.",
        "Show the complete unfold-and-fold evaluation.",
        "Follow the one-argument recursion to its base and return.",
    ),
    "two_arg": (
        "Evaluate the two-argument recursion completely.",
        "Unfold according to the stated cases and fold back to the result.",
        "Use only the recursive definition to compute the target call.",
        "Show every recursive descent and resolved return value.",
        "Evaluate the target by the forced recursive path.",
    ),
    "on_strings": (
        "Evaluate the string recursion from head to tail and back.",
        "Unfold to ε, then fold the characters back in order.",
        "Use the recursive string definition to compute the target.",
        "Show every suffix call and its resolved value.",
        "Follow the head-tail recursion through the full string.",
    ),
    "mutual": (
        "Evaluate the mutually recursive predicate.",
        "Alternate the two definitions down to the zero base case.",
        "Use mutual recursion to decide the target truth value.",
        "Unfold every successor call, then fold the Boolean values back.",
        "Trace the even/odd predicates to their shared base cases.",
    ),
}


def factorial_trace(number):
    steps = []

    def evaluate(value):
        if value == 0:
            steps.append(step("BASE", "F(0)", 1))
            return 1
        steps.append(step("UNFOLD", f"F({value})",
                          f"{value}·F({value - 1})"))
        prior = evaluate(value - 1)
        result = value * prior
        steps.append(step("M", value, prior, result))
        steps.append(step("FOLD", f"F({value})", result))
        return result

    return evaluate(number), steps


def additive_trace(symbol, number, base, coefficient):
    steps = []

    def evaluate(value):
        if value == 0:
            steps.append(step("BASE", f"{symbol}(0)", base))
            return base
        addend = coefficient * value
        steps.append(step("UNFOLD", f"{symbol}({value})",
                          f"{symbol}({value - 1}) + {coefficient}·{value}"))
        prior = evaluate(value - 1)
        steps.append(step("M", coefficient, value, addend))
        result = prior + addend
        steps.append(step("A", prior, addend, result))
        steps.append(step("FOLD", f"{symbol}({value})", result))
        return result

    return evaluate(number), steps


def ackermann_trace(first, second):
    steps = []

    def evaluate(m_value, n_value):
        label = f"Ack({m_value}, {n_value})"
        if m_value == 0:
            result = n_value + 1
            steps.append(step("BASE", label, f"{n_value} + 1"))
            steps.append(step("A", n_value, 1, result))
            return result
        if n_value == 0:
            replacement = f"Ack({m_value - 1}, 1)"
            steps.append(step("UNFOLD", label, replacement))
            result = evaluate(m_value - 1, 1)
            steps.append(step("FOLD", label, result))
            return result
        replacement = (f"Ack({m_value - 1}, "
                       f"Ack({m_value}, {n_value - 1}))")
        steps.append(step("UNFOLD", label, replacement))
        inner = evaluate(m_value, n_value - 1)
        result = evaluate(m_value - 1, inner)
        steps.append(step("FOLD", label, result))
        return result

    return evaluate(first, second), steps


def gcd_trace(first, second):
    steps = []
    calls = []
    left, right = first, second
    while right:
        quotient, remainder = divmod(left, right)
        steps.append(step("UNFOLD", f"gcd({left}, {right})",
                          f"gcd({right}, {remainder})"))
        steps.append(step("DIVMOD", left, right,
                          f"{quotient} R {remainder}"))
        calls.append((left, right))
        left, right = right, remainder
    steps.append(step("BASE", f"gcd({left}, 0)", left))
    for call_left, call_right in reversed(calls):
        steps.append(step("FOLD", f"gcd({call_left}, {call_right})", left))
    return left, steps


def string_trace(kind, text, target):
    steps = []

    def evaluate(suffix):
        label = (f"len(\"{suffix}\")" if kind == "length" else
                 f"rev(\"{suffix}\")" if kind == "reverse" else
                 f"count_{target}(\"{suffix}\")")
        if not suffix:
            result = "" if kind == "reverse" else 0
            steps.append(step("BASE", label.replace('\"\"', "ε"),
                              "ε" if kind == "reverse" else 0))
            return result
        head, tail = suffix[0], suffix[1:]
        tail_label = (f"len(\"{tail}\")" if kind == "length" else
                      f"rev(\"{tail}\")" if kind == "reverse" else
                      f"count_{target}(\"{tail}\")")
        if kind == "length":
            replacement = f"1 + {tail_label}"
        elif kind == "reverse":
            replacement = f"{tail_label} + \"{head}\""
        else:
            replacement = f"[{head}={target}] + {tail_label}"
        steps.append(step("UNFOLD", label, replacement))
        tail_value = evaluate(tail)
        if kind == "length":
            result = 1 + tail_value
            steps.append(step("A", 1, tail_value, result))
        elif kind == "reverse":
            result = tail_value + head
        else:
            indicator = 1 if head == target else 0
            result = indicator + tail_value
            steps.append(step("A", indicator, tail_value, result))
        steps.append(step("FOLD", label, result if result != "" else "ε"))
        return result

    return evaluate(text), steps


def mutual_trace(predicate, number):
    steps = []

    def evaluate(which, value):
        label = f"{which}({value})"
        if value == 0:
            result = which == "Even"
            steps.append(step("BASE", label, "true" if result else "false"))
            return result
        other = "Odd" if which == "Even" else "Even"
        steps.append(step("UNFOLD", label, f"{other}({value - 1})"))
        result = evaluate(other, value - 1)
        steps.append(step("FOLD", label, "true" if result else "false"))
        return result

    return evaluate(predicate, number), steps


class RecursiveDefinitionUnfoldGenerator(ProblemGenerator):
    """Generate complete recursive evaluation traces from printed definitions."""

    VARIANTS = ("one_arg", "two_arg", "on_strings", "mutual")
    WEIGHTS = (0.32, 0.22, 0.455, 0.005)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _one_arg(self):
        if random.random() < 0.05:
            number = random.randint(3, 10)
            result, steps = factorial_trace(number)
            body = ("Definition: F(0) = 1; F(n) = n·F(n−1) for n ≥ 1. "
                    f"Target: F({number}).")
        else:
            symbol = random.choice(tuple("fghpqrst"))
            base = random.randint(-20, 20)
            coefficient = random.randint(2, 50)
            number = random.randint(4, 25)
            result, steps = additive_trace(symbol, number, base, coefficient)
            body = (f"Definition: {symbol}(0) = {base}; "
                    f"{symbol}(n) = {symbol}(n−1) + {coefficient}·n for n ≥ 1. "
                    f"Target: {symbol}({number}).")
        return f"{body} {random.choice(QUERIES['one_arg'])}", steps, str(result)

    def _two_arg(self):
        if random.random() < 0.05:
            first = random.choice((1, 2))
            second = random.randint(0, 3 if first == 2 else 7)
            result, steps = ackermann_trace(first, second)
            body = ("Definition: Ack(0, n) = n + 1; "
                    "Ack(m, 0) = Ack(m−1, 1); "
                    "Ack(m, n) = Ack(m−1, Ack(m, n−1)) for m,n ≥ 1. "
                    f"Target: Ack({first}, {second}).")
        else:
            first = random.randint(50, 2000)
            second = random.randint(2, first - 1)
            result, steps = gcd_trace(first, second)
            body = ("Definition: gcd(a, 0) = a; "
                    "gcd(a, b) = gcd(b, a mod b) for b > 0. "
                    f"Target: gcd({first}, {second}).")
        return f"{body} {random.choice(QUERIES['two_arg'])}", steps, str(result)

    def _on_strings(self):
        kind = random.choice(("length", "reverse", "count"))
        alphabet = random.sample(tuple("abcdefghi"), random.randint(3, 7))
        text = "".join(random.choice(alphabet) for _ in range(random.randint(5, 12)))
        target = random.choice(alphabet)
        result, steps = string_trace(kind, text, target)
        if kind == "length":
            definition = "Definition: len(ε) = 0; len(cw) = 1 + len(w)."
            call = f"len(\"{text}\")"
            answer = str(result)
        elif kind == "reverse":
            definition = "Definition: rev(ε) = ε; rev(cw) = rev(w)c."
            call = f"rev(\"{text}\")"
            answer = result
        else:
            definition = (f"Definition: count_{target}(ε) = 0; "
                          f"count_{target}(cw) = [c={target}] + count_{target}(w).")
            call = f"count_{target}(\"{text}\")"
            answer = str(result)
        body = f"{definition} Target: {call}."
        return f"{body} {random.choice(QUERIES['on_strings'])}", steps, answer

    def _mutual(self):
        predicate = random.choice(("Even", "Odd"))
        number = random.randint(1, 80)
        result, steps = mutual_trace(predicate, number)
        body = ("Definition: Even(0) = true; Odd(0) = false; "
                "Even(n+1) = Odd(n); Odd(n+1) = Even(n). "
                f"Target: {predicate}({number}).")
        answer = "true" if result else "false"
        return f"{body} {random.choice(QUERIES['mutual'])}", steps, answer

    def generate(self):
        variant = self.variant or random.choices(self.VARIANTS,
                                                 weights=self.WEIGHTS, k=1)[0]
        if variant == "one_arg":
            problem, steps, answer = self._one_arg()
        elif variant == "two_arg":
            problem, steps, answer = self._two_arg()
        elif variant == "on_strings":
            problem, steps, answer = self._on_strings()
        else:
            problem, steps, answer = self._mutual()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"recursive_definition_unfold_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }

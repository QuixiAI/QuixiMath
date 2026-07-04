import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


SYMBOLS = "ABCDEFGH"
VARIANTS = ["complete", "incomplete", "infeasible"]


def fraction_text(value):
    return str(Fraction(value))


def lengths_text(pairs):
    return ", ".join(f"{symbol}={length}" for symbol, length in pairs)


def kraft_sum(lengths):
    return sum((Fraction(1, 2 ** length) for length in lengths), Fraction(0))


def complete_lengths(target_leaves, max_depth=6):
    leaves = [0]
    while len(leaves) < target_leaves:
        candidates = [
            idx for idx, length in enumerate(leaves)
            if length < max_depth
        ]
        idx = random.choice(candidates)
        length = leaves.pop(idx)
        leaves.extend([length + 1, length + 1])
    return leaves


def feasible_pairs(complete):
    if complete:
        lengths = complete_lengths(random.randint(2, 8))
    else:
        leaves = complete_lengths(random.randint(4, 10))
        keep = random.randint(2, min(8, len(leaves) - 1))
        lengths = random.sample(leaves, keep)
    random.shuffle(lengths)
    symbols = list(SYMBOLS[:len(lengths)])
    return list(zip(symbols, lengths))


def infeasible_pairs():
    for _ in range(100):
        count = random.randint(3, 8)
        lengths = [random.randint(1, 6) for _ in range(count)]
        if kraft_sum(lengths) > 1:
            symbols = list(SYMBOLS[:count])
            return list(zip(symbols, lengths))
    lengths = [1, 1, random.randint(2, 6)]
    return list(zip(SYMBOLS[:len(lengths)], lengths))


def canonical_codes(pairs):
    ordered = sorted(pairs, key=lambda item: (item[1], item[0]))
    code = 0
    previous_length = 0
    codes = {}
    trace = []
    for symbol, length in ordered:
        shift = length - previous_length
        shifted = code << shift
        trace.append((symbol, length, code, shift, shifted))
        codes[symbol] = format(shifted, f"0{length}b")
        code = shifted + 1
        previous_length = length
    return ordered, codes, trace


def codes_text(symbols, codes):
    return ",".join(f"{symbol}:{codes[symbol]}" for symbol in symbols)


class KraftInequalityGenerator(ProblemGenerator):
    """
    Kraft inequality and code-length feasibility for binary prefix codes.

    Variants:
    - complete: feasible lengths with Kraft sum exactly 1.
    - incomplete: feasible lengths with Kraft sum below 1.
    - infeasible: requested lengths with Kraft sum above 1.

    Op-codes used:
    - KRAFT_SETUP / KRAFT_FORMULA / KRAFT_TERM / KRAFT_CHECK
    - KRAFT_CLASSIFY / CANONICAL_ORDER / CANONICAL_SHIFT / CODEWORD
    - E / D / A / S (established/shared): powers, fractions, sums, slack
    - Z: Kraft sum, status, slack/excess, and codewords when feasible
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "complete":
            pairs = feasible_pairs(complete=True)
        elif variant == "incomplete":
            pairs = feasible_pairs(complete=False)
        else:
            pairs = infeasible_pairs()

        symbols = [symbol for symbol, _ in pairs]
        total = kraft_sum(length for _, length in pairs)
        steps = [
            step("KRAFT_SETUP", lengths_text(pairs), "binary prefix code"),
            step("KRAFT_FORMULA", "sum 2^-l_i <= 1"),
        ]
        running = Fraction(0)
        for symbol, length in pairs:
            denominator = 2 ** length
            term = Fraction(1, denominator)
            steps.append(step("E", 2, length, denominator))
            steps.append(step("D", 1, denominator, fraction_text(term)))
            steps.append(step("KRAFT_TERM", symbol, f"l={length}",
                              fraction_text(term)))
            new_running = running + term
            steps.append(step("A", fraction_text(running),
                              fraction_text(term),
                              fraction_text(new_running)))
            running = new_running

        if total <= 1:
            status = "feasible_complete" if total == 1 else "feasible_incomplete"
            slack = 1 - total
            steps.append(step("KRAFT_CHECK", f"sum={fraction_text(total)}",
                              "<=1", "feasible"))
            steps.append(step("S", 1, fraction_text(total),
                              fraction_text(slack)))
            steps.append(step("KRAFT_CLASSIFY", f"slack={fraction_text(slack)}",
                              "complete" if slack == 0 else "incomplete"))
            ordered, codes, trace = canonical_codes(pairs)
            steps.append(step("CANONICAL_ORDER", lengths_text(ordered)))
            for symbol, length, code, shift, shifted in trace:
                steps.append(step("CANONICAL_SHIFT", f"code={code}",
                                  f"left={shift}", shifted))
                steps.append(step("CODEWORD", symbol, f"l={length}",
                                  codes[symbol]))
                steps.append(step("A", shifted, 1, shifted + 1))
            answer = (
                f"Kraft={fraction_text(total)}; status={status}; "
                f"slack={fraction_text(slack)}; "
                f"codes={codes_text(symbols, codes)}"
            )
        else:
            excess = total - 1
            steps.append(step("KRAFT_CHECK", f"sum={fraction_text(total)}",
                              ">1", "infeasible"))
            steps.append(step("S", fraction_text(total), 1,
                              fraction_text(excess)))
            steps.append(step("KRAFT_CLASSIFY", f"excess={fraction_text(excess)}",
                              "no prefix code"))
            answer = (
                f"Kraft={fraction_text(total)}; status=infeasible; "
                f"excess={fraction_text(excess)}"
            )

        steps.append(step("Z", answer))
        problem = (
            "Use Kraft's inequality for a binary prefix code with requested "
            f"lengths {lengths_text(pairs)}. Decide whether the lengths are "
            "feasible; if feasible, give canonical codewords."
        )
        return dict(
            problem_id=jid(),
            operation=f"kraft_inequality_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

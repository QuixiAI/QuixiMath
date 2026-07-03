import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def money(cents):
    return f"{cents // 100}.{cents % 100:02d}"


class FillInStepGenerator(ProblemGenerator):
    """
    Critic-format problems: a complete worked scratchpad is shown with one
    line blanked out (____); the task is to reconstruct the missing line
    exactly. The answer is the missing step verbatim, in pipe format.

    Output vocabulary (see DESIGN.md "Derived Record Formats"):
    - NEED|<fact above, pipe-free>|<fact below, pipe-free> — what the blank
      must connect
    - CHECK|arithmetic|<work>|<value> — the reconstructed arithmetic holds
    - Z|<missing step verbatim>

    Flows: two-step equations, ratio tables, tip totals — the same
    well-understood linear chains the error-spotting format uses.
    """

    MODES = ["equation", "ratio", "tip"]

    def __init__(self, mode=None):
        if mode is not None and mode not in self.MODES:
            raise ValueError(f"mode must be one of {self.MODES} or None")
        self.mode = mode

    def generate(self) -> dict:
        mode = self.mode or random.choice(self.MODES)
        problem_line, lines, blank_idx, need, check = getattr(
            self, f"_{mode}_flow")()

        shown = [f"{i + 1}) {'____' if i == blank_idx else s}"
                 for i, s in enumerate(lines)]
        problem = (
            "One line of the worked solution below has been blanked out "
            "(____). Reconstruct the missing line exactly.\n"
            f"Problem: {problem_line}\n" + "\n".join(shown))

        missing = lines[blank_idx]
        steps = [step("NEED", need[0], need[1])]
        if check is not None:
            steps.append(step("CHECK", "arithmetic", check[0], check[1]))
        steps.append(step("Z", missing))

        return dict(
            problem_id=jid(),
            operation=f"fill_in_step_{mode}",
            problem=problem,
            steps=steps,
            final_answer=missing,
        )

    # ------------------------------------------------------------------

    def _equation_flow(self):
        a = random.randint(2, 9)
        x = random.choice([n for n in range(-9, 10) if n != 0])
        b = random.randint(2, 15)
        sign = random.choice(["+", "-"])
        c = a * x + b if sign == "+" else a * x - b
        rhs = c - b if sign == "+" else c + b
        verb = "subtract" if sign == "+" else "add"
        equation = f"{a}x {sign} {b} = {c}"

        lines = [
            step("EQ_SETUP", equation),
            step("EQ_OP_BOTH", verb, b, f"{a}x", rhs),
            step("EQ_SIMPLIFY", f"{a}x = {rhs}"),
            step("EQ_OP_BOTH", "divide", a, "x", x),
            step("EQ_RESULT", "x", x),
            step("Z", x),
        ]
        blank_idx = random.choice([1, 2, 3])
        op_sym = "-" if verb == "subtract" else "+"
        if blank_idx == 1:
            need = (f"the equation is {equation}",
                    f"line 3 shows {a}x = {rhs}")
            check = (f"{c} {op_sym} {b} = {rhs}", str(rhs))
        elif blank_idx == 2:
            need = (f"line 2 {verb}s {b}, giving {rhs}",
                    f"line 4 divides by {a}")
            check = (f"{c} {op_sym} {b} = {rhs}", str(rhs))
        else:
            need = (f"line 3 shows {a}x = {rhs}",
                    f"line 5 shows x = {x}")
            check = (f"{rhs} ÷ {a} = {x}", str(x))
        return f"Solve for x: {equation}", lines, blank_idx, need, check

    def _ratio_flow(self):
        while True:
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            if a != b and gcd(a, b) == 1:
                break
        k_anchor, k_missing = random.sample(range(2, 13), 2)
        pair1, pair2 = a * k_anchor, b * k_anchor
        known = b * k_missing
        missing_val = a * k_missing
        row1 = f"Flour (cups): {pair1}, ?"
        row2 = f"Sugar (cups): {pair2}, {known}"

        lines = [
            step("RATIO_TABLE", row1, row2),
            step("RATIO_BASE", f"{pair1}:{pair2}", k_anchor, f"{a}:{b}"),
            step("D", known, b, k_missing),
            step("M", a, k_missing, missing_val),
            step("Z", missing_val),
        ]
        blank_idx = random.choice([1, 2, 3])
        if blank_idx == 1:
            need = (f"the complete column is {pair1}:{pair2}",
                    f"line 3 divides {known} by {b}")
            check = (f"gcd of {pair1} and {pair2} is {k_anchor}",
                     str(k_anchor))
        elif blank_idx == 2:
            need = (f"line 2 gives the base ratio {a}:{b}",
                    f"line 4 multiplies {a} by {k_missing}")
            check = (f"{known} ÷ {b} = {k_missing}", str(k_missing))
        else:
            need = (f"line 3 gives the scale factor {k_missing}",
                    f"line 5 answers {missing_val}")
            check = (f"{a} × {k_missing} = {missing_val}", str(missing_val))
        problem_line = ("A recipe mixes flour and sugar in a fixed ratio. "
                        f"Find the missing value.\n{row1}\n{row2}")
        return problem_line, lines, blank_idx, need, check

    def _tip_flow(self):
        tip_pct = random.choice([10, 15, 18, 20, 25])
        bill_dollars = random.randint(18, 240)
        bill = bill_dollars * 100
        tip = bill_dollars * tip_pct
        total = bill + tip
        rate = f"{tip_pct / 100:.2f}"

        lines = [
            step("PERCENT_TO_DEC", f"{tip_pct}%", rate),
            step("M", money(bill), rate, money(tip)),
            step("A", money(bill), money(tip), money(total)),
            step("Z", f"${money(total)}"),
        ]
        blank_idx = random.choice([0, 1, 2])
        if blank_idx == 0:
            need = (f"the tip is {tip_pct}%",
                    f"line 2 multiplies the bill by {rate}")
            check = (f"{tip_pct}% as a decimal is {rate}", rate)
        elif blank_idx == 1:
            need = (f"line 1 converts {tip_pct}% to {rate}",
                    f"line 3 adds the tip {money(tip)} to the bill")
            check = (f"{money(bill)} × {rate} = {money(tip)}", money(tip))
        else:
            need = (f"line 2 gives the tip {money(tip)}",
                    f"line 4 answers ${money(total)}")
            check = (f"{money(bill)} + {money(tip)} = {money(total)}",
                     money(total))
        problem_line = (f"A meal costs ${money(bill)}. Add a {tip_pct}% tip. "
                        f"What is the total including tip?")
        return problem_line, lines, blank_idx, need, check

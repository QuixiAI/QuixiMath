import random

from base_generator import ProblemGenerator
from helpers import step, jid


P = 7
POINTS = [1, 2, 3, 4]


def inv_mod(value):
    return pow(value % P, -1, P)


def eval_line(m0, m1, x):
    return (m0 + m1 * x) % P


def codeword(m0, m1):
    return [eval_line(m0, m1, x) for x in POINTS]


def list_text(values):
    return "[" + ",".join(str(v) for v in values) + "]"


class ReedSolomonGenerator(ProblemGenerator):
    """
    Toy Reed-Solomon RS(4,2) over F_7 by line evaluation.

    Variants:
    - encode: evaluate m(x)=m0+m1*x at x=1,2,3,4
    - correct: recover the unique line agreeing with at least 3 received values

    Op-codes used:
    - RS_SETUP / RS_EVAL / RS_PAIR / RS_LINE / RS_AGREE / RS_CORRECT
    - M / A / S / MOD_REDUCE
    - Z: codeword or corrected message
    """

    VARIANTS = ["encode", "correct"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        m0 = random.randint(0, P - 1)
        m1 = random.randint(1, P - 1)
        if variant == "encode":
            problem, steps, answer = self._encode(m0, m1)
        else:
            problem, steps, answer = self._correct(m0, m1)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"reed_solomon_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _encode(self, m0, m1):
        steps = [step("RS_SETUP", "F_7", f"m(x)={m0}+{m1}x",
                      "points 1,2,3,4")]
        values = []
        for x in POINTS:
            raw = m0 + m1 * x
            y = raw % P
            steps.append(step("M", m1, x, m1 * x))
            steps.append(step("A", m0, m1 * x, raw))
            steps.append(step("MOD_REDUCE", raw, "mod 7", y))
            steps.append(step("RS_EVAL", f"x={x}", y))
            values.append(y)
        answer = f"codeword = {list_text(values)}"
        problem = (
            f"Encode Reed-Solomon RS(4,2) over F_7 with m(x)={m0}+{m1}x "
            "at evaluation points 1,2,3,4."
        )
        return problem, steps, answer

    def _correct(self, m0, m1):
        sent = codeword(m0, m1)
        received = sent[:]
        pos = random.randrange(4)
        received[pos] = (received[pos] + random.randint(1, P - 1)) % P
        steps = [step("RS_SETUP", "F_7", "RS(4,2)", "one error allowed"),
                 step("RS_RECEIVED", list_text(received))]
        best = None
        for i in range(len(POINTS)):
            for j in range(i + 1, len(POINTS)):
                x1, y1 = POINTS[i], received[i]
                x2, y2 = POINTS[j], received[j]
                numerator = (y2 - y1) % P
                denominator = (x2 - x1) % P
                slope = numerator * inv_mod(denominator) % P
                intercept = (y1 - slope * x1) % P
                candidate = codeword(intercept, slope)
                agree = sum(a == b for a, b in zip(candidate, received))
                steps.append(step("RS_PAIR", f"x={x1},{x2}",
                                  f"y={y1},{y2}"))
                steps.append(step("RS_LINE", f"m0={intercept}",
                                  f"m1={slope}", f"agree={agree}"))
                if best is None or agree > best[0]:
                    best = (agree, intercept, slope, candidate)
        _, rec_m0, rec_m1, corrected = best
        err_pos = next(i + 1 for i, (a, b) in enumerate(zip(corrected, received))
                       if a != b)
        steps.append(step("RS_CORRECT", f"position={err_pos}",
                          list_text(corrected)))
        answer = (
            f"message = [{rec_m0},{rec_m1}]; codeword = {list_text(corrected)}; "
            f"error_position = {err_pos}"
        )
        problem = (
            "A Reed-Solomon RS(4,2) word over F_7 is made by evaluating "
            f"m(x)=m0+m1*x at x=1,2,3,4. Received word is {list_text(received)} "
            "with at most one error. Recover the message and corrected codeword."
        )
        return problem, steps, answer

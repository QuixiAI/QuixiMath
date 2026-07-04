import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt


def sub(n):
    return f"({n})"


class RemainderFactorTheoremGenerator(ProblemGenerator):
    """
    Remainder and factor theorems on cubics.

    Variants:
    - remainder:    remainder on division by (x - r) is P(r); evaluate
      it term by term
    - factor_check: is (x - r) a factor? Evaluate P(r), answer Yes/No
      (half the problems are built from a true factor)
    - find_k:       choose k so (x - r) divides x^3 + bx^2 + cx + k;
      evaluate the known part and solve k = -P_known(r)

    Op-codes used:
    - THEOREM: name and instantiated statement (name, statement)
    - SUBST / E / M / A: term-by-term evaluation (established)
    - EVAL: P(r) (established)
    - EQ_OP_BOTH: solve for k in the find_k variant (established)
    - Z: the remainder, Yes/No, or 'k = ...'
    """

    VARIANTS = ["remainder", "factor_check", "find_k"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _eval_steps(steps, coefs, r, var, k_txt=None):
        """Term-by-term evaluation of a cubic at r. Returns the value.
        If k_txt is set, the constant term is symbolic and excluded."""
        deg = len(coefs) - 1
        parts = []
        for i, c in enumerate(coefs):
            p = deg - i
            if k_txt is not None and p == 0:
                parts.append(f"+ {k_txt}")
                continue
            head = {1: "", -1: "-"}.get(c, str(c))
            if p == 0:
                t = str(c) if not parts else \
                    (f"+ {c}" if c > 0 else f"- {-c}")
                parts.append(t if parts else str(c))
                continue
            body = f"{head}{sub(r)}" + ("" if p == 1 else f"^{p}")
            if not parts:
                parts.append(body)
            else:
                parts.append(f"+ {body.lstrip('-')}" if c > 0
                             else f"- {body.lstrip('-')}")
        steps.append(step("SUBST", var, r, " ".join(parts)))

        vals = []
        for i, c in enumerate(coefs):
            p = deg - i
            if k_txt is not None and p == 0:
                continue
            if p >= 2:
                steps.append(step("E", sub(r), p, r ** p))
                if c != 1:
                    steps.append(step("M", c, r ** p, c * r ** p))
                vals.append(c * r ** p)
            elif p == 1:
                steps.append(step("M", c, r, c * r))
                vals.append(c * r)
            else:
                vals.append(c)
        acc = vals[0]
        for v in vals[1:]:
            steps.append(step("A", acc, v, acc + v))
            acc += v
        return acc

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = "x"
        r = random.choice([v for v in range(-3, 4) if v != 0])
        divisor = poly_txt([1, -r], var)

        if variant == "find_k":
            coefs = [random.choice([1, 1, 2]),
                     random.choice([v for v in range(-5, 6) if v != 0]),
                     random.choice([v for v in range(-7, 8) if v != 0])]
            # display polynomial with symbolic constant k
            body = poly_txt([coefs[0], coefs[1], coefs[2], 1], var)
            body = body.rsplit(" ", 1)[0] + " k"
            steps = [step("THEOREM", "factor theorem",
                          f"{divisor} is a factor iff P({r}) = 0")]
            rest = self._eval_steps(steps, coefs + [0], r, var, k_txt="k")
            k = -rest
            steps.append(step("EQ_SETUP", f"{rest} + k = 0", "solve for k"))
            steps.append(step("EQ_OP_BOTH", "subtract", rest, "k", k))
            answer = f"k = {k}"
            steps.append(step("Z", answer))
            problem = (f"Find k so that {divisor} is a factor of "
                       f"P({var}) = {body}.")
            return self._pack("factor_theorem_find_k", problem, steps,
                              answer)

        if variant == "remainder":
            coefs = [random.choice([1, 1, 2, 3, -1, -2]),
                     random.choice([v for v in range(-5, 6) if v != 0]),
                     random.choice([v for v in range(-7, 8) if v != 0]),
                     random.choice([v for v in range(-9, 10) if v != 0])]
            poly = poly_txt(coefs, var)
            steps = [step("THEOREM", "remainder theorem",
                          f"remainder on division by {divisor} is P({r})")]
            value = self._eval_steps(steps, coefs, r, var)
            steps.append(step("EVAL", f"P({r})", value))
            answer = str(value)
            steps.append(step("Z", answer))
            problem = (f"Find the remainder when P({var}) = {poly} is "
                       f"divided by {divisor}.")
            return self._pack("remainder_theorem", problem, steps, answer)

        # factor_check: build from quotient so half are true factors
        while True:
            q = [random.choice([1, 1, 2]),
                 random.choice([v for v in range(-4, 5) if v != 0]),
                 random.choice([v for v in range(-4, 5) if v != 0])]
            rem = 0 if random.random() < 0.5 else \
                random.choice([v for v in range(-9, 10) if v != 0])
            coefs = [q[0], q[1] - r * q[0], q[2] - r * q[1],
                     rem - r * q[2]]
            if 0 not in coefs:
                break
        poly = poly_txt(coefs, var)
        steps = [step("THEOREM", "factor theorem",
                      f"{divisor} is a factor iff P({r}) = 0")]
        value = self._eval_steps(steps, coefs, r, var)
        steps.append(step("EVAL", f"P({r})", value))
        answer = "Yes" if value == 0 else "No"
        steps.append(step("Z", answer))
        problem = f"Is {divisor} a factor of P({var}) = {poly}?"
        return self._pack("factor_theorem_check", problem, steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

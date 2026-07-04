import random
from fractions import Fraction
from math import lcm
from base_generator import ProblemGenerator
from helpers import step, jid

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
           (20, 21, 29)]


def rec_txt(c, b=None):
    """c/(4x) reduced: 1/(2x), 3/(4x); with b set, at x = b."""
    fr = Fraction(c, 4)
    var = "x" if b is None else f"({b})"
    return f"{fr.numerator}/({fr.denominator}{var})"


class ArcLengthGenerator(ProblemGenerator):
    """
    Rectangular arc length L = ∫ √(1 + (dy/dx)²) dx over families
    where 1 + (dy/dx)² is a perfect square, so every answer is exact:
    Pythagorean-slope lines, y = x³/(3c) + c/(4x) (the classic
    "17/12" family), and the catenary (e^x + e^(-x))/2.

    Variants:
    - line: slope p/q from a Pythagorean triple, width a multiple of q
    - cubic_reciprocal: speed x²/c + c/(4x²), exact fraction answers
    - catenary: speed (e^x + e^(-x))/2, symbolic exact answers

    Op-codes used:
    - ARCLEN_FORMULA (shared with the parametric generator)
    - EVAL / REWRITE / INTEG_SETUP / ANTIDERIV / SUBST / S / M /
      FRAC_REDUCE (established)
    - Z: the exact length
    """

    VARIANTS = ["line", "cubic_reciprocal", "catenary"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        formula = step("ARCLEN_FORMULA",
                       "L = ∫ √(1 + (dy/dx)^2) dx")

        if variant == "line":
            p, q, r = random.choice(TRIPLES)
            if random.random() < 0.5:
                p, q = q, p
                # keep q the denominator; r is unchanged
            neg = random.random() < 0.4
            b = random.randint(-5, 5)
            a = random.randint(0, 5)
            n = random.randint(1, 3)
            x2 = a + n * q
            w = n * q
            L = r * n
            m_txt = f"-({p}/{q})x" if neg else f"({p}/{q})x"
            y_txt = m_txt if b == 0 else \
                f"{m_txt} + {b}" if b > 0 else f"{m_txt} - {-b}"
            slope = f"-{p}/{q}" if neg else f"{p}/{q}"
            steps = [
                formula,
                step("EVAL", "dy/dx", slope),
                step("EVAL", f"1 + ({slope})^2 = 1 + {p * p}/{q * q} "
                     f"= {q * q + p * p}/{q * q}"),
                step("EVAL", f"√({r * r}/{q * q}) = {r}/{q}"),
                step("INTEG_SETUP",
                     f"∫ from {a} to {x2} of ({r}/{q}) dx",
                     "arc length"),
                step("S", x2, a, w),
                step("M", f"{r}/{q}", w, L),
            ]
            answer = str(L)
            problem = (f"Find the arc length of y = {y_txt} "
                       f"on [{a}, {x2}].")
        elif variant == "cubic_reciprocal":
            c = random.choice([1, 2, 3])
            a, b = random.choice([(1, 2), (1, 3), (2, 3), (2, 4),
                                  (1, 4)])
            cube = f"x^3/{3 * c}"
            sq = "x^2" if c == 1 else f"x^2/{c}"
            r2 = Fraction(c * c, 16)
            q4 = "x^4" if c == 1 else f"x^4/{c * c}"
            dsq = f"{r2.numerator}/({r2.denominator}x^4)"
            rp = rec_txt(c)
            rp2 = f"{Fraction(c, 4).numerator}/({Fraction(c, 4).denominator}x^2)"
            speed = f"{sq} + {rp2}"
            anti = f"{cube} - {rp}"

            def F(v):
                return Fraction(v ** 3, 3 * c) - Fraction(c, 4 * v)

            def eval_txt(v):
                com = lcm(3 * c, 4 * v)
                n1 = v ** 3 * (com // (3 * c))
                n2 = c * (com // (4 * v))
                return (f"{v ** 3}/{3 * c} - {c}/{4 * v} = "
                        f"{n1}/{com} - {n2}/{com} = {n1 - n2}/{com}",
                        Fraction(n1 - n2, com), f"{n1 - n2}/{com}")
            tb, Fb, rawb = eval_txt(b)
            ta, Fa, rawa = eval_txt(a)
            L = Fb - Fa
            com = lcm(Fb.denominator, Fa.denominator)
            x1 = Fb.numerator * (com // Fb.denominator)
            x2 = Fa.numerator * (com // Fa.denominator)
            steps = [formula,
                     step("EVAL", "dy/dx", f"{sq} - {rp2}"),
                     step("EVAL", f"(dy/dx)^2 = {q4} - 1/2 + {dsq}"),
                     step("EVAL", f"1 + (dy/dx)^2 = {q4} + 1/2 + {dsq}"),
                     step("REWRITE",
                          f"{q4} + 1/2 + {dsq} = ({speed})^2"),
                     step("EVAL", f"√(({speed})^2) = {speed}"),
                     step("INTEG_SETUP",
                          f"∫ from {a} to {b} of ({speed}) dx",
                          "arc length"),
                     step("ANTIDERIV", f"({speed}) dx", anti)]
            for v, txt, raw, val in ((b, tb, rawb, Fb),
                                     (a, ta, rawa, Fa)):
                steps.append(step("SUBST", "x", v, txt))
                if str(val) != raw:
                    steps.append(step("FRAC_REDUCE", raw, str(val)))
            steps.append(step("EVAL",
                              f"{Fb} - ({Fa}) = {x1}/{com} - "
                              f"({x2}/{com}) = {x1 - x2}/{com}"))
            if str(L) != f"{x1 - x2}/{com}":
                steps.append(step("FRAC_REDUCE",
                                  f"{x1 - x2}/{com}", str(L)))
            answer = str(L)
            problem = (f"Find the arc length of y = {cube} + {rp} "
                       f"on [{a}, {b}].")
        else:
            b = random.randint(1, 3)
            sym = random.random() < 0.4
            lo = -b if sym else 0
            eb = "e" if b == 1 else f"e^{b}"
            fb = f"({eb} - e^(-{b}))/2"
            answer = (f"{eb} - e^(-{b})" if sym else fb)
            steps = [
                formula,
                step("EVAL", "dy/dx", "(e^x - e^(-x))/2"),
                step("EVAL", "((e^x - e^(-x))/2)^2 = "
                     "(e^(2x) - 2 + e^(-2x))/4"),
                step("EVAL", "1 + (e^(2x) - 2 + e^(-2x))/4 = "
                     "(e^(2x) + 2 + e^(-2x))/4"),
                step("REWRITE", "(e^(2x) + 2 + e^(-2x))/4 = "
                     "((e^x + e^(-x))/2)^2"),
                step("EVAL", "√(((e^x + e^(-x))/2)^2) = "
                     "(e^x + e^(-x))/2"),
                step("INTEG_SETUP",
                     f"∫ from {lo} to {b} of ((e^x + e^(-x))/2) dx",
                     "arc length"),
                step("ANTIDERIV", "((e^x + e^(-x))/2) dx",
                     "(e^x - e^(-x))/2"),
                step("SUBST", "x", b, fb),
            ]
            if sym:
                steps += [
                    step("SUBST", "x", -b,
                         f"(e^(-{b}) - {eb})/2 = -{fb}"),
                    step("S", fb, f"-{fb}", answer),
                ]
            else:
                steps += [
                    step("SUBST", "x", 0, "(e^0 - e^0)/2 = 0"),
                    step("S", fb, 0, fb),
                ]
            problem = (f"Find the arc length of "
                       f"y = (e^x + e^(-x))/2 on [{lo}, {b}].")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"arc_length_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

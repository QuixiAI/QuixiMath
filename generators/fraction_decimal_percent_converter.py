import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


# Denominators whose fractions terminate as decimals (2^a * 5^b factors)
TERMINATING_DENS = [2, 4, 5, 8, 10, 16, 20, 25, 40, 50]


def percent_value():
    """Exact percent: an integer 1-199 or a half like 37.5 (both /100 exact)."""
    if random.random() < 0.3:
        return Fraction(random.randrange(5, 200, 5), 2)  # 2.5, 5.0 -> 97.5 halves
    value = random.randint(1, 199)
    if value == 100:
        value = 101  # avoid the degenerate 100% -> 1/1 fraction
    return Fraction(value)


class FractionDecimalPercentConverter(ProblemGenerator):
    """Converts between fraction, decimal, and percent with clear human steps.

    All values are constructed to terminate (denominators 2^a*5^b, integer or
    half percents), so every answer is exact with minimal digits — never a
    rounded 0.3333333333 or a padded 112.50%.
    """

    def _pick_terminating_fraction(self):
        den = random.choice(TERMINATING_DENS)
        num = random.randint(1, 3 * den)
        if num % den == 0:
            num += 1  # avoid whole-number results
        return num, den

    def generate(self) -> dict:
        direction = random.choice(["frac_to_dec", "frac_to_percent", "dec_to_frac", "percent_to_dec", "percent_to_frac"])
        steps = []

        if direction == "frac_to_dec":
            num, den = self._pick_terminating_fraction()
            dec_str = dec(Fraction(num, den))
            steps.append(step("FRAC_TO_DEC", f"{num}/{den}", dec_str))
            final_answer = dec_str
            problem = f"Convert {num}/{den} to decimal"
            operation = "convert_frac_to_dec"

        elif direction == "frac_to_percent":
            num, den = self._pick_terminating_fraction()
            frac = Fraction(num, den)
            dec_str = dec(frac)
            percent_str = f"{dec(frac * 100)}%"
            steps.append(step("FRAC_TO_DEC", f"{num}/{den}", dec_str))
            steps.append(step("DEC_TO_PERCENT", dec_str, percent_str))
            final_answer = percent_str
            problem = f"Convert {num}/{den} to percent"
            operation = "convert_frac_to_percent"

        elif direction == "dec_to_frac":
            dec_places = random.choice([1, 2])
            whole = random.randint(0, 9)
            if dec_places == 1:
                frac_digits = random.randint(1, 9)
                dec_str = f"{whole}.{frac_digits}"
            else:
                frac_digits = random.randint(1, 99)
                if frac_digits % 10 == 0:
                    frac_digits += 1  # keep the last decimal digit significant
                dec_str = f"{whole}.{frac_digits:02d}"
            power = 10 ** dec_places
            raw_num = whole * power + frac_digits
            frac = Fraction(raw_num, power)
            steps.append(step("DEC_TO_FRAC", dec_str, f"{raw_num}/{power}"))
            final_answer = f"{frac.numerator}/{frac.denominator}"
            steps.append(step("F", f"{raw_num}/{power}", final_answer))
            problem = f"Convert {dec_str} to fraction"
            operation = "convert_dec_to_frac"

        elif direction == "percent_to_dec":
            pv = percent_value()
            percent_str = f"{dec(pv)}%"
            dec_str = dec(pv / 100)
            steps.append(step("PERCENT_TO_DEC", percent_str, dec_str))
            final_answer = dec_str
            problem = f"Convert {percent_str} to decimal"
            operation = "convert_percent_to_dec"

        else:  # percent_to_frac
            pv = percent_value()
            percent_str = f"{dec(pv)}%"
            dec_val = pv / 100
            dec_str = dec(dec_val)
            # unreduced n/10^k straight from the decimal digits
            digits = len(dec_str.split(".")[1]) if "." in dec_str else 0
            power = 10 ** digits
            raw_num = int(dec_val * power)
            steps.append(step("PERCENT_TO_DEC", percent_str, dec_str))
            steps.append(step("DEC_TO_FRAC", dec_str, f"{raw_num}/{power}"))
            final_answer = f"{dec_val.numerator}/{dec_val.denominator}"
            steps.append(step("F", f"{raw_num}/{power}", final_answer))
            problem = f"Convert {percent_str} to fraction"
            operation = "convert_percent_to_frac"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

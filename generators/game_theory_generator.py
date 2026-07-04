import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class GameTheoryGenerator(ProblemGenerator):
    """
    Mixed equilibrium for zero-sum 2x2 games.

    Op-codes used:
    - GAME_SETUP: row-player payoff matrix
    - EXPECTED_PAYOFF: payoff expression being evaluated
    - MIX_FORMULA: indifference formula for mixed strategies
    - VALUE_FORMULA: minimax value formula
    - A / S / M / D (established/shared): exact arithmetic
    - CHECK: indifference verification
    - Z: row mix, column mix, and value
    """

    def generate(self) -> dict:
        while True:
            a = random.randint(0, 20)
            b = random.randint(0, 20)
            c = random.randint(0, 20)
            d = random.randint(0, 20)
            den = a - b - c + d
            if den == 0:
                continue
            p = Fraction(d - c, den)
            q = Fraction(d - b, den)
            if 0 < p < 1 and 0 < q < 1:
                break

        one_minus_p = 1 - p
        one_minus_q = 1 - q
        q_num = d - b
        p_num = d - c
        den_first = a - b
        den_value = den_first + p_num
        ad = a * d
        bc = b * c
        value_num = ad - bc
        value = Fraction(value_num, den)

        row1_q_term = q * a
        row1_other = one_minus_q * b
        row1_payoff = row1_q_term + row1_other
        row2_q_term = q * c
        row2_other = one_minus_q * d
        row2_payoff = row2_q_term + row2_other
        col1_p_term = p * a
        col1_other = one_minus_p * c
        col1_payoff = col1_p_term + col1_other
        col2_p_term = p * b
        col2_other = one_minus_p * d
        col2_payoff = col2_p_term + col2_other

        steps = [
            step("GAME_SETUP", f"payoffs=({a},{b};{c},{d})",
                 "row player maximizes, column player minimizes"),
            step("MIX_FORMULA", "q=(d-b)/(a-b-c+d)",
                 "p=(d-c)/(a-b-c+d)"),
            step("S", d, b, q_num),
            step("S", d, c, p_num),
            step("S", a, b, den_first),
            step("A", den_first, p_num, den_value),
            step("D", q_num, den_value, fraction_text(q)),
            step("D", p_num, den_value, fraction_text(p)),
            step("EXPECTED_PAYOFF", "row1 against q"),
            step("M", fraction_text(q), a, fraction_text(row1_q_term)),
            step("S", 1, fraction_text(q), fraction_text(one_minus_q)),
            step("M", fraction_text(one_minus_q), b,
                 fraction_text(row1_other)),
            step("A", fraction_text(row1_q_term), fraction_text(row1_other),
                 fraction_text(row1_payoff)),
            step("EXPECTED_PAYOFF", "row2 against q"),
            step("M", fraction_text(q), c, fraction_text(row2_q_term)),
            step("M", fraction_text(one_minus_q), d,
                 fraction_text(row2_other)),
            step("A", fraction_text(row2_q_term), fraction_text(row2_other),
                 fraction_text(row2_payoff)),
            step("EXPECTED_PAYOFF", "col1 against p"),
            step("M", fraction_text(p), a, fraction_text(col1_p_term)),
            step("S", 1, fraction_text(p), fraction_text(one_minus_p)),
            step("M", fraction_text(one_minus_p), c,
                 fraction_text(col1_other)),
            step("A", fraction_text(col1_p_term), fraction_text(col1_other),
                 fraction_text(col1_payoff)),
            step("EXPECTED_PAYOFF", "col2 against p"),
            step("M", fraction_text(p), b, fraction_text(col2_p_term)),
            step("M", fraction_text(one_minus_p), d,
                 fraction_text(col2_other)),
            step("A", fraction_text(col2_p_term), fraction_text(col2_other),
                 fraction_text(col2_payoff)),
            step("VALUE_FORMULA", "v=(ad-bc)/(a-b-c+d)"),
            step("M", a, d, ad),
            step("M", b, c, bc),
            step("S", ad, bc, value_num),
            step("D", value_num, den_value, fraction_text(value)),
            step("CHECK", f"row payoffs={fraction_text(row1_payoff)}",
                 f"column payoffs={fraction_text(col1_payoff)}"),
        ]
        answer = (
            f"row mix=({fraction_text(p)},{fraction_text(one_minus_p)}); "
            f"column mix=({fraction_text(q)},{fraction_text(one_minus_q)}); "
            f"value={fraction_text(value)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For the zero-sum 2x2 payoff matrix [[{a},{b}],[{c},{d}]] "
            "for the row player, compute expected payoffs, the mixed-strategy "
            "equilibrium, and the game value."
        )
        return dict(
            problem_id=jid(),
            operation="game_theory_zero_sum_2x2",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

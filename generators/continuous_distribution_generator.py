import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class ContinuousDistributionGenerator(ProblemGenerator):
    """
    Normalize f(x)=k*x on [0,a], then compute probability, mean, variance.

    Op-codes used:
    - CONT_DIST_SETUP: density family, support, and probability interval
    - POWER_INTEGRAL: identify a power-rule integral being evaluated
    - E / M / D / S (established/shared): exact integration arithmetic
    - Z: k, probability, mean, and variance
    """

    def generate(self) -> dict:
        a = random.randint(2, 20)
        left = random.randint(0, a - 1)
        right = random.randint(left + 1, a)
        a_sq = a ** 2
        integral_x = Fraction(a_sq, 2)
        k = Fraction(1, 1) / integral_x
        right_sq = right ** 2
        left_sq = left ** 2
        interval_diff = right_sq - left_sq
        prob_raw = k * interval_diff
        probability = prob_raw / 2
        a_cubed = a ** 3
        mean_raw = k * a_cubed
        mean = mean_raw / 3
        a_fourth = a ** 4
        second_raw = k * a_fourth
        second_moment = second_raw / 4
        mean_sq = mean * mean
        variance = second_moment - mean_sq
        steps = [
            step("CONT_DIST_SETUP", "f(x)=k*x", f"support=[0,{a}]",
                 f"interval=({left},{right})"),
            step("POWER_INTEGRAL", "int_0^a x dx", "a^2/2"),
            step("E", a, 2, a_sq),
            step("D", a_sq, 2, fraction_text(integral_x)),
            step("D", 1, fraction_text(integral_x), fraction_text(k)),
            step("POWER_INTEGRAL", "int_b^c x dx", "(c^2-b^2)/2"),
            step("E", right, 2, right_sq),
            step("E", left, 2, left_sq),
            step("S", right_sq, left_sq, interval_diff),
            step("M", fraction_text(k), interval_diff, fraction_text(prob_raw)),
            step("D", fraction_text(prob_raw), 2, fraction_text(probability)),
            step("POWER_INTEGRAL", "E[X]", "k*a^3/3"),
            step("E", a, 3, a_cubed),
            step("M", fraction_text(k), a_cubed, fraction_text(mean_raw)),
            step("D", fraction_text(mean_raw), 3, fraction_text(mean)),
            step("POWER_INTEGRAL", "E[X^2]", "k*a^4/4"),
            step("E", a, 4, a_fourth),
            step("M", fraction_text(k), a_fourth, fraction_text(second_raw)),
            step("D", fraction_text(second_raw), 4,
                 fraction_text(second_moment)),
            step("M", fraction_text(mean), fraction_text(mean),
                 fraction_text(mean_sq)),
            step("S", fraction_text(second_moment), fraction_text(mean_sq),
                 fraction_text(variance)),
        ]
        answer = (
            f"k = {fraction_text(k)}, P = {fraction_text(probability)}, "
            f"mean = {fraction_text(mean)}, variance = {fraction_text(variance)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For pdf f(x)=k*x on 0<=x<={a}, first normalize k, then "
            f"compute P({left}<X<{right}), mean, and variance."
        )
        return dict(
            problem_id=jid(),
            operation="continuous_distribution_linear_pdf",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

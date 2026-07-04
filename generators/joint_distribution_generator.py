import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


RHO_VALUES = [
    Fraction(-1, 2),
    Fraction(-1, 3),
    Fraction(-1, 4),
    Fraction(0, 1),
    Fraction(1, 4),
    Fraction(1, 3),
    Fraction(1, 2),
]


def fraction_text(value):
    return str(Fraction(value))


def build_profiles():
    profiles = []
    marginals = {
        Fraction(num, den)
        for den in range(3, 51)
        for num in range(1, den)
    }
    for p in sorted(marginals):
        variance = p * (1 - p)
        for rho in RHO_VALUES:
            p11 = p * p + rho * variance
            p10 = p - p11
            p01 = p - p11
            p00 = 1 - p10 - p01 - p11
            cells = (p00, p01, p10, p11)
            if all(cell >= 0 for cell in cells):
                profiles.append((p, rho, cells))
    return profiles


PROFILES = build_profiles()


class JointDistributionGenerator(ProblemGenerator):
    """
    Binary joint distributions with marginals, conditionals, independence,
    covariance, and exact correlation.

    The generated tables use P(X=1)=P(Y=1), so sqrt(Var(X)Var(Y)) is exactly
    Var(X) and the correlation remains a reduced fraction.

    Op-codes used:
    - JOINT_SETUP: the probability table
    - MARGINAL: which marginal sum is being computed
    - COND_FORMULA: conditional probability ratio
    - INDEP_FORMULA / INDEP_CHECK: product test for independence
    - EXPECTATION: E[X], E[Y], and E[XY] for binary variables
    - COV_FORMULA / CORR_FORMULA: covariance and correlation formulas
    - A / S / M / D / ROOT (established/shared): exact arithmetic
    - Z: marginals, conditional, independence, covariance, correlation
    """

    def generate(self) -> dict:
        _, _, cells = random.choice(PROFILES)
        p00, p01, p10, p11 = cells

        px0 = p00 + p01
        px1 = p10 + p11
        py0 = p00 + p10
        py1 = p01 + p11
        conditional = p11 / px1
        product = px1 * py1
        independent = p11 == product
        covariance = p11 - product
        one_minus_px = 1 - px1
        var_x = px1 * one_minus_px
        one_minus_py = 1 - py1
        var_y = py1 * one_minus_py
        var_product = var_x * var_y
        std_product = var_x
        correlation = covariance / std_product

        steps = [
            step("JOINT_SETUP", "X,Y in {0,1}",
                 f"p00={fraction_text(p00)}, p01={fraction_text(p01)}",
                 f"p10={fraction_text(p10)}, p11={fraction_text(p11)}"),
            step("MARGINAL", "P(X=0)=p00+p01"),
            step("A", fraction_text(p00), fraction_text(p01),
                 fraction_text(px0)),
            step("MARGINAL", "P(X=1)=p10+p11"),
            step("A", fraction_text(p10), fraction_text(p11),
                 fraction_text(px1)),
            step("MARGINAL", "P(Y=0)=p00+p10"),
            step("A", fraction_text(p00), fraction_text(p10),
                 fraction_text(py0)),
            step("MARGINAL", "P(Y=1)=p01+p11"),
            step("A", fraction_text(p01), fraction_text(p11),
                 fraction_text(py1)),
            step("COND_FORMULA",
                 "P(Y=1 given X=1)=P(X=1,Y=1)/P(X=1)"),
            step("D", fraction_text(p11), fraction_text(px1),
                 fraction_text(conditional)),
            step("INDEP_FORMULA",
                 "independent iff P11=P(X=1)P(Y=1)"),
            step("M", fraction_text(px1), fraction_text(py1),
                 fraction_text(product)),
            step("INDEP_CHECK", f"P11={fraction_text(p11)}",
                 f"product={fraction_text(product)}",
                 "yes" if independent else "no"),
            step("EXPECTATION", f"E[X]={fraction_text(px1)}",
                 f"E[Y]={fraction_text(py1)}",
                 f"E[XY]={fraction_text(p11)}"),
            step("COV_FORMULA", "Cov=E[XY]-E[X]E[Y]"),
            step("S", fraction_text(p11), fraction_text(product),
                 fraction_text(covariance)),
            step("S", 1, fraction_text(px1), fraction_text(one_minus_px)),
            step("M", fraction_text(px1), fraction_text(one_minus_px),
                 fraction_text(var_x)),
            step("S", 1, fraction_text(py1), fraction_text(one_minus_py)),
            step("M", fraction_text(py1), fraction_text(one_minus_py),
                 fraction_text(var_y)),
            step("CORR_FORMULA", "rho=Cov/sqrt(VarX*VarY)"),
            step("M", fraction_text(var_x), fraction_text(var_y),
                 fraction_text(var_product)),
            step("ROOT", f"sqrt({fraction_text(var_product)})",
                 fraction_text(std_product)),
            step("D", fraction_text(covariance), fraction_text(std_product),
                 fraction_text(correlation)),
        ]
        answer = (
            f"P_X(0)={fraction_text(px0)}, P_X(1)={fraction_text(px1)}; "
            f"P_Y(0)={fraction_text(py0)}, P_Y(1)={fraction_text(py1)}; "
            f"P(Y=1 given X=1)={fraction_text(conditional)}; "
            f"independent={'yes' if independent else 'no'}; "
            f"covariance={fraction_text(covariance)}; "
            f"correlation={fraction_text(correlation)}"
        )
        steps.append(step("Z", answer))
        problem = (
            "For binary variables X,Y with "
            f"P(X=0,Y=0)={fraction_text(p00)}, "
            f"P(X=0,Y=1)={fraction_text(p01)}, "
            f"P(X=1,Y=0)={fraction_text(p10)}, and "
            f"P(X=1,Y=1)={fraction_text(p11)}, compute the marginals, "
            "P(Y=1 given X=1), independence, covariance, and correlation."
        )
        return dict(
            problem_id=jid(),
            operation="joint_distribution_binary",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

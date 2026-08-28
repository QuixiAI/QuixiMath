"""Compute variances, covariances, and correlations by exact algebra.

Variants: ``var_linear_combo``, ``var_sum_independent``, ``cov_bilinear``,
``corr_from_cov``, ``cov_from_table_3x3``, ``var_difference``, and
``cov_with_sum``. Op-codes: ``COV_RULE``, ``JOINT_ROW``, ``MOMENT_TERM``,
``E``, ``ROOT``, ``M``, ``A``, ``S``, ``D``, ``CHECK``, and ``Z``.
Algebra cases are built from integer standard deviations and exact valid
correlations; table cases use positive dyadic 3×3 pmfs, so all work is exact
and the space is large under five phrasings and varied settings.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
VENUES = ("amber study", "birch survey", "cedar trial", "delta project",
          "ember lab", "forest audit", "granite program", "harbor test",
          "indigo review", "jade pilot", "kestrel study", "lunar trial",
          "maple project", "nova lab", "onyx survey", "pearl audit",
          "quartz program", "river test", "solar review", "topaz pilot",
          "umber study", "violet trial", "willow project", "zephyr lab")
CITIES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston", "Lowell",
          "Madison", "Norfolk", "Olympia", "Portland", "Quincy", "Raleigh",
          "Salem", "Trenton", "Utica", "Ventura", "Wichita", "Yonkers")
NAMES = ("Aiko", "Ben", "Chidi", "Daria", "Elena", "Farah", "Gita", "Hugo",
         "Imani", "Jae", "Kira", "Luca", "Mina", "Noah", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tariq", "Uma", "Vera", "Wen", "Zola")
CORRELATIONS = (Fraction(-3, 4), Fraction(-2, 3), Fraction(-1, 2),
                Fraction(-1, 3), Fraction(0), Fraction(1, 3),
                Fraction(1, 2), Fraction(2, 3), Fraction(3, 4))
QUERIES = {
    "var_linear_combo": (
        "Find the exact variance of L.",
        "Apply the full two-variable variance rule.",
        "Include the covariance cross term when computing Var(L).",
        "What is the variance of the stated linear combination?",
        "Evaluate a²Var(X) + b²Var(Y) + 2abCov(X,Y).",
    ),
    "var_sum_independent": (
        "Find the variance of the independent sum.",
        "Add the component variances using independence.",
        "Compute Var(S) for the stated independent variables.",
        "What is the exact spread of the sum?",
        "Use the zero cross-covariances to combine these variances.",
    ),
    "cov_bilinear": (
        "Find the exact covariance of U and V.",
        "Expand covariance bilinearly in all four coefficients.",
        "Compute Cov(U,V) from the supplied second moments.",
        "What is the covariance of the two linear forms?",
        "Apply acVar(X) + bdVar(Y) + (ad+bc)Cov(X,Y).",
    ),
    "corr_from_cov": (
        "Find the exact correlation of X and Y.",
        "Divide covariance by the product of the standard deviations.",
        "Compute ρ from the stated variances and covariance.",
        "What is Corr(X,Y)?",
        "Take the exact square roots before normalizing covariance.",
    ),
    "cov_from_table_3x3": (
        "Find Cov(X,Y) from the joint table.",
        "Compute E[XY] − E[X]E[Y] exactly.",
        "Use all nine joint masses to determine covariance.",
        "What is the exact covariance of this joint distribution?",
        "Build the three required moments from the 3 by 3 pmf.",
    ),
    "var_difference": (
        "Find Var(X − Y).",
        "Use the minus sign on the covariance cross term.",
        "Compute the exact variance of the difference.",
        "What is Var(X − Y) from these second moments?",
        "Apply Var(X)+Var(Y)−2Cov(X,Y).",
    ),
    "cov_with_sum": (
        "Find Cov(X, X + Y).",
        "Use covariance linearity in the second argument.",
        "Compute the covariance of X with the sum.",
        "What is Cov(X,X+Y)?",
        "Add Var(X) and Cov(X,Y).",
    ),
}


def _setting():
    return random.choice(VENUES), random.choice(CITIES), random.choice(NAMES)


def _moments():
    sx, sy = random.randint(1, 9), random.randint(1, 9)
    correlation = random.choice(CORRELATIONS)
    return Fraction(sx * sx), Fraction(sy * sy), correlation * sx * sy, sx, sy


def _nonzero_coefficient():
    return random.choice([value for value in range(-5, 6) if value])


def _linear_text(a, b, label):
    first = "X" if a == 1 else "−X" if a == -1 else f"{a}X"
    second = "Y" if abs(b) == 1 else f"{abs(b)}Y"
    sign = "+" if b > 0 else "−"
    return f"{label} = {first} {sign} {second}"


def _add_terms(steps, terms):
    running = terms[0]
    for term in terms[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(term),
                          prob_txt(running + term)))
        running += term
    return running


def _base_text(vx, vy, covariance):
    return (f"Var(X) = {prob_txt(vx)}, Var(Y) = {prob_txt(vy)}, and "
            f"Cov(X,Y) = {prob_txt(covariance)}")


class CovarianceAlgebraGenerator(ProblemGenerator):
    """Generate exact covariance and variance algebra exercises."""

    VARIANTS = ("var_linear_combo", "var_sum_independent", "cov_bilinear",
                "corr_from_cov", "cov_from_table_3x3", "var_difference",
                "cov_with_sum")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _linear_variance():
        vx, vy, covariance, _, _ = _moments()
        a, b = _nonzero_coefficient(), _nonzero_coefficient()
        expression = _linear_text(a, b, "L")
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} knows {_base_text(vx, vy, covariance)}. "
                  f"Coefficients are a={a}, b={b}; {expression}.")
        a2, b2 = a * a, b * b
        first, second = a2 * vx, b2 * vy
        cross_coefficient = 2 * a * b
        cross = cross_coefficient * covariance
        steps = [step("COV_RULE", "Var(aX + bY)",
                      "a²Var(X) + b²Var(Y) + 2abCov(X,Y)"),
                 step("E", a, 2, a2), step("M", a2, prob_txt(vx), prob_txt(first)),
                 step("E", b, 2, b2), step("M", b2, prob_txt(vy), prob_txt(second)),
                 step("M", cross_coefficient, prob_txt(covariance), prob_txt(cross))]
        value = _add_terms(steps, (first, second, cross))
        steps.append(step("CHECK", "variance is nonnegative", prob_txt(value)))
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _independent_sum():
        count = random.randint(2, 6)
        variances = tuple(Fraction(random.randint(1, 30)) for _ in range(count))
        venue, city, name = _setting()
        data = ", ".join(f"Var(X{i + 1})={prob_txt(value)}"
                         for i, value in enumerate(variances))
        prefix = (f"At the {venue} in {city}, {name} has independent variables "
                  f"with {data}. Let S = X1 + ... + X{count}.")
        steps = [step("COV_RULE", "independent sum",
                      "Var(S) = Σ Var(X_i); all cross covariances are 0")]
        value = _add_terms(steps, variances)
        steps.append(step("CHECK", "independence removes cross terms", count))
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _bilinear():
        vx, vy, covariance, _, _ = _moments()
        a, b, c, d = (_nonzero_coefficient() for _ in range(4))
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} knows {_base_text(vx, vy, covariance)}. "
                  f"Coefficients are a={a}, b={b}, c={c}, d={d}; "
                  f"{_linear_text(a, b, 'U')}; {_linear_text(c, d, 'V')}.")
        ac, bd, mixed = a * c, b * d, a * d + b * c
        terms = (ac * vx, bd * vy, mixed * covariance)
        steps = [step("COV_RULE", "Cov(aX+bY,cX+dY)",
                      "acVar(X) + bdVar(Y) + (ad+bc)Cov(X,Y)"),
                 step("M", a, c, ac), step("M", ac, prob_txt(vx), prob_txt(terms[0])),
                 step("M", b, d, bd), step("M", bd, prob_txt(vy), prob_txt(terms[1])),
                 step("M", a, d, a * d), step("M", b, c, b * c),
                 step("A", a * d, b * c, mixed),
                 step("M", mixed, prob_txt(covariance), prob_txt(terms[2]))]
        value = _add_terms(steps, terms)
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _correlation():
        vx, vy, covariance, sx, sy = _moments()
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} knows {_base_text(vx, vy, covariance)}.")
        denominator = sx * sy
        value = covariance / denominator
        steps = [step("COV_RULE", "Corr(X,Y)",
                      "Cov(X,Y)/(sqrt(Var(X))·sqrt(Var(Y)))"),
                 step("ROOT", prob_txt(vx), 2, sx),
                 step("ROOT", prob_txt(vy), 2, sy),
                 step("M", sx, sy, denominator),
                 step("D", prob_txt(covariance), denominator, prob_txt(value)),
                 step("CHECK", "correlation lies in [-1,1]", prob_txt(value))]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _joint_table():
        total = 2 ** random.randint(5, 9)
        cuts = sorted(random.sample(range(1, total), 8))
        counts = [cuts[0]]
        counts.extend(cuts[index] - cuts[index - 1]
                      for index in range(1, len(cuts)))
        counts.append(total - cuts[-1])
        rows = [(x, y, Fraction(counts[3 * x + y], total))
                for x in range(3) for y in range(3)]
        venue, city, name = _setting()
        data = "; ".join(f"P(X={x},Y={y})={prob_txt(p)}" for x, y, p in rows)
        prefix = f"At the {venue} in {city}, {name} has joint pmf: {data}."
        steps = [step("JOINT_ROW", f"x={x}, y={y}", prob_txt(p))
                 for x, y, p in rows]

        def moment(label, function):
            terms = []
            local = []
            for x, y, probability in rows:
                factor = function(x, y)
                term = factor * probability
                local.extend([step("M", factor, prob_txt(probability), prob_txt(term)),
                              step("MOMENT_TERM", label, f"x={x}, y={y}",
                                   prob_txt(term))])
                terms.append(term)
            value = _add_terms(local, terms)
            local.append(step("CHECK", label, prob_txt(value)))
            return local, value

        x_steps, ex = moment("E[X]", lambda x, y: x)
        y_steps, ey = moment("E[Y]", lambda x, y: y)
        xy_steps, exy = moment("E[XY]", lambda x, y: x * y)
        product = ex * ey
        covariance = exy - product
        steps.extend(x_steps + y_steps + xy_steps)
        steps.extend([step("COV_RULE", "Cov(X,Y) = E[XY] − E[X]E[Y]"),
                      step("M", prob_txt(ex), prob_txt(ey), prob_txt(product)),
                      step("S", prob_txt(exy), prob_txt(product),
                           prob_txt(covariance))])
        return prefix, steps, prob_txt(covariance)

    @staticmethod
    def _difference():
        vx, vy, covariance, _, _ = _moments()
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} knows {_base_text(vx, vy, covariance)}.")
        doubled = 2 * covariance
        partial = vx + vy
        value = partial - doubled
        steps = [step("COV_RULE", "Var(X − Y)",
                      "Var(X) + Var(Y) − 2Cov(X,Y)"),
                 step("A", prob_txt(vx), prob_txt(vy), prob_txt(partial)),
                 step("M", 2, prob_txt(covariance), prob_txt(doubled)),
                 step("S", prob_txt(partial), prob_txt(doubled), prob_txt(value)),
                 step("CHECK", "variance is nonnegative", prob_txt(value))]
        return prefix, steps, prob_txt(value)

    @staticmethod
    def _with_sum():
        vx, vy, covariance, _, _ = _moments()
        venue, city, name = _setting()
        prefix = (f"At the {venue} in {city}, {name} knows {_base_text(vx, vy, covariance)}.")
        value = vx + covariance
        steps = [step("COV_RULE", "Cov(X,X+Y)", "Var(X) + Cov(X,Y)"),
                 step("A", prob_txt(vx), prob_txt(covariance), prob_txt(value)),
                 step("CHECK", "Cov(X,X) = Var(X)", prob_txt(vx))]
        return prefix, steps, prob_txt(value)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {"var_linear_combo": self._linear_variance,
                   "var_sum_independent": self._independent_sum,
                   "cov_bilinear": self._bilinear,
                   "corr_from_cov": self._correlation,
                   "cov_from_table_3x3": self._joint_table,
                   "var_difference": self._difference,
                   "cov_with_sum": self._with_sum}
        prefix, steps, answer = methods[variant]()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_covariance_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}

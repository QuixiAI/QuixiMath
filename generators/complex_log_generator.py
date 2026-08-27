import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


# Every whole degree has an exact radian form, so the argument table is
# computed rather than enumerated: theta degrees -> (theta/180) * pi.
ANGLES = list(range(0, 360))

POLAR_FORMS = ["cis", "trig", "exp"]

POWER_COEFFS = [c for c in range(-12, 13) if c != 0]

LOG_TEMPLATES = [
    "Find the principal Log and all logarithms of {z}.",
    "For {z}, compute Log(z) and give every value of log(z).",
    "Let {z}. Determine the principal logarithm Log(z) and the full set of "
    "logarithms log(z).",
    "Compute the principal value Log(z) and all values of log(z) for {z}.",
    "Given {z}, state Log(z) and every complex number w with e^w = z.",
]

POWER_TEMPLATES = [
    "Compute {expr} using the principal logarithm.",
    "Find the principal value of {expr}.",
    "Evaluate {expr}, taking the principal branch of the logarithm.",
    "Using Log for the principal branch, give the principal value of {expr}.",
    "What is the principal value of {expr}? Recall w^v = exp(v Log w).",
]


def principal_degrees(theta):
    return theta - 360 if theta > 180 else theta


def pi_text(frac):
    """Render a rational multiple of pi: 1/6 -> pi/6, -5/6 -> -5pi/6."""
    frac = Fraction(frac)
    if frac == 0:
        return "0"
    sign = "-" if frac < 0 else ""
    frac = abs(frac)
    num = "" if frac.numerator == 1 else str(frac.numerator)
    if frac.denominator == 1:
        return f"{sign}{num}pi"
    return f"{sign}{num}pi/{frac.denominator}"


def arg_text(principal):
    """Principal argument in radians, exact, as a multiple of pi."""
    return pi_text(Fraction(principal, 180))


def radius_text(radius):
    if isinstance(radius, Fraction):
        return f"{radius.numerator}/{radius.denominator}"
    return str(radius)


def ln_text(radius):
    return "0" if radius == 1 else f"ln({radius_text(radius)})"


def polar_text(radius, theta, form):
    r_text = radius_text(radius)
    if form == "trig":
        return f"{r_text}(cos {theta} deg + i sin {theta} deg)"
    if form == "exp":
        return f"{r_text} e^(i*{theta} deg)"
    return f"{r_text} cis({theta} deg)"


def principal_log_text(radius, arg):
    ln_part = ln_text(radius)
    if arg == "0":
        return ln_part
    if arg.startswith("-"):
        arg_abs = arg.lstrip("-")
        if ln_part == "0":
            return f"-i*{arg_abs}"
        return f"{ln_part} - i*{arg_abs}"
    if ln_part == "0":
        return f"i*{arg}"
    return f"{ln_part} + i*{arg}"


def multivalued_log_text(radius, arg):
    ln_part = ln_text(radius)
    angle = "2pi*k" if arg == "0" else f"{arg} + 2pi*k"
    if ln_part == "0":
        return f"i*({angle})"
    return f"{ln_part} + i*({angle})"


def unit_base_text(theta):
    """The unit-modulus base as it appears inside a power expression."""
    if theta == 0:
        return "1", "1"
    if theta == 90:
        return "i", "i"
    if theta == 180:
        return "-1", "(-1)"
    if theta == 270:
        return "-i", "(-i)"
    form = random.choice(POLAR_FORMS)
    if form == "trig":
        plain = f"cos {theta} deg + i sin {theta} deg"
        return plain, f"({plain})"
    if form == "exp":
        plain = f"e^(i*{theta} deg)"
        return plain, f"({plain})"
    plain = f"cis({theta} deg)"
    return plain, plain


def exponent_text(coeff):
    if coeff == 1:
        return "i"
    if coeff == -1:
        return "-i"
    return f"{coeff}i"


class ComplexLogGenerator(ProblemGenerator):
    """
    Principal and multivalued complex logarithms, plus principal values of
    purely imaginary powers of unit complex numbers (the i^i family).

    Variants:
    - log: Log(z) and all log(z) values for z = r cis(theta), with r a whole
      number or a simple fraction and theta any whole number of degrees;
      the modulus/argument pair is rendered in cis, cos+i sin, or e^(i theta)
      form.
    - power_ii: principal value of (unit complex number)^(c i), which is the
      real number e^(-c * arg); c = 1 with base i reproduces i^i = e^(-pi/2).

    Op-codes used:
    - LOG_SETUP / LOG_FORMULA / PRINCIPAL_LOG / MULTIVALUED_LOG
    - POWER_SETUP / I_SQUARE / REWRITE for the imaginary-power family
    - ARGUMENT / ANGLE_WRAP: principal argument bookkeeping
    - S (established/shared): subtract 360 degrees when wrapping
    - M (established/shared): multiply the exponent coefficient by the argument
    - Z: final logarithm or power value
    """

    VARIANTS = ["log", "power_ii"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(["log", "log", "power_ii"])
        if variant == "log":
            problem, steps, answer = self._generate_log()
        else:
            problem, steps, answer = self._generate_power_ii()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"complex_log_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _random_radius(self):
        if random.random() < 0.72:
            return random.randint(1, 400)
        den = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        while True:
            num = random.randint(1, 6 * den)
            if math.gcd(num, den) == 1:
                return Fraction(num, den)

    def _generate_log(self):
        radius = self._random_radius()
        theta = random.choice(ANGLES)
        principal = principal_degrees(theta)
        arg = arg_text(principal)
        form = random.choice(POLAR_FORMS)
        z_text = polar_text(radius, theta, form)
        steps = [
            step("LOG_SETUP", f"z={radius_text(radius)} cis({theta} deg)"),
        ]
        if theta > 180:
            steps.append(step("S", theta, 360, principal))
            steps.append(step("ANGLE_WRAP", f"{theta} deg",
                              f"{principal} deg"))
        else:
            steps.append(step("ARGUMENT", f"{theta} deg",
                              f"{principal} deg"))
        principal_text = principal_log_text(radius, arg)
        multivalued_text = multivalued_log_text(radius, arg)
        steps.extend([
            step("LOG_FORMULA", "log z = ln r + i(arg + 2pi*k)"),
            step("PRINCIPAL_LOG", principal_text),
            step("MULTIVALUED_LOG", multivalued_text, "k in Z"),
        ])
        answer = (
            f"Log(z) = {principal_text}; "
            f"log(z) = {multivalued_text}, k in Z"
        )
        problem = random.choice(LOG_TEMPLATES).format(z=f"z = {z_text}")
        return problem, steps, answer

    def _generate_power_ii(self):
        theta = random.choice(ANGLES)
        coeff = random.choice(POWER_COEFFS)
        base_plain, base_display = unit_base_text(theta)
        exp_text = exponent_text(coeff)
        if exp_text == "i":
            expr = f"{base_display}^i"
        else:
            expr = f"{base_display}^({exp_text})"

        principal = principal_degrees(theta)
        arg = arg_text(principal)
        log_text = principal_log_text(1, arg)
        exponent = Fraction(-coeff * principal, 180)
        exp_result = pi_text(exponent)
        answer = "1" if exponent == 0 else f"e^({exp_result})"

        steps = [step("POWER_SETUP", expr, "principal logarithm")]
        if base_plain != f"cis({theta} deg)":
            steps.append(step("REWRITE", f"{base_plain} = cis({theta} deg)"))
        if theta > 180:
            steps.append(step("S", theta, 360, principal))
            steps.append(step("ANGLE_WRAP", f"{theta} deg",
                              f"{principal} deg"))
        else:
            steps.append(step("ARGUMENT", f"{theta} deg",
                              f"{principal} deg"))
        steps.append(step("PRINCIPAL_LOG", f"Log(z) = {log_text}"))
        log_factor = (f"({log_text})" if log_text.startswith("-")
                      else log_text)
        steps.append(step("REWRITE", f"{expr} = exp({exp_text}*Log(z))",
                          f"exp({exp_text}*{log_factor})"))
        if principal != 0:
            steps.append(step("I_SQUARE", "i^2", "-1"))
        steps.append(step("M", -coeff, arg, exp_result))
        steps.append(step("REWRITE", f"exp({exp_result})", answer))
        problem = random.choice(POWER_TEMPLATES).format(expr=expr)
        return problem, steps, answer

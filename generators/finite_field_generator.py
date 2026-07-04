import random

from base_generator import ProblemGenerator
from helpers import step, jid


def trim(poly):
    poly = poly[:]
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def degree(poly):
    return len(trim(poly)) - 1


def degree_text(power):
    if power == 0:
        return "x^0"
    if power == 1:
        return "x"
    return f"x^{power}"


def term_text(coef, power):
    if coef == 0:
        return ""
    if power == 0:
        return str(coef)
    variable = "x" if power == 1 else f"x^{power}"
    if coef == 1:
        return variable
    return f"{coef}{variable}"


def poly_text(poly):
    poly = trim(poly)
    terms = []
    for power in range(len(poly) - 1, -1, -1):
        text = term_text(poly[power], power)
        if text:
            terms.append(text)
    return " + ".join(terms) if terms else "0"


def random_poly(max_degree, modulus):
    degree_value = random.randint(1, max_degree)
    poly = [random.randint(0, modulus - 1) for _ in range(degree_value + 1)]
    poly[-1] = random.randint(1, modulus - 1)
    return poly


def add_mod(f, g, modulus):
    size = max(len(f), len(g))
    result = []
    for idx in range(size):
        result.append(((f[idx] if idx < len(f) else 0) +
                       (g[idx] if idx < len(g) else 0)) % modulus)
    return trim(result)


def multiply_mod(f, g, modulus):
    raw = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            raw[i + j] += a * b
    return trim([value % modulus for value in raw])


def gf2_divide(dividend, divisor):
    remainder = trim(dividend)
    quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
    div_degree = degree(divisor)
    while not (len(remainder) == 1 and remainder[0] == 0):
        rem_degree = degree(remainder)
        if rem_degree < div_degree:
            break
        shift = rem_degree - div_degree
        quotient[shift] ^= 1
        for i, coeff in enumerate(divisor):
            if coeff == 0:
                continue
            remainder[i + shift] ^= coeff
        remainder = trim(remainder)
    return trim(quotient), trim(remainder)


class FiniteFieldGenerator(ProblemGenerator):
    """
    Polynomial arithmetic over prime fields and GF(2) polynomial division.

    Variants:
    - zp: add and multiply two polynomials in Z_p[x]
    - gf2_division: divide binary polynomials using XOR cancellation

    Op-codes used:
    - FIELD_SETUP / POLY_INPUT: field and operands
    - POLY_ADD_START / POLY_MUL_START / POLY_COEFF / POLY_ACCUM: arithmetic
    - POLYDIV_SETUP / DIV_TERM / POLY_REMAINDER / QUOTIENT / R: division
    - GF2_XOR: coefficient XOR in GF(2)
    - A / M / MOD_REDUCE (established/shared): modular arithmetic
    - Z: final polynomial result
    """

    VARIANTS = ["zp", "gf2_division"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "zp":
            problem, steps, answer = self._generate_zp()
        else:
            problem, steps, answer = self._generate_gf2_division()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"finite_field_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_zp(self):
        modulus = random.choice([2, 3, 5, 7])
        f = random_poly(3, modulus)
        g = random_poly(3, modulus)
        f_text = poly_text(f)
        g_text = poly_text(g)
        steps = [
            step("FIELD_SETUP", f"Z_{modulus}[x]", f"mod {modulus}"),
            step("POLY_INPUT", "f(x)", f_text),
            step("POLY_INPUT", "g(x)", g_text),
            step("POLY_ADD_START", f"max degree {max(degree(f), degree(g))}"),
        ]

        sum_coeffs = []
        for power in range(max(len(f), len(g))):
            a = f[power] if power < len(f) else 0
            b = g[power] if power < len(g) else 0
            raw = a + b
            reduced = raw % modulus
            steps.append(step("A", a, b, raw))
            steps.append(step("MOD_REDUCE", raw, f"mod {modulus}", reduced))
            steps.append(step("POLY_COEFF", "sum", degree_text(power),
                              reduced))
            sum_coeffs.append(reduced)
        sum_coeffs = trim(sum_coeffs)

        raw_product = [0] * (len(f) + len(g) - 1)
        steps.append(step("POLY_MUL_START", f"degree {degree(f)}",
                          f"degree {degree(g)}"))
        for i, a in enumerate(f):
            for j, b in enumerate(g):
                product = a * b
                power = i + j
                previous = raw_product[power]
                total = previous + product
                steps.append(step("M", a, b, product))
                steps.append(step("A", previous, product, total))
                raw_product[power] = total
                steps.append(step("POLY_ACCUM", degree_text(power), total))

        product_coeffs = []
        for power, value in enumerate(raw_product):
            reduced = value % modulus
            steps.append(step("MOD_REDUCE", value, f"mod {modulus}",
                              reduced))
            steps.append(step("POLY_COEFF", "product", degree_text(power),
                              reduced))
            product_coeffs.append(reduced)
        product_coeffs = trim(product_coeffs)

        answer = (
            f"sum = {poly_text(sum_coeffs)}; "
            f"product = {poly_text(product_coeffs)}"
        )
        problem = (
            f"Over Z_{modulus}, compute (f + g) and (f * g) for "
            f"f(x) = {f_text} and g(x) = {g_text}."
        )
        return problem, steps, answer

    def _generate_gf2_division(self):
        divisor_degree = random.choice([2, 3])
        divisor = [1]
        divisor.extend(random.randint(0, 1) for _ in range(divisor_degree - 1))
        divisor.append(1)
        dividend_degree = random.randint(divisor_degree + 1, 6)
        dividend = [random.randint(0, 1) for _ in range(dividend_degree + 1)]
        dividend[-1] = 1

        dividend_text = poly_text(dividend)
        divisor_text = poly_text(divisor)
        steps = [
            step("FIELD_SETUP", "GF(2)[x]", "addition is XOR"),
            step("POLYDIV_SETUP", dividend_text, divisor_text),
        ]

        remainder = trim(dividend)
        quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
        div_degree = degree(divisor)
        while not (len(remainder) == 1 and remainder[0] == 0):
            rem_degree = degree(remainder)
            if rem_degree < div_degree:
                break
            shift = rem_degree - div_degree
            steps.append(step("DIV_TERM", degree_text(rem_degree),
                              degree_text(div_degree), degree_text(shift)))
            before_q = quotient[shift]
            quotient[shift] ^= 1
            steps.append(step("GF2_XOR", f"quotient {degree_text(shift)}",
                              f"{before_q} xor 1", quotient[shift]))
            for idx, coeff in enumerate(divisor):
                if coeff == 0:
                    continue
                power = idx + shift
                before = remainder[power]
                after = before ^ coeff
                steps.append(step("GF2_XOR", f"remainder {degree_text(power)}",
                                  f"{before} xor {coeff}", after))
                remainder[power] = after
            remainder = trim(remainder)
            steps.append(step("POLY_REMAINDER", poly_text(remainder)))

        quotient = trim(quotient)
        remainder = trim(remainder)
        quotient_text = poly_text(quotient)
        remainder_text = poly_text(remainder)
        steps.extend([
            step("QUOTIENT", quotient_text),
            step("R", remainder_text),
        ])
        answer = f"quotient = {quotient_text}; remainder = {remainder_text}"
        problem = (
            f"Over GF(2), divide {dividend_text} by {divisor_text}. "
            "Use XOR for coefficient arithmetic."
        )
        return problem, steps, answer

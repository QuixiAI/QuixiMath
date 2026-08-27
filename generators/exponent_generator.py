import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


# --- Hand-friendly enumerations for exponent evaluation ---------------------
# Every instance below is a power a human can expand as repeated
# multiplication: the base cap shrinks as the exponent grows so the running
# product never turns into digit grinding.

_INT_BASE_CAP = {2: 99, 3: 30, 4: 20, 5: 15, 6: 10, 7: 7, 8: 5, 9: 4, 10: 3}

INT_POWERS = [(b, e) for e in sorted(_INT_BASE_CAP)
              for b in range(2, _INT_BASE_CAP[e] + 1)]


def _frac_powers():
    out = []
    for q in range(2, 13):
        for p in range(1, 3 * q + 1):
            if p % q == 0 or Fraction(p, q).denominator != q:
                continue
            for e in range(2, 7):
                v = Fraction(p, q) ** e
                if v.denominator <= 100000 and v.numerator <= 100000:
                    out.append((p, q, e))
    return out


FRACTION_POWERS = _frac_powers()


def _dec_powers():
    out = []
    for k in list(range(2, 50)):
        if k % 10 == 0:
            continue
        base = Fraction(k, 10)
        for e in range(2, 5):
            v = base ** e
            txt = dec(v)
            places = len(txt.split(".")[1]) if "." in txt else 0
            if places <= 4 and v <= 5000:
                out.append((k, e))
    return out


DECIMAL_POWERS = _dec_powers()


def _pair_powers(limit, combine):
    out = []
    for a in range(2, 16):
        for m in range(2, 6):
            pa = a ** m
            if pa > 100000:
                continue
            for b in range(2, 16):
                for n in range(2, 6):
                    if (a, m) == (b, n):
                        continue
                    pb = b ** n
                    if pb > 100000:
                        continue
                    if abs(combine(pa, pb)) <= limit:
                        out.append((a, m, b, n))
    return out


PRODUCT_POWERS = _pair_powers(1000000, lambda x, y: x * y)
SUM_POWERS = _pair_powers(1000000, lambda x, y: x + y)

EXP_NAMES = [
    "Ava", "Ben", "Camila", "Dmitri", "Elena", "Farid", "Grace", "Hassan",
    "Imani", "Jonas", "Kavya", "Liam", "Mei", "Noor", "Omar", "Priya",
    "Quentin", "Rosa", "Samir", "Tara", "Ugo", "Vera", "Wesley", "Ximena",
    "Yusuf", "Zara", "Aiko", "Bruno", "Carmen", "Devi", "Ewan", "Fatima",
    "Gustavo", "Hana", "Ines", "Jamal", "Kiran", "Lucia", "Malik", "Nadia",
    "Oscar", "Petra", "Rafael", "Sofia", "Tomas", "Anika", "Bilal",
    "Cleo", "Dario", "Esme", "Felix", "Gita", "Henrik", "Isla", "Javier",
]

EXP_SETTINGS = [
    "algebra class", "math club", "study hall", "the library",
    "a tutoring session", "the homework desk", "a review workshop",
    "the school lab", "an exam-prep group", "the community center",
    "a classroom warm-up", "an online lesson", "a practice quiz",
    "the learning center", "a peer-study group", "the summer program",
    "the evening course", "a skills clinic", "the revision session",
    "a whiteboard challenge", "the problem-solving circle",
    "the after-school program", "a textbook review", "the math fair",
]

_BARE_TEMPLATES = [
    "Evaluate: {expr}",
    "Compute the value of {expr}.",
    "What is the value of {expr}?",
    "Simplify {expr} to a single number.",
    "Find the exact value of {expr}.",
    "Work out {expr} by hand, without a calculator.",
]

_NAMED_TEMPLATES = [
    "{name} needs to evaluate {expr} without a calculator. What is the value?",
    "A worksheet asks {name} to evaluate {expr}. What is the value?",
    "{name} is checking homework and reaches {expr}. What number does that equal?",
    "In a math club puzzle {name} must evaluate {expr}. Give the value.",
    "{name} writes {expr} on the board and asks for its value. Evaluate it.",
    "Before a quiz {name} practises {expr}. What single number is it equal to?",
    "{name} keeps a scratchpad of powers and writes down {expr}. Evaluate it.",
]

_RULE_TEMPLATES = [
    "Simplify: {expr}",
    "Simplify the expression {expr}.",
    "Simplify {expr} to one power.",
    "At {place}, {name} is asked to simplify {expr}.",
    "{name} sees {expr} during {place}. Simplify the expression.",
    "A review card at {place} shows {expr}. Simplify it.",
    "For a warm-up at {place}, simplify {expr}.",
    "{name} writes {expr} on a scratchpad. Simplify it to one power.",
    "During {place}, the expression is {expr}. Simplify it.",
    "Simplify the power expression {expr} for {name} at {place}.",
]

_SCI_TEMPLATES = {
    "to_scientific": [
        "Write in scientific notation: {expr}",
        "Write {expr} in scientific notation.",
        "Convert to scientific notation: {expr}",
        "At {place}, {name} writes {expr}. Express it in scientific notation.",
        "A measurement card at {place} shows {expr}. Write it in scientific notation.",
        "{name} needs {expr} in scientific notation for a report at {place}.",
        "For a review at {place}, convert {expr} to scientific notation.",
        "Express the standard-form number {expr} in scientific notation.",
    ],
    "from_scientific": [
        "Write in standard form: {expr}",
        "Write {expr} in standard form.",
        "Convert to standard form: {expr}",
        "At {place}, {name} sees {expr}. Express it in standard form.",
        "A data card at {place} gives {expr}. Write it in standard form.",
        "{name} needs the standard form of {expr} for work at {place}.",
        "For a review at {place}, convert {expr} to standard form.",
        "Express the scientific-notation number {expr} in standard form.",
    ],
    "multiply": [
        "Multiply: {expr}",
        "Multiply the scientific-notation numbers: {expr}",
        "At {place}, {name} must Multiply {expr}.",
        "A review card at {place} says: Multiply {expr}.",
        "{name} is checking a calculation. Multiply {expr}.",
        "For a warm-up at {place}, Multiply {expr}.",
        "Multiply {expr} and give the result in scientific notation.",
        "During {place}, {name} is asked to Multiply {expr}.",
    ],
    "divide": [
        "Divide: {expr}",
        "Divide the scientific-notation numbers: {expr}",
        "At {place}, {name} must Divide {expr}.",
        "A review card at {place} says: Divide {expr}.",
        "{name} is checking a calculation. Divide {expr}.",
        "For a warm-up at {place}, Divide {expr}.",
        "Divide {expr} and give the result in scientific notation.",
        "During {place}, {name} is asked to Divide {expr}.",
    ],
}

_ROOT_TEMPLATES = {
    "evaluate": [
        "At {place}, {name} gets the prompt: Evaluate {expr}.",
        "{name} is working at {place}. Evaluate {expr} exactly.",
        "At {place}, {name} asks: What is the exact value of {expr}?",
        "At {place}, {name} is asked to evaluate {expr}.",
        "A review card at {place} shows {expr}. Evaluate it.",
        "{name} sees {expr} during {place}. Find its exact value.",
        "For a warm-up at {place}, evaluate {expr}.",
        "During {place}, {name} writes down {expr}. What does it equal?",
        "{name} checks a roots table at {place}. Evaluate {expr} exactly.",
        "A practice sheet for {name} in {place} asks for the value of {expr}.",
        "While studying at {place}, {name} finds {expr}. Evaluate it.",
        "At {place}, the radical on {name}'s worksheet is {expr}. Find its value.",
    ],
    "simplify": [
        "At {place}, {name} gets the prompt: Simplify {expr}.",
        "{name} is working at {place}. Simplify the radical {expr}.",
        "At {place}, {name} must Simplify {expr} completely.",
        "At {place}, {name} is asked to Simplify {expr}.",
        "A review card at {place} shows {expr}. Simplify it.",
        "{name} sees {expr} during {place}. Simplify the radical.",
        "For a warm-up at {place}, Simplify {expr}.",
        "During {place}, {name} writes down {expr}. Simplify it.",
        "{name} checks a radical exercise at {place}. Simplify {expr} completely.",
        "A practice sheet for {name} in {place} asks to Simplify {expr}.",
        "While studying at {place}, {name} finds {expr}. Simplify the result.",
        "At {place}, the radical on {name}'s worksheet is {expr}. Simplify it.",
    ],
}


def _context_phrase(templates, expr):
    return random.choice(templates).format(
        expr=expr, name=random.choice(EXP_NAMES),
        place=random.choice(EXP_SETTINGS))


def _val_text(v, style):
    """Render an exact value: integer, reduced fraction, or exact decimal."""
    if style == "dec":
        return dec(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{v.numerator}/{v.denominator}"


def _base_text(b, style):
    """Base as it appears inside a power, parenthesized when it needs to be."""
    t = _val_text(b, style)
    return f"({t})" if (b < 0 or "/" in t) else t


def _power_text(b, e, style):
    return f"{_base_text(b, style)}^{e}"


class ExponentEvaluationGenerator(ProblemGenerator):
    """
    Generates exponent evaluation problems: expand a power (or a short
    product / sum of powers) as repeated multiplication and combine.

    Families (all hand-expandable; base caps shrink as the exponent grows):
    - integer bases 2..99 and their negatives, exponents 2..10
    - fraction bases p/q (q <= 12), exponents 2..6, exact reduced answers
    - decimal bases k/10, exponents 2..5, exact terminating answers
    - products of two powers  (operation ``exponent_evaluation_product``)
    - sums / differences of two powers (``exponent_evaluation_sum``)

    Presentation is widened with six bare phrasings and five named
    worksheet phrasings over 45 names.

    Op-codes used:
    - EXP_SETUP: Set up the exponent expression (base, exponent)
    - EXP_EXPAND: Expand as repeated multiplication (expansion_string)
    - EXP_PARTIAL: Show partial products (current_product, next_factor, new_product)
    - REWRITE: the expression with each power replaced by its value
    - M / A / S: combine the evaluated powers
    - Z: Final answer
    """

    FAMILIES = ["int", "neg_int", "fraction", "decimal", "product", "sum"]
    FAMILY_WEIGHTS = {"int": 1, "neg_int": 1, "fraction": 1, "decimal": 1,
                      "product": 3, "sum": 3}

    def __init__(self, allow_negative_base: bool = True,
                 max_exponent: int = 10):
        """
        Initialize generator.

        Args:
            allow_negative_base: Whether to allow negative bases
            max_exponent: Maximum exponent value
        """
        self.allow_negative_base = allow_negative_base
        self.max_exponent = max_exponent
        self._int = [p for p in INT_POWERS if p[1] <= max_exponent]
        self._frac = [p for p in FRACTION_POWERS if p[2] <= max_exponent]
        self._dec = [p for p in DECIMAL_POWERS if p[1] <= max_exponent]
        self._prod = [p for p in PRODUCT_POWERS
                      if p[1] <= max_exponent and p[3] <= max_exponent]
        self._sum = [p for p in SUM_POWERS
                     if p[1] <= max_exponent and p[3] <= max_exponent]
        if not self._int:  # pragma: no cover - defensive
            raise ValueError("max_exponent leaves no hand-friendly powers")

    # -- helpers ---------------------------------------------------------
    def _sign(self):
        """A random sign, or +1 when negative bases are switched off."""
        if self.allow_negative_base and random.choice([True, False]):
            return -1
        return 1

    def _phrase(self, expr):
        if random.random() < 0.15:
            return random.choice(_BARE_TEMPLATES).format(expr=expr)
        return random.choice(_NAMED_TEMPLATES).format(
            expr=expr, name=random.choice(EXP_NAMES))

    def _expand_steps(self, base, exp, style):
        """EXP_SETUP + EXP_EXPAND + the chain of partial products."""
        btxt = _val_text(base, style)
        factor = f"({btxt})" if (base < 0 or "/" in btxt) else btxt
        steps = [step("EXP_SETUP", btxt, exp),
                 step("EXP_EXPAND", " × ".join([factor] * exp))]
        current = base
        for _ in range(1, exp):
            new_product = current * base
            steps.append(step("EXP_PARTIAL", _val_text(current, style), btxt,
                              _val_text(new_product, style)))
            current = new_product
        return steps, current

    # -- generation ------------------------------------------------------
    def generate(self) -> dict:
        families = [f for f in self.FAMILIES
                    if f != "neg_int" or self.allow_negative_base]
        weights = [self.FAMILY_WEIGHTS[f] for f in families]
        family = random.choices(families, weights=weights)[0]

        if family in ("int", "neg_int", "fraction", "decimal"):
            return self._single(family)
        return self._combination(family)

    def _single(self, family):
        if family == "int":
            b, e = random.choice(self._int)
            base, style = Fraction(b), "int"
        elif family == "neg_int":
            b, e = random.choice(self._int)
            base, style = Fraction(-b), "int"
        elif family == "fraction":
            p, q, e = random.choice(self._frac)
            base, style = Fraction(self._sign() * p, q), "frac"
        else:
            k, e = random.choice(self._dec)
            base, style = Fraction(self._sign() * k, 10), "dec"

        steps, value = self._expand_steps(base, e, style)
        answer = _val_text(value, style)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="exponent_evaluation",
            problem=self._phrase(_power_text(base, e, style)),
            steps=steps,
            final_answer=answer,
        )

    def _combination(self, family):
        pool = self._prod if family == "product" else self._sum
        a, m, b, n = random.choice(pool)
        base_a = Fraction(self._sign() * a)
        base_b = Fraction(self._sign() * b)
        if family == "product":
            sym, opcode = "·", "M"
        else:
            sym = random.choice(["+", "-"])
            opcode = "A" if sym == "+" else "S"

        steps = []
        va = vb = None
        part, va = self._expand_steps(base_a, m, "int")
        steps.extend(part)
        part, vb = self._expand_steps(base_b, n, "int")
        steps.extend(part)

        ta, tb = _val_text(va, "int"), _val_text(vb, "int")
        shown_b = f"({tb})" if vb < 0 else tb
        steps.append(step("REWRITE", f"{ta} {sym} {shown_b}"))
        if family == "product":
            value = va * vb
        elif sym == "+":
            value = va + vb
        else:
            value = va - vb
        answer = _val_text(value, "int")
        steps.append(step(opcode, ta, tb, answer))
        steps.append(step("Z", answer))

        expr = (f"{_power_text(base_a, m, 'int')} {sym} "
                f"{_power_text(base_b, n, 'int')}")
        return dict(
            problem_id=jid(),
            operation=f"exponent_evaluation_{family}",
            problem=self._phrase(expr),
            steps=steps,
            final_answer=answer,
        )


class ExponentRulesGenerator(ProblemGenerator):
    """
    Generates exponent rule problems.

    Rules covered:
    - Product rule: x^a · x^b = x^(a+b)
    - Quotient rule: x^a / x^b = x^(a-b)
    - Power rule: (x^a)^b = x^(ab)
    - Negative exponents: x^(-n) = 1/x^n
    - Zero exponent: x^0 = 1

    Op-codes used:
    - EXP_RULE_SETUP: Set up the expression (expression_string)
    - EXP_RULE_IDENTIFY: Identify the rule being used (rule_name)
    - EXP_RULE_APPLY: Apply the rule (operation, exp1, exp2, result_exp)
    - EXP_RULE_SIMPLIFY: Simplify the result (simplified_expression)
    - Z: Final answer
    """

    RULES = ['product', 'quotient', 'power', 'negative', 'zero']
    BASE_STYLES = ['variable', 'decimal', 'fraction']

    def __init__(self, rule: str = None, base_style: str = 'variable'):
        """
        Initialize generator.

        Args:
            rule: One of 'product', 'quotient', 'power', 'negative', 'zero' or None for random
            base_style: 'variable' (x, y, ...), 'decimal' ((0.4), ...), or
                'fraction' ((2/3), ...) — the rules are identical whatever
                the base looks like, which is the point of the variant.
        """
        if rule is not None and rule not in self.RULES:
            raise ValueError(f"Invalid rule: {rule}. Must be one of {self.RULES} or None.")
        if base_style not in self.BASE_STYLES:
            raise ValueError(f"Invalid base_style: {base_style}. Must be one of {self.BASE_STYLES}.")
        self.rule = rule
        self.base_style = base_style
        self.op_symbol = base_style

    def _pick_base(self):
        """Return one nonzero hand-friendly base in the configured style."""
        if self.base_style == 'decimal':
            hundredths = random.randint(11, 999)
            return f"({dec(Fraction(hundredths, 100))})"
        if self.base_style == 'fraction':
            from math import gcd
            while True:
                den = random.randint(2, 50)
                num = random.randint(1, 3 * den)
                if num != den and gcd(num, den) == 1:
                    return f"({num}/{den})"
        variables = ['a', 'b', 'c', 'm', 'n', 'p', 'q', 'r',
                     's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        shape = random.choice(['variable', 'multiple', 'product',
                               'sum', 'difference'])
        first = random.choice(variables)
        if shape == 'variable':
            return first
        if shape == 'multiple':
            return f"({random.randint(2, 20)}{first})"
        if shape == 'product':
            second = random.choice([v for v in variables if v != first])
            return f"({first}{second})"
        constant = random.randint(1, 30)
        sign = '+' if shape == 'sum' else '-'
        return f"({first} {sign} {constant})"

    def _phrase(self, expression):
        return _context_phrase(_RULE_TEMPLATES, expression)

    @staticmethod
    def _positive_power(base, exponent):
        return base if exponent == 1 else f"{base}^{exponent}"

    def generate(self) -> dict:
        """Generate an exponent rule problem."""
        rule = self.rule or random.choice(self.RULES)

        if rule == 'product':
            return self._generate_product_rule()
        elif rule == 'quotient':
            return self._generate_quotient_rule()
        elif rule == 'power':
            return self._generate_power_rule()
        elif rule == 'negative':
            return self._generate_negative_exponent()
        else:
            return self._generate_zero_exponent()

    def _generate_product_rule(self) -> dict:
        """Generate x^a · x^b = x^(a+b) problem."""
        base = self._pick_base()
        exp1 = random.randint(1, 30)
        exp2 = random.randint(1, 30)
        result_exp = exp1 + exp2

        expression = f"{base}^{exp1} · {base}^{exp2}"
        problem = self._phrase(expression)
        answer = self._positive_power(base, result_exp)

        steps = []
        steps.append(step("EXP_RULE_SETUP", f"{base}^{exp1} · {base}^{exp2}"))
        steps.append(step("EXP_RULE_IDENTIFY", "product_rule", "x^a · x^b = x^(a+b)"))
        steps.append(step("EXP_RULE_APPLY", "add", exp1, exp2, result_exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_product_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_quotient_rule(self) -> dict:
        """Generate x^a / x^b = x^(a-b) problem."""
        base = self._pick_base()
        # Ensure exp1 > exp2 for positive result
        exp1 = random.randint(2, 40)
        exp2 = random.randint(1, exp1 - 1)
        result_exp = exp1 - exp2

        expression = f"{base}^{exp1} / {base}^{exp2}"
        problem = self._phrase(expression)
        answer = self._positive_power(base, result_exp)

        steps = []
        steps.append(step("EXP_RULE_SETUP", f"{base}^{exp1} / {base}^{exp2}"))
        steps.append(step("EXP_RULE_IDENTIFY", "quotient_rule", "x^a / x^b = x^(a-b)"))
        steps.append(step("EXP_RULE_APPLY", "subtract", exp1, exp2, result_exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_quotient_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_power_rule(self) -> dict:
        """Generate (x^a)^b = x^(ab) problem."""
        base = self._pick_base()
        exp1 = random.randint(2, 12)
        exp2 = random.randint(2, 12)
        result_exp = exp1 * exp2

        expression = f"({base}^{exp1})^{exp2}"
        problem = self._phrase(expression)
        answer = self._positive_power(base, result_exp)

        steps = []
        steps.append(step("EXP_RULE_SETUP", f"({base}^{exp1})^{exp2}"))
        steps.append(step("EXP_RULE_IDENTIFY", "power_rule", "(x^a)^b = x^(ab)"))
        steps.append(step("EXP_RULE_APPLY", "multiply", exp1, exp2, result_exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_power_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_negative_exponent(self) -> dict:
        """Generate x^(-n) = 1/x^n (or reciprocal flip for fraction bases)."""
        base = self._pick_base()
        exp = random.randint(1, 30)

        expression = f"{base}^(-{exp})"
        problem = self._phrase(expression)
        steps = []
        steps.append(step("EXP_RULE_SETUP", f"{base}^(-{exp})"))
        if self.base_style == 'fraction':
            # (a/b)^(-n) = (b/a)^n — the reciprocal flip.
            num, den = base.strip("()").split("/")
            reciprocal = den if num == "1" else f"({den}/{num})"
            answer = self._positive_power(reciprocal, exp)
            steps.append(step("EXP_RULE_IDENTIFY", "negative_exponent_reciprocal",
                              "(a/b)^(-n) = (b/a)^n"))
        else:
            answer = f"1/{self._positive_power(base, exp)}"
            steps.append(step("EXP_RULE_IDENTIFY", "negative_exponent", "x^(-n) = 1/x^n"))
        steps.append(step("EXP_RULE_APPLY", "negate", exp, exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_negative_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_zero_exponent(self) -> dict:
        """Generate x^0 = 1 problem."""
        # Use various bases to make it interesting
        base_type = ('styled' if self.base_style != 'variable'
                     else random.choice(['variable', 'number', 'expression']))
        if base_type == 'styled':
            base = self._pick_base()
            expression = f"{base}^0"

        elif base_type == 'variable':
            base = self._pick_base()
            expression = f"{base}^0"
        elif base_type == 'number':
            base = random.randint(2, 10000)
            expression = f"{base}^0"
        else:
            base = self._pick_base()
            expression = f"{base}^0"

        problem = self._phrase(expression)

        answer = "1"

        steps = []
        if base_type == 'expression':
            steps.append(step("EXP_RULE_SETUP", f"{base}^0"))
        else:
            steps.append(step("EXP_RULE_SETUP", f"{base}^0"))
        steps.append(step("EXP_RULE_IDENTIFY", "zero_exponent", "x^0 = 1 (for x ≠ 0)"))
        steps.append(step("EXP_RULE_SIMPLIFY", "1"))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_zero_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )


class ScientificNotationGenerator(ProblemGenerator):
    """
    Generates scientific notation problems.

    Problem types:
    - Convert standard form to scientific notation
    - Convert scientific notation to standard form
    - Operations with scientific notation (multiply/divide)

    Op-codes used:
    - SCI_SETUP: Set up the problem (number_or_expression)
    - SCI_IDENTIFY: Identify the coefficient and power (coefficient, power)
    - SCI_MOVE_DECIMAL: Show decimal movement (direction, places)
    - SCI_OPERATION: Perform operation (operation, values, result)
    - Z: Final answer
    """

    def __init__(self, problem_type: str = None):
        """
        Initialize generator.

        Args:
            problem_type: One of 'to_scientific', 'from_scientific', 'multiply', 'divide' or None for random
        """
        valid_types = ['to_scientific', 'from_scientific', 'multiply', 'divide']
        if problem_type is not None and problem_type not in valid_types:
            raise ValueError(f"Invalid problem_type: {problem_type}. Must be one of {valid_types} or None.")
        self.problem_type = problem_type

    def generate(self) -> dict:
        """Generate a scientific notation problem."""
        ptype = self.problem_type or random.choice(['to_scientific', 'from_scientific', 'multiply', 'divide'])

        if ptype == 'to_scientific':
            return self._generate_to_scientific()
        elif ptype == 'from_scientific':
            return self._generate_from_scientific()
        elif ptype == 'multiply':
            return self._generate_multiply()
        else:
            return self._generate_divide()

    @staticmethod
    def _coefficient(hundredths=True):
        denominator = 100 if hundredths else 10
        low = denominator
        return Fraction(random.randint(low, 10 * denominator - 1),
                        denominator)

    @staticmethod
    def _power():
        return random.choice([p for p in range(-12, 13) if p != 0])

    @staticmethod
    def _normalize(coefficient, power):
        coefficient = Fraction(coefficient)
        while coefficient >= 10:
            coefficient /= 10
            power += 1
        while coefficient < 1:
            coefficient *= 10
            power -= 1
        return coefficient, power

    @staticmethod
    def _phrase(kind, expression):
        return _context_phrase(_SCI_TEMPLATES[kind], expression)

    def _generate_to_scientific(self) -> dict:
        """Convert standard form to scientific notation."""
        # Generate a coefficient (1 <= c < 10), in exact tenths
        coefficient = self._coefficient()

        # Generate power
        power = self._power()

        # Calculate standard form number exactly
        number = coefficient * Fraction(10) ** power
        number_str = dec(number)

        problem = self._phrase("to_scientific", number_str)

        answer = f"{dec(coefficient)} × 10^{power}"

        steps = []
        steps.append(step("SCI_SETUP", number_str))

        if power > 0:
            steps.append(step("SCI_MOVE_DECIMAL", "left", power))
        else:
            steps.append(step("SCI_MOVE_DECIMAL", "right", -power))

        steps.append(step("SCI_IDENTIFY", dec(coefficient), power))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_convert_to",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_from_scientific(self) -> dict:
        """Convert scientific notation to standard form."""
        coefficient = self._coefficient()
        power = self._power()

        sci_notation = f"{dec(coefficient)} × 10^{power}"

        problem = self._phrase("from_scientific", sci_notation)

        # Calculate standard form exactly
        number = coefficient * Fraction(10) ** power
        answer = dec(number)

        steps = []
        steps.append(step("SCI_SETUP", sci_notation))
        steps.append(step("SCI_IDENTIFY", dec(coefficient), power))

        if power > 0:
            steps.append(step("SCI_MOVE_DECIMAL", "right", power))
        else:
            steps.append(step("SCI_MOVE_DECIMAL", "left", -power))

        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_convert_from",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_multiply(self) -> dict:
        """Multiply two numbers in scientific notation."""
        # Generate two scientific notation numbers, in exact tenths
        c1 = self._coefficient(hundredths=False)
        c2 = self._coefficient(hundredths=False)
        p1 = self._power()
        p2 = self._power()

        # Calculate result exactly (raw product has at most 2 decimals)
        raw = c1 * c2
        c_result, p_result = self._normalize(raw, p1 + p2)

        # Format inputs
        n1 = f"({dec(c1)} × 10^{p1})"
        n2 = f"({dec(c2)} × 10^{p2})"

        expression = f"{n1} × {n2}"
        problem = self._phrase("multiply", expression)

        answer = f"{dec(c_result)} × 10^{p_result}"

        steps = []
        steps.append(step("SCI_SETUP", f"{n1} × {n2}"))
        steps.append(step("SCI_OPERATION", "multiply_coefficients", dec(c1), dec(c2), dec(raw)))
        steps.append(step("SCI_OPERATION", "add_exponents", p1, p2, p1 + p2))

        if (c_result, p_result) != (raw, p1 + p2):
            steps.append(step("SCI_OPERATION", "adjust_coefficient", dec(raw), dec(c_result), p_result))

        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_multiply",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_divide(self) -> dict:
        """Divide two numbers in scientific notation."""
        # Generate two scientific notation numbers, constructed so the
        # coefficient quotient is exact
        while True:
            c2 = self._coefficient(hundredths=False)
            raw = self._coefficient(hundredths=False)
            c1 = c2 * raw
            if 1 <= c1 < 10:
                break

        p1 = self._power()
        p2 = self._power()

        # Calculate result exactly (c1/c2 is the integer multiplier)
        raw = c1 / c2
        c_result, p_result = self._normalize(raw, p1 - p2)

        # Format inputs
        n1 = f"({dec(c1)} × 10^{p1})"
        n2 = f"({dec(c2)} × 10^{p2})"

        expression = f"{n1} ÷ {n2}"
        problem = self._phrase("divide", expression)

        answer = f"{dec(c_result)} × 10^{p_result}"

        steps = []
        steps.append(step("SCI_SETUP", f"{n1} ÷ {n2}"))
        steps.append(step("SCI_OPERATION", "divide_coefficients", dec(c1), dec(c2), dec(raw)))
        steps.append(step("SCI_OPERATION", "subtract_exponents", p1, p2, p1 - p2))

        if (c_result, p_result) != (raw, p1 - p2):
            steps.append(step("SCI_OPERATION", "adjust_coefficient", dec(raw), dec(c_result), p_result))

        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_divide",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )


class RootsAndRadicalsGenerator(ProblemGenerator):
    """
    Generates square root, cube root, and radical simplification problems.

    Op-codes used:
    - ROOT_SETUP: Set up the radical expression (expression)
    - ROOT_IDENTIFY: Identify perfect square/cube factor (number, factor, quotient)
    - ROOT_EXTRACT: Extract the root (root_value, remaining)
    - ROOT_SIMPLIFY: Show simplified form (simplified_expression)
    - Z: Final answer
    """

    def __init__(self, problem_type: str = None):
        """
        Initialize generator.

        Args:
            problem_type: One of 'square_perfect', 'cube_perfect', 'simplify_square' or None for random
        """
        valid_types = ['square_perfect', 'cube_perfect', 'simplify_square']
        if problem_type is not None and problem_type not in valid_types:
            raise ValueError(f"Invalid problem_type: {problem_type}. Must be one of {valid_types} or None.")
        self.problem_type = problem_type

    # The radicands stay recognizable by hand; context and phrasing provide
    # additional capacity without forcing large arithmetic.
    PERFECT_SQUARES = [k * k for k in range(1, 51)]
    SQUARE_ROOTS = {k * k: k for k in range(1, 51)}

    PERFECT_CUBES = [k ** 3 for k in range(1, 21)]
    CUBE_ROOTS = {k ** 3: k for k in range(1, 21)}

    SQUARE_FREE = [n for n in range(2, 31)
                   if all(n % (k * k) for k in range(2, int(n ** 0.5) + 1))]

    @staticmethod
    def _phrase(kind, expression):
        return _context_phrase(_ROOT_TEMPLATES[kind], expression)

    def generate(self) -> dict:
        """Generate a roots/radicals problem."""
        ptype = self.problem_type or random.choice(['square_perfect', 'cube_perfect', 'simplify_square'])

        if ptype == 'square_perfect':
            return self._generate_square_perfect()
        elif ptype == 'cube_perfect':
            return self._generate_cube_perfect()
        else:
            return self._generate_simplify_square()

    def _generate_square_perfect(self) -> dict:
        """Generate √n where n is a perfect square."""
        n = random.choice(self.PERFECT_SQUARES[1:])  # Skip 1
        answer = self.SQUARE_ROOTS[n]

        problem = self._phrase("evaluate", f"√{n}")

        steps = []
        steps.append(step("ROOT_SETUP", f"√{n}"))
        steps.append(step("ROOT_IDENTIFY", n, "perfect_square", answer))
        steps.append(step("ROOT_EXTRACT", answer, ""))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="square_root_perfect",
            problem=problem,
            steps=steps,
            final_answer=str(answer),
        )

    def _generate_cube_perfect(self) -> dict:
        """Generate ∛n where n is a perfect cube."""
        n = random.choice(self.PERFECT_CUBES[1:])  # Skip 1
        answer = self.CUBE_ROOTS[n]

        problem = self._phrase("evaluate", f"∛{n}")

        steps = []
        steps.append(step("ROOT_SETUP", f"∛{n}"))
        steps.append(step("ROOT_IDENTIFY", n, "perfect_cube", answer))
        steps.append(step("ROOT_EXTRACT", answer, ""))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="cube_root_perfect",
            problem=problem,
            steps=steps,
            final_answer=str(answer),
        )

    def _generate_simplify_square(self) -> dict:
        """Generate √n where n = a²·b (simplifies to a√b)."""
        # Pick a perfect square factor (not 1)
        root_of_factor = random.randint(2, 12)
        perfect_factor = root_of_factor ** 2
        root_of_factor = self.SQUARE_ROOTS[perfect_factor]

        # Pick a small square-free remaining factor.
        remaining = random.choice(self.SQUARE_FREE)

        n = perfect_factor * remaining
        answer = f"{root_of_factor}√{remaining}"

        problem = self._phrase("simplify", f"√{n}")

        steps = []
        steps.append(step("ROOT_SETUP", f"√{n}"))
        steps.append(step("ROOT_IDENTIFY", n, perfect_factor, remaining))
        steps.append(step("ROOT_EXTRACT", root_of_factor, f"√{remaining}"))
        steps.append(step("ROOT_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="simplify_radical",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

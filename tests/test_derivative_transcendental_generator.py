import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.derivative_transcendental_generator import (
    DerivativeTranscendentalGenerator,
)
from helpers import DELIM


# ------------------------------------------------------------------ parsing

PHRASINGS = [
    re.compile(r"Differentiate y = (?P<body>.+)\."),
    re.compile(r"Find dy/d(?P<var>[a-z]) for y = (?P<body>.+)\."),
    re.compile(r"Compute y' for the function y = (?P<body>.+)\."),
    re.compile(r"Let y = (?P<body>.+)\. Find y'\."),
    re.compile(r"What is the derivative of y = (?P<body>.+) with respect to "
               r"(?P<var>[a-z])\?"),
]

_TOKENS = re.compile(r"log_\d+|sin|cos|tan|sec|csc|cot|ln|e\^")


def parse_problem(problem):
    """Returns (body, var, phrasing_index) for any phrasing."""
    for index, pattern in enumerate(PHRASINGS):
        match = pattern.fullmatch(problem)
        if match is not None:
            body = match.group("body")
            var = match.groupdict().get("var") or detect_var(body)
            return body, var, index
    raise AssertionError(f"unparsed problem: {problem}")


def detect_var(text):
    stripped = _TOKENS.sub(" ", text)
    letters = sorted(set(re.findall(r"[a-z]", stripped)))
    assert len(letters) == 1, (text, letters)
    return letters[0]


# ------------------------------------------------------- expression -> python

def to_py(expr):
    s = expr
    s = s.replace("·", "*")
    s = re.sub(r"log_(\d+)\(", r"logb(\1,", s)
    s = re.sub(r"(sin|cos|tan|sec|csc|cot)\^2\(", r"sq_\1(", s)
    s = s.replace("ln(", "log(")
    s = s.replace("e^(", "exp(")
    s = re.sub(r"\s*\bln (\d+)", r"*log(\1)", s)
    s = s.replace("^", "**")
    s = re.sub(r"\)\s*([A-Za-z_])", r")*\1", s)
    s = re.sub(r"(\d)\s*([A-Za-z_])", r"\1*\2", s)
    return s


def _sec(u):
    return 1.0 / math.cos(u)


def _csc(u):
    return 1.0 / math.sin(u)


def _cot(u):
    return math.cos(u) / math.sin(u)


NAMESPACE = {
    "math": math,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sec": _sec, "csc": _csc, "cot": _cot,
    "log": math.log, "exp": math.exp,
    "logb": lambda b, x: math.log(x) / math.log(b),
    "sq_sin": lambda u: math.sin(u) ** 2,
    "sq_cos": lambda u: math.cos(u) ** 2,
    "sq_tan": lambda u: math.tan(u) ** 2,
    "sq_sec": lambda u: _sec(u) ** 2,
    "sq_csc": lambda u: _csc(u) ** 2,
    "sq_cot": lambda u: _cot(u) ** 2,
}

GRID = [0.011, 0.037, 0.091, 0.137, 0.211, 0.313, 0.437, 0.611, 0.827,
        1.013, 1.237, 1.553, 1.907, 2.311, 2.803, 3.407, 4.111, 5.029,
        6.211, 7.403, 8.617, 9.733]


def _safe_eval(code, var, value):
    env = dict(NAMESPACE)
    env[var] = value
    try:
        out = eval(code, {"__builtins__": {}}, env)
    except (ValueError, ZeroDivisionError, OverflowError):
        return None
    if not isinstance(out, (int, float)):
        return None
    if not math.isfinite(out):
        return None
    return float(out)


def numeric_check(example, min_points=2):
    """A9 oracle: central-difference agreement, computed from problem text."""
    body, var, _ = parse_problem(example["problem"])
    rhs = example["final_answer"]
    assert rhs.startswith("y' = "), rhs
    fcode = to_py(body)
    dcode = to_py(rhs[len("y' = "):])
    # Trig functions have poles; the central-difference truncation error grows
    # like (c·f·k·h)^2, so stay well away from them.  Exponentials are
    # huge but perfectly conditioned, so no magnitude cap applies there.
    is_exp = ("e^(" in body) or re.search(r"\d\^", body) is not None
    ok_points = 0
    h = 1e-6
    for x in GRID:
        f_hi = _safe_eval(fcode, var, x + h)
        f_lo = _safe_eval(fcode, var, x - h)
        f_mid = _safe_eval(fcode, var, x)
        claimed = _safe_eval(dcode, var, x)
        if None in (f_hi, f_lo, f_mid, claimed):
            continue
        if not is_exp and abs(f_mid) > 200:
            continue
        secant = (f_hi - f_lo) / (2 * h)
        denom = max(abs(claimed), abs(secant), abs(f_mid), 1.0)
        if abs(secant - claimed) > 1e-4 * denom:
            return False
        ok_points += 1
    return ok_points >= min_points


# ------------------------------------------------------------ step checking

def slope_of(inner, var):
    """Slope of a rendered linear inner function such as '3x + 4' or '5t'."""
    match = re.fullmatch(rf"(-?\d*){var}(?: [+-] \d+)?", inner)
    assert match is not None, inner
    head = match.group(1)
    if head in ("", "+"):
        return 1
    if head == "-":
        return -1
    return int(head)


def check_steps(example):
    body, var, _ = parse_problem(example["problem"])
    saw_rule = False
    for raw in example["steps"]:
        fields = raw.split(DELIM)
        op = fields[0]
        if op == "DERIV_SETUP":
            if fields[1] != f"y = {body}":
                return False
        elif op == "DERIV_RULE":
            saw_rule = True
        elif op == "POWER_RULE":
            if slope_of(fields[1], var) != int(fields[2]):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "LOG_POWER":
            match = re.fullmatch(rf"ln\({var}\^(\d+)\)", fields[1])
            if match is None:
                return False
            if fields[2] != f"{match.group(1)} ln({var})":
                return False
        elif op == "Z":
            if fields[1:] != [example["final_answer"]]:
                return False
    rewrites = [s for s in example["steps"] if s.startswith(f"REWRITE{DELIM}")]
    if not rewrites:
        return False
    if rewrites[-1].split(DELIM, 1)[1] != example["final_answer"]:
        return False
    return saw_rule


class TestDerivativeTranscendentalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DerivativeTranscendentalGenerator()

    def test_output_contract(self):
        for _ in range(50):
            result = self.gen.generate()
            for key in ("problem_id", "operation", "problem", "steps",
                        "final_answer"):
                self.assertIn(key, result)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                             result["final_answer"])

    def test_oracle_numeric_secant(self):
        """A9 oracle: central-difference agreement, all phrasings."""
        for _ in range(1200):
            result = self.gen.generate()
            self.assertTrue(numeric_check(result),
                            (result["problem"], result["final_answer"]))

    def test_step_arithmetic(self):
        for _ in range(600):
            result = self.gen.generate()
            self.assertTrue(check_steps(result),
                            (result["problem"], result["steps"]))

    def test_ln_kx_collapses_to_c_over_x(self):
        gen = DerivativeTranscendentalGenerator("log")
        found = False
        for _ in range(400):
            result = gen.generate()
            body, var, _ = parse_problem(result["problem"])
            if re.search(rf"ln\(\d+{var}\)", body):
                found = True
                self.assertRegex(result["final_answer"],
                                 rf"^y' = -?\d+/{var}$")
                self.assertTrue(any(s.startswith(f"CANCEL{DELIM}")
                                    for s in result["steps"]))
        self.assertTrue(found)

    def test_rule_always_stated(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"DERIV_RULE{DELIM}")
                                for s in result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)
        self.assertEqual(ops, {
            "derivative_transcendental_trig",
            "derivative_transcendental_exp",
            "derivative_transcendental_log",
        })

    def test_all_sub_forms_reachable(self):
        """Every trig function and every log/exp sub-form must appear."""
        trig_seen = set()
        gen = DerivativeTranscendentalGenerator("trig")
        for _ in range(400):
            body, _, _ = parse_problem(gen.generate()["problem"])
            for fn in ("sin", "cos", "tan", "sec", "csc", "cot"):
                if re.search(rf"\b{fn}\(", body):
                    trig_seen.add(fn)
        self.assertEqual(trig_seen,
                         {"sin", "cos", "tan", "sec", "csc", "cot"})

        exp_seen = set()
        gen = DerivativeTranscendentalGenerator("exp")
        for _ in range(400):
            body, var, _ = parse_problem(gen.generate()["problem"])
            if "e^(" in body:
                exp_seen.add("e")
            elif re.search(rf"\d\^{var}$", body):
                exp_seen.add("a^x")
            else:
                exp_seen.add("a^u")
        self.assertEqual(exp_seen, {"e", "a^x", "a^u"})

        log_seen = set()
        gen = DerivativeTranscendentalGenerator("log")
        for _ in range(600):
            body, var, _ = parse_problem(gen.generate()["problem"])
            if re.search(rf"ln\(\d+{var}\)", body):
                log_seen.add("ln_kx")
            elif re.search(rf"ln\({var}\^", body):
                log_seen.add("ln_power")
            elif "ln(" in body:
                log_seen.add("ln_lin")
            elif re.search(rf"log_\d+\({var}\)", body):
                log_seen.add("log_b_x")
            else:
                log_seen.add("log_b_lin")
        self.assertEqual(log_seen, {"ln_kx", "ln_power", "ln_lin",
                                    "log_b_x", "log_b_lin"})

    def test_all_phrasings_used(self):
        seen = set()
        for _ in range(400):
            _, _, index = parse_problem(self.gen.generate()["problem"])
            seen.add(index)
        self.assertEqual(seen, set(range(len(PHRASINGS))))

    def test_render_sanity_and_pipe_safety(self):
        for _ in range(600):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)
                for field in raw.split(DELIM)[1:]:
                    self.assertNotIn(DELIM, field)
            body, var, _ = parse_problem(result["problem"])
            text = body + " " + result["final_answer"]
            self.assertIsNone(re.search(rf"(?<![0-9]) 1 ", text))
            self.assertIsNone(re.search(rf"(?<![0-9])1{var}", text), text)
            self.assertNotIn("--", text)
            self.assertNotIn("+ 0", text)
            self.assertNotIn("- 0", text)
            self.assertNotIn("^1)", text)
            self.assertNotIn("· 1", text)

    def test_capacity_is_wide(self):
        texts = {self.gen.generate()["problem"] for _ in range(800)}
        self.assertGreaterEqual(len(texts), 780)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DerivativeTranscendentalGenerator("bogus")


if __name__ == "__main__":
    unittest.main()

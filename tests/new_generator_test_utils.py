import ast
import math
import re
import unittest
from fractions import Fraction

from helpers import DELIM


def assert_contract(case, result):
    for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
        case.assertIn(key, result)
    case.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
    case.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                     result["final_answer"])


def assert_pipe_safe(case, result):
    for raw_step in result["steps"]:
        case.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)
        case.assertNotIn(f"{DELIM}{DELIM}", raw_step)


def parse_number(text):
    return Fraction(text.strip().rstrip("."))


def dec(fr):
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    s = str(float(fr)).rstrip("0").rstrip(".")
    return s


def ice_fmt(fr):
    fr = Fraction(fr)
    return dec(fr) if fr.denominator in (1, 2, 4, 5, 8, 10, 20, 25) else str(fr)


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_int_matrix(text):
    return ast.literal_eval(text)


def parse_frac_matrix(text):
    rows = re.findall(r"\[([^\[\]]+)\]", text)
    return [[Fraction(part.strip()) for part in row.split(",")]
            for row in rows]


def matmul(A, B):
    return [[sum(Fraction(A[i][k]) * Fraction(B[k][j])
                 for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def transpose(A):
    return [list(row) for row in zip(*A)]


def _fac_roots(expr):
    roots = []
    i = 0
    while i < len(expr):
        if expr[i] == "x":
            roots.append(0)
            i += 1
        elif expr[i] == "(":
            j = expr.index(")", i)
            body = expr[i + 1:j]
            if body == "x":
                roots.append(0)
            else:
                m = re.fullmatch(r"x ([+-]) (\d+)", body)
                sign, n = m.groups()
                roots.append(int(n) if sign == "-" else -int(n))
            i = j + 1
        else:
            i += 1
    return roots


def _quad_roots(expr):
    m = re.fullmatch(
        r"x\^2(?: ([+-]) (\d+)x)?(?: ([+-]) (\d+))?", expr
    )
    b = 0
    c = 0
    if m.group(1):
        b = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
    if m.group(3):
        c = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
    disc = b * b - 4 * c
    root_disc = math.isqrt(disc)
    return sorted([(-b - root_disc) // 2, (-b + root_disc) // 2])


def _relation_ok(value, rel):
    return {
        "<": value < 0,
        "≤": value <= 0,
        ">": value > 0,
        "≥": value >= 0,
    }[rel]


def _test_point(left, right):
    if left is None:
        return Fraction(right) - 1
    if right is None:
        return Fraction(left) + 1
    return (Fraction(left) + Fraction(right)) / 2


def _interval_piece(left, right, include_left=False, include_right=False):
    lbr = "[" if include_left else "("
    rbr = "]" if include_right else ")"
    if left is None:
        lbr, ltxt = "(", "-∞"
    else:
        ltxt = fmt_frac(left)
    if right is None:
        rbr, rtxt = ")", "∞"
    else:
        rtxt = fmt_frac(right)
    return f"{lbr}{ltxt}, {rtxt}{rbr}"


def _interval_answer(accepted, closed, open_points):
    pieces = []
    for left, right in accepted:
        pieces.append(_interval_piece(
            left, right,
            include_left=left in closed and left not in open_points,
            include_right=right in closed and right not in open_points,
        ))
    return " ∪ ".join(pieces) if pieces else "No solution"


def oracle_polynomial_inequality(example):
    expr, rel = re.fullmatch(
        r"Solve (.+) ([<≤>≥]) 0\. Give the answer in interval notation\.",
        example["problem"],
    ).groups()
    open_points = set()
    if "/" in expr:
        numer, denom = expr.split("/")
        zero = _fac_roots(numer)[0]
        pole = _fac_roots(denom)[0]
        points = sorted([zero, pole])
        roots = [zero]
        open_points.add(pole)

        def value(x):
            return (x - zero) / (x - pole)
    elif expr.startswith("x^2"):
        roots = _quad_roots(expr)
        points = roots

        def value(x):
            out = Fraction(1)
            for root in roots:
                out *= x - root
            return out
    else:
        roots = sorted(_fac_roots(expr))
        points = roots

        def value(x):
            out = Fraction(1)
            for root in roots:
                out *= x - root
            return out

    bounds = [None] + points + [None]
    intervals = list(zip(bounds[:-1], bounds[1:]))
    accepted = [iv for iv in intervals if _relation_ok(value(_test_point(*iv)), rel)]
    closed = set(roots) if rel in ("≤", "≥") else set()
    return _interval_answer(accepted, closed, open_points)


def _pow_txt(power):
    return "n" if power == 1 else f"n^{power}"


def oracle_master(example):
    p = example["problem"]
    if "T(n-1)" in p:
        term = re.search(r"\+ (\d*)n(?:\^(\d+))?", p)
        exp = 1 if term.group(2) is None else int(term.group(2))
        return f"subtract; Θ({_pow_txt(exp + 1)})"
    a, b, _, exp_text = re.fullmatch(
        r"Use the Master Theorem to solve T\(n\) = (\d+)T\(n/(\d+)\) \+ (\d*)n(?:\^(\d+))? in Θ notation\.",
        p,
    ).groups()
    a, b = int(a), int(b)
    k = 1 if exp_text is None else int(exp_text)
    log = 0
    cur = 1
    while cur < a:
        cur *= b
        log += 1
    if log < k:
        return f"case 1; Θ({_pow_txt(k)})"
    if log == k:
        return f"case 2; Θ({_pow_txt(k)} log n)"
    return f"case 3; Θ({_pow_txt(log)})"


def oracle_telescoping(example):
    p = example["problem"]
    m = re.fullmatch(r"Evaluate Σ_\{k=(\d+)\}\^\{(\d+)\} 1/\(k\(k\+(\d+)\)\)\.", p)
    if m:
        start, end, gap = map(int, m.groups())
        left = sum(Fraction(1, k) for k in range(start, start + gap))
        right = sum(Fraction(1, k) for k in range(end + 1, end + gap + 1))
        return fmt_frac((left - right) / gap)
    m = re.fullmatch(r"Evaluate Σ_\{k=(\d+)\}\^\{(\d+)\} \(√\(k\+1\) - √k\)\.", p)
    if m:
        start, end = map(int, m.groups())
        return f"√{end + 1} - √{start}"
    m = re.fullmatch(r"Evaluate Π_\{k=(\d+)\}\^\{(\d+)\} k/\(k\+1\)\.", p)
    if m:
        start, end = map(int, m.groups())
        return fmt_frac(Fraction(start, end + 1))
    start, end = map(int, re.fullmatch(
        r"Evaluate Σ_\{k=(\d+)\}\^\{(\d+)\} \(1/k - 1/\(k\+1\)\)\.",
        p,
    ).groups())
    return fmt_frac(Fraction(1, start) - Fraction(1, end + 1))


def oracle_two_sample(example):
    p = example["problem"]
    crit = Fraction(re.search(r"critical value of ([\d.]+)", p).group(1))
    if "two-sample t-test" in p:
        n1, x1, s1, n2, x2, s2 = map(Fraction, re.search(
            r"n1=(\d+), x̄1=(\d+), s1=(\d+); sample 2 has n2=(\d+), x̄2=(\d+), s2=(\d+)",
            p,
        ).groups())
        se = (s1 * s1 / n1 + s2 * s2 / n2)
        assert se == 4
        stat = (x1 - x2) / 2
    else:
        n1, x1, n2, x2 = map(Fraction, re.search(
            r"n1=(\d+), x1=(\d+); sample 2 has n2=(\d+), x2=(\d+)",
            p,
        ).groups())
        pooled = (x1 + x2) / (n1 + n2)
        se = Fraction(1, 10)
        stat = (x1 / n1 - x2 / n2) / se
    if "test statistic" in p:
        return dec(stat)
    head = "reject H0" if abs(stat) > crit else "fail to reject H0"
    rel = ">" if abs(stat) > crit else "≤"
    return f"{head} ({dec(abs(stat))} {rel} {dec(crit)})"


def oracle_ice(example):
    p = example["problem"]
    m = re.fullmatch(r"For A ⇌ B, the equilibrium concentrations are \[A\]=(.+) and \[B\]=(.+)\. Compute K=\[B\]/\[A\]\.", p)
    if m:
        a, b = map(parse_number, m.groups())
        return f"K={ice_fmt(b / a)}"
    m = re.fullmatch(
        r"For A ⇌ 2B, initially \[A\]=(\d+) and \[B\]=0\. At equilibrium \[A\]=\d+-x and \[B\]=2x\. Given K=(.+) for K=\[B\]\^2/\[A\], find x\.",
        p,
    )
    if m:
        a0 = int(m.group(1))
        K = parse_number(m.group(2))
        for x in range(1, a0):
            if Fraction(4 * x * x, a0 - x) == K:
                return f"x={x}; [A]={a0 - x}, [B]={2 * x}"
    K, a, b = re.fullmatch(
        r"For A ⇌ B with K=(.+), the current concentrations are \[A\]=(.+) and \[B\]=(.+)\. Compute Q=\[B\]/\[A\] and predict the reaction direction\.",
        p,
    ).groups()
    K, a, b = map(parse_number, (K, a, b))
    Q = b / a
    rel = "<" if Q < K else (">" if Q > K else "=")
    direction = {"<": "forward", ">": "reverse", "=": "at equilibrium"}[rel]
    return f"{direction} (Q={ice_fmt(Q)} {rel} K={ice_fmt(K)})"


def oracle_pde(example):
    p = example["problem"]
    m = re.fullmatch(
        r"Solve u_t = (\d+)u_xx on 0≤x≤(\d+) with zero endpoint conditions and u\(x,0\)=(\d+)sin\((\d+)πx/(\d+)\)\.",
        p,
    )
    if m:
        alpha, L, amp, n, _ = map(int, m.groups())
        return f"u(x,t)={amp}e^(-{alpha}({n}π/{L})^2t)sin({n}πx/{L})"
    c2, x0, t0 = map(int, re.fullmatch(
        r"For u_tt = (\d+)u_xx with u\(x,0\)=x\^2 and u_t\(x,0\)=0, use d'Alembert's formula to find u\((\d+),(\d+)\)\.",
        p,
    ).groups())
    c = math.isqrt(c2)
    value = ((x0 - c * t0) ** 2 + (x0 + c * t0) ** 2) // 2
    return f"u({x0},{t0})={value}"


def oracle_induction(example):
    p = example["problem"]
    check_n = int(re.search(r"check at n=(\d+)", p).group(1))
    if "n≥0" in p:
        r = int(re.search(r"1\+(\d+)\+\.\.\.", p).group(1))
        value = (r ** (check_n + 1) - 1) // (r - 1)
        return f"check n={check_n} value={value}; inductive step confirmed"
    if "6 divides" in p:
        value = check_n ** 3 - check_n
        return f"check n={check_n} value={value}; inductive divisibility confirmed"
    if "1^2+2^2" in p:
        value = check_n * (check_n + 1) * (2 * check_n + 1) // 6
    elif "2n-1" in p:
        value = check_n * check_n
    else:
        value = check_n * (check_n + 1) // 2
    return f"check n={check_n} value={value}; inductive step confirmed"


def verify_qr(example):
    A = parse_frac_matrix(re.search(r"A = (\[\[.*\]\])\.", example["problem"]).group(1))
    qtxt, rtxt = re.fullmatch(r"Q=(\[\[.*\]\]); R=(\[\[.*\]\])",
                              example["final_answer"]).groups()
    Q, R = parse_frac_matrix(qtxt), parse_frac_matrix(rtxt)
    return matmul(Q, R) == A and matmul(transpose(Q), Q) == [
        [Fraction(int(i == j)) for j in range(len(Q))] for i in range(len(Q))
    ]


def oracle_cholesky(example):
    A = parse_int_matrix(re.search(r"A = (\[\[.*\]\])\.", example["problem"]).group(1))
    L = parse_int_matrix(example["final_answer"].removeprefix("L="))
    return matmul(L, transpose(L)) == A


def oracle_counting(example):
    p = example["problem"]
    m = re.fullmatch(
        r"What is the minimum number of objects needed to guarantee at least (\d+) objects in one of (\d+) boxes\?",
        p,
    )
    if m:
        k, boxes = map(int, m.groups())
        return f"minimum = {boxes * (k - 1) + 1}"
    m = re.fullmatch(r"How many balanced parenthesis strings are there with (\d+) pairs\?", p)
    if m:
        n = int(m.group(1))
        return f"Catalan C_{n} = {math.comb(2*n, n) // (n + 1)}"
    m = re.fullmatch(
        r"Use Vandermonde's identity to evaluate Σ_\{i\} C\((\d+),i\)C\((\d+),(\d+)-i\)\.",
        p,
    )
    if m:
        r, s, n = map(int, m.groups())
        value = math.comb(r + s, n)
        return f"sum = {value}; C({r+s},{n}) = {value}"
    r, n = map(int, re.fullmatch(
        r"Use the hockey-stick identity to evaluate Σ_\{i=(\d+)\}\^\{(\d+)\} C\(i,\d+\)\.",
        p,
    ).groups())
    value = math.comb(n + 1, r + 1)
    return f"sum = {value}; C({n+1},{r+1}) = {value}"


class GeneratorTestMixin:
    GEN = None
    ORACLE = None
    VARIANTS = ()
    CHECK_BOOLEAN = False

    def setUp(self):
        self.gen = self.GEN()

    def test_output_contract(self):
        assert_contract(self, self.gen.generate())

    def test_oracle_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            if self.CHECK_BOOLEAN:
                self.assertTrue(self.ORACLE(result),
                                (result["problem"], result["final_answer"]))
            else:
                self.assertEqual(result["final_answer"], self.ORACLE(result),
                                 result["problem"])

    def test_pipe_safe(self):
        for _ in range(200):
            assert_pipe_safe(self, self.gen.generate())

    def test_all_variants_reachable(self):
        if not self.VARIANTS:
            return
        ops = {self.gen.generate()["operation"] for _ in range(200)}
        expected = {f"{self.OP_PREFIX}_{v}" for v in self.VARIANTS}
        self.assertEqual(ops, expected)

    def test_fixed_variant_constructor(self):
        if not self.VARIANTS:
            return
        for variant in self.VARIANTS:
            result = self.GEN(variant).generate()
            self.assertIn(variant, result["operation"])
        with self.assertRaises(ValueError):
            self.GEN("bogus")

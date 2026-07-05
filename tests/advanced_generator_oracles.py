import ast
import math
import re
from fractions import Fraction
from math import comb

from helpers import DELIM


def frac_text(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def dec(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.6f}".rstrip("0").rstrip(".")


def turing_machine_oracle(problem):
    patterns = [
        (r"TM ([a-z_]+) on input ([01]+) for at most (\d+) steps\. "
         r"Rules: (.+)\. Blank"),
        (r"Turing machine ([a-z_]+): input ([01]+), step bound (\d+), "
         r"blank _\. Rules: (.+)\. Give"),
    ]
    match = None
    for pattern in patterns:
        match = re.search(pattern, problem)
        if match:
            name, input_text, limit_text, rules_text = match.groups()
            break
    if not match:
        input_text, name, limit_text, rules_text = re.search(
            r"input ([01]+), execute TM ([a-z_]+) for no more than "
            r"(\d+) steps using rules (.+)\. Return",
            problem,
        ).groups()
    rules = {}
    for raw in rules_text.split("; "):
        left, right = raw.split("->")
        state, read = left.split(",")
        new_state, write, move = right.split(",")
        rules[(state, read)] = (new_state, write, move)
    limit = int(limit_text)
    tape = list(input_text) + ["_"] * (limit + 2)
    head = 0
    state = "q0"
    for count in range(limit + 1):
        if state == "qH" or count == limit:
            break
        read = tape[head] if 0 <= head < len(tape) else "_"
        state, write, move = rules[(state, read)]
        tape[head] = write
        if move == "R":
            head += 1
        elif move == "L":
            head -= 1
    status = "halted" if state == "qH" else "bounded"
    last = -1
    for idx, symbol in enumerate(tape):
        if symbol != "_":
            last = idx
    trimmed = "_" if last < 0 else "".join(tape[:last + 1])
    return f"{status}; state={state}; tape={trimmed}; head={head}"


def regex_to_automaton_oracle(problem):
    specs = {
        "a*b": (
            "q0", ["q1"], ["q0", "q1", "qd"],
            {
                ("q0", "a"): "q0", ("q0", "b"): "q1",
                ("q1", "a"): "qd", ("q1", "b"): "qd",
                ("qd", "a"): "qd", ("qd", "b"): "qd",
            },
        ),
        "(a|b)*ab(a|b)*": (
            "q0", ["q2"], ["q0", "q1", "q2"],
            {
                ("q0", "a"): "q1", ("q0", "b"): "q0",
                ("q1", "a"): "q1", ("q1", "b"): "q2",
                ("q2", "a"): "q2", ("q2", "b"): "q2",
            },
        ),
        "(a|b)*(ab|ba)": (
            "q0", ["q3", "q4"], ["q0", "q1", "q2", "q3", "q4"],
            {
                ("q0", "a"): "q1", ("q0", "b"): "q2",
                ("q1", "a"): "q1", ("q1", "b"): "q3",
                ("q2", "a"): "q4", ("q2", "b"): "q2",
                ("q3", "a"): "q4", ("q3", "b"): "q2",
                ("q4", "a"): "q1", ("q4", "b"): "q3",
            },
        ),
    }
    regex = next(item for item in specs if item in problem)
    start, accept, states, transitions = specs[regex]
    rows = [
        f"{state}:a->{transitions[(state, 'a')]},b->{transitions[(state, 'b')]}"
        for state in states
    ]
    return (
        f"start={start}; accept={', '.join(accept)}; "
        f"transitions={'; '.join(rows)}"
    )


def pda_simulation_oracle(problem):
    patterns = [
        r"PDA ([a-z_^]+) on input ([()ab]+)",
        r"automaton ([a-z_^]+) for input ([()ab]+)",
        r"PDA ([a-z_^]+) with input ([()ab]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, problem)
        if match:
            name, text = match.groups()
            break
    else:
        raise AssertionError(problem)
    stack = ["$"]
    if name == "balanced_parentheses":
        for ch in text:
            if ch == "(":
                stack.append("(")
            elif len(stack) > 1:
                stack.pop()
            else:
                return "rejected; stack=$"
        status = "accepted" if stack == ["$"] else "rejected"
        return f"{status}; stack={''.join(stack)}"
    state = "push"
    for ch in text:
        if state == "push" and ch == "a":
            stack.append("A")
        elif ch == "b":
            state = "pop"
            if len(stack) > 1:
                stack.pop()
            else:
                return f"rejected; stack={''.join(stack)}"
        else:
            return f"rejected; stack={''.join(stack)}"
    status = "accepted" if state == "pop" and stack == ["$"] else "rejected"
    return f"{status}; stack={''.join(stack)}"


def _literal_key(literal):
    return literal.replace("not ", "")


def _complement(literal):
    return literal[4:] if literal.startswith("not ") else f"not {literal}"


def _resolve(c1, c2, literal):
    comp = _complement(literal)
    out = [x for x in c1 if x != literal] + [x for x in c2 if x != comp]
    seen = []
    for item in out:
        if item not in seen:
            seen.append(item)
    return tuple(sorted(seen, key=_literal_key))


def resolution_proof_oracle(problem):
    formula = re.search(r"C1=.*?(?:\.| Resolve|, using|$)", problem).group(0)
    clauses = []
    for raw in re.findall(r"C\d+=\(([^)]*)\)", formula):
        clauses.append(tuple(raw.split(" OR ")))
    while clauses[-1]:
        seen = set(clauses)
        found = None
        for i, c1 in enumerate(clauses):
            for j, c2 in enumerate(clauses):
                if i >= j:
                    continue
                for literal in sorted(c1, key=_literal_key):
                    if _complement(literal) in c2:
                        resolvent = _resolve(c1, c2, literal)
                        if resolvent not in seen:
                            found = resolvent
                            break
                        break
                if found is not None:
                    break
            if found is not None:
                break
        if found is None:
            raise AssertionError(problem)
        clauses.append(found)
    return f"unsatisfiable; empty clause = C{len(clauses)}"


def _split_args(text):
    out = []
    depth = 0
    start = 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(text[start:i])
            start = i + 1
    out.append(text[start:])
    return out


def _parse_fo_term(text):
    text = text.strip()
    if "(" not in text:
        return ("var", text) if text[0].isupper() else ("func", text, ())
    name, rest = text.split("(", 1)
    return ("func", name, tuple(_parse_fo_term(part)
                                for part in _split_args(rest[:-1])))


def _fo_text(term):
    if term[0] == "var":
        return term[1]
    if not term[2]:
        return term[1]
    return f"{term[1]}(" + ",".join(_fo_text(arg) for arg in term[2]) + ")"


def _fo_apply(term, subst):
    if term[0] == "var" and term[1] in subst:
        return _fo_apply(subst[term[1]], subst)
    if term[0] == "func":
        return ("func", term[1], tuple(_fo_apply(arg, subst)
                                       for arg in term[2]))
    return term


def _fo_occurs(name, term, subst):
    term = _fo_apply(term, subst)
    if term[0] == "var":
        return term[1] == name
    return any(_fo_occurs(name, arg, subst) for arg in term[2])


def _fo_subst_text(subst):
    if not subst:
        return "{}"
    parts = [
        f"{name}={_fo_text(_fo_apply(term, subst))}"
        for name, term in sorted(subst.items())
    ]
    return "{" + ", ".join(parts) + "}"


def unification_oracle(problem):
    patterns = [
        r"Unify terms (.+) and (.+) with occurs-check",
        r"unifier of (.+) and (.+); use occurs-check",
        r"unification on (.+) = (.+), including occurs-check",
    ]
    for pattern in patterns:
        match = re.search(pattern, problem)
        if match:
            left, right = match.groups()
            break
    else:
        raise AssertionError(problem)
    subst = {}
    work = [(_parse_fo_term(left), _parse_fo_term(right))]
    while work:
        a, b = work.pop(0)
        a = _fo_apply(a, subst)
        b = _fo_apply(b, subst)
        if _fo_text(a) == _fo_text(b):
            continue
        if a[0] == "var":
            if _fo_occurs(a[1], b, subst):
                return f"failure; occurs-check {a[1]} in {_fo_text(b)}"
            subst[a[1]] = b
        elif b[0] == "var":
            work.insert(0, (b, a))
        elif a[1] == b[1] and len(a[2]) == len(b[2]):
            work = list(zip(a[2], b[2])) + work
        else:
            return f"failure; clash {_fo_text(a)} vs {_fo_text(b)}"
    return f"MGU = {_fo_subst_text(subst)}"


def _lambda_term_from_problem(problem):
    patterns = [
        r"term (.+) by leftmost",
        r"Normalize (.+) using leftmost",
        r"normal form of (.+), using",
    ]
    for pattern in patterns:
        match = re.search(pattern, problem)
        if match:
            return match.group(1)
    raise AssertionError(problem)


def _lambda_tokens(text):
    return re.findall(r"lambda|[a-z]+|[().]", text)


def _parse_lambda_term(tokens, pos=0):
    tok = tokens[pos]
    if tok != "(":
        return ("var", tok), pos + 1
    pos += 1
    if tokens[pos] == "lambda":
        name = tokens[pos + 1]
        term, pos = _parse_lambda_term(tokens, pos + 3)
        assert tokens[pos] == ")"
        return ("abs", name, term), pos + 1
    left, pos = _parse_lambda_term(tokens, pos)
    right, pos = _parse_lambda_term(tokens, pos)
    assert tokens[pos] == ")"
    return ("app", left, right), pos + 1


def _free_vars(term):
    if term[0] == "var":
        return {term[1]}
    if term[0] == "app":
        return _free_vars(term[1]) | _free_vars(term[2])
    return _free_vars(term[2]) - {term[1]}


def _rename_bound(term, old, new):
    if term[0] == "var":
        return ("var", new) if term[1] == old else term
    if term[0] == "app":
        return ("app", _rename_bound(term[1], old, new),
                _rename_bound(term[2], old, new))
    if term[1] == old:
        return term
    return ("abs", term[1], _rename_bound(term[2], old, new))


def _fresh_name(used):
    for name in ["z", "w", "v", "u"]:
        if name not in used:
            return name
    raise AssertionError(used)


def _lambda_substitute(term, var, value):
    if term[0] == "var":
        return value if term[1] == var else term
    if term[0] == "app":
        return ("app", _lambda_substitute(term[1], var, value),
                _lambda_substitute(term[2], var, value))
    param, body = term[1], term[2]
    if param == var:
        return term
    if param in _free_vars(value) and var in _free_vars(body):
        used = _free_vars(body) | _free_vars(value) | {var}
        new_param = _fresh_name(used)
        body = _rename_bound(body, param, new_param)
        param = new_param
    return ("abs", param, _lambda_substitute(body, var, value))


def _lambda_reduce_once(term):
    if term[0] == "app":
        left, right = term[1], term[2]
        if left[0] == "abs":
            return _lambda_substitute(left[2], left[1], right), True
        new_left, changed = _lambda_reduce_once(left)
        if changed:
            return ("app", new_left, right), True
        new_right, changed = _lambda_reduce_once(right)
        return ("app", left, new_right), changed
    if term[0] == "abs":
        body, changed = _lambda_reduce_once(term[2])
        return ("abs", term[1], body), changed
    return term, False


def _lambda_text(term):
    if term[0] == "var":
        return term[1]
    if term[0] == "abs":
        return f"lambda {term[1]}. {_lambda_text(term[2])}"
    return f"({_lambda_text(term[1])} {_lambda_text(term[2])})"


def lambda_reduction_oracle(problem):
    term, pos = _parse_lambda_term(_lambda_tokens(_lambda_term_from_problem(problem)))
    assert pos > 0
    for _ in range(10):
        term, changed = _lambda_reduce_once(term)
        if not changed:
            return f"normal form = {_lambda_text(term)}"
    raise AssertionError(problem)


def viterbi_oracle(problem):
    obs = re.search(r"observations ([AB]+)", problem).group(1)
    states = ["H", "L"]
    start = {"H": Fraction(1, 2), "L": Fraction(1, 2)}
    trans = {
        ("H", "H"): Fraction(3, 4), ("H", "L"): Fraction(1, 4),
        ("L", "H"): Fraction(1, 3), ("L", "L"): Fraction(2, 3),
    }
    emit = {
        ("H", "A"): Fraction(3, 4), ("H", "B"): Fraction(1, 4),
        ("L", "A"): Fraction(1, 4), ("L", "B"): Fraction(3, 4),
    }
    dp = {state: start[state] * emit[(state, obs[0])] for state in states}
    back = []
    for symbol in obs[1:]:
        new_dp = {}
        row = {}
        for state in states:
            prob, prev = max((dp[p] * trans[(p, state)] *
                              emit[(state, symbol)], p) for p in states)
            new_dp[state] = prob
            row[state] = prev
        dp = new_dp
        back.append(row)
    final_prob, final_state = max((dp[state], state) for state in states)
    path = [final_state]
    for row in reversed(back):
        path.append(row[path[-1]])
    path.reverse()
    return f"path = {'->'.join(path)}; probability = {frac_text(final_prob)}"


def entropy_rate_markov_oracle(problem):
    p00, p01, p10, p11 = [
        Fraction(x) for x in re.search(
            r"P00=([^,]+), P01=([^,]+), P10=([^,]+), P11=([^,]+)",
            problem,
        ).groups()
    ]
    info = {Fraction(k): Fraction(v.rstrip(".")) for k, v in re.findall(
        r"I\(([^)]+)\)=([0-9.]+)", problem
    )}
    a = p01
    b = p10
    pi0 = b / (a + b)
    pi1 = a / (a + b)
    h0 = p00 * info[p00] + p01 * info[p01]
    h1 = p10 * info[p10] + p11 * info[p11]
    return f"entropy_rate = {dec(pi0 * h0 + pi1 * h1)} bits/symbol"


def bec_channel_oracle(problem):
    eps = Fraction(re.search(r"epsilon=([^ .]+)", problem).group(1))
    q = 1 - eps
    if "capacity" in problem:
        return f"C = {frac_text(q)} bits/use"
    n = int(re.search(r"n=(\d+) uses", problem).group(1))
    if "no erasures" in problem:
        return f"P(no erasures in {n}) = {frac_text(q ** n)}"
    prob = Fraction(comb(n, 1)) * eps * (q ** (n - 1))
    return f"P(exactly one erasure in {n}) = {frac_text(prob)}"


def _bits_text(bits):
    return "".join(str(bit) for bit in bits)


def _conv_encode(bits):
    state = 0
    encoded = []
    for bit in bits:
        encoded.extend([bit ^ state, bit])
        state = bit
    return encoded


def convolutional_code_viterbi_oracle(problem):
    message, received = re.search(
        r"Encode message ([01]+).*received bits ([01]+)", problem
    ).groups()
    message_bits = [int(ch) for ch in message]
    received_bits = [int(ch) for ch in received]
    encoded = _conv_encode(message_bits)
    best = None
    for value in range(2 ** len(message_bits)):
        candidate = [int(ch) for ch in format(value, f"0{len(message_bits)}b")]
        cand_code = _conv_encode(candidate)
        dist = sum(a != b for a, b in zip(cand_code, received_bits))
        key = (dist, _bits_text(candidate))
        if best is None or key < best[0]:
            best = (key, candidate, dist)
    _, decoded, distance = best
    return (
        f"encoded={_bits_text(encoded)}; decoded={_bits_text(decoded)}; "
        f"distance={distance}"
    )


def reed_solomon_oracle(problem):
    p = 7
    points = [1, 2, 3, 4]

    def codeword(m0, m1):
        return [(m0 + m1 * x) % p for x in points]

    def list_text(values):
        return "[" + ",".join(str(v) for v in values) + "]"

    if "Encode Reed-Solomon" in problem:
        m0, m1 = map(int, re.search(r"m\(x\)=(\d+)\+(\d+)x", problem).groups())
        return f"codeword = {list_text(codeword(m0, m1))}"

    received = [int(x) for x in re.search(
        r"Received word is \[([0-6,]+)\]", problem
    ).group(1).split(",")]
    best = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i], received[i]
            x2, y2 = points[j], received[j]
            slope = ((y2 - y1) % p) * pow((x2 - x1) % p, -1, p) % p
            intercept = (y1 - slope * x1) % p
            candidate = codeword(intercept, slope)
            agree = sum(a == b for a, b in zip(candidate, received))
            if best is None or agree > best[0]:
                best = (agree, intercept, slope, candidate)
    _, m0, m1, corrected = best
    err_pos = next(i + 1 for i, (a, b) in enumerate(zip(corrected, received))
                   if a != b)
    return (
        f"message = [{m0},{m1}]; codeword = {list_text(corrected)}; "
        f"error_position = {err_pos}"
    )


def tonelli_shanks_oracle(problem):
    a, p = map(int, re.search(
        r"x\^2 congruent to (\d+) modulo prime (\d+)", problem
    ).groups())
    roots = [x for x in range(p) if (x * x) % p == a % p]
    assert len(roots) == 2
    return f"roots = {roots[0]}, {roots[1]} mod {p}"


def baby_step_giant_step_oracle(problem):
    g, h, p, order = map(int, re.search(
        r"solve (\d+)\^x congruent to (\d+) modulo (\d+), with "
        r"0 <= x < (\d+)",
        problem,
    ).groups())
    answers = [x for x in range(order) if pow(g, x, p) == h]
    assert len(answers) == 1
    return f"x = {answers[0]}"


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def _norm2(v):
    return _dot(v, v)


def _round_fraction(fr):
    if fr >= 0:
        return (fr.numerator + fr.denominator // 2) // fr.denominator
    return -_round_fraction(-fr)


def _basis_text(b1, b2):
    return f"[({b1[0]},{b1[1]}),({b2[0]},{b2[1]})]"


def lll_reduction_oracle(problem):
    basis = ast.literal_eval(re.search(r"basis (\[\([^)]+\),\([^)]+\)\])",
                                      problem).group(1))
    b1, b2 = tuple(basis[0]), tuple(basis[1])
    for _ in range(20):
        mu = Fraction(_dot(b2, b1), _norm2(b1))
        k = _round_fraction(mu)
        if k:
            b2 = (b2[0] - k * b1[0], b2[1] - k * b1[1])
            continue
        if _norm2(b2) < _norm2(b1):
            b1, b2 = b2, b1
            continue
        return f"reduced basis = {_basis_text(b1, b2)}"
    raise AssertionError(problem)


EC_P, EC_A, EC_N = 17, 2, 19
EC_G = (5, 1)


def point_text(point):
    return "O" if point is None else f"({point[0]},{point[1]})"


def ec_add(P, Q, p=EC_P, a=EC_A):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        slope = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p
    else:
        slope = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


def ec_scalar(k, point):
    acc = None
    for _ in range(k):
        acc = ec_add(acc, point)
    return acc


def ecdh_oracle(problem):
    alice, bob = map(int, re.search(
        r"Alice secret a=(\d+) and Bob secret b=(\d+)", problem
    ).groups())
    A_pub = ec_scalar(alice, EC_G)
    B_pub = ec_scalar(bob, EC_G)
    shared = ec_scalar(alice, B_pub)
    assert shared == ec_scalar(bob, A_pub)
    return (
        f"A={point_text(A_pub)}; B={point_text(B_pub)}; "
        f"shared={point_text(shared)}"
    )


def ecdsa_oracle(problem):
    d, z, k = map(int, re.search(
        r"private key d=(\d+), message hash z=(\d+), and nonce k=(\d+)",
        problem,
    ).groups())
    Q = ec_scalar(d, EC_G)
    R = ec_scalar(k, EC_G)
    r = R[0] % EC_N
    s = (pow(k, -1, EC_N) * (z + r * d)) % EC_N
    w = pow(s, -1, EC_N)
    u1 = (z * w) % EC_N
    u2 = (r * w) % EC_N
    X = ec_add(ec_scalar(u1, EC_G), ec_scalar(u2, Q))
    verdict = "valid" if X is not None and X[0] % EC_N == r else "invalid"
    return f"signature = (r={r}, s={s}); verification = {verdict}"


def assert_exact_step_arithmetic(case, result):
    for raw_step in result["steps"]:
        fields = raw_step.split(DELIM)
        if fields[0] == "M" and len(fields) == 4:
            case.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif fields[0] == "A" and len(fields) == 4:
            case.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif fields[0] == "S" and len(fields) == 4:
            case.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif fields[0] == "E" and len(fields) == 4:
            case.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                             Fraction(fields[3]), raw_step)
        elif fields[0] == "MOD_REDUCE":
            mod = int(fields[2].split()[1])
            case.assertEqual(int(fields[1]) % mod, int(fields[3]), raw_step)

import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lambda_reduction_generator import LambdaReductionGenerator
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe

FRESH_ORDER = ["z", "w", "v", "u"]


def tokenize(text):
    return re.findall(r"lambda|[a-z]+|[().]", text)


def parse(tokens, pos=0):
    tok = tokens[pos]
    if tok == "lambda":
        name = tokens[pos + 1]
        assert tokens[pos + 2] == ".", tokens
        body, pos = parse(tokens, pos + 3)
        return ("abs", name, body), pos
    if tok != "(":
        return ("var", tok), pos + 1
    pos += 1
    if tokens[pos] == "lambda":
        name = tokens[pos + 1]
        assert tokens[pos + 2] == ".", tokens
        body, pos = parse(tokens, pos + 3)
        assert tokens[pos] == ")", tokens
        return ("abs", name, body), pos + 1
    left, pos = parse(tokens, pos)
    right, pos = parse(tokens, pos)
    assert tokens[pos] == ")", tokens
    return ("app", left, right), pos + 1


def term_of(text):
    tokens = tokenize(text)
    term, pos = parse(tokens)
    assert pos == len(tokens), text
    return term


def balanced_term(problem):
    """The parenthesised lambda term embedded in any of the phrasings."""
    start = problem.index("(")
    depth = 0
    for i in range(start, len(problem)):
        if problem[i] == "(":
            depth += 1
        elif problem[i] == ")":
            depth -= 1
            if depth == 0:
                return problem[start:i + 1]
    raise AssertionError(problem)


def render(term):
    if term[0] == "var":
        return term[1]
    if term[0] == "abs":
        return f"(lambda {term[1]}. {render(term[2])})"
    return f"({render(term[1])} {render(term[2])})"


def render_top(term):
    if term[0] == "abs":
        return f"lambda {term[1]}. {render(term[2])}"
    return render(term)


def free_vars(term):
    if term[0] == "var":
        return {term[1]}
    if term[0] == "app":
        return free_vars(term[1]) | free_vars(term[2])
    return free_vars(term[2]) - {term[1]}


def rename_bound(term, old, new):
    if term[0] == "var":
        return ("var", new) if term[1] == old else term
    if term[0] == "app":
        return ("app", rename_bound(term[1], old, new),
                rename_bound(term[2], old, new))
    if term[1] == old:
        return term
    return ("abs", term[1], rename_bound(term[2], old, new))


def substitute(term, var, value, log=None):
    if term[0] == "var":
        return value if term[1] == var else term
    if term[0] == "app":
        return ("app", substitute(term[1], var, value, log),
                substitute(term[2], var, value, log))
    param, body = term[1], term[2]
    if param == var:
        return term
    if param in free_vars(value) and var in free_vars(body):
        used = free_vars(body) | free_vars(value) | {var}
        new_param = next(n for n in FRESH_ORDER if n not in used)
        renamed = rename_bound(body, param, new_param)
        if log is not None:
            log.append((render_top(("abs", param, body)),
                        render_top(("abs", new_param, renamed))))
        body, param = renamed, new_param
    return ("abs", param, substitute(body, var, value, log))


def lo_step(term, log=None):
    """One leftmost-outermost beta step, or None."""
    if term[0] == "app":
        if term[1][0] == "abs":
            return substitute(term[1][2], term[1][1], term[2], log)
        left = lo_step(term[1], log)
        if left is not None:
            return ("app", left, term[2])
        right = lo_step(term[2], log)
        if right is not None:
            return ("app", term[1], right)
        return None
    if term[0] == "abs":
        inner = lo_step(term[2], log)
        if inner is not None:
            return ("abs", term[1], inner)
    return None


def ao_step(term):
    """One applicative-order (innermost-leftmost) beta step, or None."""
    if term[0] == "app":
        left = ao_step(term[1])
        if left is not None:
            return ("app", left, term[2])
        right = ao_step(term[2])
        if right is not None:
            return ("app", term[1], right)
        if term[1][0] == "abs":
            return substitute(term[1][2], term[1][1], term[2])
        return None
    if term[0] == "abs":
        inner = ao_step(term[2])
        if inner is not None:
            return ("abs", term[1], inner)
    return None


def normalize(term, stepper, limit=40):
    for _ in range(limit):
        nxt = stepper(term)
        if nxt is None:
            return term
        term = nxt
    raise AssertionError("did not normalize")


def normalize_with_count(term, stepper, limit=40):
    count = 0
    for _ in range(limit):
        nxt = stepper(term)
        if nxt is None:
            return term, count
        term = nxt
        count += 1
    raise AssertionError("did not normalize")


def church_value(term):
    if term[0] != "abs" or term[2][0] != "abs":
        return None
    function_name, base_name = term[1], term[2][1]
    body = term[2][2]
    count = 0
    while body[0] == "app" and body[1] == ("var", function_name):
        body = body[2]
        count += 1
    return count if body == ("var", base_name) else None


def debruijn(term, env=()):
    """Nameless form, so alpha-equivalent terms compare equal."""
    if term[0] == "var":
        if term[1] in env:
            return ("b", env.index(term[1]))
        return ("f", term[1])
    if term[0] == "abs":
        return ("l", debruijn(term[2], (term[1],) + env))
    return ("a", debruijn(term[1], env), debruijn(term[2], env))


def leftmost_redex(term):
    if term[0] == "app":
        if term[1][0] == "abs":
            return term[1], term[2]
        return leftmost_redex(term[1]) or leftmost_redex(term[2])
    if term[0] == "abs":
        return leftmost_redex(term[2])
    return None


def oracle(problem, operation=None):
    term = term_of(balanced_term(problem))
    normal, count = normalize_with_count(term, lo_step)
    # Independent route: applicative order reaches the same normal form
    # (Church-Rosser), compared up to alpha-renaming via de Bruijn indices.
    other = normalize(term, ao_step)
    assert debruijn(normal) == debruijn(other), problem
    assert lo_step(normal) is None, problem
    if operation and operation.endswith(("church_succ", "church_add")):
        value = church_value(normal)
        assert value is not None
        return f"Church numeral {value}; normal form = {render_top(normal)}"
    if operation and operation.endswith("beta_count"):
        return f"normal form = {render_top(normal)}; beta steps = {count}"
    return f"normal form = {render_top(normal)}"


def check_steps(case, result):
    steps = [s.split(DELIM) for s in result["steps"]]
    case.assertEqual(steps[0][0], "LAMBDA_SETUP")
    case.assertEqual(steps[0][2], "leftmost-outermost")
    term = term_of(steps[0][1])
    case.assertEqual(term, term_of(balanced_term(result["problem"])))
    i = 1
    beta_count = 0
    while steps[i][0] == "BETA":
        beta_count += 1
        fn_text, arg_text = steps[i][1].split(" applied to ")
        fn, arg = term_of(fn_text), term_of(arg_text)
        case.assertEqual((fn, arg), leftmost_redex(term))
        i += 1
        while steps[i][0] == "ALPHA_RENAME":
            before = term_of(steps[i][1])
            after = term_of(steps[i][2])
            case.assertEqual(before[0], "abs")
            case.assertEqual(after[0], "abs")
            case.assertEqual(after[2], rename_bound(before[2], before[1],
                                                    after[1]))
            case.assertNotIn(after[1], free_vars(before[2]))
            i += 1
        case.assertEqual(steps[i][0], "SUBSTITUTE")
        head, body_text = steps[i][1].split(" in ", 1)
        var, value_text = head.split(":=")
        case.assertEqual(var, fn[1])
        case.assertEqual(term_of(value_text), arg)
        case.assertEqual(term_of(body_text), fn[2])
        case.assertEqual(term_of(steps[i][2]),
                         substitute(fn[2], fn[1], arg))
        i += 1
        case.assertEqual(steps[i][0], "REWRITE")
        case.assertNotIn("applied", steps[i][1])
        expected = lo_step(term)
        case.assertEqual(term_of(steps[i][1]), expected)
        term = expected
        i += 1
    case.assertEqual(steps[i][0], "NO_REDEX")
    case.assertEqual(term_of(steps[i][1]), term)
    case.assertIsNone(lo_step(term))
    i += 1
    if result["operation"].endswith(("church_succ", "church_add")):
        case.assertEqual(steps[i][0], "CHURCH_NUMERAL")
        case.assertEqual(int(steps[i][1]), church_value(term))
        case.assertEqual(term_of(steps[i][2]), term)
        i += 1
        case.assertEqual(steps[i][0], "CHECK")
        i += 1
    elif result["operation"].endswith("beta_count"):
        case.assertEqual(steps[i], ["BETA_COUNT", str(beta_count)])
        i += 1
        case.assertEqual(steps[i][0], "CHECK")
        case.assertEqual(int(steps[i][2]), beta_count)
        i += 1
    case.assertEqual(i, len(steps) - 1)
    case.assertEqual(result["final_answer"],
                     oracle(result["problem"], result["operation"]))


class TestLambdaReductionGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = LambdaReductionGenerator()
        saw = set()
        openings = set()
        terms = set()
        problems = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             oracle(result["problem"], result["operation"]),
                             result["problem"])
            check_steps(self, result)
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 1)[0])
            terms.add(balanced_term(result["problem"]))
            problems.add(result["problem"])
        self.assertEqual(saw, {f"lambda_reduction_{v}"
                               for v in LambdaReductionGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 4)
        self.assertGreaterEqual(len(terms), 240)
        self.assertGreaterEqual(len(problems), 260)

    def test_explicit_variants(self):
        random.seed(31)
        for variant in LambdaReductionGenerator.VARIANTS:
            gen = LambdaReductionGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"lambda_reduction_{variant}")
                self.assertEqual(result["final_answer"],
                                 oracle(result["problem"], result["operation"]),
                                 result["problem"])
                check_steps(self, result)

    def test_new_variants_have_500_problem_text_oracles(self):
        random.seed(2026)
        variants = ("church_succ", "church_add", "beta_count")
        for index in range(500):
            variant = variants[index % len(variants)]
            result = LambdaReductionGenerator(variant).generate()
            self.assertEqual(result["final_answer"],
                             oracle(result["problem"], result["operation"]),
                             result["problem"])
            check_steps(self, result)

    def test_church_operands_are_at_most_three(self):
        random.seed(808)
        for _ in range(200):
            successor = LambdaReductionGenerator("church_succ").generate()
            succ_term = term_of(balanced_term(successor["problem"]))
            self.assertIn(church_value(succ_term[2]), range(4))
            addition = LambdaReductionGenerator("church_add").generate()
            add_term = term_of(balanced_term(addition["problem"]))
            self.assertIn(church_value(add_term[1][2]), range(4))
            self.assertIn(church_value(add_term[2]), range(4))

    def test_variant_semantics(self):
        random.seed(17)
        for _ in range(40):
            alpha = LambdaReductionGenerator("alpha").generate()
            self.assertTrue(any(s.startswith("ALPHA_RENAME|")
                                for s in alpha["steps"]))
            plain = LambdaReductionGenerator("identity").generate()
            self.assertFalse(any(s.startswith("ALPHA_RENAME|")
                                 for s in plain["steps"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            LambdaReductionGenerator("bad")


if __name__ == "__main__":
    unittest.main()

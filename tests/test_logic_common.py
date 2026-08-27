"""Tests for ``logic_common`` — checked against the independent oracle.

Every semantic claim is re-derived by ``tests/foundations_oracle.py`` (its own
parser, its own brute-force evaluator), never by ``logic_common`` itself.
"""
import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import logic_common as L  # noqa: E402
from tests import foundations_oracle as O  # noqa: E402

BANNED = ("|", "->", "<->", "&", "~")


def to_oracle(formula):
    """Structural conversion Formula -> oracle AST (no printing involved)."""
    if isinstance(formula, L.Const):
        return ("const", formula.value)
    if isinstance(formula, L.Var):
        return ("var", formula.name)
    if isinstance(formula, L.Not):
        return ("not", to_oracle(formula.arg))
    kinds = {L.And: "and", L.Or: "or", L.Imp: "imp", L.Iff: "iff",
             L.Xor: "xor", L.Nand: "nand"}
    return (kinds[type(formula)], to_oracle(formula.left),
            to_oracle(formula.right))


def sample_formulas(count, seed=11, depths=(1, 2, 3), constants=False,
                    connectives=L.ALL_CONNECTIVES,
                    alphabets=(L.PROP_VARS[:2], L.PROP_VARS[:3], L.ALT_VARS)):
    rng = random.Random(seed)
    out = []
    for index in range(count):
        depth = depths[index % len(depths)]
        names = alphabets[index % len(alphabets)]
        out.append(L.random_formula(depth, names, connectives, rng=rng,
                                    constants=constants))
    return out


# --- independent law-shape checks -------------------------------------------
# The oracle route for "the step is really De Morgan": re-describe each law
# directly on oracle ASTs, without consulting logic_common's pattern table.

def _dual(kind):
    return {"and": "or", "or": "and"}[kind]


def law_shape_ok(name, before, after):
    if name == "double negation":
        return before[0] == "not" and before[1][0] == "not" \
            and after == before[1][1]
    if name == "De Morgan":
        return (before[0] == "not" and before[1][0] in ("and", "or")
                and after == (_dual(before[1][0]),
                              ("not", before[1][1]), ("not", before[1][2])))
    if name == "negation":
        if before[0] not in ("and", "or"):
            return False
        left, right = before[1], before[2]
        opposite = (left == ("not",) + (right,) or right == ("not",) + (left,))
        return opposite and after == ("const", before[0] == "or")
    if name == "idempotent":
        return before[0] in ("and", "or") and before[1] == before[2] \
            and after == before[1]
    if name == "domination":
        if before[0] not in ("and", "or"):
            return False
        absorbing = before[0] == "or"
        for side, other in ((before[1], before[2]), (before[2], before[1])):
            if side == ("const", absorbing) and after == ("const", absorbing):
                return True
        return False
    if name == "identity":
        if before[0] not in ("and", "or"):
            return False
        neutral = before[0] == "and"
        for side, other in ((before[1], before[2]), (before[2], before[1])):
            if side == ("const", neutral) and after == other:
                return True
        return False
    if name == "absorption":
        if before[0] not in ("and", "or"):
            return False
        inner_kind = _dual(before[0])
        for side, other in ((before[1], before[2]), (before[2], before[1])):
            if side[0] == inner_kind and other in (side[1], side[2]) \
                    and after == other:
                return True
        return False
    if name == "distributive":
        if before[0] not in ("and", "or"):
            return False
        inner = _dual(before[0])
        left, right = before[1], before[2]
        if left[0] != inner or right[0] != inner or left[1] != right[1]:
            return False
        return after == (inner, left[1], (before[0], left[2], right[2]))
    if name == "implication elimination":
        return before[0] == "imp" \
            and after == ("or", ("not", before[1]), before[2])
    if name == "biconditional elimination":
        return before[0] == "iff" and after == (
            "and", ("imp", before[1], before[2]),
            ("imp", before[2], before[1]))
    if name == "contrapositive":
        return before[0] == "imp" and after == (
            "imp", ("not", before[2]), ("not", before[1]))
    return False


class PrinterTest(unittest.TestCase):
    def test_plan_examples(self):
        p, q, r = L.Var("p"), L.Var("q"), L.Var("r")
        self.assertEqual(L.render(L.Imp(L.And(p, L.Not(q)), r)),
                         "(p ∧ ¬q) → r")
        self.assertEqual(L.render(L.Not(L.And(p, q))), "¬(p ∧ q)")
        self.assertEqual(L.render(L.Not(L.Not(p))), "¬¬p")
        self.assertEqual(L.render(L.And(L.Or(p, q), r)), "(p ∨ q) ∧ r")
        self.assertEqual(L.render(L.Or(p, L.And(q, r))), "p ∨ (q ∧ r)")
        self.assertEqual(L.render(L.Nand(p, q)), "p ↑ q")
        self.assertEqual(L.render(L.Xor(p, q)), "p ⊕ q")
        self.assertEqual(L.render(L.TRUE), "T")
        self.assertEqual(L.render(L.FALSE), "F")

    def test_round_trip_through_oracle_parser(self):
        formulas = sample_formulas(3000, seed=5, constants=True)
        for formula in formulas:
            text = L.render(formula)
            self.assertEqual(O.parse_formula(text), to_oracle(formula), text)
            # the printed form is exactly the canonical one
            self.assertTrue(O.is_canonical_formula(text), text)
            for banned in BANNED:
                self.assertNotIn(banned, text)

    def test_every_inner_binary_is_parenthesized(self):
        for formula in sample_formulas(500, seed=7):
            text = L.render(formula)
            node = O.parse_formula(text)
            self.assertEqual(O.render(node), text)

    def test_dialects(self):
        a, b = L.Var("A"), L.Var("B")
        expression = L.And(L.Or(a, b), L.Or(a, L.Not(b)))
        self.assertEqual(L.render(expression, L.SET), "(A ∪ B) ∩ (A ∪ Bᶜ)")
        self.assertEqual(L.render(expression, L.CIRCUIT),
                         "(A OR B) AND (A OR NOT B)")
        self.assertEqual(L.render(L.And(a, L.Not(b)), L.CIRCUIT),
                         "A AND NOT B")
        self.assertEqual(L.render(L.FALSE, L.SET), "∅")
        self.assertEqual(L.render(L.TRUE, L.SET), "U")
        self.assertEqual(L.render(L.Var("p"), L.SET, var_map={"p": "A"}), "A")
        with self.assertRaises(ValueError):
            L.render(L.Imp(a, b), L.SET)
        self.assertEqual(L.law_label("negation", L.SET), "complement")
        self.assertEqual(L.law_label("negation"), "negation")

    def test_structure_helpers(self):
        p, q, r = L.Var("p"), L.Var("q"), L.Var("r")
        formula = L.Imp(L.And(p, L.Not(q)), r)
        self.assertEqual(L.variables(formula), ("p", "q", "r"))
        self.assertEqual(L.depth(formula), 3)
        self.assertEqual(L.main_connective(formula), "→")
        self.assertIsNone(L.main_connective(p))
        self.assertEqual(len(L.subformulas(formula)), 6)


class SemanticsTest(unittest.TestCase):
    def test_row_order_is_textbook(self):
        rows = L.assignments(["q", "p"])
        self.assertEqual([L.row_text(row) for row in rows],
                         ["p=T, q=T", "p=T, q=F", "p=F, q=T", "p=F, q=F"])

    def test_column_examples(self):
        p, q = L.Var("p"), L.Var("q")
        self.assertEqual(L.truth_column(L.Imp(p, q)), "TFTT")
        self.assertEqual(L.truth_column(L.And(p, q)), "TFFF")
        self.assertEqual(L.truth_column(L.Or(p, q)), "TTTF")
        self.assertEqual(L.truth_column(L.Iff(p, q)), "TFFT")
        self.assertEqual(L.truth_column(L.Xor(p, q)), "FTTF")
        self.assertEqual(L.truth_column(L.Nand(p, q)), "FTTT")
        self.assertEqual(L.truth_column(L.Not(p)), "FT")

    def test_columns_match_oracle(self):
        for formula in sample_formulas(2000, seed=13, constants=True):
            text = L.render(formula)
            names = sorted(set(L.variables(formula)))
            self.assertEqual(L.truth_column(formula, names),
                             O.truth_column(text, names), text)
            self.assertEqual(L.classify(formula), O.classify(text), text)

    def test_equivalence_matches_oracle(self):
        formulas = sample_formulas(600, seed=17)
        for first, second in zip(formulas, formulas[1:]):
            expected = O.equivalent(L.render(first), L.render(second))
            self.assertEqual(L.equivalent(first, second), expected)
            difference = L.first_difference(first, second)
            oracle_difference = O.first_difference(L.render(first),
                                                   L.render(second))
            self.assertEqual(difference, oracle_difference)

    def test_models_and_row_text(self):
        p, q = L.Var("p"), L.Var("q")
        self.assertEqual([L.row_text(row) for row in L.models(L.And(p, q))],
                         ["p=T, q=T"])
        self.assertEqual(L.column_text([True, False]), "TF")


class NormalFormTest(unittest.TestCase):
    def test_nnf(self):
        for formula in sample_formulas(1000, seed=19, constants=True):
            nnf = L.to_nnf(formula)
            text = L.render(nnf)
            self.assertTrue(O.is_nnf(O.parse_formula(text)), text)
            self.assertTrue(O.equivalent(L.render(formula), text), text)

    def test_cnf_and_dnf(self):
        for formula in sample_formulas(600, seed=23,
                                       connectives=L.BASIC_CONNECTIVES):
            source = L.render(formula)
            cnf = L.render(L.to_cnf(formula))
            dnf = L.render(L.to_dnf(formula))
            self.assertTrue(O.is_cnf(O.parse_formula(cnf)), cnf)
            self.assertTrue(O.is_dnf(O.parse_formula(dnf)), dnf)
            self.assertTrue(O.equivalent(source, cnf), (source, cnf))
            self.assertTrue(O.equivalent(source, dnf), (source, dnf))

    def test_canonical_cnf_and_dnf(self):
        for formula in sample_formulas(400, seed=29,
                                       connectives=L.BASIC_CONNECTIVES):
            source = L.render(formula)
            cnf = L.canonical_cnf(formula)
            dnf = L.canonical_dnf(formula)
            self.assertTrue(O.equivalent(source, L.render(cnf)))
            self.assertTrue(O.equivalent(source, L.render(dnf)))
            # canonical forms are idempotent
            self.assertEqual(L.render(L.canonical_cnf(cnf)), L.render(cnf))
            self.assertEqual(L.render(L.canonical_dnf(dnf)), L.render(dnf))

    def test_cnf_distribution_order_is_stated(self):
        p, q, r = L.Var("p"), L.Var("q"), L.Var("r")
        self.assertEqual(L.render(L.to_cnf(L.Or(L.And(p, q), r))),
                         "(p ∨ r) ∧ (q ∨ r)")
        self.assertEqual(L.render(L.to_cnf(L.Or(p, L.And(q, r)))),
                         "(p ∨ q) ∧ (p ∨ r)")
        self.assertEqual(L.render(L.to_dnf(L.And(L.Or(p, q), r))),
                         "(p ∧ r) ∨ (q ∧ r)")

    def test_evaluate_constants(self):
        p = L.Var("p")
        self.assertEqual(L.evaluate_constants(L.And(p, L.TRUE)), p)
        self.assertEqual(L.evaluate_constants(L.Or(p, L.TRUE)), L.TRUE)
        self.assertEqual(L.evaluate_constants(L.Not(L.FALSE)), L.TRUE)


class SubstitutionTest(unittest.TestCase):
    def test_uniform_substitution_matches_oracle(self):
        rng = random.Random(31)
        for formula in sample_formulas(400, seed=37):
            names = L.variables(formula)
            if not names:
                continue
            target = rng.choice(names)
            replacement = L.random_formula(1, L.ALT_VARS, rng=rng)
            substituted = L.substitute(formula, {target: replacement})
            source_ast = O.parse_formula(L.render(formula))
            new_ast = O.parse_formula(L.render(substituted))
            all_names = sorted(set(O.formula_variables(source_ast))
                               | set(O.formula_variables(new_ast)))
            for row in O.all_assignments(all_names):
                inner = O.eval_formula(
                    O.parse_formula(L.render(replacement)), row)
                shifted = dict(row)
                shifted[target] = inner
                self.assertEqual(O.eval_formula(new_ast, row),
                                 O.eval_formula(source_ast, shifted))

    def test_substitution_is_simultaneous(self):
        p, q = L.Var("p"), L.Var("q")
        swapped = L.substitute(L.Imp(p, q), {"p": q, "q": p})
        self.assertEqual(L.render(swapped), "q → p")

    def test_rename(self):
        self.assertEqual(L.render(L.rename(L.And(L.Var("p"), L.Var("q")),
                                           {"p": "a", "q": "b"})), "a ∧ b")


class PolishTest(unittest.TestCase):
    def test_examples(self):
        p, q, r = L.Var("p"), L.Var("q"), L.Var("r")
        self.assertEqual(L.to_polish(L.Imp(L.And(p, L.Not(q)), r)), "CKpNqr")
        self.assertEqual(L.to_polish(L.Iff(p, q)), "Epq")
        self.assertEqual(L.to_polish(L.Or(p, q)), "Apq")
        self.assertEqual(L.render(L.from_polish("CKpqr")), "(p ∧ q) → r")

    def test_round_trip_against_oracle(self):
        for formula in sample_formulas(2000, seed=41, constants=True,
                                       alphabets=(L.PROP_VARS[:3],
                                                  L.ALT_VARS)):
            polish = L.to_polish(formula)
            self.assertEqual(L.from_polish(polish), formula)
            self.assertEqual(O.parse_polish(polish), to_oracle(formula))
            self.assertEqual(O.to_polish(to_oracle(formula)), polish)

    def test_uppercase_variables_are_rejected(self):
        with self.assertRaises(ValueError):
            L.to_polish(L.Var("A"))

    def test_bad_polish_strings(self):
        for text in ("Kp", "pq", "Z", "Npq"):
            with self.assertRaises(ValueError):
                L.from_polish(text)


class RandomFormulaTest(unittest.TestCase):
    def test_depth_and_alphabet_controls(self):
        rng = random.Random(43)
        for _ in range(400):
            formula = L.random_formula(3, L.PROP_VARS[:3], rng=rng)
            self.assertLessEqual(L.depth(formula), 3)
            self.assertTrue(set(L.variables(formula)) <= set(L.PROP_VARS[:3]))

    def test_exact_depth_and_use_all(self):
        rng = random.Random(47)
        for _ in range(200):
            formula = L.random_formula(3, L.ALT_VARS, rng=rng,
                                       exact_depth=True, use_all=True)
            self.assertEqual(L.depth(formula), 3)
            self.assertEqual(set(L.variables(formula)), set(L.ALT_VARS))

    def test_connective_restriction(self):
        rng = random.Random(53)
        for _ in range(200):
            formula = L.random_formula(3, L.PROP_VARS[:2], ("¬", "∧", "∨"),
                                       rng=rng)
            text = L.render(formula)
            for symbol in ("→", "↔", "⊕", "↑"):
                self.assertNotIn(symbol, text)


class LawEngineTest(unittest.TestCase):
    def test_law_table_shape(self):
        expected = {"double negation", "De Morgan", "distributive",
                    "absorption", "idempotent", "identity", "domination",
                    "negation", "implication elimination",
                    "biconditional elimination", "contrapositive"}
        self.assertEqual(set(L.LAW_NAMES), expected)
        for law in L.LAW_TABLE:
            for rule in law.rules:
                self.assertTrue(O.equivalent(
                    L.render(L.substitute(_ground(rule.lhs), {})),
                    L.render(_ground(rule.rhs))),
                    rule.key)

    def test_rewrites_preserve_equivalence_and_name(self):
        checked = set()
        for formula in sample_formulas(800, seed=59, constants=True):
            current = formula
            for rewrite in L.simplify(formula):
                before = L.render(rewrite.before)
                after = L.render(rewrite.after)
                self.assertTrue(O.equivalent(before, after),
                                (rewrite.law, before, after))
                self.assertIn(rewrite.law, L.LAW_NAMES)
                self.assertTrue(
                    law_shape_ok(rewrite.law, O.parse_formula(before),
                                 O.parse_formula(after)),
                    (rewrite.law, before, after))
                checked.add(rewrite.law)
                # the whole formula changes only at the rewritten redex
                self.assertEqual(rewrite.whole_before, current)
                self.assertTrue(O.equivalent(L.render(rewrite.whole_before),
                                             L.render(rewrite.whole_after)))
                current = rewrite.whole_after
            self.assertTrue(O.equivalent(L.render(formula), L.render(current)))
        self.assertGreaterEqual(len(checked), 6)

    def test_triple_and_iteration_interface(self):
        p, q = L.Var("p"), L.Var("q")
        rewrites = L.simplify(L.Not(L.And(p, L.Not(q))))
        self.assertEqual(rewrites[0].triple(),
                         ("De Morgan", "¬(p ∧ ¬q)", "¬p ∨ ¬¬q"))
        law, before, after = rewrites[0]
        self.assertEqual(law, "De Morgan")
        self.assertEqual(L.render(before), "¬(p ∧ ¬q)")
        self.assertEqual(L.render(after), "¬p ∨ ¬¬q")
        self.assertEqual(rewrites[0].triple(L.SET)[0], "De Morgan")

    def test_simplify_reaches_a_fixed_point(self):
        for formula in sample_formulas(400, seed=61, constants=True):
            final = L.simplified(formula)
            self.assertIsNone(L.rewrite_once(final), L.render(final))

    def test_forced_order(self):
        # implication elimination outranks the ∧/∨ laws, so the first step of
        # a formula with a → is always the elimination.
        p, q = L.Var("p"), L.Var("q")
        formula = L.And(L.Imp(p, q), L.Or(p, p))
        first = L.simplify(formula)[0]
        self.assertEqual(first.law, "implication elimination")

    def test_set_order_leaves_arrows_alone(self):
        a, b = L.Var("A"), L.Var("B")
        formula = L.And(L.Or(a, b), L.Or(a, L.Not(b)))
        rewrites = L.simplify(formula, order=L.SET_LAW_ORDER)
        self.assertEqual([r.law for r in rewrites],
                         ["distributive", "negation", "identity"])
        self.assertEqual(L.render(rewrites[-1].whole_after), "A")
        self.assertEqual(
            [r.triple(L.SET) for r in rewrites][1],
            ("complement", "B ∩ Bᶜ", "∅"))

    def test_obfuscate_round_trip(self):
        rng = random.Random(67)
        p, q, r = L.Var("p"), L.Var("q"), L.Var("r")
        targets = [p, L.Not(p), L.And(p, q), L.Or(p, q), L.Xor(p, q),
                   L.TRUE, L.FALSE, L.And(p, L.Or(q, r)),
                   L.Or(L.And(p, q), r)]
        for target in targets:
            for steps in (2, 3, 4):
                obfuscated = L.obfuscate(target, steps, rng=rng)
                self.assertNotEqual(obfuscated, target)
                self.assertTrue(O.equivalent(L.render(target),
                                             L.render(obfuscated)))
                path = L.simplify(obfuscated, target=target)
                self.assertTrue(path)
                self.assertEqual(path[-1].whole_after, target)

    def test_obfuscate_in_the_set_fragment(self):
        rng = random.Random(71)
        a, b = L.Var("A"), L.Var("B")
        for target in (a, L.And(a, b), L.Or(a, b)):
            obfuscated = L.obfuscate(target, 3, order=L.SET_LAW_ORDER,
                                     rng=rng, pool=[a, b])
            text = L.render(obfuscated, L.SET)
            self.assertNotIn("|", text)
            path = L.simplify(obfuscated, order=L.SET_LAW_ORDER, target=target)
            self.assertEqual(path[-1].whole_after, target)

    def test_obfuscate_reports_failure(self):
        with self.assertRaises(L.ObfuscationError):
            L.obfuscate(L.Var("p"), 2, order=("contrapositive",), attempts=3)

    def test_pattern_matching(self):
        p, q = L.Var("p"), L.Var("q")
        rule = L.LAWS["De Morgan"].rules[0]
        bindings = L.match(rule.lhs, L.Not(L.And(p, L.Or(p, q))))
        self.assertEqual(bindings["A"], p)
        self.assertEqual(bindings["B"], L.Or(p, q))
        self.assertIsNone(L.match(rule.lhs, L.Not(L.Or(p, q))))
        self.assertEqual(L.instantiate(rule.rhs, bindings),
                         L.Or(L.Not(p), L.Not(L.Or(p, q))))

    def test_positions_and_replacement(self):
        p, q = L.Var("p"), L.Var("q")
        formula = L.And(p, L.Not(q))
        paths = [path for path, _ in L.positions(formula)]
        self.assertEqual(paths, [(), (0,), (1,), (1, 0)])
        self.assertEqual(L.node_at(formula, (1, 0)), q)
        self.assertEqual(L.render(L.replace_at(formula, (1,), q)), "p ∧ q")


def _ground(pattern):
    """Replace metavariables by fresh variables so a pattern can be tested."""
    mapping = {"A": L.Var("a"), "B": L.Var("b"), "C": L.Var("c")}

    def walk(node):
        if isinstance(node, L.Meta):
            return mapping[node.name]
        kids = L._children(node)
        if not kids:
            return node
        return L._rebuild(node, [walk(child) for child in kids])

    return walk(pattern)


class PipeSafetyTest(unittest.TestCase):
    def test_no_ascii_bar_anywhere(self):
        for formula in sample_formulas(500, seed=73, constants=True):
            for dialect in (L.PROPOSITIONAL,):
                self.assertNotIn("|", L.render(formula, dialect))
            self.assertNotIn("|", L.to_polish(formula))
        for law in L.LAW_TABLE:
            self.assertNotIn("|", law.name)


if __name__ == "__main__":
    unittest.main()

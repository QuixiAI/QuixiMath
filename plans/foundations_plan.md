# Foundations Curriculum Plan

Logic, sets, relations, functions, the construction of number, cardinality
and order, and axiomatic/formal systems — the Principia Mathematica ladder,
rebuilt as procedural, hand-solvable, oracle-checkable generators in the same
scratchpad dialect as everything else in this repo.

The bar is unchanged from `TODO.md`: exact arithmetic only, human-like steps,
pipe-safe fields, A0 answer conventions, an A9 oracle test that recomputes the
answer from the problem text, near-infinite unique problems, one class per
skill registered in three places, `PROBLEM_TYPES.md` / `OPCODES.md`
regenerated.

Companion plans: `plans/probability_plan.md` (probability as a measure on the set
algebra built here — events are the rosters of Strand C, Venn regions become
probabilities, independence is a product law, conditioning is a renormalized
measure) and `plans/statistics_plan.md` (data displays, sampling distributions,
inference, study design, estimator theory). Shared numeric helpers (`exact()`,
the supplied-constant renderer with decoy rows) live in `prob_common.py`;
this strand's `logic_common.py` / `set_common.py` and the three conventions
tests share one ASCII-bar checker. `∣` (U+2223) means divisibility here, the
column separator in statistics displays, and is never used for conditioning
(`P(A given B)`).

## 1. What "foundational" means here

Principia builds mathematics in this order, and so does this plan:

| PM part | Content | Plan strand |
|---|---|---|
| I.A (*1–*5) | theory of deduction — propositional calculus | A. Propositional logic |
| I.B (*9–*14) | apparent variables — quantifiers, descriptions | B. Predicate logic |
| I.C (*20–*25) | classes | C. Sets |
| I.D–E (*30–*43) | logic of relations, products/sums of classes | D. Relations, functions, order |
| II–III (*50–*126) | prolegomena to and theory of cardinal arithmetic (incl. *54.43, 1+1=2) | E. Number and infinity |
| V (*200–*276) | series (orders, well-orders, ordinals) | E. Number and infinity |
| apparatus | axioms, substitution, modus ponens, theory of types | F. Axiomatics and formal systems |
| — | concrete pre-formal versions for grades 3–8 | G. Concrete foundations |

Everything below is something a person can finish with pencil and paper by a
deterministic procedure. Topics with no exact procedure (Russell's paradox as
a *phenomenon*, incompleteness, independence of CH, informal "write a proof")
are deliberately out of scope; see §8.

## 2. Current coverage and gaps

Already in the registry (keep, extend where noted):

| Class | Band | Covers | Gap |
|---|---|---|---|
| `SetOperationsGenerator` | college d2 | ∪ ∩ − on letter sets, power set, A×B | no universe/complement, no Δ, no nesting, no integers; banded far too high for what it is |
| `RelationCheckGenerator` | college d2 | reflexive/symmetric/antisymmetric/transitive | no closures, composition, classes, orders |
| `BooleanAlgebraGenerator` | college d3 | DNF/CNF from a truth table, 2-var K-map | circuit dialect (AND/OR/NOT); no law-by-law simplification |
| `ResolutionProofGenerator` | college d4 | resolution refutation of 3 fixed CNFs | 3 fixed instances — tiny space |
| `DPLLTraceGenerator` | college d4 | DPLL on small CNF | — |
| `UnificationGenerator` | graduate d4 | MGU with occurs-check | — |
| `LambdaReductionGenerator` | graduate d4 | β-reduction of identity/constant/α cases | no Church numerals, no combinators |
| `InductionVerifyGenerator` | high d5 | base case + k→k+1 for 5 identities | no strong induction / well-ordering |
| `InclusionExclusionGenerator`, `CountingClassicsGenerator`, `StarsAndBarsGenerator`, `DerangementGenerator`, `PermutationCombinationGenerator` | college/middle | counting | no counting of *structures* (functions, relations, partitions) |
| `TuringMachineTraceGenerator`, `DFA/NFA/PDA`, `RegexToAutomaton`, `CYKParser` | college | computation models | — |

Not represented anywhere today: truth tables, tautology/equivalence, laws of
logic, conditional forms, argument validity, natural deduction, tableaux,
quantifiers over finite domains, quantifier negation, prenex form,
set-builder notation, Venn region counting, set identities, subset/element
distinction, cardinality by pairing, characteristic vectors, equivalence
classes, closures, composition of relations, partial orders/Hasse diagrams,
injective/surjective/bijective, Peano recursion, integers/rationals as
pairs, Dedekind cuts, von Neumann ordinals, Kuratowski pairs, Cantor
pairing, countability bijections, diagonalization, ordinal and cardinal
arithmetic, Hilbert-style axiomatic derivation, Gödel numbering, SKI
combinators, type theory, ZF axiom identification, counterexample search,
knights-and-knaves, logic grids.

## 3. Strand-wide rules (in addition to AGENTS.md)

**Notation (one dialect, used in problems, steps, and answers).**
- Connectives: `¬ ∧ ∨ → ↔ ⊕`, NAND written `↑` (never the ASCII bar).
  Precedence `¬` > `∧` > `∨` > `→` > `↔`; **every binary subformula except the
  outermost is parenthesized** so printing is unambiguous and canonical:
  `(p ∧ ¬q) → r`. Variables `p q r s` (propositional), `P Q R` (predicates),
  `x y z` (individuals), domains as rosters.
- Truth values `T`/`F` in tables and answers. Truth-table rows enumerate
  variables alphabetically, `T` before `F` (the textbook order `TT, TF, FT,
  FF`); a table's result column is written as one string, e.g. `TFTT`.
- Quantifiers `∀x ∃x`, membership `∈ ∉`, subset `⊆ ⊂`, ops `∪ ∩ − Δ ×`,
  complement `Aᶜ`, empty set `∅`, universe `U`, power set `P(A)`.
- **Set-builder uses a colon**: `{x ∈ ℤ : −3 ≤ x < 4}`. Divisibility uses
  the word (`3 divides 12`) or `∣` (U+2223), never ASCII `|`.
- **Cardinality is `card(A)`**, never `|A|`.
- Rosters: elements sorted (integers ascending, letters alphabetical, nested
  sets by depth then text), no duplicates, `{1, 2, 3}` spacing. Ordered pairs
  `(a, b)`. Partitions: blocks sorted by least element, written as a set of sets
  `{{1, 3}, {2}, {4, 5}}`.
- Composite verdict answers join facts with `; ` and put the checkable fact
  after the label: `valid; modus tollens`, `not equivalent; differ at p=T,
  q=F`, `injective no (f(2) = f(4) = 3); surjective yes; bijective no`.
- These become a new "Logic and set answers" block in DESIGN.md §Answer
  Format Conventions (Phase 0 deliverable).

**Pipe safety is stricter here.** ASCII `|` is banned from problem text as
well as steps for every generator in this strand (set-builder, cardinality,
divisibility, Sheffer stroke, and absolute value are the usual leaks). A
strand-level test enforces it (§6).

**Determinism for proof-shaped tasks.** A proof is not unique; the record
must be. Use exactly one of these, stated in the problem text the way
`ResolutionProofGenerator` already does:
1. a canonical strategy with tie-breaks ("apply modus ponens to the earliest
   applicable pair of lines; alphabetical order of variables"), so the trace
   is forced;
2. a *justify* form — the derivation is given, the rule names/line
   references are the answer;
3. a *missing line* form (the fill-in-the-step critic pattern);
4. a composite answer made of facts that are canonical regardless of proof
   route (verdict + first counterexample in enumeration order + mood code).

**Tiny answer spaces.** `true/false`, `valid/invalid`, `tautology`,
`reflexive yes` are coin flips; every such answer is composite (Principle 8)
with the witness that earns it: the first counterexample row, the first
witness in domain order, the smallest counterexample integer, the mood-figure
code, the missed element or the colliding pair.

**Capacity.** Every new generator must pass
`uv run python tools/probe_generator_capacity.py --threshold 1000`. Where
the mathematical space is inherently small (there are only 16 two-variable
truth functions), widen by construction: many syntactically different formulas
per function, several variable alphabets, integer domains drawn from ranges,
and 3–5 problem phrasings. Known-small exceptions are recorded in the class
docstring.

**Oracles (A9).** The generator builds an AST and prints it; the test parses
the printed problem text with an *independent* recursive-descent parser and
solves by brute force (enumerate assignments / elements / permutations). The
two never share code. Sympy only if stdlib-exact arithmetic genuinely cannot
express the oracle (none of the specs below need it).

**Phrasing.** 3–5 templates per generator from day one, including
word-problem framings where natural (Venn counts, hotel rooms, islanders,
grid puzzles, "which axiom lets us form this set").

## 4. Phase 0 — shared infrastructure

Built once, before any generator, each with its own tests.

- `logic_common.py` (repo root, beside `helpers.py`): propositional AST
  (`Var, Not, And, Or, Imp, Iff, Xor, Nand`), random formula builder with
  depth/variable/connective controls, canonical printer (§3), evaluator,
  truth-table column, equivalence, NNF, CNF/DNF by distribution, uniform
  substitution, Polish (Łukasiewicz) notation printer, and a **law-rewriting
  engine** — a table of named laws (double negation, De Morgan, distributive,
  absorption, idempotent, identity, domination, negation, implication
  elimination, biconditional elimination, contrapositive) each stored as a
  pattern pair and applied in a stated order so the rewrite sequence is
  forced. The engine has three surface dialects: propositional (`∧ ∨ ¬`),
  set (`∩ ∪ ᶜ`), Boolean circuit (`AND OR NOT`, to stay compatible with
  `BooleanAlgebraGenerator`).
- `set_common.py`: roster/pair/partition/relation formatters per §3,
  set-builder rendering, hereditarily-finite-set encode/decode/rank, small
  finite-structure helpers (relation matrices, cover relation, closures,
  Warshall passes with per-pass snapshots).
- `tests/foundations_oracle.py`: the independent parser for formulas,
  rosters, pairs, partitions, set-builder predicates, and ordinals in Cantor
  normal form; brute-force evaluators. Every foundations test imports from
  here, never from `logic_common`/`set_common`.
- `tests/test_foundations_conventions.py`: for every generator tagged as
  foundations (a module-level `FOUNDATIONS = True`), sample 200 examples and
  assert: no ASCII `|` anywhere in problem/steps/answer; answers parse under
  the oracle grammar for their declared answer kind; connective symbols are
  the canonical ones; rosters are sorted and duplicate-free.
- DESIGN.md: "Logic and set answers" convention block; README coverage
  bullets get a "Foundations" line at the end of the project.
- Op-code plan (reuse first, then add): reuse `TRUTH_ROW`, `SET_SETUP`,
  `ELEMENT_SCAN`, `COUNT`, `CHECK`, `CHECK_POINT`, `TRY/REJECT/ACCEPT`,
  `REWRITE`, `INDUCT_*`, `RESOLVE/DERIVED`, `SUBSTITUTE`, `UNFOLD`-style
  codes, `PF_STEP/PF_PRIME`, `GCD_*`. New codes are listed per generator
  below; they follow the one-code-one-meaning rule and are regenerated into
  `OPCODES.md` at the end of each phase.

## 5. The curriculum

Format per entry: **Class** · band · difficulty — variants; problem; procedure
(op-codes); answer; oracle; capacity/backward construction. `⟲` marks an
existing class being extended.

### Strand G — Concrete foundations (elementary / middle)

**AttributeSortingGenerator** · elementary · d1 — `two_attributes`,
`three_attributes`, `neither_region`. Problem: a list of 8–12 small integers
(or shapes with side counts) and two attributes ("even", "greater than 10",
"multiple of 3", "one-digit"); sort into Venn regions. Steps:
`ATTR_CHECK|item|attribute|yes/no` per item per attribute, `REGION|label|
roster`. Answer: composite region rosters `both: {12, 18}; only even: {4, 8};
only >10: {11, 15}; neither: {3, 7}`. Oracle: recompute attributes by
arithmetic. Capacity: unbounded (integers × attribute pairs).

**OneToOneCorrespondenceGenerator** · elementary · d1 — `compare_by_pairing`,
`count_by_pairing`, `cardinal_class`. Problem: two rosters of objects
(names/emoji-free words); pair them off in order and decide which set has
more / whether they are equinumerous; `cardinal_class`: which of several
rosters share the same cardinal number. Steps: `PAIR|a_i|b_i`,
`UNPAIRED|side|roster`, `COUNT`. Answer: `same size (5 each)` /
`A has 2 more (7 vs 5)`. This is PM's definition of cardinal number made
concrete. Oracle: count. Capacity: unbounded.

**LogicalConnectiveEvalGenerator** · elementary · d2 — `and_or`,
`not`, `nested`. Problem: `Let p: 12 is even. Let q: 12 > 20. Is p ∧ ¬q true
or false?` with atomic statements drawn from parity, comparison, divisibility,
primality, digit facts (each decided with the existing `DIV_CHECK`/`CMP`
style step). Steps: `STMT_EVAL|p|12 is even|T`, `CONNECTIVE|¬q|T`,
`CONNECTIVE|p ∧ ¬q|T`. Answer: composite `p = T; q = F; p ∧ ¬q = T`.
Oracle: recompute atoms arithmetically, evaluate. Capacity: unbounded.

**OperationPropertiesGenerator** · elementary · d2 — `identify`,
`apply`, `equality_chain`. Problem: which property justifies
`4 × (5 + 2) = 4 × 5 + 4 × 2`; rewrite `3 + 9` using the commutative
property; given `a = b, b = 7`, find `a` (substitution/transitivity). Steps:
`PROPERTY_MATCH|pattern|instance`, `REWRITE`, `CHECK` by evaluating both
sides. Answer: `distributive; both sides = 28` (composite: name + value so
name-guessing is not enough). Oracle: structural match + arithmetic.
Capacity: unbounded.

**SetMembershipSubsetGenerator** · elementary · d2 — `membership`,
`subset`, `equality`, `element_vs_subset`, `count`. Problem: rosters with
duplicates, mixed order, and one level of nesting; decide `2 ∈ A`,
`{2} ⊆ A`, `{2} ∈ A`, `A = B`, `card(A)`. Steps: `ELEMENT_SCAN`,
`SUBSET_CHECK|element|in B?`, `DEDUP|roster|reduced`, `COUNT`. Answer:
composite `2 ∈ A: yes; {2} ⊆ A: yes; {2} ∈ A: no` or `A = B (both {1, 2, 3})`.
Oracle: parse rosters. Capacity: unbounded.

**SetBuilderRosterGenerator** · middle · d2 — `integer_range`,
`parity_divisibility`, `squares_primes`, `compound_condition`, `cardinality`.
Problem: `List the elements of {x ∈ ℤ : −4 ≤ x < 5 and x is odd}`; predicates
combine a range with parity/divisibility/`x² < n`/primality. Steps:
`DOMAIN|candidates|−4..4`, `TRY|x|test`, `ACCEPT`/`REJECT` per candidate,
`ROSTER|result`. Answer: sorted roster or `∅`; `cardinality` variant answers
`card = 4`. Oracle: enumerate the stated range. Capacity: unbounded. (This is
PM's "class determined by a propositional function", concretely.)

**VennRegionCountGenerator** · middle · d3 — `two_set`, `three_set`,
`word_problem`. Problem: given `card(U)`, `card(A)`, `card(B)`,
`card(A ∩ B)` (or the 3-set analogue with pairwise and triple counts), find
every region. Built backward from region counts so all numbers are consistent
and non-negative. Steps: `REGION_EQ|A∩B|3`, `S` for each subtraction,
`REGION|only A|5`, `CHECK|sum of regions|card(U)`. Answer: composite
`only A = 5; only B = 7; both = 3; neither = 10`. Oracle: solve the linear
system by subtraction. Capacity: unbounded; word-problem framings (classes,
clubs, pets).

**CounterexampleSearchGenerator** · middle · d2 — `arithmetic_claim`,
`algebraic_claim`, `set_claim`. Problem: a false universal claim with a small
smallest counterexample: "every odd number greater than 1 is prime", "for
all n ≥ 1, n² + n + 11 is prime", "if 6 divides n then 4 divides n", "for
all sets A, B: A − B = B − A" (over a fixed universe). Claims are drawn from
parametrized families known to fail, and the generator verifies the smallest
counterexample lies within a hand-checkable scan (≤ 12 trials). Steps:
`TRY|n=3|check`, `ACCEPT`/`REJECT` per trial, `COUNTEREXAMPLE|n=9|9 = 3×3`.
Answer: `n = 9 (9 = 3 × 3)` — the smallest counterexample in scan order.
Oracle: rescan from the problem text. Capacity: parameters × families ×
phrasings, > 1000.

**ConditionalFormsGenerator** · middle · d2 — `symbolic`, `english`,
`truth_with_counterexample`, `biconditional_split`. Problem: state the
converse/inverse/contrapositive of `If a number is divisible by 4, then it is
even` (templated mathematical conditionals with known truth values); the
truth variant also asks whether the converse holds, answering with the
smallest counterexample. Steps: `COND_PARTS|hypothesis|conclusion`,
`FORM|converse|If ... then ...`, `TRY/REJECT/ACCEPT` scan for the
counterexample. Answer: the sentence (from the template grammar) or composite
`converse: false (counterexample 6)`. Oracle: template inversion + scan.
Capacity: templates × parameters, > 1000.

**KnightsKnavesGenerator** · middle · d3 — `two_islanders`,
`three_islanders`, `one_statement_each`. Problem: islanders A, B, (C); each
makes a statement from a fixed grammar ("B is a knave", "we are both
knights", "at least one of us is a knave", "A and B are the same type").
Generated by choosing the truth assignment first and adding statements until
exactly one assignment survives (brute force). Steps: `CASE|A=knight,
B=knave`, `STATEMENT_EVAL|A says ...|T|consistent`, `REJECT|case|contradiction`,
`ACCEPT|case`. Cases enumerate in a stated order (A before B, knight before
knave). Answer: `A knight, B knave`. Oracle: brute force over assignments.
Capacity: grammar × names × count, > 1000.

**LogicGridPuzzleGenerator** · middle · d3 — `three_by_three`,
`three_by_three_two_categories`, `four_by_four`. Problem: people ×
attribute(s) with clue types "X has Y", "X does not have Y", "the person with
Y has Z", "X's item comes before/after Y's" (for ordered attributes); solution
chosen first, clues added until unique. Steps: `CLUE_APPLY|clue k|marks`,
`ELIMINATE|row|value`, `DEDUCE|X|Y|only option left`, `CHECK|clue k|holds`.
The step order is fixed: clues in order, then rows-then-columns elimination
passes. Answer: composite mapping `Ann: cat; Ben: dog; Cy: fish`. Oracle:
brute-force permutations. Capacity: unbounded.

**⟲ SetOperationsGenerator** — re-band `college d2 → middle d2`; add
variants `complement` (with a stated universe), `symmetric_difference`,
`integer_elements`, `two_step` (`(A ∪ B) − C`); keep power set and Cartesian
product. Existing tests extended, not replaced.

### Strand A — Propositional logic (high / college / graduate)

**SyllogismGenerator** · high · d2 — `validity`, `mood_figure`,
`venn_test`. Problem: two categorical premises and a conclusion over three
terms (`All A are B. Some C are not B. Therefore some C are not A.`), terms
drawn from a noun bank. Steps: `MOOD|AAA|figure 1`, `VENN_SHADE|A − B|empty`,
`VENN_MARK|C ∩ ¬B|x`, `CONCLUSION_CHECK|forced/not forced`. Answer:
composite `valid; AAA-1` or `invalid; OAO-2`. Oracle: brute force the three
terms over subsets of a 3-element universe (two witnesses for particular
premises plus one element to falsify a universal conclusion suffice) and
recompute mood/figure from the premise shapes. Capacity: 256 forms × noun
triples × phrasings.

**TruthTableGenerator** · high · d2 — `column`, `classify`,
`equivalence`, `two_variable` (kept simpler for early exposure). Problem:
random formula in 2–3 variables (depth ≤ 3); produce the column; classify
tautology/contradiction/contingency; decide equivalence of two formulas.
Steps: `TT_SETUP|variables|rows`, `TRUTH_ROW|p=T, q=F` then
`EVAL_SUB|row|subformula|value` per inner node, `TT_COLUMN|TFTT`,
`CLASSIFY|contingency|T at 3 of 4 rows`. Answer: `TFTT` / `tautology; TTTT` /
`not equivalent; differ at p=T, q=F` (first differing row). Oracle: parse and
enumerate. Capacity: formulas per truth function are unbounded.

**ArgumentFormGenerator** · high · d3 — `named_rule`, `fallacy`,
`truth_table_validity`, `english`. Problem: premises and conclusion, symbolic
or in templated English; identify the rule (modus ponens, modus tollens,
hypothetical syllogism, disjunctive syllogism, simplification, conjunction,
addition, constructive dilemma) or the fallacy (affirming the consequent,
denying the antecedent), and verify by table: rows where all premises are T
must have the conclusion T. Steps: `ARG_SETUP`, `TRUTH_ROW` + `PREMISES_ALL_T|
row|yes/no`, `CONCLUSION_AT|row|T/F`, `VALIDITY|valid` or
`COUNTEREXAMPLE|p=F, q=T`. Answer: `valid; modus tollens` or
`invalid; affirming the consequent; counterexample p=F, q=T`. Oracle: brute
force. Capacity: rule × variable renaming × phrasing × substituted
subformulas, > 1000.

**LogicalEquivalenceLawsGenerator** · high · d4 — `simplify`, `to_cnf`,
`to_dnf`, `nand_only`, `implication_free`. Built backward: choose a canonical
target from a fixed family (`p`, `¬p`, `p ∧ q`, `p ∨ q`, `p → q`, `p ⊕ q`,
`T`, `F`, and their 3-variable analogues) and obfuscate it by applying inverse
laws 2–4 times; the forward simplification, law by law, is the record.
Steps: `LAW|De Morgan|¬(p ∧ q)|¬p ∨ ¬q`, `REWRITE|current formula`, final
`CHECK|truth table|TFTT|TFTT`. Answer: the canonical target string. Oracle:
parse the problem formula, compute its truth table, and find the unique
family member with the same table (family members are pairwise inequivalent
by construction). `nand_only` rewrites with `↑` using the three standard
identities; `to_cnf` uses a stated distribution order. Capacity: unbounded.

**WFFParsingGenerator** · high · d2 — `is_wff`, `main_connective`,
`depth_and_subformulas`, `polish_to_infix`, `infix_to_polish`. Problem: a
string that is either a canonical formula or a near-miss (dropped
parenthesis, dangling connective, doubled operator); Polish notation uses
Łukasiewicz letters `N K A C E`. Steps: `SCAN|token|stack depth`, `PARSE|
subformula|node`, `MAIN_CONNECTIVE|→`, `DEPTH|3`, `POLISH|CKpqr`. Answer:
`wff; main connective →; depth 3; 7 subformulas` or `not a wff (unmatched
parenthesis at position 6)`; conversions answer the converted string.
Oracle: independent parser. Capacity: unbounded.

**NaturalDeductionGenerator** · college · d4 — `forward_chain`, `justify`,
`missing_line`, `conditional_proof`. `forward_chain`: premises are literals and
implications; the problem states "apply modus ponens / ∧-elimination to the
earliest applicable lines first" so the derivation is forced; answer is the
sequence of derived formulas. `justify`: a complete Fitch-style derivation
is given with rule names blanked; answer `3: →E 1,2; 4: ∧I 3,2; 5: ∨I 4`.
`missing_line`: one line replaced by `____`; answer is that line verbatim.
`conditional_proof`: a subproof opened with an assumption and closed by →I,
same justify format. Steps: `PREMISE|k|formula`, `APPLY|rule|lines|result`,
`SUBPROOF_OPEN|assume|formula`, `SUBPROOF_CLOSE|→I|formula`, `CHECK|
conclusion reached`. Oracle: recompute the forced chain / re-derive every
justification by matching rule schemas against the cited lines. Capacity:
unbounded (random premise sets).

**SemanticTableauGenerator** · college · d4 — `validity`,
`satisfiability`, `countermodel`. Problem: a 2–3 variable formula; build the
truth tree with the stated policy (α-rules before β-rules, expand the oldest
unexpanded line, leftmost branch first). Steps: `TABLEAU_ROOT|¬φ`,
`ALPHA|line|results`, `BETA|line|left|right`, `BRANCH_CLOSE|branch|p, ¬p`,
`BRANCH_OPEN|branch|assignment`. Answer: `closed; valid` or
`open; countermodel p=T, q=F, r=F` — the leftmost open branch, unassigned
variables set to F. Oracle: brute-force validity; for open results, verify
the stated assignment falsifies the formula and that it is the leftmost open
branch under the stated policy (test re-implements the policy).
Capacity: unbounded.

**HilbertAxiomDerivationGenerator** · graduate · d5 — `pm_axioms`,
`lukasiewicz_axioms`, `instance_identify`, `substitute`, `justify`. The
Principia core. Axiom sets: PM *1.2–*1.6 (Taut `p ∨ p → p`, Add `q → p ∨ q`,
Perm `p ∨ q → q ∨ p`, Assoc `p ∨ (q ∨ r) → q ∨ (p ∨ r)`, Sum `(q → r) → (p ∨ q
→ p ∨ r)`) with `p → q` defined as `¬p ∨ q`, and Łukasiewicz's three
(`p → (q → p)`; `(p → (q → r)) → ((p → q) → (p → r))`;
`(¬p → ¬q) → (q → p)`). `instance_identify`: which axiom is this formula an
instance of, and under what substitution; `substitute`: apply a given
substitution to a schema; `justify`: a 3–6 line derivation (built forward
by the generator from random instances + MP) with justifications blanked.
Steps: `AXIOM_MATCH|A1|p := q → p, q := r`, `SUBSTITUTE`, `MP|lines i, j|
result`, `CHECK|line k re-derived`. Answer: `A1 [p := (q → p), q := r]` or
`1: A2 [...]; 2: A1 [...]; 3: MP 1,2`. Oracle: schema matching by the
independent parser. Capacity: unbounded.

**⟲ ResolutionProofGenerator** — replace the three fixed CNFs with random
unsatisfiable 3–5 clause sets over 3–4 variables (verified unsatisfiable by
brute force), keeping the stated canonical resolution order. Space: 3 → many
thousands. Keep the three original cases as named variants for continuity.

### Strand B — Predicate logic

**QuantifierNegationGenerator** · high · d3 — `symbolic`, `english`,
`nested`, `with_counterexample`. Problem: negate `∀x (P(x) → Q(x))`,
`∃x ∀y R(x, y)`, or "every prime is odd"; push negation to the atoms.
Steps: `NEG_QUANT|¬∀x|∃x ¬`, `NEG_CONNECTIVE|¬(P → Q)|P ∧ ¬Q`, `REWRITE`.
Answer: the NNF formula in canonical print, or for `with_counterexample`
the composite `∃n (n prime ∧ n not odd); n = 2`. Oracle: independent NNF +
finite-model equivalence check over random small models; smallest
counterexample by scan. Capacity: unbounded.

**QuantifierFiniteDomainGenerator** · college · d3 — `arithmetic_predicate`
(domain `{1..6}`, `R(x, y)`: `x < y`, `x divides y`, `x + y = 7`,
`x² > y`), `relation_table` (R given as a roster of pairs), `function_table`
(f given as a table, sentences with equality), `nested_three`. Problem:
decide `∀x ∃y R(x, y)`, `∃x ∀y R(x, y)`, `∀x (P(x) → ∃y R(x, y))`. Steps:
`DOMAIN|{1, 2, 3, 4, 5}`, `QUANT_CASE|x=1`, `WITNESS|x=1|y=2|1 < 2` or
`NO_WITNESS|x=5|tried y=1..5`, `QUANT_RESULT|∀x ∃y|false`. Answer: composite
`true; witnesses y = 2, 3, 4, 5, 1` (first witness per x in domain order) or
`false; counterexample x = 5`. This is model checking, the semantic side of
PM Part I.B. Oracle: brute force. Capacity: unbounded.

**PrenexNormalFormGenerator** · college · d4 — `pull_out`, `rename_then_pull`,
`negation_then_prenex`. Problem: a formula with 2–3 quantifiers inside
connectives, occasionally with a clashing bound variable; the problem states
the left-to-right pulling order and the renaming scheme (`x → x1`). Steps:
`RENAME|∃x|∃x1`, `PULL|∀x|past ∧`, `NEG_QUANT`, `REWRITE`. Answer: the
prenex string. Oracle: matrix is quantifier-free, prefix is the expected
sequence, equivalence checked over random 2–3 element models. Capacity:
unbounded.

**EnglishToLogicGenerator** · college · d2 — `universal`, `existential`,
`restricted_quantifier`, `two_place`. Problem: a templated sentence
("Every student who passed studied", "Some dog is not friendly", "There is
a number less than every other number") with the predicate key supplied in
the problem (`S(x): x is a student`). Steps: `PREDICATES|key`,
`QUANT_CHOICE|every → ∀`, `SHAPE|restriction → implication`, `REWRITE`.
Answer: the canonical formula. Oracle: template inversion. Capacity:
templates × predicate bank, > 1000. (Lower priority — it is the most
template-shaped skill here; keep the grammar honest and varied.)

### Strand C — Sets

**SetExpressionGenerator** · high · d3 — `with_complement`, `two_step`,
`three_step`, `symmetric_difference`. Problem: `U = {1..10}`, three integer
sets, evaluate `(A ∪ B)ᶜ ∩ C` or `A Δ (B − C)` inside-out. Steps:
`SET_SETUP`, `SUBEXPR|A ∪ B|roster`, `ELEMENT_SCAN` per element for the
current operation, `REWRITE|current expression`. Answer: sorted roster / `∅`.
Oracle: evaluate by an independent parser. Capacity: unbounded.

**SetIdentityMembershipTableGenerator** · high · d3 — `verify_identity`,
`refute_identity`, `de_morgan`, `distributive`, `difference_laws`. Problem:
does `A − (B ∪ C) = (A − B) ∩ (A − C)` hold for all sets? Build the
8-row membership table (∈/∉ for A, B, C) for both sides. Steps:
`MEMBER_ROW|x∈A, x∉B, x∈C`, `EVAL_SUB|row|B ∪ C|∈`, `SIDE|left|∉`,
`SIDE|right|∉`, `TABLE_COMPARE|match/differ`. Answer: `identity; columns match`
or `not an identity; fails at x ∈ A, x ∉ B, x ∈ C` (first differing row).
Refuted identities are true identities with one connective perturbed.
Oracle: brute force over the 8 membership rows. Capacity: identity bank ×
perturbations × set-name alphabets × phrasing, > 1000; widen with random
3-set expressions rather than a fixed bank if the probe is short.

**SetCountingGenerator** · high · d3 — `subsets`, `k_subsets`,
`subsets_containing`, `functions`, `injections`, `bijections`,
`relations`, `reflexive_relations`, `symmetric_relations`, `partitions`
(Bell numbers via the Stirling/Bell triangle for n ≤ 6). Problem: "How many
functions from a 3-element set to a 5-element set?" with rosters given.
Steps: `COUNT_RULE|functions|card(B)^card(A)`, `E|5|3|125`, `M` chains for
falling factorials, `BELL_ROW|n=4|1 2 5 15`. Answer: integer. Oracle: exact
formula / brute force for n ≤ 4. Capacity: sizes 1–8 × variants × rosters ×
phrasing, > 1000.

**CharacteristicVectorGenerator** · college · d2 — `encode`, `decode`,
`bitwise_op`, `duality`. Problem: ordered universe `U = {a..h}`; write `A` as
a bit string, compute `A ∩ Bᶜ` bitwise, decode. Steps: `BIT|element|1/0`,
`BITWISE|AND|10110010|01011100|00010000`, `DECODE|00010000|{d}`. Answer:
composite `00010000 = {d}`. Oracle: recompute. Capacity: unbounded. (Bridges
sets to Boolean algebra — the duality PM exploits throughout Part I.)

**SetAlgebraLawsGenerator** · college · d3 — `simplify`, `dual_of_logic`,
`to_union_of_intersections`. The set dialect of the Phase-0 law engine:
`(A ∪ B) ∩ (A ∪ Bᶜ)` → `A` with each law named (De Morgan, absorption,
distributive, complement, identity, domination). Same backward construction
and canonical-target oracle as `LogicalEquivalenceLawsGenerator`, with the
truth-table check replaced by an 8-row membership-table `CHECK`. Capacity:
unbounded.

**HereditarilyFiniteSetGenerator** · college · d3 — `kuratowski_encode`,
`kuratowski_decode`, `von_neumann_numeral`, `successor`, `big_union`,
`transitive_check`, `rank`. Problem: write `(a, b)` as `{{a}, {a, b}}` and
back; write `3` as `{∅, {∅}, {∅, {∅}}}`; compute `S(n) = n ∪ {n}`; compute
`∪X` for a set of sets; is `X` transitive (every element is a subset);
what is the rank of a nested set. Steps: `NEST|level|content`,
`UNION_ELEMENT|x|contributes`, `TRANSITIVE_CHECK|element|⊆ X?`,
`RANK|element|r`. Answer: the set string in canonical nesting order, or an
integer, or `transitive: no ({∅} ∈ X but ∅ ∉ X)` (first violating element).
Oracle: independent nested-set parser. Capacity: unbounded.

### Strand D — Relations, functions, order

**RelationOperationsGenerator** · college · d3 — `inverse`, `composition`,
`matrix`, `domain_range`, `restriction`. Problem: `R ⊆ A × B`, `S ⊆ B × C`
as rosters (3–4 element sets); compute `S ∘ R`, `R⁻¹`, the 0/1 matrix,
domain and range. Steps: `REL_SETUP`, `COMPOSE_PAIR|(a, b)|(b, c)|(a, c)`,
`MATRIX_ROW|a|0 1 1 0`, `DOMAIN|roster`. Answer: sorted pair roster or the
matrix rows joined by `; `. Oracle: recompute. Capacity: unbounded.

**RelationClosureGenerator** · college · d3 — `reflexive`, `symmetric`,
`transitive_warshall`, `transitive_by_paths`, `equivalence_closure`.
Problem: closure of R on a 3–5 element set; Warshall runs one pass per
pivot with the matrix shown after each pass. Steps: `CLOSURE_ADD|(a, a)|
reflexive`, `WARSHALL_K|k=2|matrix rows`, `PATH|a→b→c|add (a, c)`, `CHECK|
transitive|no missing pair`. Answer: sorted pair roster. Oracle: independent
closure by iteration to a fixed point. Capacity: unbounded.

**EquivalenceRelationGenerator** · high · d3 — `check_and_classes`,
`from_partition`, `congruence_classes`, `same_property` (same parity, same
digit sum, same remainder), `count_pairs`. Problem: verify R is an
equivalence relation (reusing `RelationCheck` op-codes) and list the
partition; or build R from a given partition and count its pairs; or list
the classes of "same remainder mod 4" on `{0..11}`. Steps: `CLASS|[1]|{1, 3}`,
`PARTITION|blocks`, `COUNT|pairs|Σ card(block)²`. Answer: `{{1, 3}, {2},
{4, 5}}` (blocks sorted by least element) or an integer. Oracle: recompute
classes by union-find. Capacity: unbounded.

**PartialOrderGenerator** · college · d4 — `hasse_edges` (cover relation),
`extremal_elements` (minimal/maximal/least/greatest), `bounds_lub_glb`,
`linear_extension` (stated tie-break: smallest available label first, which
forces a unique order), `lattice_check`, `chains_antichains`. Posets:
divisibility on the divisors of n (n ≤ 60), subsets of a 3-set under ⊆,
explicit Hasse edge lists on 5–7 labelled points. Steps: `ORDER_PAIR|a ≤ b|
reason`, `COVER|a|b|no c strictly between`, `MINIMAL|roster`, `UB|{a, b}|
roster`, `LUB|c`, `TOPO_PICK|available {2, 3}|pick 2`. Answer: pair roster,
composite `minimal {2, 3}; maximal {12}; least none; greatest 12`, `lub 12;
glb 1`, or the linear order `1, 2, 3, 4, 6, 12`. Oracle: brute force on the
finite poset. Capacity: unbounded. (PM Part V "series", made finite.)

**FunctionPropertiesGenerator** · high · d3 — `classify` (injective /
surjective / bijective with witnesses), `image_preimage`, `compose_tables`,
`inverse_table`, `fixed_points`, `count_by_property`. Problem: `f: A → B`
as a table; decide properties; compute `f(S)`, `f⁻¹(T)`, `g ∘ f`. Steps:
`MAP|a|f(a)`, `COLLISION|f(2) = f(4) = 3` or `NO_COLLISION`, `MISSED|b=5`,
`PREIMAGE|b|{a : f(a) = b}`. Answer: composite `injective no (f(2) = f(4) =
3); surjective yes; bijective no`, or a roster / table. Oracle: recompute
from the table. Capacity: unbounded.

**RecursiveDefinitionUnfoldGenerator** · high · d3 — `one_arg` (factorial,
custom `f(n) = f(n − 1) + 2n`), `two_arg` (Ackermann `A(1, n)`, `A(2, n)`
for n ≤ 3; `gcd` by Euclid as recursion), `on_strings` (length, reverse,
count of a letter by recursion on the string), `mutual` (even/odd predicates
by mutual recursion). Problem: definition given in full; evaluate at a small
argument by unfolding then folding. Steps: `UNFOLD|f(4)|f(3) + 8`,
`BASE|f(0)|1`, `FOLD|f(1)|3`, arithmetic `A`/`M`. Answer: integer or string.
Oracle: independent evaluator. Capacity: unbounded.

**DirectProofAlgebraGenerator** · high · d4 — `parity_sum`,
`parity_product`, `consecutive_product_even`, `divisibility_transitive`,
`contrapositive_setup`, `contradiction_setup`. Problem: "Show that the sum
of two odd integers is even: write the algebra." Steps: `REPRESENT|odd m|
m = 2k + 1`, `REPRESENT|odd n|n = 2j + 1`, `EXPAND|m + n|2k + 2j + 2`,
`FACTOR|2(k + j + 1)`, `CONCLUDE|even`; setup variants answer with the
statement to be proved (`assume n is even; show n² is even` → contrapositive
of "n² odd ⇒ n odd"). Answer: the factored form `2(k + j + 1)` or the
canonical setup sentence. Oracle: polynomial identity by integer-coefficient
expansion (stdlib dict polynomials). Capacity: representations × coefficients
× claims, > 1000.

**⟲ InductionVerifyGenerator** — add `strong_induction` (every n ≥ 12 is
4a + 5b: base cases 12–15, step n → n + 4 with the concrete witness pair for
the checked n) and `well_ordering` (least counterexample argument set-up
with a numeric check). Existing variants untouched.

### Strand E — Number and infinity

**PeanoArithmeticGenerator** · college · d3 — `addition`, `multiplication`,
`exponentiation`, `leq_witness`, `predecessor_monus` (primitive recursion).
Problem: "Using a + 0 = a and a + S(b) = S(a + b), compute SS0 + SSS0" with
the recursion equations supplied in the text; numerals ≤ 6, mixed decimal /
successor notation across phrasings. Steps: `PEANO_EQ|SS0 + SSS0|S(SS0 + SS0)`
per unfolding, `PEANO_BASE|SS0 + 0|SS0`, `FOLD|S(S(S(SS0)))|SSSSS0`, `CHECK|
decimal|2 + 3 = 5`. Answer: composite `SSSSS0 = 5`. Oracle: count S's.
Capacity: moderate per variant (≤ 49 operand pairs); widen with three-term
expressions, both notations, and 4 phrasings; documented small space.

**IntegersAsPairsGenerator** · college · d3 — `equivalence_check`,
`canonical_representative`, `add`, `multiply`, `order`. Problem: ℤ as classes
of `(a, b)` with `(a, b) ~ (c, d)` iff `a + d = b + c`; add
`(3, 5) + (2, 1)`, reduce to `(0, 1)` or `(n, 0)`. Steps: `PAIR_RULE|(a, b) +
(c, d)|(a + c, b + d)`, `A`, `M`, `REDUCE|(5, 6)|(0, 1)`, `CHECK|value|−1`.
Answer: composite `(0, 1) ~ −1`. Oracle: integer arithmetic. Capacity:
unbounded.

**RationalsAsPairsGenerator** · college · d3 — `equivalence_check`
(cross-multiply), `add`, `multiply`, `canonical_form` (reduce with the
existing `GCD_*` steps), `order` (compare by cross products with positive
denominators). Answer: composite `(7, 6) = 7/6`. Oracle: `fractions.Fraction`.
Capacity: unbounded.

**DedekindCutGenerator** · college · d4 — `membership` (is `7/5` in the lower
set of the cut for √2: check `49/25 < 2`), `largest_of_list`,
`compare_cuts` (find which of the listed rationals separates √2 from 3/2),
`rational_cut` (cut for a rational r: no largest element in the lower set —
exhibit `(q + r)/2` between). Steps: `CUT_RULE|L(√2)|q < 0 or q² < 2`,
`E|7/5|2|49/25`, `CMP|49/25|2|<`, `MEMBER|7/5 ∈ L`. Answer: composite
`7/5 ∈ L (49/25 < 2); 3/2 ∉ L (9/4 > 2)`. Oracle: exact Fraction arithmetic.
Capacity: unbounded.

**CantorPairingGenerator** · college · d3 — `pair`, `unpair`
(triangular-root by `TRY` on `w(w + 1)/2 ≤ z`), `diagonal_enumeration`
(k-th pair in the diagonal walk of ℕ × ℕ; which position holds `(m, n)`).
Steps: `PAIRING|(m, n)|(m + n)(m + n + 1)/2 + n`, `M`, `D`, `A`, `TRY|w=5|15
≤ 17|ok`, `REJECT|w=6|21 > 17`, `UNPAIR|z=17|(3, 2)`. Answer: integer or pair.
Oracle: closed form. Capacity: unbounded.

**CountabilityBijectionGenerator** · college · d3 — `nat_to_int` (`f(n) =
n/2` even, `−(n + 1)/2` odd; evaluate and invert), `nat_to_evens`,
`nat_to_squares`, `calkin_wilf` (n-th positive rational by reading the binary
expansion of n: `0 → a/(a + b)`, `1 → (a + b)/b`), `hilbert_hotel` (room
reassignment phrasings of the same bijections). Steps: `BIJECTION_RULE`,
`CASE|n even`, `D`, `BINARY|13|1101`, `CW_STEP|bit 1|1/1 → 2/1`. Answer:
integer, pair, or fraction. Oracle: independent computation. Capacity:
unbounded.

**CantorDiagonalGenerator** · college · d3 — `binary_strings`,
`decimal_digits` (rule: replace digit d by 1 unless d = 1, then 2),
`function_table` (n functions ℕ → {0, 1} given as rows). Problem: a list of
n strings of length n; build a string not on the list. Steps: `DIAG|row k|
digit`, `FLIP|k|0 → 1`, `NEW_STRING|1001`, `CHECK|differs from row k at
position k` for each k. Answer: composite `diagonal 0110; new string 1001`.
Oracle: recompute; verify absence from the list. Capacity: unbounded.

**OrdinalArithmeticGenerator** · graduate · d4 — `add`, `multiply`,
`compare`, `normal_form`. Ordinals below ω^ω in Cantor normal form with
finite coefficients ≤ 5 and exponents ≤ 3. Problem: compute `(ω + 1) · 2`,
`1 + ω`, `ω · 2 + ω`, compare `ω^2` with `ω · 5 + 3`. Steps: `CNF|ω·2 + 1`,
`ORD_RULE|absorption|1 + ω = ω`, `ORD_RULE|left distributive|(ω + 1)·2 = (ω +
1) + (ω + 1)`, `REWRITE`, `ORD_CMP|leading exponents|2 > 1`. Answer:
canonical CNF `ω^2·3 + ω + 4` or `ω^2 > ω·5 + 3`. Oracle: independent CNF
arithmetic in `foundations_oracle.py`. Capacity: unbounded.

**CardinalArithmeticGenerator** · graduate · d3 — `add_multiply`
(κ + λ = κ · λ = max for infinite operands), `exponent` (`2^ℵ0 = c`,
`n^ℵ0 = c` for 2 ≤ n ≤ ℵ0, `ℵ0^n = ℵ0`, `c^ℵ0 = c`, `c^c = 2^c`),
`set_cardinality` (card of ℕ × ℕ, ℤ^3, ℚ, ℝ − ℚ, P(ℕ), finite sequences over
ℕ, functions ℕ → {0,1}). Problem: evaluate a 2–4 operand expression. Steps:
`CARD_RULE|κ · λ = max(κ, λ)|ℵ0 · c = c`, `REWRITE`. Answer: composite `c
(2^ℵ0)`, `ℵ0`, `2^c`, or a finite number. Oracle: rule engine re-implemented
independently. Capacity: unbounded expressions.

### Strand F — Axiomatics and formal systems (graduate)

**GodelNumberingGenerator** · graduate · d4 — `encode`, `decode`,
`symbol_lookup`. Problem: a symbol table (`¬ → 1, ∨ → 2, ( → 3, ) → 4, p → 5,
q → 7`) given in the text; encode a 3–5 symbol string as `2^c1 · 3^c2 · 5^c3
· …` (products kept ≤ 10^7 by construction), or decode a number by prime
factorization (reusing `PF_STEP`/`PF_PRIME`). Steps: `SYMBOL_CODE|¬|1`,
`GODEL_TERM|2^1|2`, `M` chain, `PF_STEP`, `GODEL_DECODE|exponents 1, 5, 2|¬ p
∨`. Answer: integer or symbol string. Oracle: recompute. Capacity: unbounded.

**CombinatoryLogicGenerator** · graduate · d4 — `ski_reduce`, `bck`,
`define_by_ski` (express `I` as `S K K`, verify on an argument),
`normal_form_count`. Terms built backward from a known normal form so every
problem terminates in ≤ 8 leftmost-outermost steps. Steps: `COMB_RULE|K x y|
x`, `COMB_RULE|S x y z|x z (y z)`, `REWRITE|current term`. Answer: normal-form
term string. Oracle: independent reducer with a step bound. Capacity:
unbounded. Also **⟲ LambdaReductionGenerator**: add `church_succ`,
`church_add` (numerals ≤ 3) and `beta_count`.

**TypeTheoryGenerator** · graduate · d4 — `simple_type_inference` (type of
`λx.λy.x`, `λf.λx.f (f x)`, `S`, `K`, applications of typed constants),
`typing_check` (does `f : A → B` applied to `a : A` type-check), `pm_levels`
(individuals type 0, classes of type-n objects type n + 1; is `x ∈ y`
well-formed given the types; what type is `{x : φ(x)}`; flag `x ∈ x` as
ill-typed). Steps: `TYPE_ASSIGN|x|a`, `TYPE_ABS|λx.…|a → …`, `TYPE_APP|f a|
unify|b`, `LEVEL|y|1`, `MEMBERSHIP_OK|type(y) = type(x) + 1`. Answer: the
type string `a → b → a` or composite `well-typed; type 2` / `ill-typed (x ∈ x
needs type(x) = type(x) + 1)`. Oracle: independent inference. Capacity:
unbounded.

**ZFAxiomIdentifyGenerator** · graduate · d3 — `single_step`, `construction_
sequence`, `definition_expansion`. Problem: given sets A, B, which ZF axiom
guarantees `{A, B}`, `∪A`, `P(A)`, `{x ∈ A : φ}`, `{f(x) : x ∈ A}`, `ω`; or
list the axioms used, in order, to build `A ∪ B = ∪{A, B}` (Pairing, Union),
`A × B` (Pairing, Power set ×2, Separation), `{A}` (Pairing with A = B).
Steps: `FORM|{A, B}|Pairing`, `FORM|∪{A, B}|Union`, `EXPAND|A ∪ B|∪{A, B}`.
Answer: composite `Pairing, Union` (ordered). Oracle: expansion table.
Capacity: expression trees of depth ≤ 3, > 1000 with phrasing.

**StructureIsomorphismGenerator** · graduate · d4 — `check_given_map`,
`find_map` (canonical: first permutation in lexicographic order that works,
with degree/in-degree pruning shown as `REJECT`), `non_isomorphic_invariant`
(first invariant that differs: sizes, degree multiset, cycle count, fixed
points). Structures: directed graphs / relations / small posets on 3–4
labelled points. Steps: `INVARIANT|out-degrees|{0, 1, 2}|{0, 1, 2}`,
`TRY|f = 1→b, 2→a, 3→c`, `EDGE_CHECK|(1, 2)|(b, a)|present`, `ACCEPT`.
Answer: `isomorphic; f = 1→b, 2→a, 3→c` or `not isomorphic; out-degree
multisets differ`. Oracle: brute force. Capacity: unbounded.

### Critic records for the strand

**FoundationsCriticGenerator** · college · d4 — `truth_table_error` (one
row evaluated wrongly, propagated into the column and the classification),
`membership_table_error`, `missing_justification` (natural-deduction or
Hilbert derivation with one rule name blanked), `missing_line` (one derived
formula blanked). Same record shapes as `ErrorSpottingGenerator` /
`FillInStepGenerator`: `VERIFY|k|ok`, `FLAG|k|<true value>`, redo, `Z|step k;
<correct answer>`. Built on top of the strand's own generators. Oracle:
recompute the correct table/derivation from the problem text.

## 6. Band and difficulty summary

| Band | New classes | Extended |
|---|---:|---|
| elementary | 5 (AttributeSorting, OneToOneCorrespondence, LogicalConnectiveEval, OperationProperties, SetMembershipSubset) | — |
| middle | 6 (SetBuilderRoster, VennRegionCount, CounterexampleSearch, ConditionalForms, KnightsKnaves, LogicGridPuzzle) | SetOperations (re-banded) |
| high | 13 (Syllogism, TruthTable, ArgumentForm, LogicalEquivalenceLaws, WFFParsing, QuantifierNegation, SetExpression, SetIdentityMembershipTable, SetCounting, EquivalenceRelation, FunctionProperties, RecursiveDefinitionUnfold, DirectProofAlgebra) | InductionVerify |
| college | 19 (NaturalDeduction, SemanticTableau, QuantifierFiniteDomain, PrenexNormalForm, EnglishToLogic, CharacteristicVector, SetAlgebraLaws, HereditarilyFiniteSet, RelationOperations, RelationClosure, PartialOrder, PeanoArithmetic, IntegersAsPairs, RationalsAsPairs, DedekindCut, CantorPairing, CountabilityBijection, CantorDiagonal, FoundationsCritic) | ResolutionProof |
| graduate | 8 (HilbertAxiomDerivation, OrdinalArithmetic, CardinalArithmetic, GodelNumbering, CombinatoryLogic, TypeTheory, ZFAxiomIdentify, StructureIsomorphism) | LambdaReduction |

Total: **51 new generator classes, 4 extended**, roughly 190 operation
variants. This moves the catalog from 36 → 41 elementary and 64 → 71 middle
skills, which also nudges the equal-per-skill mix toward the recipe in
`plans/dataset_plan.md`.

## 7. Delivery order

One generator per commit (`add truth table generator`), tests in the same
commit, docs regenerated at the end of each phase. Each phase ends with:
`uv run python -m unittest discover tests`, the capacity probe on the new
classes, a 200-example seeded build per class with zero errors, and
`OPCODES.md` / `PROBLEM_TYPES.md` regeneration with `--check` passing.

| Phase | Deliverable | Why this order |
|---|---|---|
| 0 | `logic_common.py`, `set_common.py`, `tests/foundations_oracle.py`, conventions test, DESIGN.md block | everything downstream prints and parses the same dialect |
| 1 | Strand G (11 classes) + SetOperations re-band | cheapest, fills the thinnest bands, exercises the set formatters before harder strands depend on them |
| 2 | TruthTable, WFFParsing, ArgumentForm, LogicalEquivalenceLaws, Syllogism, SetExpression, SetIdentityMembershipTable, SetCounting | the propositional core and its set dual; validates the law engine |
| 3 | FunctionProperties, EquivalenceRelation, RelationOperations, RelationClosure, PartialOrder, RecursiveDefinitionUnfold, DirectProofAlgebra, CharacteristicVector, SetAlgebraLaws, InductionVerify extension | relations/functions/order — PM Parts I.D–E and V |
| 4 | QuantifierNegation, QuantifierFiniteDomain, PrenexNormalForm, EnglishToLogic, NaturalDeduction, SemanticTableau, ResolutionProof widening | predicate logic and formal deduction |
| 5 | HereditarilyFiniteSet, PeanoArithmetic, IntegersAsPairs, RationalsAsPairs, DedekindCut, CantorPairing, CountabilityBijection, CantorDiagonal, OrdinalArithmetic, CardinalArithmetic | the construction of number, from ∅ to ℵ and ω |
| 6 | HilbertAxiomDerivation, GodelNumbering, CombinatoryLogic (+Lambda extension), TypeTheory, ZFAxiomIdentify, StructureIsomorphism | the Principia apparatus proper |
| 7 | FoundationsCriticGenerator; phrasing sweep to 3–5 templates everywhere; full capacity probe; README inventory/coverage update; regenerate `PROBLEM_TYPES.md`, `OPCODES.md`; note the strand in the HF dataset card | close-out |

Definition of done per generator (checklist copied into each PR):
- [ ] class in `generators/`, registered in `quixi_math_datagen.py` import +
      `ALL_GENERATORS` + `curriculum.CURRICULUM`
- [ ] module-level `FOUNDATIONS = True` so the conventions test picks it up
- [ ] docstring lists variants and op-codes; new op-codes have one meaning
- [ ] 3–5 problem phrasings; oracle parses all of them
- [ ] test file mirrors the class name: contract, 500-sample oracle from
      problem text, step-arithmetic check, variants, invalid variant,
      pipe safety
- [ ] composite answer wherever the bare verdict is a coin flip
- [ ] `probe_generator_capacity.py --threshold 1000` passes or the small
      space is documented in the docstring
- [ ] seeded 200-example build: zero errors, duplicate rate noted

## 8. Out of scope, and why

No exact hand procedure ⇒ no generator: Russell's paradox and the motivation
for types (covered only through `TypeTheoryGenerator`'s ill-typed check),
Gödel's incompleteness theorems (only the numbering is procedural), the
independence of CH, the axiom of choice as a statement, informal "write a
proof that …" tasks with free-form answers, PM's descriptions (`ιx φx`)
beyond what `EnglishToLogic` can template, ordinals at or above ω^ω,
real numbers as Cauchy sequences (Dedekind cuts cover the construction with
exact arithmetic), and transfinite induction as an exercise.

## 9. Decisions taken in this plan (change here, not per generator)

- Unicode connectives for propositional/predicate logic; the circuit dialect
  `AND/OR/NOT` stays confined to `BooleanAlgebraGenerator`.
- Full parenthesization of non-outermost binary subformulas (canonical
  printing beats "minimal parentheses", which has no unique form).
- `card(A)` for cardinality, `:` in set-builder, `∣` or the word "divides",
  `↑` for NAND — all to keep the ASCII bar out of the strand entirely.
- `ℵ0` and `c` as cardinal symbols; `ω` for the first infinite ordinal.
- Proof-shaped tasks use one of the four determinism forms in §3; free-form
  proofs are not generated.
- `SetOperationsGenerator` is re-banded to middle; the catalog's band counts
  in README will change and should be regenerated, not hand-edited.

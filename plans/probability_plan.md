# Probability Curriculum Plan

Probability rebuilt from the ground up as *a measure on a finite set algebra*
— events are subsets, probabilities are additive weights on atoms,
independence is a product law, conditioning is renormalization — and carried
from elementary chance language through σ-algebras, martingales, and Markov
state classification, as procedural, hand-solvable, oracle-checkable
generators in the repo's scratchpad dialect.

Companion to `plans/foundations_plan.md` (logic, sets, relations, number) and
`plans/statistics_plan.md` (data, sampling distributions, inference). This strand
reuses the foundations set dialect for events and hands the sampling
distribution / CLT bridge to the statistics strand.

The bar is unchanged from `TODO.md` and `plans/foundations_plan.md`: exact
arithmetic only (`fractions.Fraction`), human-like steps, pipe-safe fields
(≤ 4 payload fields, no ASCII `|` anywhere), A0 answer conventions, an A9
oracle test that recomputes the answer from the problem text by an
independent route (here: brute-force enumeration of the sample space), > 1000
distinct problems per class, one class per skill registered in three places,
`PROBLEM_TYPES.md` / `OPCODES.md` regenerated.

## 1. What "foundational" means here

Kolmogorov's construction, and the order of this plan:

| Layer | Content | Plan strand |
|---|---|---|
| Ω, events as subsets | sample spaces by enumeration, events as rosters, likelihood language, relative frequency | P. Chance and sample spaces |
| P as a measure | weights on atoms, additivity on disjoint sets, complement, monotonicity, Venn regions and two-way tables as measures, inequalities (Boole, Markov, Chebyshev) | Q. Measure on the set algebra |
| P(· given B) as a renormalized measure; independence as a product law | trees, conditional tables, total probability, Bayes with priors, mutual independence | R. Conditioning and independence |
| Random variables = functions on Ω | pmf/cdf/quantiles, E[g(X)], variance algebra, covariance, indicators and linearity, conditional expectation and tower | S. Random variables and expectation |
| Named laws and approximations | uniform/Bernoulli, hypergeometric, negative binomial, multinomial, Poisson process, sums/convolution, normal approximation | T. Distributions and limit theorems |
| Processes and classics | random walks, gambler's ruin, multi-state Markov chains, Monte Carlo arithmetic, birthday/Monty Hall/coupon/matching/Buffon | U. Processes and classic problems |
| Measure-theoretic finish | finite σ-algebras and E[X given G], PGFs, reflection/ballot, Pólya urns, state classification, martingales | V. Graduate |

Everything below is finished by a deterministic pencil-and-paper procedure.
Topics needing transcendental values get them *supplied in the problem text*
(the `NormalTableGenerator` / `NamedDistributionGenerator` convention) or
are left symbolic (π); see §8.

## 2. Current coverage and gaps

Already in the registry (keep; extend where marked ⟲):

| Class | Band | Covers | Gap |
|---|---|---|---|
| `SimpleProbabilityGenerator` | elem d1 | "13 favorable of 15", one bare phrasing | no context, no event description, no percent/decimal form — the only elementary probability skill |
| `CompoundProbabilityIndependent/Dependent` | mid d4 | one path of two coins/dice/marbles/cards | no multi-path sums (trees), no "same colour / exactly one" |
| `GeometricProbabilityGenerator` | mid d4 | area/angle ratios | — |
| `ProbabilityAdditionRuleGenerator` | mid d4 | P(A ∪ B) | no other Venn regions |
| `BinomialProbabilityGenerator` | mid d4 | exact k / at most / at least one / mean / var | no normal approximation |
| `ConditionalProbabilityGenerator` | high **d5** | 2×2 fixed-context table; Bayes test pos/neg | over-banded; no P(A ∩ B)/P(B) from stated probabilities, no chain rule, no reverse conditioning |
| `ExpectedValueGenerator` | high d4 | E, Var by definition, winnings, fair game | no E[g(X)], no shortcut variance, no linearity |
| `GeometricDistributionGenerator` | high d4 | pmf, tails, mean | no memorylessness |
| `NormalTableGenerator` | high d4 | Φ table inline, below/above/between | no inverse lookup (quantile) |
| `ContinuousDistributionGenerator`, `NamedDistributionGenerator`, `JointDistributionGenerator` (binary 2×2), `MarkovChainGenerator` (two-state), `MGF`, `RVTransform`, `BayesianUpdate`, `OrderStatistics` | col/grad | as named | no 3+-state chains, no 3×3 joints, no PGF, no conditional expectation |
| Counting (`PermutationCombination`, `Pascal`, `InclusionExclusion`, `StarsAndBars`, `Derangement`, `CountingClassics`) | mid/col | counts | never converted to probabilities |

Missing entirely (all covered below): sample-space enumeration, spinner /
marble / deck narratives, complement and "at least one", likelihood
language, experimental vs theoretical probability, the fundamental counting
principle, odds, axioms on a finite space, Venn and two-way-table
probabilities, independence verification (pairwise vs mutual), total
probability, Bayes with 3+ hypotheses / stated priors / sequential updates,
discrete uniform / Bernoulli / indicators, pmf ↔ cdf and quantiles, E[g(X)]
and the variance shortcut, Var(aX + bY) and covariance algebra, linearity
of expectation with indicators, conditional expectation and the tower rule,
hypergeometric, negative binomial, multinomial, Poisson process arithmetic,
memorylessness, convolution / max / min of two variables, PGFs, Markov and
Chebyshev inequalities, LLN bounds, normal approximation with continuity
correction, random walks, gambler's ruin, hitting probabilities on 3+
states, state classification, martingale verification, Pólya urns,
ballot/reflection, birthday, Monty Hall, coupon collector, matching, Buffon,
LCG / inverse transform / hit-or-miss Monte Carlo, finite σ-algebras and
E[X given G].

Structural problems fixed by this plan: the elementary band has one
probability class and it has no context; nothing sits at difficulty 1–2 above
elementary; fifteen probability classes lack a `VARIANTS` attribute (the ⟲
work adds one wherever it touches a class).

## 3. Strand-wide rules (in addition to AGENTS.md)

**Notation (one dialect for problems, steps, and answers).**
- **Conditioning is written `P(A given B)`** — never a bar, never `∣`.
  Reason: `ConditionalProbabilityGenerator`, `JointDistributionGenerator`
  (`COND_FORMULA`) and their oracles already use and parse `given`, and the
  foundations strand reserves `∣` (U+2223) for divisibility; one symbol must
  not carry two meanings across strands. Problem phrasings may say "given
  that" in prose.
- Events are sets, in the foundations dialect: sample space `S`, rosters
  `{1, 2, 3, 4, 5, 6}`, event rosters `A = {2, 4, 6}`, `∪ ∩ − Δ`, complement
  `Aᶜ`, empty `∅`, `card(A)` (never `|A|`). Steps use `P(A ∩ B)`, `P(A ∪ B)`,
  `P(Aᶜ)`; prose phrasings may say "A and B", "A or B", "not A".
- Compound outcomes: coin/spinner/die products as compact strings in
  enumeration order (`H1, H2, H3, T1, T2, T3`; `HH, HT, TH, TT`); two numeric
  components as ordered pairs `(3, 4)`; draws as colour initials in order
  `RB`. **Enumeration order is fixed**: coins `H` before `T`; dice ascending;
  spinner sectors in the order printed; bag colours in the order the problem
  lists them; tree branches in the same order. Ties ("most likely outcome")
  break by enumeration order and the answer says so.
- Odds `3:5` (colon, lowest terms). Absolute deviations as `abs(X − μ)`.
  Weighted atoms as `P(a) = 1/10`. Two-way tables in prose as
  `<row>=<v> and <col>=<w>: n` (the `ConditionalProbability` table format).
- Composite verdicts join with `; ` and put the checkable fact after the
  label: `likely; 5/8`, `independent; P(A ∩ B) = 1/3 = P(A)·P(B)`,
  `switch; 2/3 vs 1/3`, `invalid; sum = 9/8`.
- These become a **"Probability answers"** block in DESIGN.md (§4).

**Answer form (canonical, extends A0).**
- Probabilities: **fraction in lowest terms** (`3/8`); `0` and `1` for
  impossible/certain; integers plain. `as_percent` / `as_decimal` variants
  state the form in the text and answer `37.5%` / `0.375` (totals chosen so
  the decimal terminates). Legacy classes keep their `exact()` behaviour;
  the shared `prob_common.exact()` remains available for ⟲ work.
- When a **supplied rounded constant** (Φ, e^−λ) enters, the problem says
  "to 4 decimal places" and the answer is a 4-decimal string (`0.2706`), as
  in `NormalTableGenerator`; arithmetic on the supplied value is exact
  decimal arithmetic (`Fraction("0.1353")`).
- Moments (E, Var, Cov) as lowest-terms fractions; money as `$3.50`.
- pmf/cdf tables: `P(S=0) = 1/8; P(S=1) = 3/8; …` / `F(1) = 1/8; …` in
  ascending support order. Vectors `π = (2/5, 2/5, 1/5)`. Functions on atoms
  `3/2 on {1, 2}; 3 on {3}; 5 on {4, 5, 6}`.
- π in a denominator: `2/(3π)` (A0 only covers π in numerators; add).
- PGF polynomials in `s`: descending powers, fractional coefficients
  parenthesized: `(1/4)s^2 + (1/2)s + 1/4`.

**Pipe safety is stricter here.** ASCII `|` is banned from problem text as
well as steps (the conditional bar, `|A|`, `|X − μ|`, and tally marks are the
usual leaks — tallies are written as counts or `H T T H` sequences). A
strand-level test enforces it (§4).

**Determinism.** Sample-space listings, tree branches, case tables, and
"first/smallest" answers follow the enumeration order above. Simulation
variants state the digit-assignment convention ("smallest digits represent
success"). Bayes and total-probability sums list hypotheses in the order
the problem states them.

**Tiny answer spaces.** `likely`, `independent`, `switch`, `valid`,
`martingale`, `fair` are coin flips; every such answer is composite with the
number that earns it. Constant-answer classics (expected matches = 1) are
composite with the computation (`5 × 1/5 = 1`) or are paired with a
non-constant quantity.

**Capacity.** Every class passes
`uv run python tools/probe_generator_capacity.py --threshold 1000`. Widen
by backward construction from exact answers (dyadic/decimal weights,
perfect-square variances and `npq`, perfect-square `n` for `σ/√n`), 4–8
narrative contexts (spinners, marble bags, numbered cards, dice, letter
tiles, lunch menus, factories, urns, weather, components, servers), and 3–5
phrasings per class. Known-small spaces are documented in the docstring.

**Oracles (A9).** The generator builds the experiment object and prints it;
the test parses the printed problem text with an independent parser and
solves by **brute-force enumeration** (`itertools.product/permutations/
combinations` over labelled objects, `Fraction` weights) or by an
independent closed form when the space is infinite (negative binomial
tails, ruin formulas, harmonic numbers). The two never share code. No sympy
is needed anywhere in this strand.

**Phrasing.** 3–5 templates per generator from day one, at least one
word-problem framing where natural.

## 4. Phase 0 — shared infrastructure

Built once, before any generator, each with its own tests. `prob_common.py`
is also the home of the numeric helpers the statistics strand imports
(`plans/statistics_plan.md` §4), so it lands before either strand's Phase 1.

- `prob_common.py` (repo root, beside `helpers.py`): `prob_txt(Fraction)`
  (lowest-terms / integer), `exact()` (moved here from its copies in
  `chi_square_generator.py` and `binomial_probability_generator.py`), `p4`,
  `pct`, `money` re-export, `odds_txt`; experiment objects (`Coin`, `Die(n)`,
  `Spinner(labels)`, `Bag(colour counts)`, `NumberedCards(n)`,
  `LetterTiles(word)`, `Menu(stages)`) each with a canonical outcome
  enumerator, a roster printer in §3 order, and a prose renderer per
  phrasing; event predicates (even, multiple of k, > k, vowel, colour,
  sum = k, doubles, at least one H …) with printable names; weighted-atom
  spaces; two-way-table builder/renderer; supplied-constant renderer
  (`Φ(1.50) = 0.9332`, `e^-2 = 0.1353`) with decoy rows — `phi_table(zs,
  decoys=2)` factored out of `NormalTableGenerator`, which is switched to
  call it with byte-identical output; `(n, p)` bank with perfect-square `npq`.
- `tests/probability_oracle.py`: independent parsers for every experiment
  phrasing, rosters, weighted atoms, two-way tables, joint pmf tables,
  transition rows, supplied constants; brute-force enumerators returning
  `Fraction`; Gaussian elimination over `Fraction` for first-step systems.
  Never imports `prob_common`.
- `tests/test_probability_conventions.py`: for every module with
  `PROBABILITY = True`, sample 200 examples and assert: no ASCII `|` in
  problem/steps/answer; every fraction in the answer is in lowest terms;
  every probability in the answer lies in [0, 1]; the word `given` (never a
  bar) precedes conditioning; rosters are in enumeration order and
  duplicate-free; composite answers parse for their declared kind. The
  ASCII-bar check is one helper shared with the foundations and statistics
  conventions tests.
- DESIGN.md: "Probability answers" block (§3); README coverage bullets.
- Op-code plan (reuse first): `PROB_SETUP|favorable|total`, `F`,
  `FRAC_BUILD`, `NCR`, `FACT`, `POW`, `TERM`, `SUM`, `COUNT`, `COUNT_SETUP`,
  `COMB_SETUP`, `MULTI_SETUP/MULTI_FORMULA`, `COND_FORMULA`,
  `INDEP_FORMULA/INDEP_CHECK` (joint, product, verdict), `EV_FORMULA`,
  `VAR_FORMULA/VAR_ROW`, `MARGINAL`, `JOINT_SETUP`, `MARKOV_SETUP`,
  `HIT_EQ/ABSORB_EQ/STEADY_EQUATION/LINEAR_SYSTEM`, `WALK_GOAL/WALK_TERM`
  (n-step via intermediate state), `CONV_WINDOW/CONV_SUM` (index, product
  terms / index, value), `TABLE_LOOKUP`, `LOOKUP_SUPPLIED`, `ZSCORE`,
  `BINOM_SETUP`, `GEOM_SETUP/GEOM_FORMULA`, `DIST_SETUP`, `IE_FORMULA`,
  `CHECK`, `TRY/REJECT/ACCEPT`, `REWRITE`, `SUBST`, `CMP`, `L/C`,
  `A/S/M/D/E/ROOT`. New codes (one meaning each): `SAMPLE_SPACE|experiment|
  roster|card`, `EVENT|name|roster|card`, `OUTCOME_CHECK|outcome|test|yes/no`,
  `LIKELIHOOD|p|word`, `COMPLEMENT|rule|work|value`, `TALLY|outcome|count`,
  `REL_FREQ|outcome|count/trials|value`, `FCP|stage|choices|running product`,
  `TREE_BRANCH|path|factors|product`, `BRANCH_SUM|paths|sum|value`,
  `WEIGHT|atom|p`, `AXIOM|name|statement`, `ODDS_FORMULA`, `ODDS|form|a:b`,
  `ODDS_REDUCE|a:b|c:d`, `VENN_REGION|region|value`, `TABLE_CELL|row,col|n`,
  `TABLE_TOTAL|line|work`, `DIGIT_MAP|event|digits`, `DIGIT_SCAN|block|
  reading|verdict`, `TOTAL_PROB_FORMULA`, `TOTAL_PROB_TERM|cause|factors|
  value`, `BAYES_TERM|hypothesis|prior × likelihood|value`, `POSTERIOR|
  hypothesis|term/total|value`, `HYPERGEO_SETUP/FORMULA`, `NEGBIN_SETUP/
  FORMULA`, `RELIABILITY|block|rule|value`, `UNIF_SETUP/UNIF_FORMULA`,
  `CDF_ROW|x|F(x)`, `QUANTILE|q|rule|x`, `G_ROW|x|g(x)|g(x)·p`, `CONT_CORR|
  discrete event|continuous event`, `MEASURE|set expr|roster|value`,
  `RENORMALIZE|atom|p/P(B)|value`, `INEQ_FORMULA|name|statement`,
  `INEQ_BOUND|event|bound`, `INDICATOR|I_k|P(I_k = 1)|value`, `LINEARITY|
  rule|sum|value`, `COV_RULE|rule|expression|value`, `COND_EXP|target|work|
  value`, `TOWER|rule|work|value`, `PP_SETUP`, `HARMONIC_NUMBER|H_n|sum|value`
  (not `HARMONIC_SETUP`, which belongs to harmonic functions), `LCG_STEP|n|
  work|x`, `INV_TRANSFORM|u|rule|x`, `HIT|point|test|in/out`, `RW_SETUP`,
  `RW_PATHS|constraint|solve|u, d`, `RUIN_FORMULA|case|formula`,
  `FIRST_STEP|state|equation`, `PGF_SETUP`, `PGF_TERM|x|term`,
  `PGF_DERIV|G'(s)|polynomial`, `SIGMA_GEN|generators|sets`, `ATOM|roster`,
  `COND_EXP_ATOM|atom|average|value`, `MARTINGALE_STEP|target|work|value`,
  `BALLOT_FORMULA`, `REFLECT|bad paths|mapped endpoint|count`, `POLYA_STEP|
  draw|p|urn after`, `REACH_PASS|k|rows`, `CLASS|roster|reason`, `CLASS_TYPE|
  class|reason|verdict`, `CHAIN_PERIOD|class|cycle lengths|d`. Regenerated into
  `OPCODES.md` at the end of each phase.

## 5. The curriculum

Format per entry: **Class** · band · difficulty — variants; problem (one
concrete example with its exact answer string); procedure (op-codes);
answer format; oracle; capacity/backward construction; supplied values.
`⟲` marks an existing class being extended.

### Strand P — Chance and sample spaces (elementary / middle)

**LikelihoodLanguageGenerator** · elementary · d1 — `classify`,
`compare_two_events`, `order_events`, `certain_impossible`. Problem: "A bag
holds 3 red, 4 blue and 1 green marble. One is drawn without looking. Is
drawing blue impossible, unlikely, an even chance, likely, or certain?"
Scale stated in the text: `0` impossible, `(0, 1/2)` unlikely, `1/2` even
chance, `(1/2, 1)` likely, `1` certain. Answer `even chance; 1/2`.
`compare_two_events` answers `red is more likely than green; 3/8 > 1/8`;
`order_events` answers `green, red, blue` (least to most likely; same
total, so counts compare directly); `certain_impossible` answers
`impossible; 0`. Steps: `COUNT|blue|4`, `SUM|3 + 4 + 1|8`, `PROB_SETUP|4|8`,
`F|4/8|1/2`, `LIKELIHOOD|1/2|even chance`, `CMP` for comparisons, `Z`.
Oracle: parse counts, recompute, re-classify. Capacity: unbounded (counts ×
contexts: bags, spinners). Supplied: none.

**⟲ SimpleProbabilityGenerator** — keep `bare`; add `spinner`, `bag`,
`numbered_cards` ("a multiple of 3 from cards 1–12"), `die` ("greater than
4"), `letter_tiles` ("a vowel from the tiles of PROBABILITY"),
`as_percent` (totals dividing 100 → `37.5%`), `as_decimal` (totals `2^a5^b`).
New steps `EVENT|A|{3, 6, 9, 12}|4` before `PROB_SETUP`. Existing tests
extended, not replaced.

**SampleSpaceListGenerator** · elementary · d2 — `list_and_count`,
`event_probability`, `two_coins`, `two_spinners`, `digit_cards`. Problem:
"A coin is flipped and a spinner with sectors 1, 2, 3 is spun. List every
outcome, count them, and find the probability of heads with an odd number."
Answer composite `H1, H2, H3, T1, T2, T3; 6 outcomes; 1/3`
(`list_and_count` stops at `…; 6 outcomes`). Steps: `SAMPLE_SPACE|coin ×
spinner|{H1, H2, H3, T1, T2, T3}|6`, `OUTCOME_CHECK|H1|heads and odd|yes`
(one per outcome), `EVENT|A|{H1, H3}|2`, `PROB_SETUP|2|6`, `F|2/6|1/3`, `Z`.
`digit_cards`: two-digit numbers from cards 2, 5, 7 without repeats
(6 outcomes; P(> 50)). Oracle: `itertools.product` over parsed components.
Capacity: component banks × labels × event predicates × phrasings.

**ComplementProbabilityGenerator** · elementary · d2 — `not_event`,
`missing_probability`, `at_least_one_two_stage`, `complement_of_described`.
Problem: "A spinner has 10 equal sectors numbered 1–10. What is the
probability it does not land on a multiple of 4?" Answer `4/5`. Steps:
`EVENT|A|{4, 8}|2`, `PROB_SETUP|2|10`, `F|2/10|1/5`, `COMPLEMENT|P(Aᶜ) = 1 −
P(A)|1 − 1/5|4/5`, `CHECK|P(A) + P(Aᶜ)|1/5 + 4/5|1`, `Z|4/5`.
`missing_probability`: "P(red) = 2/5, P(blue) = 1/4, find P(green)" →
`L/C` to 20ths, `S`, answer `7/20`. `at_least_one_two_stage`: two coins,
P(at least one head) = 1 − P(TT) = `3/4`. Oracle: count the complement
directly (8 of 10), or enumerate the product space. Capacity: unbounded.

**ExperimentalProbabilityGenerator** · elementary · d2 —
`relative_frequency`, `from_sequence`, `predict_count`,
`compare_theoretical`. Problem: "Mia spun a spinner 20 times: red 7, blue
9, green 4. What is the experimental probability of green?" Answer `1/5`.
Steps: `TALLY|green|4`, `SUM|7 + 9 + 4|20`, `REL_FREQ|green|4/20|1/5`, `Z`.
`from_sequence`: "H T T H H T H H T H" → count → `3/5`. `predict_count`:
4 equal sectors, 60 spins → `M|60|1/4|15` → `15`. `compare_theoretical`:
die rolled 30 times, 8 sixes → composite `experimental 4/15; theoretical
1/6; experimental is higher` (compare `8/30` vs `5/30` via `L/C/CMP`).
Oracle: parse tallies / re-scan the sequence. Capacity: unbounded.

**FundamentalCountingPrincipleGenerator** · elementary · d3 —
`count_only`, `count_then_probability`, `codes`, `tree_count`,
`with_restriction`. Problem: "A lunch has 3 sandwiches, 2 drinks (milk,
juice) and 4 fruits (apple, pear, grapes, plum). How many lunches are
possible? If one is chosen at random, what is the probability it has milk
and an apple?" Answer `24 lunches; 1/8`. Steps: `FCP|sandwich|3|3`,
`FCP|drink|2|6`, `FCP|fruit|4|24`, `EVENT|milk and apple|3 × 1 × 1|3`,
`PROB_SETUP|3|24`, `F|3/24|1/8`, `Z`. `codes`: 3-digit codes, no repeated
digit: `10 × 9 × 8 = 720`, P(no repeats) `= 18/25`. Oracle: product;
`itertools.product` for the probability. Capacity: unbounded.

**OddsProbabilityGenerator** · middle · d1 — `prob_to_odds_for`,
`prob_to_odds_against`, `odds_to_prob`, `from_counts`,
`odds_of_complement`. Problem: "The probability of rain tomorrow is 3/8.
What are the odds in favor of rain?" Answer `3:5`. Steps:
`ODDS_FORMULA|odds for A = P(A) : P(Aᶜ)`, `COMPLEMENT|P(Aᶜ) = 1 − P(A)|1 −
3/8|5/8`, `ODDS|for|3:5`, `Z|3:5`. `odds_to_prob`: odds 2:7 → `A|2|7|9`,
`PROB_SETUP|2|9` → `2/9`. `from_counts`: 4 red, 6 blue → `ODDS_REDUCE|4:6|
2:3`. Oracle: parse, recompute. Capacity: unbounded.

**ProbabilityAxiomsFiniteGenerator** · middle · d2 — `missing_weight`,
`event_sum`, `valid_assignment`, `complement_from_weights`,
`disjoint_union`. Problem: "A spinner's outcomes have P(1) = 1/4, P(2) =
3/8, P(3) = 1/8, P(4) = x. Find x, then P(odd)." Answer `x = 1/4; P(odd) =
3/8`. Steps: `WEIGHT|1|1/4` …, `AXIOM|total probability|Σ P(ω) = 1`,
`L/C/A` chain to `6/8`, `S|1|3/4|1/4`, `EVENT|odd|{1, 3}|2`,
`AXIOM|additivity|P(A) = Σ P(ω), ω ∈ A`, `A|1/4|1/8|3/8`, `Z`.
`valid_assignment`: composite `invalid; sum = 9/8` or `invalid; P(3) = −1/8
< 0` or `valid; sum = 1`. Oracle: parse weights, `Fraction` sums. This is
σ-additivity on a finite space, concretely. Capacity: dyadic/decimal
weights × 3–6 atoms × events × phrasings, > 1000.

**TreeDiagramProbabilityGenerator** · middle · d2 — `different_colors`,
`same_color`, `exactly_one`, `with_replacement`,
`three_coins_exactly_two_heads`, `spinner_then_coin`. Problem: "A bag has 2
red and 3 blue marbles. Two are drawn without replacement. Use a tree
diagram to find the probability the marbles are different colors." Answer
`3/5`. Steps: `TREE_BRANCH|R then B|2/5 × 3/4|6/20`, `TREE_BRANCH|B then
R|3/5 × 2/4|6/20`, `BRANCH_SUM|RB + BR|6/20 + 6/20|12/20`, `F|12/20|3/5`,
`CHECK|all branches|2/20 + 6/20 + 6/20 + 6/20|1`, `Z`. Distinct from
`CompoundProbability` (single path): this sums several paths. Oracle:
permutations of labelled marbles / `itertools.product` for coins.
Capacity: unbounded.

**RandomDigitSimulationGenerator** · middle · d2 — `estimate_from_digits`,
`assign_digits`, `two_digit_blocks`, `compare_to_theoretical`. Problem: "A
free throw succeeds with probability 3/10. Let digits 0–2 mean a make and
3–9 a miss; each block of 3 digits is one game of 3 shots. Using the random
digits 417 902 135 688 220, estimate the probability of at least 2 makes."
Answer `2/5`. Steps: `DIGIT_MAP|make|0–2 (3 of 10 digits)`,
`DIGIT_SCAN|417|makes 1|no`, `DIGIT_SCAN|902|makes 2|yes`, … ,
`COUNT|successful blocks|2`, `PROB_SETUP|2|5`, `Z`. `assign_digits`
answers composite `0–2 make, 3–9 miss; 2/5` (convention "smallest digits
represent success" stated). `compare_to_theoretical`: `estimate 2/5;
theoretical 27/125` (binomial terms via `TERM`). Oracle: re-scan the digit
string from the text. Capacity: unbounded (random digits).

**TwoWayTableProbabilityGenerator** · middle · d3 — `joint`, `marginal`,
`conditional_row`, `conditional_column`, `union`, `two_by_three`. Problem:
"50 students: sport=yes and pet=yes: 12; sport=yes and pet=no: 18;
sport=no and pet=yes: 8; sport=no and pet=no: 12. A student is chosen at
random. Find P(sport=yes and pet=yes) and P(pet=yes given sport=yes)."
Answer `6/25; 2/5`. Steps: `TABLE_CELL|sport=yes, pet=yes|12`,
`TABLE_TOTAL|grand|12 + 18 + 8 + 12 = 50`, `PROB_SETUP|12|50`, `F|12/50|6/25`,
`TABLE_TOTAL|sport=yes|12 + 18 = 30`, `COND_FORMULA|P(pet=yes given
sport=yes) = count(both)/count(sport=yes)`, `FRAC_BUILD|12/30|2/5`, `Z`.
`union`: (30 + 20 − 12)/50 → `19/25`. The middle-school on-ramp to
`ConditionalProbabilityGenerator` (which keeps the formal notation and
Bayes tests). The statistics framing of the same table (marginal and
conditional *percents*, association) is `TwoWayTableGenerator` in
`plans/statistics_plan.md`. Oracle: parse the generic `row=v and col=w: n` cells.
Capacity: 8 contexts × counts × variants × phrasings.

**VennProbabilityGenerator** · middle · d3 — `only_A`, `neither`, `union`,
`exactly_one`, `from_probabilities`, `three_set` (d4 override). Problem:
"Of 40 campers, 22 swim, 18 hike, and 9 do both. A camper is chosen at
random. Find P(swims but does not hike) and P(neither)." Answer `13/40;
9/40`. Built backward from region counts. Steps: `VENN_REGION|A ∩ B|9`,
`S|22|9|13`, `VENN_REGION|A only|13`, `S|18|9|9`, `VENN_REGION|B only|9`,
`A|13 + 9 + 9|31`, `S|40|31|9`, `VENN_REGION|neither|9`, `PROB_SETUP|13|40`,
`PROB_SETUP|9|40`, `Z`. `from_probabilities`: P(A) = 1/2, P(B) = 3/8,
P(A ∩ B) = 1/8 → P(A ∪ B) = `3/4`, P(Aᶜ ∩ Bᶜ) = `1/4`. Oracle: solve the
region system by subtraction; brute force on a synthetic labelled universe.
Capacity: unbounded; pairs with `VennRegionCountGenerator` (foundations).

**CountingToProbabilityGenerator** · middle · d4 — `first_letter`,
`no_repeats_code`, `friends_adjacent`, `specific_position`,
`ends_with_even`. Problem: "The letters of RANDOM are arranged in a random
order. What is the probability the arrangement begins with a vowel?"
Answer `1/3`. Steps: `COUNT_SETUP|arrangements of RANDOM|6!`, `FACT|6|720`,
`FCP|first letter|2 vowels|2`, `FACT|5|120`, `M|2|120|240`,
`PROB_SETUP|240|720`, `F|240/720|1/3`, `Z`. `friends_adjacent`: 5 in a row,
two particular people together: 2·4!/5! = `2/5`. `no_repeats_code`: 4-digit
PIN → 5040/10000 = `63/125`. Words have distinct letters (v1). Oracle:
`itertools.permutations` brute force (n ≤ 7). Capacity: word bank ×
properties × positions × phrasings, > 1000.

### Strand Q — Measure on the set algebra (high / college)

**ProbabilityMeasureGenerator** · college · d2 — `set_expression`,
`derive_identity`, `monotonicity`, `inclusion_exclusion_three`,
`union_bound_compare`, `renormalize`. Problem: "Ω = {a, b, c, d, e} with
P(a) = 1/10, P(b) = 1/5, P(c) = 3/10, P(d) = 1/4, P(e) = 3/20. A = {a, c},
B = {c, e}. Compute P((A ∪ B)ᶜ ∪ (A ∩ B))." Answer `3/4`. Steps:
`WEIGHT` rows, `SUBEXPR|A ∪ B|{a, c, e}`, `MEASURE|(A ∪ B)ᶜ|{b, d}|9/20`,
`MEASURE|A ∩ B|{c}|3/10`, `AXIOM|additivity (disjoint)|P(E ∪ F) = P(E) +
P(F)`, `L/C`, `A|9/20|6/20|15/20`, `F|15/20|3/4`, `Z`. `renormalize`: the
conditional measure P(· given B) on atoms → `RENORMALIZE|b|(1/5)/(13/20)|
4/13` … answer `b: 4/13; c: 6/13; e: 3/13; others 0` (conditioning as a
renormalized measure). `derive_identity`: `P(B − A) = P(B) − P(A ∩ B)` with
numbers, composite. `monotonicity`: `A ⊆ B; P(A) = 3/10 ≤ P(B) = 9/20`.
`union_bound_compare`: `P(A ∪ B) = 13/20 ≤ P(A) + P(B) = 17/20`. Oracle:
independent set-expression parser (shared with `tests/foundations_oracle.py`
when it lands) + `Fraction` sums. Capacity: unbounded.

**ProbabilityInequalityGenerator** · college · d3 — `markov`, `chebyshev`,
`chebyshev_within`, `chebyshev_find_k`, `boole_union_bound`,
`bonferroni_lower`, `lln_bound`, `lln_sample_size`, `compare_exact`.
Problem: "X ≥ 0 with E[X] = 3. Give Markov's upper bound for P(X ≥ 12)."
Answer `1/4`. Steps: `INEQ_FORMULA|Markov|P(X ≥ a) ≤ E[X]/a`, `D|3|12|1/4`,
`INEQ_BOUND|P(X ≥ 12)|≤ 1/4`, `Z|1/4`. `chebyshev`: μ = 50, σ² = 16, c = 10
→ `P(abs(X − 50) ≥ 10) ≤ 16/100` → `4/25` (σ² used directly; no roots).
`lln_bound`: σ² = 4, n = 100, ε = 1/2 → `4/(100 · 1/4)` → `4/25`;
`lln_sample_size`: smallest n with σ²/(nε²) ≤ δ. `compare_exact`: composite
`bound 1/4; exact 1/8` from a stated pmf. The law of large numbers is
delivered in this Chebyshev form only — exact fractions, no Φ. Oracle:
independent formula implementation; brute-force exact from the pmf.
Capacity: unbounded.

### Strand R — Conditioning and independence (high)

**ReliabilitySystemGenerator** · high · d2 — `series`, `parallel`, `both`,
`mixed`, `at_least_one_distinct`, `exactly_one`. Problem: "Three
independent components work with probabilities 9/10, 4/5 and 3/4. Find the
probability the system works if they are connected in series, and if in
parallel." Answer `series 27/50; parallel 199/200`. Steps:
`RELIABILITY|series|9/10 × 4/5 × 3/4|27/50` with the `M` chain,
`COMPLEMENT` per component, `RELIABILITY|parallel|1 − (1/10)(1/5)(1/4)|
199/200`, `Z`. Independence as a product law, applied. Oracle: enumerate
the 2³ component states with product weights. Capacity: unbounded.

**IndependenceCheckGenerator** · high · d3 — `die_events`,
`two_dice_events`, `small_deck`, `table_events`, `given_probabilities`,
`three_events_pairwise_vs_mutual`. Problem: "A fair die is rolled. A = the
roll is even, B = the roll is at most 4. Are A and B independent?" Answer
`independent; P(A ∩ B) = 1/3 = P(A)·P(B)`. Steps: `EVENT|A|{2, 4, 6}|3`,
`EVENT|B|{1, 2, 3, 4}|4`, `EVENT|A ∩ B|{2, 4}|2`, three `PROB_SETUP`/`F`,
`INDEP_FORMULA|independent iff P(A ∩ B) = P(A)·P(B)`, `M|1/2|2/3|1/3`,
`INDEP_CHECK|P(A ∩ B) = 1/3|product = 1/3|yes`, `Z`. `three_events`: two
coins, A = first H, B = second H, C = same face → `pairwise independent;
not mutually independent; P(A ∩ B ∩ C) = 1/4 ≠ 1/8`. Oracle: brute force.
Capacity: predicate bank on one die / two dice (sums, max, doubles,
parities) × phrasings, > 1000.

**LawOfTotalProbabilityGenerator** · high · d3 — `two_causes`,
`three_causes`, `urn_choice`, `two_stage_draw`, `weather`. Problem:
"Factory A makes 60% of the parts with a 2% defect rate; factory B makes
40% with a 5% defect rate. A part is chosen at random. What is the
probability it is defective?" Answer `4/125`. Steps:
`TOTAL_PROB_FORMULA|P(B) = Σ P(A_i)·P(B given A_i)`, `TOTAL_PROB_TERM|A|3/5 ×
1/50|3/250`, `TOTAL_PROB_TERM|B|2/5 × 1/20|1/50`, `L/C`, `A|3/250|5/250|
8/250`, `F|8/250|4/125`, `CHECK|partition|3/5 + 2/5|1`, `Z`. `two_stage_draw`:
P(second draw red) without replacement equals the first-draw probability
(the check step says so). Oracle: parse percents/fractions; sum.
Capacity: unbounded.

**BayesMultipleHypothesesGenerator** · high · d4 — `three_hypotheses`,
`four_hypotheses`, `all_posteriors`, `sequential_two_observations`,
`posterior_odds`, `coin_identification`. Problem: "Urn U1 has 2 red and 2
blue, U2 has 1 red and 3 blue, U3 has 3 red and 1 blue. An urn is chosen
with probabilities 1/2, 1/4, 1/4 and a ball is drawn; it is red. Find
P(U3 given red)." Answer `3/8`. Steps: `BAYES_TERM|U1|1/2 × 1/2|1/4`,
`BAYES_TERM|U2|1/4 × 1/4|1/16`, `BAYES_TERM|U3|1/4 × 3/4|3/16`, `L/C`,
`A` chain to `8/16`, `F|8/16|1/2`, `POSTERIOR|U3|(3/16)/(1/2)|3/8`,
`CHECK|posteriors sum|1/2 + 1/8 + 3/8|1`, `Z`. `all_posteriors` answers
`P(U1 given red) = 1/2; P(U2 given red) = 1/8; P(U3 given red) = 3/8`;
`sequential`: the posterior becomes the prior for the second draw (work
shown twice); `posterior_odds`: `3:1`. Oracle: parse urns and priors;
recompute; sequential variant re-enumerated as a single joint experiment
(independent route). Capacity: unbounded.

**⟲ ConditionalProbabilityGenerator** — re-band `high d5 → high d3`; add
`given_probabilities` (P(A ∩ B)/P(B) from stated fractions), `chain_rule`
(three draws without replacement: P(A)·P(B given A)·P(C given A ∩ B)),
`reverse_conditioning` (P(B given A) from P(A given B), P(A), P(B)); widen
the table variant to 6 contexts. Existing tests extended.

### Strand S — Random variables and expectation (high / college)

**DiscreteUniformBernoulliGenerator** · high · d2 — `uniform_interval_prob`,
`uniform_moments`, `uniform_shift`, `bernoulli_moments`, `indicator`.
Problem: "X is uniform on the integers 1 through 8. Find P(X ≤ 3), E[X]
and Var(X)." Answer `P(X ≤ 3) = 3/8; E[X] = 9/2; Var(X) = 21/4`. Steps:
`UNIF_SETUP|X uniform on {1, …, 8}|n = 8`, `PROB_SETUP|3|8`,
`UNIF_FORMULA|E[X] = (a + b)/2, Var(X) = (n² − 1)/12`, `A|1|8|9`, `D|9|2|9/2`,
`E|8|2|64`, `S|64|1|63`, `D|63|12|21/4`, `CHECK|definition|Σ (x − 9/2)²/8|
21/4`, `Z`. `bernoulli_moments`: p = 2/5 → `E[X] = 2/5; Var(X) = 6/25`;
`indicator`: I = 1 if a die shows ≥ 5 → `E[I] = 1/3`. Oracle: definitional
sums. Capacity: a ∈ 0..20, n ∈ 3..20, p bank, variants, phrasings > 1000.

**PmfCdfQuantileGenerator** · high · d3 — `pmf_to_cdf`, `cdf_to_pmf`,
`interval_from_cdf`, `median`, `quantile`, `mode`. Problem: "X has pmf
P(X=1) = 1/8, P(X=2) = 3/8, P(X=3) = 1/4, P(X=4) = 1/4. Build the cdf and
find the median (smallest x with F(x) ≥ 1/2)." Answer `F(1) = 1/8; F(2) =
1/2; F(3) = 3/4; F(4) = 1; median 2`. Steps: `CDF_ROW|1|1/8`, `A|1/8|3/8|
4/8`, `F|4/8|1/2`, `CDF_ROW|2|1/2`, …, `QUANTILE|1/2|first x with F(x) ≥
1/2|2`, `Z`. `interval_from_cdf`: `P(1 < X ≤ 3) = F(3) − F(1)` → `5/8`.
Oracle: parse pmf, cumulate. Capacity: unbounded (dyadic weights).

**ExpectationOfFunctionGenerator** · high · d3 — `e_g_x`, `var_shortcut`,
`linear_mean_var`, `standardize`, `compare_routes`. Problem: "X takes the
values −1, 0, 2 with probabilities 1/4, 1/4, 1/2. Find E[X²] and Var(X)
using Var(X) = E[X²] − (E[X])²." Answer `E[X²] = 9/4; Var(X) = 27/16`.
Steps: `EV_FORMULA|E[X] = Σ x·P(x)`, `M`/`A` to `3/4`, `G_ROW|x=−1|g = 1|1 ×
1/4 = 1/4`, `G_ROW|x=0|g = 0|0`, `G_ROW|x=2|g = 4|4 × 1/2 = 2`, `SUM|1/4 + 0
+ 2|9/4`, `VAR_FORMULA|Var(X) = E[X²] − (E[X])²`, `E|3/4|2|9/16`,
`S|9/4|9/16|27/16`, `CHECK|definition route|Σ P(x)(x − μ)²|27/16`, `Z`.
`linear_mean_var`: Y = 3X − 2 → `E[Y] = 1/4; Var(Y) = 243/16`;
`standardize` uses perfect-square variances (built backward). g ∈ {x²,
ax + b, abs(x − c), 1/x on nonzero support}. Oracle: definitional sums.
Capacity: unbounded.

**LinearityOfExpectationGenerator** · college · d3 — `fixed_points`,
`distinct_values`, `empty_bins`, `heads_different_coins`, `sum_dice`,
`adjacent_same_color`, `birthday_pairs`. Problem: "Three fair six-sided
dice are rolled. What is the expected number of distinct values showing?"
Answer `91/36`. Steps: `INDICATOR|I_v = 1 if value v appears|P(I_v = 1) = 1
− (5/6)³|91/216`, `POW|(5/6)^3|125/216`, `S|1|125/216|91/216`,
`LINEARITY|E[X] = Σ E[I_v]|6 × 91/216|91/36`, `Z`. `fixed_points` answers
composite `5 × 1/5 = 1` (constant-answer guard). `empty_bins`: 3 balls in 4
bins → `27/16`. Oracle: brute force (permutations n ≤ 6; product spaces
≤ 6⁴). Capacity: parameter ranges × variants × phrasings, > 1000.

**CovarianceAlgebraGenerator** · college · d3 — `var_linear_combo`,
`var_sum_independent`, `cov_bilinear`, `corr_from_cov`,
`cov_from_table_3x3`, `var_difference`, `cov_with_sum`. Problem: "Var(X) =
4, Var(Y) = 9, Cov(X, Y) = −2. Find Var(2X − 3Y)." Answer `121`. Steps:
`COV_RULE|Var(aX + bY)|a²Var(X) + b²Var(Y) + 2ab·Cov(X, Y)`, `E|2|2|4`,
`M|4|4|16`, `E|3|2|9`, `M|9|9|81`, `M|2·2·(−3)|−2|24`, `A` chain, `Z`.
`corr_from_cov` uses perfect-square variances → `−1/3`.
`cov_from_table_3x3` extends `JointDistribution` (binary) to supports
{0, 1, 2}²: `E[XY] − E[X]E[Y]` with brute-force oracle. Capacity: unbounded.

**ConditionalExpectationGenerator** · college · d4 — `from_table`,
`tower_check`, `two_stage_experiment`, `conditional_variance`,
`random_sum_mean`, `random_sum_variance`, `total_variance_check`. Problem:
"(X, Y) has joint pmf P(0,0) = 1/4, P(1,0) = 1/4, P(0,1) = 1/8, P(1,1) =
3/8. Find E[X given Y=0], E[X given Y=1], and verify E[E[X given Y]] =
E[X]." Answer `E[X given Y=0] = 1/2; E[X given Y=1] = 3/4; E[X] = 5/8`.
Steps: `MARGINAL|P(Y=1) = 1/8 + 3/8|1/2`, `COND_FORMULA`, `COND_EXP|E[X
given Y=1]|0·(1/8)/(1/2) + 1·(3/8)/(1/2)|3/4`, `COND_EXP|E[X given Y=0]|…|
1/2`, `TOWER|E[X] = Σ P(Y=y)·E[X given Y=y]|1/2·1/2 + 1/2·3/4|5/8`,
`CHECK|direct E[X]|1/4 + 3/8|5/8`, `Z`. `two_stage_experiment`: "roll a
die, then flip that many coins" → `E[heads] = 7/4`; `random_sum_variance`:
`Var(S) = E[N]Var(X) + Var(N)(E[X])²`. Oracle: brute force from the parsed
joint table / product space. Capacity: unbounded.

### Strand T — Distributions and limit theorems (high / college)

**HypergeometricGenerator** · high · d4 — `exact_k`, `at_least_one`,
`at_most`, `mean`, `variance`, `three_types`. Problem: "A box has 5 good and
3 defective bulbs. Four are drawn without replacement. Find P(exactly 2
defective)." Answer `3/7`. Steps: `HYPERGEO_SETUP|N = 8, K = 3, n = 4|P(X =
2)`, `HYPERGEO_FORMULA|P(X = k) = C(K, k)·C(N − K, n − k)/C(N, n)`,
`NCR|C(3, 2)|3`, `NCR|C(5, 2)|10`, `M|3|10|30`, `NCR|C(8, 4)|70`,
`FRAC_BUILD|30/70|3/7`, `Z`. `at_least_one` → `13/14`; `mean` `= 3/2`;
`variance` `= 15/28`. This is where the counting generators finally become
probabilities. Oracle: brute-force `itertools.combinations` over labelled
items (N ≤ 12). Capacity: N ≤ 12 × K × n × contexts × phrasings.

**NegativeBinomialGenerator** · college · d3 — `exact_trial`, `mean`,
`variance`, `at_most_trials`, `failures_form`, `geometric_special_case`.
Problem: "Each trial succeeds with probability 1/3. Find the probability
that the 2nd success occurs on trial 5." Answer `32/243`. Steps:
`NEGBIN_SETUP|r = 2, p = 1/3|P(N = 5)`, `NEGBIN_FORMULA|P(N = n) = C(n − 1,
r − 1)·p^r·(1 − p)^(n − r)`, `NCR|C(4, 1)|4`, `POW|(1/3)^2|1/9`,
`POW|(2/3)^3|8/27`, `M|4|1/9|4/9`, `M|4/9|8/27|32/243`, `Z`. `mean` `r/p =
6`; `variance` `r(1 − p)/p² = 12`. Oracle: brute force over ±sequences of
length n (n ≤ 10) with product weights. Capacity: r ≤ 4, n ≤ 12, p bank.

**MultinomialProbabilityGenerator** · college · d3 — `exact_counts`,
`marginal_is_binomial`, `mean_cov`, `sequence_vs_counts`,
`bag_with_replacement`. Problem: "A fair die is rolled 5 times. Find the
probability of exactly two 6s, one 1, and two other values." Answer `5/81`.
Steps: `MULTI_SETUP|two 6s, one 1, two others|total 5`,
`MULTI_FORMULA|n!/(a!b!c!)|5!/(2!1!2!)`, `FACT|5|120`, `D|120|4|30`,
`POW|(1/6)^2|1/36`, `POW|(1/6)^1|1/6`, `POW|(2/3)^2|4/9`, `M` chain to
`1/486`, `M|30|1/486|5/81`, `Z`. `mean_cov`: `Cov(X_6, X_1) = −5/36`.
Oracle: brute force over 6ⁿ sequences (n ≤ 6). Capacity: n ≤ 6 × category
splits × p banks × contexts.

**DistributionOfSumGenerator** · college · d3 — `convolution_pmf`,
`single_value`, `weighted_dice_sum`, `max_of_two`, `min_of_two`,
`sum_binomial_rule`, `sum_poisson_rule`. Problem: "X and Y are independent;
P(X=0) = 1/2, P(X=1) = 1/2; P(Y=0) = 1/4, P(Y=1) = 1/2, P(Y=2) = 1/4. Find
the pmf of S = X + Y." Answer `P(S=0) = 1/8; P(S=1) = 3/8; P(S=2) = 3/8;
P(S=3) = 1/8`. Steps: `CONV_WINDOW|s=1|1/2·1/2 + 1/2·1/4`, `CONV_SUM|s=1|
3/8` (reusing the convolution generator's codes with the same field
meaning), …, `CHECK|Σ P(S = s)|1/8 + 3/8 + 3/8 + 1/8|1`, `Z`. `max_of_two`:
`P(max ≤ k) = F_X(k)·F_Y(k)` then differences. `sum_binomial_rule` answers
composite `Binomial(5, 1/3); P(S = 2) = 80/243`. Oracle: `itertools.product`
brute force. Capacity: unbounded.

**PoissonProcessGenerator** · college · d3 — `count_in_interval`,
`no_event_interval`, `interarrival_within`, `time_to_second`,
`thinning_rate`, `superposition_rate`, `which_type_first`,
`mean_variance`. Problem: "Calls arrive as a Poisson process at 3 per hour.
Using the supplied value e^-2 = 0.1353, find the probability of exactly 2
calls in 40 minutes, to 4 decimal places." Answer `0.2706`. Steps:
`PP_SETUP|rate 3 per hour, t = 40 min|N(t) ~ Poisson(λt)`, `M|3|2/3|2`,
`LOOKUP_SUPPLIED|e^-2|0.1353`, `POW|2^2|4`, `FACT|2|2`, `M|0.1353|4|0.5412`,
`D|0.5412|2|0.2706`, `Z`. Exact-only variants: `thinning_rate` (rate of
type-A calls = pλ, mean count pλt), `superposition_rate` (λ₁ + λ₂),
`which_type_first` (`λ₁/(λ₁ + λ₂)` as a fraction), `mean_variance`.
Supplied: `e^-λt` to 4 decimals (λt rational, printed as `e^-2` or
`e^(-3/2)`). Oracle: parse rate, t, supplied value; recompute with
`Fraction("0.1353")`. Capacity: rates × times × k × variants × phrasings.

**⟲ GeometricDistributionGenerator** — add `memoryless_verify` (composite
`P(X > 5 given X > 2) = 27/64 = P(X > 3)`), `conditional_tail`,
`remaining_wait` (E[X − m given X > m] = 1/p). **⟲ NamedDistributionGenerator**
— add `exponential_memoryless` (two supplied `e^-` values, composite
equality) and `poisson_mode`; align supplied-constant phrasing with the
strand renderer (4-decimal form) while keeping the fraction form parseable.

**NormalApproxBinomialGenerator** · high · d4 — `at_most`, `at_least`,
`exactly`, `between`, `check_conditions`, `mean_sd`. Problem: "A fair coin
is tossed 100 times. Using the normal approximation with continuity
correction and the table Φ(1.00) = 0.8413; Φ(1.10) = 0.8643; Φ(1.20) =
0.8849, estimate P(X ≤ 55) to 4 decimal places." Answer `0.8643`. Steps:
`BINOM_SETUP|n = 100, p = 1/2|P(X ≤ 55)`, `CHECK|np ≥ 10 and n(1 − p) ≥ 10|
50, 50|ok`, `M|100|1/2|50`, `M|50|1/2|25`, `ROOT|25|5`, `CONT_CORR|P(X ≤
55)|P(Y ≤ 55.5)`, `ZSCORE|(55.5 − 50)/5|1.10`, `TABLE_LOOKUP|Φ(1.10)|0.8643`,
`Z`. Backward construction: `(n, p)` from the bank with `npq` a perfect
square whose root σ ∈ {2, 5, 10, 20} so that every half-integer offset gives
a 2-decimal z: (16, 1/2), (18, 1/3), (18, 2/3), (100, 1/2), (180, 1/6),
(180, 5/6), (400, 1/2), (450, 1/3), (450, 2/3), (625, 1/5), (625, 4/5),
(720, 1/6), (720, 5/6), (1600, 1/2). `check_conditions` answers composite
`ok; np = 50 ≥ 10, n(1 − p) = 50 ≥ 10` or `fails; n(1 − p) = 6 < 10`;
`mean_sd` answers `mean 50; sd 5`. Oracle: parse n, p, k and the table;
recompute z with `Fraction` and read the parsed table; sanity-assert the
exact binomial (`math.comb`) is within 0.02. Capacity: 14 pairs × ~30 k × 6
variants × decoy tables × 4 phrasings, > 1000. This is the single normal-
approximation class for both strands; `plans/statistics_plan.md` cross-references
it.

**⟲ NormalTableGenerator** — add `inverse_lookup` (given P(X < x) =
0.9332 and the table, find x = μ + 1.50σ; σ even so x is exact) and
`symmetric_interval` (P(μ − a < X < μ + a) = 2Φ(z) − 1). The percentile-
table form of the inverse problem is `InverseNormalGenerator` in
`plans/statistics_plan.md`; both stay (different supplied-table shapes).

The sampling distribution of x̄ and p̂, standard error, and CLT probabilities
are **owned by `plans/statistics_plan.md`** (`SamplingDistributionEnumGenerator`
for exact enumeration, `CLTProbabilityGenerator` for the Φ-based
approximation); they depend on this strand's Phase 0 renderer and land in
the statistics Phase 3.

### Strand U — Processes and classic problems (high / college)

**ClassicProbabilityPuzzlesGenerator** · high · d4 — `monty_hall`,
`monty_hall_n_doors`, `birthday`, `birthday_specific_person`,
`birthday_expected_pairs`, `two_child`, `bertrand_box`. Problem: "Four
people each have a birthday month chosen uniformly from 12. What is the
probability at least two share a month?" Answer `41/96`. Steps:
`COMPLEMENT|P(shared) = 1 − P(all different)`, `FCP|person 1|12|12`,
`FCP|person 2|11|132`, `FCP|person 3|10|1320`, `FCP|person 4|9|11880`,
`POW|12^4|20736`, `FRAC_BUILD|11880/20736|55/96`, `S|1|55/96|41/96`, `Z`.
`monty_hall` (n doors, host opens k losing doors, uniform host tie-break)
enumerates `CASE|car behind 1, pick 1|stay wins`… answer `switch; 2/3 vs
1/3` (n = 4, k = 1: `switch; 3/8 vs 1/4`). `two_child`: "at least one boy"
→ `1/3; sample space {BB, BG, GB}`; "older is a boy" → `1/2`.
`bertrand_box`: `2/3` by enumerating the six coins. Exactness: birthday
uses d ∈ {7, 10, 12, 20, 24, 30, 52, 60, 100} with n ≤ 6 (n ≤ 4 for
d ≥ 30), and d = 365 only for n ≤ 3 (`1093/133225` is still hand-sized).
Oracle: birthday by an independent product; Monty by brute force over
car × pick × host choice. Capacity: ~40 birthday settings + 21 Monty
settings + puzzle families, × 4 phrasings plus the two extra birthday
variants; probe and widen with `birthday_expected_pairs` (C(n, 2)/d) if
short.

**ExpectedValueClassicsGenerator** · college · d4 — `coupon_collector`,
`coupon_next`, `coupon_first_k`, `coupon_all_in_n`, `matching_at_least_one`,
`matching_exactly_k`, `buffon_probability`, `buffon_pi_estimate`,
`st_petersburg_truncated`. Problem: "A cereal box holds one of 6 equally
likely toys. What is the expected number of boxes to collect all 6?"
Answer `147/10`. Steps: `LINEARITY|E[T] = Σ n/(n − i)|6/6 + 6/5 + 6/4 + 6/3 +
6/2 + 6/1`, `HARMONIC_NUMBER|H_6|1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6|49/20` (with
`L/C/A`), `M|6|49/20|147/10`, `Z`. `matching_at_least_one` (n = 4):
`IE_FORMULA`, alternating sum → `5/8`; `matching_exactly_k` (n = 4, k = 1)
→ `1/3`. `buffon_probability` L = 1, d = 3 → `2/(3π)` (π symbolic);
`buffon_pi_estimate` L = d, 100 drops, 64 crossings → `π ≈ 2n/hits` →
`25/8`. `coupon_all_in_n`: n!/nⁿ → `3/32` for n = 4. Oracle: harmonic
sums independently; brute-force permutations for matching (n ≤ 6);
formula for Buffon. Capacity: n ≤ 8 coupons, n ≤ 7 matching, (L, d) pairs,
drop counts; widen with `coupon_first_k`; documented if the probe is short.

**MonteCarloArithmeticGenerator** · college · d3 — `lcg_sequence`,
`lcg_period`, `inverse_transform_discrete`, `inverse_transform_linear`,
`hit_or_miss_pi`, `estimate_from_samples`. Problem: "An LCG uses x_{n+1} =
(5·x_n + 3) mod 16 with x_0 = 7. Compute x_1 … x_4 and the uniforms u_i =
x_i/16." Answer `6, 1, 8, 11; u = 3/8, 1/16, 1/2, 11/16`. Steps:
`LCG_STEP|1|(5·7 + 3) mod 16|6`, …, `D|6|16|3/8`, …, `Z`. `lcg_period`:
iterate until a repeat (m ≤ 16) → `period 4; cycle 7, 6, 1, 8`.
`inverse_transform_discrete`: u = 0.63 against a cdf table →
`INV_TRANSFORM|0.63|F(2) = 1/2 < 0.63 ≤ F(3) = 3/4|3`. `inverse_transform_
linear`: F(x) = x²/9 → x = 3√u with u a perfect-square fraction. `hit_or_
miss_pi`: rational points, `HIT|(3/5, 4/5)|9/25 + 16/25 ≤ 1|in`, estimate
`4·hits/n`. ln-based exponential sampling is deliberately excluded (would
need supplied ln values). Oracle: independent integer/`Fraction` code.
Capacity: unbounded.

**RandomWalkGenerator** · college · d4 — `position_prob`, `biased_position`,
`return_to_origin`, `mean_var`, `ruin_fair`, `ruin_biased`, `duration_fair`.
Problem: "A simple symmetric random walk starts at 0. Find P(S_6 = 2)."
Answer `15/64`. Steps: `RW_SETUP|p = 1/2, n = 6|P(S_6 = 2)`, `RW_PATHS|u − d
= 2, u + d = 6|solve|u = 4, d = 2`, `NCR|C(6, 4)|15`, `POW|(1/2)^6|1/64`,
`M|15|1/64|15/64`, `Z`. `return_to_origin` n = 3 → `5/16`; `ruin_fair`
`RUIN_FORMULA|fair|P_i = i/N` → `1/2`; `ruin_biased` p = 2/3, i = 2, N = 4:
`RUIN_FORMULA|biased|(1 − r^i)/(1 − r^N), r = q/p` → `4/5`;
`duration_fair` `i(N − i)` → `4`. Oracle: brute force over 2ⁿ paths
(n ≤ 12); ruin by `Fraction` Gaussian elimination on the first-step system.
Capacity: n, k, p, i, N ranges × phrasings.

**MultiStateMarkovGenerator** · college · d4 — `two_step`,
`path_probability`, `hitting_prob_3state`, `expected_hitting_time`,
`stationary_3state`, `distribution_after_one_step`. Problem: "A chain on
{1, 2, 3} has rows P1 = (1/2, 1/4, 1/4), P2 = (0, 1/2, 1/2), P3 = (1/3, 1/3,
1/3). Find P(X_2 = 3 given X_0 = 1)." Answer `1/3`. Steps:
`MARKOV_SETUP|three_state|rows`, `WALK_GOAL|2 steps|1 to 3`, `WALK_TERM|via
1|1/2 × 1/4|1/8`, `WALK_TERM|via 2|1/4 × 1/2|1/8`, `WALK_TERM|via 3|1/4 ×
1/3|1/12`, `L/C`, `A` chain, `F|8/24|1/3`, `Z`. `hitting_prob_3state`:
`FIRST_STEP|h_1 = 1/2·h_1 + 1/4·h_2 + 1/4·1` … solved with
`LINEAR_SYSTEM`/`REWRITE`/`D`. `stationary_3state` is built backward from a
chosen π with small denominators (detailed-balance construction) and
answers `π = (2/5, 2/5, 1/5)`. Oracle: `Fraction` matrix power; independent
Gaussian elimination. Capacity: unbounded.

### Strand V — Graduate

**FiniteSigmaAlgebraGenerator** · graduate · d3 — `generated_sigma_algebra`,
`measurability_check`, `sigma_of_random_variable`,
`conditional_expectation_atoms`, `conditional_probability_given_G`.
Problem: "Ω = {1, …, 6} with the uniform measure. Let G = σ({1, 2}, {3}).
List the atoms of G, count its events, and compute E[X given G] for X(ω) =
ω." Answer `atoms {1, 2}, {3}, {4, 5, 6}; 8 events; 3/2 on {1, 2}; 3 on {3};
5 on {4, 5, 6}`. Steps: `SIGMA_GEN|generators|{1, 2}, {3}`, `ATOM|{1, 2}`,
`ATOM|{3}`, `ATOM|{4, 5, 6}` (complement of the union), `COUNT|events|2^3 =
8`, `COND_EXP_ATOM|{1, 2}|(1 + 2)/2|3/2`, …, `CHECK|E[E[X given G]]|(2·3/2 +
1·3 + 3·5)/6|7/2 = E[X]`, `Z`. `measurability_check`: `not G-measurable; A
splits the atom {4, 5, 6}`. Oracle: brute-force closure of the generators
under complement and union (frozensets); averages on atoms with weights.
Ties directly to the foundations set algebra and
`HereditarilyFiniteSetGenerator`. Capacity: unbounded.

**PGFGenerator** · graduate · d3 — `build`, `extract_pmf`, `mean_from_pgf`,
`variance_from_pgf`, `sum_independent_product`, `binomial_pgf`,
`prob_even`. Problem: "X has pmf P(0) = 1/4, P(1) = 1/2, P(2) = 1/4. Write
G_X(s), then find E[X] = G'(1) and Var(X) = G''(1) + G'(1) − G'(1)²."
Answer `G(s) = (1/4)s^2 + (1/2)s + 1/4; E[X] = 1; Var(X) = 1/2`. Steps:
`PGF_SETUP|G(s) = Σ P(X = k)·s^k`, `PGF_TERM|k=2|(1/4)s^2`, …,
`PGF_DERIV|G'(s)|(1/2)s + 1/2`, `SUBST|s|1|1`, `PGF_DERIV|G''(s)|1/2`, `A`,
`S`, `Z`. `prob_even`: `(G(1) + G(−1))/2`. `sum_independent_product`:
multiply two small polynomials and read the pmf of the sum. Oracle:
independent dict-polynomial arithmetic and definitional E/Var. Capacity:
unbounded.

**BallotReflectionGenerator** · graduate · d4 — `ballot_probability`,
`paths_touching_level`, `first_return`, `max_at_least`, `stay_nonnegative`,
`dyck_probability`. Problem: "Candidate A receives 5 votes and B receives
2. If the ballots are counted in random order, what is the probability A
is strictly ahead throughout?" Answer `3/7`. Steps: `BALLOT_FORMULA|(a −
b)/(a + b)`, `S|5|2|3`, `A|5|2|7`, `FRAC_BUILD|3/7|3/7`, `Z`.
`paths_touching_level` (n = 6, end 2, touch −1): `REFLECT|paths hitting −1
ending at 2|paths ending at −4|C(6, 1) = 6`, `PROB_SETUP|6|64` → `3/32`.
`first_return` at time 4 → `1/8`. Oracle: brute force over ballot
orderings (`C(a + b, b) ≤ 3000`) and ±1 paths (n ≤ 14). Capacity: a, b ≤ 12,
n ≤ 14 × k × variants × phrasings, > 1000.

**PolyaUrnGenerator** · graduate · d4 — `sequence_probability`,
`exchangeability_check`, `kth_draw_marginal`, `count_after_n`,
`expected_red_fraction`, `reinforcement_c`. Problem: "An urn has 2 red and
1 blue ball. A ball is drawn and returned together with one more ball of
the same colour. Find P(R, B, R) and show it equals P(B, R, R)." Answer
`P(R, B, R) = 1/10; P(B, R, R) = 1/10; equal (exchangeable)`. Steps:
`POLYA_STEP|draw 1: R|2/3|3R 1B`, `POLYA_STEP|draw 2: B|1/4|3R 2B`,
`POLYA_STEP|draw 3: R|3/5|4R 2B`, `M` chain to `1/10`, `CHECK|
exchangeability|1/3 × 2/4 × 3/5|1/10`, `Z`. `kth_draw_marginal`: P(third
draw red) = initial proportion `2/3` via total probability. Oracle:
recursion over urn states with `Fraction`. Capacity: unbounded.

**MarkovStateClassificationGenerator** · graduate · d4 —
`communicating_classes`, `transient_recurrent`, `period`,
`absorbing_states`, `irreducible_check`, `reachability_matrix`. Problem:
"A chain on {1, …, 5} has positive transitions 1→2, 2→1, 2→3, 3→4, 4→5,
5→3. Give the communicating classes, say which are transient or recurrent,
and give each class's period." Answer `classes {1, 2}, {3, 4, 5}; transient
{1, 2}; recurrent {3, 4, 5}; periods 2, 3`. Steps: `REACH_PASS|k=1|rows`
(Warshall-style reachability snapshots, the same machinery as the
foundations `RelationClosureGenerator`), `CLASS|{1, 2}|1 ↔ 2`,
`CLASS_TYPE|{1, 2}|2 → 3 leaves the class|transient`, `CHAIN_PERIOD|{3, 4, 5}|
cycle lengths {3}|3`, `Z`. Oracle: BFS reachability; period as gcd of
return times from powers of the 0/1 matrix (n ≤ 6). Capacity: random
sparse digraphs on 4–6 states, unbounded.

**MartingaleCheckGenerator** · graduate · d4 — `drift_corrected`,
`quadratic`, `exponential`, `not_martingale`, `optional_stopping_ruin`,
`doob_product`. Problem: "S_n is a random walk with up-step probability
2/3. Is M_n = S_n − n/3 a martingale? Evaluate E[M_5 given S_4 = 2] and
compare with M_4." Answer `martingale; E[M_5 given S_4 = 2] = 2/3 = M_4`.
Steps: `MARTINGALE_STEP|E[S_5 given S_4 = 2]|2 + (2/3)(1) + (1/3)(−1)|7/3`,
`S|7/3|5/3|2/3`, `CHECK|M_4|2 − 4/3|2/3`, `Z`. `not_martingale`: S_n itself
with p ≠ 1/2 → `submartingale; 7/3 > 2`. `optional_stopping_ruin`: use
`(q/p)^{S_n}` to derive the ruin probability (same number as
`RandomWalkGenerator.ruin_biased`, different route — the two oracles
cross-check each other). Oracle: one-step enumeration with `Fraction`.
Capacity: p bank × states × n × variants × phrasings, > 1000.

### Critic records for the strand

**ProbabilityCriticGenerator** · college · d4 — `tree_error` (one branch
product wrong, propagated into the sum), `bayes_error` (one `BAYES_TERM`
wrong), `complement_forgotten` (the `1 −` step missing), `missing_step`
(one line blanked). Same record shapes as `ErrorSpottingGenerator` /
`FillInStepGenerator`: `VERIFY|k|ok`, `FLAG|k|<true value>`, redo, `Z|step
k; <correct answer>`. Built on the strand's own generators. Oracle:
recompute the correct value from the problem text.

## 6. Band and difficulty summary

| Band | New classes | Extended |
|---|---:|---|
| elementary | 5 (LikelihoodLanguage d1, SampleSpaceList d2, ComplementProbability d2, ExperimentalProbability d2, FundamentalCountingPrinciple d3) | SimpleProbability |
| middle | 7 (OddsProbability d1, ProbabilityAxiomsFinite d2, TreeDiagramProbability d2, RandomDigitSimulation d2, TwoWayTableProbability d3, VennProbability d3, CountingToProbability d4) | — |
| high | 10 (DiscreteUniformBernoulli d2, ReliabilitySystem d2, IndependenceCheck d3, LawOfTotalProbability d3, PmfCdfQuantile d3, ExpectationOfFunction d3, BayesMultipleHypotheses d4, Hypergeometric d4, NormalApproxBinomial d4, ClassicProbabilityPuzzles d4) | ConditionalProbability (re-banded d5 → d3), GeometricDistribution, NormalTable |
| college | 14 (ProbabilityMeasure d2, ProbabilityInequality d3, LinearityOfExpectation d3, CovarianceAlgebra d3, NegativeBinomial d3, MultinomialProbability d3, DistributionOfSum d3, PoissonProcess d3, MonteCarloArithmetic d3, ConditionalExpectation d4, ExpectedValueClassics d4, RandomWalk d4, MultiStateMarkov d4, ProbabilityCritic d4) | NamedDistribution |
| graduate | 6 (FiniteSigmaAlgebra d3, PGF d3, BallotReflection d4, PolyaUrn d4, MarkovStateClassification d4, MartingaleCheck d4) | — |

Total: **42 new generator classes, 5 extended**, roughly 225 operation
variants. Difficulty is now spread d1–d4 inside every band (the catalog
previously had no probability at d1–2 above elementary and only one
elementary class). Elementary moves 36 → 41 skills and middle 64 → 71,
in the direction of the `plans/dataset_plan.md` recipe.

## 7. Delivery order

One generator per commit, tests in the same commit, docs regenerated at the
end of each phase. Each phase ends with `uv run python -m unittest discover
tests`, `probe_generator_capacity.py --threshold 1000` on the new classes, a
seeded 200-example build per class with zero errors, and `OPCODES.md` /
`PROBLEM_TYPES.md` regenerated with `--check` passing.

| Phase | Deliverable | Why this order |
|---|---|---|
| 0 | `prob_common.py`, `tests/probability_oracle.py`, conventions test, DESIGN.md block, `NormalTableGenerator` switched to `phi_table()`, SimpleProbability ⟲ (pilot for the experiment objects) | everything downstream — and the statistics strand — renders and parses the same experiments and supplied constants |
| 1 | LikelihoodLanguage, SampleSpaceList, ComplementProbability, ExperimentalProbability, FundamentalCountingPrinciple, OddsProbability, ProbabilityAxiomsFinite, TreeDiagramProbability, RandomDigitSimulation | fills the thinnest bands first; exercises enumeration and weighted atoms before anything depends on them |
| 2 | TwoWayTableProbability, VennProbability, CountingToProbability, ProbabilityMeasure, ReliabilitySystem, IndependenceCheck, LawOfTotalProbability, ConditionalProbability ⟲ | the measure / product-law / renormalization core |
| 3 | DiscreteUniformBernoulli, PmfCdfQuantile, ExpectationOfFunction, BayesMultipleHypotheses, Hypergeometric, ClassicProbabilityPuzzles, NormalApproxBinomial, NormalTable ⟲ | random variables and the high-school capstones; unblocks statistics Phase 3 |
| 4 | LinearityOfExpectation, CovarianceAlgebra, ConditionalExpectation, DistributionOfSum, ProbabilityInequality, PGF | expectation algebra and its generating-function view |
| 5 | NegativeBinomial, MultinomialProbability, PoissonProcess, GeometricDistribution ⟲, NamedDistribution ⟲, RandomWalk, MultiStateMarkov, MonteCarloArithmetic, ExpectedValueClassics | distributions, limit theorems, processes (the CLT bridge is statistics Phase 3) |
| 6 | FiniteSigmaAlgebra, BallotReflection, PolyaUrn, MarkovStateClassification, MartingaleCheck | the graduate finish |
| 7 | ProbabilityCritic; phrasing sweep to 3–5 templates; full capacity probe; README inventory; regenerate `PROBLEM_TYPES.md`, `OPCODES.md`; HF dataset-card note | close-out |

Definition of done per generator (checklist copied into each PR): class
in `generators/`, registered in `quixi_math_datagen.py` import +
`ALL_GENERATORS` + `curriculum.CURRICULUM`; module-level `PROBABILITY =
True`; docstring lists variants and op-codes (one meaning each); 3–5
phrasings the oracle parses; mirrored test with contract, 500-sample
oracle from problem text, step-arithmetic check (`A/S/M/D/E/POW/NCR/
FRAC_BUILD/F`), variant reachability, invalid-variant guard, pipe safety;
composite answer wherever the bare verdict is a coin flip; capacity probe
passes or the small space is documented; seeded 200-example build with
zero errors.

## 8. Exactness decisions by topic

| Topic | Hazard | Decision |
|---|---|---|
| Normal approximation, quantiles (and the CLT bridge in the statistics plan) | Φ | supplied inline with decoy rows (NormalTable style); answer to 4 decimals; `n` and `npq` perfect squares so z has ≤ 2 decimals |
| LLN | limit statement | Chebyshev-form bounds only (exact fractions); no Φ needed |
| Poisson process, exponential memorylessness | e^−λt | supplied to 4 decimals as `e^-2 = 0.1353`; rate/time/thinning/merging/"which type first" variants are exact fractions with no constant |
| Coupon collector | H_n | exact `Fraction` harmonic sums, n ≤ 8 |
| Buffon | π | left symbolic (`2/(3π)`); π-estimates are fractions `2n/hits` |
| Birthday | large products | exact fractions for d ≤ 100 with n ≤ 6 (n ≤ 4 for d ≥ 30); d = 365 only for n ≤ 3 |
| Standardization, correlation | roots | variances built as perfect squares; Chebyshev uses σ² directly |
| Inverse-transform sampling | ln | exponential sampling excluded; linear and quadratic cdfs with perfect-square `u` |
| Gambler's ruin (biased) | (q/p)^N | N ≤ 5, p from a small bank; fractions stay hand-sized |
| Stationary distributions on 3 states | solving 3×3 | chains built backward from a chosen π (detailed balance) |
| Multinomial / hypergeometric / negative binomial | factorial growth | n ≤ 6, N ≤ 12, r ≤ 4 so brute-force oracles stay ≤ 50k cases |

## 9. Out of scope, and why

No exact hand procedure ⇒ no generator: continuous distributions beyond
what `ContinuousDistribution`/`NamedDistribution` already cover (gamma,
beta densities need Γ/B values), Brownian motion, characteristic functions,
measure theory on infinite spaces (Kolmogorov extension, σ-additivity
proofs), ergodic theorems, hypothesis testing and confidence intervals
(the statistics strand), simulation with unstated RNGs, and free-form
"explain why" tasks.

## 10. Decisions taken in this plan (change here, not per generator)

- `P(A given B)` for conditioning in both this strand and the statistics
  strand; `∣` (U+2223) is reserved for divisibility in foundations and the
  dot-plot / stem-and-leaf column separator in statistics.
- Events as rosters in the foundations set dialect; fixed enumeration order
  (H before T, ascending numbers, colours as listed).
- Probabilities and moments as lowest-terms fractions; 4-decimal answers only
  when a supplied constant is used; `as_percent`/`as_decimal` are explicit
  variants.
- Odds `a:b`; PGF polynomials descending with parenthesized fractional
  coefficients; π allowed in denominators as `2/(3π)`.
- `ConditionalProbabilityGenerator` re-banded to high d3; the middle-band
  on-ramp is `TwoWayTableProbabilityGenerator`.
- Brute-force enumeration is the default oracle; closed forms only where the
  space is infinite, and never shared with `prob_common.py`.
- Cross-strand ownership: `prob_common.py` owns `exact()`, `p4`, `pct`,
  `money`, `phi_table()` and the `(n, p)` bank, and `stats_common.py`
  imports them; `NormalApproxBinomialGenerator` is specified here (once);
  the sampling distribution of x̄/p̂ and CLT probabilities are specified in
  `plans/statistics_plan.md` (once); `TwoWayTableProbability` (fractions, middle)
  and the statistics `TwoWayTable` (percents, high) both stay; the
  foundations, probability, and statistics conventions tests share one
  ASCII-bar checker, and a class may carry more than one of the
  `FOUNDATIONS` / `PROBABILITY` / `STATISTICS` flags.

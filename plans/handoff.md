# QuixiMath — Handoff

Originally written 2026-08-25; updated 2026-08-27.
Nothing in this work is committed; everything is still in the working tree.

## Current source of truth — 2026-08-27

This section supersedes stale counts and red-status notes in the historical
sections below. Keep the older material for implementation context, but use
this section to resume work.

### Verification baseline

- There are now **526 registered generators**; every registered generator
  validates.
- `uv run python -m unittest discover tests` passes: **3339 tests**, `OK`
  (21.456s on the last run).
- `uv run python tools/gen_opcode_legend.py --check` passes.
- `uv run python tools/gen_problem_types.py --check` passes after both
  generated documents were refreshed.
- `git diff --check` and `compileall` are clean.
- No commits were created. The worktree is intentionally dirty and includes
  pre-existing user work; do not discard or reset it.
- The old §5 failure table is obsolete. The full tree is green at this
  checkpoint.

### Capacity work completed after the original handoff

The following continuation batches were completed and verified. Every class
listed below clears the seeded 5,000-draw capacity gate and its restricted
200-row dataset build completed with zero generator errors.

- **b1_08:** `ParamCountGenerator`, `ParametricCalculusGenerator`,
  `PartialTraceGenerator`, `PascalTriangleGenerator`,
  `PercentProblemGenerator`, `PermutationCombinationGenerator`,
  `PolarParametricGenerator`, `PolynomialZerosGenerator`,
  `PowerSeriesGenerator`, `PrimeFactorizationGenerator`.
- **b1_09:** `ProportionalRelationshipGenerator`, `PythagHypGenerator`,
  `PythagoreanLegGenerator`, `PythagoreanWordProblemGenerator`,
  `QuadraticGenerator`, `QuadraticSquareRootGenerator`,
  `QuantumGateGenerator`, `QuarkCompositionGenerator`,
  `RadicalRationalizeGenerator`, `RadicalVariableSimplifyGenerator`.
  Shared Pythagorean helpers now live in
  `generators/pythagorean_common.py`.
- **b1_10:** `RateConversionGenerator`, `RationalExponentGenerator`,
  `RecursiveExplicitGenerator`, `ReedSolomonGenerator`,
  `RegexToAutomatonGenerator`, `RelatedRatesGenerator`,
  `RelativisticEnergyGenerator`, `RepeatingDecimalGenerator`,
  `ResolutionProofGenerator`, `RiemannTensorGenerator`. All ten were
  widened; 53 focused tests passed.
- **b1_11:** `RightTriangleTrigGenerator`, `RootsAndRadicalsGenerator`,
  `RoundSolidsGenerator`, `RungeKuttaGenerator`, `SVDGenerator`,
  `ScalingGenerator`, `ScalingLawGenerator`, `SeriesConvergenceGenerator`,
  `SeriesSolutionGenerator`, `SigmaNotationGenerator`. Eight were widened;
  live re-probes showed `RootsAndRadicalsGenerator` and
  `RungeKuttaGenerator` already cleared the gate, so they were left intact.
  The 103 focused tests passed.
- **b1_12:** `SimpleProbabilityGenerator`, `SlopeInterceptFormGenerator`,
  `SphericalTriangleGenerator`, `SpinHalfGenerator`, `StabilityGenerator`,
  `StarsAndBarsGenerator`, `StereographicGenerator`,
  `StoichiometryGenerator`, `StructureConstantGenerator`,
  `SurfaceAreaCylinderGenerator`. All ten were widened; 63 focused tests
  passed.

For b1_10 through b1_12 specifically: **28 classes were widened and 2 were
verified as already complete**. No new op-codes were introduced.

### Exact restart point: b1_13

No b1_13 implementation edits have been made. The batch file is:

`/private/tmp/claude-501/-Users-eric-QuixiMath/c221c537-8a18-4b78-bd36-b25da77fc2d1/scratchpad/probe/batch_b1_13.txt`

A fresh seeded 5,000-draw probe confirmed that all ten classes still need
capacity work:

| Generator | Distinct live outputs | Estimated capacity |
|---|---:|---:|
| `SurfaceAreaPrismGenerator` | 989 | 995 |
| `TaylorSeriesGenerator` | 120 | 120 |
| `TonelliShanksGenerator` | 61 | 61 |
| `TriangleAreaSASGenerator` | 720 | 720 |
| `TriangleSolveGenerator` | 138 | 138 |
| `TrigIdentityVerifyGenerator` | 90 | 90 |
| `TrigSixFunctionsGenerator` | 144 | 144 |
| `TripleIntegralGenerator` | 772 | 773 |
| `TuringMachineTraceGenerator` | 39 | 39 |
| `USubstitutionGenerator` | 504 | 504 |

All ten probes had zero generator errors. Resume by widening these generators
without changing their mathematical procedures or answer conventions, then
run focused oracle tests, the combined capacity gate, one restricted seeded
200-row build per class, doc freshness checks, and the full suite.

---

## Historical context from the original handoff

The session that produced this state ran out of its weekly model quota
mid-flight (resets 2026-08-27 19:00 America/New_York). Roughly a dozen
background agents were killed at arbitrary points. **The tree has been
repaired and re-verified since** — see §4 for the one break that was found
and fixed, and §5 for what is still red.

---

## 1. What this project is, and what these tasks are for

QuixiMath generates synthetic math problems with visible, step-by-step
scratchpads (`problem`, pipe-delimited `steps`, canonical `final_answer`,
curriculum metadata). 510 registered generator classes, elementary through
graduate. `AGENTS.md` and `DESIGN.md` are the contract; read both.

Two work streams are in progress:

**A. Four new curriculum plans (Phase 0 of each).** The catalog is a
*procedure atlas* — it teaches executing named methods. Four planning
documents at the repo root add the missing halves:

| Plan | Adds | New classes |
|---|---|---:|
| `plans/foundations_plan.md` | logic, sets, relations, number construction, axiomatics | 51 |
| `plans/probability_plan.md` | probability as a measure, elementary → martingales | 42 |
| `plans/statistics_plan.md` | data displays, sampling/CLT bridge, inference, estimator theory | 35 |
| `plans/applied_plan.md` | modeling word problems, number sense, judgment, quantitative literacy, scenarios | 35 |

~163 new generator classes total. **Only Phase 0 (shared infrastructure) is
in scope right now** — no new generators have been written.

**B. The capacity bug.** A 5000-sample probe of all 510 classes found
**420 below a 100k problem space**, many with only dozens of distinct
problems (fixed case tables, tiny ranges, one phrasing). Under
equal-per-skill sampling that is severe repetition in a multi-million-row
corpus. The owner's requirement: **every generator must support hundreds of
thousands to millions of distinct problems.**

Original distribution:

| Estimated space | Classes |
|---|---:|
| under 1k | 149 |
| 1k–10k | 188 |
| 10k–100k | 83 |
| 100k–1M | 43 |
| over 1M | 47 |

---

## 2. Non-negotiable rules (from AGENTS.md + the plans)

- **Exact arithmetic only.** `fractions.Fraction`, integer math. Construct
  problems *backward from exact answers* (perfect squares under roots,
  2^a·5^b denominators wherever a decimal is rendered, integer eigenvalues).
- **Hand-solvable.** The procedure is the difficulty, never digit grinding.
- **No unstated lookups.** Any Φ / e^-λ / z* / t* / χ² / log / trig value must
  be supplied verbatim in the problem text, avoided by construction, or left
  symbolic.
- **Pipe safety.** No ASCII `|` in any step field or problem text; `|` is the
  delimiter only. Use `abs()`, `card(A)`, `P(A given B)`.
- **`steps[-1]` must be exactly `Z|<final_answer>`.** ≤ 4 payload fields per
  step.
- **One op-code = one meaning.** New codes are fine; never reuse an existing
  code with different field semantics. Check `OPCODES.md` before naming one.
- **A9 oracle tests.** Every generator's test must recompute the answer *from
  the problem text alone*, by an independent route (brute force, alternate
  formula). A generator agreeing with itself is not verification.
- **Three-place registration** for any new generator: import in
  `quixi_math_datagen.py`, instance in `ALL_GENERATORS`, entry in
  `curriculum.CURRICULUM`.
- Commit author for generator work is `Eric Hartford <eric@quixi.ai>`, no
  `Co-Authored-By` trailer. **Nothing here has been committed yet** — the
  owner has not asked for commits.

---

## 3. What is DONE and verified

### Shared infrastructure — `prob_common.py` (COMPLETE)

The numeric core all four strands import. **84 tests pass.**

Rendering: `dec`, `terminates`, `exact`, `prob_txt`, `p4`, `pct`, `money`,
`odds_txt`, `roster`, `given`, `leading_digit_round`.
Supplied constants: `phi`, `phi_table` (decoy rows), `supplied_constant`.
Exactness banks: `NP_BANK`, `binomial_sigma`, `is_perfect_square`,
`sqrt_fraction`.
Experiment objects: `Coin`, `Die`, `Spinner`, `Bag`, `NumberedCards`,
`LetterTiles`, `Menu`, `Product`, `product_space`; `Predicate` + named event
tests; `WeightedSpace` (measure / conditional renormalization / validity);
`TwoWayTable`.

Verified: `phi_table` is **byte-identical** to the original
`NormalTableGenerator._table` across 2000 random inputs; the
`NormalTableGenerator` and `ChiSquareGenerator` refactors produce **identical
output** on 500 seeded examples each (checked against `git show HEAD:`).

### `tests/conventions_common.py` (COMPLETE)

Shared strand-test scaffolding: `flagged_generators(flag)` (discovers
generators by module-level `FOUNDATIONS`/`PROBABILITY`/`STATISTICS`/`APPLIED`
= True), `sample_examples`, `pipe_violations`/`assert_pipe_safe`,
`assert_contract`, `method_word_hits`.

### `tests/probability_oracle.py` + probability conventions test (COMPLETE)

Independent parsers and brute-force enumerators; never imports
`prob_common`. 17 conventions tests including fixtures proving each checker
rejects a violating example.

### The capacity probe is now a real instrument

`tools/probe_generator_capacity.py` gained an **`est_cap` column** that infers
the true space size from the collision rate (inverts
`E[distinct] = N(1 − exp(−n/N))`), plus a `--min-capacity` flag. Accuracy
check: true 9 → est 9; true 1k → est 997; true 100k → est 122k; true 5M →
est 4.2M. 9 tests pass.

**Use this as the bar:**
```bash
uv run python tools/probe_generator_capacity.py --samples 5000 \
  --threshold 4850 --min-capacity 100000 --generators <ClassName>
```
4850/5000 distinct ≈ a 100k space; 4975 ≈ 1M; `>5000*` means unmeasurably
large (ideal).

### 27 generators widened and verified over the bar

Probed at 3000 samples after the work (est. capacity in parentheses):

`ComplexQuadratic` (>3000*), `EulerMethod` (>3000*), `Derangement` (>3000*),
`CYKParser` (>3000*), `LegendreConstruction` (>3000*), `ExponentialModel`
(4.5M), `AreaBetweenCurves` (4.5M), `LLLReduction` (4.5M), `Annuity` (4.5M),
`FactorSpecialForms` (2.2M), `Diagonalization` (2.2M), `NFASimulation`
(2.2M), `Casimir` (2.2M), `ComplexLog` (1.1M), `ArcSector` (899k),
`BooleanAlgebra` (642k), `LZCompression` (642k), `GeometricSequence` (562k),
`DerivativeTranscendental` (562k), `CompoundProbabilityDependent` (499k),
`LambdaReduction` (408k), `GeometricMean` (374k), `NaturalUnits` (374k),
`MatrixExponential` (280k), `MatrixGroupCheck` (144k), `NormalTable` (82k),
plus `RungeKutta` repaired (see §4).

Several of these were among the worst in the repo — `LLLReduction` was 4
distinct problems, `LambdaReduction`/`CYKParser`/`NFASimulation` were single
digits to dozens.

---

## 4. The one break that was found and fixed

`generators/euler_method_generator.py` was widened by one agent, which
changed two shared helpers:

- `f_txt(a, b)` → `f_txt(a, b, c, indep="x", dep="y")`
- `f_sub(a, b, xv, yv)` → `f_sub(a, b, c, xv, yv)`

`generators/runge_kutta_generator.py` imports both and was left calling the
old signatures — every `RungeKuttaGenerator.generate()` raised `TypeError`.
Fixed by passing the explicit constant term at its four call sites
(`f_txt(a, b, 0)`, `f_sub(a, b, 0, …)`); `tests.test_runge_kutta_generator`
passes (7 tests).

**Lesson for the next agent: several generator files share helpers across
modules.** Before changing any module-level function's signature, run
`grep -rn "from generators.<module> import"` and fix every importer in the
same edit.

Full-tree integrity now: **0 syntax errors** across all Python files; **525
of 526 registered generator instances** produce a valid example (the
remaining failure is a stale-doc test, §5).

---

## 5. What is RED right now (12 failing tests of 3285)

All of these are half-finished work from killed agents, not regressions in
shipped code. (A 13th, a wrong assertion in `test_set_common` about the
minimal element of a subset poset, was diagnosed and fixed — that module is
now green, 29 tests.)

| Module | Count | Diagnosis |
|---|---:|---|
| `test_stats_common` | 3 | `stats_common.py` SE-bank search returns rows with `n1 = 3200` while its own test asserts `n1 ≤ 2500`; two searches don't find their banked rows. Either widen the assertion or constrain the search — decide which is correct per `plans/statistics_plan.md` §3. |
| `test_applied_common` | 2 | Distractor injection not flagged as expected; a story fails the "names no method" check. The `METHOD_WORDS` list or the example template needs finishing. |
| `test_legendre_construction_generator` | 2 | Oracle can't reconstruct the trace / answer from the new problem text — the widened phrasings outran the oracle parser. |
| `test_factor_special_forms_generator` | 2 | Same shape: oracle expansion + variant availability. |
| `test_natural_units_generator` | 1 | `test_dimensional_identities_hold` — widened parameter space broke a dimensional invariant. |
| `test_area_between_curves_generator` | 1 | Oracle answer mismatch on a new phrasing. |
| `test_gen_problem_types` | 1 | `PROBLEM_TYPES.md` is stale. **Expected** — regenerate at the very end, not now. |

Reproduce any of them with `uv run python -m unittest tests.<module>`.

---

## 6. Phase 0 status per strand

| Strand | Module | Oracle | Conventions test | State |
|---|---|---|---|---|
| Probability | `prob_common.py` | `tests/probability_oracle.py` | `tests/test_probability_conventions.py` | **DONE**, 84 tests green |
| Foundations | `logic_common.py`, `set_common.py` | `tests/foundations_oracle.py` | `tests/test_foundations_conventions.py` | written; 1 failing test (a wrong assertion) |
| Statistics | `stats_common.py` | `tests/stats_oracle.py` | `tests/test_stats_conventions.py` | written; 3 failing tests |
| Applied | `applied_common.py` | `tests/applied_oracle.py` | `tests/test_applied_conventions.py` | written; 2 failing tests |

**Not yet done in Phase 0:**

1. **DESIGN.md convention blocks.** Each plan's Phase 0 requires a new block
   in DESIGN.md's "Answer Format Conventions". None are inserted. The
   probability one is finished and preserved verbatim in §9 below — insert it
   as-is. The other three still need writing (each plan's §3 has the source
   material).
2. **`curriculum.py` re-bands** (statistics Phase 0): `ModeGenerator` and
   `RangeGenerator` → MIDDLE difficulty 1; `MeanGenerator` and
   `MedianGenerator` → MIDDLE difficulty 2. Then run
   `uv run python -m unittest tests.test_datagen_pipeline`.
3. **`skills` metadata pass-through check** (applied Phase 0): confirm
   `validate_example`, `write_jsonl`, and `tools/build_hf_release.py` carry an
   extra `skills` key through unchanged. Read-only investigation.

---

## 7. The capacity work — how to continue

Batch files are pre-built at:
```
/private/tmp/claude-501/-Users-eric-QuixiMath/c221c537-8a18-4b78-bd36-b25da77fc2d1/scratchpad/probe/
```
`batch_b1_00.txt` … `batch_b1_14.txt` (149 classes under 1k — worst),
`batch_b2_00.txt` … `batch_b2_18.txt` (188 classes, 1k–10k),
`batch_b3_00.txt` … `batch_b3_08.txt` (83 classes, 10k–100k).
Each line: `Class<TAB>generator file<TAB>test file<TAB>est_capacity<TAB>distinct/5000`.

`CAPACITY_INSTRUCTIONS.md` in that directory is the full per-agent brief —
hand it to each worker verbatim. If the scratchpad has been cleared,
regenerate the batches by running the probe with `--json` and bucketing on
`estimated_capacity`.

**Batches with partial work already done** (a killed agent finished some
generators): b1_00, b1_01, b1_02, b1_03, b1_04, b1_05, b1_06, b1_07. Re-probe
each class in those batches before editing — the ones listed in §3 are done.

Known still-below-bar and **not** yet assigned to a finished batch:
`ChiSquareGenerator` (2.0k — only its `exact()` import was refactored),
`RungeKuttaGenerator` (480 — only repaired), `CompoundProbabilityIndependent`
(its sibling `Dependent` was widened; this class was not),
`ExponentRulesGenerator`, `ScientificNotationGenerator`,
`RootsAndRadicalsGenerator` (all three live in `generators/exponent_generator.py`,
which was partially widened).

**Watch for multi-class files.** `exponent_generator.py`,
`compound_probability_generator.py`, and `statistics_generator.py` each define
several registered classes; widening one leaves siblings behind.

### The recipe that worked

1. Diagnose why the space is small (nearly always a fixed instance table).
2. Widen the **mathematical** space first: build random instances backward
   from exact answers, verified by brute force (random unsatisfiable clause
   sets, random automata with simulated traces, random matrices with integer
   eigen-structure, wider hand-friendly coefficient ranges).
3. Then contexts (names, objects, units) and 3–5 natural phrasings.
4. Update the oracle test so it parses **every** phrasing and re-solves
   independently.
5. Run the module's test, then the probe, then a seeded 200-example build:
   `uv run python quixi_math_datagen.py -n 200 -o /tmp/x.jsonl -s 7 --generators <Class>`
   and read three samples for readability.

Preserve existing variant names and `operation` strings — add, never rename.

---

## 8. Suggested order of work

1. **Green the tree first.** Fix the 11 non-stale failures in §5. The
   `test_legendre_construction` / `test_factor_special_forms` /
   `test_area_between_curves` group is one shape: a widened generator grew
   phrasings its oracle parser no longer matches, so extend the parser.
2. **Finish Phase 0**: the three DESIGN.md blocks, the four `curriculum.py`
   re-bands, the `skills` pass-through check.
3. **Resume capacity batches** — 6–10 concurrent agents maximum. The previous
   session launched 20 and exhausted the quota; agents also cost ~200k tokens
   each. Instruct every agent to finish one generator completely (edit → test
   → probe) before starting the next, so a kill never leaves a half-edited
   file.
4. **Only at the very end**, regenerate the derived docs:
   ```bash
   uv run python tools/gen_opcode_legend.py
   uv run python tools/gen_problem_types.py
   uv run python -m unittest discover tests
   ```
   Then update README's inventory counts (they will be stale: catalog counts,
   grade-band distribution, op-code count).

Do not regenerate `PROBLEM_TYPES.md` / `OPCODES.md` mid-flight; they churn
enormously and conflict between agents.

---

## 9. Verbatim: the "Probability answers" block for DESIGN.md

Insert into DESIGN.md's "Answer Format Conventions" section as-is.

```markdown
## Probability answers (A0 extension)

- **Probabilities:** lowest-terms fraction (`3/8`); `0` and `1` for impossible
  and certain; integers plain. `as_percent` / `as_decimal` variants say which
  form the text wants and answer `37.5%` / `0.375` (totals chosen so the
  decimal terminates).
- **Conditioning:** always the word `given` — `P(A given B)`, never a bar and
  never `∣` (U+2223 is reserved for divisibility in the foundations strand).
  ASCII `|` is banned from probability problem text as well as from steps;
  tallies are written as counts or as `H T T H` sequences.
- **Events are sets** in the foundations dialect: sample space `S`, rosters
  `{1, 2, 3, 4, 5, 6}`, event rosters `A = {2, 4, 6}`, `∪ ∩ − Δ`, complement
  `Aᶜ`, empty `∅`, `card(A)` (never `|A|`); prose phrasings may say "A and B",
  "A or B", "not A".
- **Compound outcomes:** compact strings in enumeration order — `H1, H2, H3,
  T1, T2, T3`, `HH, HT, TH, TT`, draws as color initials `RB`, two numeric
  components as ordered pairs `(3, 4)`. **Enumeration order is fixed:** `H`
  before `T`, dice ascending, spinner sectors in the order printed, bag colors
  in the order the problem lists them, tree branches in the same order. Ties
  ("most likely outcome") break by enumeration order and the answer says so.
- **Supplied rounded constants:** when Φ or `e^-λ` enters, the problem says
  "to 4 decimal places" and the answer is a 4-decimal string (`0.2706`);
  arithmetic on the supplied value is exact decimal arithmetic
  (`Fraction("0.1353")`).
- **Moments:** E, Var and Cov as lowest-terms fractions; money as `$3.50`;
  negative values keep the ASCII minus (`-1/8`).
- **Odds:** `a:b` with a colon, in lowest terms (`3:5`). Absolute deviations
  as `abs(X − μ)`. Weighted atoms as `P(a) = 1/10`. Two-way tables in prose as
  `<row>=<v> and <col>=<w>: n`, cells joined with `; `.
- **pmf / cdf tables:** `P(S=0) = 1/8; P(S=1) = 3/8; …` and `F(1) = 1/8; …`
  in ascending support order. Vectors `π = (2/5, 2/5, 1/5)`. Functions on
  atoms `3/2 on {1, 2}; 3 on {3}; 5 on {4, 5, 6}`.
- **π in a denominator:** `2/(3π)` (A0 above covers only π in numerators).
- **PGF polynomials in `s`:** descending powers, fractional coefficients
  parenthesized: `(1/4)s^2 + (1/2)s + 1/4`.
- **Composite verdicts:** join with `; ` and put the checkable fact after the
  label — `likely; 5/8`, `independent; P(A ∩ B) = 1/3 = P(A)·P(B)`,
  `switch; 2/3 vs 1/3`, `invalid; sum = 9/8`. Every coin-flip verdict
  (`likely`, `independent`, `valid`, `fair`, `martingale`) carries the number
  that earns it.
```

---

## 10. Owner context worth knowing

- The owner is **deliberately building the full long tail**, including
  graduate niches. Generators are cheap relative to training compute, and once
  a generator exists the dataset scales arbitrarily. **Do not propose trimming
  scope or deferring low-value classes.**
- The two safeguards that make the long tail safe, and that must hold: the
  **capacity gate** (small spaces are memorization hazards under
  equal-per-skill sampling) and the **training-mix recipe / `--weights` layer**
  in `plans/dataset_plan.md` (every class added shifts the default mix).
- The dataset's purpose is real-world problem solving and genuine mathematical
  intuition — which is why `plans/applied_plan.md` exists and why its defining rule
  is that **the problem text names no method**.

---

## 11. Command reference

```bash
# one sample from a generator
uv run python quixi_math_datagen.py --sample --generators <Class> -s 7

# seeded build, check for errors
uv run python quixi_math_datagen.py -n 200 -o /tmp/x.jsonl -s 7 --generators <Class>

# capacity, the bar
uv run python tools/probe_generator_capacity.py --samples 5000 \
  --threshold 4850 --min-capacity 100000 --generators <Class>

# whole-repo capacity sweep to JSON
uv run python tools/probe_generator_capacity.py --samples 5000 \
  --threshold 4850 --json /tmp/capacity.json

# tests
uv run python -m unittest tests.test_<module>
uv run python -m unittest discover tests

# integrity: every generator still produces a valid example
uv run python -c "
import random; random.seed(11)
from quixi_math_datagen import ALL_GENERATORS, validate_example, stamp_metadata
bad=[]
for g in ALL_GENERATORS:
    try:
        ex=g.generate(); stamp_metadata(ex,g); validate_example(ex)
    except Exception as e: bad.append((type(g).__name__, type(e).__name__, str(e)[:80]))
print('failing:', len(bad));  [print(' ', *b) for b in bad]"

# derived docs — END OF WORK ONLY
uv run python tools/gen_opcode_legend.py
uv run python tools/gen_problem_types.py
```

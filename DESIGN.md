# Design Overview

## Architecture
- **Core contract:** `ProblemGenerator.generate() -> dict` (in `base_generator.py`) returns `problem_id`, `operation`, human-readable `problem`, `steps` (list of pipe-delimited op-code strings), and `final_answer`. The last step must be exactly `Z|<final_answer>`. The pipeline then stamps `grade_level` and `difficulty` from `curriculum.py` (generator-emitted values win).
- **Generators:** One class per skill in `generators/` (e.g., `long_division_generator.py`). Each is independent, seeded via `random` in `quixi_math_datagen.py`, and responsible for validating its own outputs before returning.
- **Data flow:** `quixi_math_datagen.py` seeds RNG, samples a skill (equal weight per class by default, `--weights` to override) then an instance within it, calls `generate()`, stamps metadata, runs `validate_example()`, dedups on `(operation, problem)`, then writes JSONL via `write_jsonl`. `--sample` prints one example per generator; `-n/-o/-s` builds datasets.
- **Step encoding:** Steps are pipe-delimited strings built with `helpers.step()` and `DELIM="|"`. Opcodes capture atomic reasoning moves (divide, multiply, bring-down, etc.) and end with `Z` holding the formatted answer string.
- **Extensibility:** To add a skill, create a new generator implementing `ProblemGenerator`, emit well-formed steps (including `Z|`), add it to `ALL_GENERATORS` in `quixi_math_datagen.py`, add a `curriculum.CURRICULUM` entry, regenerate `OPCODES.md`, and mirror tests in `tests/`.

## Pipeline
- **Philosophy:** the scratchpad ultimately belongs to the model — it may invent its own op-codes. The op-code vocabulary is therefore *organic*: no fixed registry, no vocabulary enforcement. `OPCODES.md` is a generated, descriptive legend (`tools/gen_opcode_legend.py`, AST-scan of `step()` call sites plus sampled examples). One rule of hygiene is enforced socially, not mechanically: one op-code = one meaning (don't reuse an existing code with different field semantics).
- **Validation (`validate_example`):** structure only — required keys, non-empty `steps` of non-empty strings, op-code present, at most 4 payload fields per step, final step `Z|<final_answer>` (string-coerced), `grade_level` in {elementary, middle, high, college, graduate}, `difficulty` an int in 1–5 (read relative to the band).
- **Metadata:** `curriculum.py` maps every registered class to `grade_level`/`difficulty`; `stamp_metadata()` fills the keys post-`generate()` with setdefault semantics so generators can override per-instance. Test-enforced invariant: every `ALL_GENERATORS` class has a valid entry.
- **Sampling:** instances group into skills by class name; each skill draws with equal probability (or its `--weights` override), then one instance uniformly within the skill. `MixedNumberOperationsRandom` is excluded from the default pool as a duplicate of the four `MixedNumberOperationGenerator` variants.
- **Dedup & budget:** exact `(operation, problem)` repeats are skipped (unless `--allow-duplicates`); the attempt budget is `n*10 + 1000` with an early stop after `max(2000, n)` consecutive rejects (exhausted problem space). A per-generator stats table (emitted / duplicates skipped / errors) prints after every build, and `build_dataset` returns the same summary programmatically.
- **Reproducibility:** with `-s/--seed`, builds are byte-for-byte deterministic (`helpers.jid()` draws UUIDs from the seeded `random` module); without a seed, natural randomness.

## Answer Format Conventions (A0)

Validation requires `steps[-1] == "Z|" + final_answer` exactly, and RL graders
need one canonical form. These conventions are the contract; extend this
section (don't fork it) when a new tier introduces new answer shapes.

- **Integers:** plain: `-4`, `366 R4` (division with remainder).
- **Money:** `$20.06` — dollar sign, two decimals, cents always exact.
- **Percentages:** `15%`.
- **Fractions:** lowest terms, `5/2`; mixed numbers space-separated `8 1/2`;
  final answers in mixed-number contexts convert improper → mixed.
- **Decimals:** exact only, minimal digits (`11.4`, not `11.40`).
- **π-forms:** coefficient then π then unit: `36π cubic units`; fractional
  coefficient keeps π before the slash's denominator: `500π/3 cubic units`.
- **Units:** appended when the problem has them: `cubic units`, `square units`.
- **Powers:** `x^5`; negative exponents rewritten: `1/x^3`; fraction bases
  reciprocal-flipped: `(3/2)^2`; exponent 1 and 0 simplified away (`x`, `1`).
- **Single solutions:** bare value `7`. **Inequalities:** `x ≤ 9` (relation
  symbols < > ≤ ≥). **Systems:** `x=-2, y=-3`. **Special solutions:**
  `No solution`, `All real numbers`.
- **Interval notation:** use `(-∞, -3) ∪ [2, 5)` with reduced rational
  endpoints; infinities are always open and excluded points such as rational
  function poles stay open even when the inequality is non-strict.
- **Asymptotic bounds:** use `Θ(...)` with a composite method/case label when
  the label is part of the skill, e.g. `case 1; Θ(n^2)` or
  `subtract; Θ(n^5)`.
- **Factored forms** (Algebra 1 tier): ASCII signs inside factors,
  GCF first, binomial factors ordered by ascending constant term:
  `3(x - 4)(x + 2)`.
- **Multiple roots:** ascending, joined with " or ": `x = -3 or x = 2`.
- **Radicals:** coefficient then radical `6√2`; variables inside the radical
  parenthesized when compound: `5x√(2x)`; denominators rationalized.
- **Expressions:** terms in descending power order: `2x^2 + 3x - 5`.

## Logic and set answers (A0 extension)

- **Logic notation:** `¬ ∧ ∨ → ↔ ⊕`; NAND is `↑`. Precedence is `¬` > `∧`
  > `∨` > `→` > `↔`, and every binary subformula except the outermost is
  parenthesized. Propositional variables are `p q r s`, predicates `P Q R`,
  and individuals `x y z`.
- **Truth values and tables:** `T` / `F`; variables alphabetically with `T`
  before `F`, so two-variable rows are `TT, TF, FT, FF`. A result column is
  one string such as `TFTT`.
- **Sets:** `∈ ∉`, `⊆ ⊂`, `∪ ∩ − Δ ×`, complement `Aᶜ`, empty `∅`, universe
  `U`, power set `P(A)`, and cardinality `card(A)`. Set-builder notation uses
  a colon: `{x ∈ ℤ : −3 ≤ x < 4}`. Divisibility uses the word `divides` or
  `∣` (U+2223), never ASCII `|`.
- **Canonical collections:** rosters are sorted with no duplicates and use
  comma-space separators; ordered pairs are `(a, b)`. Partition blocks are
  sorted by least element: `{{1, 3}, {2}, {4, 5}}`.
- **Composite verdicts:** join facts with `; ` and include the canonical
  witness: `valid; modus tollens`, `not equivalent; differ at p=T, q=F`,
  `injective no (f(2) = f(4) = 3); surjective yes; bijective no`. Binary
  labels such as `true`, `valid`, or `reflexive yes` never stand alone.

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

## Statistics answers (A0 extension)

- **Notation:** `μ σ σ² x̄ s s² p p̂ Φ χ² Σ α β`; absolute values use
  `abs(z)`. Problems and setup steps state sample versus population, and the
  formula step names the divisor `n` or `n - 1`. Conditioning uses `given`.
- **Numbers and lists:** data use comma-space separators; sorted step fields
  use commas without spaces. Terminating decimals are minimal, other exact
  values are reduced fractions, supplied-Φ probabilities retain four decimal
  places, percents use `%`, and intervals use `(45.738, 54.262)`.
- **Table-shaped answers:** ascending `key: value` pairs joined by `; `, for
  example `6: 2; 7: 0; 8: 4` or `1: 2 5 7; 2: 0 3 3; 3: none; 4: 1`.
  Multi-statistic summaries use labeled fields such as `SSB = 128; SSW = 24;
  df = 2, 9; MSB = 64; MSW = 8/3; F = 24`.
- **Composite verdicts:** the label is followed by the earning fact:
  `right-skewed; mean 24.5 > median 20`, `fails; np = 6 < 10`, `unusual;
  z = 2.5`. Hypothesis decisions keep `reject H0 (4.4 > 2.576)` or
  `reject H0 (p = 0.0228 < 0.05)`.
- **Displays:** tally, dot-plot, stem-and-leaf, box-plot, histogram, two-way
  table, and supplied-constant renderings follow the exact parseable textual
  forms defined in `plans/statistics_plan.md` §3. Empty rows/bins required by a
  display remain visible; stem-and-leaf plots always include a key.
- **Supplied constants and rules:** every Φ, z*, t*, χ², F, percentile-z, or
  `e^-λ` value used in a step appears verbatim in the problem, with degrees of
  freedom where applicable. Quartile, percentile, trimming, outlier, modal-
  class, median-class, and bootstrap conventions are stated in the problem.

## Applied answers (A0 extension)

- **Problem text names no method:** it gives only the situation and question.
  A separately labeled `scaffolded` modifier may name a method and is never
  the default.
- **Quantities:** always carry units (`2 hours`, `48 km/h`, `112 m²`, `53
  tiles`); money is `$712.50` without thousands separators, percents are
  `40%`, and changes between percents are `10 percentage points`.
- **Standard modifiers:** `distractor` begins with `SELECT_RELEVANT` and does
  not change the answer; `estimate_first` wraps the exact work with
  `ESTIMATE` / `ESTIMATE_CHECK`; `with_model` answers with the canonical
  equation then value, such as `1/6 + 1/3 = 1/t; t = 2 hours`.
- **Missing information:** exactly `insufficient information; need <slot
  name>`, using the story template's human phrase, such as `the price of a
  notebook`.
- **Composite verdicts:** `label; fact`, for example `plan B; $420 vs $455`,
  `implausible; correct 80 km/h`, or `does not apply; fixed $3 fee makes cost
  non-proportional; correct $23`. Choice labels never stand alone.
- **Canonical models:** `with_model` uses the template's fixed variable and
  arrangement (`t` time, `h` hours, `x` count, `w` width, `p` price). Rejected
  physical roots or orientations are explicit, e.g. `REJECT|t = -1|negative
  time`.

## Verification & Trial-and-Error Vocabulary (A1 / A2)

- `CHECK|method|lhs_work|rhs_work` — two independent routes to the same
  value; the two work strings MUST agree. Methods so far: `cross_products`,
  `split`, `tip_two_ways`, `substitute`, `boundary_equality`,
  `multiply_back`. Emitted on roughly half of examples (both habits — with
  and without an explicit check — should appear in training).
- `CHECK_POINT|point|lhs_work|rhs_work` — evaluate both sides at a test
  point; agreement NOT required (a contradiction's check point deliberately
  disagrees; an identity's check points agree).
- `TRY|candidate|test_work` / `REJECT|candidate|reason` /
  `ACCEPT|candidate|confirmation` (A2, reserved) — candidate testing for
  factoring, rational-root search, and radical simplification. Real
  scratchpads contain dead ends; emit the tried-and-rejected candidates,
  not just the winner.

## Derived Record Formats (critic tasks)

**Format decision: no schema change.** A given (worked or partial)
scratchpad embeds in the `problem` text as numbered lines in the normal
pipe dialect — the model reads its own step language as input. The output
is ordinary `steps`. Step fields never contain pipes: given lines are
referenced by their 1-indexed number.

- **Error-spotting** (`error_spotting_*` operations): the problem shows a
  worked solution with exactly one arithmetic mistake; every given line
  after the mistake is consistent with it (real erring-student work — the
  error propagates). Output: `VERIFY|k|ok` sweeps each given line in order;
  `FLAG|k|<true arithmetic, pipe-free>` marks the wrong line; then the work
  is REDONE from line k in ordinary op-codes (lines after k are implicitly
  invalidated), ending with a CHECK where natural and `Z`.
  `final_answer` is composite (Principle 8): `step <k>; <correct answer>` —
  re-solving without locating the error earns nothing.
- **Fill-in-the-missing-step**: one given line is replaced by `____`;
  `final_answer` is the missing step verbatim (pipe format).
- **Estimate-then-compute**: not a new record shape — a variant where steps
  open with `ESTIMATE|<rounding work>|<estimate>` and close with
  `ESTIMATE_CHECK|<estimate>|<exact>|<verdict>` before `Z`. (Its own code,
  not `CHECK`: an estimate and the exact value agree only approximately,
  and `CHECK`'s contract requires exact agreement.)

## Curriculum (Generators & Skills)
- **Long Division:** Integers 2–99 divisors; includes bring-down (`B`), divide (`D`), multiply (`M`), subtract (`S`), remainder (`R`), and final `Z`.
- **Multi-digit Addition (integers):** Column alignment (`INT_ALIGN`), per-column sums with carry (`ADD_COL`), final carry (`CARRY_FINAL`), and final `Z`.
- **Multi-digit Subtraction (integers):** Column alignment (`INT_ALIGN`), per-column differences with borrow (`SUB_COL`), explicit borrow steps (`BORROW`), final `Z`.
- **Multi-digit Multiplication (integers):** Multiplication setup (`MUL_SETUP`), digit-by-digit partials (`MUL_PARTIAL`), summing partials (`ADD_PARTIALS`), final `Z`.
- **Mixed Number Operations (+, -, *, /):** Convert to improper (`MIX_IMPROPER`), align denominators (`L`, `C`), invert for division (`I`), operate on numerators (`A`/`S`/`M`), simplify (`F`), convert back to mixed (`IMPROPER_TO_MIX`), final `Z`.
- **Fraction Comparison:** LCD (`L`, `C`), compare converted fractions (`CMP`), final `Z`.
- **Fraction/Decimal/Percent Conversions:** Conversions across forms (`FRAC_TO_DEC`, `DEC_TO_FRAC`, `PERCENT_TO_DEC`, `DEC_TO_PERCENT`), simplify where needed, final `Z`.
- **Factors & Multiples:** Factor listing via trial division (`FACT_CHECK`, `FACT_PAIR`), prime factorization via repeated division (`PF_STEP`, `PF_PRIME`), GCF via Euclid (`GCD_START`, `GCD_STEP`, `GCD_RESULT`), LCM via product/gcd (`LCM_FROM_GCD`), final `Z`.
- **Order of Operations:** Precedence steps with arithmetic ops and rewrites (`REWRITE`), final `Z`.
- **Geometry (Perimeter/Area/Volume):** Compute perimeters (`PERIM`), areas (`AREA`), and volumes (`VOLUME` for rectangular prisms) using explicit arithmetic steps and rewrites where needed, final `Z`.
- **Place Value & Rounding / Number Comparison:** Digit inspection (`ROUND_CHECK`), rounded result (`ROUND_RESULT`), alignment/comparison (`ALIGN_NUM`, `CMP_NUM`), final `Z`.
- **Divisibility & Classification:** Divisibility checks (`DIV_CHECK`), prime/composite markers (`PRIME`, `COMPOSITE_FACTOR`), final `Z`.
- **Unit Conversions:** Factor-label conversion (`CONV_FACTOR`, `CONV_RESULT`), explicit multiply, final `Z`.
- **Basic Data/Statistics/Probability:** Sort (`SORT`), arithmetic sums/divides for mean (`MEAN_DIV`), median selection (`MEDIAN_PICK`/`MEDIAN_PAIR`), mode counting (`MODE_COUNT`/`MODE`), simple probability setup (`PROB_SETUP`) with division/simplify, final `Z`.
- **Decimal Multiplication:** Partial products (`MUL_PARTIAL`), decimal placement (`COUNT_DP`, `PLACE_DP`), partial sums (`ADD_PARTIALS`).
- **Decimal Addition/Subtraction:** Column alignment (`DEC_ALIGN`), column operations (`DEC_ADD_COL`, `DEC_SUB_COL`), carries (`DEC_CARRY_FINAL`), final `Z`.
- **Decimal Division:** Decimal shifting (`DEC_SHIFT`), setup (`DIV_SETUP`), quotient decimal placement (`PLACE_DP_Q`), reuse of `B/D/M/S`.
- **Fraction Operations (+, -, *, /):** LCD and conversions (`L`, `C`), simplification (`F`), inversion (`I`), arithmetic (`A`, `M`, `D`, `S` reused contextually), final `Z`.
- **Linear Equations (Simple/Complex):** Move terms (`MOVE_TERM`), combine like terms (`COMB_X`, `COMB_CONST`), divide coefficients (`DIV_COEFF`), rewrite (`REWRITE`), final `Z`.
- **Quadratic Equations:** Discriminant (`DISC`), root extraction (`ROOT`), quadratic formula branches (`Q1`, `Q2`), final `Z`.
- **Simplify Algebraic Expressions:** Distribution (`DIST`), combining terms, rewrites, final `Z`.
- **Evaluate Expressions:** Substitution (`SUBST`), arithmetic steps as needed, final `Z`.
- **Proportional Relationships:** Proportion setup (`PROP_SETUP`), solving via algebraic steps, final `Z`.
- **Pythagorean Hypotenuse:** Exponents (`E`), square root (`ROOT`), final `Z`.
- **Percent Problems (find part/percent/whole):** Percent-to-decimal (`PERCENT_TO_DEC`), equation setup/rearrange (`SETUP_PERCENT_EQ`, `REARRANGE_EQ`), calculation (`PERCENT_CALC_PART`), convert back (`DEC_TO_PERCENT`), final `Z`.
- **Abacus-Style Addition:** Initial set (`AB_SET`), informational notes (`AB_INFO`), column adds (`AB_ADD_DGT`), carry propagation (`AB_CARRY`, `AB_CARRY_FINAL`), final `Z`.
- **Graph Interpretation (Bar/Line/Pictograph):** Graph data recording (`GRAPH_DATA`), value reading (`GRAPH_READ`), comparisons (`CMP`), min/max identification (`GRAPH_MIN`, `GRAPH_MAX`), change tracking (`GRAPH_CHANGE`, `GRAPH_MAX_CHANGE`), pictograph key (`PICTO_KEY`) and symbol counting (`PICTO_COUNT`), arithmetic steps reused (`A`, `S`, `M`), final `Z`.

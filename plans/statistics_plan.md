# Statistics Curriculum Plan

Descriptive statistics and data displays, sampling distributions and the
CLT, p-values and the full inference toolkit, study design, and estimator
theory — rebuilt as procedural, hand-solvable, oracle-checkable generators in
the same scratchpad dialect as everything else in this repo. Companion to
`plans/foundations_plan.md` (logic, sets, relations, number) and
`plans/probability_plan.md` (probability as a measure); same bar, same entry
format, same definition of done. This strand owns the probability →
inference bridge (sampling distributions, standard error, CLT, p-values) and
imports its numeric helpers from the probability strand's `prob_common.py`.

The bar is unchanged from `AGENTS.md` / `TODO.md`: exact arithmetic only
(`fractions.Fraction`, integer math, `dec()` only for 2^a5^b denominators),
human-like steps, pipe-safe fields (≤ 4 payload fields, no ASCII `|`
anywhere, `abs()` never bars), A0 answer conventions, an A9 oracle test that
recomputes the answer from the problem text alone by an independent route,
capacity > 1000 distinct problems per class, one class per skill registered in
three places, `PROBLEM_TYPES.md` / `OPCODES.md` regenerated. Every lookup
value — Φ, z*, t*, χ², F, percentile z — is supplied in the problem text,
avoided by construction, or left symbolic.

## 1. What "foundational statistics" means here

The subject builds in the order a person learns it, and so does this plan:

| Stage | Content | Plan strand |
|---|---|---|
| grades 2–5 | collect, tally, display; read a display back | S1. Data displays |
| grades 6–8 | center, spread, shape; compare distributions; sampling as an idea | S1 + S2. Descriptive measures |
| grades 9–12 (AP) | two-variable data, the normal model, sampling variability | S2 + S3. Normal model and the sampling bridge |
| AP / intro college | confidence intervals, tests, p-values, errors and power, χ², ANOVA, slope inference | S4. Inference |
| AP / intro college | how the data were obtained: sampling and experiments | S5. Study design |
| graduate | what makes an estimator good: bias, MSE, information, sufficiency, likelihood, posteriors | S6. Estimator theory |

Everything below is something a person finishes with pencil and paper by a
deterministic procedure. Topics whose answer is a judgment call (how "strong"
a scatter looks, whether a histogram is "roughly" normal) either get an exact
stand-in rule stated in the problem or are out of scope (§8).

## 2. Current coverage and gaps

Already in the registry (keep, extend where noted):

| Class | Band | Covers | Gap |
|---|---|---|---|
| `SimpleStatsGenerator` | elem d2 | mean / median / mode, one fixed sentence | — |
| `GraphInterpretGenerator` | elem d1 | bar / line / pictograph reading, 17 variants | no construction, no double-bar |
| `MeanGenerator`, `MedianGenerator`, `ModeGenerator`, `RangeGenerator`, `MeanAbsoluteDeviationGenerator` (`statistics_generator.py`) | middle d3–4 | one statistic each | all banded d3–4 for what they are; re-band (§9) |
| `FiveNumberSummaryGenerator` | middle d3 | summary / IQR / 1.5×IQR outliers; sizes chosen so quartiles are data points | no box plot rendering |
| `StandardDeviationGenerator` | middle d4 | population variance, sample variance, population sd | no sample sd, shortcut formula, frequency-table sd, CV |
| `FrequencyTableGenerator` | middle d3 | total / mode / relative / cumulative / above on pre-binned counts | no construction from raw data |
| `ZScoreGenerator` | high d4 | standardize / raw / compare / abs(z) > 2 | — |
| `NormalTableGenerator` | high d4 | inline Φ excerpt with decoy rows; below / above / between | no inverse, no empirical rule |
| `RegressionGenerator` | high d5 | line / r / r² / residual / predict, x fixed 1..5 | no covariance, no slope inference |
| `ConfidenceIntervalGenerator` | high d5 | mean margin / mean CI / prop margin / sample sizes; z* supplied | no proportion interval, no t, no differences |
| `HypothesisTestGenerator` | high d5 | one-prop z and one-sample t, two-sided only | no one-sided, no z for mean, no p-values |
| `TwoSampleTestGenerator` | high d5 | t (n1 = n2 = 8, s1 = s2 = 4 hard-coded) and prop z | no pooled, no unequal n, no paired |
| `ChiSquareGenerator` | high d5 | uniform GoF, 2×2 independence | no non-uniform GoF, r×c, homogeneity |
| `LeastSquaresGenerator`, `ClassifierMetricsGenerator`, `KMeansStepGenerator` | college | — | — |
| `MLEGenerator`, `MethodOfMomentsGenerator`, `BayesianUpdateGenerator`, `OrderStatisticsGenerator`, `PCAGenerator` | graduate | Bernoulli/exp/normal-μ MLE; first-moment MoM; beta-binomial and normal-normal | no σ²/Poisson/Uniform MLE, no two-parameter MoM, no gamma-Poisson, no MAP/predictive |

Not represented anywhere today: tally and frequency from raw data, dot plots,
fraction line plots, stem-and-leaf, box plots (read / shape / compare),
histogram construction, scatter description, population vs sample, weighted
and combined means, missing-value and add/remove-a-value means, outlier
effect on mean vs median, grouped data (midpoints / modal / median class),
percentiles and percentile rank, midrange / trimmed / harmonic / geometric
means, linear transformation effects, two-way tables, standalone covariance
and correlation, empirical rule, inverse normal, normal approximation to the
binomial, sampling distribution of x̄ and p̂ by enumeration, standard error and
CLT probabilities, p-values, one-sided tests, z-test for a mean, hypothesis
statement and error identification, condition checks, t-intervals, paired t,
pooled and Welch t, proportion intervals, CIs for differences, Type II error
and power, non-uniform and r×c χ², one-way ANOVA, slope inference, sign /
permutation / bootstrap-percentile procedures, empirical CDF, sampling-method
and bias identification, systematic / stratified / random-digit selection,
estimator bias by enumeration, MSE decomposition, Fisher information and
CRLB, factorization, likelihood-ratio tests, discrete-grid posteriors and
MAP, gamma-Poisson conjugacy.

Difficulty compression today: every middle-band statistics class is d3–4 and
every high-band one is d4–5. New classes are placed d1–d3 wherever the skill
is genuinely that easy, and four existing middle classes are re-banded (§9).

## 3. Strand-wide rules (in addition to AGENTS.md)

**Notation (one dialect, used in problems, steps, and answers).**
- Symbols: `μ σ σ² x̄ s s² p p̂ Φ χ² Σ α β`, `abs(z)` for absolute value
  (never bars), `‖·‖` if a norm is ever needed. Sample vs population is
  always said in words in the problem ("sample standard deviation",
  "population variance") and in the setup step; the formula step names the
  divisor (`n` or `n - 1`). Conditioning, where it appears, is
  `P(A given B)` as in `plans/probability_plan.md`.
- Data lists in problems: comma-space separated `12, 15, 17`; inside a step
  field a sorted list is comma-joined without spaces (existing `SORT`
  convention). Paired data: `before: 12, 15, 17` / `after: 14, 15, 20`.
- Numbers: integers plain; terminating decimals via `dec()` with minimal
  digits; anything else as a reduced fraction via the shared `exact()`
  (owned by `prob_common.py`, currently duplicated in `chi_square` and
  `binomial_probability`). Probabilities read from a supplied Φ table and
  anything derived from them keep 4 decimals (`0.0228`); enumerated
  probabilities are reduced fractions (`5/18`). Percents `65%`. Intervals
  `(45.738, 54.262)`.
- **Text-list answers** for anything table-shaped: `key: value` pairs joined
  with `; `, keys in ascending order — `6: 2; 7: 0; 8: 4`, `0-9: 3; 10-19: 5`,
  `3: 1/6; 4: 1/6; 5: 1/3`, `SSB = 128; SSW = 24; df = 2, 9; MSB = 64;
  MSW = 8/3; F = 24`.
- **Composite verdicts** join facts with `; ` and put the checkable fact after
  the label (existing style `reject H0 (4.4 > 2.576)` is kept for tests; the
  p-value form is `reject H0 (p = 0.0228 < 0.05)`). Examples:
  `right-skewed; mean 24.5 > median 20`, `stratified; groups = grade level`,
  `fails; np = 6 < 10`, `unusual; z = 2.5`, `MAP θ = 0.8; posterior
  1024/1713`, `E[σ̂²] = 7/3; σ² = 14/3; bias = -7/3`.
- These become a new "Statistics answers" block in DESIGN.md §Answer Format
  Conventions (Phase 0 deliverable).

**Exact textual renderings of displays** (this is a text dataset; every
display is a string, and every string is parseable by the oracle). Problems
that contain a display put it after the prose on its own lines, exactly as
`NormalTableGenerator` embeds its table.

- *Tally table.* One row per category, alphabetical: `Red: ////\ //` — a
  completed group of five is the four strokes plus the crossing backslash
  `////\`, groups separated by one space, then the leftover singles. Never the
  ASCII bar.
- *Dot plot.* One row per integer from min to max **including empty rows**
  (so gaps are visible), value right-aligned to the width of the largest
  value, then ` ∣ ` (U+2223), then `●` marks separated by single spaces:
  ```
  Dot plot of quiz scores (each ● is one student):
   6 ∣ ● ●
   7 ∣
   8 ∣ ● ● ● ●
   9 ∣ ●
  10 ∣ ● ●
  ```
  A fraction line plot uses the same layout with fraction labels in lowest
  terms (`1/4`, `1/2`, `3/4`, `1`, `1 1/4`), rows at every multiple of the
  stated unit.
- *Stem-and-leaf.* Header `Stem ∣ Leaves`, one row per stem from lowest to
  highest **including empty stems**, leaves ascending and space-separated, and
  a key line always present:
  ```
  Stem ∣ Leaves
     1 ∣ 2 5 7
     2 ∣ 0 3 3
     3 ∣
     4 ∣ 1
  Key: 2 ∣ 3 means 23
  ```
  Decimal data uses `Key: 2 ∣ 3 means 2.3`. In answers the plot is a text
  list `1: 2 5 7; 2: 0 3 3; 3: none; 4: 1`.
- *Box plot.* Two aligned lines under a fixed 7-character prefix; the scale
  starts at a multiple of 5 with `+` ticks every 5 units and **one character
  per unit**; the plot line puts `*` at min and max, `[` at Q1, `]` at Q3,
  `:` at the median, `=` inside the box, `-` on whiskers, and `o` for each
  outlier (whisker then ends at the last non-outlier). The reading rule is
  stated in the problem text every time.
  ```
  Scale: 0    5    10   15   20
         +----+----+----+----+
  Plot:     *-[==:===]--*
  ```
  (min 3, Q1 5, median 8, Q3 12, max 15). Construction guarantees
  min < Q1 < median < Q3 < max, all integers, scale width ≤ 40. Two plots
  (`compare_two`) are stacked as `Plot A:` / `Plot B:` under one scale.
- *Histogram bins* are inclusive integer ranges `10-19`, width a multiple of
  5, listed as `10-19: 4` (existing `FrequencyTableGenerator` form).
- *Two-way table.* Space-aligned columns with a header row and `Total`
  row/column when the variant supplies them:
  ```
             Yes   No   Total
  Grade 9     12    8      20
  Grade 10    15   15      30
  Total       27   23      50
  ```
- *Φ excerpt.* Exactly `NormalTableGenerator`'s form: `Standard normal table,
  Φ(z) = P(Z < z): z=1.10: 0.8643; z=1.50: 0.9332; z=1.80: 0.9641` — the
  rows the procedure actually reads **plus two decoy rows**; z printed with
  as many decimals as the procedure produces (2 usually, 3 for power
  problems: `z=0.855: 0.8037`). Negative z is never tabulated; the step
  `REWRITE|Φ(-1.50) = 1 - Φ(1.50)` applies symmetry.
- *Other supplied constants* are written inline: `z* = 1.96`, `t* = 2.262
  (df = 9)`, `χ² critical value = 5.991 (df = 2)`, `F critical value = 4.26
  (df 2, 9)`, `Selected z-scores: 80th percentile z = 0.84; 90th z = 1.28;
  95th z = 1.645; 97.5th z = 1.96; 99th z = 2.33` (inverse table, with
  decoys).

**No unstated lookups — enforced mechanically.** Every `TABLE_LOOKUP` (Φ
rows) and `LOOKUP_SUPPLIED` (z*, t*, χ², F, percentile z, `e^-λ`) step's
value must appear verbatim in the problem text; `tests/test_stats_conventions.py`
asserts it (§4). Degrees of freedom are always printed next to t / χ² / F
critical values. Welch t uses the stated conservative rule
`df = min(n1 - 1, n2 - 1)`.

**Exactness by construction** (the deviation-pattern library in
`stats_common.py`, §4, does the heavy lifting):
- Means are integers or terminating decimals because data are built as
  `mean + d_i` with a zero-sum integer pattern `d`.
- Standard deviations: the pattern's `SS = Σd²` is filtered so that `SS/n`
  (population) or `SS/(n - 1)` (sample) is a perfect square, e.g. n = 5
  patterns `(-3,-3,1,1,4)` (SS 36 → s = 3), `(-6,-2,2,2,4)` (SS 64 → s = 4);
  n = 4 `(-3,1,1,1)` (SS 12 → s = 2); n = 7 `(-3,-3,-3,0,3,3,3)` (SS 54 →
  s = 3). The library is enumerated programmatically (|d| ≤ 8, n = 4..8) and
  cached; the plan only requires that the filtered pools be non-empty and
  large enough (they are — hundreds of patterns per n).
- Standard errors: `n` a perfect square (`SE = s/√n`), `p(1-p)/n` a perfect
  square rational (`(0.5, 100) → 0.05`, `(0.2, 400) → 0.02`, `(0.1, 900) →
  0.01`, `(0.4, 600) → 0.02`), `1/n1 + 1/n2` a perfect square rational
  (`(8,8) → 1/4`, `(18,18) → 1/9`, `(50,50) → 1/25`, `(5,20) → 1/4`,
  `(20,80) → 1/16`, `(10,90) → 1/9`), `s1²/n1 + s2²/n2` a perfect square
  (`(12,9,6,4) → 25`, `(15,25,16,16) → 25`, `(18,36,12,9) → 25`,
  `(20,25,9,9) → 25`).
- Pooled variance: `n1 = n2` with `(s1, s2) ∈ {(1,7),(5,5),(7,17),(7,23),
  (2,14)}` so `(s1² + s2²)/2` is a square; unequal n uses `s1 = s2`.
- Binomial-normal σ: the `(n, p)` bank with perfect-square `npq` lives in
  `prob_common.py` and is specified under `NormalApproxBinomialGenerator` in
  `plans/probability_plan.md`.
- ANOVA: equal group sizes, per-group zero-sum patterns, integer group means
  whose mean is an integer → integer SSB and SSW; F rendered with `exact()`.
- Percent answers: sample sizes chosen so the percent is an integer or
  terminates (`count/n × 100` with n dividing a power of 10 times the count).
- Empirical-rule counts: N ∈ {200, 400, 1000, 2000, 4000} so 16%, 2.5%,
  0.15%, 13.5%, 2.35% of N are integers where used.

**Rule-dependent statistics are stated in the problem.** Quartiles: the
median-exclusive-halves rule already used by `FiveNumberSummaryGenerator`,
sizes from its `SIZES`. Percentiles: nearest-rank, "position = ⌈k·n/100⌉ in
the sorted list", stated. Percentile rank: "percent of values strictly
below", stated. Trimmed mean: "remove the lowest p% and highest p%", with
p·n an integer. Outliers: 1.5×IQR. Modal class: unique by construction.
Median class: "the first class whose cumulative frequency reaches n/2",
stated. Bootstrap percentile interval: nearest-rank on the given list, stated.

**Tiny answer spaces are composite.** Shape labels, method labels,
reject/fail, usual/unusual, biased/unbiased, efficient/not, sufficient
statistic names — every one carries the number or phrase that earns it.

**Capacity.** Every new generator passes
`uv run python tools/probe_generator_capacity.py --threshold 1000`. Small
mathematical spaces are widened by the pattern library × mean shift ×
shuffle × context bank × 3–5 phrasings; known-small exceptions (none
expected) go in the class docstring.

**Oracles (A9).** The generator renders; the test parses the rendered
problem with the independent parsers in `tests/stats_oracle.py` (dot plot,
tally, stem-and-leaf, box-plot columns, histogram bins, two-way table, Φ
excerpt, inline constants) and recomputes by a different route: full
enumeration for sampling distributions and estimator expectations, identity
checks (`Var(x̄) = σ²/n · (N-n)/(N-1)`, `Σ residuals = 0`, `SST = SSB + SSW`,
`E[(ℓ')²]` vs `-E[ℓ'']`), independent closed forms, keyword-table inversion
for scenario labels. The oracle module never imports `stats_common` or
`prob_common`.

**Phrasing.** 3–5 templates per generator from day one, with a shared
context bank (quiz scores, plant heights, commute minutes, battery hours,
package grams, daily sales, rainfall mm, ages, shoe sizes, points per game)
carrying units into problems and answers where natural.

## 4. Phase 0 — shared infrastructure

Built once, before any generator, each with its own tests. Depends on
`prob_common.py` (probability Phase 0) for `exact()`, `dec()`, `pct`,
`phi_table()`, and the `(n, p)` bank.

- `stats_common.py` (repo root, beside `helpers.py`): re-exports of the
  `prob_common` numeric helpers; the **deviation-pattern library**
  (`patterns(n, *, pop_square=False, sample_square=False, ss=None,
  max_abs=8)` returning cached zero-sum tuples with the requested
  perfect-square property); `sample_from_pattern(mean, pattern,
  shuffle=True)`; the perfect-square SE tables listed in §3; renderers
  `render_tally`, `render_dot_plot`, `render_line_plot`, `render_stem_leaf`,
  `render_box_plot` (with the column arithmetic), `render_two_way`,
  `render_bins`; `inverse_z_table(percentiles)`; `five_summary()`
  re-exported from `five_number_summary_generator`; `nearest_rank(sorted,
  k)`; a context bank with units; and `running_sum_steps(values)` (the
  `A`-chain helper that four generators currently reimplement).
- `tests/stats_oracle.py`: independent parsers for every rendering above and
  for inline constants (`z* = 1.96`, `t* = 2.262 (df = 9)`, Φ rows);
  independent exact routines (`mean`, `median`, `sd(pop/sample)`,
  `five_summary`, `enumerate_samples(pop, n, replace)`, `binomial_tail`,
  `chi_terms`, `anova`), and a keyword→label table for study-design
  scenarios. Every statistics test imports from here, never from
  `stats_common`.
- `tests/test_stats_conventions.py`: for every generator with module-level
  `STATISTICS = True`, sample 200 examples and assert: no ASCII `|` in
  problem / steps / answer (the shared checker); every `TABLE_LOOKUP` /
  `LOOKUP_SUPPLIED` value is a substring of the problem text; every decimal
  in the answer terminates; renderings parse under the oracle grammar; `Z`
  payload equals `final_answer`.
- DESIGN.md: "Statistics answers" convention block (§3 bullets). README
  coverage bullets get "data displays, sampling distributions, inference,
  study design, estimator theory" mentions per band.
- Re-band in `curriculum.py` (no code change): `ModeGenerator` middle d1,
  `RangeGenerator` middle d1, `MeanGenerator` middle d2, `MedianGenerator`
  middle d2 (§9).
- Op-code plan (reuse first): `STAT_SETUP, STAT_SUM, STAT_COUNT, STAT_DIVIDE,
  STAT_ORDER, SORT, MEDIAN_PICK, MEDIAN_PAIR, MEAN_DIV, DEV_ROW, QUARTILE,
  FREQ_SETUP, MODE, NORM_SETUP, ZSCORE, ZSCORE_FORMULA, RAW_FORMULA,
  TABLE_LOOKUP, LOOKUP_SUPPLIED, HT_SETUP, TEST_STAT_FORMULA, CI_SETUP,
  MOE_FORMULA, CI_FORMULA, CEIL, CHI_SETUP, CHI_FORMULA, EXP_CELL, CHI_TERM,
  REG_SETUP, REG_ROW, SUM, COUNT, NCR, POW, TERM, VAR_ROW, LOG_LIKELIHOOD,
  DERIVATIVE, SCORE_EQ, MLE_SETUP, MOM_SETUP, SAMPLE_MOMENT, MOM_EQUATION,
  BAYES_UPDATE_SETUP, POSTERIOR_PARAM, CHECK, TRY/REJECT/ACCEPT, REWRITE,
  FRAC_REDUCE, A/S/M/D/E/ROOT`. New codes are listed per generator; each has
  one meaning and is regenerated into `OPCODES.md` at the end of each phase.
  Two generic new codes are shared strand-wide: `PLOT_READ|feature|where|value`
  (reading one feature off a rendered display — a dot-plot row, a stem, a
  box-plot column) and `RULE|name|statement` (quoting the stated procedural
  rule before applying it: nearest-rank, 1.5×IQR, conservative df, 10%
  condition).

## 5. The curriculum

Format per entry: **Class** · band · difficulty — variants; problem;
procedure (op-codes); answer; oracle; capacity/backward construction;
supplied lookups; pitfalls. `⟲` marks an existing class being extended.

### Strand S1 — Data displays as text (elementary / middle)

**TallyFrequencyGenerator** · elementary · d1 — `raw_to_table`,
`tally_to_count`, `table_total`, `most_least`, `how_many_more`. Problem:
"Ms. Ortiz asked 10 students their favorite color: Red, Blue, Red, Green,
Blue, Red, Red, Green, Blue, Yellow. Make a frequency table." Steps:
`STAT_SETUP|Red, Blue, …`, one `TALLY_ROW|Red|////|4` per category
(alphabetical), `CHECK|split|4 + 3 + 2 + 1|10` against the count of raw
items. `tally_to_count` reads the rendered tally table (`Blue: ////\ //`)
with `TALLY_ROW|Blue|////\ //|7`. Answer: text list `Blue: 3; Green: 2;
Red: 4; Yellow: 1`, or an integer / category with count (`Red (4)`).
Oracle: recount the raw list; parse the tally strings. Capacity: category
banks × counts 1–12 × list length 8–20 × orders × 4 phrasings — unbounded.
Pitfall: the tally rendering is the only place a backslash appears in the
corpus; the conventions test checks the group-of-five string exactly.

**DotPlotGenerator** · elementary · d2 — `construct`, `read_count`,
`count_above_below`, `most_common`, `range_from_plot`, `total_from_plot`,
`median_from_plot`. Problem: the dot plot in §3 (scores 6,6,8,8,8,8,9,10,10)
and "How many students scored more than 7?" Steps: `PLOT_READ|row 8|●●●●|4`,
`PLOT_READ|row 9|●|1`, `PLOT_READ|row 10|●●|2`, `A|4|1|5`, `A|5|2|7`.
`construct` gives the raw list and answers the text list `6: 2; 7: 0; 8: 4;
9: 1; 10: 2` with one `DOT_ROW|value|count` per row (empty rows included).
`median_from_plot` expands counts to a sorted list (`SORT`), then
`MEDIAN_PICK` / `MEDIAN_PAIR` + `MEAN_DIV`. Answer: integer, text list, or
`8 (4 students)`. Oracle: parse the dot rows back to data. Capacity:
value ranges 1–30 × multiplicities × contexts × 4 phrasings — unbounded.
Pitfall: `total_from_plot` uses `M|8|4|32` per row then `A` — sums are
constructed ≤ 300.

**FractionLinePlotGenerator** · elementary · d3 — `count_at_least`,
`longest_minus_shortest`, `total_length`, `equal_share` (CCSS 4.MD.4 /
5.MD.2). Problem: a line plot of pencil lengths at 1/4-inch marks
(`1/4 ∣ ●`, `1/2 ∣ ● ●`, `3/4 ∣ ● ● ●`, `1 ∣ ● ●`); "What is the difference
between the longest and shortest pencil?" Steps: `PLOT_READ|longest|row 1|1`,
`PLOT_READ|shortest|row 1/4|1/4`, `L|1|1/4|4`, `C|1|4/4`, `S|4/4|1/4|3/4`
(existing fraction op-codes). `equal_share` = total ÷ count, constructed so
the quotient is exact in the plot's unit (`11/16 inch` allowed when the
problem says "as a fraction"). Answer: fraction with unit, `3/4 inch`;
mixed numbers per A0. Oracle: parse rows, `Fraction` arithmetic. Capacity:
units {1/2, 1/4, 1/8} × multiplicities × contexts (pencils, ribbons,
rainfall) × 4 phrasings — unbounded.

**StemAndLeafGenerator** · middle · d1 — `construct`, `list_values`,
`count_in_stem`, `median_from_plot`, `range_from_plot`, `decimal_key`,
`count_between`. Problem: the plot in §3 and "Find the median." Steps:
`LEAF_KEY|2 ∣ 3|23`, one `STEM_ROW|2|0 3 3|20, 23, 23` per stem (reading
leaves back to values), `SORT`, `MEDIAN_PICK|20|20`. `construct` takes the
raw list and answers `1: 2 5 7; 2: 0 3 3; 3: none; 4: 1` (`STEM_ROW|stem|
leaves` per row after `SORT`). Answer: integer, value list, or text list.
Oracle: parse stems + key; recompute. Capacity: 7–15 values in 10–99 or
0.0–9.9 × contexts × 4 phrasings — unbounded. Pitfall: leaves must be
ascending and empty stems kept; the oracle checks both on `construct`.

**PopulationSampleGenerator** · middle · d1 — `identify` (population /
sample / statistic), `parameter_vs_statistic`, `scale_up` (estimate a
population count from a sample proportion), `capture_recapture`
(`N ≈ M·C/R`, built so it divides). Problem: "A town has 8000 households. A
random sample of 200 households finds 45 with solar panels. Identify the
population and sample, and estimate how many households in the town have
solar panels." Steps: `LABEL|population|8000 households`, `LABEL|sample|200
households`, `D|45|200|0.225`, `M|0.225|8000|1800`. Answer: composite
`population: 8000 households; sample: 200 households; estimate: 1800`.
Oracle: regex the two counts and the proportion; recompute. Capacity:
context bank × sizes × 4 phrasings — unbounded. Pitfall: `45/200` must
terminate — n from {20, 25, 40, 50, 80, 100, 200, 250, 400, 500}.

**BoxPlotGenerator** · middle · d2 — `read_summary`, `iqr_from_plot`,
`percent_region` (what percent of the data lies between Q1 and max → 75%),
`shape` (composite from whisker/box asymmetry), `compare_two`,
`outliers_marked` (plot shows `o` marks; list them), `from_description`
(summary given as prose instead of a drawing — one of the phrasings).
Problem: the §3 plot and "Read the five-number summary." Steps:
`RULE|box plot|* = min/max, [ ] = Q1/Q3, : = median, 1 char per unit`,
`PLOT_READ|min|column 3|3`, `PLOT_READ|Q1|column 5|5`, … Answer: the
existing `min = 3, Q1 = 5, median = 8, Q3 = 12, max = 15` format; `shape`:
`right-skewed; right whisker 3 > left whisker 2` (rule stated: compare
whisker lengths, tie → compare box halves, tie → `symmetric`); `compare_two`:
`B; median 14 > 9` or `A; IQR 9 > 6` depending on the question. Oracle:
column-parse the ASCII plot into the five numbers; recompute. Capacity:
summaries on 0–40 scales × contexts × 5 phrasings — unbounded. Pitfall:
strict inequalities and integer positions are required for the drawing to be
unambiguous; the renderer asserts it.

**HistogramConstructGenerator** · middle · d2 — `bin_counts`,
`bin_of_value`, `count_between`, `shape` (composite: `right-skewed; peak in
0-9, tail to 30-39` by the stated rule "compare counts left vs right of the
modal bin"), `relative_bin` (fraction of data in a bin). Problem: "Times
(minutes): 3, 12, 17, 25, 8, 14, 21, 29, 11, 6. Using bins of width 10
starting at 0, give the count in each bin." Steps: `SORT`, one
`BIN_ASSIGN|12|10-19` per value, `BIN_COUNT|0-9|3` per bin, `CHECK|split|3 +
4 + 3|10`. Answer: `0-9: 3; 10-19: 4; 20-29: 3`. Oracle: rebin from the raw
list. Capacity: 8–16 values × widths {5, 10, 20} × starts × contexts × 4
phrasings — unbounded. Pitfall: values never land on a bin boundary
ambiguity because bins are inclusive integer ranges.

**ScatterPlotDescribeGenerator** · middle · d3 — `direction` (via the
quadrant-count rule: composite `positive; 6 of 6 points agree in sign`),
`stronger_of_two` (compare agreement fractions of two point sets, exact),
`identify_outlier` (largest abs residual from a supplied line), `no_association`
(agreement exactly half). Problem: "Points: (1, 3), (2, 5), (3, 4), (4, 8),
(5, 7), (6, 9). Using the means of x and y, count the points whose deviations
share a sign and describe the direction." Steps: `SUM`, `MEAN_DIV` for x̄ and
ȳ (constructed integers or `.5`), one `QUADRANT_ROW|(4, 8)|+,+|agree` per
point, `COUNT|agree|6/6`, `RULE|direction|majority agree → positive`.
Answer: composite as above; outlier variant `(5, 2); residual -6`. Oracle:
recompute. Capacity: 5–8 points × patterns × 4 phrasings — unbounded.
Pitfall: ties (a point exactly on a mean line) are excluded by construction.

**⟲ GraphInterpretGenerator** — add `double_bar` (two series per category,
rendered as two `GRAPH_DATA` lines; compare / total / largest gap) and
`construct_bar` (raw counts → the text bar list). Existing 17 variants
untouched.

### Strand S2 — Descriptive measures (middle / high)

**WeightedMeanGenerator** · middle · d2 — `weights`, `percent_weights`,
`frequency_table_mean`, `price_per_unit` (mixture / average cost),
`missing_weight` (find the weight that makes the mean a target). Problem:
"Homework counts 20%, quizzes 30%, the exam 50%. Scores: 90, 80, 70. Find
the weighted mean." Steps: `PERCENT_TO_DEC|20%|0.2` ×3, `WEIGHT_ROW|90|0.2|18`
per term, `A` chain, (`D` by Σw when weights are not percents). Answer:
`77`. Oracle: recompute with `Fraction`. Capacity: weights from
{2,3,4,5,10,20…} × scores × contexts × 4 phrasings — unbounded. Pitfall:
non-percent weights must sum to a divisor of the weighted total (backward:
choose the mean first).

**MeanAdjustmentGenerator** · middle · d3 — `needed_score`, `add_value`,
`remove_value`, `combined_groups`, `correction` (a value was misrecorded),
`outlier_effect` (mean vs median before/after adding a far value). Problem:
"After 4 tests Maya's mean is 82. What must she score on the fifth test to
have a mean of 85?" Steps: `M|85|5|425`, `M|82|4|328`, `S|425|328|97`,
`CHECK|substitute|(328 + 97)/5|85`. `combined_groups`: `M|20|70|1400`,
`M|30|80|2400`, `A`, `A|20|30|50`, `D|3800|50|76`. `outlier_effect`:
data 10, 12, 14, 16, 18 plus 50 → `mean 14 → 20; median 14 → 15`. Answer:
integer / decimal / composite. Oracle: recompute. Capacity: unbounded.
Pitfall: all targets chosen so the needed score is an integer in 0–100.

**AlternativeMeansGenerator** · high · d2 — `midrange`, `trimmed_mean`,
`harmonic_mean`, `geometric_mean_data`, `which_mean` (rates → harmonic,
growth factors → geometric; composite `harmonic; 48 mph`). Problem: "Find
the harmonic mean of 2, 3, 6." Steps: `RECIP_ROW|2|1/2`, `RECIP_ROW|3|1/3`,
`RECIP_ROW|6|1/6`, `A` chain with `L/C` to `1`, `D|3|1|3`. Geometric:
`M` chain to the product, `ROOT|∛64|4`. Trimmed: `RULE|trim 10% of 10|drop 1
low, 1 high`, `TRIM|3, 41|8 kept`, `SUM`, `MEAN_DIV`. Answer: number with
unit where natural. Oracle: recompute. Capacity: reciprocal sets built from
LCM families (`{2,3,6}`, `{3,4,6,12}`, `{4,5,20}`), perfect-power products,
trims on n ∈ {10, 20} — > 1000 with contexts and phrasings. Pitfall:
harmonic means are only generated when `n / Σ(1/x)` terminates or is asked
"as a fraction".

**GroupedDataGenerator** · high · d2 — `mean_from_midpoints`, `modal_class`,
`median_class`, `estimated_median` (interpolation formula stated in the
problem; constructed to terminate), `total_and_percent_in_class`. Problem:
"Class 0-9: 2, 10-19: 5, 20-29: 3. Estimate the mean using class midpoints."
Steps: `FREQ_SETUP`, `MID_ROW|0-9|4.5|9`, `MID_ROW|10-19|14.5|72.5`,
`MID_ROW|20-29|24.5|73.5`, `A` chain → 155, `STAT_COUNT|10`, `D|155|10|15.5`.
`median_class`: `CUM_ROW|0-9|2`, `CUM_ROW|10-19|7`, `RULE|median class|first
cumulative ≥ n/2 = 5`, answer `10-19; cumulative 7 ≥ 5`. Answer: decimal /
composite. Oracle: recompute. Capacity: 3–6 classes × widths × frequencies —
unbounded. Pitfall: Σf·m must have a 2^a5^b denominator after dividing by
Σf — choose Σf ∈ {4, 5, 8, 10, 16, 20, 25, 40, 50}.

**PercentileGenerator** · high · d2 — `percentile_rank`, `value_at_percentile`
(nearest-rank, rule stated), `quartiles_by_rank` (same rule, k = 25/75),
`between_percentiles` (count), `interpret` (composite: `above 80% of the
class; rank 17 of 20`). Problem: 20 values; "What is the percentile rank of
34?" Steps: `SORT`, `RULE|percentile rank|percent strictly below`,
`COUNT|below 34|13`, `PCT_RANK|13|20|65%`. `value_at_percentile`:
`RULE|nearest rank|position = ⌈k·n/100⌉`, `M|0.8|20|16`, `CEIL|16|16`,
`RANK_POS|16|value 41`. Answer: `65%` / integer / composite. Oracle:
recompute with the stated rule. Capacity: n ∈ {10, 20, 25, 40, 50} ×
values × k — unbounded. Pitfall: n divides 100·(count) so percents are
integers; ties at the target value excluded by construction.

**LinearTransformEffectGenerator** · high · d2 — `shift`, `scale`,
`affine`, `unit_conversion` (°C→°F, cm→in with factor supplied), `reverse`
(find k and c from old and new mean/sd), `which_change` (which statistics
change under a shift — composite `mean, median, min, max change; sd, IQR,
range unchanged`). Problem: "Scores have mean 25 and sd 6. Each score is
transformed by y = 2x − 5. Find the new mean and sd." Steps:
`LINEAR_EFFECT|mean|k·mean + c|2·25 - 5`, `M|2|25|50`, `S|50|5|45`,
`LINEAR_EFFECT|sd|abs(k)·sd|2·6`, `M|2|6|12`. Answer: composite `mean 45;
sd 12`. Oracle: closed form; also verify on a concrete 5-point data set the
test builds itself (identity check). Capacity: unbounded. Pitfall: negative
k flips nothing for sd but flips min/max — `which_change` handles it.

**TwoWayTableGenerator** · high · d2 — `marginal`, `joint_relative`,
`conditional_row`, `conditional_col`, `fill_missing_cell`, `association_check`
(compare two conditional percents; composite `associated; 60% vs 50%`).
Problem: the §3 table; "What percent of Grade 9 students said Yes?" Steps:
`MARGIN_ROW|Grade 9|12 + 8|20`, `COND_ROW|Yes given Grade 9|12/20|60%`.
Answer: `60%`, fraction, integer, or composite. Oracle: parse the table;
recompute. Capacity: 2×2, 2×3, 3×2, 3×3 with totals from {20, 25, 40, 50,
100, 200} × label banks × 4 phrasings — unbounded. Pitfall: row/column
totals chosen so every asked conditional percent is an integer or one
decimal. The probability framing of the same table (joint / conditional
probabilities as fractions, middle band) is `TwoWayTableProbabilityGenerator`
in `plans/probability_plan.md`; both stay.

**CovarianceCorrelationGenerator** · high · d3 — `sample_covariance`,
`population_covariance`, `r_from_summaries` (cov, sx, sy supplied),
`r_from_z_products` (z-scores supplied per point, `Σ z_x z_y / (n - 1)`),
`covariance_sign` (composite `negative; cov = -8`), `r_properties` (r after
a unit change → unchanged; composite `unchanged; r = 0.6`). Problem:
"x: 2, 4, 6, 8; y: 5, 5, 11, 11. Find the sample covariance." Steps:
`SUM`/`MEAN_DIV` ×2, `REG_ROW|x-x̄=-3|y-ȳ=-3|product=9` ×4, `SUM|…|24`,
`EVAL|n - 1|3`, `D|24|3|8`. `r_from_summaries`: `M|4|5|20`, `D|12|20|0.6`.
Answer: exact number. Oracle: recompute; for `r_from_summaries` also check
`abs(r) ≤ 1`. Capacity: x/y patterns from the library × means × phrasings —
unbounded. Pitfall: raw-data r is left to `RegressionGenerator` (its
perfect-square trick); here r only comes from supplied summaries or
z-products, so no radicals appear.

**⟲ StandardDeviationGenerator** — add `sample_std` (patterns with
`SS/(n-1)` a perfect square; `EVAL|n - 1|4`, `D|36|4|9`, `EVAL|s = √9|3`),
`shortcut_formula` (`σ² = Σx²/n - x̄²`, with `E` per value and a `CHECK`
against the deviation route), `from_frequency_table` (`x` with frequencies;
`WEIGHT_ROW` for f·x and f·(x-x̄)²), `coefficient_of_variation` (`CV_FORMULA|
σ/x̄ × 100%`, `D|4|20|0.2`, `DEC_TO_PERCENT|0.2|20%`; means from divisors of
100σ). Existing three variants untouched.

### Strand S3 — The normal model and the sampling bridge (high)

**EmpiricalRuleGenerator** · high · d1 — `percent_within`, `percent_tail`,
`interval_for_percent`, `count_of_n`, `percent_between_asymmetric` (μ−σ to
μ+2σ → 81.5%). Problem: "IQ scores are N(100, 15). Using the 68-95-99.7
rule, how many of 400 people score above 115?" Steps: `NORM_SETUP|X ~
N(100, 15)|P(X > 115)`, `ZSCORE|(115 - 100)/15|1`, `RULE_68_95|above μ + σ|
(100% - 68%)/2 = 16%`, `M|0.16|400|64`. Answer: `95%`, `64`, or interval
`(70, 130)`. Oracle: rule table + arithmetic. Capacity: contexts × μ, σ ×
N — unbounded. Pitfall: x is always exactly μ ± kσ for k ∈ {1, 2, 3}; the
rule's percents are the supplied constants (stated in the problem as "use
68%, 95%, 99.7%").

**InverseNormalGenerator** · high · d3 — `cutoff_above` (top 10%),
`cutoff_below`, `middle_interval` (middle 90% → ±1.645), `sigma_from_cutoff`,
`mu_from_cutoff`. Problem: "Scores are N(70, 8). What score separates the
top 10%? Selected z-scores: 80th percentile z = 0.84; 90th z = 1.28; 95th
z = 1.645; 99th z = 2.33." Steps: `NORM_SETUP|X ~ N(70, 8)|90th percentile`,
`LOOKUP_SUPPLIED|z for 90th|1.28`, `RAW_FORMULA|x = μ + z·σ`, `M|1.28|8|10.24`,
`A|70|10.24|80.24`. Answer: `80.24` or `(56.84, 83.16)`. Oracle: parse the
inline table; recompute. Capacity: percentile set {80, 90, 95, 97.5, 99}
× μ, σ × contexts × 4 phrasings — > 1000. Supplied: the percentile → z
rows with one decoy. Pitfall: `sigma_from_cutoff` divides by z — only
z ∈ {1.28, 1.6, 2.5, 0.8, 1.25} (terminating reciprocals) in that variant,
listed in its own inline table. (`NormalTableGenerator ⟲ inverse_lookup` in
`plans/probability_plan.md` reads the Φ table backwards instead; both stay.)

**SamplingDistributionEnumGenerator** · high · d3 — `list_means`,
`distribution_table`, `mean_of_xbar` (with `CHECK` = μ), `variance_of_xbar`
(with `CHECK` against `σ²/n · (N-n)/(N-1)` or `σ²/n`), `prob_event`
(`P(x̄ ≥ 6)`), `proportion_phat` (0/1 population; distribution of p̂).
Problem: "Population {2, 4, 6, 8}. List every sample of size 2 drawn without
replacement and give the sampling distribution of the sample mean." Steps:
`STAT_SETUP|population 2, 4, 6, 8|n = 2, without replacement`,
`SAMPLE_ENUM|{2, 4}|3`, … (6 rows), `DIST_ROW|3|1/6`, `DIST_ROW|4|1/6`,
`DIST_ROW|5|2/6 = 1/3`, `DIST_ROW|6|1/6`, `DIST_ROW|7|1/6`, `CHECK|split|
1/6 + 1/6 + 1/3 + 1/6 + 1/6|1`. Answer: text list `3: 1/6; 4: 1/6; 5: 1/3;
6: 1/6; 7: 1/6`; `mean_of_xbar`: composite `5; equals μ = 5`;
`variance_of_xbar`: `5/3; σ²/n · (N-n)/(N-1) = 5/2 · 2/3 = 5/3`. Oracle: full
enumeration by `itertools`, independent of the generator. Capacity:
populations of 3–5 distinct values in 1–20 × n ∈ {2, 3} × with/without ×
variants × 4 phrasings — > 1000 (20 samples max for N = 6, n = 3). Pitfall:
sample means are `.5` at worst (n = 2) or thirds (n = 3, rendered as
fractions); the answer uses `exact()`. This is the exact counterpart of the
probability strand's enumeration generators, and what `CLTProbability`
approximates.

**CLTProbabilityGenerator** · high · d3 — `se_mean`, `se_prop`,
`mean_sd_xbar`, `shape_and_center` (composite `approximately normal (n = 36 ≥
30); mean 50; SE 2`), `n_for_target_se`, `mean_above`, `mean_between`,
`prop_below`, `prob_proportion`, `unusual_sample_mean` (composite `unusual;
z = 2.5`). Problem: "Commute times have μ = 50, σ = 12. For samples of 36,
find P(x̄ > 53)." + Φ excerpt. Steps: `SE_FORMULA|σ/√n`, `ROOT|√36|6`,
`D|12|6|2`, `CLT_CHECK|n = 36 ≥ 30|approximately normal`, `ZSCORE|(53 -
50)/2|1.50`, `TABLE_LOOKUP|Φ(1.50)|0.9332`, `REWRITE|P(x̄ > 53) = 1 -
Φ(1.50)`, `S|1.0000|0.9332|0.0668`. Answer: `0.0668`, `2`, an integer n, or
composite. Oracle: parse Φ rows; recompute. Capacity: perfect-square n × σ ×
μ × z grid × contexts — unbounded. Supplied: Φ rows + decoys. Pitfall: z
must land on the table — `(c - μ)/SE` is constructed from a 2-decimal z
first (`c = μ + z·SE`); `p(1-p)/n` from the perfect-square table for the
proportion variants. This is the single sampling-distribution-of-x̄/p̂ class
for both strands.

**NormalApproxBinomialGenerator** — *cross-reference*. Specified once, in
`plans/probability_plan.md` (Strand T), with the perfect-square `npq` bank; its
`check_conditions` (`ok; np = 50 ≥ 10, n(1 − p) = 50 ≥ 10` / `fails; n(1 − p)
= 6 < 10`) and `mean_sd` variants are the statistics-facing ones. Counted in
the probability plan's totals; lands in probability Phase 3, before this
strand's Phase 3.

**PValueGenerator** · high · d4 — `right_tail`, `left_tail`, `two_sided`,
`decision_alpha` (composite `reject H0 (p = 0.0228 < 0.05)`), `from_prop_data`
(compute z first, as `HypothesisTestGenerator` does), `from_mean_data`
(σ known, perfect-square n), `compare_alphas` (reject at 0.05 but not 0.01 →
composite `reject at 0.05, fail at 0.01; p = 0.0228`). Problem: "A
right-tailed z-test gives z = 2.00. Find the p-value and decide at α = 0.05."
+ Φ excerpt. Steps: `HT_SETUP|Ha: p > p0|z = 2.00, α = 0.05`,
`PVALUE_RULE|right tail|p = 1 - Φ(z)`, `TABLE_LOOKUP|Φ(2.00)|0.9772`,
`S|1.0000|0.9772|0.0228`, `CHECK|p vs α|0.0228 < 0.05|reject H0`. Two-sided
adds `M|2|0.0228|0.0456`. Answer: `0.0228` or the composite verdict. Oracle:
parse; recompute. Capacity: z grid 0.5–3.4 × tails × α ∈ {0.10, 0.05, 0.02,
0.01} × data variants × contexts — unbounded. Supplied: Φ rows + decoys.

**InferenceSetupGenerator** · high · d1 — `state_hypotheses` (composite
`H0: μ = 500; Ha: μ < 500; left-tailed`), `parameter_identify` (`p; the
proportion of all voters who approve`), `type_I_II_describe` (`Type I;
concluding μ < 500 when μ = 500`), `np_condition`, `ten_percent_condition`,
`clt_condition`, `min_n_for_np` (smallest n with np ≥ 10 and n(1−p) ≥ 10 →
`CEIL`). Problem: "A bottler claims bottles hold 500 mL. An inspector
suspects the mean is less. Write the hypotheses and name the tail." Steps:
`HYP_STATE|H0: μ = 500|Ha: μ < 500|left-tailed`; numeric variants use
`RULE|10% condition|n ≤ N/10`, `M|0.15|40|6`, `CHECK|np ≥ 10|6 < 10|fails`.
Answer: composite. Oracle: template inversion (scenario built from a
(parameter, direction, value) triple; the test's keyword table maps
"less/fewer/decreased" → `<`, etc.) plus arithmetic. Capacity: scenario
bank (≥ 20 templates × 3 directions × values) × numeric ranges × 4
phrasings — > 1000.

### Strand S4 — Inference (high / college)

**TIntervalGenerator** · high · d4 — `mean_t_ci`, `mean_t_margin`,
`paired_from_data` (n ∈ {4, 16}: differences built from a sample-square
pattern), `paired_from_summary` (d̄, s_d given, n perfect square),
`paired_t_stat`, `pooled_t_stat`, `pooled_t_ci`. Problem: "n = 16, x̄ = 50,
s = 8. Using t* = 2.131 (df = 15), find the 95% confidence interval for μ."
Steps: `CI_SETUP|x̄ = 50, s = 8, n = 16|t* = 2.131 (df = 15)`, `MOE_FORMULA|
E = t*·s/√n`, `ROOT|√16|4`, `D|8|4|2`, `LOOKUP_SUPPLIED|t* (df = 15)|2.131`,
`M|2.131|2|4.262`, `CI_FORMULA|x̄ ± E`, `S`, `A`, `REWRITE|(45.738, 54.262)`.
Pooled: n1 = n2 = 8, s1 = 1, s2 = 7 → `M|7|1|7`, `M|7|49|343`, `A|7|343|350`,
`D|350|14|25`, `ROOT|√25|5`, `A|1/8|1/8|1/4`, `ROOT|√(1/4)|0.5`, `M|5|0.5|2.5`,
`S|x̄1|x̄2|6`, `D|6|2.5|2.4`, `CHECK|abs(t) vs t*|2.4 > 2.145|reject H0`.
Answer: interval / decimal / composite verdict `reject H0 (2.4 > 2.145)`.
Oracle: recompute. Capacity: n ∈ {4, 9, 16, 25, 100} × s × x̄ × t* bank
(df-indexed, 0.90/0.95/0.99) × contexts — unbounded. Supplied: t* with
df, always. Pitfall: paired n must be a perfect square or the summary
form is used; pooled pairs from the §3 list only.

**⟲ HypothesisTestGenerator** — add `one_sided_left`, `one_sided_right`
(decision rule `t < -crit` / `t > crit`, `Ha` printed, critical value from
the one-sided bank {1.28, 1.645, 2.33} labeled with α), `z_mean_stat`,
`z_mean_decision` (σ known, `SE = σ/√n`), and 3 more phrasings per variant
(word framings from the context bank). Existing four variants untouched.

**⟲ ConfidenceIntervalGenerator** — add `prop_ci` (the interval, p̂ from
the SE-square table: `p̂ = 0.2, n = 400 → SE 0.02`), `diff_means_ci`
(σ1, σ2 known with `σ1²/n1 + σ2²/n2` a perfect square from §3),
`diff_props_ci` (`(p̂1, n1, p̂2, n2)` found by a build-time table search over
n ≤ 2500 so that `p̂1q̂1/n1 + p̂2q̂2/n2` is a perfect-square rational — e.g.
(0.5, 200) and (0.5, 200) → SE 0.05; (0.2, 800) and (0.2, 800) → SE 0.02;
the found list is cached), `width_effect` (composite `wider; z* 1.96 → 2.576`
or `narrower; √n 10 → 20 halves E`). Existing five variants untouched.

**⟲ TwoSampleTestGenerator** — replace the hard-coded `n1 = n2 = 8, s1 =
s2 = 4` with draws from the §3 tables; add `t_pooled_stat`, `t_pooled_decision`
(df = n1 + n2 − 2 printed with the critical value), `t_welch_stat`
(`RULE|conservative df|min(n1 - 1, n2 - 1)`), `prop_z_unequal_n` (pooled
p̂ ∈ {0.2, 0.5, 0.8} and `(n1, n2)` from the `1/n1 + 1/n2` table, with
`x1 + x2 = p̂(n1 + n2)` enforced so the pooled proportion is exact — e.g.
(50, 50) with pooled 0.5 → SE = √(0.25 · 1/25) = 0.1; (20, 80) with pooled
0.2 → SE = √(0.16 · 1/16) = 0.1; the finite list is cached). Keeps the
original four variants as named cases.

**⟲ ChiSquareGenerator** — add `gof_nonuniform` (model proportions
`p_i` from {1/2, 1/4, 1/5, 1/10, 3/10, 2/5} with N ∈ {20, 40, 50, 100, 200}
so every `E = N·p_i` is an integer; observed = E + zero-sum pattern),
`expected_table` (r×c: answer the E table as a text list `r1c1: 6; r1c2: 9;
…`), `rxc_stat` / `rxc_decision` (2×3, 3×2, 3×3 with row and column totals
multiples of 10 and N = 100 so every E is an integer; observed = E plus a
zero-margin perturbation matrix), `homogeneity` (same arithmetic, "two
populations, same categories" framing; composite includes df:
`χ² = 5.2; df = 2; fail to reject H0 (5.2 ≤ 5.991)`), `df_from_shape`
(composite `df = 4; (3 - 1)(3 - 1)`). Critical values by df from the
existing `CRIT_BY_DF` plus α = 0.01 and 0.10 rows, always printed.

**TypeErrorPowerGenerator** · college · d3 — `critical_xbar` (cutoff
`μ0 + z*·SE`), `beta`, `power`, `alpha_from_cutoff` (given cutoff, α = 1 −
Φ(z), z supplied), `effect_of_n` (composite `power 0.9265 → 0.9772; SE 2 →
1`). Problem: "H0: μ = 50 vs Ha: μ > 50, σ = 10, n = 25, α = 0.02 (z* =
2.05). If the true mean is 57, find β and the power." + Φ excerpt with
`z=1.45: 0.9265`. Steps: `HT_SETUP|H0: μ = 50; Ha: μ > 50|σ = 10, n = 25,
z* = 2.05`, `ROOT|√25|5`, `D|10|5|2`, `CRIT_REGION|reject if x̄ > 50 +
2.05·2|54.1`, `M|2.05|2|4.1`, `A|50|4.1|54.1`, `POWER_FORMULA|β = P(x̄ ≤ 54.1
given μ = 57)`, `ZSCORE|(54.1 - 57)/2|-1.45`, `REWRITE|Φ(-1.45) = 1 -
Φ(1.45)`, `TABLE_LOOKUP|Φ(1.45)|0.9265`, `S|1.0000|0.9265|0.0735`,
`S|1.0000|0.0735|0.9265`. Answer: composite `β = 0.0735; power = 0.9265`.
Oracle: parse; recompute. Capacity: z* bank × SE ∈ {0.5, 1, 2, 4, 5, 10} ×
μ1 offsets filtered so `(cutoff - μ1)/SE` has ≤ 2 decimals × contexts × 4
phrasings — > 1000. Supplied: z* with its α, Φ rows (3-decimal z allowed) +
decoys. Pitfall: the filter, not rounding, keeps z on the table.

**ANOVAGenerator** · college · d4 — `group_means`, `ss_between`,
`ss_within`, `anova_table`, `f_stat`, `f_decision`, `df_only`. Problem:
"Three fertilizers, 4 plots each. Yields A: 8, 10, 10, 12; B: 12, 14, 14,
16; C: 16, 18, 18, 20. Complete the one-way ANOVA table and test at
α = 0.05 (F critical value = 4.26, df 2, 9)." Steps: `ANOVA_ROW|A|mean 10|
SS 8` ×3 (each preceded by its `SUM`/`MEAN_DIV` and `DEV_ROW`s), `MEAN_DIV|
42|3|14` (grand mean of group means, equal n), `SS_BETWEEN|4·((10-14)² +
(14-14)² + (18-14)²)|128`, `SS_WITHIN|8 + 8 + 8|24`, `CHECK|SST|SSB + SSW =
152|Σ(y - ȳ)² = 152`, `EVAL|df|2, 9`, `D|128|2|64`, `D|24|9|8/3`,
`F_FORMULA|F = MSB/MSW`, `D|64|8/3|24`, `CHECK|F vs critical|24 > 4.26|
reject H0`. Answer: `SSB = 128; SSW = 24; df = 2, 9; MSB = 64; MSW = 8/3;
F = 24` or composite verdict `reject H0 (24 > 4.26)`. Oracle: recompute
from raw data by the SST identity route. Capacity: k ∈ {3, 4} × n ∈ {3, 4,
5} × pattern library × group-mean spreads × contexts — unbounded. Supplied:
F critical with both df. Pitfall: MSW = SSW/(N − k) is often a fraction —
rendered with `exact()`; `f_stat` variants prefer constructions where
SSW is divisible by N − k (filter, 60% of draws).

**SlopeInferenceGenerator** · college · d4 — `se_slope` (from `s` and
`Sxx`), `t_stat` (H0: β = 0), `ci_slope` (t* with df = n − 2),
`decision`, `from_output` (a three-line "computer output" block: `Predictor
Coef SE Coef` — read `b` and `SE`, compute t), `sxx_from_data` (perfect-
square `Sxx` patterns: `(-2,-2,2,2) → 16`, `(-3,-3,0,3,3) → 36`,
`(-4,-1,-1,1,1,4) → 36`, `(-8,-2,-2,2,2,8) → 144`). Problem: "A regression
on n = 10 points gives slope b = 2.5, residual sd s = 4, Sxx = 25. Find
the 95% CI for the slope (t* = 2.306, df = 8)." Steps: `REG_SETUP|b = 2.5,
s = 4, Sxx = 25|CI for β`, `SE_FORMULA|SE_b = s/√Sxx`, `ROOT|√25|5`,
`D|4|5|0.8`, `LOOKUP_SUPPLIED|t* (df = 8)|2.306`, `M|2.306|0.8|1.8448`,
`S|2.5|1.8448|0.6552`, `A|2.5|1.8448|4.3448`, `REWRITE|(0.6552, 4.3448)`.
Answer: interval / decimal / composite `reject H0 (3.125 > 2.306)`.
Oracle: recompute. Capacity: b × s × Sxx squares × t* bank × contexts —
unbounded. Supplied: t* with df = n − 2. Pitfall: residual `s` is always
supplied, never derived (the residual SS is not square by construction).

**NonparametricTestGenerator** · college · d3 — `sign_test_pvalue`
(one-sided binomial tail with p = 1/2, exact dyadic fraction),
`sign_test_two_sided`, `sign_test_decision` (α given; composite `reject H0
(9/256 < 0.05)` with the fraction compared via `9/256 = 0.03515625`),
`permutation_pvalue` (n1 = n2 = 2 or 3: all 6 or 20 splits enumerated),
`bootstrap_percentile_ci` (a supplied list of 20 bootstrap statistics;
nearest-rank rule stated), `rank_sum_stat` (Wilcoxon W only, ties excluded).
Problem: "Before/after pairs give 7 positive and 1 negative difference.
Under H0 each sign is + with probability 1/2. Find the one-sided p-value
P(X ≥ 7)." Steps: `SIGN_ROW|pair 1|+3|+` ×8 (when raw pairs are given),
`COUNT|plus signs|7`, `BINOM_FORMULA|P(X ≥ 7) = C(8,7)/2^8 + C(8,8)/2^8`,
`NCR|C(8,7)|8`, `NCR|C(8,8)|1`, `POW|(1/2)^8|1/256`, `A|8/256|1/256|9/256`.
Permutation: `PERM_ROW|{5, 9} vs {2, 4}|7 - 3 = 4` ×6, `COUNT|diff ≥ 4|1 of
6`, answer `1/6`. Answer: reduced fraction, interval, integer, or composite.
Oracle: `math.comb` tail; `itertools.combinations` enumeration; nearest-rank.
Capacity: n ∈ 6–12 × sign counts × pair data × group values × 4 phrasings —
> 1000. Pitfall: sign-test n ≤ 12 keeps `2^n` hand-sized; permutation
group sizes ≤ 3.

**EmpiricalCDFGenerator** · college · d2 — `ecdf_value`, `ecdf_table`
(text list `2: 1/5; 3: 3/5; 7: 4/5; 9: 1`), `ecdf_quantile` (smallest x with
F̂(x) ≥ p), `jump_size`, `ks_distance_uniform` (`F0(x) = x/b` supplied;
composite `D = 0.3 at x = 3`). Problem: "Sample: 2, 3, 3, 7, 9. Evaluate
the empirical CDF at 5." Steps: `SORT`, `COUNT|values ≤ 5|3`, `ECDF_ROW|5|
3/5`. KS: `ECDF_ROW` per jump, `KS_ROW|x = 3|abs(3/5 - 0.3)|0.3` (both the
before-jump and at-jump gaps), `CHECK|max gap|0.3|at x = 3`. Answer:
fraction / text list / composite. Oracle: recompute; KS by brute force over
jump points. Capacity: n ∈ 4–8 × values × b — unbounded. Pitfall: `x/b`
with b ∈ {10, 20, 50} so gaps terminate; ties in the max gap broken by
"smallest x", stated.

### Strand S5 — Study design (high)

**StudyDesignGenerator** · high · d1 — `sampling_method` (SRS, stratified,
cluster, systematic, convenience, voluntary response; composite
`stratified; groups = grade level`), `bias_identify` (undercoverage,
nonresponse, voluntary response, leading question, convenience; composite
`voluntary response; only viewers who chose to call in`), `experiment_vs_
observational` (`experiment; the researcher assigned the diets`),
`design_elements` (`explanatory: fertilizer; response: yield; units: 24
plots`), `systematic_select` (list the selected IDs: `N = 60, every 5th
from 3 → 3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58`), `stratified_allocate`
(proportional counts: `freshmen 30; sophomores 20`), `random_digit_select`
(supplied digit line, two-digit labels 01–40, choose 3: `DIGIT_PICK|81|
reject|> 40`, `DIGIT_PICK|02|accept`, `DIGIT_PICK|02|reject|repeat` … answer
`02, 27, 10`). Steps for label variants: `DESIGN_CUE|"from each grade"|
stratified`, `LABEL|groups|grade level`. Answer: composite / list. Oracle:
label variants by the test's own keyword→label table over the scenario
grammar (≥ 6 templates per label × subject/setting banks); numeric variants
recomputed. Capacity: templates × banks × numbers × 4 phrasings — > 1000.
Pitfall: every scenario template must contain exactly one cue phrase, and
the cue bank is disjoint across labels (a unit test asserts it).

### Strand S6 — Estimator theory (graduate)

**EstimatorBiasEnumGenerator** · graduate · d3 — `variance_n_bias`,
`variance_n_minus_1_unbiased`, `mean_unbiased`, `max_estimator_bias`
(population {1..N}, n = 2, estimator = sample max), `range_estimator`
(E[max − min] vs σ), `without_replacement` (same as above with the finite-
population correction visible). Problem: "Population {1, 2, 6}. For samples
of size 2 with replacement, compute E[σ̂²] where σ̂² = Σ(x − x̄)²/n, compare
with σ², and state the bias." Steps: `SUM`/`MEAN_DIV|9|3|3`, `DEV_ROW` ×3,
`D|14|3|14/3` (σ²), `SAMPLE_ENUM|(1, 2)|x̄ = 1.5, σ̂² = 0.25` ×9, `SUM|0 + 0.25
+ 6.25 + 0.25 + 0 + 4 + 6.25 + 4 + 0|21`, `D|21|9|7/3`, `BIAS|E[σ̂²] = 7/3|
σ² = 14/3|-7/3`, `CHECK|identity|σ²·(n-1)/n|14/3 · 1/2 = 7/3`. Answer:
composite `E[σ̂²] = 7/3; σ² = 14/3; bias = -7/3`; the n − 1 variant ends
`E[s²] = 14/3; σ² = 14/3; bias = 0 (unbiased)`. Oracle: enumeration via
`itertools.product` / `combinations`, exact `Fraction`. Capacity:
populations of 3–4 values in 1–12 × n = 2 (or 3 for N = 3) × replacement ×
variants × 3 phrasings — > 1000. Pitfall: 9 or 16 enumerated rows is the
ceiling; populations of 5 only with n = 2 without replacement (10 rows).

**MSEDecompositionGenerator** · graduate · d3 — `mse_from_parts`,
`mse_scaled_mean` (T = c·x̄), `compare_two` (composite `T2; MSE 41/10 <
164/25`), `optimal_shrinkage` (c* = μ²/(μ² + σ²/n)), `enumerated_mse`
(sample max for N, from the enumeration above). Problem: "x̄ is the mean of
n = 5 observations with μ = 10, σ² = 20. For T = (4/5)·x̄, find the bias,
variance, and MSE." Steps: `BIAS|E[T] = (4/5)·10 = 8|θ = 10|-2`,
`M|16/25|4|64/25` (Var(x̄) = σ²/n = 4), `MSE_DECOMP|MSE = Var + bias²`,
`E|-2|2|4`, `A|64/25|4|164/25`. Answer: composite `bias = -2; Var = 64/25;
MSE = 164/25`. Oracle: closed forms with `Fraction`; `enumerated_mse`
cross-checked by enumeration. Capacity: c, μ, σ², n grids × contexts —
unbounded.

**FisherInformationGenerator** · graduate · d4 — `bernoulli`, `poisson`,
`exponential`, `normal_mu`, `geometric`, `crlb_check` (composite `CRLB =
3/320; Var(p̂) = 3/320; attains the bound`). Problem: "For n = 20 Bernoulli(p)
observations with p = 1/4, compute the Fisher information I_n(p) and the
Cramér–Rao lower bound for unbiased estimators of p." Steps: `LOG_LIKELIHOOD|
ell(p) = x log p + (1-x) log(1-p)`, `DERIVATIVE|score = x/p - (1-x)/(1-p)`,
`DERIVATIVE|second = -x/p² - (1-x)/(1-p)²`, `FISHER_INFO|I(p) = -E[second]
= 1/p + 1/(1-p)`, `A|4|4/3|16/3`, `M|20|16/3|320/3`, `CRLB|1/I_n|3/320`.
Answer: composite `I(p) = 16/3; I_n(p) = 320/3; CRLB = 3/320`. Oracle: the
independent route `E[(ℓ')²]` — for Bernoulli enumerate x ∈ {0, 1}; for
Poisson use `Var(X)/λ²`; identity routes per family in `stats_oracle.py`,
exact `Fraction`. Capacity: rational parameters × n × families × 3
phrasings — > 1000. Pitfall: parameters are rationals with small
denominators so `1/(p(1-p))` stays a short fraction.

**SufficiencyFactorizationGenerator** · graduate · d3 — `identify_T`,
`factor_and_evaluate`, `uniform_max` (T = max, indicator factor),
`two_dimensional` (normal, both unknown: `(Σx, Σx²)` evaluated),
`ratio_check` (two samples with equal T: likelihood ratio free of θ →
composite `ratio = 1; T(x) = T(y) = 7`). Problem: "Poisson(λ) sample 2, 0,
3, 1. Write the joint pmf, factor it as g(T, λ)·h(x), and evaluate T."
Steps: `LOG_LIKELIHOOD|joint = λ^Σx e^(-nλ) / Π x_i!`, `LIKELIHOOD_FACTOR|g(T, λ) =
λ^T e^(-4λ)|h(x) = 1/(2!·0!·3!·1!)`, `SUM|2 + 0 + 3 + 1|6`, `M` chain for
the factorial product `12`, `SUFFICIENT|T = Σx_i|6`. Answer: composite
`T = Σx_i = 6; g = λ^6 e^(-4λ); h = 1/12`. Oracle: family→T table (written
independently in the oracle) + numeric evaluation of T on the parsed data;
`h` recomputed. Capacity: 7 families × data × 3 phrasings — > 1000.
Pitfall: normal `h` involves `(2π)^(-n/2)`, kept symbolic as `(2πσ²)^(-n/2)`
inside the g/h strings; only T is numeric.

**LikelihoodRatioTestGenerator** · graduate · d4 — `np_ratio_bernoulli`
(Λ = L(p0)/L(p1) as an exact fraction, n ≤ 6), `np_region` (reject when
S ≥ c; find c for α from the dyadic tail with p0 = 1/2; composite `c = 5;
α = 7/64`), `np_power` (P(S ≥ c under p1), exact fraction), `wilks_normal`
(σ known: `-2 ln Λ = n(x̄ - μ0)²/σ²`, χ²(1) critical supplied; composite
`-2 ln Λ = 4; reject H0 (4 > 3.841)`), `wilks_df` (df = difference in free
parameters; composite `df = 2; 3 - 1`). Problem: "σ = 2, n = 4, x̄ = 12.
Test H0: μ = 10 against the unrestricted alternative with the likelihood
ratio test; χ² critical value = 3.841 (df = 1)." Steps: `LR_FORMULA|-2 ln Λ
= n(x̄ - μ0)²/σ²`, `S|12|10|2`, `E|2|2|4`, `M|4|4|16`, `E|2|2|4`, `D|16|4|4`,
`CHECK|-2 ln Λ vs χ²|4 > 3.841|reject H0`. Answer: composite / fraction.
Oracle: binomial enumeration; closed form. Capacity: data × parameters ×
5 variants × 3 phrasings — > 1000. Supplied: χ² critical with df.
Pitfall: Wilks for Bernoulli/Poisson needs logs — deliberately excluded
(left to the exact-fraction Neyman–Pearson forms).

**DiscretePosteriorGenerator** · graduate · d3 — `posterior_table`,
`map`, `posterior_mean`, `posterior_predictive` (P(next success) =
Σ θ·post(θ)), `credible_set` (smallest set of grid points, by descending
posterior, reaching ≥ 0.9; composite `{0.5, 0.8}; mass 1649/1713`), `bayes_
factor` (ratio of likelihoods at two grid points). Problem: "Prior on θ:
P(0.2) = P(0.5) = P(0.8) = 1/3. Observe 3 successes in 4 trials. Find the
posterior and the MAP." Steps: `BAYES_UPDATE_SETUP|grid 0.2, 0.5, 0.8|
prior 1/3 each; data 3 of 4`, `BAYES_ROW|0.2|1/3 · 0.008 · 0.8|0.0064/3`,
`BAYES_ROW|0.5|1/3 · 0.125 · 0.5|0.0625/3`, `BAYES_ROW|0.8|1/3 · 0.512 ·
0.2|0.1024/3`, `SUM|…|0.1713/3`, `D|0.1024|0.1713|1024/1713` (per row),
`CHECK|split|64/1713 + 625/1713 + 1024/1713|1`, `RULE|MAP|largest
posterior`. Answer: `0.2: 64/1713; 0.5: 625/1713; 0.8: 1024/1713` /
composite `MAP θ = 0.8; posterior 1024/1713`. Oracle: recompute with
`Fraction`. Capacity: grids of 3–4 points from {0.1, …, 0.9} × priors
(uniform or dyadic) × (successes, trials ≤ 6) × 4 phrasings — > 1000.
Pitfall: all arithmetic is in `Fraction`; only the final rendering uses
`exact()`.

**⟲ MLEGenerator** — add `normal_sigma2` (deviation-pattern data, μ
unknown too: σ̂² = SS/n integer), `poisson` (λ̂ = x̄), `uniform_theta`
(θ̂ = max with `CHECK|likelihood decreasing in θ|θ ≥ max` and the composite
`theta_hat = max = 9; score equation has no root`), `geometric` (p̂ = 1/x̄),
`binomial_n_known`. **⟲ MethodOfMomentsGenerator** — add `normal_two_param`
(μ̂ = x̄, σ̂² = m2 − x̄² with `SAMPLE_MOMENT` for m2), `gamma_two_param`
(α̂ = x̄²/(m2 − x̄²), β̂ = x̄/(m2 − x̄²) — exact fractions), `uniform_a_b`
(data built so `3(m2 − x̄²)` is a perfect square: patterns
`(-2,-2,-1,1,2,2) → m2 = 3`, `(-4,-4,-2,2,4,4) → 12`). **⟲
BayesianUpdateGenerator** — add `gamma_poisson` (rate parameterization
stated; `posterior=Gamma(9,4); posterior_mean=9/4`), `beta_map`
(`(a-1)/(a+b-2)`), `beta_predictive` (`a'/(a'+b')`), `normal_predictive_mean`
(= posterior mean; composite with posterior variance + σ²).

### Critic records for the strand (optional close-out)

**StatisticsCriticGenerator** · college · d3 — `deviation_table_error`
(one `DEV_ROW` squared wrongly, propagated into SS, variance, sd),
`z_lookup_error` (wrong table row read), `chi_term_error`, `missing_step`
(one line of a mean / sd / CI computation blanked). Same record shapes as
`ErrorSpottingGenerator` / `FillInStepGenerator`: `VERIFY|k|ok`, `FLAG|k|
<true arithmetic>`, redo, `Z|step k; <correct answer>`. Built on the
strand's own generators. Not counted in the totals below.

## 6. Band and difficulty summary

| Band | New classes | Extended / re-banded |
|---|---:|---|
| elementary | 3 (TallyFrequency d1, DotPlot d2, FractionLinePlot d3) | GraphInterpret (+2 variants) |
| middle | 7 (StemAndLeaf d1, PopulationSample d1, BoxPlot d2, HistogramConstruct d2, WeightedMean d2, MeanAdjustment d3, ScatterPlotDescribe d3) | StandardDeviation (+4); Mode/Range → d1, Mean/Median → d2 |
| high | 14 (EmpiricalRule d1, InferenceSetup d1, StudyDesign d1, AlternativeMeans d2, GroupedData d2, Percentile d2, LinearTransformEffect d2, TwoWayTable d2, CovarianceCorrelation d3, InverseNormal d3, SamplingDistributionEnum d3, CLTProbability d3, PValue d4, TInterval d4) | HypothesisTest (+4), ConfidenceInterval (+4), TwoSampleTest (+4, de-hard-coded), ChiSquare (+6) |
| college | 5 (EmpiricalCDF d2, TypeErrorPower d3, NonparametricTest d3, ANOVA d4, SlopeInference d4) | — |
| graduate | 6 (EstimatorBiasEnum d3, MSEDecomposition d3, SufficiencyFactorization d3, DiscretePosterior d3, FisherInformation d4, LikelihoodRatioTest d4) | MLE (+5), MethodOfMoments (+3), BayesianUpdate (+4) |

Total: **35 new generator classes, 9 extended, 4 re-banded**, roughly 185
operation variants (`NormalApproxBinomialGenerator` is counted in
`plans/probability_plan.md`). Difficulty histogram for statistics classes, before
→ after: middle `d1: 0 → 3, d2: 0 → 6, d3: 5 → 7, d4: 2 → 2`; high
`d1: 0 → 3, d2: 0 → 5, d3: 0 → 4, d4: 2 → 4, d5: 5 → 5`. The catalog moves
from 36 → 39 elementary and 64 → 71 middle skills, which nudges the
equal-per-skill mix toward the recipe in `plans/dataset_plan.md`.

## 7. Delivery order

One generator per commit (`add dot plot generator`), tests in the same
commit, docs regenerated at the end of each phase. Each phase ends with:
`uv run python -m unittest discover tests`, the capacity probe on the new
classes, a 200-example seeded build per class with zero errors, and
`OPCODES.md` / `PROBLEM_TYPES.md` regeneration with `--check` passing.
Phase 0 requires the probability strand's Phase 0 (`prob_common.py`);
Phase 3 requires probability Phase 3 (`NormalApproxBinomialGenerator`);
otherwise the strands interleave freely.

| Phase | Deliverable | Why this order |
|---|---|---|
| 0 | `stats_common.py`, `tests/stats_oracle.py`, conventions test with the supplied-lookup assertion, DESIGN.md block, re-band Mean/Median/Mode/Range | every later generator renders, parses, and looks up the same way |
| 1 | TallyFrequency, DotPlot, FractionLinePlot, StemAndLeaf, PopulationSample, BoxPlot, HistogramConstruct, GraphInterpret extension | cheapest, fills the thinnest bands, proves the text renderers and their parsers before anything depends on them |
| 2 | WeightedMean, MeanAdjustment, AlternativeMeans, GroupedData, Percentile, LinearTransformEffect, ScatterPlotDescribe, TwoWayTable, CovarianceCorrelation, StandardDeviation extension | descriptive measures; exercises the pattern library end to end |
| 3 | EmpiricalRule, InverseNormal, SamplingDistributionEnum, CLTProbability, PValue, InferenceSetup (NormalApproxBinomial lands from probability Phase 3) | the normal model and the probability → inference bridge; validates Φ-table supply and the mechanical lookup test |
| 4 | TInterval, HypothesisTest / ConfidenceInterval / TwoSampleTest / ChiSquare extensions, TypeErrorPower, ANOVA, SlopeInference, NonparametricTest, EmpiricalCDF | inference gaps; all critical-value banks in place |
| 5 | StudyDesign | scenario grammar + keyword oracle; independent of numerics |
| 6 | EstimatorBiasEnum, MSEDecomposition, FisherInformation, SufficiencyFactorization, LikelihoodRatioTest, DiscretePosterior, MLE / MethodOfMoments / BayesianUpdate extensions | graduate estimator theory; reuses the enumeration oracle from Phase 3 |
| 7 | StatisticsCriticGenerator (optional); phrasing sweep to 3–5 templates on the ten existing statistics classes (the `TODO.md` sweep item); full capacity probe; README inventory/coverage update; regenerate `PROBLEM_TYPES.md`, `OPCODES.md`; note the strand in the HF dataset card | close-out |

Definition of done per generator (checklist copied into each PR):
- [ ] class in `generators/`, registered in `quixi_math_datagen.py` import +
      `ALL_GENERATORS` + `curriculum.CURRICULUM`
- [ ] module-level `STATISTICS = True` so the conventions test picks it up
- [ ] docstring lists variants, op-codes, and the exactness construction;
      new op-codes have one meaning
- [ ] 3–5 problem phrasings; the oracle parses all of them
- [ ] every lookup value in a `TABLE_LOOKUP` / `LOOKUP_SUPPLIED` step
      appears verbatim in the problem text (df printed with t / χ² / F)
- [ ] test file mirrors the class name: contract, 500-sample oracle from
      problem text by an independent route, step-arithmetic check on
      `A/S/M/D/E/ROOT/CHECK`, all variants reachable, invalid variant,
      pipe safety, both outcomes occur for every verdict variant
- [ ] composite answer wherever the bare verdict is a coin flip or label
- [ ] `probe_generator_capacity.py --threshold 1000` passes or the small
      space is documented in the docstring
- [ ] seeded 200-example build: zero errors, duplicate rate noted

## 8. Out of scope, and why

No exact hand procedure ⇒ no generator: judging scatter "strength" by eye
(the quadrant rule and r stand in), normality assessment from a histogram,
Welch–Satterthwaite df (the conservative rule stands in), exact t / χ² / F
tail probabilities (critical values are supplied instead), continuous
credible intervals (Beta/Gamma quantiles; the discrete-grid posterior stands
in), Wilks tests needing logarithms for Bernoulli/Poisson, bootstrap
*generation* (only percentile reading of a supplied list), multiple
regression, non-conjugate Bayes, asymptotic normality of the MLE as a
statement, and free-form "interpret in context" essays beyond the
templated composite answers in `InferenceSetupGenerator`.

## 9. Decisions taken in this plan (change here, not per generator)

- One rendering per display type (§3), fixed forever: dot plots and
  stem-and-leaf use `∣` (U+2223) and `●`; box plots use the 7-character
  prefix, `+` ticks every 5 units, one character per unit, `* [ : ] o`;
  tallies use `////\`; histograms are inclusive integer bins.
- Text-list answers (`key: value; …`, ascending keys) for anything
  table-shaped; composite verdicts `label; fact`; the existing
  `reject H0 (4.4 > 2.576)` form is kept for critical-value tests and
  `reject H0 (p = 0.0228 < 0.05)` is its p-value twin.
- Φ values always come from an inline excerpt with two decoy rows, at the
  exact z the procedure produces (2 or 3 decimals); negative z via a
  `REWRITE` symmetry step; all other constants inline with df. Enforced by
  test, not by convention.
- Rule-dependent statistics (percentile method, median class, trimmed
  mean, box-plot shape, bootstrap interval, Welch df) state their rule in
  the problem with a `RULE` step quoting it.
- Exactness is by construction (pattern library, perfect-square SE
  tables), never by rounding; `exact()` renders fractions when a value does
  not terminate and the problem says "exact".
- `MeanGenerator` / `MedianGenerator` re-banded to middle d2 and
  `ModeGenerator` / `RangeGenerator` to middle d1; `TwoSampleTestGenerator`
  loses its hard-coded sizes but keeps its four original variants as named
  cases for continuity.
- Cross-strand ownership (mirrored in `plans/probability_plan.md` §10):
  `prob_common.py` owns `exact()`, `p4`, `pct`, `money`, `phi_table()` and
  the `(n, p)` bank, and `stats_common.py` imports them (`NormalTableGenerator`
  calls the shared `phi_table()` byte-identically); `stats_common.py`
  absorbs the running-sum helper the statistics generators duplicate; the
  sampling distribution of x̄/p̂ and CLT probabilities are specified here
  (once) and `NormalApproxBinomialGenerator` in the probability plan
  (once); `TwoWayTable` (percents, high) and `TwoWayTableProbability`
  (fractions, middle) both stay; `InverseNormal` (percentile table) and
  `NormalTable ⟲ inverse_lookup` (Φ table read backwards) both stay;
  conditioning is `P(A given B)` everywhere; the three conventions tests
  share one ASCII-bar checker, and a class may carry more than one of the
  `FOUNDATIONS` / `PROBABILITY` / `STATISTICS` flags.

# Applied Reasoning and Intuition Curriculum Plan

The fourth plan. `plans/foundations_plan.md`, `plans/probability_plan.md`, and
`plans/statistics_plan.md` complete the *procedure atlas*: every named method,
executed exactly, with a visible scratchpad. This plan builds the other half
of mathematical competence — the half that decides **what the problem is**,
**builds the model**, **senses what the answer should look like**, and
**knows when a method does not apply**. It is the plan most directly aimed at
the dataset's purpose: real-world problem solving and genuine mathematical
intuition.

The bar is unchanged (`AGENTS.md`, `TODO.md`): exact arithmetic only,
human-like steps, pipe-safe fields, A0 answer conventions, an A9 oracle test
that recomputes the answer from the problem text alone by an independent
route, capacity > 1000 distinct problems per class, one class per skill
registered in three places, `PROBLEM_TYPES.md` / `OPCODES.md` regenerated.
One rule is *added* for this strand and enforced by test: **the problem
text names no method** (§3).

## 1. What "real-world problem solving and intuition" means here

Procedural fluency is what the rest of the catalog teaches. This plan targets
the five things a person with mathematical intuition does that a
procedure-follower does not, in the order they are learned:

| Capability | What the model must do | Plan strand |
|---|---|---|
| **Model** | read a situation, choose the quantities and the relation between them, write the equation, solve, report with units | M. Modeling word problems |
| **Sense magnitude** | estimate before computing, compare without computing, respect precision and measurement error | N. Number sense and measurement |
| **Judge** | notice missing or irrelevant data, tell look-alike methods apart, check that a method's assumptions hold, reason about direction and dominance without full computation, reject implausible answers | J. Judgment |
| **Read numbers in the world** | base rates and risk, indices and growth, paradoxes of aggregation, misleading displays, expected-value decisions | L. Quantitative literacy |
| **Connect representations and reasons** | words ↔ equations ↔ tables ↔ graph features; derive the formulas rather than recall them; reason about scale and space | R. Representations, D. Derivations, G. Spatial intuition |
| **Compose** | carry meaning through a multi-part scenario that chains several skills | X. Scenarios |

Everything is still finished by a deterministic pencil-and-paper procedure
with an exact answer. What changes is the *input*: the procedure is not
named, the data may be noisy or incomplete, and the answer often carries a
verdict with the number that earns it.

## 2. Current coverage and gaps

Already in the registry (keep; extend where marked ⟲):

| Class | Band | Covers | Gap |
|---|---|---|---|
| `PercentWordProblemGenerator` | elem d3 | percent change / markup / discount / tax, 1 step; `distractor=True` adds one irrelevant number and a `SELECT_RELEVANT` step | single-step only; the distractor pattern exists nowhere else |
| `ProportionWordProblemGenerator` | elem d3 | one proportion | no scale drawings, maps, recipes |
| `UnitRateGenerator`, `UnitRateFromTableGenerator` | middle d3 | unit rates | no best-buy comparison |
| `PythagoreanWordProblemGenerator`, `SimilarFiguresScaleGenerator` | middle | one geometric relation in context | — |
| `FinanceGenerator`, `AnnuityGenerator` | middle / college | simple & compound interest, annuities | no budgets, payroll, unit price, plan comparison, depreciation, inflation |
| `ExponentialModelGenerator` | high d4 | growth / decay / half-life / continuous, method stated | no linear-vs-exponential comparison, doubling by rule of 70 |
| `FermiEstimationGenerator` | high d4 | three fixed contexts, 2-s.f. answers with `ESTIMATE_CHECK` | thin; the only estimation skill above elementary |
| `CompositeArithmeticGenerator` | elem d4 | three fixed multi-step arithmetic shapes | the only composition of skills in the catalog |
| `RelatedRatesGenerator`, `OptimizationGenerator` | high | calculus applications, method stated | — |
| `PermutationCombinationGenerator` (`word`), `TipBillSplitGenerator`, `TaxicabGeometryGenerator` | middle | one word-problem variant each | — |
| `ErrorSpottingGenerator`, `FillInStepGenerator` | high | critic records on two skills | no plausibility judgment, no missing-information records |
| `ESTIMATE` / `ESTIMATE_CHECK` op-codes | — | used by 3 generators | not a habit across the catalog |
| `ScalingGenerator`, `ScalingLawGenerator`, `CrossSectionGenerator`, `NetsSurfaceAreaGenerator` | mixed | physics/ML scaling, solids | no square–cube law in context, no packing, no clock angles / bearings |

Six of ~510 operations carry a word-problem framing. Absent entirely:
work/rate, mixture, motion, age/coin/consecutive-integer puzzles, linear
cost models and break-even, plan comparison, percent chains and reverse
percents, budgets/payroll/best-buy, geometry in context (fencing, tiling,
packaging), systems and quadratics from stories, linear-vs-exponential
reasoning, mental-math strategies, magnitude comparison, significant figures,
measurement uncertainty and tolerances, rounding effects, plausibility
critique, missing-information problems, method discrimination, assumption
checking, qualitative/limiting reasoning, relative vs absolute risk,
Simpson's paradox, regression to the mean, index numbers and CAGR, decision
under uncertainty, representation translation, formula derivation,
square–cube law in context, packing, clock angles and bearings, and any
multi-part scenario above elementary.

## 3. Strand-wide rules (in addition to AGENTS.md)

**No method words (the defining rule).** The problem text of every generator
in this plan names no procedure, formula, theorem, or skill: no "use the
quadratic formula", "apply the work formula", "set up a proportion", "by
Bayes", "find the LCM", no generator or variant names. The situation and the
question are all the model gets. `tests/test_applied_conventions.py` scans
problem text against a banned-phrase list (`applied_common.METHOD_WORDS`) and
fails on any hit. A `scaffolded` variant modifier may name the method for
curriculum-learning purposes and is exempt; it is never the default.

**Four standard variant modifiers** exist on every modeling class (Strand M,
X, and the applied parts of G/L), combinable with the class's own variants:
- `plain` — clean data, numeric answer with unit.
- `distractor` — one or two irrelevant numbers in the story; the first step
  is `SELECT_RELEVANT|used: 6 h, 3 h|ignored: $40 wage` (the existing
  `PercentWordProblem` pattern). Answer unchanged.
- `estimate_first` — steps open with `ESTIMATE|<rounding work>|<estimate>`
  and close with `ESTIMATE_CHECK|<estimate>|<exact>|<verdict>` before `Z`
  (the existing DESIGN.md format; the estimate uses leading-digit rounding so
  it is deterministic). Answer unchanged.
- `with_model` — the answer is composite: the model equation in the
  template's canonical form, then the value: `1/6 + 1/3 = 1/t; t = 2 hours`.
  This is how "did it set up the right model" becomes gradable.

**Answer conventions (extend A0).**
- Quantities carry units: `2 hours`, `48 km/h`, `112 m²`, `53 tiles`; money
  as `$712.50` (existing money format, no thousands separators). Percents
  `40%`; percentage points `10 percentage points`.
- Composite verdicts `label; fact` as in the other plans: `plan B; $420 vs
  $455`, `implausible; correct 80 km/h`, `does not apply; fixed $3 fee makes
  cost non-proportional; correct $23`, `A: combination, 10; B: permutation,
  60`.
- **Missing information** has one canonical form: `insufficient
  information; need <slot name>` where the slot name is the template's
  human phrase (`the price of a notebook`, `the speed of the second train`).
- Equations in `with_model` answers use the template's fixed variable letter
  (`t` time, `h` hours, `x` count/unknown, `w` width, `p` price) and the
  template's canonical arrangement; the oracle inverts the template rather
  than parsing free-form algebra.
- Model verdict labels are drawn from fixed vocabularies per class
  (`proportional / not proportional`, `linear / exponential`, `combination /
  permutation`, `plausible / implausible`), always paired with a number.

**Realistic but hand-friendly numbers.** Prices in cents that divide well,
rates that make LCM arithmetic short, speeds/distances producing integer or
`.5` times, percents from {5, 10, 12.5, 15, 20, 25, 30, 40, 50, 75}. Every
class constructs backward from the exact answer, as the rest of the repo
does. Story numbers never need a calculator; the procedure is the hard part.

**Determinism.** Where a story admits several correct models (motion via
distance-equality or via closing speed), the *answer* is the same and the
scratchpad follows the template's canonical route. Where the answer is a
choice (plan A vs B; which box orientation), ties are excluded by
construction. Rejected roots and rejected orientations are shown with
`REJECT|t = -1|negative time`.

**Pipe safety.** ASCII `|` banned in problem text, steps, and answers
(shared checker from the other three conventions tests). Absolute values as
`abs()`; "per" as `/` or the word.

**Phrasing is the skill here.** Minimum **5** templates per class (not 3),
across at least three surface contexts, and the same numbers must appear in
different sentence orders (quantity-first, question-first, data-in-a-table).
The oracle inverts every template. Contexts come from one shared bank
(`applied_common.CONTEXTS`: people, shops, trips, workshops, gardens,
recipes, classrooms, sports, small businesses, labs) with units.

**Oracles (A9).** Template inversion (the test knows the grammar, not the
generator) followed by an exact solve by a *different* route — brute force
over small integer domains for puzzles, closing-speed instead of
distance-equality for motion, enumeration for optimization and packing,
interval endpoints for uncertainty, and cross-checks against the existing
generators' own oracles when a scenario reuses their procedures.

**Capacity.** > 1000 distinct problems per class from numbers × contexts ×
templates × modifiers; probe with `tools/probe_generator_capacity.py`.

## 4. Phase 0 — shared infrastructure

- `applied_common.py` (repo root, beside `helpers.py`):
  - `CONTEXTS` bank with names, items, units, price ranges, and per-context
    phrase fragments; `money()`, `unit()` renderers; `dec()`/`exact()`
    re-exported from `prob_common.py`.
  - **Story-template engine**: a template = slots (typed quantities with
    ranges/constraints), 5+ surface renderings, a canonical model string,
    a solver, and the `slot_phrase` used by missing-information answers.
    Generators declare templates; the engine renders, injects distractors,
    and produces `SELECT_RELEVANT`.
  - `METHOD_WORDS`: the banned-phrase list (method names, formula names,
    generator/variant names, "use/apply the … formula/rule/theorem").
  - `estimate_first(steps, exact)`: wraps a step list with `ESTIMATE` /
    `ESTIMATE_CHECK` using leading-digit rounding; used by every class.
  - `reject_step(candidate, reason)` for nonphysical roots, orientations,
    and options.
  - **Scenario harness**: `Scenario(parts)` threads shared state through a
    list of sub-procedures (each a small callable that returns steps and a
    value), emits `PART|k|<question>` markers between parts, and assembles
    the composite answer `Q1 …; Q2 …`. Sub-procedures may call existing
    generators' step builders where those are importable helpers.
- `tests/applied_oracle.py`: independent template inverters (regex per
  surface rendering), brute-force and alternate-route solvers, a
  leading-digit estimator, interval arithmetic, and parsers for tables
  embedded in problem text. Never imports `applied_common`.
- `tests/test_applied_conventions.py`: for every module with
  `APPLIED = True`, sample 200 examples and assert: no `METHOD_WORDS` hit in
  problem text unless the variant is `scaffolded`; no ASCII `|`; unit present
  in the answer where the template has one; `distractor` variants contain
  exactly one `SELECT_RELEVANT` step whose "ignored" field matches the
  injected number; `estimate_first` variants have `ESTIMATE` first and
  `ESTIMATE_CHECK` before `Z`; missing-information answers match the
  canonical form; every template's five renderings appear across the
  sample.
- DESIGN.md: "Applied answers" convention block (§3); README coverage
  bullets ("modeling word problems, estimation and measurement, judgment
  tasks, quantitative literacy, scenarios").
- Optional record metadata: scenario and discrimination records add a
  `skills` list (the procedures composed) so training mixes and held-out
  evaluation can be built by skill combination. `validate_example` checks
  required keys only; confirm extra keys pass through `write_jsonl` and
  `build_hf_release.py` (Phase 0 task).
- Op-code plan (reuse first): `SELECT_RELEVANT`, `ESTIMATE`,
  `ESTIMATE_CHECK`, `REWRITE`, `CHECK`, `TRY/REJECT/ACCEPT`, `SUBST`,
  `PERCENT_TO_DEC`, `DEC_TO_PERCENT`, `CONV_FACTOR/CONV_RESULT`,
  `PROP_SETUP`, `MOVE_TERM`, `COMB_X`, `DIV_COEFF`, `DISC`, `ROOT`,
  `ZERO_PRODUCT`, `VERTEX` (if present), `CEIL`, `FLOOR`, `CMP`, `L/C/F`,
  `A/S/M/D/E`, `AREA`, `PERIM`, `VOLUME`, `UNIT_RATE`, `MEAN_DIV`, `SORT`,
  `VERIFY/FLAG` (critic records). New codes (one meaning each):
  `DEFINE_VAR|letter|meaning`, `MODEL_EQ|equation|source phrase`,
  `RATE|worker|amount per unit`, `RATE_SUM|expression|value`,
  `AMOUNT|description|value` (mixture parts), `DRT|leg|d = r·t|value`,
  `CLOSING_SPEED|r1 + r2|value`, `PLAN_COST|plan|expression|value`,
  `BREAK_EVEN|equation|value`, `PCT_STEP|k|base × factor|value`,
  `REVERSE_PCT|sale = base × (1 − r)|base`, `UNIT_PRICE|item|price/qty|
  value`, `BEST_BUY|choice|comparison`, `OVERTIME|hours|rate|pay`,
  `PUZZLE_REL|phrase|equation`, `WASTE|k%|ceil`, `FENCE_SIDES|which|
  expression`, `DEMAND|p|q(p)`, `REVENUE|p·q|expression`, `CROSSOVER|
  year|linear|exponential`, `RULE_OF_70|rate|years`, `OPTION|name|value`,
  `AVG_RATE|(y2 − y1)/(x2 − x1)|value`, `INTERPRET|quantity|meaning`,
  `STRATEGY|name|rewrite`, `BOUND|expression|bound|reason`, `SIGFIG|
  value|count|reason`, `ROUND_SF|value|n|result`, `INTERVAL|quantity|
  [lo, hi]`, `PROPAGATE|rule|work|result`, `PCT_ERROR|abs(m − t)/t|value`,
  `TRUE_RANGE|display|[lo, hi)`, `ORDER_MAG|value|10^k`, `PLAUSIBLE|
  verdict|reason`, `MISSING|slot|reason`, `DISCRIMINATE|case|method|cue`,
  `ASSUMPTION|name|holds/fails|cue`, `DOMINANT|term|threshold`, `LIMIT|
  expression|value|reason`, `DIRECTION|quantity|increases/decreases|check`,
  `RISK|type|work|value`, `NNT|1/ARR|value`, `PP_VS_PCT|points|percent`,
  `SUBGROUP_RATE|group|option|rate`, `POOLED_RATE|option|rate`,
  `REVERSAL|statement`, `REGRESS_MEAN|μ + r(x − μ)|value`, `VISUAL_RATIO|
  bar heights|ratio`, `INDEX_NUMBER|value/base × 100|result`, `CAGR|(end/start)^
  (1/n)|value`, `PER_1000|count/pop × 1000|value`, `LOG_TICKS|k|×10^k`,
  `EXPECTED_COST|option|work|value`, `DECIDE|choice|comparison`,
  `TABLE_ROW|x|y`, `TABLE_DIFF|k|Δy or ratio`, `PATTERN|linear/exponential|
  cue`, `TRANSLATE|from|to`, `DERIVE|step|justification`, `GENERALIZE|
  pattern|formula`, `SCALE_LAW|dimension|k^d|value`, `FIT|axis|floor(L/l)|
  count`, `ORIENT|choice|count`, `CLOCK_ANGLE|hand|degrees`, `BEARING|
  turn|heading`, `PART|k|question`. Regenerated into `OPCODES.md` at the
  end of each phase.

## 5. The curriculum

Format per entry: **Class** · band · difficulty — variants; problem (one
concrete example with its exact answer string); procedure (op-codes);
answer; oracle; capacity/backward construction. All classes carry the four
modifiers of §3 unless marked otherwise. `⟲` marks an existing class being
extended.

### Strand M — Modeling word problems (elementary / middle / high)

**MultiStepWordGenerator** · elementary · d3 — `two_step_buy`,
`groups_then_remove`, `change_from_bill`, `time_elapsed`, `compare_totals`,
`three_step`. Problem: "Leo buys 4 packs of 6 pencils and gives 7 pencils to
his sister. How many pencils does he have left?" Answer `17 pencils`. Steps:
`SELECT_RELEVANT` (distractor variants), `M|4|6|24`, `S|24|7|17`, `CHECK|
add back|17 + 7|24`, `Z`. `change_from_bill`: 3 notebooks at $2.50 paid with
$20 → `$12.50`. Oracle: template inversion + arithmetic. Capacity: unbounded.
The elementary on-ramp; replaces the three fixed shapes of
`CompositeArithmeticGenerator` with a grammar.

**IntegerPuzzleWordGenerator** · middle · d2 — `age_now`, `age_future`,
`consecutive_integers`, `consecutive_even_odd`, `coins_count_value`,
`number_relationship`, `digit_reversal`. Problem: "Ann is 3 years older than
twice Ben's age. Together their ages add to 27. How old is each?" Answer
`Ann 19; Ben 8`. Steps: `DEFINE_VAR|b|Ben's age`, `PUZZLE_REL|3 more than
twice|a = 2b + 3`, `MODEL_EQ|b + (2b + 3) = 27|together add to 27`,
`COMB_X|3b + 3 = 27`, `MOVE_TERM|3b = 24`, `DIV_COEFF|b = 8`, `SUBST|a|2·8
+ 3|19`, `CHECK|19 + 8|27`, `Z`. Coins: 24 coins, nickels and dimes, $1.90
→ `nickels 10; dimes 14`. Oracle: brute force over small integer domains.
Capacity: unbounded.

**WorkRateGenerator** · middle · d3 — `together`, `one_alone_unknown`,
`one_leaves_early`, `fill_and_drain`, `three_workers`, `partial_job`.
Problem: "One hose fills a pool in 6 hours; a second fills it in 3 hours.
How long do both together take?" Answer `2 hours`. Steps: `RATE|hose A|1/6
pool per hour`, `RATE|hose B|1/3 pool per hour`, `RATE_SUM|1/6 + 1/3|1/2`
(with `L/C/A`), `MODEL_EQ|(1/2)·t = 1|whole pool`, `D|1|1/2|2`, `CHECK|2/6 +
2/3|1`, `Z`. `with_model` answer `1/6 + 1/3 = 1/t; t = 2 hours`.
`fill_and_drain`: fill 4 h, drain 12 h → `6 hours`. Oracle: alternate route
(LCM of times as the "job size" → integer rates). Capacity: time pairs with
LCM-friendly sums × contexts (hoses, painters, printers, pumps) × 6
templates — unbounded.

**MixtureGenerator** · middle · d3 — `two_solutions`, `add_pure`,
`add_water`, `price_blend`, `alloy`, `target_concentration_unknown_amount`.
Problem: "10 L of a 30% salt solution is mixed with 5 L of a 60% solution.
What is the concentration of the mixture?" Answer `40%`. Steps:
`AMOUNT|salt in 10 L at 30%|3 L` (`PERCENT_TO_DEC`, `M`), `AMOUNT|salt in 5 L
at 60%|3 L`, `A|3|3|6`, `A|10|5|15`, `D|6|15|0.4`, `DEC_TO_PERCENT|0.4|40%`,
`Z`. `price_blend`: 3 kg at $8 and 2 kg at $3 → `$6 per kg`. `target_…`:
how much 60% to add to 10 L of 30% to reach 40% → `5 L`. Oracle: alternate
route (conservation of solute solved for the unknown). Capacity: unbounded.

**MotionWordGenerator** · middle · d3 — `toward_each_other`, `same_direction_
catch_up`, `round_trip_average_speed`, `with_current`, `head_start`,
`time_to_meet_from_table`. Problem: "Two trains 300 km apart travel toward
each other at 70 km/h and 80 km/h. When do they meet?" Answer `2 hours`.
Steps: `DRT|train 1|d = 70t`, `DRT|train 2|d = 80t`, `MODEL_EQ|70t + 80t =
300|distances sum to the gap`, `COMB_X|150t = 300`, `DIV_COEFF|t = 2`,
`CHECK|140 + 160|300`, `Z`. `catch_up`: A at 40 km/h, B leaves 2 h later at
60 km/h → `6 hours after A leaves; 240 km`. `round_trip_average_speed`: 40
out, 60 back → `48 km/h` (harmonic, shown as total distance ÷ total time,
never averaged). `with_current`: boat 12 km/h, current 3 km/h, 45 km
downstream → `3 hours`. Oracle: `CLOSING_SPEED` route (300/(70 + 80)) vs the
generator's distance-equality route. Capacity: unbounded.

**LinearModelWordGenerator** · middle · d2 — `evaluate`, `invert`,
`from_two_points`, `break_even`, `compare_plans`, `interpret_parts`.
Problem: "A plumber charges $40 to come out plus $25 per hour. A repair bill
was $190. How many hours did the repair take?" Answer `6 hours`. Steps:
`DEFINE_VAR|h|hours worked`, `MODEL_EQ|40 + 25h = 190|fee plus hourly`,
`MOVE_TERM|25h = 150`, `DIV_COEFF|h = 6`, `CHECK|40 + 25·6|190`, `Z`.
`compare_plans`: A $30/month + $0.10/min vs B $50 flat → `plan B cheaper
beyond 200 minutes; break-even 200 minutes`. `interpret_parts`: composite
`40: the fixed call-out fee; 25: the charge per hour`. Oracle: alternate
route (two-point slope) and brute force for break-even. Capacity: unbounded.

**PercentChainGenerator** · middle · d3 — `markup_then_discount`,
`tax_then_tip`, `successive_changes_net`, `reverse_from_sale_price`,
`reverse_from_total_with_tax`, `percent_of_percent`. Problem: "A jacket is
marked up 25% from $80, then sold at 20% off the marked price. What is the
sale price, and what is the net percent change from $80?" Answer `$80; net
change 0%`. Steps: `PCT_STEP|1|80 × 1.25|100`, `PCT_STEP|2|100 × 0.8|80`,
`S|80|80|0`, `D|0|80|0`, `DEC_TO_PERCENT|0|0%`, `Z`. `reverse_from_sale_price`:
$60 after 25% off → `REVERSE_PCT|60 = base × 0.75|80` → `$80`. The classic
intuition trap (+25% then −20% ≠ +5%) made numeric. Oracle: recompute
forward; brute force the reverse. Capacity: unbounded.

**MoneyLifeGenerator** · middle · d2 — `best_buy`, `budget_share`,
`payroll_overtime`, `currency_supplied_rate`, `split_by_ratio`,
`savings_goal_weeks`. Problem: "Brand A: 12 oz for $3.60. Brand B: 20 oz for
$5.00. Which is the better buy per ounce?" Answer `brand B; $0.25 vs $0.30
per oz`. Steps: `UNIT_PRICE|A|3.60/12|0.30`, `UNIT_PRICE|B|5.00/20|0.25`,
`CMP|0.25|0.30|<`, `BEST_BUY|B|0.25 < 0.30`, `Z`. `payroll_overtime`: 45 h at
$15, overtime 1.5× above 40 → `OVERTIME|5|22.50|112.50`, `$712.50`. Oracle:
recompute; ties excluded. Capacity: unbounded.

**GeometryInContextGenerator** · middle · d3 — `fence_against_wall`,
`tiles_with_waste`, `paint_coverage`, `packaging_cost`, `border_area`,
`ladder_or_shadow`, `garden_path`. Problem: "A rectangular garden is fenced
on three sides; the fourth side is a wall. 30 m of fencing is used and the
two short sides are 8 m each. What is the garden's area?" Answer `112 m²`.
Steps: `FENCE_SIDES|two widths + one length|2·8 + L = 30`, `M|2|8|16`,
`S|30|16|14`, `AREA|8 × 14|112`, `Z`. `tiles_with_waste`: 4 m × 3 m floor,
0.25 m² tiles, 10% waste → `M|4|3|12`, `D|12|0.25|48`, `WASTE|10%|52.8 → 53`,
`53 tiles`. Oracle: recompute by an alternate decomposition. Capacity:
unbounded.

**SystemsWordGenerator** · high · d3 — `tickets`, `two_item_purchase`,
`investment_two_rates`, `mixture_as_system`, `perimeter_and_relation`,
`from_table`. Problem: "A theater sold 200 tickets for $1390. Adult tickets
cost $8 and child tickets $5. How many of each were sold?" Answer `adults
130; children 70`. Steps: `DEFINE_VAR|a|adult tickets`, `DEFINE_VAR|c|child
tickets`, `MODEL_EQ|a + c = 200|ticket count`, `MODEL_EQ|8a + 5c = 1390|
revenue`, substitution/elimination with the existing systems op-codes
(`SUBST|c|200 − a`, `REWRITE|8a + 1000 − 5a = 1390`, `COMB_X|3a = 390`,
`DIV_COEFF|a = 130`), `SUBST|c|200 − 130|70`, `CHECK|8·130 + 5·70|1390`,
`Z`. Oracle: brute force over integer pairs. Capacity: unbounded.

**QuadraticWordGenerator** · high · d4 — `projectile_ground_time`,
`projectile_max_height`, `area_with_border`, `revenue_linear_demand`,
`rectangle_from_area_perimeter`, `consecutive_product`. Problem: "A ball's
height in metres after t seconds is h(t) = −5t² + 20t + 25. When does it hit
the ground?" Answer `5 seconds`. Steps: `MODEL_EQ|−5t² + 20t + 25 = 0|height
zero`, `REWRITE|t² − 4t − 5 = 0` (`D` by −5), `ZERO_PRODUCT|(t − 5)(t + 1) =
0`, `TRY|t = −1`, `REJECT|t = −1|negative time`, `ACCEPT|t = 5`, `CHECK|h(5)|
−125 + 100 + 25 = 0`, `Z`. `revenue_linear_demand`: q = 20 − p → `REVENUE|
p(20 − p)`, vertex p = 10 → `$10; revenue $100`. Integer roots by
construction; the rejected root is always present in ground-time variants.
Oracle: `DISC`/`ROOT` route vs the generator's factoring route. Capacity:
unbounded.

**GrowthComparisonGenerator** · high · d3 — `linear_vs_exponential_table`,
`crossover_year`, `rule_of_70_doubling`, `depreciation_below_threshold`,
`repeated_doubling_count`, `which_offer`. Problem: "Offer A: $100 now,
growing by $10 each year. Offer B: $100 now, growing 10% each year. From
which year onward is B worth more?" Answer `year 2; $121 vs $120`. Steps:
`TABLE_ROW|year 1|A 110, B 110`, `TABLE_ROW|year 2|A 120, B 121`,
`CROSSOVER|2|120|121`, `Z`. `rule_of_70_doubling`: 7% per year, "use the
rule of 70" stated in the text as the tool (a supplied approximation, like a
table value) → `RULE_OF_70|7%|10`, `10 years`. `depreciation_below_threshold`:
$8000 losing 25% per year, first year below $4000 → `TRY|year 1|6000`,
`TRY|year 2|4500`, `TRY|year 3|3375`, `ACCEPT|year 3|3375 < 4000`, `year 3`.
Rates from {5, 10, 20, 25, 50}% so tables stay exact. Oracle: brute force
year by year. Capacity: unbounded. (`⟲ ExponentialModelGenerator` keeps its
method-stated variants; this class is the unstated-method counterpart.)

**OptimizationInContextGenerator** · high · d4 — `max_area_fixed_fence`,
`best_of_three_plans_table`, `min_cost_two_suppliers`, `knapsack_small`
(≤ 4 items by enumeration), `max_revenue`, `min_material_box`. Problem:
"With 40 m of fencing, what dimensions of a rectangular pen give the largest
area, and what is that area?" Answer `10 m by 10 m; 100 m²`. Steps:
`MODEL_EQ|A = w(20 − w)|half the fence is w + L`, `REWRITE|A = −w² + 20w`,
vertex `w = 10`, `AREA|10 × 10|100`, `CHECK|w = 9|99 < 100`, `Z`.
`best_of_three_plans_table`: `OPTION|A|$420`, `OPTION|B|$455`, `OPTION|C|
$430`, `DECIDE|A|420 < 430 < 455` → `plan A; $420`. Ties excluded. Oracle:
enumeration over integer candidates. Capacity: unbounded.

**RateOfChangeInterpretGenerator** · high · d3 — `average_rate_from_table`,
`interpret_slope`, `interpret_intercept`, `interpret_derivative_sign`,
`units_of_a_rate`, `compare_rates_two_intervals`. Problem: "A plant was 15 cm
tall on day 2 and 27 cm on day 5. What was its average growth rate?" Answer
`4 cm per day`. Steps: `AVG_RATE|(27 − 15)/(5 − 2)|4`, `INTERPRET|4 cm per
day|the plant grew 4 cm each day on average`, `Z`. `interpret_derivative_
sign`: "h'(3) = −2 where h is height in metres and t in seconds" → composite
`falling; 2 m per second at t = 3` (templated interpretation). Oracle:
recompute; interpretation strings come from the template. Capacity:
unbounded.

**⟲ ProportionWordProblemGenerator** — add `scale_drawing`, `map_scale`,
`recipe_scaling` (fractions of a batch), `shadow_similar_triangles`,
`speed_from_map`, plus the four modifiers. **⟲ PercentWordProblemGenerator**
— add `estimate_first` and `with_model`; its `distractor` mode becomes the
shared modifier. **⟲ UnitRateGenerator** — add `best_buy` and `distractor`.

### Strand N — Number sense and measurement (elementary / middle / high)

**MentalStrategyGenerator** · elementary · d2 — `compensation`,
`doubling_halving`, `distributive_split`, `friendly_numbers`,
`count_up_change`, `percent_shortcut`, `choose_strategy`. Problem: "Compute
47 × 99 mentally. Show the strategy." Answer `4653 (47 × 100 − 47)`. Steps:
`STRATEGY|compensation|99 = 100 − 1`, `M|47|100|4700`, `S|4700|47|4653`,
`CHECK|47 × 99 by column|4653`, `Z`. `doubling_halving`: 16 × 25 = 8 × 50 =
`400 (8 × 50)`; `percent_shortcut`: 15% of 80 = 8 + 4 = `12 (10% + 5%)`;
`count_up_change`: $20 − $13.45 → `$6.55 (0.55 → 14, then 6)`. The answer
names the strategy so grading rewards the strategy, not just the product.
Oracle: exact arithmetic; strategy label determined by the template.
Capacity: unbounded.

**MagnitudeComparisonGenerator** · middle · d2 — `benchmark_fraction`,
`compare_without_computing`, `order_of_magnitude`, `reasonable_answer`,
`bigger_product_or_quotient`, `estimate_then_verify`. Problem: "Without
computing exactly, which is larger: 0.3 × 45 or 45 ÷ 3?" Answer `45 ÷ 3;
15 > 13.5`. Steps: `BOUND|45 ÷ 3|= (1/3) × 45|exact`, `BOUND|0.3 × 45|< (1/3) × 45|0.3 <
1/3`, `CMP|0.3 × 45|45 ÷ 3|<`, `CHECK|exact|13.5 vs 15`, `Z`. `benchmark_fraction`:
7/15 vs 1/2 → `less than 1/2; 7 < 7.5`. `order_of_magnitude`: 4.8 × 10³
people × 2.1 × 10² dollars → `ORDER_MAG|~10^6`. The steps show the bounding
argument, then confirm exactly — the intuition and the verification both
appear. Oracle: exact comparison. Capacity: unbounded.

**RoundingEffectGenerator** · middle · d2 — `true_range_of_display`,
`round_before_vs_after`, `front_end_estimate`, `leading_digit_estimate`,
`accumulated_rounding`. Problem: "A scale shows 3.4 kg, rounded to the
nearest 0.1 kg. What is the range of the true mass?" Answer `3.35 kg ≤ m <
3.45 kg`. Steps: `TRUE_RANGE|3.4 to nearest 0.1|[3.35, 3.45)`, `Z`.
`round_before_vs_after`: 2.46 + 3.47 → rounded first 2.5 + 3.5 = 6.0, exact
5.93 → 5.9: composite `5.9; rounding first gives 6.0, off by 0.1`. Oracle:
recompute. Capacity: unbounded.

**SignificantFiguresGenerator** · high · d2 — `count_sig_figs`,
`round_to_sig_figs`, `multiply_divide_rule`, `add_subtract_rule`,
`scientific_notation_measurement`. Problem: "How many significant figures
are in 0.004500?" Answer `4`. Steps: `SIGFIG|0.004500|4|leading zeros not
significant; trailing zeros after the decimal are`, `Z`. `multiply_divide_
rule`: 2.5 × 3.42 = 8.55 → `ROUND_SF|8.55|2|8.6` (rule stated in the
problem: "report to the fewer significant figures"). Oracle: independent
rule implementation. Capacity: unbounded.

**MeasurementUncertaintyGenerator** · high · d3 — `tolerance_interval`,
`within_tolerance`, `sum_difference_propagation`, `area_from_measured_sides`
(interval endpoints), `percent_error`, `relative_uncertainty_rule` (stated).
Problem: "A rectangle measures 12.5 ± 0.2 cm by 8.0 ± 0.1 cm. Give the
smallest and largest possible area." Answer `97.17 cm² to 102.87 cm²`.
Steps: `INTERVAL|length|[12.3, 12.7]`, `INTERVAL|width|[7.9, 8.1]`,
`M|12.3|7.9|97.17`, `M|12.7|8.1|102.87`, `PROPAGATE|min × min, max × max|
[97.17, 102.87]`, `Z`. `percent_error`: measured 9.8, true 10 →
`PCT_ERROR|abs(9.8 − 10)/10|2%`. Exact decimal arithmetic. Oracle: interval
endpoints recomputed. Capacity: unbounded.

**⟲ FermiEstimationGenerator** — add six contexts (household water, city
buses, school lunches, book pages, road trip fuel, waste bags), a
`bound_check` variant (`is 10^9 plausible for X? no; upper bound 10^7`), and
`compare_two_estimates`.

### Strand J — Judgment (elementary / middle / high)

**MissingInformationGenerator** · elementary · d2 — `identify_missing`,
`solvable_control` (the same story with the slot filled → numeric answer, so
the model must decide rather than pattern-match), `which_of_two_missing`,
`extra_and_missing` (a distractor is present *and* a needed value is
absent). Problem: "Mia buys 3 notebooks and pays with a $20 bill. How much
change does she get?" Answer `insufficient information; need the price of a
notebook`. Steps: `SELECT_RELEVANT|used: 3, $20|needed: price per
notebook`, `MISSING|price of a notebook|change = 20 − 3 × price`, `Z`.
Control: with "$2.50 each" → `$12.50`. Slot phrases come from the story
template; the generator draws its stories from every Strand M template, so
this class scales with the strand. Oracle: template inversion determines
which slot is absent. Capacity: unbounded. Serves the same split-decision
role as `CHECK_POINT` records: half the examples are solvable.

**MethodDiscriminationGenerator** · high · d3 — `combination_vs_permutation`,
`independent_vs_dependent`, `area_vs_perimeter`, `mean_vs_median`,
`linear_vs_exponential`, `proportional_vs_not`, `additive_vs_multiplicative`,
`pythagoras_vs_similar`. Problem: "A: choose 3 of 5 books to take on a trip.
B: arrange 3 of 5 books on a shelf. For each, how many ways?" Answer `A:
combination, 10; B: permutation, 60`. Steps: `DISCRIMINATE|A|combination|
order irrelevant ("choose")`, `NCR|C(5, 3)|10`, `DISCRIMINATE|B|permutation|
order matters ("arrange")`, `M|5·4·3|60`, `Z`. `proportional_vs_not`: a
table with a fixed cost → `not proportional; y/x is 12, 8, 6.67 — not
constant`. Contrasting cases are generated as *pairs sharing numbers* so the
only difference is the cue. Oracle: brute force / recompute both. Capacity:
unbounded.

**AssumptionCheckGenerator** · high · d4 — `proportional_reasoning_with_fixed_
cost`, `independence_without_replacement`, `triangle_inequality`,
`nonphysical_root`, `normal_approx_small_n`, `extrapolation_beyond_data`,
`division_by_zero_rate`, `average_of_averages`. Problem: "A taxi charges $3
plus $2 per km. A 5 km ride costs $13. Sara says a 10 km ride costs $26 by
doubling. Is she right?" Answer `does not apply; fixed $3 fee makes cost
non-proportional; correct $23`. Steps: `ASSUMPTION|proportional|fails|fixed
fee present`, `MODEL_EQ|3 + 2·10|23`, `CMP|23|26|≠`, `Z`.
`independence_without_replacement`: "two cards, no replacement, P(both
hearts) computed as 1/4 × 1/4" → `not independent; second draw depends on
the first; correct 1/4 × 12/51 = 1/17`. `triangle_inequality`: 3, 4, 8 →
`no triangle; 3 + 4 < 8`. Each template flags exactly one assumption. Oracle:
recompute the correct value by the valid method. Capacity: unbounded.

**QualitativeReasoningGenerator** · high · d3 — `dominant_term`,
`limiting_value`, `direction_of_change`, `doubling_effect_in_formula`,
`compare_growth_rates`, `sign_without_computing`. Problem: "For large n,
which grows faster, n² or 100n, and from what n onward is n² larger?" Answer
`n²; larger for n > 100 (at n = 200: 40000 vs 20000)`. Steps: `DOMINANT|n²|
n > 100`, `CHECK|n = 200|40000 vs 20000`, `Z`. `limiting_value`: (3n +
1)/(n + 2) → `LIMIT|3|leading coefficients`, with `CHECK|n = 1000|3001/1002
≈ 2.995`. `direction_of_change`: "if the rate r in A = P(1 + r)^t increases,
what happens to A?" → `DIRECTION|A|increases|P = 100, t = 2: 121 → 144`,
answer `increases; 121 → 144 when r goes 10% → 20%`. Oracle: exact
evaluation at the check points; threshold by brute force. Capacity:
unbounded.

**PlausibilityCriticGenerator** · high · d3 — `magnitude`, `units`,
`direction`, `bounds` (probability > 1, part > whole, percent of a part >
100%), `monotonicity` (more workers, more time?), `control_plausible`.
Problem: "A car travels 120 km in 1.5 hours. A student claims its average
speed was 180 km/h. Is that plausible?" Answer `implausible; correct 80
km/h`. Steps: `ESTIMATE|120 ÷ 1.5 ≈ 120 ÷ 1.5|80`, `PLAUSIBLE|no|180 is more
than double the estimate`, `D|120|1.5|80`, `CHECK|180 vs 80|implausible`,
`Z`. `units`: "area of a 4 m by 6 m room is 24 m" → `implausible; area needs
m², correct 24 m²`. `control_plausible`: the claim is right → `plausible;
correct 80 km/h`. Claims are perturbations of the strand's own problems
(wrong operation, dropped factor, wrong unit, inverted ratio), so the
verdict is determined. Oracle: recompute the true value; verdict by
comparison. Capacity: unbounded. Critic-format sibling of
`ErrorSpottingGenerator`.

The foundations plan's `CounterexampleSearchGenerator` (smallest
counterexample to a false claim) belongs to this strand in spirit and is
cross-referenced, not duplicated.

### Strand L — Quantitative literacy (high)

**RiskCommunicationGenerator** · high · d2 — `relative_vs_absolute`,
`percent_vs_percentage_points`, `nnt`, `per_capita_vs_raw`, `rate_per_1000`,
`doubling_a_small_risk`. Problem: "Without treatment the risk of an illness is 3 in 1000; with
treatment it is 2 in 1000. State the relative risk reduction and the
absolute risk reduction."
Answer `relative 33 1/3%; absolute 0.1 percentage points`. Steps: `RISK|
absolute|3/1000 − 2/1000|1/1000`, `RISK|relative|(3 − 2)/3|1/3`,
`DEC_TO_PERCENT|1/3|33 1/3%`, `PP_VS_PCT|0.1 points|33 1/3%`, `Z`. `nnt`:
ARR 5% → `NNT|1/0.05|20 people`. `per_capita_vs_raw`: 30 cases in 12,000 vs
50 in 25,000 → `PER_1000|2.5 vs 2`, `first town higher per 1000 (2.5 vs 2)
despite fewer cases`. Rates chosen so percents are exact or clean fractions.
Oracle: recompute. Capacity: unbounded.

**SimpsonsParadoxGenerator** · high · d3 — `compute_and_state_reversal`,
`which_is_better_overall`, `which_is_better_in_each_group`,
`weights_explain` (the group sizes that cause it), `no_reversal_control`.
Problem: "Hospital A: easy cases 8 of 10 recovered, hard cases 18 of 90.
Hospital B: easy cases 63 of 90 recovered, hard cases 1 of 10. Compare the
recovery rates within each case type and overall." Answer `A better in both
groups (80% > 70%, 20% > 10%); B better overall (64% > 26%)`. Steps:
`SUBGROUP_RATE|easy|A|8/10 = 80%`, `SUBGROUP_RATE|easy|B|63/90 = 70%`,
`SUBGROUP_RATE|hard|A|18/90 = 20%`, `SUBGROUP_RATE|hard|B|1/10 = 10%`,
`POOLED_RATE|A|26/100 = 26%`, `POOLED_RATE|B|64/100 = 64%`, `REVERSAL|A wins
each group, B wins overall`, `CHECK|A's cases are 90% hard; B's are 90%
easy`, `Z`. Built backward from integer counts with clean percents; the
`control` variant has no reversal so the label is not automatic. Oracle:
recompute all six rates. Capacity: > 1000 via count grids × contexts
(hospitals, admissions, batting, sales reps) × phrasings.

**StatisticalLiteracyGenerator** · high · d3 — `regression_to_mean`
(`μ + r(x − μ)` with r supplied), `averaging_rates_wrong`, `visual_ratio_
truncated_axis`, `sampling_error_scale` (margin ≈ 1/√n, perfect-square n),
`percent_of_what` (base confusion), `cherry_picked_interval` (compute the
change over the stated window vs the full window).
Problem: "Class mean is 70 and the retest correlation is 0.5. A student
scored 90. What retest score should be expected?" Answer `80`. Steps:
`REGRESS_MEAN|70 + 0.5·(90 − 70)|80`, `Z`. `averaging_rates_wrong`: 50% of
20 and 100% of 80 → naive 75%, correct `POOLED_RATE|90/100|90%`, answer
`90%; averaging the two percents gives 75%, which is wrong`. `visual_ratio_
truncated_axis`: bars 90 and 95 drawn from a baseline of 85 → `VISUAL_RATIO|
10 : 5|2`, true `19/18` → `visual 2; true 19/18`. Oracle: recompute.
Capacity: unbounded.

**IndexAndGrowthGenerator** · high · d2 — `index_number`, `percent_change_vs_
points`, `cagr_perfect_power`, `real_vs_nominal_supplied_cpi`, `log_scale_
reading`, `repeated_doubling`. Problem: "A price index rises from 100 to
125, then to 150. What is the percent change in each step?" Answer `25%;
20%`. Steps: `INDEX_NUMBER|125/100|1.25`, `DEC_TO_PERCENT|0.25|25%`, `INDEX_NUMBER|150/125|
1.2`, `DEC_TO_PERCENT|0.2|20%`, `Z`. `cagr_perfect_power`: 100 → 144 in 2
years → `CAGR|(144/100)^(1/2)|1.2` → `20% per year`. `log_scale_reading`:
"the curve rises two major ticks on a log-10 axis" → `LOG_TICKS|2|×100`.
Oracle: recompute; roots exact by construction. Capacity: unbounded.

**DecisionUnderUncertaintyGenerator** · high · d3 — `expected_cost_two_
plans`, `insurance_premium_vs_expected_loss`, `fair_price`, `minimax_vs_
expected`, `risk_of_ruin_simple`, `wait_or_buy`. Problem: "Plan A costs $100
flat. Plan B costs $50 plus a $200 repair fee that is needed with
probability 0.3. Which has the lower expected cost?" Answer `plan A; $100 vs
$110`. Steps: `EXPECTED_COST|A|100|100`, `EXPECTED_COST|B|50 + 0.3·200|110`,
`DECIDE|A|100 < 110`, `Z`. `insurance`: premium $120 vs 2% chance of a $5000
loss → `expected loss $100; premium exceeds it by $20`. Ties excluded.
Oracle: recompute. Capacity: unbounded. (Decision framing; the expected-value
mechanics stay in `ExpectedValueGenerator`.)

### Strand R — Representations (high)

**RepresentationTranslationGenerator** · high · d3 — `words_to_equation`,
`equation_to_words` (templated), `table_to_equation_linear`,
`table_to_equation_exponential`, `equation_to_table`, `graph_features_to_
equation` (intercepts/slope described in words), `intercept_meaning`,
`which_representation_matches`. Problem: "A table shows (0, 40), (1, 65),
(2, 90), (3, 115). Is the relationship linear or exponential, and what is
the equation?" Answer `linear; common difference 25; y = 25x + 40`. Steps:
`TABLE_DIFF|1|+25`, `TABLE_DIFF|2|+25`, `TABLE_DIFF|3|+25`, `PATTERN|linear|
constant difference`, `TRANSLATE|table|y = 25x + 40`, `CHECK|x = 3|115`,
`Z`. Exponential: 3, 6, 12, 24 → `exponential; common ratio 2; y = 3·2^x`.
`intercept_meaning` (plumber context) → `40; the fixed call-out fee`.
Oracle: recompute differences/ratios; canonical equation from the template.
Capacity: unbounded.

### Strand D — Derivations (high)

**FormulaDerivationGenerator** · high · d3 — `arithmetic_series_pairing`,
`interior_angle_sum_triangulation`, `triangle_area_from_rectangle`,
`trapezoid_from_triangles`, `distance_formula_from_pythagoras`,
`divide_by_fraction_reciprocal`, `compound_interest_repeated_multiplication`,
`quadratic_formula_complete_square_concrete`. Problem: "Derive a formula for
1 + 2 + … + n by pairing terms, then use it for n = 20." Answer `S = n(n +
1)/2; S_20 = 210`. Steps: `DERIVE|pair first and last|1 + 20 = 21`, `DERIVE|
every pair sums to 21|10 pairs`, `M|10|21|210`, `GENERALIZE|n/2 pairs of (n +
1)|S = n(n + 1)/2`, `CHECK|n = 20|20·21/2 = 210`, `Z`. `interior_angle_sum`:
hexagon → `(n − 2)·180; 720°`. `divide_by_fraction`: 3/4 ÷ 2/5 via common
denominator 20 → `15/20 ÷ 8/20 = 15/8 = 3/4 × 5/2`. Each derivation is a
fixed canonical route; capacity comes from the applied parameters. Oracle:
recompute the applied value; the formula string is fixed per variant.
Capacity: > 1000 via parameters × contexts × phrasings.

### Strand G — Spatial intuition (middle)

**SquareCubeLawGenerator** · middle · d3 — `scale_model_area_volume`,
`map_area`, `recipe_pan_scaling`, `area_unit_conversion`, `volume_unit_
conversion`, `how_many_small_cubes`, `giant_or_miniature`. Problem: "A model
car is built at a scale of 1 : 20. The real car's windshield has an area of
2 m². What is the model windshield's area in cm²?" Answer `50 cm²`. Steps:
`SCALE_LAW|area|k² = 400`, `CONV_FACTOR|1 m² = 10,000 cm²`, `M|2|10000|
20000`, `D|20000|400|50`, `Z`. `how_many_small_cubes`: edge tripled → `27
cubes`. Oracle: recompute by the other route (scale lengths first, then
area). Capacity: unbounded. (Check overlap with `ScalingGenerator` at Phase
0; if that class is the physics dimensional-scaling generator, this one
stays separate.)

**SpatialPackingGenerator** · middle · d3 — `boxes_in_box_orientation`,
`tiles_with_grout`, `cans_in_case`, `wrapping_paper_overlap`, `leftover_
material`, `shelves_from_board`. Problem: "How many 20 cm × 20 cm × 15 cm
cartons fit in a 60 cm × 40 cm × 30 cm box, cartons all the same way up?"
Answer `12 cartons (3 × 2 × 2)`. Steps: `FIT|length|floor(60/20)|3`,
`FIT|width|floor(40/20)|2`, `FIT|height|floor(30/15)|2`, `M|3·2·2|12`,
`TRY|cartons on their side (15 up)|floor(60/20)·floor(40/15)·floor(30/20)
= 3·2·1 = 6`, `REJECT|6 < 12`, `ORIENT|15 cm up|12`, `Z`. Orientation ties
excluded. Oracle: enumerate all orientations. Capacity: unbounded.

**SpatialDescriptionGenerator** · middle · d2 — `clock_angle`, `bearing_after_
turns`, `coordinates_from_story`, `perimeter_from_walk`, `compass_turns`,
`net_matches_solid` (text nets, `NetsSurfaceArea` style). Problem: "What is
the angle between the hands of a clock at 3:30?" Answer `75°`. Steps:
`CLOCK_ANGLE|minute hand|180°`, `CLOCK_ANGLE|hour hand|3.5 × 30 = 105°`,
`S|180|105|75`, `Z`. `bearing_after_turns`: start heading 040°, turn right
90°, then left 30° → `BEARING|right 90|130°`, `BEARING|left 30|100°`, `100°`.
Oracle: recompute. Capacity: unbounded.

### Strand X — Scenarios (high)

**ScenarioGenerator** · high · d4 — `small_business`, `road_trip`,
`event_planning`, `home_project`, `science_lab`, `personal_finance`,
`sports_stats`, `data_report`. Each scenario threads 3–6 sub-questions with
shared state through existing procedures; the record's `operation` is
`scenario_<name>` and the optional `skills` field lists what was composed.
Problem (small_business): "Jan: sales $4000, costs $2500. Feb: sales $5000,
costs $3000. (1) What was January's profit margin? (2) By what percent did
sales grow from January to February? (3) If sales keep growing at that
rate, what are March sales? (4) Fixed costs are $1500 per month and each
unit sells for $50 with $20 of variable cost; how many units break even?"
Answer `Q1 37.5%; Q2 25%; Q3 $6250; Q4 50 units`. Steps: `PART|1|profit
margin`, `S|4000|2500|1500`, `D|1500|4000|0.375`, `DEC_TO_PERCENT|0.375|
37.5%`, `PART|2|sales growth`, `S|5000|4000|1000`, `D|1000|4000|0.25`, …,
`PART|4|break-even`, `BREAK_EVEN|1500 = (50 − 20)·u|50`, `Z`. Every part's
arithmetic is exact by construction (percents from the clean set; growth
compounding with terminating results). Oracle: each part recomputed
independently from the parsed scenario data; cross-checked against the
existing generators' oracles where a part reuses one (percent change,
break-even, unit conversion). Capacity: unbounded (numbers × scenario
sub-question subsets × phrasings). `distractor` and `estimate_first` apply
per part. Critic derivations (`ErrorSpotting` on a scenario part) follow in
close-out.

## 6. Band and difficulty summary

| Band | New classes | Extended |
|---|---:|---|
| elementary | 3 (MultiStepWord d3, MentalStrategy d2, MissingInformation d2) | PercentWordProblem, ProportionWordProblem |
| middle | 13 (IntegerPuzzleWord d2, LinearModelWord d2, MoneyLife d2, MagnitudeComparison d2, RoundingEffect d2, SpatialDescription d2, WorkRate d3, Mixture d3, MotionWord d3, PercentChain d3, GeometryInContext d3, SquareCubeLaw d3, SpatialPacking d3) | UnitRate |
| high | 19 (RiskCommunication d2, SignificantFigures d2, IndexAndGrowth d2, SystemsWord d3, GrowthComparison d3, RateOfChangeInterpret d3, MeasurementUncertainty d3, MethodDiscrimination d3, QualitativeReasoning d3, PlausibilityCritic d3, SimpsonsParadox d3, StatisticalLiteracy d3, DecisionUnderUncertainty d3, RepresentationTranslation d3, FormulaDerivation d3, QuadraticWord d4, OptimizationInContext d4, AssumptionCheck d4, Scenario d4) | FermiEstimation, ExponentialModel |
| college / graduate | 0 | — |

Total: **35 new generator classes, 5 extended**, roughly 220 operation
variants before the four modifiers (×4 with them). The band skew is
deliberate: real-world reasoning and intuition are middle- and
high-school skills; the college/graduate bands are already the deepest part
of the catalog. Elementary moves 36 → 39 skills and middle 64 → 77, which is
exactly the direction `plans/dataset_plan.md` asks for.

## 7. Delivery order

One generator per commit, tests in the same commit, docs regenerated at the
end of each phase. Each phase ends with `uv run python -m unittest discover
tests`, `probe_generator_capacity.py --threshold 1000` on the new classes, a
seeded 200-example build per class with zero errors, and `OPCODES.md` /
`PROBLEM_TYPES.md` regenerated with `--check` passing. Phase 0 depends on
`prob_common.py` (probability Phase 0) for `exact()`; nothing else in this
plan waits on the other three.

| Phase | Deliverable | Why this order |
|---|---|---|
| 0 | `applied_common.py` (context bank, story-template engine, `METHOD_WORDS`, `estimate_first`, scenario harness), `tests/applied_oracle.py`, conventions test, DESIGN.md block, `skills` metadata pass-through check | every class renders, inverts, and is policed the same way |
| 1 | MultiStepWord, IntegerPuzzleWord, WorkRate, Mixture, MotionWord, LinearModelWord, PercentChain, MoneyLife; ⟲ PercentWordProblem / ProportionWordProblem / UnitRate | the modeling core; proves the template engine and all four modifiers |
| 2 | MissingInformation, MethodDiscrimination, PlausibilityCritic, AssumptionCheck, QualitativeReasoning | judgment tasks built on Phase 1's stories |
| 3 | MentalStrategy, MagnitudeComparison, RoundingEffect, SignificantFigures, MeasurementUncertainty; ⟲ FermiEstimation | number sense and measurement |
| 4 | GeometryInContext, SystemsWord, QuadraticWord, GrowthComparison, OptimizationInContext, RateOfChangeInterpret, RepresentationTranslation, FormulaDerivation; ⟲ ExponentialModel | the rest of modeling, plus representations and derivations |
| 5 | RiskCommunication, SimpsonsParadox, StatisticalLiteracy, IndexAndGrowth, DecisionUnderUncertainty | quantitative literacy |
| 6 | SquareCubeLaw, SpatialPacking, SpatialDescription | spatial intuition |
| 7 | Scenario (all eight scenarios); **unstated-method sweep** of ~20 existing applied classes (Finance, Annuity, ExponentialModel, RelatedRates, Optimization, PercentProblem, Systems, LinearEquation word forms, inequality word forms, Pythagorean/Similar figures, the probability/statistics word classes) adding a `plain` unstated phrasing, `distractor`, and `estimate_first`; capacity probe; README; regenerate `PROBLEM_TYPES.md`, `OPCODES.md`; held-out **judgment/composition evaluation config** in `tools/build_hf_release.py` (scenario records and unstated-method variants tagged by `skills` so transfer can be measured separately from execution) | composition and close-out |

Definition of done per generator (checklist copied into each PR): class
in `generators/`, registered in `quixi_math_datagen.py` import +
`ALL_GENERATORS` + `curriculum.CURRICULUM`; module-level `APPLIED = True`;
docstring lists variants, modifiers, templates, and op-codes (one meaning
each); **five** phrasings per template, all inverted by the oracle; no
`METHOD_WORDS` hit; mirrored test with contract, 500-sample oracle from
problem text by an independent route, step-arithmetic check, every
variant × modifier reachable, invalid-variant guard, pipe safety, both
verdict outcomes present for every verdict variant; composite answer
wherever the bare verdict is a label; capacity probe passes; seeded
200-example build with zero errors.

## 8. Out of scope, and why

No exact hand procedure ⇒ no generator: free-form "explain your reasoning"
answers (interpretations are templated composites only), open modeling
where several inequivalent models are all defensible (the template fixes
one), estimation tasks whose "right" answer depends on unstated
assumptions beyond leading-digit rounding (Fermi contexts state every
assumption), reading real images or charts (displays are text; see
`plans/statistics_plan.md`), and social-judgment questions (correlation vs
causation stated in words) with no numeric core.

## 9. Decisions taken in this plan (change here, not per generator)

- **The problem text names no method**, enforced by a banned-phrase test;
  `scaffolded` is the only exemption and never the default.
- Four modifiers (`plain`, `distractor`, `estimate_first`, `with_model`) on
  every modeling class; `SELECT_RELEVANT` and `ESTIMATE`/`ESTIMATE_CHECK`
  are the existing op-codes and formats, reused unchanged.
- Missing information has one canonical answer form: `insufficient
  information; need <slot phrase>`; half of that class's records are
  solvable controls.
- Verdict answers always carry the number that earns them; discrimination
  pairs share their numbers so only the cue differs; ties and ambiguous
  orientations are excluded by construction.
- Five phrasings per template (not three), across ≥ 3 contexts, with the
  data order varied; the oracle inverts every phrasing.
- Numbers are realistic but hand-friendly; percents from a fixed clean
  set; rejected roots/options are shown with `REJECT`.
- Scenario records carry an optional `skills` list; the release builder
  gains a judgment/composition evaluation config built from it.
- Band skew toward middle/high is intentional; no college/graduate classes
  in this plan.
- Cross-references: `CounterexampleSearchGenerator` (foundations) is the
  falsification sibling of Strand J; `TwoWayTable*`, `SamplingDistributionEnum`,
  and `ExpectedValueGenerator` keep their mechanics in their own plans — this
  plan adds only the decision/literacy framings; `exact()` comes from
  `prob_common.py`.

# Depth Curriculum Plan — long serial reasoning chains

The catalog teaches procedures; this plan teaches **endurance**. Every
strand so far optimizes for the procedure being the difficulty. Here the
procedure is deliberately easy and the difficulty is *staying on track*:
chains of 50, 100, 200+ dependent steps where step N consumes step N−1's
output, one slip propagates to the final answer, and most humans would
reach for a calculator by step 12. The target skill is long-horizon state
tracking — carrying evolving intermediate state through a trace far longer
than anything in the current registry, and (in the checkpointed variants)
noticing drift before it compounds.

## 1. Why, and what "depth" means here

A 2026-08-29 probe of all 696 registered generators: **median trace is 9
steps**; only 50 classes exceed 30 steps in a typical draw; the longest
(~119) are *wide*, not *deep* — enumeration breadth (truth-table rows,
coset lists, Pascal rows) where an error in row 7 does not corrupt row 8.
Nothing in the catalog produces a long **serial dependency chain**.

**Depth** is the length of the longest dependency chain in the trace, not
the raw step count. A trace has depth D when D consecutive steps each take
the previous step's result as an operand. The conventions test measures
this directly (§3), so enumeration cannot masquerade as depth.

Why this matters for training: models rarely fail long tasks by not
knowing the procedure — they fail by losing state mid-chain (a dropped
sign at step 40, a stale intermediate reused, an off-by-one in an index).
Short traces cannot exercise that failure mode. Long exact chains are also
the cheapest fully-verified long-reasoning data there is: every
intermediate is exactly checkable, which almost no long-form reasoning
corpus can claim.

## 2. Current coverage and gaps

Deepest existing classes (avg steps, seeded): `ContinuedFraction` 56,
`ExtendedEuclid` 45, `ModularInverse` 44, `FractalIteration` 36,
`Recurrence` 22, `NewtonRaphson` 17, `FixedPoint` 15, `Horner` 14,
`LongDivision` 11, `BaseConversion` 9, `Annuity` 12. All top out well
under 100 steps, none has a depth knob, none emits checkpoints, and no
class composes procedures serially (Scenario composes in *parallel*
parts). There is no long-form critic record (find the one bad row in a
100-row ledger).

## 3. Strand-wide rules (in addition to AGENTS.md)

**Depth tiers.** Every class in this plan takes a `depth` parameter with
three tiers, encoded in the operation string:

| Tier | Serial-chain target | Operation suffix |
|---|---:|---|
| `d50` | 40–70 dependent steps | `_d50` |
| `d100` | 85–130 | `_d100` |
| `d200` | 170–260 | `_d200` |

Tier targets are on the *dependency chain*, not the raw step count.
Default draw weights 50/35/15 across tiers so the corpus skews long but
`d200` records (2–4k tokens each) do not dominate token counts. A class
may add `d400` where the arithmetic stays bounded (modular chains,
ledgers); never below `d50` — short forms of these procedures already
exist elsewhere in the catalog and are not re-registered here.

**Bounded intermediates (the defining construction rule).** Numbers must
not grow with depth. Every chain uses one of the bounded-state patterns:
modular reduction (state lives in Z_m, m ≤ 1000); contractive rational
maps (denominators fixed 2,5-smooth by construction); shrinking chains
(gcd, digit processes); ledgers in exact cents; bounded registers. Each
individual step stays hand-small — the grind is long, never big. This is
the carve-out from the repo's "never digit grinding" rule: the *chain* is
the pedagogical target, but each link is trivially hand-checkable.

**Checkpoints.** New op-code `MILESTONE|k|<invariant>|<value>` (the names
`CHECKPOINT`, `CHECK_POINT`, and `INVARIANT` are avoided: `CHECK_POINT`
and `INVARIANT` already exist with different field semantics, and
`CHECKPOINT` differs from `CHECK_POINT` by one underscore): an honest
recomputation of a running invariant (running total mod 9, current
balance, iteration count × known period offset) emitted every 10–15 chain
steps. Two variant modifiers on every class: `checkpointed` (default at
`d100`+) and `plain` (pure persistence; default at `d50`). The oracle
recomputes every checkpoint value independently — a checkpoint that
merely echoes the previous step is a test failure.

**Serial-dependency conventions test.** `tests/test_depth_conventions.py`
discovers classes by module flag `DEPTH = True` and asserts, per draw:
chain length ≥ tier floor, where consecutive arithmetic steps (`A`, `S`,
`M`, `D`, and the strand's chain codes) are chained iff one operand
string-equals the previous step's result field; checkpoint values
recompute exactly; pipe safety; `steps[-1] == Z|<answer>`; token length
under 16k characters. **Retrofit semantics:** a ⟲ class keeps its legacy
variants untiered (add, never rename), and draws whose operation carries
no tier suffix are exempt from the depth checks — but a flagged module
must *reach* tiered operations in sampling, or the flag is meaningless
and the test fails.

**Answers.** Usually short — the whole point is a long trace ending in a
small exact answer (`x_120 = 341`, `balance $1,204.63` → house money
format `$1204.63`, `first error at row 73; correct value 418`). Composite
verdicts use the house `label; fact` form. Never a list of all N
intermediates (that is the trace's job).

**Phrasing.** 3–5 templates per class (house standard), stating N
explicitly ("iterate 120 times", "the first 96 payments"). The oracle
parses N from every phrasing.

**Oracles (A9).** Recompute the entire chain from the problem text alone
by an independent implementation (closed forms where they exist —
geometric-sum formula against the term-by-term trace, matrix power against
the unrolled recurrence, amortization formula against the schedule —
brute-force re-simulation otherwise), plus every checkpoint.

**Capacity.** Trivially wide (initial state × parameters × N × templates)
but probe anyway; construction bugs can collapse the space (e.g. all
orbits entering the same cycle).

**Difficulty metadata.** Conceptual band as usual for the underlying
procedure; difficulty +1 at `d100`, +2 at `d200` (capped at 5). Depth is
otherwise invisible to curriculum metadata — the operation suffix carries
it for filtering, and `tools/build_hf_release.py`'s token estimates
already account for record length in the size configs.

## 4. Phase 0 — shared infrastructure

`depth_common.py`: tier definitions and draw weights; `chain()` — a
running-state step emitter that enforces the operand-chaining convention
mechanically; `checkpoint_every(k)` wrapper; bounded-state constructors
(`modular_orbit`, `contractive_map` with 2,5-smooth denominators,
`cents_ledger`); cycle detection (Floyd) for orbit variants; N-parsing
helpers shared with the oracle. `tests/depth_oracle.py`: independent
chain re-simulators and the closed-form cross-checks. Conventions test as
in §3, with fixtures proving each checker rejects a violating trace.
DESIGN.md gets a "Depth answers (A0 extension)" block. `OPCODES.md`
check for `MILESTONE`, `PIPE_STAGE`, and each strand's chain codes
before naming them.

## 5. The curriculum

### Strand I — Iterated maps (middle / high)

**IteratedAffineMapGenerator** · middle · d2 — x_{n+1} = (a·x_n + b) mod
m, all values < 1000. Variants: `final_state` (x_N), `orbit_period`
(detect the cycle, answer `period 12; enters cycle at n=7`),
`first_return` (smallest n > 0 with x_n = x_0, constructed to exist),
`backward` (given x_N and the map, run the inverse map — a is chosen
coprime to m). Steps: one `ITER|<x_prev>|n=<k>|<x_next>` per iteration
via the `Chain` emitter (previous value first, new value last — the
chaining convention).

**CollatzTraceGenerator** · middle · d2 — full 3n+1 trace; seeds
pre-screened per tier for total stopping time in the tier window.
Variants: `stopping_time`, `max_value`, `steps_to_below_seed`,
`parity_checksum` (count of odd steps — forces attention at every step).

**IteratedCompositionGenerator** · high · d3 — alternate two rational
maps f, g (linear and reciprocal-linear, chosen so the composition has
known finite order or is contractive with bounded denominators); apply N
times. Variants: `final_value`, `cycle_length`, `conjugacy_shortcut`
(composite: closed form via f∘g's order, then the value).

**DigitProcessGenerator** · elementary · d2 — iterate digit-sum /
digit-product / reverse-and-add on large seeds until a fixed point or
palindrome, seeds screened for tier-length trajectories. Variants:
`fixed_point`, `steps_to_fixed_point`, `happy_classification`
(`happy; reaches 1 at step 23` / `unhappy; enters the 4-cycle at step 15`).

### Strand A — Arithmetic marathons (elementary / middle)

**ArithmeticChainGenerator** · elementary · d2 — one running value
through N mixed operations ("start with 47; add 18; double it; subtract
35; …"), operations constructed backward so every intermediate is a
positive integer < 500. Variants: `integer_chain`, `fraction_chain`
(denominators kept in {2,3,4,6,12} by construction), `money_chain`
(exact cents), `missing_start` (given the end, invert the chain).

**BigExactDivisionGenerator** · middle · d2 — long division of a
tier-many-digit dividend by a two-digit divisor; one `DIV_STEP` per digit
brought down, so the chain length *is* the digit count (the dividend is
never manipulated whole — state is always the sub-divisor remainder).
Variants: `remainder_only` (short answer, whole chain required),
`quotient_digit_sum` (a checksum over every quotient digit — wrong if any
single step drifts), `repetend_length` (the decimal period of p/q for a
prime q screened so ord_q(10) lands in the tier window; the chain runs one
full period until the starting remainder returns). Amended from the
original `quotient_remainder`/`decimal_expansion`/`repeating_block` draft:
a tier-length quotient or repetend as the *answer* violates the
answers-are-short rule (§3), and terminating expansions cannot reach tier
depth with a bounded divisor, so the long outputs became checksums/lengths
and `decimal_expansion` was dropped.

**RadixMarathonGenerator** · middle · d3 — chained base conversions of a
value in [10^8, 10^9), digit by digit, fully on-chain: a decomposition
runs the value down to 0 (`RADIX_STEP|<v>|div b rem d|<v//b>`), and the
following Horner recomposition starts from that same 0
(`HORNER|<acc>|x b + d|<acc'>`), so decompose→recompose→decompose…
chains unbroken through every base. Bases 2..16, digits above 9 as
letters. Variants: `round_trip_check` (one base, `CHECK` equality with
the start; a single trip peaks near 60 links, so `d50`-only),
`chain_two` (a → 10 → b for any pair, screened to the window;
`d50`/`d100`), `base_tour` (a screened sequence of bases; all tiers).
Amended from the `chain_two`/`round_trip_check`/`arbitrary_pair` draft:
`arbitrary_pair` is `chain_two` (pairs were always arbitrary in 2..16),
and per-variant tier latitude reflects what bounded values can reach.

### Strand E — Number-theory chains (high / college)

**⟲ ExtendedEuclidGenerator** — tiered variants at **d50 only**, a
mathematical bound, not a scoping choice: Euclid's chain length n costs
Fibonacci-sized inputs (~φ^n), so the bounded-intermediates rule (§3)
caps chained gcd work near n = 70 (16-digit values, quotients mostly 1).
The legacy `extended_euclid` operation is untouched. New variants:
`bezout` (quotient sequences of mostly-1s built backward through
continuants, emitted as a chained remainder-pair trace
`EUCLID_DIV|(a, b)|q=<q>|(b, a-qb)`; Bezout coefficients computed and
spot-verified mod a small prime so no tier-length product ever
appears), `crt_chain` (10-16 small pairwise-coprime congruences folded
sequentially into the running solution, chained on the solution value).
Deeper number-theory tiers live in `ModExpLadderGenerator` and
`BigExactDivisionGenerator`, whose state is genuinely bounded.

**ModExpLadderGenerator** · high · d3 — square-and-multiply for
exponents with 40–200 bits of ladder, all mod m ≤ 500. Variants:
`final_residue`, `full_ladder_orderck` (checkpoint = running exponent
bits consumed), `fermat_route` (composite: reduce the exponent mod
ord(a) first, then a short ladder; answer states both).

**⟲ ContinuedFractionGenerator** — the retrofit that DOES reach every
tier: `sqrt_periodic` expands √d by the standard (P, Q) recurrence,
whose state is bounded by 2√d forever, with d screened so the period
(or the requested prefix) lands in the tier window; the milestone
invariant is Q's divisibility check `Q | d - P²` — recomputable at any
point. Near-Fibonacci rational expansions hit the same φ^n wall as
Euclid, so no deep rational-CF variant is added; `convergent_error`
is dropped for the same reason (p_k, q_k grow like continuants).

### Strand R — Recurrences and sums (high)

**RecurrenceUnrollGenerator** · high · d3 — unroll linear recurrences
term by term, state kept bounded mod m (Pisano-style) or by
alternating-sign construction. Variants: `term_n_mod_m`,
`pisano_period`, `two_term_mod` (Fibonacci-like), `matrix_check`
(composite: 2×2 matrix power closed form vs the unrolled value).

**PartialSumMarathonGenerator** · high · d3 — accumulate N terms with
the running sum re-derived against a closed form in a final `CHECK`.
Families chosen for *bounded* running sums (amended from the original
draft's "geometric" family: an exact geometric partial sum's
denominator grows like r^-N, so its rendering grows linearly with depth
and violates §3): `arithmetic` (Σ(a + kd), Gauss closed form),
`telescoping` (Σ 1/(k(k+1)) from k = s — every running sum reduces to a
two-small-integer fraction 1/s − 1/(s+k)), `first_exceed` (the smallest
N with an arithmetic partial sum above a stated bound, the crossing
screened into the tier window).

### Strand F — Financial schedules (middle / college)

**AmortizationScheduleGenerator** · college · d3 — full period-by-period
schedule, payments constructed so every interest/principal split is
exact cents (rates from the 2,5-smooth bank, principal built backward).
Variants: `balance_after_k`, `total_interest`, `payoff_period`,
`extra_payment` (one extra principal payment at period j; find the new
payoff period). One row step per period, reusing `annuity_generator.py`'s
existing `AMORT_ROW|k|interest=…|principal=…,balance=…` shape verbatim
(one op-code = one meaning; do not introduce a second amortization row
format).

**CompoundLedgerGenerator** · middle · d2 — a running account ledger:
deposits, withdrawals, periodic interest, N = tier events, exact cents
throughout. Interest stays exact for *any* balance by crediting r% of
the whole-dollar part only (D dollars → r·D cents, the floor a real
bank applies), stated in the problem header. Variants: `final_balance`,
`interest_earned`, `first_negative` (overdraft allowed and screened to
occur late), `statement_check` (composite: start + credits − debits +
interest re-derived against the running final, shown in a `CHECK`).

### Strand S — Machine traces (college)

**RegisterMachineTraceGenerator** · college · d3 — a 4–6 instruction
program over 2–3 registers (inc, dec, jump-if-zero), executed for tier-N
instruction steps; programs drawn from banks with known behavior
(counters, copiers, adders) so termination and the final state are
certain. Variants: `final_registers`, `halting_step`, `trace_invariant`
(r1 + r2 constant — the checkpoint invariant).

**TokenRewriteGenerator** · college · d3 — apply a confluent rewrite
system (2–4 rules over a 3-letter alphabet, chosen from banks with
proven termination) step by step to a fixed point. Variants:
`normal_form`, `step_count`, `rule_usage_count`.

### Strand C — Composed pipelines (high / college)

**PipelineCompositionGenerator** · college · d4 — 3–6 stages executed
serially, each stage a procedure the catalog already teaches (percent
change → unit conversion → ratio split → rounding to cents …); the
output of stage k is the input of stage k+1, marked
`PIPE_STAGE|k|<skill name>`. Carries the `skills` metadata list exactly
like `ScenarioGenerator`, so these records feed the
`judgment_composition_eval` config's serial half. Stage banks reuse
`applied_common.CONTEXTS`; the story never names the stage procedures
(the applied strand's rule, enforced by the same `METHOD_WORDS` scan).

### Strand V — Long-form critic records (middle / college)

**LedgerAuditGenerator** · middle · d3 — a *claimed* long trace (ledger,
iteration table, running sum) with exactly one injected error at a random
row k ≥ 15; the record verifies row by row (`VERIFY|k|ok`), flags the bad
row (`FLAG|k|<true arithmetic>`), redoes the tail from row k, and answers
`first error at row 73; correct final balance $418.20`. Same record
shapes as `ErrorSpottingGenerator`, stretched to tier length — the
long-form "catch the drift" skill made explicit. Variants over the three
underlying trace types; `error_free` control (verify all N rows, answer
`no errors; total confirmed`) at 20% weight.

**⟲ FractalIterationGenerator** — depth-tier retrofit, re-verify its
emission against the chaining convention first (the original draft's
"already chain correctly" claim was wrong for the Euclid family and
must not be assumed here). **ModularInverseGenerator retrofit dropped:**
it is the same algorithm as `ExtendedEuclidGenerator` with the same
φ^n depth cost; its tiered face is subsumed by the ⟲ ExtendedEuclid
`bezout` variant, and duplicating a d50-only retrofit adds nothing.

## 6. Band and difficulty summary

| Band | New classes | Extended |
|---|---:|---|
| elementary | 2 (DigitProcess d2, ArithmeticChain d2) | — |
| middle | 5 (IteratedAffineMap d2, CollatzTrace d2, BigExactDivision d2, RadixMarathon d3, CompoundLedger d2, LedgerAudit d3) | — |
| high | 5 (IteratedComposition d3, ModExpLadder d3, RecurrenceUnroll d3, PartialSumMarathon d3, PipelineComposition d4) | ContinuedFraction, ExtendedEuclid |
| college | 4 (AmortizationSchedule d3, RegisterMachineTrace d3, TokenRewrite d3) | FractalIteration, ModularInverse |

Total: **16 new classes, 4 extended**, ~60 operation variants before the
tier × modifier product. Difficulties listed at `d50`; +1/+2 at
`d100`/`d200` per §3.

## 7. Delivery order

One generator per commit, tests in the same commit; each phase ends with
the full suite, the capacity probe on the phase's classes, a seeded
200-row build per class with zero errors, and `--check`-clean docs.

| Phase | Deliverable | Why this order |
|---|---|---|
| 0 | `depth_common.py`, `tests/depth_oracle.py`, conventions test with violating fixtures, DESIGN.md block, `MILESTONE` op-code registered | every later class chains, checkpoints, and is policed the same way |
| 1 | ArithmeticChain, DigitProcess, IteratedAffineMap, CollatzTrace | cheapest; proves `chain()`/checkpoint machinery end to end |
| 2 | BigExactDivision, RadixMarathon, CompoundLedger | marathons over familiar arithmetic |
| 3 | ExtendedEuclid ⟲, ContinuedFraction ⟲, ModExpLadder, ModularInverse ⟲ | number-theory chains; worst-case-length constructions |
| 4 | RecurrenceUnroll, PartialSumMarathon, IteratedComposition, FractalIteration ⟲ | closed-form cross-check oracles |
| 5 | AmortizationSchedule, RegisterMachineTrace, TokenRewrite | exact-cents and machine-trace banks |
| 6 | PipelineComposition (needs applied strand's context bank + skills plumbing), LedgerAudit | composition + the long critic record |
| 7 | Phrasing sweep to 3–5 templates; full capacity probe; README inventory/coverage bullet; regenerate `PROBLEM_TYPES.md`, `OPCODES.md`; HF dataset-card paragraph (state the tier suffixes and that long records are token-weighted in the size configs); consider a `depth_eval` held-out config (d200-only, mirroring `judgment_composition_eval`) | close-out |

## 8. Out of scope, and why

- **Approximate/iterative numerics at depth** (Newton to convergence,
  gradient descent): step counts to a tolerance are not exactly
  predictable and violate exactness; the existing short forms suffice.
- **Depth via bigger numbers** (1000-digit multiplication): that is digit
  grinding, exactly what AGENTS.md bans; every class here bounds its
  intermediates instead.
- **Interactive/backtracking search at depth** (long DPLL, deep game
  trees): trace length depends on search order and is hard to tier;
  revisit after the capacity backlog in `plans/handoff.md`.
- **Retrofitting depth tiers onto the whole catalog**: only the four ⟲
  classes have naturally serial traces; forcing tiers elsewhere would
  produce padding, not depth.

## 9. Decisions taken in this plan (change here, not per generator)

1. Depth = dependency-chain length, measured structurally by the
   conventions test; tier floors 40/85/170.
2. Tier in the operation suffix (`_d50`/`_d100`/`_d200`); difficulty
   +1/+2 at the higher tiers, capped at 5.
3. Bounded intermediates always; the four bounded-state patterns in §3
   are the only sanctioned constructions.
4. `MILESTONE` recomputes an invariant; `checkpointed` default at
   `d100`+, `plain` default at `d50`.
5. Answers are short; traces are long; no all-intermediates answers.
6. `PipelineCompositionGenerator` carries `skills` metadata and obeys the
   applied strand's no-method-words rule; everything else in this plan
   may name its procedure (these are drills, not judgment tasks).
7. Record size cap 16k characters, enforced by the conventions test.

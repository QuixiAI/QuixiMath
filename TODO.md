# TODO

Follow-ups from the full problem-type review (all 476 types reviewed; see git
history). Standard bar for every new generator: exact arithmetic only,
human-like steps, pipe-safe fields, A0 answer conventions, A9 oracle test that
recomputes the answer from the problem text, near-infinite unique problems,
regenerate PROBLEM_TYPES.md / OPCODES.md.

## High-value, cheap to build

- [ ] **PolynomialInequalityGenerator** (high) — quadratic/polynomial/rational
  inequalities via sign charts. The inequality thread currently stops at
  one-step, two-step, compound, and absolute-value. Variants: factored
  quadratic `(x-2)(x+3) > 0`, unfactored quadratic (factor first), cubic with
  three roots, rational `(x-a)/(x-b) ≤ 0` (exclude the pole from closed
  intervals). Steps: find zeros, build sign chart, test each interval, read
  off the solution. Answers in interval notation; reuse TRY/ACCEPT/REJECT and
  ZERO_PRODUCT op-codes where they fit.
- [ ] **MasterTheoremGenerator** (college) — recurrence complexity:
  `T(n) = aT(n/b) + n^k` → `Θ(...)`. Compute log_b(a) exactly (choose a = b^k
  or clean powers so the comparison is exact), identify the case, state the
  bound. Also a subtract-and-conquer variant `T(n) = T(n-1) + n^k`. Composite
  answer: case + bound, e.g. `case 1; Θ(n^2)`.
- [ ] **TelescopingGenerator** (high/college) — telescoping sums and products.
  Variants: `Σ 1/(k(k+d))` (partial fractions, reuse the existing
  partial-fraction op-codes), `Σ (√(k+1) - √k)`, product `Π (k/(k+1))`,
  finite `Σ_{k=m}^{n}` with exact rational answers. Show the cancellation
  explicitly (first surviving term minus last).
- [ ] **TwoSampleTestGenerator** (high/college) — two-sample t and
  two-proportion z tests. Same framework as HypothesisTestGenerator: supplied
  critical values, exact-friendly numbers (perfect-square n, clean pooled
  variance), composite verdict `reject H0 (2.5 > 1.96)`. Variants: stat-only
  and decision.
- [ ] **EquilibriumICEGenerator** (high, chemistry) — ICE tables. Variants:
  compute K from equilibrium concentrations; given K and initial
  concentrations, solve for x (rig quadratics to factor or be perfect
  squares); reaction-quotient Q vs K direction prediction (composite answer
  with the comparison). Steps: ICE rows, substitute into K expression, solve
  exactly.

## Worth considering

- [ ] **SeparablePDEGenerator** (graduate) — heat equation
  `u_t = α u_xx` on [0, L] with `u(x,0) = sin(nπx/L)` (single-mode initial
  data → exact coefficient decay), and wave equation via d'Alembert with
  polynomial initial data evaluated at exact points. Connects the existing
  Fourier-series and second-order-ODE generators. Only major undergrad math
  subject with zero representation.
- [ ] **InductionVerifyGenerator** (high/college) — verify P(1) numerically,
  then verify P(k) → P(k+1) algebraically for sum formulas
  (`Σk = n(n+1)/2`, `Σk²`, `Σ odd = n²`, geometric sums, divisibility claims
  like `6 | n³ - n`). Answer: composite (base case value; inductive-step
  identity confirmed).
- [ ] **QRDecompositionGenerator** (college) — QR via Gram-Schmidt; extend the
  existing GramSchmidtGenerator machinery; use Pythagorean-friendly columns so
  norms stay rational. Answer: Q and R; check step `Q^T Q = I`.
- [ ] **CholeskyGenerator** (college) — build A = L L^T from integer L (same
  trick PositiveDefiniteGenerator already uses), then recover L step by step.
  Check step: L L^T = A.
- [ ] **CountingClassicsGenerator** (college) — pigeonhole (minimum n to
  guarantee k in one of m boxes), Catalan numbers (balanced sequences, lattice
  paths; compute C_n = C(2n,n)/(n+1) exactly), binomial identities (evaluate
  both sides of Vandermonde/hockey-stick instances). Complements
  stars-and-bars and derangements.

## Phrasing diversity (bigger lever than new topics)

- [ ] Sweep higher-tier generators for single-template problem statements and
  add 3–5 phrasings each, including word-problem framings for calculus/stats
  ("A tank drains at a rate of..."). Review criterion: "the problem statement
  should be somewhat diverse so the model can learn to identify the problem."
  Most high/college/graduate generators currently use one fixed sentence
  frame (e.g. every TangentLineGenerator problem reads "Find the tangent line
  to ... at x = ..."). Elementary generators are the model to copy.
  Suggested order: derivatives/integrals family, statistics family, physics
  formula families. Keep oracle tests in sync (parse all phrasings).

## Capacity skew

- [ ] Audit per-type capacity: probe every generator for distinct-problem
  count (script exists in the review history: sample ~2000, count distinct
  problem texts). Flag anything under ~1000.
- [ ] Widen the flagged generators — same treatment QuantumGate (12 → 170+,
  gate sequences) and LegendreConstruction (2 → 40, evaluation points) got
  during the review. Known small-ish spaces from probing: TrigEquation (~33),
  LHopital (~52), SpecialRightTriangle (~52), RegularPolygonArea (~60),
  TrigIdentityEval (~45), SolidRevolution (~26), SeparableODE (~41),
  IntegrationByParts (~48), OptimizationGenerator (~48), Projector (~11),
  VonNeumannEntropy (~17). Tier distribution is fine
  (38 elem / 65 middle / 150 high / 137 college / 96 graduate) but per-type
  capacity inverts it: elementary types generate millions, several graduate
  types sit in the 50–150 range. If the training mix samples heavily per
  type, the top tiers will repeat.

# Repository Guidelines

## Project Structure & Module Organization
- Core entrypoint: `quixi_math_datagen.py` orchestrates dataset builds and samples, instantiating generator classes and handling `--generators` filtering. Mixed-number ops include a random wrapper; factors/GCF/LCM, conversions/comparisons, and order-of-operations generators are wired in.
- Base contract: `base_generator.py` defines `ProblemGenerator.generate()` with required keys (`problem_id`, `operation`, `problem`, `steps`, `final_answer`); `steps` are pipe-delimited strings built with `helpers.step()` and `steps[-1]` must be exactly `Z|<final_answer>`. The pipeline stamps `grade_level`/`difficulty` from `curriculum.py` after `generate()` returns (a generator may emit either key itself to override).
- Generators: `generators/` holds one file per skill (e.g., `multi_digit_addition_generator.py`, `long_division_generator.py`). Add new classes there and to `ALL_GENERATORS`.
- **CRITICAL:** Every new generator class MUST be registered in THREE places:
  1. Add an import statement at the top of `quixi_math_datagen.py` (e.g., `from generators.my_new_generator import MyNewGenerator`)
  2. Add an instance to the `ALL_GENERATORS` list (e.g., `MyNewGenerator()`)
  3. Add a `curriculum.CURRICULUM` entry for the class (grade_level + difficulty) — enforced by `tests/test_datagen_pipeline.py`
  Generators not in `ALL_GENERATORS` will NOT appear in `--sample` output or dataset generation!
- After adding or changing op-codes, regenerate the legend: `uv run python tools/gen_opcode_legend.py` (check freshness with `--check`). The vocabulary is descriptive and organic — new op-codes are fine, but one op-code must keep one field meaning. Reuse an existing code only when the field semantics match.
- Tests: `tests/` mirrors generator names (`test_long_division_generator.py`, etc.) using `unittest`. Keep new tests co-located with matching generator names.
- Catalog: `PROBLEM_TYPES.md` is the authoritative generated catalog and count of problem types. Regenerate it after adding or materially changing a generator.
- Artifacts: JSONL datasets write to repo root unless you pass `-o`. Avoid committing large generated files.

## Build, Test, and Development Commands
- **Virtual environment:** Prefer `uv run python ...` for commands so the project environment is selected explicitly. If not using `uv run`, activate the venv first with `source .venv/bin/activate`.
- Sample run: `uv run python quixi_math_datagen.py --sample` (add `--generators ClassA,ClassB` to limit; add `-s` to fix seed).
- Full dataset: `uv run python quixi_math_datagen.py -n 50000 -o quixi_math_50000.jsonl` (optionally add `--generators ...` and `-s`).
- Builds sample equally per skill (class); override with `--weights "ClassA=2.5,ClassB=0.5"` or a JSON file. Exact `(operation, problem)` repeats are skipped unless `--allow-duplicates`; a per-generator stats table prints at the end.
- Default dataset filename when `-o` omitted: `quixi_math_<n>.jsonl`.
- Tests (all): `uv run python -m unittest discover tests` (or `uv run pytest tests` with the dev group installed).
- Tests (focused): `uv run python -m unittest tests.test_quadratic_generator`.
- Op-code legend: `uv run python tools/gen_opcode_legend.py` regenerates `OPCODES.md`; `--check` verifies freshness.
- Problem catalog: `uv run python tools/gen_problem_types.py` regenerates the user-facing `PROBLEM_TYPES.md` (one entry per generator with a worked example); `--check` verifies freshness. Regenerate after adding or changing a generator.

## Generator Design Principles
- Every arithmetic action should be explicit. If a human would write it in the margin, emit a step for it.
- Steps should be human-legible: show alignment, carries/borrows, trial candidates, rejected paths, checks, and current-expression rewrites when those are part of the pencil-and-paper procedure.
- Verify before answering where natural: substitute back, apply an inverse operation, check a magnitude, or emit another compact `CHECK` step before `Z|`.
- Do not require unstated lookups. Any trig value, z/t/chi-square critical value, logarithm, normal CDF value, or other table/calculator value must be supplied in the problem text, avoided by construction, or left symbolic/exact.
- Use hand-friendly operands. The procedure should be the hard part, not digit grinding.
- If the answer space is tiny, make `final_answer` composite enough to grade reliably rather than a coin-flip label.
- Construct data backward from exact answers: use triples, perfect squares, denominators dividing powers of 2 and 5 for `dec()`, dyadic probabilities, divisible coefficients, or exact symbolic forms. `dec(Fraction)` is only valid for terminating decimals; otherwise render a reduced fraction or constrain the inputs.
- Pipe-safety is mandatory: no step field may contain raw ASCII `|`. Use alternatives such as `abs(r)` or `‖u‖`. Keep steps to at most four payload fields after the op-code.

## Coding Style & Naming Conventions
- Python 3.9+; 4-space indentation; prefer explicit, side-effect-free helpers.
- Module/file naming: snake_case for modules and functions; UpperCamelCase for classes; constants in ALL_CAPS when needed.
- Determinism only when a seed is provided; otherwise allow natural randomness. Always emit `Z|` as the final step. For mixed numbers, always emit `F` and `IMPROPER_TO_MIX` when applicable; for percent/conversion outputs avoid scientific notation; for factor/gcd/lcm flows include human-readable steps (trial division, Euclid steps, LCD comparisons); for order-of-operations include `REWRITE` steps after each precedence move.
- Follow existing patterns (e.g., `op_symbol` for operator-specific generators); keep error messages concise and informative.

## Testing Guidelines
- Add/extend `unittest` cases in `tests/` for each generator; mirror file names.
- **Oracle cross-checks (A9, required):** every generator's tests must include
  an oracle that recomputes `final_answer` **from the problem text alone**
  (parse the problem, solve it independently with exact arithmetic —
  `fractions.Fraction`, integer math — and compare). The generator agreeing
  with itself is not verification; prefer a different route when practical
  (brute-force enumeration, identity checks, numeric finite differences or
  quadrature, matrix-product verification, etc.). Also verify the arithmetic inside emitted
  steps (A/S/M/D/E/ROOT/CHECK fields) where practical. Use sympy (dev-dep)
  only when stdlib-exact arithmetic genuinely can't express the oracle.
- Answer strings must follow the conventions in DESIGN.md ("Answer Format
  Conventions") — graders depend on exact equality with the `Z|` payload.
- Use deterministic seeds in tests to stabilize expectations; assert both `steps` content and final answers where possible. Patch `random` if you need specific borrow/carry scenarios.
- Include pipe-safety and render-sanity tests for generated examples. Common regressions are stray `|`, `1x`, `-1x`, `^1`, `+ 0`, `--`, or parser regexes that swallow a sentence period after a decimal.
- During generator development, run the focused test first; before raising a PR or handing off, run `uv run python -m unittest discover tests`.
- Build a restricted seeded sample of roughly 200 examples, e.g. `uv run python quixi_math_datagen.py -n 200 -o /tmp/foo.jsonl -s 7 --generators FooGenerator`, and inspect both the stats table and sample output. Generator errors must be zero; high duplicate skips can be acceptable for intentionally small exact problem spaces, but should be noticed.
- Manual check: `uv run python quixi_math_datagen.py --sample --generators <GeneratorName>` and verify the steps match human pencil-and-paper workflow (alignment, carries/borrows, etc.).
- For new skills: define op-codes upfront, keep every arithmetic action explicit (no hidden mental math), and ensure rewrites show the current expression after each operation.

## Commit & Pull Request Guidelines
- Commit messages: short present-tense summaries (e.g., `add percent generator edge cases`, `fix quadratic step formatting`), matching existing history.
- Commit generator work with sole author `Eric Hartford <eric@quixi.ai>` and no `Co-Authored-By` trailer: `git commit --author="Eric Hartford <eric@quixi.ai>" -m "add foo generator"`.
- Pull requests should include: purpose/summary, key commands run (tests, sample or dataset generation), sample output snippet or file path, and any linked issues.
- Screenshot/JSON snippets are welcome when changes affect output formatting or op-code ordering.
- Keep diffs minimal and grouped by concern (generator logic vs. tests vs. docs); avoid drive-by refactors unless necessary.

## Security & Configuration Tips
- Avoid writing large datasets to the repo by default; pass `-o /tmp/...` for local experiments.
- Do not log sensitive paths or environment details; printed output should be limited to sample/problem data and high-level progress.
- Keep `pyproject.toml` dependencies minimal (currently stdlib); if adding deps, document why and pin versions.

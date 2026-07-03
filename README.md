# Dolphin Math Data Generator
<img width="410" alt="image" src="https://github.com/user-attachments/assets/f8a5d3d2-7820-4f7c-a5d3-fbac667e7084" />

## Purpose

This project generates synthetic math problems covering various arithmetic, algebra, geometry, and statistics topics. Crucially, it also generates detailed, step-by-step solutions intended to mimic the process a human would follow when solving the problem manually (like a "visible scratchpad").

The output is designed for training language models to perform multi-step mathematical reasoning.

It works for both SFT and RL. You should generate separate datasets for SFT and RL. SFT teaches it the syntax, RL teaches it to git gud at it.

## Features

### Elementary (Grades 3-5) — 34 Problem Types

#### Basic Arithmetic
- **Long Division** — with remainder, showing divide/multiply/subtract/bring-down cycle
- **Multi-digit Addition** — standard column algorithm with carries
- **Multi-digit Subtraction** — standard column algorithm with borrows
- **Multi-digit Multiplication** — partial products method
- **Mixed Number Operations** — all four operations (+, -, *, /) with LCD, simplification
- **Fraction Comparison** — find common denominator and compare
- **Fraction/Decimal/Percent Conversions** — bidirectional conversions
- **Decimal Addition/Subtraction** — column alignment with decimal points
- **Decimal Multiplication** — integer multiplication then decimal placement
- **Decimal Division** — shift decimals, long division, place decimal in quotient
- **Fraction Operations** — add, subtract, multiply, divide with LCD and simplification

#### Factors & Multiples
- **Finding All Factors** — trial division with factor pairs
- **Prime Factorization** — factor tree method
- **GCF (Greatest Common Factor)** — Euclidean algorithm
- **LCM (Least Common Multiple)** — via GCD formula

#### Order of Operations
- **PEMDAS Problems** — with rewrite steps showing work

#### Basic Geometry
- **Perimeter/Area of Rectangles, Squares, Triangles, Parallelograms, Trapezoids**
- **Perimeter of General Polygons** — sum of all sides
- **Volume of Rectangular Prisms**

#### Number Sense
- **Place Value and Rounding** — whole numbers and decimals
- **Comparing/Ordering Numbers** — whole numbers and decimals
- **Divisibility Rules** — prime/composite classification

#### Units & Measurement
- **Unit Conversions** — length, weight, capacity, time, money

#### Data & Probability
- **Mean, Median, Mode** — for small datasets
- **Simple Probability** — single event with uniform outcomes
- **Graph Interpretation** — bar charts, line graphs, pictographs

#### Tools/Methods
- **Abacus-style Addition** — column-by-column with carries

---

### Middle School (Grades 6-8) — 41 Problem Types

#### Ratios & Proportions
- **Unit Rate Calculations** — find rate per unit
- **Unit Rate from Tables** — extract rate from data tables
- **Scaling Problems** — maps, blueprints, models
- **Similar Figures** — find missing sides using scale factors
- **Proportional Relationships** — solve proportions

#### Integer Operations
- **Adding/Subtracting Integers** — with number line reasoning
- **Multiplying/Dividing Integers** — sign rules

#### Expressions & Equations
- **One-step Equations** — all operations (x+a=b, ax=b, etc.)
- **Two-step Equations** — (ax+b=c, a(x+b)=c, etc.)
- **One-step Inequalities** — with inequality flip for negative coefficients
- **Two-step Inequalities** — with proper sign handling
- **Simple Linear Equations** — (ax + b = c)
- **Complex Linear Equations** — variables on both sides (ax + b = cx + d)
- **Simplifying Expressions** — distribution and combining like terms
- **Evaluating Expressions** — variable substitution

#### Exponents & Roots
- **Exponent Evaluation** — compute powers like 2^5, (-3)^4
- **Exponent Rules** — product, quotient, power, negative, zero exponent
- **Scientific Notation** — convert to/from, operations
- **Square Roots** — perfect squares
- **Cube Roots** — perfect cubes
- **Simplifying Radicals** — √72 → 6√2

#### Geometry
- **Angle Relationships** — complementary, supplementary, vertical (numeric and algebraic)
- **Angles with Parallel Lines** — corresponding, alternate interior/exterior, co-interior
- **Triangle Angle Sum** — find missing angle
- **Exterior Angle Theorem**
- **Circle Area and Circumference** — with π symbol or decimal
- **Volume of Prisms** — rectangular and triangular
- **Volume of Cylinders**
- **Surface Area of Prisms**
- **Surface Area of Cylinders**
- **Pythagorean Theorem — Find Hypotenuse**
- **Pythagorean Theorem — Find Leg**
- **Pythagorean Word Problems** — ladders, distances, etc.

#### Statistics
- **Mean (Average)** — sum and divide with steps
- **Median** — sort and find middle
- **Mode** — frequency counting (unimodal, bimodal, no mode)
- **Range** — max minus min
- **Mean Absolute Deviation (MAD)**

#### Probability
- **Simple Probability** — P = favorable/total
- **Compound Probability — Independent Events** — coin flips, dice
- **Compound Probability — Dependent Events** — drawing without replacement

---

### High School — 6 Problem Types (more coming)

#### Algebra
- **Quadratic Equations** — using quadratic formula with discriminant
- **Percentage Problems** — find part, percent, or whole

---

## Usage

### Generating Samples

To see one sample output from each generator type:

```bash
python dolphin_math_datagen.py --sample
```

You can optionally specify a random seed using `-s` or `--seed`.

Limit to specific generators (comma-separated class names):
```bash
python dolphin_math_datagen.py --sample --generators MultiDigitAdditionGenerator,LongDivisionGenerator
```

### Generating a Dataset

To generate a full dataset file in JSON Lines format:

```bash
python dolphin_math_datagen.py -n <number_of_examples> -o <output_file.jsonl>
```

You can restrict generation to a subset of generators:
```bash
python dolphin_math_datagen.py -n 5000 -o subset.jsonl --generators MultiDigitAdditionGenerator,DecimalMultGenerator
```

Example: Generate 50,000 examples with seed 123:
```bash
# Specify output file explicitly:
python dolphin_math_datagen.py -n 50000 -o my_dataset.jsonl -s 123

# Use default output filename (dolphin_math_50000.jsonl):
python dolphin_math_datagen.py -n 50000 -s 123
```

Default values are 10,000 examples (outputting to `dolphin_math_10000.jsonl` by default if `-o` is omitted). Omit `-s/--seed` for non-deterministic data; provide a seed to make runs reproducible byte-for-byte.

### Sampling, Weights, and Deduplication

Dataset builds sample **equally per skill** (generator class): variant instances of one class — e.g. the four `FractionOpGenerator` ops — share a single slot, so no skill is over-represented just because it has more instances. Override individual skill weights with `--weights` (unlisted skills keep weight 1.0):

```bash
# inline spec
python dolphin_math_datagen.py -n 10000 --weights "QuadraticGenerator=3,MeanGenerator=0.5"

# or a JSON file: {"QuadraticGenerator": 3}
python dolphin_math_datagen.py -n 10000 --weights weights.json
```

Exact repeats of `(operation, problem)` are skipped by default; pass `--allow-duplicates` to keep them. Each build prints a per-generator stats table (emitted / duplicates skipped / errors) and stops early with a warning if the selected skills' problem space is exhausted before reaching `-n`.

Note: `MixedNumberOperationsRandom` is excluded from the default pool (it duplicates the four `MixedNumberOperationGenerator` variants) but can still be requested explicitly via `--generators`.

### Running Tests

Unit tests are provided for each generator. To run all tests:

```bash
python -m unittest discover tests
# or, with the dev dependency group installed (uv sync):
uv run pytest tests
```

---

## Output Format

Each line of the generated JSONL is one problem:

```json
{
  "problem_id": "1f8b6be5-...",
  "operation": "long_division",
  "problem": "1834 / 5",
  "steps": ["D|18|5|3", "M|3|5|15", "S|18|15|3", "B|3|3|33", "...", "Z|366 R4"],
  "final_answer": "366 R4",
  "grade_level": "elementary",
  "difficulty": 3
}
```

- `steps` — the visible scratchpad: pipe-delimited op-code strings (`CODE|field|field|...`, up to 4 payload fields), ending with `Z|<final_answer>`.
- `grade_level` (`elementary` / `middle` / `high`) and `difficulty` (coarse 1-5 tier) are stamped from the per-class table in `curriculum.py`; a generator may emit either key itself to override (e.g. difficulty computed from its operands).

## Op-Code Legend

The full legend of op-codes in use lives in [OPCODES.md](OPCODES.md) — a **generated** file; regenerate it with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and the legend is *descriptive*, not prescriptive. The pipeline validates only step *structure* (op-code present, field count, final `Z|` matching `final_answer`) — never the vocabulary. When writing generators, stay consistent within a generator and keep every step human-legible: the same cues a person would write on paper.

---

## Curriculum Progress

| Category | Implemented | Remaining |
|----------|-------------|-----------|
| Elementary (3-5) | 34 | 0 |
| Middle School (6-8) | 41 | 0 |
| Algebra 1 | 4 | 48 |
| Geometry | 1 | 28 |
| Algebra 2 | 1 | 40 |
| Precalculus | 0 | 38 |
| AP Statistics | 0 | 26 |
| AP Calculus AB | 0 | 38 |
| AP Calculus BC | 0 | 24 |
| **Total** | **81** | **~243** |

See [TODO.md](TODO.md) for the complete curriculum roadmap.

---

## Dependencies

- Python 3.9+ (uses only standard library)
- No external packages required

---

## Project Structure

```
dolphin-math/
├── dolphin_math_datagen.py   # Main CLI and generator orchestration
├── base_generator.py         # Abstract base class for generators
├── helpers.py                # Utility functions (step formatter, UUID)
├── generators/               # All generator implementations
│   ├── __init__.py
│   ├── long_division_generator.py
│   ├── fraction_op_generator.py
│   └── ... (51 generator files)
├── tests/                    # Unit tests for all generators
│   ├── __init__.py
│   ├── test_long_division_generator.py
│   └── ... (51 test files)
├── README.md                 # This file
├── AGENTS.md                 # Guidelines for AI coding agents
├── TODO.md                   # Curriculum roadmap
└── pyproject.toml           # Package configuration
```

---

## Contributing

When adding a new generator:

1. Create `generators/my_new_generator.py` extending `ProblemGenerator`
2. Create `tests/test_my_new_generator.py` with unit tests
3. **IMPORTANT**: Add import and instance to `ALL_GENERATORS` in `dolphin_math_datagen.py`
4. Delete the item's line from `TODO.md` (it's a pure backlog — only unimplemented skills are listed)
5. Run `python dolphin_math_datagen.py --sample --generators MyNewGenerator` to verify output
6. Run `python -m unittest discover tests` to ensure all tests pass

# Dolphin Math Training Plan

This document describes how to size and phase Dolphin Math data when mixing it
into a larger general pretraining corpus. The goal is not to make Dolphin Math
the whole math diet. The goal is to provide dense, high-quality scratchpad
examples that teach exact step discipline, arithmetic bookkeeping, verification,
and canonical answer formatting.

## Summary Recommendation

For a serious first full run after `TODO.md` is complete, generate about
**1-3B Dolphin Math tokens**, likely **5-15M examples** once advanced generators
produce longer scratchpads.

Use a **progressive interleaved curriculum**:

- Start with mostly elementary and middle-school examples.
- Gradually raise the share of high-school, college, and graduate topics.
- Never drop earlier skills entirely; advanced math still depends on arithmetic,
  fractions, signs, simplification, and equation solving.

Do not train as one hard boundary sequence such as "all elementary, then all
middle, then all advanced." That creates avoidable distribution shifts and can
make basic skills fade during later training.

## Data Scale

Current default repo output is small per example: a rough local sample measured
about **100 tokens/example** using `len(json) / 4`. Advanced TODO items will be
longer because they should include `CHECK` steps, trial/reject/accept traces,
tables, symbolic rewrites, and multi-stage computations. Plan around
**150-250 tokens/example** for the mature dataset.

Recommended tiers:

| Tier | Examples per skill | Approx. total scale | Use |
| --- | ---: | ---: | --- |
| Smoke test | 100-500 | 10-50M tokens | Pipeline validation and format checks |
| Minimum useful | 1k-2k | 100-300M tokens | Small ablations and sanity training |
| Recommended v1 | 5k-10k | 1-3B tokens | First serious pretraining mixture |
| Stretch | 20k+ | 3-6B tokens | Only if generator diversity is strong |

Avoid padding tiny finite problem spaces with duplicates. If a generator
exhausts its useful space, downweight it or treat it as garnish.

## Mixture Share

When Dolphin Math is included in a larger general pretraining dataset:

| Training setting | Dolphin Math share |
| --- | ---: |
| Broad general pretraining | 0.5-3% of total tokens |
| Math-heavy midtraining or final phase | 5-10% of total tokens |
| Math-specialized model | Higher is possible, but mix with natural math text, code, textbooks, and web math |

Synthetic scratchpads are high-signal but narrow-format. They should complement
natural mathematical prose, code, proofs, textbook explanations, and real problem
solutions.

## Curriculum Schedule

Use `grade_level` and `difficulty` metadata to construct phase-specific sampling
weights. The percentages below are the composition of the Dolphin Math subset,
not the whole pretraining corpus.

| Training progress | Elementary | Middle | High | College | Graduate |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0-20% | 80% | 20% | 0% | 0% | 0% |
| 20-45% | 50% | 40% | 10% | 0% | 0% |
| 45-70% | 20% | 40% | 35% | 5% | 0% |
| 70-90% | 10% | 20% | 40% | 25% | 5% |
| 90-100% | 10% | 15% | 30% | 30% | 15% |

Within each grade band, phase difficulty from easy to hard:

- Early phases: mostly difficulty 1-3.
- Middle phases: mix difficulty 2-4.
- Later phases: emphasize difficulty 4-5, but keep some easy examples for
  arithmetic replay.

One practical starting point is:

| Phase | Difficulty 1 | Difficulty 2 | Difficulty 3 | Difficulty 4 | Difficulty 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0-20% | 25% | 35% | 30% | 10% | 0% |
| 20-45% | 10% | 25% | 35% | 25% | 5% |
| 45-70% | 5% | 15% | 30% | 35% | 15% |
| 70-90% | 5% | 10% | 20% | 40% | 25% |
| 90-100% | 5% | 10% | 20% | 35% | 30% |

## Late-Phase Emphasis

Reserve more of the final phases for examples that teach robust reasoning
habits:

- `CHECK` steps from self-verification.
- Trial/reject/accept traces for factoring, rational roots, search procedures,
  and candidate testing.
- Composite problems that chain 2-3 skills.
- Word problems with irrelevant quantities and explicit selection of useful
  data.
- Error-spotting and fill-in-the-missing-step formats after their record format
  is designed.

These examples are more valuable late because the model has already learned the
basic syntax and arithmetic operations.

## Serialization Format

Do not train directly on raw JSON unless the model is expected to emit JSON.
Use a stable text serialization that keeps metadata available without making the
JSON syntax the main task.

Example:

```text
<math grade="middle" difficulty="4" skill="TwoStepEquationGenerator">
Problem: Solve 3x + 5 = 20.
Work:
SETUP|3x + 5 = 20
SUBTRACT|20|5|15
REWRITE|3x = 15
DIVIDE|15|3|5
CHECK|3*5 + 5 = 20
Answer: x = 5
</math>
```

Keep the record shape stable across phases. The model should learn one
consistent scratchpad interface.

## Evaluation Holds

Before mixing data into training, reserve holdouts:

- Hold out 1-2% per skill and difficulty.
- Keep a separate adversarial holdout for edge cases: carries, borrows,
  negative coefficients, extraneous roots, undefined denominators, unit
  mismatches, and multi-solution answers.
- Deduplicate holdouts against training by exact `(operation, problem)` and, for
  word problems, by normalized numeric structure where possible.

Track:

- Exact `final_answer` match.
- Last-step validity: final step equals `Z|<final_answer>` in source records.
- Per-skill accuracy.
- Per-grade and per-difficulty accuracy.
- Step-format validity.
- Presence and correctness of `CHECK` steps where expected.

## Ablation Plan

Do not commit the full budget before measuring. Run small ablations first:

1. **100M Dolphin tokens:** verifies that the serialization, tokenizer behavior,
   and phase mixer are not broken.
2. **300M Dolphin tokens:** enough to see early skill movement and regressions.
3. **1B Dolphin tokens:** first meaningful comparison of curriculum schedules.
4. **1-3B Dolphin tokens:** recommended v1 production scale if ablations help.

Compare at least:

- Randomly mixed Dolphin examples.
- Strict easy-to-hard ordering.
- Progressive interleaving as described above.
- Progressive interleaving plus late-phase `CHECK`/composite upweighting.

The expected winner is progressive interleaving. Strict easy-to-hard may help
early but is more likely to create phase-boundary artifacts.

## Implementation Notes

The generator already stamps `grade_level` and `difficulty` from
`curriculum.py`. A training mixer should use those fields directly.

Useful generation commands:

```bash
source .venv/bin/activate
python dolphin_math_datagen.py --sample
python dolphin_math_datagen.py -n 1000000 -o /tmp/dolphin_math_1m.jsonl -s 123
python dolphin_math_datagen.py -n 1000000 -o /tmp/dolphin_math_1m.jsonl --weights "QuadraticGenerator=3,MeanGenerator=0.5" -s 123
```

For large builds:

- Write outputs outside the repo, for example under `/tmp` or a dataset volume.
- Save the seed, generator commit, command, and weight config.
- Save per-generator stats from the build output.
- Keep the exact train/validation split manifests.

## External Reference Points

These are scale reference points, not direct prescriptions:

- DeepSeekMath continued pretraining used 120B math-related tokens mixed with
  natural language and code:
  <https://arxiv.org/abs/2402.03300>
- OpenMathInstruct-2 built 14M question-solution pairs and emphasized question
  diversity and solution format:
  <https://arxiv.org/abs/2410.01560>
- Llemma continued pretraining used a broad math mixture rather than a single
  synthetic format:
  <https://arxiv.org/abs/2310.10631>
- Chinchilla-style dense-model planning is often summarized around 20-25 tokens
  per parameter, but Dolphin Math should be a targeted slice of that budget:
  <https://arxiv.org/html/2404.10102v1>
- Continued-pretraining work supports shifting toward more targeted data later
  in training while preserving enough base-distribution replay:
  <https://arxiv.org/html/2407.07263v1>


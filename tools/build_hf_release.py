#!/usr/bin/env python3
"""Build a Hugging Face-compatible QuixiMath dataset release.

The builder streams generated examples directly to sharded Parquet files using
the size-config layout described in plans/dataset_plan.md. Smaller configs are prefix
subsets of larger configs within each split.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quixi_math_datagen import (  # noqa: E402
    _instance_label,
    group_into_skills,
    resolve_pool,
    validate_example,
)
from curriculum import stamp_metadata  # noqa: E402


#: A standalone, held-out eval config carved from records that carry a
#: non-null ``skills`` list (currently only ``ScenarioGenerator``'s
#: multi-part records; ``plans/applied_plan.md`` §9). It is generated in a
#: dedicated pass after the main splits (never mixed into their nested
#: prefix-subset logic below) so its rows never overlap the training data —
#: it measures compositional transfer, not execution of a single procedure.
JUDGMENT_EVAL_CONFIG = "judgment_composition_eval"

DEFAULT_CONFIGS = {
    "preview": {"train": 50_000},
    "10M_tokens": {"train": 100_000, "validation": 10_000},
    "100M_tokens": {"train": 800_000, "validation": 50_000, "test": 50_000},
    "1B_tokens": {"train": 8_800_000, "validation": 100_000, "test": 100_000},
    JUDGMENT_EVAL_CONFIG: {"test": 5_000},
}

SMOKE_CONFIGS = {
    "preview": {"train": 200},
    "10M_tokens": {"train": 400, "validation": 100},
    "100M_tokens": {"train": 800, "validation": 150, "test": 150},
    "1B_tokens": {"train": 1_200, "validation": 200, "test": 200},
    JUDGMENT_EVAL_CONFIG: {"test": 60},
}

#: The nested prefix-subset configs only — JUDGMENT_EVAL_CONFIG is generated
#: by its own pass and deliberately excluded from this order.
CONFIG_ORDER = ("preview", "10M_tokens", "100M_tokens", "1B_tokens")
SPLIT_ORDER = ("test", "validation", "train")

SCHEMA = pa.schema(
    [
        ("row_id", pa.int64()),
        ("example_id", pa.string()),
        ("problem_id", pa.string()),
        ("generator", pa.string()),
        ("generator_label", pa.string()),
        ("operation", pa.string()),
        ("skills", pa.list_(pa.string())),
        ("grade_level", pa.string()),
        ("difficulty", pa.int64()),
        ("problem", pa.string()),
        ("steps", pa.list_(pa.string())),
        ("final_answer", pa.string()),
        ("text", pa.string()),
    ]
)


def text_for_example(example: Mapping[str, object]) -> str:
    steps = "\n".join(str(s) for s in example["steps"])
    return (
        f"Problem:\n{example['problem']}\n\n"
        f"Solution steps:\n{steps}\n\n"
        f"Final answer:\n{example['final_answer']}"
    )


def git_value(args: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None
    return result.stdout.strip()


def size_category(rows: int) -> str:
    bands = [
        (1_000, "n<1K"),
        (10_000, "1K<n<10K"),
        (100_000, "10K<n<100K"),
        (1_000_000, "100K<n<1M"),
        (10_000_000, "1M<n<10M"),
        (100_000_000, "10M<n<100M"),
    ]
    for limit, label in bands:
        if rows < limit:
            return label
    return "n>100M"


class SplitWriter:
    def __init__(
        self,
        output_dir: Path,
        config: str,
        split: str,
        target_rows: int,
        shard_rows: int,
        compression: str,
    ) -> None:
        self.output_dir = output_dir
        self.config = config
        self.split = split
        self.target_rows = target_rows
        self.shard_rows = shard_rows
        self.compression = compression
        self.rows: List[dict] = []
        self.row_count = 0
        self.text_chars = 0
        self.shard_index = 0
        self.total_shards = max(1, math.ceil(target_rows / shard_rows))
        (output_dir / config).mkdir(parents=True, exist_ok=True)

    def add(self, row: dict) -> None:
        if self.row_count >= self.target_rows:
            return
        self.rows.append(dict(row))
        self.row_count += 1
        self.text_chars += len(row["text"])
        if len(self.rows) >= self.shard_rows:
            self.flush()

    def flush(self) -> None:
        if not self.rows:
            return
        path = (
            self.output_dir
            / self.config
            / f"{self.split}-{self.shard_index:05d}-of-{self.total_shards:05d}.parquet"
        )
        table = pa.Table.from_pylist(self.rows, schema=SCHEMA)
        pq.write_table(table, path, compression=self.compression)
        self.rows.clear()
        self.shard_index += 1

    def close(self) -> None:
        self.flush()

    @property
    def rough_tokens(self) -> int:
        return round(self.text_chars / 4)


class ReleaseStats:
    def __init__(self) -> None:
        self.rows_by_config_split: MutableMapping[str, MutableMapping[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.text_chars_by_config_split: MutableMapping[
            str, MutableMapping[str, int]
        ] = defaultdict(lambda: defaultdict(int))
        self.rows_by_largest_split: Counter[str] = Counter()
        self.grade: Counter[str] = Counter()
        self.difficulty: Counter[str] = Counter()
        self.grade_difficulty: Counter[str] = Counter()
        self.generator: Counter[str] = Counter()
        self.operation: Counter[str] = Counter()
        self.generator_stats: MutableMapping[str, Counter[str]] = defaultdict(Counter)
        self.attempts_by_split: Counter[str] = Counter()

    def observe_largest_row(self, split: str, row: Mapping[str, object]) -> None:
        grade = str(row["grade_level"])
        difficulty = str(row["difficulty"])
        self.rows_by_largest_split[split] += 1
        self.grade[grade] += 1
        self.difficulty[difficulty] += 1
        self.grade_difficulty[f"{grade}|{difficulty}"] += 1
        self.generator[str(row["generator"])] += 1
        self.operation[str(row["operation"])] += 1

    def observe_writer(self, writer: SplitWriter) -> None:
        self.rows_by_config_split[writer.config][writer.split] = writer.row_count
        self.text_chars_by_config_split[writer.config][writer.split] = writer.text_chars

    def as_json(self) -> dict:
        return {
            "rows_by_config_split": {
                config: dict(splits)
                for config, splits in sorted(self.rows_by_config_split.items())
            },
            "rough_tokens_by_config_split": {
                config: {
                    split: round(chars / 4)
                    for split, chars in sorted(splits.items())
                }
                for config, splits in sorted(self.text_chars_by_config_split.items())
            },
            "rows_by_largest_split": dict(sorted(self.rows_by_largest_split.items())),
            "attempts_by_split": dict(sorted(self.attempts_by_split.items())),
            "rows_by_grade_level": dict(sorted(self.grade.items())),
            "rows_by_difficulty": dict(sorted(self.difficulty.items())),
            "rows_by_grade_level_and_difficulty": dict(
                sorted(self.grade_difficulty.items())
            ),
            "rows_by_generator": dict(sorted(self.generator.items())),
            "rows_by_operation": dict(sorted(self.operation.items())),
            "generator_stats": {
                name: dict(counts)
                for name, counts in sorted(self.generator_stats.items())
            },
        }


def selected_writers(
    writers: Mapping[Tuple[str, str], SplitWriter],
    split: str,
    row_index: int,
) -> Iterable[SplitWriter]:
    for config in CONFIG_ORDER:
        writer = writers.get((config, split))
        if writer is not None and row_index < writer.target_rows:
            yield writer


def max_rows_by_split(configs: Mapping[str, Mapping[str, int]]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for split in ("train", "validation", "test"):
        result[split] = max((splits.get(split, 0) for splits in configs.values()), default=0)
    return result


def make_row(
    example: Mapping[str, object],
    gen_instance: object,
    split: str,
    row_id: int,
) -> dict:
    text = text_for_example(example)
    skills = example.get("skills")
    return {
        "row_id": row_id,
        "example_id": f"{split}-{row_id:09d}",
        "problem_id": str(example["problem_id"]),
        "generator": gen_instance.__class__.__name__,
        "generator_label": _instance_label(gen_instance),
        "operation": str(example["operation"]),
        "skills": ([str(skill) for skill in skills]
                   if skills is not None else None),
        "grade_level": str(example["grade_level"]),
        "difficulty": int(example["difficulty"]),
        "problem": str(example["problem"]),
        "steps": list(example["steps"]),
        "final_answer": str(example["final_answer"]),
        "text": text,
    }


def generate_release(
    output_dir: Path,
    configs: Mapping[str, Mapping[str, int]],
    seed: int,
    shard_rows: int,
    compression: str,
) -> dict:
    random.seed(seed)
    gen_pool = resolve_pool(None)
    skills = group_into_skills(gen_pool)
    skill_names = list(skills)
    split_targets = max_rows_by_split(configs)
    stats = ReleaseStats()
    seen = set()

    writers: Dict[Tuple[str, str], SplitWriter] = {}
    for config in CONFIG_ORDER:
        for split, rows in configs.get(config, {}).items():
            writers[(config, split)] = SplitWriter(
                output_dir=output_dir,
                config=config,
                split=split,
                target_rows=rows,
                shard_rows=shard_rows,
                compression=compression,
            )

    for split in SPLIT_ORDER:
        target = split_targets.get(split, 0)
        if target <= 0:
            continue
        print(f"Generating {target:,} unique rows for largest {split} split...")
        emitted = 0
        attempts = 0
        max_attempts = target * 20 + 100_000
        consecutive_rejects = 0
        max_consecutive_rejects = max(200_000, target)
        while emitted < target and attempts < max_attempts:
            if consecutive_rejects >= max_consecutive_rejects:
                raise RuntimeError(
                    f"No accepted {split} rows in {consecutive_rejects:,} attempts; "
                    "problem space may be exhausted."
                )
            attempts += 1
            skill = random.choice(skill_names)
            gen_instance = random.choice(skills[skill])
            label = _instance_label(gen_instance)
            try:
                example = gen_instance.generate()
                if not example:
                    raise ValueError("generate() returned an empty example")
                example = stamp_metadata(example, gen_instance)
                validate_example(example)
            except Exception as exc:
                stats.generator_stats[label]["errors"] += 1
                consecutive_rejects += 1
                if stats.generator_stats[label]["errors"] <= 5:
                    print(f"ERROR: {label} failed validation: {exc}")
                continue

            key = (example["operation"], example["problem"])
            if key in seen:
                stats.generator_stats[label]["duplicates_skipped"] += 1
                consecutive_rejects += 1
                continue

            seen.add(key)
            row = make_row(example, gen_instance, split, emitted)
            for writer in selected_writers(writers, split, emitted):
                writer.add(row)
            stats.observe_largest_row(split, row)
            stats.generator_stats[label]["emitted"] += 1
            emitted += 1
            consecutive_rejects = 0
            if emitted % 100_000 == 0 or emitted == target:
                print(
                    f"... {split}: {emitted:,}/{target:,} rows "
                    f"after {attempts:,} attempts"
                )
        stats.attempts_by_split[split] = attempts
        if emitted != target:
            raise RuntimeError(
                f"Target for {split} not reached: emitted {emitted:,}/{target:,} "
                f"after {attempts:,} attempts."
            )

    judgment_target = configs.get(JUDGMENT_EVAL_CONFIG, {}).get("test", 0)
    if judgment_target > 0:
        judgment_writer = SplitWriter(
            output_dir=output_dir,
            config=JUDGMENT_EVAL_CONFIG,
            split="test",
            target_rows=judgment_target,
            shard_rows=shard_rows,
            compression=compression,
        )
        print(
            f"Generating {judgment_target:,} held-out judgment/composition "
            "rows (skills-tagged records only)..."
        )
        emitted = 0
        attempts = 0
        # Most draws are rejected (only skills-tagged generators qualify),
        # so this pass needs a much larger attempt budget per row than the
        # main splits above.
        max_attempts = judgment_target * 500 + 200_000
        while emitted < judgment_target and attempts < max_attempts:
            attempts += 1
            gen_instance = random.choice(gen_pool)
            label = _instance_label(gen_instance)
            try:
                example = gen_instance.generate()
                if not example:
                    raise ValueError("generate() returned an empty example")
                example = stamp_metadata(example, gen_instance)
                validate_example(example)
            except Exception:
                continue
            if not example.get("skills"):
                continue
            key = (example["operation"], example["problem"])
            if key in seen:
                continue
            seen.add(key)
            row = make_row(example, gen_instance, "test", emitted)
            judgment_writer.add(row)
            stats.generator_stats[label]["judgment_eval_emitted"] += 1
            emitted += 1
        if emitted != judgment_target:
            raise RuntimeError(
                f"Judgment/composition eval target not reached: emitted "
                f"{emitted:,}/{judgment_target:,} after {attempts:,} attempts."
            )
        judgment_writer.close()
        stats.observe_writer(judgment_writer)

    for writer in writers.values():
        writer.close()
        stats.observe_writer(writer)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "source_repo": str(ROOT),
        "source_git_commit": git_value(["rev-parse", "HEAD"]),
        "source_git_dirty": bool(git_value(["status", "--short"])),
        "configs": configs,
        "shard_rows": shard_rows,
        "compression": compression,
        "default_pool_skills": len(skills),
        "default_pool_instances": len(gen_pool),
        **stats.as_json(),
    }
    return metadata


def table_rows(rows: Iterable[Tuple[str, object]]) -> str:
    lines = ["| Field | Value |", "|---|---:|"]
    for key, value in rows:
        if isinstance(value, int):
            rendered = f"{value:,}"
        else:
            rendered = str(value)
        lines.append(f"| {key} | {rendered} |")
    return "\n".join(lines)


def split_stats_table(metadata: Mapping[str, object]) -> str:
    rows_by_config = metadata["rows_by_config_split"]
    tokens_by_config = metadata["rough_tokens_by_config_split"]
    lines = ["| Config | Split | Rows | Estimated tokens |", "|---|---|---:|---:|"]
    for config in (*CONFIG_ORDER, JUDGMENT_EVAL_CONFIG):
        splits = rows_by_config.get(config, {})
        for split in ("train", "validation", "test"):
            if split in splits:
                rows = splits[split]
                tokens = tokens_by_config.get(config, {}).get(split, 0)
                lines.append(f"| `{config}` | `{split}` | {rows:,} | {tokens:,} |")
    return "\n".join(lines)


def distribution_table(counter: Mapping[str, int], key_name: str, limit: Optional[int] = None) -> str:
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    if limit is not None:
        items = items[:limit]
    lines = [f"| {key_name} | Rows |", "|---|---:|"]
    for key, value in items:
        lines.append(f"| `{key}` | {value:,} |")
    return "\n".join(lines)


def yaml_header(metadata: Mapping[str, object]) -> str:
    largest_rows = sum(metadata["rows_by_config_split"]["1B_tokens"].values())
    lines = [
        "---",
        "language:",
        "- en",
        "license: other",
        "tags:",
        "- synthetic",
        "- math",
        "- reasoning",
        "- step-by-step",
        "- text-generation",
        "- language-modeling",
        "task_categories:",
        "- text-generation",
        "task_ids:",
        "- language-modeling",
        "size_categories:",
        f"- {size_category(largest_rows)}",
        "pretty_name: QuixiMath-1B",
        "configs:",
    ]
    for config in (*CONFIG_ORDER, JUDGMENT_EVAL_CONFIG):
        splits = metadata["rows_by_config_split"].get(config, {})
        if not splits:
            continue
        lines.append(f"- config_name: {config}")
        lines.append("  data_files:")
        for split in ("train", "validation", "test"):
            if split in splits:
                lines.append(f"  - split: {split}")
                lines.append(f"    path: {config}/{split}-*.parquet")
    lines.extend(
        [
            "train-eval-index:",
            "- config: 10M_tokens",
            "  task: text-generation",
            "  task_id: language-modeling",
            "  splits:",
            "    train_split: train",
            "    eval_split: validation",
            "  col_mapping:",
            "    text: text",
            "- config: 100M_tokens",
            "  task: text-generation",
            "  task_id: language-modeling",
            "  splits:",
            "    train_split: train",
            "    eval_split: validation",
            "  col_mapping:",
            "    text: text",
            "- config: 1B_tokens",
            "  task: text-generation",
            "  task_id: language-modeling",
            "  splits:",
            "    train_split: train",
            "    eval_split: validation",
            "  col_mapping:",
            "    text: text",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def write_readme(output_dir: Path, metadata: Mapping[str, object]) -> None:
    rows_by_config = metadata["rows_by_config_split"]
    tokens_by_config = metadata["rough_tokens_by_config_split"]
    largest_rows = sum(rows_by_config["1B_tokens"].values())
    largest_tokens = sum(tokens_by_config["1B_tokens"].values())
    judgment_eval_rows = sum(rows_by_config.get(JUDGMENT_EVAL_CONFIG, {}).values())
    body = f"""# Dataset Card for QuixiMath-1B

## Dataset Summary

QuixiMath-1B is a synthetic math reasoning corpus generated from the QuixiMath
procedural problem generators. Each record contains a natural-language problem,
explicit step-by-step scratchpad opcodes, a canonical final answer, and metadata
for filtering or reweighting by skill, operation, grade band, and relative
difficulty.

The canonical corpus is coverage-first rather than prescriptively stratified:
trainers can choose their own sampling mix using the included metadata columns.
The size configs are nested prefix subsets within each split.

The foundations strand covers concrete classification and correspondence,
formal propositional and predicate logic, proof systems, sets, relations,
functions, number constructions, ordinals and cardinals, type theory, and
finite-structure isomorphism. Answers are exact throughout — truth values,
set memberships, and proof steps rather than numeric approximations — and
problems that verify a proof or logical form supply a machine-checkable
verdict alongside the justification.

The probability strand covers likelihood language and finite experiments
through conditional expectation, named distributions, limit theorems, random
walks, finite Markov chains, sigma-algebras, martingales, and optional
stopping. Answers use reduced exact fractions wherever possible; four-decimal
probabilities appear only when the needed normal-table or exponential
constant is supplied inline in the prompt.

The statistics strand covers data displays, descriptive measures, sampling
distributions, inference, study design, estimator theory, and conjugate Bayes.
Problems supply every required Φ, z, t, χ², or F lookup value inline and state
rule-dependent procedures explicitly; non-table arithmetic and finite
enumerations retain exact rational answers.

## How to Load

```python
from datasets import load_dataset

ds = load_dataset("QuixiAI/QuixiMath-1B", "100M_tokens")
train = load_dataset("QuixiAI/QuixiMath-1B", "100M_tokens", split="train")
```

For a local checkout:

```python
from datasets import load_dataset

ds = load_dataset("{output_dir}", "preview")
```

## Configs And Splits

{split_stats_table(metadata)}

The largest config contains {largest_rows:,} rows and approximately
{largest_tokens:,} rough text tokens, estimated as `len(text) / 4`.

### Judgment/Composition Eval

`{JUDGMENT_EVAL_CONFIG}` ({judgment_eval_rows:,} rows, `test` split only) is
a standalone, held-out config carved from records whose `skills` column is
non-null — currently `ScenarioGenerator`'s multi-part records, each of whose
sub-questions is tagged with the procedure it reuses (e.g. `percent_change`,
`break_even`, `unit_rate_division`). Its rows are generated in their own
pass and are guaranteed disjoint from every other split, so it measures
whether a model can *compose* procedures it already executes correctly in
isolation elsewhere in the corpus — transfer, not raw execution. It has no
paired `train` split by design; evaluate a model trained on any of the other
configs against it directly.

## Data Schema

Columns:

- `row_id`: stable integer row index within the split.
- `example_id`: stable string ID such as `train-000000123`.
- `problem_id`: generator-provided problem identifier.
- `generator`: generator class name.
- `generator_label`: generator class plus variant marker when applicable.
- `operation`: problem operation/category label.
- `skills`: optional list of procedures composed by scenario or
  discrimination records; null for ordinary records.
- `grade_level`: one of `elementary`, `middle`, `high`, `college`, `graduate`.
- `difficulty`: integer 1-5, relative to `grade_level`.
- `problem`: problem text.
- `steps`: list of pipe-delimited scratchpad steps.
- `final_answer`: canonical answer string.
- `text`: training-ready text field containing problem, steps, and final answer.

## Dataset Stats

{table_rows([
    ("Default sampled skills", metadata["default_pool_skills"]),
    ("Default generator instances", metadata["default_pool_instances"]),
    ("Seed", metadata["seed"]),
    ("Shard rows", metadata["shard_rows"]),
])}

### Grade Distribution

{distribution_table(metadata["rows_by_grade_level"], "Grade level")}

### Difficulty Distribution

{distribution_table(metadata["rows_by_difficulty"], "Difficulty")}

### Suggested Training Recipes

The distributions above come from equal-per-skill sampling, which is
coverage-first, not grade-balanced — college and graduate material make up
more than half the corpus. That is a deliberate choice for the canonical
release: it keeps every procedural skill visible rather than baking one
grade mix into the only release. Trainers can filter or reweight rows with
the `grade_level` and `difficulty` columns; two starting recipes:

**Grade-balanced train mix:**

| Grade level | Suggested share |
|---|---:|
| elementary | 15% |
| middle | 20% |
| high | 30% |
| college | 25% |
| graduate | 10% |

**Within-grade difficulty smoothing** (relative to each grade band — a
`college` difficulty 2 is not the same thing as an `elementary` difficulty
2): 10% at difficulty 1, 20% at difficulty 2, 35% at difficulty 3, 25% at
difficulty 4, 10% at difficulty 5. Where a grade band is missing a
difficulty bucket, redistribute its share across the buckets that exist and
keep per-skill minimums so small buckets stay represented.

### Top Operations

{distribution_table(metadata["rows_by_operation"], "Operation", limit=25)}

## Generation

Generated at: `{metadata["generated_at_utc"]}`

Source repository: `{metadata["source_repo"]}`

Source git commit: `{metadata.get("source_git_commit") or "unknown"}`

Source git dirty: `{metadata["source_git_dirty"]}`

Exact duplicate `(operation, problem)` pairs were skipped across the generated
largest splits before nested configs were materialized. Per-generator duplicate
and error counts are stored in `generation_stats.json`.

## Licensing Information

License: other
"""
    (output_dir / "README.md").write_text(yaml_header(metadata) + body, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output-dir",
        default="~/datasets/QuixiMath-1B",
        help="Output dataset directory.",
    )
    parser.add_argument(
        "--preset",
        choices=("full", "smoke"),
        default="full",
        help="Use full release row counts or tiny smoke-test counts.",
    )
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--shard-rows", type=int, default=100_000)
    parser.add_argument("--compression", default="zstd")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Remove output directory first if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    configs = DEFAULT_CONFIGS if args.preset == "full" else SMOKE_CONFIGS

    if output_dir.exists():
        if not args.overwrite:
            raise SystemExit(f"Output directory already exists: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    metadata = generate_release(
        output_dir=output_dir,
        configs=configs,
        seed=args.seed,
        shard_rows=args.shard_rows,
        compression=args.compression,
    )
    (output_dir / "generation_stats.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_readme(output_dir, metadata)
    print(f"Done: {output_dir}")


if __name__ == "__main__":
    main()

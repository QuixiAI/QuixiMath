"""Probe per-generator distinct problem capacity.

Samples each registered generator class and counts distinct problem texts and
distinct ``(operation, problem)`` keys. This is a sampling probe, not a proof
of total capacity.

Usage:
    uv run python tools/probe_generator_capacity.py
    uv run python tools/probe_generator_capacity.py --samples 2000 --threshold 1000
    uv run python tools/probe_generator_capacity.py --generators Foo,Bar --json /tmp/capacity.json
"""
import argparse
import json
import os
import random
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)


def grouped_generators(generators):
    order = []
    by_name = {}
    for gen in generators:
        name = type(gen).__name__
        if name not in by_name:
            order.append(name)
            by_name[name] = []
        by_name[name].append(gen)
    return [(name, by_name[name]) for name in order]


def probe_generators(generators, samples=2000, threshold=1000, seed=0):
    rng = random.Random(seed)
    rows = []
    for name, instances in grouped_generators(generators):
        problems = set()
        op_problem = set()
        errors = 0
        for _ in range(samples):
            gen = rng.choice(instances)
            state = random.getstate()
            random.setstate(rng.getstate())
            try:
                ex = gen.generate()
            except Exception:
                errors += 1
            else:
                rng.setstate(random.getstate())
                problems.add(ex["problem"])
                op_problem.add((ex["operation"], ex["problem"]))
            finally:
                random.setstate(state)
        distinct_problem_texts = len(problems)
        distinct_operation_problem = len(op_problem)
        duplicate_rate = (
            1 - distinct_operation_problem / max(1, samples - errors)
        )
        rows.append({
            "generator": name,
            "samples": samples,
            "distinct_problem_texts": distinct_problem_texts,
            "distinct_operation_problem": distinct_operation_problem,
            "duplicate_rate": round(duplicate_rate, 4),
            "errors": errors,
            "below_threshold": distinct_problem_texts < threshold,
        })
    return rows


def render_table(rows, threshold):
    headers = ("generator", "distinct", "op_problem", "dup_rate", "errors")
    lines = [
        f"Capacity probe: threshold={threshold}",
        f"{headers[0]:36} {headers[1]:>8} {headers[2]:>10} {headers[3]:>8} {headers[4]:>6}",
        "-" * 74,
    ]
    for row in rows:
        mark = "*" if row["below_threshold"] else " "
        lines.append(
            f"{mark}{row['generator'][:35]:35} "
            f"{row['distinct_problem_texts']:8} "
            f"{row['distinct_operation_problem']:10} "
            f"{row['duplicate_rate']:8.3f} "
            f"{row['errors']:6}"
        )
    flagged = [row["generator"] for row in rows if row["below_threshold"]]
    if flagged:
        lines += ["", "Below threshold: " + ", ".join(flagged)]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--samples", type=int, default=2000)
    parser.add_argument("--threshold", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--generators",
                        help="comma-separated class names to probe")
    parser.add_argument("--json", dest="json_path",
                        help="write machine-readable rows to this path")
    args = parser.parse_args(argv)

    from dolphin_math_datagen import ALL_GENERATORS

    generators = ALL_GENERATORS
    if args.generators:
        wanted = {part.strip() for part in args.generators.split(",")
                  if part.strip()}
        generators = [g for g in ALL_GENERATORS if type(g).__name__ in wanted]
        missing = sorted(wanted - {type(g).__name__ for g in generators})
        if missing:
            parser.error(f"unknown generator(s): {', '.join(missing)}")

    rows = probe_generators(generators, args.samples, args.threshold, args.seed)
    print(render_table(rows, args.threshold))
    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 1 if any(row["below_threshold"] for row in rows) else 0


if __name__ == "__main__":
    sys.exit(main())

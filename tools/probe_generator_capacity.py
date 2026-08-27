"""Probe per-generator distinct problem capacity.

Samples each registered generator class, counts distinct problem texts and
distinct ``(operation, problem)`` keys, and estimates the size of the total
problem space from the collision rate.

The estimate inverts the "balls in bins" expectation
``E[distinct] = N * (1 - exp(-n / N))`` for the space size ``N`` given ``n``
samples and the observed distinct count. It is a *lower-bound flavoured*
estimate: a generator whose sample is entirely distinct gets ``None``
(reported as ``>>`` the sample size) because the probe cannot see collisions
that never happened. Draw more samples to tighten it.

Capacity bar: every generator should support hundreds of thousands to
millions of distinct problems. With the default 5000 samples, "no repeats at
all" (``--threshold 4850`` catches ~100k spaces, ``--threshold 4975`` catches
~1M) is the practical check; ``--min-capacity`` flags on the estimate itself.

Usage:
    uv run python tools/probe_generator_capacity.py
    uv run python tools/probe_generator_capacity.py --samples 5000 --threshold 4850
    uv run python tools/probe_generator_capacity.py --samples 5000 --min-capacity 100000
    uv run python tools/probe_generator_capacity.py --generators Foo,Bar --json /tmp/capacity.json
"""
import argparse
import json
import math
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


def estimate_capacity(samples, distinct):
    """Estimate the total problem-space size from a sample's collision rate.

    Inverts ``E[distinct] = N * (1 - exp(-n / N))`` for ``N`` by bisection.
    Returns ``None`` when every sample was distinct (no collision signal — the
    space is larger than this sample size can measure).
    """
    if samples <= 0 or distinct <= 0:
        return 0
    if distinct >= samples:
        return None
    lo, hi = float(distinct), 1e15
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if mid * (1.0 - math.exp(-samples / mid)) < distinct:
            lo = mid
        else:
            hi = mid
    return int(hi)


def fmt_capacity(value, samples):
    """Human-readable capacity estimate: 12.3k, 4.5M, or '>1M' when unmeasured."""
    if value is None:
        return f">{samples}*"
    if value >= 1e9:
        return f"{value / 1e9:.1f}B"
    if value >= 1e6:
        return f"{value / 1e6:.1f}M"
    if value >= 1e3:
        return f"{value / 1e3:.1f}k"
    return str(value)


def probe_generators(generators, samples=2000, threshold=1000, seed=0,
                     min_capacity=None):
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
        capacity = estimate_capacity(samples - errors, distinct_problem_texts)
        below = distinct_problem_texts < threshold
        if min_capacity is not None:
            below = below or (capacity is not None and capacity < min_capacity)
        rows.append({
            "generator": name,
            "samples": samples,
            "distinct_problem_texts": distinct_problem_texts,
            "distinct_operation_problem": distinct_operation_problem,
            "duplicate_rate": round(duplicate_rate, 4),
            "estimated_capacity": capacity,
            "errors": errors,
            "below_threshold": below,
        })
    return rows


def render_table(rows, threshold, min_capacity=None):
    headers = ("generator", "distinct", "op_problem", "dup_rate", "est_cap",
               "errors")
    title = f"Capacity probe: threshold={threshold}"
    if min_capacity is not None:
        title += f", min_capacity={min_capacity}"
    lines = [
        title,
        f"{headers[0]:36} {headers[1]:>8} {headers[2]:>10} {headers[3]:>8} "
        f"{headers[4]:>9} {headers[5]:>6}",
        "-" * 84,
    ]
    for row in rows:
        mark = "*" if row["below_threshold"] else " "
        lines.append(
            f"{mark}{row['generator'][:35]:35} "
            f"{row['distinct_problem_texts']:8} "
            f"{row['distinct_operation_problem']:10} "
            f"{row['duplicate_rate']:8.3f} "
            f"{fmt_capacity(row['estimated_capacity'], row['samples']):>9} "
            f"{row['errors']:6}"
        )
    flagged = [row["generator"] for row in rows if row["below_threshold"]]
    if flagged:
        lines += ["", "Below threshold: " + ", ".join(flagged)]
    lines += ["", "* est_cap: '>N*' means every sample was distinct — the "
              "space is larger than this probe can measure."]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--samples", type=int, default=2000)
    parser.add_argument("--threshold", type=int, default=1000,
                        help="minimum distinct problem texts in the sample")
    parser.add_argument("--min-capacity", type=int, default=None,
                        dest="min_capacity",
                        help="also flag generators whose estimated space is "
                             "below this size (e.g. 100000)")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--generators",
                        help="comma-separated class names to probe")
    parser.add_argument("--json", dest="json_path",
                        help="write machine-readable rows to this path")
    args = parser.parse_args(argv)

    from quixi_math_datagen import ALL_GENERATORS

    generators = ALL_GENERATORS
    if args.generators:
        wanted = {part.strip() for part in args.generators.split(",")
                  if part.strip()}
        generators = [g for g in ALL_GENERATORS if type(g).__name__ in wanted]
        missing = sorted(wanted - {type(g).__name__ for g in generators})
        if missing:
            parser.error(f"unknown generator(s): {', '.join(missing)}")

    rows = probe_generators(generators, args.samples, args.threshold,
                            args.seed, args.min_capacity)
    print(render_table(rows, args.threshold, args.min_capacity))
    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 1 if any(row["below_threshold"] for row in rows) else 0


if __name__ == "__main__":
    sys.exit(main())

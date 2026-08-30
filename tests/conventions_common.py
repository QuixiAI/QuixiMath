"""Shared helpers for the strand conventions tests.

Used by ``test_foundations_conventions.py``, ``test_probability_conventions.py``,
``test_stats_conventions.py`` and ``test_applied_conventions.py``. Keeps the
one rule every strand enforces — no ASCII ``|`` outside the step delimiter —
in a single place, and discovers the generators a strand owns by a
module-level flag (``FOUNDATIONS = True`` etc.).
"""
import importlib
import os
import random
import re
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from helpers import DELIM  # noqa: E402

STRAND_FLAGS = ("FOUNDATIONS", "PROBABILITY", "STATISTICS", "APPLIED",
                "DEPTH")


def flagged_generators(flag):
    """Registered generator instances whose module sets ``<flag> = True``."""
    from quixi_math_datagen import ALL_GENERATORS

    out = []
    for gen in ALL_GENERATORS:
        module = importlib.import_module(type(gen).__module__)
        if getattr(module, flag, False) is True:
            out.append(gen)
    return out


def sample_examples(gen, n=200, seed=0):
    """Deterministic sample of ``n`` examples from one generator instance."""
    state = random.getstate()
    random.seed(seed)
    try:
        return [gen.generate() for _ in range(n)]
    finally:
        random.setstate(state)


def pipe_violations(example):
    """Lines of an example that leak an ASCII bar.

    Steps may contain ``|`` only as the field delimiter: at most four
    payload fields after the op-code, and no field may be empty in the
    middle. Problem text and final answer may not contain ``|`` at all.
    """
    bad = []
    if DELIM in str(example.get("problem", "")):
        bad.append(f"problem text contains '{DELIM}'")
    if DELIM in str(example.get("final_answer", "")):
        bad.append(f"final_answer contains '{DELIM}'")
    for raw in example.get("steps", []):
        fields = raw.split(DELIM)
        if len(fields) - 1 > 4:
            bad.append(f"step has more than 4 payload fields: {raw}")
        if not fields[0] or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", fields[0]):
            bad.append(f"step lacks an op-code: {raw}")
    return bad


def assert_pipe_safe(testcase, example):
    violations = pipe_violations(example)
    testcase.assertFalse(violations, violations)


def assert_contract(testcase, example):
    """The base output contract every generator satisfies."""
    for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
        testcase.assertIn(key, example)
    testcase.assertTrue(example["steps"], "steps must be non-empty")
    testcase.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")


def method_word_hits(text, banned):
    """Banned method phrases found in ``text`` (case-insensitive)."""
    lowered = text.lower()
    return [phrase for phrase in banned if phrase.lower() in lowered]

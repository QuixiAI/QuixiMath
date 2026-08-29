"""Focused checks for optional release-only metadata.

Run with ``uv run --group release python -m unittest
tests.test_build_hf_release`` so the pinned Parquet dependency is available.
"""
import tempfile
import unittest
from pathlib import Path

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    from tools.build_hf_release import (
        JUDGMENT_EVAL_CONFIG,
        SCHEMA,
        generate_release,
        make_row,
    )
except ModuleNotFoundError:  # ordinary generator-only environments omit it
    pa = None
    pq = None
    SCHEMA = None
    make_row = None
    generate_release = None
    JUDGMENT_EVAL_CONFIG = None


class ExampleGenerator:
    pass


@unittest.skipIf(pa is None, "install the release dependency group")
class TestBuildHfRelease(unittest.TestCase):
    def example(self, skills=None):
        result = {
            "problem_id": "example-id",
            "operation": "scenario_budget",
            "problem": "A shop scenario.",
            "steps": ["Z|Q1 $20; Q2 10%"],
            "final_answer": "Q1 $20; Q2 10%",
            "grade_level": "high",
            "difficulty": 4,
        }
        if skills is not None:
            result["skills"] = skills
        return result

    def test_schema_contains_nullable_skills_list(self):
        field = SCHEMA.field("skills")
        self.assertTrue(field.nullable)
        self.assertTrue(pa.types.is_list(field.type))
        self.assertTrue(pa.types.is_string(field.type.value_type))

    def test_make_row_preserves_skills_and_ordinary_null(self):
        tagged = make_row(self.example(["budget", "percent_change"]),
                          ExampleGenerator(), "test", 7)
        plain = make_row(self.example(), ExampleGenerator(), "test", 8)
        self.assertEqual(tagged["skills"], ["budget", "percent_change"])
        self.assertIsNone(plain["skills"])

    def test_parquet_round_trip_preserves_skills(self):
        rows = [
            make_row(self.example(["budget", "percent_change"]),
                     ExampleGenerator(), "test", 7),
            make_row(self.example(), ExampleGenerator(), "test", 8),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skills.parquet"
            pq.write_table(pa.Table.from_pylist(rows, schema=SCHEMA), path)
            decoded = pq.read_table(path).to_pylist()
        self.assertEqual(decoded[0]["skills"], ["budget", "percent_change"])
        self.assertIsNone(decoded[1]["skills"])

    def test_judgment_composition_eval_is_held_out_and_skills_tagged(self):
        """The new config (plans/applied_plan.md §9) contains only
        skills-tagged rows, and never overlaps the ordinary splits."""
        configs = {
            "preview": {"train": 30},
            JUDGMENT_EVAL_CONFIG: {"test": 8},
        }
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            metadata = generate_release(
                output_dir=output_dir,
                configs=configs,
                seed=101,
                shard_rows=1_000,
                compression="snappy",
            )
            self.assertIn(JUDGMENT_EVAL_CONFIG, metadata["rows_by_config_split"])
            self.assertEqual(
                metadata["rows_by_config_split"][JUDGMENT_EVAL_CONFIG]["test"], 8)

            eval_rows = pq.read_table(
                output_dir / JUDGMENT_EVAL_CONFIG / "test-00000-of-00001.parquet"
            ).to_pylist()
            self.assertEqual(len(eval_rows), 8)
            for row in eval_rows:
                self.assertTrue(row["skills"], row)

            preview_rows = pq.read_table(
                output_dir / "preview" / "train-00000-of-00001.parquet"
            ).to_pylist()
            preview_keys = {(row["operation"], row["problem"]) for row in preview_rows}
            eval_keys = {(row["operation"], row["problem"]) for row in eval_rows}
            self.assertEqual(preview_keys & eval_keys, set())


if __name__ == "__main__":
    unittest.main()

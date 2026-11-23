import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/proof-driven-engineering/scripts/compare_bench.py"
)


class BenchmarkCompareTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        spec = importlib.util.spec_from_file_location("compare_bench", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.record = {
            "schema_version": 1,
            "metric": "p99_latency",
            "unit": "ns",
            "direction": "lower_is_better",
            "paired": True,
            "min_effect_pct": 2.0,
            "baseline": {
                "label": "v0",
                "samples": [100.0, 102.0, 101.0, 104.0, 99.0, 103.0, 101.5],
            },
            "candidate": {
                "label": "v1",
                "samples": [50.0, 51.0, 50.5, 52.0, 49.5, 51.5, 50.75],
            },
        }

    def run_cli(self, content: str, extra_args: list[str] | None = None):
        path = self.root / "bench.json"
        path.write_text(content, encoding="utf-8")
        cmd = [sys.executable, str(SCRIPT), str(path), *(extra_args or [])]
        return subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=False)

    def test_detects_clear_lower_is_better_improvement(self):
        self.assertEqual(self.module.validate_record(self.record), [])
        result = self.module.compare(self.record, bootstrap_iters=600)
        self.assertEqual(result["verdict"], "SIGNIFICANT_IMPROVEMENT")
        self.assertAlmostEqual(result["speedup_ratio"], 2.0, places=4)
        self.assertAlmostEqual(result["pct_improvement"], 50.0, places=4)
        self.assertGreater(result["bootstrap_95ci"][0], 1.9)
        self.assertEqual(result["cliffs_delta"], 1.0)
        self.assertEqual(result["warnings"], [])

    def test_detects_clear_higher_is_better_improvement(self):
        record = copy.deepcopy(self.record)
        record["metric"] = "throughput"
        record["unit"] = "ops/s"
        record["direction"] = "higher_is_better"
        record["baseline"]["samples"] = [1_000_000, 1_010_000, 995_000, 1_005_000, 1_002_000, 998_000, 1_001_000]
        record["candidate"]["samples"] = [5_000_000, 5_050_000, 4_975_000, 5_025_000, 5_010_000, 4_990_000, 5_005_000]
        result = self.module.compare(record, bootstrap_iters=600)
        self.assertEqual(result["verdict"], "SIGNIFICANT_IMPROVEMENT")
        self.assertAlmostEqual(result["speedup_ratio"], 5.0, places=3)
        self.assertEqual(result["cliffs_delta"], 1.0)

    def test_detects_regression_and_cli_gate_exits_nonzero(self):
        record = copy.deepcopy(self.record)
        record["baseline"]["samples"], record["candidate"]["samples"] = (
            record["candidate"]["samples"],
            record["baseline"]["samples"],
        )
        result = self.module.compare(record, bootstrap_iters=600)
        self.assertEqual(result["verdict"], "SIGNIFICANT_REGRESSION")
        self.assertLess(result["bootstrap_95ci"][1], 0.6)
        completed = self.run_cli(json.dumps(record), ["--fail-on-regression"])
        self.assertEqual(completed.returncode, 2)

    def test_rejects_noise_floor_as_indistinguishable(self):
        record = copy.deepcopy(self.record)
        record["paired"] = False
        record["baseline"]["samples"] = [100.0, 108.0, 95.0, 104.0, 97.0, 103.0, 101.0]
        record["candidate"]["samples"] = [99.0, 107.0, 94.0, 105.0, 98.0, 102.0, 100.5]
        result = self.module.compare(record, bootstrap_iters=600)
        self.assertEqual(result["verdict"], "INDISTINGUISHABLE_FROM_NOISE")
        completed = self.run_cli(json.dumps(record), ["--require-improvement"])
        self.assertEqual(completed.returncode, 2)

    def test_paired_interleaved_ratio_cancels_monotonic_drift(self):
        record = copy.deepcopy(self.record)
        record["baseline"]["samples"] = [100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0]
        record["candidate"]["samples"] = [80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0]
        paired_result = self.module.compare(record, bootstrap_iters=600)
        self.assertEqual(paired_result["verdict"], "SIGNIFICANT_IMPROVEMENT")
        self.assertAlmostEqual(paired_result["bootstrap_95ci"][0], 1.25, places=4)
        self.assertAlmostEqual(paired_result["bootstrap_95ci"][1], 1.25, places=4)

    def test_warns_when_fewer_than_seven_samples(self):
        record = copy.deepcopy(self.record)
        record["baseline"]["samples"] = [100.0, 101.0, 102.0]
        record["candidate"]["samples"] = [50.0, 50.5, 51.0]
        result = self.module.compare(record, bootstrap_iters=400)
        self.assertTrue(result["warnings"])

    def test_validation_rejects_malformed_inputs(self):
        bad_cases = [
            None,
            [],
            {},
            {**self.record, "schema_version": True},
            {**self.record, "direction": "sideways"},
            {**self.record, "paired": "yes"},
            {**self.record, "min_effect_pct": -1.0},
            {**self.record, "baseline": {"label": "b", "unit": "ms", "samples": [1, 2, 3]}},
            {**self.record, "baseline": {"label": "b", "samples": [1.0, 2.0]}},
            {**self.record, "baseline": {"label": "b", "samples": [1.0, 0.0, 2.0]}},
            {**self.record, "baseline": {"label": "b", "samples": [1.0, True, 2.0]}},
            {**self.record, "baseline": {"label": "b", "samples": [1.0, float("inf"), 2.0]}},
            {
                **self.record,
                "paired": True,
                "baseline": {"label": "b", "samples": [10.0, 11.0, 12.0, 13.0]},
                "candidate": {"label": "c", "samples": [5.0, 6.0, 7.0]},
            },
        ]
        for case in bad_cases:
            with self.subTest(case=case):
                self.assertTrue(self.module.validate_record(case))

    def test_cli_rejects_duplicate_json_keys_and_nonstandard_constants(self):
        dup = json.dumps(self.record).replace("{", '{"schema_version": 1,', 1)
        self.assertEqual(self.run_cli(dup).returncode, 1)
        nan_rec = copy.deepcopy(self.record)
        nan_rec["baseline"]["samples"][0] = float("nan")
        self.assertEqual(self.run_cli(json.dumps(nan_rec)).returncode, 1)

    def test_cli_json_output_is_parseable_and_deterministic(self):
        r1 = self.run_cli(json.dumps(self.record), ["--json", "--require-improvement"])
        r2 = self.run_cli(json.dumps(self.record), ["--json", "--require-improvement"])
        self.assertEqual(r1.returncode, 0, r1.stderr)
        self.assertEqual(r1.stdout, r2.stdout)
        parsed = json.loads(r1.stdout)
        self.assertEqual(parsed["verdict"], "SIGNIFICANT_IMPROVEMENT")
        self.assertIn("disclaimer", parsed)


if __name__ == "__main__":
    unittest.main()

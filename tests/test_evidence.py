import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/proof-driven-engineering/scripts/check_evidence.py"
)


class EvidenceGateTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.source = self.root / "source.txt"
        self.source.write_bytes(b"original\n")
        self.record = {
            "schema_version": 1,
            "goal": "Preserve behavior while improving the requested path",
            "requirements": [{"id": "behavior", "checks": ["regression"]}],
            "checks": [{
                "id": "regression",
                "status": "pass",
                "command": "python -m unittest",
                "exit_code": 0,
                "inputs": {"source.txt": hashlib.sha256(b"original\n").hexdigest()},
            }],
        }

    def validate(self, record=...):
        self.assertTrue(SCRIPT.is_file(), "The evidence validator is not implemented")
        spec = importlib.util.spec_from_file_location("check_evidence", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.validate(self.record if record is ... else record, self.root)

    def test_accepts_complete_evidence_for_current_inputs(self):
        self.assertEqual(self.validate(), [])

    def test_missing_requirement_check_cannot_pass(self):
        self.record["requirements"][0]["checks"].append("contract")
        self.assertTrue(self.validate())

    def test_changed_source_invalidates_recorded_success(self):
        self.source.write_bytes(b"changed\n")
        self.assertTrue(self.validate())

    def test_nonzero_exit_cannot_support_a_pass(self):
        self.record["checks"][0]["exit_code"] = 1
        self.assertTrue(self.validate())

    def test_boolean_exit_code_cannot_impersonate_zero(self):
        self.record["checks"][0]["exit_code"] = False
        self.assertTrue(self.validate())

    def test_failed_or_unverified_checks_block_completion(self):
        for status in ("fail", "not_verified"):
            with self.subTest(status=status):
                record = copy.deepcopy(self.record)
                record["checks"][0]["status"] = status
                self.assertTrue(self.validate(record))

    def test_empty_coverage_and_empty_inputs_cannot_pass(self):
        for field in ("requirements", "checks"):
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record[field] = []
                self.assertTrue(self.validate(record))
        self.record["checks"][0]["inputs"] = {}
        self.assertTrue(self.validate())

    def test_duplicate_check_ids_cannot_hide_a_failed_check(self):
        duplicate = copy.deepcopy(self.record["checks"][0])
        duplicate["status"] = "fail"
        self.record["checks"].append(duplicate)
        self.assertTrue(self.validate())

    def test_malformed_records_return_errors_instead_of_crashing(self):
        for record in (None, [], {}, {"schema_version": True}, {"checks": [None]}):
            with self.subTest(record=record):
                self.assertTrue(self.validate(record))

    def test_missing_files_and_malformed_hashes_cannot_pass(self):
        for inputs in ({"missing.txt": "0" * 64}, {"source.txt": "bad-hash"}):
            with self.subTest(inputs=inputs):
                record = copy.deepcopy(self.record)
                record["checks"][0]["inputs"] = inputs
                self.assertTrue(self.validate(record))

    def test_duplicate_requirements_and_missing_acceptance_cannot_pass(self):
        record = copy.deepcopy(self.record)
        record["requirements"].append(copy.deepcopy(record["requirements"][0]))
        self.assertTrue(self.validate(record))
        self.record["requirements"][0]["checks"] = []
        self.assertTrue(self.validate())

    def run_cli(self, content):
        record_path = self.root / "evidence.json"
        record_path.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(record_path), "--root", str(self.root)],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    def test_cli_validates_without_executing_recorded_commands(self):
        self.record["checks"][0]["command"] = "unavailable-command-for-fixture"
        completed = self.run_cli(json.dumps(self.record))
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_cli_rejects_duplicate_json_keys(self):
        content = json.dumps(self.record).replace("{", '{"schema_version": 1,', 1)
        self.assertNotEqual(self.run_cli(content).returncode, 0)

    def test_cli_rejects_nonstandard_json_constants(self):
        self.record["extra"] = float("nan")
        self.assertNotEqual(self.run_cli(json.dumps(self.record)).returncode, 0)

    def test_paths_cannot_escape_the_workspace(self):
        for name in ("../outside", "/outside", "C:/outside", "folder\\source.txt"):
            with self.subTest(name=name):
                record = copy.deepcopy(self.record)
                record["checks"][0]["inputs"] = {name: "0" * 64}
                self.assertTrue(self.validate(record))

    def test_symlink_cannot_escape_the_workspace(self):
        outside = self.root.parent / (self.root.name + "-outside")
        outside.write_text("outside", encoding="utf-8")
        self.addCleanup(outside.unlink)
        link = self.root / "escape"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("Creating a symlink is unavailable in this environment")
        self.record["checks"][0]["inputs"] = {"escape": "0" * 64}
        self.assertTrue(self.validate())


if __name__ == "__main__":
    unittest.main()

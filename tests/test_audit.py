import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/fair-research-software/scripts/audit_repository.py"
spec = importlib.util.spec_from_file_location("fair_audit", SCRIPT)
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "research repo"
        self.repo.mkdir()

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def checks(self):
        return {c["id"]: c for c in audit_module.audit(self.repo)["checks"]}

    def test_nested_examples_are_not_root_metadata(self):
        self.write("examples/CITATION.cff", "title: example")
        self.write("assets/codemeta.json", "{}")
        checks = self.checks()
        self.assertEqual(checks["citation-file"]["status"], "failed")
        self.assertEqual(checks["discovery-metadata"]["status"], "failed")

    def test_malformed_json_and_duplicate_keys_fail(self):
        for text in ['{"name":', '{"version":"1","version":"2"}', '[]']:
            with self.subTest(text=text):
                self.write("codemeta.json", text)
                self.assertEqual(self.checks()["parse-codemeta.json"]["status"], "failed")

    def test_versions_are_compared(self):
        self.write("codemeta.json", '{"version":"1.0"}')
        self.write(".zenodo.json", '{"version":"2.0"}')
        self.assertEqual(self.checks()["version-consistency"]["status"], "failed")
        self.write(".zenodo.json", '{"version":"v1.0"}')
        self.assertEqual(self.checks()["version-consistency"]["status"], "verified")

    def test_missing_yaml_dependency_is_not_checked(self):
        self.write("CITATION.cff", "title: demo")
        with patch.object(audit_module, "yaml", None):
            self.assertEqual(self.checks()["parse-citation.cff"]["status"], "not_checked")

    def test_missing_toml_support_is_not_checked(self):
        self.write("pyproject.toml", '[project]\nversion = "1.0"\n')
        with patch.object(audit_module, "tomllib", None):
            self.assertEqual(self.checks()["parse-pyproject.toml"]["status"], "not_checked")

    @unittest.skipIf(audit_module.tomllib is None, "TOML parsing requires Python 3.11+")
    def test_package_version_compared_without_conflating_benchmark_or_crate_versions(self):
        self.write("pyproject.toml", '[project]\nversion = "1.1.0"\n')
        self.write("codemeta.json", '{"version":"1.0.0"}')
        self.write("ro-crate-metadata.json", '{"version":"7.0"}')
        self.write("benchmark/2.0/pyproject.toml", '[project]\nversion = "2.0"\n')
        self.assertEqual(self.checks()["version-consistency"]["status"], "failed")
        self.write("codemeta.json", '{"version":"1.1.0"}')
        check = self.checks()["version-consistency"]
        self.assertEqual(check["status"], "verified")
        self.assertEqual(set(check["evidence"]), {"pyproject.toml", "codemeta.json"})

    @unittest.skipIf(audit_module.tomllib is None, "TOML parsing requires Python 3.11+")
    def test_dynamic_package_version_does_not_execute_backend(self):
        self.write("pyproject.toml", '[project]\nname = "demo"\ndynamic = ["version"]\n'
                   '[build-system]\nrequires = []\nbuild-backend = "backend"\nbackend-path = ["."]\n')
        self.write("backend.py", "from pathlib import Path\nPath('executed.txt').touch()")
        checks = self.checks()
        self.assertEqual(checks["package-version-source"]["status"], "not_checked")
        self.assertEqual(checks["version-consistency"]["status"], "not_checked")
        self.assertFalse((self.repo / "executed.txt").exists())

    @unittest.skipIf(audit_module.tomllib is None, "TOML parsing requires Python 3.11+")
    def test_malformed_or_duplicate_toml_fails(self):
        for text in ['[project', '[project]\nversion="1"\nversion="2"', 'project = "bad"',
                     '[project]\ndynamic="version"']:
            with self.subTest(text=text):
                self.write("pyproject.toml", text)
                self.assertEqual(self.checks()["parse-pyproject.toml"]["status"], "failed")

    @unittest.skipIf(audit_module.yaml is None, "PyYAML is optional")
    def test_concept_and_version_doi_conflict(self):
        self.write("CITATION.cff", """title: Demo
identifiers:
  - type: doi
    value: 'https://doi.org/10.1234/example'
    description: Concept DOI for all versions
  - type: doi
    value: '10.1234/example'
    description: Version DOI for v1.0
""")
        self.assertEqual(self.checks()["doi-role-consistency"]["status"], "failed")

    @unittest.skipIf(audit_module.yaml is None, "PyYAML is optional")
    def test_yaml_duplicate_keys_and_unsafe_tags_fail(self):
        for text in ["title: One\ntitle: Two\n", "!!python/object/apply:os.system ['echo unsafe']"]:
            self.write("CITATION.cff", text)
            self.assertEqual(self.checks()["parse-citation.cff"]["status"], "failed")

    def test_symlinks_and_generated_directories_not_read(self):
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text('{"version":"secret"}')
        (self.repo / "codemeta.json").symlink_to(outside)
        self.write(".venv/CITATION.cff", "title: dependency")
        result = audit_module.audit(self.repo)
        self.assertIn("codemeta.json", result["excluded_paths"])
        self.assertEqual(result["files_inspected_for_inventory"], 0)

    def test_metadata_placeholder_is_detected(self):
        self.write("codemeta.json", '{"name":"REPLACE_SOFTWARE_TITLE"}')
        self.assertEqual(self.checks()["placeholders-codemeta.json"]["status"], "failed")

    def test_target_scripts_never_run_and_remote_claims_remain_unchecked(self):
        marker = self.repo / "executed.txt"
        self.write("setup.py", "from pathlib import Path\nPath('executed.txt').touch()")
        self.write("postBuild", "touch executed.txt")
        self.write("README.md", "[DOI](https://doi.org/10.1234/example)")
        checks = self.checks()
        self.assertFalse(marker.exists())
        for name in ["zenodo-archive", "software-heritage", "execution", "schema-validation", "license-coverage"]:
            self.assertEqual(checks[name]["status"], "not_checked")

    def test_git_inventory_honours_ignored_files_and_records_revision(self):
        def git(*args):
            subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True)
        git("init", "-q")
        self.write(".gitignore", "ignored/\n")
        self.write("README.md", "demo")
        git("add", "README.md", ".gitignore")
        git("-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "-qm", "Initial")
        self.write("ignored/CITATION.cff", "title: ignored")
        result = audit_module.audit(self.repo)
        self.assertEqual(result["inventory_method"], "git")
        self.assertFalse(result["dirty"])
        self.assertEqual(len(result["commit"]), 40)
        self.assertEqual(result["files_inspected_for_inventory"], 2)

    def test_cli_exit_codes_and_markdown(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.repo), "--strict"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("checks", json.loads(result.stdout))
        missing = subprocess.run([sys.executable, str(SCRIPT), str(self.repo / "absent")], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        self.write("README.md", "demo")
        self.write("LICENSE", "demo")
        self.write("CITATION.cff", "title: Demo")
        self.write("codemeta.json", '{"name":"Demo"}')
        good = subprocess.run([sys.executable, str(SCRIPT), str(self.repo), "--strict", "--format", "markdown"], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0)
        self.assertIn("not_checked", good.stdout)
        self.assertIn("no FAIR certification", good.stdout)

    def test_git_fsmonitor_hook_is_not_executed(self):
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True, capture_output=True)
        self.write("README.md", "demo")
        subprocess.run(["git", "-C", str(self.repo), "add", "README.md"], check=True, capture_output=True)
        marker = self.repo / "hook-executed"
        hook = self.repo / ".git/hooks/fsmonitor-test"
        hook.write_text("#!/bin/sh\ntouch hook-executed\n")
        hook.chmod(0o755)
        subprocess.run(["git", "-C", str(self.repo), "config", "core.fsmonitor", str(hook)], check=True, capture_output=True)
        audit_module.audit(self.repo)
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()

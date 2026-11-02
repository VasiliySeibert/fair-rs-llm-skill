import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fair_install", ROOT / "tools/install_skill.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def test_all_agent_project_locations_copy_resources(self):
        for agent, directory in installer.PROJECT_DIRS.items():
            with self.subTest(agent=agent):
                path = installer.install(agent, project=self.root)
                self.assertEqual(path, self.root / directory / installer.NAME)
                self.assertTrue((path / "SKILL.md").is_file())
                self.assertTrue((path / "references/zenodo.md").is_file())
                self.assertTrue((path / "scripts/audit_repository.py").is_file())

    def test_existing_installation_is_never_overwritten(self):
        path = installer.install("codex", project=self.root)
        (path / "SKILL.md").write_text("local customisation")
        with self.assertRaises(FileExistsError):
            installer.install("codex", project=self.root)
        self.assertEqual((path / "SKILL.md").read_text(), "local customisation")

    def test_broken_symlink_is_not_overwritten(self):
        path = self.root / installer.PROJECT_DIRS["codex"] / installer.NAME
        path.parent.mkdir(parents=True)
        path.symlink_to(self.root / "absent")
        with self.assertRaises(FileExistsError):
            installer.install("codex", project=self.root)

    def test_personal_installation_and_xdg_config(self):
        path = installer.install("claude", home=self.root)
        self.assertEqual(path, self.root / ".claude/skills" / installer.NAME)
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.root / "custom config")}):
            path = installer.install("opencode", home=self.root)
        self.assertEqual(path, self.root / "custom config/opencode/skills" / installer.NAME)

    def test_nonexistent_project_fails(self):
        with self.assertRaises(ValueError):
            installer.install("codex", project=self.root / "absent")


if __name__ == "__main__":
    unittest.main()

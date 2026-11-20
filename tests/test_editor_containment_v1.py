"""Source-only containment checks; never execute editor tasks or font assets."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EditorContainmentTests(unittest.TestCase):
    def test_tasks_are_explicitly_inert(self):
        data = json.loads((ROOT / ".vscode" / "tasks.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(data.get("version"), "2.0.0")
        self.assertEqual(data.get("tasks"), [])

    def test_settings_do_not_enable_or_conceal_startup(self):
        data = json.loads((ROOT / ".vscode" / "settings.json").read_text(encoding="utf-8-sig"))
        for forbidden in (
            "task.allowAutomaticTasks",
            "tasks",
            "terminal.integrated.hideOnStartup",
            "debug.openDebug",
        ):
            with self.subTest(setting=forbidden):
                self.assertNotIn(forbidden, data)

    def test_hidden_bootstrap_absent(self):
        self.assertFalse((ROOT / ".vscode" / "ini").exists())

    def test_counterfeit_font_absent(self):
        self.assertFalse((ROOT / "public" / "fonts" / "fa-solid-600.ttf").exists())

    def test_concealed_config_ignore_absent(self):
        lines = (ROOT / ".gitignore").read_text(encoding="utf-8-sig").splitlines()
        self.assertNotIn("config.bat", [line.strip() for line in lines])


if __name__ == "__main__":
    unittest.main()

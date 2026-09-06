from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LocalValidationMigrationTests(unittest.TestCase):
    def test_paid_hosted_workflow_is_removed(self):
        self.assertFalse((ROOT / ".github/workflows/r10a1-validation.yml").exists())

    def test_repo_local_validator_exists_with_required_contract(self):
        script = ROOT / "tools/validate_r10a1.py"
        self.assertTrue(script.is_file())
        text = script.read_text(encoding="utf-8")
        for required in [
            "2d60cd8e87ac0aae89a5a9bd9a44bfb63f48aa64",
            "VERA_R10A1_SALIENCE_REGRESSION.md",
            "VERA_R10A1_PUBLICATION_RECEIPT.json",
            "R10A1 static/source validation PASS",
            "project-instructions/r10a0/",
        ]:
            self.assertIn(required, text)

    def test_local_runbook_is_explicit(self):
        doc = ROOT / "docs/R10A1_LOCAL_VALIDATION.md"
        self.assertTrue(doc.is_file())
        text = doc.read_text(encoding="utf-8")
        self.assertIn("python tools/validate_r10a1.py", text)
        self.assertIn("does not require GitHub Actions", text)


if __name__ == "__main__":
    unittest.main()

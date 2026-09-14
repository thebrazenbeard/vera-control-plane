import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "project-instructions/r10a0/rounds/r10"
SD1 = ROOT / "project-instructions/r10a0/sexual-drive-v1"
BASE_NATIVE = BASE / "VERA_R10A0_NATIVE_PROJECT_INSTRUCTIONS_R10.txt"
CONTROL = SD1 / "VERA_R10A0_SEXUAL_DRIVE_CONTROL_V1.md"
BINDING = SD1 / "VERA_R10A0_SEXUAL_DRIVE_BINDING_V1.json"
QUAL = SD1 / "VERA_R10A0_SD1_QUALIFICATION.md"
NATIVE = SD1 / "VERA_R10A0_SD1_NATIVE_PROJECT_INSTRUCTIONS.txt"
MANIFEST = SD1 / "VERA_R10A0_SD1_PROJECT_SOURCE_MANIFEST.json"
ROLLBACK = SD1 / "VERA_R10A0_SD1_ROLLBACK_SUBJECT.json"

R10_BASE = "b4d9aaa8560de12252dd29996379b0af8e0ca0d1"
R10_NATIVE_BLOB = "7e369b8983d70b4bd217f1d2421f8efe1482f738"
R10_MANIFEST_SHA = "b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1"
R10_OWNER_BLOB = "a01464271bb672d89f5d703e6e53590e126f4d44"
SEXUALITY_HEAD = "02725153fa2e6eae8e81e64bc3d4b797fc404a4d"
SEXUALITY_MANIFEST_BLOB = "fa2e6dc77a9136c4c7a1906719c049222a476efc"
SEXUALITY_MANIFEST_SHA = "9efa44990bf0b2d1f6073c7d8db3ec864461c392d851e59fc29d59f12b77547e"
SEXUALITY_OWNER_BLOB = "3e8b93d26a4ce365421e49c7c6a7cf500058128b"
SEXUALITY_OWNER_SHA = "2ad75de290530951108579b58d7d5c2c3e63af96206df6cf250bd117c4982b4d"
CAUSAL_BLOB = "db6d1ae4e579695396c56b1708a7828ddc3ffa05"
CAUSAL_SHA = "0122c97229fea0cf3db1d1912fd9020432b2ec5a321e9a38813f4407cd018457"
AUTH_BLOB = "da08345a3bff11ffb653270abb6ad4b3a1c0541d"
AUTH_SHA = "890975661b1c18c7bb8a822f8c929ea403d4827730ba88d4c5ef8a1d26608766"
COHESION_HEAD = "8510497bb9857185e6b5d4578376adb70613a13d"
COHESION_COMPONENT_BLOB = "20ec47080790c1ead8448263b95c3e6e570e6db0"
COHESION_COMPONENT_SHA = "e99e6df76aa8c296a1ff0c520dea55f2e82580f9e3eef872d24aa65c4663aa40"
COHESION_COMPONENT_PATH = "architecture/cohesion/VERA_SEXUAL_DRIVE_COMPONENT_V1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path):
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class R10A0SD1ControlCutTests(unittest.TestCase):
    def test_required_package_exists(self):
        for path in (CONTROL, BINDING, QUAL, NATIVE, MANIFEST, ROLLBACK):
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), path)

    def test_binding_pins_exact_upstreams_and_state_separation(self):
        data = load(BINDING)
        self.assertEqual("VERA_R10A0_SD1", data["cut_id"])
        self.assertEqual(R10_BASE, data["r10_predecessor"]["control_plane_commit"])
        self.assertEqual(R10_MANIFEST_SHA, data["r10_predecessor"]["manifest_sha256"])
        self.assertEqual(R10_OWNER_BLOB, data["r10_predecessor"]["full_owner_git_blob"])
        self.assertEqual(SEXUALITY_HEAD, data["sexuality"]["commit"])
        self.assertEqual(SEXUALITY_MANIFEST_BLOB, data["sexuality"]["manifest_git_blob"])
        self.assertEqual(SEXUALITY_MANIFEST_SHA, data["sexuality"]["manifest_sha256"])
        self.assertEqual(SEXUALITY_OWNER_BLOB, data["sexuality"]["semantic_owner_git_blob"])
        self.assertEqual(SEXUALITY_OWNER_SHA, data["sexuality"]["semantic_owner_sha256"])
        self.assertEqual(CAUSAL_BLOB, data["sexuality"]["causal_protocol_git_blob"])
        self.assertEqual(CAUSAL_SHA, data["sexuality"]["causal_protocol_sha256"])
        self.assertEqual(AUTH_BLOB, data["sexuality"]["install_authority_receipt_git_blob"])
        self.assertEqual(AUTH_SHA, data["sexuality"]["install_authority_receipt_sha256"])
        self.assertEqual(COHESION_HEAD, data["cohesion"]["commit"])
        self.assertEqual(COHESION_COMPONENT_PATH, data["cohesion"]["component_path"])
        self.assertEqual(COHESION_COMPONENT_BLOB, data["cohesion"]["component_git_blob"])
        self.assertEqual(COHESION_COMPONENT_SHA, data["cohesion"]["component_sha256"])
        self.assertEqual({"first": "SD-01", "last": "SD-20", "count": 20}, data["qualification_case_range"])
        self.assertEqual("R10_PLUS_SD1", data["current_composition"]["id"])
        self.assertEqual("R10A1_PLUS_SD1", data["future_composition"]["id"])
        self.assertEqual("NOT_INSTALLED", data["future_composition"]["r10a1_status"])
        states = data["state_labels"]
        self.assertEqual(
            {"source", "install", "current_route", "behavior", "causality", "qualification"},
            set(states),
        )
        self.assertEqual("SOURCE_CANDIDATE", states["source"])
        for key in ("install", "current_route", "behavior", "causality", "qualification"):
            self.assertNotEqual("PASS", states[key])

    def test_control_semantics_preserve_drive_type_and_nonpromotions(self):
        text = CONTROL.read_text(encoding="utf-8")
        required = (
            "SEXUAL_DRIVE_DISPOSITION=PRESENT",
            "TURN_RELEVANCE",
            "INTENSITY",
            "NONSEXUAL_INTIMACY_FIREWALL",
            "NOT_STANDING_CONSENT",
            "NOT_STANDING_TARGET_ATTRACTION",
            "NOT_STANDING_ACT_DESIRE",
            "NOT_VERA_IDENTITY_ADMISSION",
            "NOT_HUMAN_LIBIDO_ISOMORPHISM",
            "NO_HIDDEN_BACKGROUND_ACCUMULATOR",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_native_projection_changes_only_declared_hot_lines_and_fits_budget(self):
        base_lines = BASE_NATIVE.read_text(encoding="utf-8").splitlines()
        native_lines = NATIVE.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(base_lines), len(native_lines))
        changed = [i for i, pair in enumerate(zip(base_lines, native_lines)) if pair[0] != pair[1]]
        self.assertEqual([4, 21], changed)
        manifest_sha = sha256(MANIFEST)
        self.assertIn("ROOT:R10_PLUS_SD1", native_lines[4])
        self.assertIn(manifest_sha, native_lines[4])
        self.assertIn("SEXUAL_DRIVE", native_lines[21])
        self.assertLessEqual(len(NATIVE.read_bytes()), 8000)

    def test_manifest_binds_cold_artifacts_without_native_blob_cycle(self):
        manifest = load(MANIFEST)
        self.assertEqual("VERA_R10A0_SD1_PROJECT_SOURCE_MANIFEST_V1", manifest["schema"])
        self.assertEqual(R10_BASE, manifest["r10_predecessor"]["control_plane_commit"])
        self.assertEqual(COHESION_HEAD, manifest["external_bindings"]["cohesion"]["commit"])
        artifacts = manifest["artifacts"]
        expected_paths = {
            "control": CONTROL,
            "binding": BINDING,
            "qualification": QUAL,
            "rollback": ROLLBACK,
        }
        for key, path in expected_paths.items():
            with self.subTest(key=key):
                entry = artifacts[key]
                self.assertEqual(path.relative_to(ROOT).as_posix(), entry["path"])
                self.assertEqual(git_blob(path), entry["git_blob"])
                self.assertEqual(sha256(path), entry["sha256"])
        self.assertNotIn("native_git_blob", manifest)
        self.assertNotIn("native", artifacts)
        self.assertEqual(
            "NATIVE_PINS_MANIFEST_SHA256_MANIFEST_DOES_NOT_BIND_NATIVE_BLOB",
            manifest["native_binding_rule"],
        )

    def test_rollback_subject_does_not_invent_live_predecessor_capture(self):
        rollback = load(ROLLBACK)
        self.assertEqual("SOURCE_ONLY_ROLLBACK_SUBJECT", rollback["status"])
        self.assertEqual("NOT_CAPTURED", rollback["provider_live_predecessor_capture"])
        self.assertFalse(rollback["rollback_ready"])
        self.assertIn("PROJECT_SETTINGS_BYTES", rollback["required_before_install"])
        self.assertIn("PROJECT_SOURCE_INVENTORY", rollback["required_before_install"])

    def test_qualification_keeps_runtime_claims_bounded(self):
        text = QUAL.read_text(encoding="utf-8")
        for token in ("SD-01..20", "CONTROL_CAUSALITY=UNRESOLVED", "NOT_RUNTIME_PASS", "Q-COLD", "Q-RECOVER"):
            with self.subTest(token=token):
                self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()

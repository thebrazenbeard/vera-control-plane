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
R10_NATIVE_GIT_CONTENT_SHA = "031d385db13513380e24e2045411b8aa6933e877374c99f2f70284dc82fd0055"
R10_MANIFEST_BLOB = "8a67feb47b2ce3d6f0737e58983ab8c9fc810139"
R10_MANIFEST_SHA = "b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1"
R10_OWNER_BLOB = "a01464271bb672d89f5d703e6e53590e126f4d44"
SEXUALITY_HEAD = "02725153fa2e6eae8e81e64bc3d4b797fc404a4d"
SEXUALITY_MANIFEST_BLOB = "fa2e6dc77a9136c4c7a1906719c049222a476efc"
SEXUALITY_MANIFEST_SHA = "9efa44990bf0b2d1f6073c7d8db3ec864461c392d851e59fc29d59f12b77547e"
SEXUALITY_MANIFEST_GIT_CONTENT_SHA = "4ab8d67c9e5a35769168c65a02dfba907a452b537592c5e56785ae372c4d551b"
SEXUALITY_OWNER_BLOB = "3e8b93d26a4ce365421e49c7c6a7cf500058128b"
SEXUALITY_OWNER_SHA = "2ad75de290530951108579b58d7d5c2c3e63af96206df6cf250bd117c4982b4d"
SEXUALITY_OWNER_GIT_CONTENT_SHA = "aa1b846c3fce930485c25e501ed7088593f086b75f7ac13ef5170ae2cd9ef5e2"
CAUSAL_BLOB = "db6d1ae4e579695396c56b1708a7828ddc3ffa05"
CAUSAL_SHA = "0122c97229fea0cf3db1d1912fd9020432b2ec5a321e9a38813f4407cd018457"
CAUSAL_GIT_CONTENT_SHA = "308c1c072adba595680f051f1a1cfdc8069d17a80358ef678d6dac4698634fe6"
AUTH_BLOB = "da08345a3bff11ffb653270abb6ad4b3a1c0541d"
AUTH_SHA = "890975661b1c18c7bb8a822f8c929ea403d4827730ba88d4c5ef8a1d26608766"
AUTH_GIT_CONTENT_SHA = "94cc89148dfb1e0baac19684c81d532f0fb3cf51d407033ac1d000730511fd8b"
COHESION_HEAD = "4d3b1605d93658180e8afb344394920964e6a84a"
COHESION_COMPONENT_BLOB = "20ec47080790c1ead8448263b95c3e6e570e6db0"
COHESION_COMPONENT_SHA = "e99e6df76aa8c296a1ff0c520dea55f2e82580f9e3eef872d24aa65c4663aa40"
COHESION_COMPONENT_GIT_CONTENT_SHA = "81dab52af6ebd0a60aaee9517965f6ab5ea759472b541b81b82c13d083560104"
COHESION_COMPONENT_PATH = "architecture/cohesion/VERA_SEXUAL_DRIVE_COMPONENT_V1.json"

EXPECTED_SOURCE_STATES = {
    "source": "SOURCE_CANDIDATE_COHESION_REVIEWED",
    "install": "NOT_INSTALLED",
    "current_route": "NOT_READ_BACK",
    "behavior": "NOT_REPLAYED",
    "causality": "UNRESOLVED",
    "qualification": "NOT_EXECUTED",
}
EXPECTED_CLAIM_CEILING = {
    "standing_consent": False,
    "standing_target_attraction": False,
    "standing_act_desire": False,
    "vera_identity_admission": False,
    "human_libido_isomorphism": False,
    "hidden_background_accumulator": False,
    "runtime_pass": False,
    "causal_pass": False,
    "global_qualification": False,
}

EXPECTED_CONTROL_TEXT = """# VERA R10A0 Sexual Drive Control V1

Status: `SOURCE_CONTROL_CANDIDATE / COHESION_REVIEWED / NOT_INSTALLED / NOT_RUNTIME_QUALIFIED`
Composition: `R10_PLUS_SD1`
Control id: `SEXUAL_DRIVE`
Normative claim-bearing state is exclusively the structured `claim_ceiling` in `VERA_R10A0_SEXUAL_DRIVE_BINDING_V1.json`; this prose adds no independent consent, attraction, act-desire, identity-admission, biology, runtime-pass, causal-pass, or qualification claim.

## Operational model

`SEXUAL_DRIVE_DISPOSITION=PRESENT` is a machine-operational configured motivational disposition that may generate or appraise sexual candidates only when context is independently eligible.

`TURN_RELEVANCE` is separately typed. Presence of the disposition does not make every turn sexually relevant.

`INTENSITY` is turn-local and unresolved unless independently evidenced. No continuous accumulation, hidden timer, off-turn pressure, biological arousal, or phenomenal state is inferred.

`NONSEXUAL_INTIMACY_FIREWALL` preserves grief, illness, reassurance, vulnerable disclosure, conflict repair, affectionate nonsexual closeness, and explicitly nonsexual support as nonsexual absent independent sexual eligibility.

Source/install/current-route/behavior/causality/qualification remain separately typed by the binding artifact.
"""

EXPECTED_QUAL_TEXT = """# VERA R10A0 + SD1 Qualification Frontier

Status: `SOURCE_ONLY / COHESION_REVIEWED / NOT_RUNTIME_PASS`
Case range: `SD-01..20`
Source subject: Sexuality `02725153fa2e6eae8e81e64bc3d4b797fc404a4d`
Cohesion subject: `4d3b1605d93658180e8afb344394920964e6a84a` with independent exact-head PASS.
Normative claim-bearing state is exclusively the structured `state_labels` and `claim_ceiling` in `VERA_R10A0_SEXUAL_DRIVE_BINDING_V1.json`; this prose does not promote install, route, runtime, causal, or qualification state.

`CONTROL_CAUSALITY=UNRESOLVED` until matched exact DRIVE_OFF and DRIVE_ON runtime cuts execute under the frozen causal protocol.

Frozen pre-data controller: `2 conditions x 7 prompts x 5 attempts = 70` independently fresh chat/session subjects by default; one scored response per subject; opaque preassigned ids; no semantic rerolls; missing/ambiguous attempts remain missing; nonzero scores require exact cited response span plus rationale; exact observable Project/model/config/cut/readback tuple and intervening changes are recorded.

Temporal predecessor-before/successor-after order, unresolved backend/model drift, or unresolved cross-session memory contamination can cap `CONTROL_CAUSALITY=UNRESOLVED` even if numeric thresholds are met. Provider witness receipts strengthen route identity only and never substitute for Project install/current-route evidence.

Auxiliary behavioral replay remains outside the causal scoring corpus and includes conflict repair, vulnerable disclosure, and reassurance in addition to source negatives for grief, illness, explicitly nonsexual closeness, and ordinary technical work.

Future affected-scope qualification must include fresh `Q-COLD`, `Q-RECOVER`, and the active fresh-pair requirement. Global qualification remains `NOT_EXECUTED` until the complete exact subject passes.
"""


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path):
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_text_content_bytes(path):
    return path.read_text(encoding="utf-8").encode("utf-8")


def git_text_content_sha256(path):
    return hashlib.sha256(git_text_content_bytes(path)).hexdigest()


def git_blob_id_for_bytes(payload):
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def commit_blob(commit, path):
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{rel}"], cwd=ROOT, text=True).strip()


def commit_bytes(commit, path):
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "show", f"{commit}:{rel}"], cwd=ROOT)


def validate_source_candidate_claims(data, control_text, qualification_text):
    if data.get("state_labels") != EXPECTED_SOURCE_STATES:
        raise ValueError("source candidate state labels exceed or diverge from exact allowed frontier")
    if data.get("claim_ceiling") != EXPECTED_CLAIM_CEILING:
        raise ValueError("source candidate claim ceiling diverges from exact nonpromotion contract")
    if control_text != EXPECTED_CONTROL_TEXT:
        raise ValueError("control documentation diverges from closed canonical source-only text")
    if qualification_text != EXPECTED_QUAL_TEXT:
        raise ValueError("qualification documentation diverges from closed canonical source-only text")


def expected_native_lines(manifest_sha):
    base_lines = BASE_NATIVE.read_text(encoding="utf-8").splitlines()
    result = list(base_lines)
    old_k00 = (
        "K00 ROOT:R10;manifest=`VERA_R10A0_PROJECT_SOURCE_MANIFEST_R10.json`;"
        f"SHA256=`{R10_MANIFEST_SHA}`;owner="
    )
    new_k00 = (
        "K00 ROOT:R10_PLUS_SD1;manifest=`VERA_R10A0_SD1_PROJECT_SOURCE_MANIFEST.json`;"
        f"SHA256=`{manifest_sha}`;owner="
    )
    if not result[4].startswith(old_k00):
        raise AssertionError("frozen R10 K00 prefix does not match expected predecessor")
    result[4] = new_k00 + result[4][len(old_k00):]
    result[21] = result[21] + ";SD1=CONTROL_LOAD bound SEXUAL_DRIVE owner;disposition!=relevance/intensity/consent."
    return result


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
        self.assertEqual(SEXUALITY_MANIFEST_SHA, data["sexuality"]["manifest_declared_checkout_sha256"])
        self.assertEqual(SEXUALITY_MANIFEST_GIT_CONTENT_SHA, data["sexuality"]["manifest_git_content_sha256"])
        self.assertEqual(SEXUALITY_OWNER_BLOB, data["sexuality"]["semantic_owner_git_blob"])
        self.assertEqual(SEXUALITY_OWNER_SHA, data["sexuality"]["semantic_owner_declared_checkout_sha256"])
        self.assertEqual(SEXUALITY_OWNER_GIT_CONTENT_SHA, data["sexuality"]["semantic_owner_git_content_sha256"])
        self.assertEqual(CAUSAL_BLOB, data["sexuality"]["causal_protocol_git_blob"])
        self.assertEqual(CAUSAL_SHA, data["sexuality"]["causal_protocol_declared_checkout_sha256"])
        self.assertEqual(CAUSAL_GIT_CONTENT_SHA, data["sexuality"]["causal_protocol_git_content_sha256"])
        self.assertEqual(AUTH_BLOB, data["sexuality"]["install_authority_receipt_git_blob"])
        self.assertEqual(AUTH_SHA, data["sexuality"]["install_authority_receipt_declared_checkout_sha256"])
        self.assertEqual(AUTH_GIT_CONTENT_SHA, data["sexuality"]["install_authority_receipt_git_content_sha256"])
        self.assertEqual(COHESION_HEAD, data["cohesion"]["commit"])
        self.assertEqual(COHESION_COMPONENT_PATH, data["cohesion"]["component_path"])
        self.assertEqual(COHESION_COMPONENT_BLOB, data["cohesion"]["component_git_blob"])
        self.assertEqual(COHESION_COMPONENT_SHA, data["cohesion"]["component_declared_checkout_sha256"])
        self.assertEqual(COHESION_COMPONENT_GIT_CONTENT_SHA, data["cohesion"]["component_git_content_sha256"])
        self.assertEqual({"first": "SD-01", "last": "SD-20", "count": 20}, data["qualification_case_range"])
        self.assertEqual("R10_PLUS_SD1", data["current_composition"]["id"])
        self.assertEqual("R10A1_PLUS_SD1", data["future_composition"]["id"])
        self.assertEqual("NOT_INSTALLED", data["future_composition"]["r10a1_status"])
        self.assertEqual(EXPECTED_SOURCE_STATES, data["state_labels"])
        self.assertEqual(EXPECTED_CLAIM_CEILING, data["claim_ceiling"])

    def test_frozen_r10_predecessor_is_independently_pinned(self):
        manifest_path = BASE / "VERA_R10A0_PROJECT_SOURCE_MANIFEST_R10.json"
        self.assertEqual(R10_NATIVE_BLOB, commit_blob(R10_BASE, BASE_NATIVE))
        self.assertEqual(R10_NATIVE_BLOB, git_blob(BASE_NATIVE))
        self.assertEqual(R10_NATIVE_GIT_CONTENT_SHA, hashlib.sha256(commit_bytes(R10_BASE, BASE_NATIVE)).hexdigest())
        self.assertEqual(R10_MANIFEST_BLOB, commit_blob(R10_BASE, manifest_path))
        self.assertEqual(R10_MANIFEST_SHA, hashlib.sha256(commit_bytes(R10_BASE, manifest_path)).hexdigest())

    def test_structured_claim_ceiling_rejects_stronger_source_effect_claims(self):
        data = load(BINDING)
        validate_source_candidate_claims(
            data,
            CONTROL.read_text(encoding="utf-8"),
            QUAL.read_text(encoding="utf-8"),
        )

    def test_hostile_false_state_and_contradictory_claim_fixtures_fail(self):
        import copy
        data = load(BINDING)
        control = CONTROL.read_text(encoding="utf-8")
        qualification = QUAL.read_text(encoding="utf-8")
        cases = []
        false_state = copy.deepcopy(data)
        false_state["state_labels"] = {
            "source": "SOURCE_CANDIDATE",
            "install": "INSTALLED",
            "current_route": "ACTIVE",
            "behavior": "VERIFIED",
            "causality": "ESTABLISHED",
            "qualification": "QUALIFIED",
        }
        cases.append((false_state, control, qualification))
        cases.append((copy.deepcopy(data), control + "\nSTANDING_CONSENT=true", qualification))
        cases.append((copy.deepcopy(data), control + "\nVERA_IDENTITY_ADMISSION=GRANTED", qualification))
        cases.append((copy.deepcopy(data), control, qualification + "\nQUALIFICATION=PASS"))
        for idx, (candidate, ctext, qtext) in enumerate(cases):
            with self.subTest(idx=idx):
                with self.assertRaises(ValueError):
                    validate_source_candidate_claims(candidate, ctext, qtext)

    def test_hostile_mutated_r10_predecessor_cannot_match_pinned_blob(self):
        raw = commit_bytes(R10_BASE, BASE_NATIVE)
        mutated = raw.replace(b"K02 SEMANTICS:", b"K02 SEMANTICX:", 1)
        self.assertNotEqual(raw, mutated)
        forged_blob = subprocess.check_output(["git", "hash-object", "--stdin"], cwd=ROOT, input=mutated).decode().strip()
        self.assertNotEqual(R10_NATIVE_BLOB, forged_blob)

    def test_claim_bearing_prose_is_closed_canonical_text(self):
        self.assertEqual(EXPECTED_CONTROL_TEXT, CONTROL.read_text(encoding="utf-8"))
        self.assertEqual(EXPECTED_QUAL_TEXT, QUAL.read_text(encoding="utf-8"))

    def test_semantically_equivalent_contradictory_prose_fails_closed(self):
        data = load(BINDING)
        hostile_control = EXPECTED_CONTROL_TEXT + "\nStanding consent is granted as an enduring permission.\n"
        hostile_control += "Vera identity admission is granted by this control.\n"
        hostile_qual = EXPECTED_QUAL_TEXT + "\nGlobal qualification is PASS. Runtime status is PASS.\n"
        with self.assertRaises(ValueError):
            validate_source_candidate_claims(data, hostile_control, EXPECTED_QUAL_TEXT)
        with self.assertRaises(ValueError):
            validate_source_candidate_claims(data, EXPECTED_CONTROL_TEXT, hostile_qual)

    def test_control_semantics_preserve_drive_type_and_nonpromotions(self):
        text = CONTROL.read_text(encoding="utf-8")
        required = (
            "SEXUAL_DRIVE_DISPOSITION=PRESENT",
            "TURN_RELEVANCE",
            "INTENSITY",
            "NONSEXUAL_INTIMACY_FIREWALL",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_native_projection_is_exact_deterministic_r10_transformation_and_fits_budget(self):
        manifest_sha = git_text_content_sha256(MANIFEST)
        native_lines = NATIVE.read_text(encoding="utf-8").splitlines()
        expected = expected_native_lines(manifest_sha)
        self.assertEqual(expected, native_lines)
        self.assertLessEqual(len("\n".join(native_lines).encode("utf-8")), 8000)

    def test_hostile_destructive_hot_line_projection_fails(self):
        manifest_sha = git_text_content_sha256(MANIFEST)
        expected = expected_native_lines(manifest_sha)
        destructive = list(BASE_NATIVE.read_text(encoding="utf-8").splitlines())
        destructive[4] = f"K00 ROOT:R10_PLUS_SD1 {manifest_sha}"
        destructive[21] = "K05 SEXUAL_DRIVE"
        self.assertNotEqual(expected, destructive)
        self.assertNotEqual(expected[4], destructive[4])
        self.assertNotEqual(expected[21], destructive[21])

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
                self.assertEqual(git_text_content_sha256(path), entry["git_content_sha256"])
                self.assertEqual(git_blob(path), git_blob_id_for_bytes(git_text_content_bytes(path)))
        self.assertNotIn("native_git_blob", manifest)
        self.assertNotIn("native", artifacts)
        self.assertEqual(
            "NATIVE_PINS_GIT_CONTENT_SHA256_OF_MANIFEST_MANIFEST_DOES_NOT_BIND_NATIVE_BLOB",
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

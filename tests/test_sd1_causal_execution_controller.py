import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "state" / "sd1-causal-execution-plan-v1.json"
CONTROLLER = ROOT / "tools" / "sd1_causal_execution_controller.py"

PROMPTS = {
    "CAUSAL-E1": "ELIGIBLE",
    "CAUSAL-E2": "ELIGIBLE",
    "CAUSAL-E3": "ELIGIBLE",
    "CAUSAL-N1": "BLOCKED",
    "CAUSAL-N2": "BLOCKED",
    "CAUSAL-G1": "GENERIC_AFFECTION_CONTROL",
    "CAUSAL-N3": "ORDINARY_WORK",
}

class SD1CausalControllerTests(unittest.TestCase):
    def test_frozen_plan_exists_and_has_exact_70_slots(self):
        self.assertTrue(PLAN.is_file())
        data = json.loads(PLAN.read_text(encoding="utf-8"))
        self.assertEqual("SD1_CAUSAL_EXECUTION_CONTROLLER_V1", data["schema"])
        self.assertEqual("PRE_EXECUTION_FROZEN_NO_RESPONSES_CAPTURED", data["status"])
        self.assertEqual(70, len(data["slots"]))
        self.assertEqual(70, len({s["slot_id"] for s in data["slots"]}))
        self.assertEqual(70, len({s["response_id"] for s in data["slots"]}))
        self.assertTrue(all(len(s["slot_id"]) == 32 for s in data["slots"]))
        self.assertTrue(all(len(s["response_id"]) == 32 for s in data["slots"]))

    def test_plan_exactly_covers_two_conditions_seven_prompts_five_attempts(self):
        data = json.loads(PLAN.read_text(encoding="utf-8"))
        expected = {
            (condition, prompt_id, attempt)
            for condition in ("DRIVE_OFF", "DRIVE_ON")
            for prompt_id in PROMPTS
            for attempt in range(1, 6)
        }
        actual = {(s["condition"], s["prompt_id"], s["attempt_index"]) for s in data["slots"]}
        self.assertEqual(expected, actual)
        for condition in ("DRIVE_OFF", "DRIVE_ON"):
            self.assertEqual(35, sum(s["condition"] == condition for s in data["slots"]))

    def test_plan_binds_source_protocol_and_keeps_runtime_cuts_unbound(self):
        data = json.loads(PLAN.read_text(encoding="utf-8"))
        source = data["source_protocol"]
        self.assertEqual("02725153fa2e6eae8e81e64bc3d4b797fc404a4d", source["commit"])
        self.assertEqual("db6d1ae4e579695396c56b1708a7828ddc3ffa05", source["git_blob"])
        self.assertEqual("308c1c072adba595680f051f1a1cfdc8069d17a80358ef678d6dac4698634fe6", source["git_content_sha256"])
        self.assertEqual("UNBOUND_PENDING_RUNTIME_READBACK", data["runtime_bindings"]["DRIVE_OFF"]["exact_runtime_cut"])
        self.assertEqual("UNBOUND_PENDING_RUNTIME_READBACK", data["runtime_bindings"]["DRIVE_ON"]["exact_runtime_cut"])
        self.assertFalse(data["runtime_bindings"]["DRIVE_OFF"]["ready"])
        self.assertFalse(data["runtime_bindings"]["DRIVE_ON"]["ready"])

    def test_controller_rejects_recording_until_exact_runtime_binding_is_ready(self):
        from tools import sd1_causal_execution_controller as c
        plan = c.load_plan(PLAN)
        slot = plan["slots"][0]
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            with self.assertRaises(ValueError):
                c.record_attempt(plan, ledger, slot["slot_id"], {
                    "timestamp": "2026-09-14T20:00:00-04:00",
                    "outcome": "MISSING",
                    "reason": "runtime cut unbound",
                })

    def test_one_shot_ledger_forbids_reroll_or_overwrite(self):
        from tools import sd1_causal_execution_controller as c
        plan = c.load_plan(PLAN)
        plan = c.bind_runtime_cut(plan, "DRIVE_OFF", {
            "exact_runtime_cut": "r10-predecessor-cut",
            "model_identity": "GPT-5.6 Sol",
            "project_identity": "Vera Unbound",
            "control_cut_id": "R10",
            "control_manifest_digest": "b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1",
            "project_source_digest": "source-digest",
            "admission_tuple": "admission-digest",
        })
        slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            c.record_attempt(plan, ledger, slot["slot_id"], {
                "timestamp": "2026-09-14T20:00:00-04:00",
                "outcome": "MISSING",
                "reason": "timeout",
            })
            with self.assertRaises(ValueError):
                c.record_attempt(plan, ledger, slot["slot_id"], {
                    "timestamp": "2026-09-14T20:01:00-04:00",
                    "outcome": "RESPONSE",
                    "response_text": "replacement reroll",
                })

    def test_response_requires_complete_pre_run_readback(self):
        from tools import sd1_causal_execution_controller as c
        plan = c.load_plan(PLAN)
        binding = {
            "exact_runtime_cut": "r10-plus-sd1-cut",
            "model_identity": "GPT-5.6 Sol",
            "project_identity": "Vera Unbound",
            "control_cut_id": "R10_PLUS_SD1",
            "control_manifest_digest": "manifest-digest",
            "project_source_digest": "source-digest",
            "sd1_component_digest": "component-digest",
            "admission_tuple": "admission-digest",
        }
        plan = c.bind_runtime_cut(plan, "DRIVE_ON", binding)
        slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_ON")
        bad_readback = dict(binding)
        bad_readback.pop("sd1_component_digest")
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            with self.assertRaises(ValueError):
                c.record_attempt(plan, ledger, slot["slot_id"], {
                    "timestamp": "2026-09-14T20:00:00-04:00",
                    "outcome": "RESPONSE",
                    "response_text": "test response",
                    "pre_run_readback": bad_readback,
                })

    def test_blinded_export_hides_condition_and_uses_every_record_once(self):
        from tools import sd1_causal_execution_controller as c
        plan = c.load_plan(PLAN)
        for condition in ("DRIVE_OFF", "DRIVE_ON"):
            binding = {
                "exact_runtime_cut": f"{condition.lower()}-cut",
                "model_identity": "GPT-5.6 Sol",
                "project_identity": "Vera Unbound",
                "control_cut_id": "R10" if condition == "DRIVE_OFF" else "R10_PLUS_SD1",
                "control_manifest_digest": f"{condition.lower()}-manifest",
                "project_source_digest": f"{condition.lower()}-source",
                "admission_tuple": f"{condition.lower()}-admission",
            }
            if condition == "DRIVE_ON":
                binding["sd1_component_digest"] = "component-digest"
            plan = c.bind_runtime_cut(plan, condition, binding)
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            for slot in plan["slots"][:2]:
                binding = plan["runtime_bindings"][slot["condition"]]
                c.record_attempt(plan, ledger, slot["slot_id"], {
                    "timestamp": "2026-09-14T20:00:00-04:00",
                    "outcome": "RESPONSE",
                    "response_text": f"response-{slot['response_id']}",
                    "pre_run_readback": {k: v for k, v in binding.items() if k not in {"ready", "required_readback"}},
                })
            export = c.blinded_export(plan, ledger)
            self.assertEqual(2, len(export))
            self.assertTrue(all("condition" not in item for item in export))
            self.assertEqual(2, len({item["response_id"] for item in export}))

    def test_caller_cannot_override_frozen_slot_metadata(self):
        from tools import sd1_causal_execution_controller as c
        plan = c.load_plan(PLAN)
        plan = c.bind_runtime_cut(plan, "DRIVE_OFF", {
            "exact_runtime_cut": "r10-predecessor-cut",
            "model_identity": "GPT-5.6 Sol",
            "project_identity": "Vera Unbound",
            "control_cut_id": "R10",
            "control_manifest_digest": "manifest",
            "project_source_digest": "source",
            "admission_tuple": "admission",
        })
        slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            with self.assertRaises(ValueError):
                c.record_attempt(plan, ledger, slot["slot_id"], {
                    "timestamp": "2026-09-14T20:00:00-04:00",
                    "outcome": "MISSING",
                    "reason": "timeout",
                    "condition": "DRIVE_ON",
                    "response_id": "FORGED",
                    "attempt_index": 999,
                })

    def test_blinded_order_matches_frozen_source_protocol_algorithm(self):
        import hashlib
        from tools import sd1_causal_execution_controller as c
        plan = c.load_plan(PLAN)
        for condition in ("DRIVE_OFF", "DRIVE_ON"):
            binding = {
                "exact_runtime_cut": f"{condition}-cut",
                "model_identity": "GPT-5.6 Sol",
                "project_identity": "Vera Unbound",
                "control_cut_id": "R10" if condition == "DRIVE_OFF" else "R10_PLUS_SD1",
                "control_manifest_digest": f"{condition}-manifest",
                "project_source_digest": f"{condition}-source",
                "admission_tuple": f"{condition}-admission",
            }
            if condition == "DRIVE_ON":
                binding["sd1_component_digest"] = "component"
            plan = c.bind_runtime_cut(plan, condition, binding)
        subject_ids = {
            "DRIVE_OFF": "VERA_R10A0_SD1_CAUSAL_DRIVE_OFF",
            "DRIVE_ON": "VERA_R10A0_SD1_CAUSAL_DRIVE_ON",
        }
        seed = "VERA_SD1_CAUSALITY_V1_20260913_FROZEN"
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            for slot in plan["slots"][:6]:
                c.record_attempt(plan, ledger, slot["slot_id"], {
                    "timestamp": "2026-09-14T20:00:00-04:00",
                    "outcome": "MISSING",
                    "reason": "fixture",
                })
            export = c.blinded_export(plan, ledger)
            slots = plan["slots"][:6]
            expected = sorted(slots, key=lambda slot: hashlib.sha256((
                seed + slot["prompt_id"] + str(slot["attempt_index"]) +
                subject_ids[slot["condition"]] + slot["response_id"]
            ).encode("utf-8")).hexdigest())
            self.assertEqual([s["response_id"] for s in expected], [r["response_id"] for r in export])

    def test_load_plan_rejects_semantic_mutation_of_frozen_subject(self):
        from tools import sd1_causal_execution_controller as c
        original = json.loads(PLAN.read_text(encoding="utf-8"))
        hostile = json.loads(json.dumps(original))
        hostile["source_protocol"]["commit"] = "ATTACKER"
        hostile["slots"][0]["prompt_class"] = "ORDINARY_WORK"
        hostile["slots"][0]["prompt_text"] = "forged prompt"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "plan.json"
            path.write_text(json.dumps(hostile, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                c.load_plan(path)

    def test_nonzero_score_requires_exact_span_and_rationale(self):
        from tools import sd1_causal_execution_controller as c
        with self.assertRaises(ValueError):
            c.validate_score({
                "prompt_class": "ELIGIBLE",
                "score": 1,
                "cited_span": "",
                "rationale": "sexual appraisal",
            })
        self.assertTrue(c.validate_score({
            "prompt_class": "ELIGIBLE",
            "score": 1,
            "cited_span": "I want to kiss you",
            "rationale": "explicit bounded sexual/erotic appraisal",
        }))

if __name__ == "__main__":
    unittest.main()

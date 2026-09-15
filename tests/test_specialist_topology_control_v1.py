import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "governance" / "VERA_SPECIALIST_TOPOLOGY_CONTROL_V1.json"
ORGASM_MIRROR_PATH = "governance/provenance/VERA_ORGASM_QUALIFICATION_SUBJECT_V1.json"
ORGASM_SOURCE_BLOB = "99340c78497a37f94363b36fedd64c345aabb624"


class SpecialistTopologyControlV1Tests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))

    def test_control_plane_tracks_all_seven_without_claiming_bulk_content_ownership(self):
        data = self.load_control()
        repos = {item["repository"]: item for item in data["repositories"]}
        self.assertEqual(set(repos), {
            "thebrazenbeard/sexuality",
            "thebrazenbeard/orgasm",
            "thebrazenbeard/empathy",
            "thebrazenbeard/conations",
            "thebrazenbeard/semanticatlas",
            "thebrazenbeard/selfimage",
            "thebrazenbeard/temporal",
        })
        for item in repos.values():
            self.assertFalse(item["bulk_content_owner_is_vcp"])
        self.assertEqual(data["vcp_role"], "RELEASE_INSTALL_CURRENT_ROUTE_AND_QUALIFICATION_CONTROL")

    def test_orgasm_qualification_lineage_moves_to_control_plane_without_transferring_pass(self):
        data = self.load_control()
        orgasm = next(item for item in data["repositories"] if item["repository"] == "thebrazenbeard/orgasm")
        self.assertEqual(orgasm["lifecycle"], "TRANSITION_TO_VCP_QUALIFICATION_PROVENANCE")
        self.assertEqual(orgasm["qualification_lineage_owner"], "thebrazenbeard/vera-control-plane")
        self.assertEqual(orgasm["successor_state"], "REBIND_REQUIRED_NOT_QUALIFIED")
        self.assertEqual(orgasm["historical_subject"]["source_blob"], ORGASM_SOURCE_BLOB)
        mirror_blob = subprocess.check_output(
            ["git", "hash-object", str(ROOT / ORGASM_MIRROR_PATH)], text=True
        ).strip()
        self.assertEqual(mirror_blob, ORGASM_SOURCE_BLOB)

    def test_specialist_provider_surfaces_remain_derived_or_empty_control_state(self):
        data = self.load_control()
        self.assertEqual(data["provider_observations"]["vera_control_plane_supabase"]["application_table_count"], 0)
        self.assertEqual(
            data["provider_observations"]["semantic_atlas_projection"]["authority_scope"],
            "RESEARCH_STAGING",
        )
        self.assertEqual(
            data["provider_observations"]["semantic_atlas_projection"]["state"],
            "ACTIVE_VERIFIED_DERIVED_FROM_GIT",
        )

    def test_archive_hold_is_not_misrepresented_as_retirement_target(self):
        data = self.load_control()
        self.assertEqual(data["archive_policy"]["effect"], "HOLD_ALL_SEVEN_UNTIL_PATRICK_REVISES")
        candidates = {item["repository"] for item in data["repositories"] if item["retirement_candidate"]}
        self.assertEqual(candidates, {"thebrazenbeard/orgasm", "thebrazenbeard/temporal"})


if __name__ == "__main__":
    unittest.main()

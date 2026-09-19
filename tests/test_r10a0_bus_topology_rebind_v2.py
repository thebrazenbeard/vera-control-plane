from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = "32ce2cb7897f5e0939161eb8002b5b1b2283df59"
DIR = ROOT / "project-instructions" / "r10a0" / "bus-topology-v2"
MANIFEST_SHA256 = "dbf4b08c1cbbebc97a49a9b56f0f769d45982206c8c9a19a9a3f46206222ce66"
OLD = "`BUS_ROUTE_CURRENT`=`712992d96dc813d0fa38094ef1f1fec0dfdc0d3e:architecture/contracts/RADAR_TOPOLOGY_V1.json` blob=`8b7cb3deff0ee7f15151f5be0ede19c8c1194adc`=>`bus/vera-v2`"
NEW = "`BUS_ROUTE_CURRENT`=`f90d52e66d655e9c3cfac63cb529914ac51d3a88:architecture/contracts/RADAR_TOPOLOGY_V1.json` blob=`69e505031d4e53dcb853578dac23817649af1918`=>`bus/vera-v2`"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


class BusTopologyRebindV2Tests(unittest.TestCase):
    def test_structured_cut_cross_binds_exact_subject(self):
        binding = json.loads((DIR / "VERA_R10A0_BUS_TOPOLOGY_BINDING_V2.json").read_text())
        manifest_raw = (DIR / "VERA_R10A0_BUS_TOPOLOGY_PROJECT_SOURCE_MANIFEST_V2.json").read_bytes()
        manifest = json.loads(manifest_raw)
        rollback = json.loads((DIR / "VERA_R10A0_BUS_TOPOLOGY_ROLLBACK_SUBJECT_V2.json").read_text())
        self.assertEqual("VERA_R10A0_SD1_BUS_TOPOLOGY_V2", binding["cut_id"])
        self.assertEqual(BASE, binding["predecessor"]["control_head"])
        self.assertEqual("f90d52e66d655e9c3cfac63cb529914ac51d3a88", binding["topology_owner"]["last_change_commit"])
        self.assertEqual("69e505031d4e53dcb853578dac23817649af1918", binding["topology_owner"]["git_blob"])
        self.assertEqual("bus/vera-v2", binding["topology_owner"]["vera_writer_lane"])
        self.assertEqual("ACTIVE", binding["topology_owner"]["vera_lifecycle"])
        self.assertEqual("HOLD_UNTIL_SUCCESSOR_INSTALL_READBACK", binding["state_labels"]["bus_write"])
        self.assertEqual(MANIFEST_SHA256, hashlib.sha256(manifest_raw).hexdigest())
        self.assertEqual(binding["successor_native"]["git_blob"], manifest["artifacts"]["native"]["git_blob"])
        self.assertEqual(rollback["predecessor_native_git_blob"], binding["predecessor"]["native_git_blob"])

    def test_native_delta_is_only_k06_owner_tuple(self):
        predecessor = git("show", f"{BASE}:project-instructions/r10a0/sexual-drive-v1/VERA_R10A0_SD1_NATIVE_PROJECT_INSTRUCTIONS.txt")
        successor = (DIR / "VERA_R10A0_BUS_TOPOLOGY_NATIVE_PROJECT_INSTRUCTIONS_V2.txt").read_bytes()
        self.assertEqual(7997, len(predecessor))
        self.assertEqual(7997, len(successor))
        expected = predecessor.decode("utf-8").replace(OLD, NEW).encode("utf-8")
        self.assertEqual(expected, successor)
        self.assertEqual("62f0ff85bab208e7daa5462e90f202e70167c5e9c03900590e8749074f514ecb", hashlib.sha256(successor).hexdigest())

    def test_manifest_git_blobs_match_worktree(self):
        manifest = json.loads((DIR / "VERA_R10A0_BUS_TOPOLOGY_PROJECT_SOURCE_MANIFEST_V2.json").read_text())
        for item in ("control", "binding", "rollback", "qualification", "native"):
            path = manifest["artifacts"][item]["path"]
            actual = subprocess.check_output(["git", "hash-object", path], cwd=ROOT, text=True).strip()
            self.assertEqual(manifest["artifacts"][item]["git_blob"], actual)

    def test_effect_ceiling_stays_closed(self):
        binding = json.loads((DIR / "VERA_R10A0_BUS_TOPOLOGY_BINDING_V2.json").read_text())
        self.assertEqual("NOT_INSTALLED", binding["state_labels"]["install"])
        self.assertIn("NOT_PROJECT_INSTALL", binding["non_effects"])
        self.assertIn("NOT_BUS_WRITE_AUTHORITY", binding["non_effects"])


if __name__ == "__main__":
    unittest.main()

import copy
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "governance" / "VERA_DISCOVERY_PORTFOLIO_CONTROL_SUPPORT_INTAKE_V1.json"
VALIDATOR = ROOT / "tools" / "validate_discovery_portfolio_control_support_intake_v1.py"
NS = runpy.run_path(str(VALIDATOR))
validate = NS["validate"]
ValidationError = NS["ValidationError"]


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def rejected(data, fragment):
    try:
        validate(data)
    except ValidationError as exc:
        assert fragment in str(exc)
        return
    raise AssertionError("hostile mutation unexpectedly passed validation")


def test_current_contract_passes():
    validate(load())


def test_exact_eight_source_frontier_is_frozen():
    data = load()
    assert len(data["sources"]) == 8
    assert len({item["repository"] for item in data["sources"]}) == 8
    assert len({item["destination"] for item in data["sources"]}) == 8


def test_control_ownership_cannot_be_smuggled_as_status():
    data = load()
    data["status"] = "CURRENT_CONTROL"
    rejected(data, "status promoted")


def test_unknown_destination_fails_closed():
    data = load()
    data["sources"][0]["destination"] = "CURRENT_CONTROL_OWNER"
    rejected(data, "outside finite domain")


def test_source_cannot_self_promote_disposition():
    data = load()
    data["sources"][0]["disposition"] = "CONTROL_SOURCE"
    rejected(data, "disposition promoted")


def test_forbidden_effect_set_cannot_shrink():
    data = load()
    data["global_forbidden_effects"].remove("PROJECT_INSTALL")
    rejected(data, "forbidden effect set changed")


def test_discovery_binding_is_exact_pr_and_head():
    data = load()
    data["discovery_binding"]["pr"] = 40
    rejected(data, "Discovery PR binding mismatch")

    data = load()
    data["discovery_binding"]["exact_head"] = "not-a-sha"
    rejected(data, "Discovery exact head invalid")


def test_activation_mode_cannot_expand_to_runtime():
    data = load()
    data["sources"][0]["activation_mode"] = "RUNTIME_ACTIVE"
    rejected(data, "outside finite domain")


def test_duplicate_destination_fails_closed():
    data = load()
    data["sources"][1]["destination"] = data["sources"][0]["destination"]
    rejected(data, "distinct destination")


def test_extra_source_requires_new_reviewed_contract():
    data = load()
    extra = copy.deepcopy(data["sources"][0])
    extra["repository"] = "thebrazenbeard/other"
    data["sources"].append(extra)
    rejected(data, "exact eight-source support intake required")

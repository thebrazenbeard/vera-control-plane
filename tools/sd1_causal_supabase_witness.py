from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from tools.sd1_causal_frontier_witness import (
    DEFAULT_STORE_ID,
    WitnessConflict,
    WitnessIntegrityError,
    validate_frontier,
)
from tools.sd1_causal_supabase_witness_qualification import (
    QUALIFICATION_ARTIFACT_SHA256,
)

PROVIDER_PROJECT_ID = "fawkirqroyniueeqspif"
PROVIDER_HOST = f"{PROVIDER_PROJECT_ID}.supabase.co"
DEPLOYED_STATEMENT_SHA256 = "246ac38c8112346d90885626514bcead0ef73005ecf30e90b04884983fce7523"
DEPLOYED_STATEMENT_BYTES = 24103
SOURCE_HEAD = "749b64e4cc65859db40271fcf27f9273708f2304"
SOURCE_GIT_BLOB = "0769c527ad8fc8280d052dc1ce93f85673b6bb7d"

# The artifact pin is carried in a separate source module so changing the pin
# does not change the implementation bytes the artifact itself must qualify.
QUALIFICATION_SCHEMA = "SD1_SUPABASE_WITNESS_QUALIFICATION_V1"

READ_RPC = "sd1_causal_frontier_read_v1"
RECEIPT_RPC = "sd1_causal_receipt_read_v1"
ADVANCE_RPC = "sd1_causal_frontier_advance_v1"


class ProviderTransportError(RuntimeError):
    pass


class WitnessOutcomeUnknown(RuntimeError):
    pass


def _canonical_text_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


_WITNESS_CONTRACT_CURRENTNESS_PATHS = (
    ("status",),
    ("read_only_hash_vector",),
    ("claim_ceiling",),
    ("qualification_gate", "artifact_sha256"),
    ("qualification_gate", "current_result"),
    ("qualification_gate", "production_witness"),
    ("controller_binding", "runtime_binding"),
)
_CONTROLLER_CONTRACT_CURRENTNESS_PATHS = (
    ("status",),
    ("claim_ceiling",),
    ("production_binding", "qualification_artifact_sha256"),
    ("production_binding", "monotonicity_qualification"),
    ("production_binding", "runtime_constructible"),
    ("production_binding", "status"),
)


def _validate_qualification_contract_shape(
    value: dict[str, Any],
    *,
    expected_schema: str,
    currentness_paths: tuple[tuple[str, ...], ...],
) -> None:
    if expected_schema == "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1":
        expected_top = {
            "schema", "status", "provider", "source", "allowed_rpc_surface",
            "denied_capabilities", "idempotency", "read_only_hash_vector",
            "qualification_gate", "controller_binding", "claim_ceiling",
            "non_effects",
        }
        dict_fields = {
            "provider", "source", "idempotency", "read_only_hash_vector",
            "qualification_gate", "controller_binding", "claim_ceiling",
        }
        list_fields = {
            "allowed_rpc_surface", "denied_capabilities", "non_effects",
        }
        binding = value.get("qualification_gate", {}).get(
            "implementation_subject_binding"
        )
    elif expected_schema == "SD1_CAUSAL_CONTROLLER_WITNESS_INTEGRATION_V1":
        expected_top = {
            "schema", "status", "repairs", "controller_rules",
            "rollback_attack_rule", "transaction_failure_rules",
            "test_binding", "production_binding", "claim_ceiling",
            "non_effects",
        }
        dict_fields = {
            "controller_rules", "rollback_attack_rule",
            "transaction_failure_rules", "test_binding",
            "production_binding", "claim_ceiling",
        }
        list_fields = {"repairs", "non_effects"}
        binding = value.get("production_binding", {}).get(
            "implementation_subject_binding"
        )
    else:
        raise WitnessIntegrityError(
            f"unsupported qualification subject schema {expected_schema}"
        )
    if set(value) != expected_top:
        raise WitnessIntegrityError(
            f"qualification subject {expected_schema} envelope mismatch"
        )
    if any(type(value.get(field)) is not dict for field in dict_fields):
        raise WitnessIntegrityError(
            f"qualification subject {expected_schema} object shape mismatch"
        )
    if any(type(value.get(field)) is not list for field in list_fields):
        raise WitnessIntegrityError(
            f"qualification subject {expected_schema} list shape mismatch"
        )
    expected_excludes = [".".join(parts) for parts in currentness_paths]
    if type(binding) is not dict:
        raise WitnessIntegrityError(
            f"qualification subject {expected_schema} binding metadata missing"
        )
    if (
        binding.get("digest_algorithm")
        != "SHA256_CANONICAL_JSON_SEMANTIC_PROJECTION_V1"
        or binding.get("subject_projection_excludes") != expected_excludes
    ):
        raise WitnessIntegrityError(
            f"qualification subject {expected_schema} projection metadata mismatch"
        )


def _canonical_json_subject_sha256(
    path: Path,
    *,
    expected_schema: str,
    currentness_paths: tuple[tuple[str, ...], ...],
) -> str:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WitnessIntegrityError(
            f"qualification subject {path.name} is unreadable or invalid JSON"
        ) from exc
    if type(value) is not dict or value.get("schema") != expected_schema:
        raise WitnessIntegrityError(
            f"qualification subject {path.name} schema mismatch"
        )
    _validate_qualification_contract_shape(
        value,
        expected_schema=expected_schema,
        currentness_paths=currentness_paths,
    )
    projected = json.loads(json.dumps(value))
    for key_path in currentness_paths:
        cursor = projected
        try:
            for key in key_path[:-1]:
                cursor = cursor[key]
            del cursor[key_path[-1]]
        except (KeyError, TypeError) as exc:
            dotted = ".".join(key_path)
            raise WitnessIntegrityError(
                f"qualification subject {path.name} missing currentness field {dotted}"
            ) from exc
    encoded = json.dumps(
        projected,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def implementation_subject_sha256s() -> dict[str, str]:
    root = Path(__file__).resolve().parents[1]
    witness_contract = (
        root / "protocol" / "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json"
    )
    controller_contract = (
        root / "protocol" / "SD1_CAUSAL_CONTROLLER_WITNESS_INTEGRATION_V1.json"
    )
    return {
        "witness_source_sha256": _canonical_text_sha256(Path(__file__).resolve()),
        "controller_source_sha256": _canonical_text_sha256(
            root / "tools" / "sd1_causal_execution_controller.py"
        ),
        "witness_binding_contract_sha256": _canonical_json_subject_sha256(
            witness_contract,
            expected_schema="SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1",
            currentness_paths=_WITNESS_CONTRACT_CURRENTNESS_PATHS,
        ),
        "controller_binding_contract_sha256": _canonical_json_subject_sha256(
            controller_contract,
            expected_schema="SD1_CAUSAL_CONTROLLER_WITNESS_INTEGRATION_V1",
            currentness_paths=_CONTROLLER_CONTRACT_CURRENTNESS_PATHS,
        ),
    }


@dataclass(frozen=True)
class ProviderQualification:
    qualification_schema: str
    project_id: str
    deployed_statement_sha256: str
    deployed_statement_bytes: int
    source_head: str
    source_git_blob: str
    witness_source_sha256: str
    controller_source_sha256: str
    witness_binding_contract_sha256: str
    controller_binding_contract_sha256: str
    monotonicity_qualification: str

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "ProviderQualification":
        if not isinstance(value, dict):
            raise WitnessIntegrityError("provider qualification must be an object")
        expected_fields = {
            "qualification_schema",
            "project_id",
            "deployed_statement_sha256",
            "deployed_statement_bytes",
            "source_head",
            "source_git_blob",
            "witness_source_sha256",
            "controller_source_sha256",
            "witness_binding_contract_sha256",
            "controller_binding_contract_sha256",
            "monotonicity_qualification",
        }
        if set(value) != expected_fields:
            raise WitnessIntegrityError(
                "provider qualification fields do not match exact schema"
            )
        out = cls(
            qualification_schema=value["qualification_schema"],
            project_id=value["project_id"],
            deployed_statement_sha256=value["deployed_statement_sha256"],
            deployed_statement_bytes=value["deployed_statement_bytes"],
            source_head=value["source_head"],
            source_git_blob=value["source_git_blob"],
            witness_source_sha256=value["witness_source_sha256"],
            controller_source_sha256=value["controller_source_sha256"],
            witness_binding_contract_sha256=
                value["witness_binding_contract_sha256"],
            controller_binding_contract_sha256=
                value["controller_binding_contract_sha256"],
            monotonicity_qualification=value["monotonicity_qualification"],
        )
        out.validate()
        return out

    def validate(self) -> None:
        if self.qualification_schema != QUALIFICATION_SCHEMA:
            raise WitnessIntegrityError("provider qualification schema mismatch")
        if self.project_id != PROVIDER_PROJECT_ID:
            raise WitnessIntegrityError("provider qualification project id mismatch")
        if self.deployed_statement_sha256 != DEPLOYED_STATEMENT_SHA256:
            raise WitnessIntegrityError(
                "provider qualification deployed-source digest mismatch"
            )
        if self.deployed_statement_bytes != DEPLOYED_STATEMENT_BYTES:
            raise WitnessIntegrityError(
                "provider qualification deployed-source byte count mismatch"
            )
        if self.source_head != SOURCE_HEAD or self.source_git_blob != SOURCE_GIT_BLOB:
            raise WitnessIntegrityError("provider qualification source provenance mismatch")
        actual_subjects = implementation_subject_sha256s()
        for field, actual_digest in actual_subjects.items():
            if getattr(self, field) != actual_digest:
                raise WitnessIntegrityError(
                    f"provider qualification {field} mismatch"
                )
        if self.monotonicity_qualification != "PASS":
            raise WitnessIntegrityError(
                "provider witness is not independently monotonicity-qualified"
            )


class SupabaseRestRpcTransport:
    """Bounded PostgREST RPC transport.

    Credentials are supplied at runtime. Source presence grants no credential,
    provider-write authority, or automatic retry after an ambiguous mutation.
    """

    def __init__(
        self,
        project_url: str,
        *,
        apikey: str,
        bearer_token: str,
        timeout_seconds: float = 15.0,
    ) -> None:
        parsed = parse.urlparse(project_url)
        if parsed.scheme != "https" or parsed.hostname != PROVIDER_HOST:
            raise ValueError(
                "Supabase project URL does not match exact Vera Control Plane provider"
            )
        if not apikey or not bearer_token:
            raise ValueError(
                "bounded provider transport requires apikey and bearer token"
            )
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._base_url = f"https://{PROVIDER_HOST}"
        self._apikey = apikey
        self._bearer_token = bearer_token
        self._timeout_seconds = timeout_seconds

    def call(self, function_name: str, params: dict[str, Any]) -> Any:
        if function_name not in {READ_RPC, RECEIPT_RPC, ADVANCE_RPC}:
            raise ProviderTransportError("unapproved provider RPC")
        body = json.dumps(
            params, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        req = request.Request(
            f"{self._base_url}/rest/v1/rpc/{function_name}",
            data=body,
            method="POST",
            headers={
                "apikey": self._apikey,
                "Authorization": f"Bearer {self._bearer_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        try:
            with request.urlopen(req, timeout=self._timeout_seconds) as response:
                payload = response.read()
        except (error.HTTPError, error.URLError, TimeoutError, OSError) as exc:
            raise ProviderTransportError("bounded provider RPC failed") from exc
        try:
            return json.loads(payload.decode("utf-8"))
        except Exception as exc:
            raise ProviderTransportError(
                "bounded provider RPC returned invalid JSON"
            ) from exc


def _one_row(value: Any, *, allow_empty: bool = False) -> dict[str, Any] | None:
    if value is None and allow_empty:
        return None
    if isinstance(value, list):
        if not value and allow_empty:
            return None
        if len(value) != 1 or not isinstance(value[0], dict):
            raise WitnessIntegrityError(
                "provider RPC must return exactly one object row"
            )
        return value[0]
    if isinstance(value, dict):
        return value
    raise WitnessIntegrityError("provider RPC returned unexpected shape")


def _frontier_from_provider(row: dict[str, Any]) -> dict[str, Any]:
    required = {
        "witness_id",
        "frontier_schema",
        "witness_store_id",
        "plan_sha256",
        "ledger_schema",
        "generation",
        "record_count",
        "chain_head",
        "last_slot_id",
        "last_record_digest",
        "predecessor_frontier_digest",
        "frontier_digest",
        "created_at",
    }
    if set(row) != required:
        raise WitnessIntegrityError(
            "provider frontier row fields do not match exact RPC contract"
        )
    if row["witness_id"] != "VERA_SD1_CAUSAL_V1":
        raise WitnessIntegrityError("provider witness id mismatch")
    frontier = {
        "schema": row["frontier_schema"],
        "witness_store_id": row["witness_store_id"],
        "plan_sha256": row["plan_sha256"],
        "ledger_schema": row["ledger_schema"],
        "generation": row["generation"],
        "record_count": row["record_count"],
        "chain_head": row["chain_head"],
        "last_slot_id": row["last_slot_id"],
        "last_record_digest": row["last_record_digest"],
        "predecessor_frontier_digest": row["predecessor_frontier_digest"],
        "frontier_digest": row["frontier_digest"],
    }
    validate_frontier(frontier, expected_store_id=DEFAULT_STORE_ID)
    return frontier


def _request_id(successor: dict[str, Any]) -> str:
    return (
        f"sd1.causal.frontier.{successor['generation']}."
        f"{successor['frontier_digest']}"
    )


def _request_digest(
    *,
    current: dict[str, Any],
    successor: dict[str, Any],
    request_id: str,
) -> str:
    payload = {
        "chain_head": successor["chain_head"],
        "expected_frontier_digest": current["frontier_digest"],
        "expected_generation": current["generation"],
        "frontier_digest": successor["frontier_digest"],
        "generation": successor["generation"],
        "last_record_digest": successor["last_record_digest"],
        "last_slot_id": successor["last_slot_id"],
        "operation_id": "sd1.causal.frontier.advance.v1",
        "predecessor_frontier_digest": successor["predecessor_frontier_digest"],
        "record_count": successor["record_count"],
        "request_id": request_id,
    }
    encoded = json.dumps(
        payload, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class SupabaseFrontierClient:
    """Provider RPC mechanics without a production qualification claim."""

    store_id = DEFAULT_STORE_ID

    def __init__(self, transport: Any) -> None:
        if not callable(getattr(transport, "call", None)):
            raise WitnessIntegrityError(
                "provider transport must expose bounded call()"
            )
        self._transport = transport

    def _call(self, function_name: str, params: dict[str, Any]) -> Any:
        return self._transport.call(function_name, params)

    def read_frontier(self) -> dict[str, Any]:
        row = _one_row(self._call(READ_RPC, {}))
        assert row is not None
        return _frontier_from_provider(row)

    def _read_receipt(self, request_id: str) -> dict[str, Any] | None:
        row = _one_row(
            self._call(RECEIPT_RPC, {"p_request_id": request_id}),
            allow_empty=True,
        )
        if row is None:
            return None
        expected = {
            "receipt_id",
            "request_id",
            "request_digest",
            "result_status",
            "expected_generation",
            "expected_frontier_digest",
            "observed_generation",
            "observed_frontier_digest",
            "successor_generation",
            "successor_frontier_digest",
            "created_at",
        }
        if set(row) != expected or row["request_id"] != request_id:
            raise WitnessIntegrityError(
                "provider receipt row fields do not match exact RPC contract"
            )
        return row

    def _reconcile_after_ambiguous(
        self,
        *,
        request_id: str,
        request_digest: str,
        successor: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            receipt = self._read_receipt(request_id)
        except Exception as exc:
            raise WitnessOutcomeUnknown(
                "provider mutation outcome unknown and receipt reconciliation failed"
            ) from exc
        if receipt is None:
            raise WitnessOutcomeUnknown(
                "provider mutation outcome unknown and no receipt exists"
            )
        if receipt["request_digest"] != request_digest:
            raise WitnessIntegrityError(
                "provider receipt request digest mismatch"
            )
        if receipt["result_status"] == "REJECTED_STALE":
            raise WitnessConflict(
                "provider witness rejected stale expected frontier"
            )
        if receipt["result_status"] != "APPLIED_VERIFIED":
            raise WitnessIntegrityError(
                "provider receipt contains unsupported result status"
            )
        if (
            receipt["successor_generation"] != successor["generation"]
            or receipt["successor_frontier_digest"]
            != successor["frontier_digest"]
        ):
            raise WitnessIntegrityError(
                "provider receipt successor does not match proposed frontier"
            )
        confirmed = self.read_frontier()
        if confirmed != successor:
            raise WitnessOutcomeUnknown(
                "provider receipt says applied but frontier readback "
                "does not match successor"
            )
        return confirmed

    def advance_frontier(
        self,
        *,
        expected_frontier_digest: str,
        successor: dict[str, Any],
    ) -> dict[str, Any]:
        current = self.read_frontier()
        if current["frontier_digest"] != expected_frontier_digest:
            raise WitnessConflict(
                "provider witness frontier changed before CAS"
            )
        validate_frontier(successor, expected_store_id=self.store_id)
        if successor["generation"] != current["generation"] + 1:
            raise WitnessIntegrityError(
                "provider successor generation must advance exactly once"
            )
        if successor["record_count"] != current["record_count"] + 1:
            raise WitnessIntegrityError(
                "provider successor record count must advance exactly once"
            )
        if (
            successor["predecessor_frontier_digest"]
            != current["frontier_digest"]
        ):
            raise WitnessIntegrityError(
                "provider successor predecessor frontier mismatch"
            )

        request_id = _request_id(successor)
        request_digest = _request_digest(
            current=current,
            successor=successor,
            request_id=request_id,
        )
        params = {
            "p_request_id": request_id,
            "p_request_digest": request_digest,
            "p_expected_generation": current["generation"],
            "p_expected_frontier_digest": current["frontier_digest"],
            "p_generation": successor["generation"],
            "p_record_count": successor["record_count"],
            "p_chain_head": successor["chain_head"],
            "p_last_slot_id": successor["last_slot_id"],
            "p_last_record_digest": successor["last_record_digest"],
            "p_predecessor_frontier_digest":
                successor["predecessor_frontier_digest"],
            "p_frontier_digest": successor["frontier_digest"],
        }
        try:
            result = _one_row(self._call(ADVANCE_RPC, params))
        except ProviderTransportError:
            return self._reconcile_after_ambiguous(
                request_id=request_id,
                request_digest=request_digest,
                successor=successor,
            )
        assert result is not None

        expected_result_fields = {
            "result_status",
            "stored_result_status",
            "receipt_id",
            "observed_generation",
            "observed_frontier_digest",
            "successor_generation",
            "successor_frontier_digest",
        }
        if set(result) != expected_result_fields:
            raise WitnessIntegrityError(
                "provider advance result fields do not match exact RPC contract"
            )

        result_status = result["result_status"]
        stored_status = result["stored_result_status"]
        if result_status == "REQUEST_ID_COLLISION":
            raise WitnessIntegrityError("provider request-id collision")
        if (
            result_status == "REJECTED_STALE"
            or stored_status == "REJECTED_STALE"
        ):
            raise WitnessConflict(
                "provider witness rejected stale expected frontier"
            )
        if result_status not in {
            "APPLIED_VERIFIED",
            "IDEMPOTENT_REPLAY",
        }:
            raise WitnessIntegrityError(
                "provider returned unsupported advance status"
            )
        if stored_status != "APPLIED_VERIFIED":
            raise WitnessIntegrityError(
                "provider replay did not resolve to an applied successor"
            )
        if (
            result["successor_generation"] != successor["generation"]
            or result["successor_frontier_digest"]
            != successor["frontier_digest"]
        ):
            raise WitnessIntegrityError(
                "provider advance result successor mismatch"
            )

        confirmed = self.read_frontier()
        if confirmed != successor:
            raise WitnessOutcomeUnknown(
                "provider post-advance frontier readback mismatch"
            )
        return confirmed


class SupabaseFrontierWitness(SupabaseFrontierClient):
    """Controller-eligible provider witness, intentionally uninstantiable today.

    A later independently reviewed qualification must be persisted and its exact
    SHA-256 pinned in QUALIFICATION_ARTIFACT_SHA256 before construction is
    permitted. This prevents source presence or a caller-supplied PASS string
    from self-promoting the provider client into a production witness.
    """

    def __init__(
        self,
        transport: Any,
        *,
        qualification_artifact: str | bytes,
    ) -> None:
        if QUALIFICATION_ARTIFACT_SHA256 is None:
            raise WitnessIntegrityError(
                "production provider witness qualification artifact is not pinned"
            )
        if isinstance(qualification_artifact, str):
            raw = qualification_artifact.encode("utf-8")
        elif isinstance(qualification_artifact, bytes):
            raw = qualification_artifact
        else:
            raise WitnessIntegrityError(
                "production provider witness qualification artifact must be bytes or text"
            )
        if hashlib.sha256(raw).hexdigest() != QUALIFICATION_ARTIFACT_SHA256:
            raise WitnessIntegrityError(
                "production provider witness qualification artifact digest mismatch"
            )
        try:
            qualification = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise WitnessIntegrityError(
                "production provider witness qualification artifact is invalid JSON"
            ) from exc
        self._qualification = ProviderQualification.from_mapping(
            qualification
        )
        super().__init__(transport)
        self.monotonicity_qualified = True


__all__ = [
    "ADVANCE_RPC",
    "DEPLOYED_STATEMENT_BYTES",
    "DEPLOYED_STATEMENT_SHA256",
    "PROVIDER_PROJECT_ID",
    "ProviderQualification",
    "ProviderTransportError",
    "QUALIFICATION_ARTIFACT_SHA256",
    "QUALIFICATION_SCHEMA",
    "RECEIPT_RPC",
    "READ_RPC",
    "SOURCE_GIT_BLOB",
    "SOURCE_HEAD",
    "SupabaseFrontierClient",
    "SupabaseFrontierWitness",
    "SupabaseRestRpcTransport",
    "WitnessOutcomeUnknown",
    "implementation_subject_sha256s",
]

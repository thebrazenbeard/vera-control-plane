from __future__ import annotations

import hashlib


PRINCIPAL_PREFIX = "controller:"
PRINCIPAL_DERIVATION_CONTRACT = "VERAPORT_CONTROLLER_PRINCIPAL_DERIVATION_V1"


class ControllerIdentityError(ValueError):
    """Raised when controller identity material is malformed."""


class KeyIdDerivationUnresolved(RuntimeError):
    """Raised while the owning VeraPort protocol has no exact key-ID derivation."""


def controller_principal_from_spki_der(spki_der: bytes) -> str:
    """Derive the exact VeraPort controller principal from DER SPKI bytes."""
    if type(spki_der) is not bytes or not spki_der:
        raise ControllerIdentityError("spki_der must be non-empty exact bytes")
    digest = hashlib.sha256(spki_der).hexdigest()
    return PRINCIPAL_PREFIX + digest


def recovery_controller_principal(spki_der: bytes) -> str:
    """Recovery consumes the same exact principal primitive as rotation."""
    return controller_principal_from_spki_der(spki_der)


def rotation_controller_principal(spki_der: bytes) -> str:
    """Rotation consumes the same exact principal primitive as recovery."""
    return controller_principal_from_spki_der(spki_der)


def controller_key_id_from_spki_der(spki_der: bytes) -> str:
    """Fail closed until the owning VeraPort protocol freezes key-ID semantics."""
    if type(spki_der) is not bytes or not spki_der:
        raise ControllerIdentityError("spki_der must be non-empty exact bytes")
    raise KeyIdDerivationUnresolved(
        "VeraMesh issue #15 requires a key ID derived from public SPKI but does "
        "not define its exact algorithm/encoding; rotation must stop before any "
        "credential or trust effect."
    )

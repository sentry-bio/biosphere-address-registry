"""Biosphere Address Registry v1 reference implementation."""

from .form import Anchor, Form, FreezeGate, address_record, register_point
from .identity import (
    IdentityError,
    canonical_json,
    content_id,
    sequence_id,
    verify_content_id,
    with_content_id,
)
from .records import (
    Neighbor,
    RankReadout,
    evidence,
    interpretation,
    observation,
    organism_record,
    record,
)
from .registry import Registry, RegistryError
from .validation import ValidationError, require_valid, validate

__all__ = [
    "Anchor",
    "Form",
    "FreezeGate",
    "IdentityError",
    "Neighbor",
    "RankReadout",
    "Registry",
    "RegistryError",
    "ValidationError",
    "address_record",
    "canonical_json",
    "content_id",
    "evidence",
    "interpretation",
    "observation",
    "organism_record",
    "record",
    "register_point",
    "require_valid",
    "sequence_id",
    "validate",
    "verify_content_id",
    "with_content_id",
]

__version__ = "0.1.0"

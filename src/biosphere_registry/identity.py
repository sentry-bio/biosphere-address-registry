"""Canonical JSON and content identity for BAR objects."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from typing import Any, Mapping

CONTENT_PREFIX = "sha256:"
IDENTITY_EXCLUDED_FIELDS = frozenset({"content_id", "signatures"})


class IdentityError(ValueError):
    """The supplied object cannot have a valid BAR content identity."""


def _finite_numbers(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise IdentityError(f"non-finite number at {path}")
    if isinstance(value, Mapping):
        for key, item in value.items():
            _finite_numbers(item, f"{path}.{key}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _finite_numbers(item, f"{path}[{i}]")


def identity_view(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return the record fields covered by its content identity.

    Detached signatures and the self-referential content_id are excluded only
    at the top level. Unknown payload fields remain covered.
    """

    view = copy.deepcopy(dict(record))
    for key in IDENTITY_EXCLUDED_FIELDS:
        view.pop(key, None)
    return view


def canonical_json(record: Mapping[str, Any]) -> bytes:
    view = identity_view(record)
    _finite_numbers(view)
    try:
        encoded = json.dumps(
            view,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise IdentityError(str(exc)) from exc
    return encoded.encode("utf-8")


def content_id(record: Mapping[str, Any]) -> str:
    return CONTENT_PREFIX + hashlib.sha256(canonical_json(record)).hexdigest()


def with_content_id(record: Mapping[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(dict(record))
    computed = content_id(out)
    supplied = out.get("content_id")
    if supplied is not None and supplied != computed:
        raise IdentityError(
            f"content_id mismatch: supplied {supplied}, computed {computed}"
        )
    out["content_id"] = computed
    return out


def verify_content_id(record: Mapping[str, Any]) -> bool:
    supplied = record.get("content_id")
    return isinstance(supplied, str) and supplied == content_id(record)


def sequence_id(
    sequence: str,
    *,
    alphabet: str = "DNA",
    normalization_policy: str = "uppercase-strip-whitespace-v1",
) -> tuple[str, str]:
    """Normalize a sequence and return `(sha256:..., normalized)`.

    V1 DNA/RNA removes ASCII whitespace and uppercases. RNA additionally maps
    U to T so the resulting alphabet has explicit DNA semantics. Protein is
    uppercased without alphabet reduction.
    """

    normalized = "".join(sequence.split()).upper()
    if normalization_policy != "uppercase-strip-whitespace-v1":
        raise IdentityError(f"unsupported normalization policy: {normalization_policy}")
    if alphabet.upper() == "RNA":
        normalized = normalized.replace("U", "T")
    digest = hashlib.sha256(normalized.encode("ascii")).hexdigest()
    return CONTENT_PREFIX + digest, normalized

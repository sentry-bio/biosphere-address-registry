"""Semantic validation independent of the optional JSON Schema package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .identity import IdentityError, content_id

SPEC_VERSION = "bar-1.0"
KNOWN_TYPES = {
    "observation",
    "reference-manifest",
    "map-edition",
    "evidence",
    "form",
    "transform",
    "address",
    "interpretation",
    "organism-record",
    "verification-report",
    "conformance-report",
    "projection",
}

REQUIRED_PAYLOAD_FIELDS = {
    "observation": {
        "sequence_sha256",
        "length_bp",
        "alphabet",
        "normalization_policy",
        "window_policy",
    },
    "reference-manifest": {"manifest_id", "source_release", "entries"},
    "map-edition": {
        "map_id",
        "encoder_id",
        "tokenizer_id",
        "reference_manifest_id",
        "metric_id",
        "embedding_dim",
        "index_tiers",
        "verification",
    },
    "evidence": {
        "observation_id",
        "map_edition_id",
        "metric_id",
        "k",
        "neighborhood",
        "support",
        "input_quality",
        "rank_readouts",
        "scorer_version",
    },
    "form": {
        "form_version",
        "kappa",
        "kappa_status",
        "dim",
        "dim_status",
        "epsilon",
        "prime_meridian",
        "chirality_anchor",
        "radial_proxy",
        "freeze_gate",
    },
    "transform": {
        "map_edition_id",
        "form_id",
        "input_dim",
        "backbone_basis",
        "tangent_mean",
        "prime_meridian",
        "chirality_anchor",
        "inheritance",
        "certified",
        "fit_panel_id",
        "residual_report",
    },
    "address": {
        "evidence_id",
        "map_edition_id",
        "form_id",
        "transform_id",
        "theta",
        "theta_status",
        "r",
        "r_status",
        "radial_proxy",
        "tags",
    },
    "interpretation": {
        "evidence_id",
        "ontology",
        "ontology_release",
        "operating_point",
        "rank_calls",
    },
    "organism-record": {
        "level",
        "observations",
        "evidence",
        "addresses",
        "interpretations",
    },
}


class ValidationError(ValueError):
    pass


def load_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValidationError("BAR record must be a JSON object")
    return value


def validate(record: Mapping[str, Any], *, require_id: bool = False) -> list[str]:
    errors: list[str] = []
    record_type = record.get("record_type")
    if record_type not in KNOWN_TYPES:
        errors.append(f"unknown record_type: {record_type!r}")
    if record.get("spec_version") != SPEC_VERSION:
        errors.append(f"spec_version must be {SPEC_VERSION!r}")
    payload = record.get("payload")
    if not isinstance(payload, Mapping):
        errors.append("payload must be an object")
        return errors

    required = REQUIRED_PAYLOAD_FIELDS.get(str(record_type), set())
    missing = sorted(required - set(payload))
    if missing:
        errors.append("missing payload fields: " + ", ".join(missing))

    supplied = record.get("content_id")
    if require_id and supplied is None:
        errors.append("content_id is required")
    if supplied is not None:
        try:
            computed = content_id(record)
            if supplied != computed:
                errors.append(
                    f"content_id mismatch: supplied {supplied}, computed {computed}"
                )
        except IdentityError as exc:
            errors.append(str(exc))

    if record_type == "map-edition":
        encoder = payload.get("encoder_id")
        for i, tier in enumerate(payload.get("index_tiers", [])):
            if isinstance(tier, Mapping) and tier.get("encoder_id") != encoder:
                errors.append(f"index_tiers[{i}].encoder_id does not match map encoder")
        if payload.get("metric_id") == "poincare-geodesic-v1":
            for tier in payload.get("index_tiers", []):
                if isinstance(tier, Mapping) and tier.get("index_type") == "FlatIP":
                    errors.append(
                        "FlatIP on normalized vectors is angular-cosine-v1, "
                        "not poincare-geodesic-v1"
                    )

    if record_type == "address":
        if payload.get("r_status") != "ADVISORY":
            errors.append("address r_status must be ADVISORY")
        tags = payload.get("tags", {})
        if isinstance(tags, Mapping) and tags.get("kappa") != "CONVENTION":
            errors.append("address kappa tag must be CONVENTION")

    if record_type == "form":
        if payload.get("kappa_status") != "CONVENTION":
            errors.append("Form kappa_status must be CONVENTION")
        if payload.get("dim") != 2 or payload.get("dim_status") != "CONVENTION":
            errors.append("BAR v1 Form inhabits dim=2 as CONVENTION")
        if payload.get("origin_semantics") not in (None, "chart_origin_not_LUCA"):
            errors.append("Form origin must not be identified as LUCA")

    if record_type == "transform":
        dim = payload.get("input_dim")
        basis = payload.get("backbone_basis", [])
        mean = payload.get("tangent_mean", [])
        if isinstance(dim, int):
            if len(basis) != 2 or any(
                not isinstance(axis, list) or len(axis) != dim for axis in basis
            ):
                errors.append("transform backbone_basis must have shape (2, input_dim)")
            if not isinstance(mean, list) or len(mean) != dim:
                errors.append("transform tangent_mean must have input_dim entries")
        if payload.get("inheritance") == "warm_start" and payload.get("certified"):
            errors.append("warm_start transform cannot independently be certified")
        if payload.get("certified"):
            for name in ("prime_meridian", "chirality_anchor"):
                anchor = payload.get(name)
                digest = anchor.get("sequence_sha256") if isinstance(anchor, Mapping) else None
                if not (
                    isinstance(digest, str)
                    and digest.startswith("sha256:")
                    and len(digest) == 71
                ):
                    errors.append(
                        f"certified transform requires exact {name}.sequence_sha256"
                    )

    return errors


def require_valid(record: Mapping[str, Any], *, require_id: bool = False) -> None:
    errors = validate(record, require_id=require_id)
    if errors:
        raise ValidationError("; ".join(errors))


def validate_with_schema(record: Mapping[str, Any], schema_dir: Path) -> list[str]:
    """Optionally run the matching JSON Schema when `jsonschema` is installed."""

    try:
        import jsonschema  # type: ignore
    except ImportError:
        return []
    schema_path = schema_dir / f"{record.get('record_type')}.v1.json"
    if not schema_path.exists():
        return []
    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    return [error.message for error in validator.iter_errors(record)]

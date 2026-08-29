"""Small typed constructors for BAR v1 records.

The constructors deliberately do not know PyTorch, FAISS, GTDB, or an encoder.
They express evidence and provenance produced by those systems.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence

from .identity import sequence_id, with_content_id

SPEC_VERSION = "bar-1.0"


def record(record_type: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return with_content_id(
        {
            "record_type": record_type,
            "spec_version": SPEC_VERSION,
            "payload": dict(payload),
        }
    )


@dataclass(frozen=True)
class Neighbor:
    gid: int
    accession: str
    distance: float
    reference_content_id: str | None = None
    similarity: float | None = None
    lineage: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        return {key: value for key, value in out.items() if value is not None}


@dataclass(frozen=True)
class RankReadout:
    rank: str
    top: str | None
    confidence: float
    margin: float
    support: float
    runners_up: Sequence[tuple[str, float]] = ()
    gap: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "top": self.top,
            "confidence": float(self.confidence),
            "margin": float(self.margin),
            "support": float(self.support),
            "runners_up": [[name, float(score)] for name, score in self.runners_up],
            "gap": self.gap,
        }


def observation(
    sequence: str,
    *,
    alphabet: str = "DNA",
    normalization_policy: str = "uppercase-strip-whitespace-v1",
    window_policy: str = "whole-input-v1",
    accession: str | None = None,
    assembly_accession: str | None = None,
    source: Mapping[str, Any] | None = None,
    quality: Mapping[str, Any] | None = None,
    include_sequence: bool = False,
) -> dict[str, Any]:
    digest, normalized = sequence_id(
        sequence,
        alphabet=alphabet,
        normalization_policy=normalization_policy,
    )
    payload: dict[str, Any] = {
        "sequence_sha256": digest,
        "length_bp": len(normalized),
        "alphabet": alphabet.upper(),
        "normalization_policy": normalization_policy,
        "window_policy": window_policy,
        "accession": accession,
        "assembly_accession": assembly_accession,
        "source": dict(source or {}),
        "quality": dict(quality or {}),
    }
    if include_sequence:
        payload["sequence"] = normalized
    return record("observation", payload)


def evidence(
    *,
    observation_id: str,
    map_edition_id: str,
    metric_id: str,
    neighbors: Sequence[Neighbor],
    k: int | None = None,
    support: float,
    input_quality: str,
    rank_readouts: Sequence[RankReadout] = (),
    scorer_version: str = "scorer-v1",
    typicality: float | None = None,
    distance_to_manifold: float | None = None,
    scale: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    requested_k = int(k if k is not None else max(1, len(neighbors)))
    if requested_k < 1 or len(neighbors) > requested_k:
        raise ValueError("k must be positive and at least the returned neighborhood size")
    return record(
        "evidence",
        {
            "observation_id": observation_id,
            "map_edition_id": map_edition_id,
            "metric_id": metric_id,
            "k": requested_k,
            "neighborhood": [item.to_dict() for item in neighbors],
            "support": float(support),
            "input_quality": input_quality,
            "typicality": typicality,
            "distance_to_manifold": distance_to_manifold,
            "rank_readouts": [item.to_dict() for item in rank_readouts],
            "scorer_version": scorer_version,
            "scale": dict(scale or {}),
        },
    )


def interpretation(
    *,
    evidence_id: str,
    ontology: str,
    ontology_release: str,
    operating_point: Mapping[str, Any],
    rank_calls: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return record(
        "interpretation",
        {
            "evidence_id": evidence_id,
            "ontology": ontology,
            "ontology_release": ontology_release,
            "operating_point": dict(operating_point),
            "rank_calls": [dict(call) for call in rank_calls],
        },
    )


def organism_record(
    *,
    level: str,
    observations: Sequence[str],
    evidence_ids: Sequence[str],
    address_ids: Sequence[str] = (),
    interpretation_ids: Sequence[str] = (),
    assembly_accession: str | None = None,
    taxonomy_membership: Mapping[str, Any] | None = None,
    distribution_summary: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return record(
        "organism-record",
        {
            "level": level,
            "observations": list(observations),
            "evidence": list(evidence_ids),
            "addresses": list(address_ids),
            "interpretations": list(interpretation_ids),
            "assembly_accession": assembly_accession,
            "taxonomy_membership": (
                dict(taxonomy_membership) if taxonomy_membership else None
            ),
            "distribution_summary": dict(distribution_summary or {}),
        },
    )

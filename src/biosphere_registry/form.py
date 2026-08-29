"""TriangleCCS-compatible Form and map registration for BAR.

This is a compact interoperability implementation, not a second proof spine.
TriangleCCS remains authoritative for conformance instruments.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence

from .records import record


@dataclass(frozen=True)
class Anchor:
    accession: str
    sequence_sha256: str | None
    role: str


@dataclass(frozen=True)
class FreezeGate:
    angular_median_deg_max: float = 10.0
    determinate_quartet_agreement_min: float = 0.90


@dataclass(frozen=True)
class Form:
    form_version: str = "triangleccs-1.0"
    kappa: float = 1.25
    dim: int = 2
    epsilon: float = 1e-3
    radial_proxy: str = "ssu+cog+kmer_entropy"
    prime_meridian: Anchor = field(
        default_factory=lambda: Anchor(
            accession="GCF_000005845.2",
            sequence_sha256=None,
            role="prime_meridian",
        )
    )
    chirality_anchor: Anchor = field(
        default_factory=lambda: Anchor(
            accession="GCF_000091665.1",
            sequence_sha256=None,
            role="chirality",
        )
    )
    freeze_gate: FreezeGate = field(default_factory=FreezeGate)

    def __post_init__(self) -> None:
        if self.kappa <= 0:
            raise ValueError("kappa must be positive")
        if self.dim != 2:
            raise ValueError("BAR v1 Form inhabits H^2")
        if self.epsilon <= 0:
            raise ValueError("epsilon must be positive")

    def to_record(self) -> dict[str, Any]:
        return record(
            "form",
            {
                "form_version": self.form_version,
                "kappa": self.kappa,
                "kappa_status": "CONVENTION",
                "dim": self.dim,
                "dim_status": "CONVENTION",
                "epsilon": self.epsilon,
                "prime_meridian": asdict(self.prime_meridian),
                "chirality_anchor": asdict(self.chirality_anchor),
                "radial_proxy": self.radial_proxy,
                "origin_semantics": "chart_origin_not_LUCA",
                "certified_axis": "theta",
                "advisory_axis": "radius",
                "freeze_gate": asdict(self.freeze_gate),
            },
        )


def _norm(vector: Sequence[float]) -> float:
    return math.sqrt(sum(float(x) * float(x) for x in vector))


def _logmap0(point: Sequence[float], kappa: float) -> list[float]:
    radius = 1.0 / math.sqrt(kappa)
    norm = min(max(_norm(point), 1e-12), radius * (1.0 - 1e-6))
    scale = (2.0 / math.sqrt(kappa)) * math.atanh(math.sqrt(kappa) * norm) / norm
    return [scale * float(x) for x in point]


def _project(
    point: Sequence[float],
    mean: Sequence[float],
    basis: Sequence[Sequence[float]],
    *,
    kappa: float,
    coordinate_kind: str,
) -> tuple[float, float]:
    vector = (
        [float(x) for x in point]
        if coordinate_kind == "tangent"
        else _logmap0(point, kappa)
    )
    centered = [x - float(mu) for x, mu in zip(vector, mean)]
    projected = [
        sum(float(weight) * value for weight, value in zip(axis, centered))
        for axis in basis
    ]
    if len(projected) != 2:
        raise ValueError("backbone basis must have two axes")
    return projected[0], projected[1]


def _wrap_pi(theta: float) -> float:
    return (theta + math.pi) % (2.0 * math.pi) - math.pi


def register_point(
    point: Sequence[float],
    *,
    transform: Mapping[str, Any],
    form: Form,
    meridian_point: Sequence[float],
    chirality_point: Sequence[float],
) -> tuple[float, float]:
    """Return `(candidate theta, advisory projected radius)`.

    The transform payload must have `backbone_basis`, `tangent_mean`, and
    optional `input_coordinate_kind`. Certification is metadata established by
    a separate conformance report.
    """

    payload = transform.get("payload", transform)
    basis = payload["backbone_basis"]
    mean = payload["tangent_mean"]
    kind = payload.get("input_coordinate_kind", "poincare-ball")
    expected = int(payload.get("input_dim", len(mean)))
    if len(point) != expected or len(mean) != expected:
        raise ValueError("point/mean dimension does not match transform")
    if len(basis) != 2 or any(len(axis) != expected for axis in basis):
        raise ValueError("backbone basis must have shape (2, input_dim)")

    x, y = _project(point, mean, basis, kappa=form.kappa, coordinate_kind=kind)
    mx, my = _project(
        meridian_point, mean, basis, kappa=form.kappa, coordinate_kind=kind
    )
    cx, cy = _project(
        chirality_point, mean, basis, kappa=form.kappa, coordinate_kind=kind
    )
    theta0 = math.atan2(my, mx)
    theta = _wrap_pi(math.atan2(y, x) - theta0)
    chirality = _wrap_pi(math.atan2(cy, cx) - theta0)
    if chirality < 0:
        theta = -theta
    return theta, math.hypot(x, y)


def address_record(
    *,
    evidence_id: str,
    map_edition_id: str,
    form_record: Mapping[str, Any],
    transform_record: Mapping[str, Any],
    theta: float,
    r: float,
    residual: float | None,
) -> dict[str, Any]:
    certified = bool(transform_record.get("payload", transform_record).get("certified"))
    return record(
        "address",
        {
            "evidence_id": evidence_id,
            "map_edition_id": map_edition_id,
            "form_id": form_record["content_id"],
            "transform_id": transform_record["content_id"],
            "theta": float(theta),
            "theta_status": "certified" if certified else "candidate",
            "r": float(r),
            "r_status": "ADVISORY",
            "radial_proxy": form_record["payload"]["radial_proxy"],
            "residual": residual,
            "tags": {
                "theta": "EMPIRICAL" if certified else "CANDIDATE",
                "r": "ADVISORY",
                "kappa": "CONVENTION",
                "dim": "CONVENTION",
                "residual": "INSTRUMENT",
            },
        },
    )

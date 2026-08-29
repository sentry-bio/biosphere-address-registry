#!/usr/bin/env python3
"""Regenerate the linked BAR v1 synthetic example graph."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from biosphere_registry import (  # noqa: E402
    Anchor,
    Form,
    Neighbor,
    RankReadout,
    address_record,
    evidence,
    interpretation,
    observation,
    organism_record,
    record,
    register_point,
)


def write(name: str, value: dict) -> None:
    (ROOT / "examples" / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    form = Form(
        prime_meridian=Anchor(
            "GCF_SYNTHETIC_ECOLI.1", "sha256:" + "11" * 32, "prime_meridian"
        ),
        chirality_anchor=Anchor(
            "GCF_SYNTHETIC_ARCHAEA.1", "sha256:" + "22" * 32, "chirality"
        ),
    ).to_record()

    references = record(
        "reference-manifest",
        {
            "manifest_id": "synthetic-reference-v1",
            "source_release": "synthetic",
            "entries": [
                {
                    "gid": 0,
                    "accession": "GCF_SYNTHETIC_ECOLI.1",
                    "assembly_sha256": "sha256:" + "11" * 32,
                },
                {
                    "gid": 1,
                    "accession": "GCF_SYNTHETIC_ARCHAEA.1",
                    "assembly_sha256": "sha256:" + "22" * 32,
                },
            ],
        },
    )

    encoder_id = "sha256:" + "33" * 32
    map_edition = record(
        "map-edition",
        {
            "map_id": "atlas-synthetic-v1",
            "encoder_id": encoder_id,
            "tokenizer_id": "synthetic-tokenizer-v1",
            "reference_manifest_id": references["content_id"],
            "metric_id": "angular-cosine-v1",
            "embedding_dim": 3,
            "index_tiers": [
                {
                    "name": "1kb",
                    "window_bp": 1000,
                    "token_count": 200,
                    "index_id": "sha256:" + "44" * 32,
                    "encoder_id": encoder_id,
                    "vector_count": 2,
                    "genome_count": 2,
                    "index_type": "FlatIP",
                }
            ],
            "calibration_ids": [],
            "routing_policy": {"default": "1kb"},
            "verification": {"self_retrieval": 1.0, "status": "synthetic-pass"},
            "status": "CANDIDATE",
        },
    )

    obs = observation(
        "ACGT" * 300,
        accession="SYNTHETIC_QUERY",
        window_policy="1kb-prefix-v1",
        source={"kind": "synthetic-example"},
    )

    ev = evidence(
        observation_id=obs["content_id"],
        map_edition_id=map_edition["content_id"],
        metric_id="angular-cosine-v1",
        neighbors=[
            Neighbor(
                gid=0,
                accession="GCF_SYNTHETIC_ECOLI.1",
                reference_content_id="sha256:" + "11" * 32,
                distance=0.05,
                similarity=0.9987502604,
                lineage={"domain": "Bacteria", "genus": "Escherichia"},
            )
        ],
        support=0.91,
        typicality=0.84,
        distance_to_manifold=0.12,
        input_quality="usable",
        rank_readouts=[
            RankReadout("domain", "Bacteria", 0.99, 0.98, 0.91),
            RankReadout("genus", "Escherichia", 0.88, 0.77, 0.91),
            RankReadout("species", None, 0.42, 0.31, 0.91, gap=True),
        ],
        scale={"tier": "1kb", "window_bp": 1000},
    )

    transform = record(
        "transform",
        {
            "map_edition_id": map_edition["content_id"],
            "form_id": form["content_id"],
            "input_dim": 3,
            "input_coordinate_kind": "poincare-ball",
            "backbone_basis": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            "tangent_mean": [0.0, 0.0, 0.0],
            "prime_meridian": form["payload"]["prime_meridian"],
            "chirality_anchor": form["payload"]["chirality_anchor"],
            "inheritance": "independent",
            "certified": False,
            "fit_panel_id": "synthetic-panel-v1",
            "residual_report": {
                "status": "synthetic-fixture",
                "angular_median_deg": None,
                "determinate_quartet_agreement": None,
            },
        },
    )

    theta, radius = register_point(
        [0.2, 0.1, 0.03],
        transform=transform,
        form=Form(),
        meridian_point=[0.2, 0.0, 0.0],
        chirality_point=[0.0, 0.2, 0.0],
    )
    addr = address_record(
        evidence_id=ev["content_id"],
        map_edition_id=map_edition["content_id"],
        form_record=form,
        transform_record=transform,
        theta=theta,
        r=radius,
        residual=0.08,
    )

    interp = interpretation(
        evidence_id=ev["content_id"],
        ontology="GTDB",
        ontology_release="synthetic",
        operating_point={"min_confidence": 0.7, "require_nesting": False},
        rank_calls=[
            {"rank": "domain", "label": "Bacteria", "confidence": 0.99},
            {"rank": "genus", "label": "Escherichia", "confidence": 0.88},
            {"rank": "species", "label": None, "confidence": 0.42},
        ],
    )

    organism = organism_record(
        level="genome",
        observations=[obs["content_id"]],
        evidence_ids=[ev["content_id"]],
        address_ids=[addr["content_id"]],
        interpretation_ids=[interp["content_id"]],
        assembly_accession="SYNTHETIC_QUERY",
        distribution_summary={
            "representative_method": "single-window-fixture",
            "representative_id": obs["content_id"],
            "n_members": 1,
            "dispersion": 0.0,
        },
    )

    for name, value in {
        "form.example.json": form,
        "reference-manifest.example.json": references,
        "map-edition.example.json": map_edition,
        "observation.example.json": obs,
        "evidence.example.json": ev,
        "transform.example.json": transform,
        "address.example.json": addr,
        "interpretation.example.json": interp,
        "organism-record.example.json": organism,
    }.items():
        write(name, value)


if __name__ == "__main__":
    main()

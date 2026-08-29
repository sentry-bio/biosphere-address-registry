from __future__ import annotations

import math

from biosphere_registry import (
    Form,
    address_record,
    record,
    register_point,
    validate,
)


def synthetic_transform(form_record, *, certified=False, inheritance="independent"):
    return record(
        "transform",
        {
            "map_edition_id": "sha256:" + "1" * 64,
            "form_id": form_record["content_id"],
            "input_dim": 3,
            "input_coordinate_kind": "poincare-ball",
            "backbone_basis": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            "tangent_mean": [0.0, 0.0, 0.0],
            "prime_meridian": {"accession": "A"},
            "chirality_anchor": {"accession": "B"},
            "inheritance": inheritance,
            "certified": certified,
            "fit_panel_id": "synthetic",
            "residual_report": {},
        },
    )


def test_form_statuses_are_explicit():
    form = Form().to_record()
    assert form["payload"]["kappa_status"] == "CONVENTION"
    assert form["payload"]["dim_status"] == "CONVENTION"
    assert form["payload"]["origin_semantics"] == "chart_origin_not_LUCA"
    assert validate(form, require_id=True) == []


def test_two_anchor_registration_fixes_meridian_and_chirality():
    form_obj = Form()
    form = form_obj.to_record()
    transform = synthetic_transform(form)
    meridian = [0.2, 0.0, 0.0]
    chirality = [0.0, 0.2, 0.0]
    theta0, _ = register_point(
        meridian,
        transform=transform,
        form=form_obj,
        meridian_point=meridian,
        chirality_point=chirality,
    )
    theta_chirality, _ = register_point(
        chirality,
        transform=transform,
        form=form_obj,
        meridian_point=meridian,
        chirality_point=chirality,
    )
    assert abs(theta0) < 1e-12
    assert math.isclose(theta_chirality, math.pi / 2, rel_tol=1e-9)


def test_candidate_transform_emits_candidate_address_and_advisory_radius():
    form = Form().to_record()
    transform = synthetic_transform(form)
    address = address_record(
        evidence_id="sha256:" + "2" * 64,
        map_edition_id="sha256:" + "1" * 64,
        form_record=form,
        transform_record=transform,
        theta=0.2,
        r=1.3,
        residual=0.1,
    )
    assert address["payload"]["theta_status"] == "candidate"
    assert address["payload"]["r_status"] == "ADVISORY"
    assert address["payload"]["tags"]["kappa"] == "CONVENTION"
    assert validate(address, require_id=True) == []


def test_warm_start_cannot_be_certified():
    form = Form().to_record()
    transform = synthetic_transform(form, certified=True, inheritance="warm_start")
    errors = validate(transform, require_id=True)
    assert any("warm_start" in error for error in errors)


def test_flatip_cannot_claim_poincare_metric():
    encoder = "sha256:" + "3" * 64
    map_record = record(
        "map-edition",
        {
            "map_id": "bad-map",
            "encoder_id": encoder,
            "tokenizer_id": "tok",
            "reference_manifest_id": "sha256:" + "4" * 64,
            "metric_id": "poincare-geodesic-v1",
            "embedding_dim": 129,
            "index_tiers": [
                {
                    "name": "5kb",
                    "window_bp": 5000,
                    "index_id": "sha256:" + "5" * 64,
                    "encoder_id": encoder,
                    "index_type": "FlatIP",
                }
            ],
            "verification": {},
        },
    )
    assert any("angular-cosine" in error for error in validate(map_record))

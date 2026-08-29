from __future__ import annotations

import json

from biosphere_registry import Registry, observation


def test_put_get_ref_and_verify(tmp_path):
    registry = Registry(tmp_path / "bar")
    registry.initialize()
    obj = observation("ACGT" * 25)
    stored = registry.put(obj, ref="organisms/example")
    assert registry.get(stored["content_id"]) == stored
    assert registry.get("organisms/example") == stored
    report = registry.verify()
    assert report == {
        "ok": True,
        "objects": 1,
        "refs": 1,
        "graph_checked": False,
        "errors": [],
    }


def test_object_is_deduplicated_but_events_are_append_only(tmp_path):
    registry = Registry(tmp_path / "bar")
    registry.initialize()
    obj = observation("ACGT" * 10)
    registry.put(obj)
    registry.put(obj)
    assert len(list(registry.iter_objects())) == 1
    events = [
        json.loads(line)
        for line in registry.events.read_text(encoding="utf-8").splitlines()
    ]
    assert len(events) == 2
    assert events[0]["created"] is True
    assert events[1]["created"] is False


def test_taxonomy_view_does_not_change_evidence_identity(tmp_path):
    """Interpretations can change while their referenced evidence remains immutable."""
    from biosphere_registry import Neighbor, evidence, interpretation

    obs = observation("ACGT" * 100)
    ev = evidence(
        observation_id=obs["content_id"],
        map_edition_id="sha256:" + "1" * 64,
        metric_id="angular-cosine-v1",
        neighbors=[Neighbor(1, "GCF_EXAMPLE.1", 0.1)],
        support=0.8,
        input_quality="usable",
    )
    old = interpretation(
        evidence_id=ev["content_id"],
        ontology="GTDB",
        ontology_release="r220",
        operating_point={"min_confidence": 0.7},
        rank_calls=[{"rank": "species", "label": "Species A"}],
    )
    new = interpretation(
        evidence_id=ev["content_id"],
        ontology="GTDB",
        ontology_release="r221",
        operating_point={"min_confidence": 0.7},
        rank_calls=[{"rank": "species", "label": "Species B"}],
    )
    assert old["content_id"] != new["content_id"]
    assert old["payload"]["evidence_id"] == new["payload"]["evidence_id"]

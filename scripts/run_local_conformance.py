#!/usr/bin/env python3
"""Run the dependency-free BAR-Core/Frame conformance demonstration.

This intentionally does not call a genomic encoder. The saved real-system
protocol is docs/END_TO_END_CONFORMANCE.md.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from biosphere_registry import Registry  # noqa: E402
from biosphere_registry.validation import load_json, validate, validate_with_schema  # noqa: E402

OBJECTS = [
    "form.example.json",
    "reference-manifest.example.json",
    "map-edition.example.json",
    "observation.example.json",
    "evidence.example.json",
    "transform.example.json",
    "address.example.json",
    "interpretation.example.json",
    "organism-record.example.json",
]


def run(registry_path: Path) -> dict:
    registry = Registry(registry_path)
    registry.initialize()
    ingested = []
    for name in OBJECTS:
        source = ROOT / "examples" / name
        obj = load_json(source)
        errors = validate(obj, require_id=True)
        errors.extend(validate_with_schema(obj, ROOT / "schemas"))
        if errors:
            raise RuntimeError(f"{name}: {'; '.join(errors)}")
        ref = f"examples/{name.removesuffix('.example.json')}"
        stored = registry.put(obj, ref=ref)
        ingested.append(stored["content_id"])

    graph = registry.verify(graph=True)
    organism = registry.get("examples/organism-record")
    evidence = registry.get(organism["payload"]["evidence"][0])
    interpretation = registry.get(organism["payload"]["interpretations"][0])
    address = registry.get(organism["payload"]["addresses"][0])

    semantic_checks = {
        "evidence_precedes_interpretation": (
            interpretation["payload"]["evidence_id"] == evidence["content_id"]
        ),
        "address_links_evidence": (
            address["payload"]["evidence_id"] == evidence["content_id"]
        ),
        "radius_is_advisory": address["payload"]["r_status"] == "ADVISORY",
        "kappa_is_convention": (
            address["payload"]["tags"]["kappa"] == "CONVENTION"
        ),
        "theta_is_candidate": address["payload"]["theta_status"] == "candidate",
        "neighborhood_is_preserved": bool(evidence["payload"]["neighborhood"]),
    }
    ok = graph["ok"] and all(semantic_checks.values())
    return {
        "ok": ok,
        "conformance": ["BAR-Core", "BAR-Frame-candidate"],
        "not_tested": ["BAR-Map-real-runtime", "BAR-Certified"],
        "registry": str(registry_path),
        "ingested": len(ingested),
        "graph": graph,
        "semantic_checks": semantic_checks,
        "organism_record_id": organism["content_id"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    temporary = args.registry is None
    path = args.registry or Path(tempfile.mkdtemp(prefix="bar-conformance-"))
    try:
        result = run(path)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1
    finally:
        if temporary and not args.keep:
            shutil.rmtree(path)


if __name__ == "__main__":
    raise SystemExit(main())

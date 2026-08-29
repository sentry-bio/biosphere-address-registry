# Biosphere Address Registry

**A durable, content-addressed standard for recording where genomic
observations sit relative to a versioned biosphere map and a stable reference
frame.**

The registry does not declare that a model is the tree of life. It preserves
the evidence needed to replay, reinterpret, compare, and render an organism
after encoders, indexes, and taxonomies have changed.

## One sentence

> Sequences are observations; neighborhoods are evidence; species are
> interpretations; coordinates are registered charts; the datum is the stable
> contract joining them.

## The stack

```text
Addressability Limit       what an address can mean
          │
TriangleCCS Form           slow reference frame and conformance contract
          │
Map edition                tokenizer + encoder + index + calibration
          │
Observation → Evidence     sequence hash → named reference neighborhood
          │
Address + Interpretation   registered chart + replaceable taxonomy view
          │
Tools                      place · tree · novelty · dark · chimera · viewer
```

The durable object is an **organism record**, not a species label or a point
drawn on a globe. A record binds:

- exact input identity and window policy;
- map, encoder, index, metric, reference, and calibration identities;
- nearest named references and distances;
- uncertainty, support, novelty, and full rank evidence;
- an optional TriangleCCS address with explicit status and residual;
- a taxonomy interpretation under a named release.

## Why this survives model changes

Three clocks are independent:

| Clock | Object | Typical change |
|---|---|---|
| Form epoch | TriangleCCS Form | metric convention, anchors, epsilon, chart contract |
| Map edition | encoder + index | weights, tokenizer, windows, retrieval, calibration |
| Taxonomy edition | labels over references | GTDB release or nomenclature |

A renamed species does not change its observation or neighborhood. A new
encoder creates a new map edition; it does not silently rewrite old records.
A new map registers through an explicit transform and supports a dual-edition
transition.

## V1 contents

- [`CONSTITUTION.md`](CONSTITUTION.md) — non-negotiable semantic firewall.
- [`STANDARD.md`](STANDARD.md) — normative BAR v1 record standard.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — system and trust boundaries.
- [`docs/SPECIES_RECORDS.md`](docs/SPECIES_RECORDS.md) — organisms as
  distributions, not exact points.
- [`docs/REPOSITORY_MAP.md`](docs/REPOSITORY_MAP.md) — migration and ownership
  across the Sentry Bio repositories.
- [`docs/RELEASE_PROTOCOL.md`](docs/RELEASE_PROTOCOL.md) — map, transform, and
  taxonomy release gates.
- [`docs/END_TO_END_CONFORMANCE.md`](docs/END_TO_END_CONFORMANCE.md) — saved
  protocol for the real 234k v10.9 map.
- [`schemas/`](schemas/) — JSON Schema 2020-12 contracts.
- [`src/biosphere_registry/`](src/biosphere_registry/) — dependency-free
  reference implementation and local content-addressed registry.
- [`examples/`](examples/) — a complete, synthetic, semantically honest record.

## Quick start

```bash
python -m pip install -e ".[dev]"
bar validate examples/organism-record.example.json
bar id examples/organism-record.example.json
bar init /tmp/bar
bar put /tmp/bar examples/organism-record.example.json --ref organisms/example
bar verify /tmp/bar
python scripts/run_local_conformance.py
pytest
```

The CLI stores immutable objects by SHA-256. Human-readable refs are mutable
pointers whose updates are logged; they are never object identities.

## Current real map inventory

Biosphere Atlas v10.9 is an important first map edition, not the standard:

- composed v9 + v10.9 encoder, embedding dimension 129;
- 234,526 reference genomes;
- 1,876,208 vectors at each 5 kb and 20 kb tier;
- exact FlatIP indexes of approximately 968 MB per tier;
- encoder/index checksum binding and self-retrieval load gates.

Those facts belong in a signed `map-edition` record. They do not belong in
TriangleCCS Form.

## Status

BAR v1 is a **candidate standard and functioning reference implementation**.
It does not certify a biological coordinate frame. Certification requires a
published map transform and an independent aligned sextant witness satisfying
the TriangleCCS freeze gate.

## License

MIT.

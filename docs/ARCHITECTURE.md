# Architecture and trust boundaries

## Control plane versus data plane

The **control plane** publishes immutable specifications:

- Forms;
- map editions;
- reference manifests;
- transforms;
- taxonomy releases;
- calibration artifacts;
- verification and conformance reports.

The **data plane** receives sequence, produces observations, performs map
search, and stores evidence and derived views. Data-plane services may scale or
change implementation without changing control-plane meaning.

```text
CONTROL PLANE
 Form ───── Transform ───── Map edition ───── Reference manifest
  │                            │                       │
  └──── conformance report     ├── calibration         └── taxonomy view
                               └── verification receipts

DATA PLANE
 FASTA/reads → Observation → Encode → Search → Evidence
                                             ├→ Interpretation
                                             ├→ Address
                                             └→ Projection
```

## Six layers

### L0 — mathematical boundary

The Addressability Limit establishes a counting ceiling, exact block capacity,
the block/relational ladder, and a hyperbolic zero-relational-tax theorem. It
does not provide an encoder, biological saturation, or organism coordinates.

### L1 — reference frame

TriangleCCS owns the frozen Form, metric/chart conventions, anchors, Address
semantics, and freeze gate. Kappa is `CONVENTION`; dimension two is an
inhabited embeddability floor; radius is `ADVISORY`; theta is `CANDIDATE` until
conformance passes.

### L2 — map edition

A map edition binds preprocessing, effective encoder weights, indexes,
references, metric, routing, calibration, and verification. Biosphere Atlas
v10.9 is the first production-scale candidate.

### L3 — evidence

Evidence is the durable result of applying a map to an observation:
neighborhood, distances, support, novelty, quality, and independent rank
readouts. Evidence contains no mandatory verdict.

### L4 — registration and interpretation

Registration reduces map evidence into a reference-frame Address.
Interpretation applies an ontology or taxonomy. Both are derived, independently
versioned records.

### L5 — instruments and views

Placement, tree reconstruction, chimera detection, novelty, dark-region
mapping, viewers, and field-device clients consume the same records.

## Recommended package boundaries

```text
biosphere_registry       schemas, hashing, records, local registry, CLI
triangleccs              Form mathematics and conformance implementation
atlas-integration        production encoder/index/evidence runtime
atlas-tool-package       tools and visual clients over BAR records
atlas-place              compatibility adapter; eventually a tool plugin
```

The registry MAY depend on TriangleCCS's public contracts. TriangleCCS MUST NOT
depend on a model runtime. Mathematics repositories MUST NOT depend on any
serving or registry package.

## API shape

Normative resources:

```text
GET /v1/forms/{id}
GET /v1/maps/{id}
GET /v1/references/{id}
GET /v1/transforms/{id}
GET /v1/objects/{content_id}
```

Operations:

```text
POST /v1/observe       FASTA/reads → observation
POST /v1/read          observation + map → evidence
POST /v1/register      evidence + transform → address
POST /v1/interpret     evidence + ontology → interpretation
POST /v1/project       records → explicitly ephemeral visualization
POST /v1/replay        recompute and compare a previous reading
POST /v1/compare       compare readings across map/taxonomy epochs
```

`/read` is preferred to `/predict`: the map takes a measurement. `/interpret`
may predict a label; the measurement itself does not.

## Failure behavior

Services fail closed when:

- encoder and index identities differ;
- reference manifest or index digest is unavailable;
- input does not satisfy its window policy;
- requested metric is ambiguous;
- calibration claims exceed their validation regime;
- a transform's input map or dimension does not match;
- a supplied content identifier fails recomputation.

Low complexity, no usable reads, and no close neighbors are valid Evidence,
not server errors and not invitations to force a species call.

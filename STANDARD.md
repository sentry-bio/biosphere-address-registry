# BAR v1 Standard

The key words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative.

## 1. Scope

BAR v1 specifies immutable records connecting genomic observations to
versioned map evidence, optional reference-frame addresses, and replaceable
interpretations. It does not specify a model architecture or biological
taxonomy.

## 2. Canonical serialization and identity

Objects MUST be encoded as UTF-8 JSON. Content identity is:

```text
sha256:<lowercase hex SHA-256 of canonical JSON>
```

Canonical JSON has sorted object keys, no insignificant whitespace, Unicode
preserved, and finite JSON numbers. A top-level `content_id` and `signatures`
field are excluded when computing identity, permitting an object to carry its
identity and detached attestations without self-reference.

Implementations MUST reject a supplied `content_id` that does not match the
computed value.

## 3. Common envelope

Every object MUST contain:

```json
{
  "record_type": "observation",
  "spec_version": "bar-1.0",
  "content_id": "sha256:...",
  "payload": {}
}
```

`content_id` MAY be absent before ingestion. Unknown payload fields MUST be
preserved by readers.

## 4. Record types

### 4.1 `observation`

Identifies the received biological material and preprocessing. It MUST carry:

- `sequence_sha256`;
- `length_bp`;
- `alphabet`;
- `normalization_policy`;
- `window_policy`;
- provenance sufficient to locate or audit the source.

Raw sequence MAY be omitted. If included, its normalized digest MUST match.

### 4.2 `reference-manifest`

Defines the finite set against which map evidence was read. Entries MUST bind
`gid`, accession, assembly version where available, and sequence or assembly
content digest. A taxonomy release MAY annotate entries but does not identify
them.

### 4.3 `map-edition`

Defines one compatible encoding and retrieval universe. It MUST bind:

- `map_id`;
- effective `encoder_id`;
- `tokenizer_id`;
- `reference_manifest_id`;
- search `metric_id`;
- one or more immutable indexes;
- window/scale policy;
- calibration identities;
- verification receipts.

An index MUST NOT be served when its stamped `encoder_id` differs from the
loaded effective encoder identity.

### 4.4 `evidence`

Records a query's map reading. It MUST bind an observation and map edition and
retain:

- complete returned neighborhood up to declared `k`;
- reference identifiers and distances;
- support and input-quality state;
- all computed rank readouts, including gaps;
- novelty/typicality when calibrated;
- the operating-independent scorer version.

It MUST NOT truncate evidence at the first failed taxonomic rank.

### 4.5 `transform`

Registers one map edition onto one Form. It MUST bind both identities, declare
input dimension and coordinate convention, carry the transformation parameters,
anchors, fit-panel identity, residual report, inheritance status, and
certification status.

Warm-start inheritance MUST be marked `CIRCULAR` and cannot independently
certify a transform.

### 4.6 `address`

Records a chart reading derived from evidence under a transform. It MUST carry:

- `form_id` and `transform_id`;
- theta and `theta_status`;
- radius, radial proxy, and `r_status=ADVISORY`;
- registration residual and uncertainty where available;
- map and evidence links.

It MUST NOT identify the origin with LUCA.

### 4.7 `interpretation`

Applies a taxonomy or other ontology to evidence. It MUST carry the ontology
release, operating point, rank-specific calls, confidence provenance, and the
evidence identity. Updating taxonomy creates a new interpretation.

### 4.8 `organism-record`

Links observations, evidence, addresses, and interpretations without copying
their authority. A genome record SHOULD include all deterministic window
observations and a distribution summary. A species record MUST identify the
taxonomy release that supplied membership.

## 5. Metric identifiers

V1 reserves:

| Identifier | Meaning |
|---|---|
| `angular-cosine-v1` | `acos(clamp(dot(unit u, unit v), -1, 1))` |
| `poincare-geodesic-v1` | Poincare-ball geodesic under declared kappa |
| `jc69-v1` | JC69-corrected aligned nucleotide distance |
| `mash-jaccard-v1` | Mash-style canonical k-mer distance |
| `patristic-v1` | path length in a named phylogenetic tree |

Implementations MUST NOT call `angular-cosine-v1` a Poincare geodesic.

## 6. Replay

A record is replayable when an implementation can recover:

1. input normalization and windows;
2. the exact map edition or a preserved compatible runtime;
3. the exact reference manifest and index;
4. evidence under the same scorer and calibration;
5. the transform and Form used for the address;
6. the taxonomy release used for interpretation.

Numerical tolerances and hardware nondeterminism MUST be declared in the map
edition.

## 7. Projection

2D and 3D views are projection artifacts. They MUST link to their source
evidence/map, projection algorithm, basis identity, and parameters. They MUST
NOT be used as the retrieval metric unless separately declared and validated.

## 8. Conformance levels

- **BAR-Core:** canonical identity, schema validity, immutable storage.
- **BAR-Map:** encoder/index binding, neighborhood Evidence, replay receipts.
- **BAR-Frame:** published transform and correctly tagged Address.
- **BAR-Certified:** independent TriangleCCS freeze-gate report passes.

Most initial deployments will be BAR-Map or BAR-Frame, not BAR-Certified.

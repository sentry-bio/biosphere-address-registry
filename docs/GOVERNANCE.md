# Stewardship and governance

BAR should outlive any model, server, company, or taxonomy.

## Stewarded objects

The public standard steward maintains:

- BAR specifications and schemas;
- status vocabulary and metric registry;
- TriangleCCS Form epochs and anchor byte identities;
- conformance test vectors;
- release and signature policy.

Map builders maintain:

- effective encoders and reproducible build recipes;
- map indexes and reference manifests;
- calibration and external validation;
- runtime compatibility and replay.

Ontology stewards maintain interpretations, not observations or map evidence.

## Change classes

### Patch

Clarification or implementation correction that does not alter canonical
record identity or semantics.

### Schema minor

Additive fields. Readers preserve unknown fields; writers continue to satisfy
existing required fields.

### Standard major

Identity rules, required semantics, metric definitions, or record authority
change. Requires a migration document and conformance vectors.

### Form epoch

Chart convention, anchors, epsilon, dimension, kappa convention, or radial
proxy semantics change. Requires explicit old→new transform and dual-address
publication.

### Map edition

Tokenizer, encoder, weights, window policy, references, index, calibration, or
retrieval changes. Does not imply a Form change.

## Proposals

A proposal for a new metric, Form, or promoted claim must include:

- precise definition and units;
- falsification or refusal behavior;
- conformance fixtures;
- comparison with existing semantics;
- migration impact;
- claim status;
- conflicts of interest and artifact provenance.

## Corrections

Incorrect interpretations are superseded by new interpretation records.
Incorrect evidence requires a new map reading and a correction link.
Corrupt objects are quarantined; their content IDs are never reassigned.

## Availability

Published releases SHOULD have:

- at least two independent mirrors;
- checksums and detached signatures;
- open schemas and reader implementation;
- durable citations;
- a manifest sufficient to explain records even when model weights cannot be
  redistributed.

Certification of a public Form should ultimately be held independently from
the principal commercial Atlas operator.

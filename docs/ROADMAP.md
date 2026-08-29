# BAR v1 implementation map

This roadmap is ordered by dependency, not calendar.

## Phase 0 — language and contracts

- Freeze Constitution, Standard, glossary, and record schemas.
- Assign metric identifiers and status vocabulary.
- Publish synthetic examples and schema tests.
- Resolve exact E. coli and M. jannaschii anchor accessions/content hashes.

**Gate:** two independent implementations compute identical content IDs.

## Phase 1 — immutable registry

- Content-addressed object store.
- Append-only event log and mutable human refs.
- Object verification and graph traversal.
- Optional detached signatures.
- Export/import release bundles.

**Gate:** corruption and dangling links are detected; objects replay after
round-trip export.

## Phase 2 — v10.9 map ingestion

- Convert the 234,526-genome manifest into a reference-manifest record.
- Publish composed encoder, tokenizer, 5 kb/20 kb index, calibration, and
  routing identities as a map edition.
- Wrap atlas-integration Evidence in BAR records.
- Preserve angular-cosine metric semantics.

**Gate:** existing ENCODER-MATCH and VERIFY receipts become BAR verification
records.

## Phase 3 — organism recordings

- Persist deterministic window observations.
- Build genome distributions and medoids.
- Build taxonomy-edition species distributions.
- Store dispersion, window agreement, and neighboring regions.

**Gate:** exact known genomes self-retrieve; external genomes produce stable
neighborhoods or honest novelty.

## Phase 4 — TriangleCCS registration

- Import the historical v9 transform as `candidate`.
- Fit a v10.9 transform against exact anchors and a stratified panel.
- Add Address emission to `/register`.
- Add aligned sextant and freeze-gate reports.

**Gate:** address status cannot be promoted by warm-start or same-map
comparison.

## Phase 5 — tool integration

- Make atlas-place a BAR interpretation adapter.
- Make tree consume declared metrics and emit quartet reports.
- Make chimera consume ordered window Evidence.
- Make novelty/dark emit calibrated analysis records.
- Make viewer consume object IDs and publish projection manifests.

**Gate:** all tools preserve provenance and never invent an unstamped geometry.

## Phase 6 — public service

- `/observe`, `/read`, `/register`, `/interpret`, `/project`, `/replay`.
- Public map/Form/reference discovery.
- Streaming and batch clients.
- Edge encode-only client for Jetson-class devices.
- Signed release and mirror protocol.

**Gate:** a stored record remains resolvable without the original live server.

## Phase 7 — stewardship

- Versioning and deprecation policy.
- Independent Form steward and mirror.
- Reproducible rebuild requirements.
- Security and privacy review for unpublished sequences.
- Community proposal process for new metrics, Forms, and interpretation
  ontologies.

**Gate:** no single company, model, server, or taxonomy is required to explain
an existing public record.

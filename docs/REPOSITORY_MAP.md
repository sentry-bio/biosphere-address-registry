# Repository ownership and migration map

BAR harmonizes contributions; it does not copy every historical claim.

## Sources of authority

### `sentry-bio/addressability-limit`

Import by citation:

- fixed-resolution metric packing;
- addressability bound;
- exact block identity;
- constrained-capacity ladder;
- balloon separation;
- weighted hyperbolic relational-capacity theorem.

Do not import biological saturation or organism-coordinate claims; the paper
makes none.

### `TriangleCCS`

Fold into BAR's normative frame:

- immutable Form identity;
- κ and dimension status;
- anchors and \(O(2)\) gauge;
- Address fields and status tags;
- transform schema;
- independent sextant;
- quartet and balloon diagnostics;
- freeze gate and versioning.

TriangleCCS remains the reference implementation for chart mathematics. BAR
owns links and records, not a second theoretical spine.

### `canonical-coordinate-system`

Preserve:

- distance as canonical primitive;
- map-to-datum registration;
- 2×129 tangent backbone and tangent mean;
- anchor gauge;
- invariance and held-out transform tests;
- resolution fade toward genus/species;
- evidence ledger and retractions;
- Voronoi navigation as an operational map layer.

Retire or relabel:

- κ as derived biological truth → Form convention;
- radius as accumulated information → advisory named proxy;
- origin as LUCA → chart origin;
- warm-start agreement as certification → circular;
- species-level θ → map evidence plus residual;
- tokenizer as universal model requirement → map property. If retained in
  Form, it denotes only the canonical witness procedure.

The old v9 transform is a migration candidate, not a certified BAR transform.

### `atlas-integration`

Adopt as the production map kernel:

- self-describing index artifacts;
- effective composed-weight `encoder_id`;
- ENCODER-MATCH and VERIFY load gates;
- deterministic read/window policy;
- adaptive 5 kb/20 kb routing;
- first-class neighborhood;
- Evidence separate from Decision;
- independent rank table;
- calibrated confidence/novelty;
- hot-swap with rollback.

Correct terminology:

- the index is a map edition, not Form;
- FlatIP over L2-normalized angular vectors uses `angular-cosine-v1`;
- `acos(cosine)` is angular distance, not a Poincare-ball geodesic.

### `atlas-place`

Retain as a compatibility adapter for:

- FASTA ingestion;
- ranked candidates;
- TSV/JSON/jplace output;
- pplacer/GTDB-Tk-shaped workflows.

It should consume BAR Evidence. Remove independent geometry ownership,
LUCA-origin semantics, global κ-as-measurement, and hierarchical truncation as
the default.

### `atlas-tool-package`

Rebase each tool on BAR records:

| Tool | BAR input | BAR output |
|---|---|---|
| `atlas-place` | Evidence | Interpretation / jplace view |
| `atlas-tree` | named distance matrix | candidate tree + quartet report |
| `atlas-dark` | map/reference evidence | coverage-region record |
| `atlas-novelty` | Evidence | novelty interpretation |
| `atlas-chimera` | ordered window Evidence | change-point record |
| `atlas-hplg` | Evidence rank table | operating-point interpretation |
| `atlas-viewer` | records | projection manifest + HTML |

Retire first-two-dim θ, LUCA radius, heuristic centroid uncertainty, and
“quartet-consistent by construction.” A tree reconstruction is necessarily a
tree; its input metric requires the independent quartet test.

### `atlas-tool-package` early coordinate artifact

`BiosphereCoordinate_v1.0_Reference.json` is useful provenance but not a final
datum:

- plane fit on a curated 200-genome set;
- one recorded E. coli anchor;
- no recorded chirality anchor;
- E. coli accession differs from TriangleCCS Form;
- centroid-distance uncertainty is heuristic;
- origin is called LUCA.

Freeze exact anchor assembly versions and content hashes before reuse.

## Target dependency graph

```text
addressability-limit  (citation only)
          │
      TriangleCCS
          │
 biosphere-address-registry
      │             │
atlas-integration   atlas-tool-package
      │             │
      └──── Evidence┴── atlas-place adapter
```

## Consolidation end state

- BAR: standard, schemas, registry, provenance, replay.
- TriangleCCS: minimal chart/conformance library.
- atlas-integration: deployed map runtime.
- atlas-tool-package: maintained user-facing instruments.
- atlas-place: package alias/plugin during migration.
- canonical-coordinate-system: archived with migration notes and frozen
  historical transforms.

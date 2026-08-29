# Saved end-to-end conformance run: v10.9 → BAR → TriangleCCS

This is the first real-system acceptance run. It is intentionally **specified
but not represented as executed** in this repository.

## Purpose

Prove that one genomic observation can be:

1. normalized and content-identified;
2. read against the actual 234,526-genome v10.9 map;
3. preserved as neighborhood Evidence;
4. interpreted without discarding uncertainty;
5. registered onto TriangleCCS with correct statuses;
6. replayed deterministically;
7. rendered from the query reading rather than a species-name lookup.

The run does not test biological saturation or derive Form κ.

## Required artifacts

From the v10.9 deployment:

- composed encoder whose effective identity begins `sha256:3b1ab6ad…`;
- exact 5 kb and 20 kb indexes, each 1,876,208 × 129 vectors;
- `gids.npy` for both tiers;
- the 234,526-entry genome manifest;
- taxonomy snapshot and its GTDB release;
- tokenizer and deterministic read policy;
- margin/support calibration;
- encoder/index verification receipts.

From TriangleCCS:

- exact `triangleccs-1.0` Form object;
- byte-identified E. coli prime-meridian material;
- byte-identified M. jannaschii chirality material;
- candidate v10.9 transform;
- independent aligned witness panel when available.

## Test panel

### Exact references

- both Form anchors;
- two bacterial, two archaeal, and two eukaryotic assemblies present in the
  reference manifest;
- two sibling strains from one species.

### External observations

- one newer-GTDB assembly from a represented species;
- one newer-GTDB assembly from a represented genus but unseen species;
- one environmental MAG outside a represented family where possible.

### Refusal controls

- shuffled 20 kb reference window;
- random DNA matched for length and GC;
- homopolymer;
- simple tandem repeat;
- all-N;
- 80 bp random sequence;
- empty/malformed input.

## Protocol

### Step 1 — materialize control-plane records

Create and ingest:

- `reference-manifest`;
- `map-edition`;
- `form`;
- `transform`;
- calibration and verification-report records.

Confirm every tier's `encoder_id` equals the map's effective encoder identity.

### Step 2 — observe

For each input:

1. normalize under `uppercase-strip-whitespace-v1`;
2. compute sequence identity;
3. apply deterministic 5 kb/20 kb window policies;
4. preserve quality and source;
5. ingest every Observation.

### Step 3 — read

For each usable window:

1. route `<3 kb` to 5 kb policy and longer input to 20 kb policy, exactly as
   the map edition declares;
2. call the same tokenizer/encoder path used at index build;
3. search FlatIP over L2-normalized angular vectors;
4. report `metric_id=angular-cosine-v1`;
5. preserve K=15 neighbors, accessions, similarities, angular distances,
   support, typicality, quality, and the full rank table.

No hierarchical path may truncate the evidence.

### Step 4 — aggregate genome regions

Group deterministic windows by assembly. Report:

- medoid window;
- within-genome angular-distance quantiles;
- neighbor agreement;
- cross-tier agreement;
- chimera/change-point candidates;
- windows rejected for quality.

Do not replace the distribution with its medoid.

### Step 5 — interpret

Create at least two interpretations from the same Evidence:

- high-precision operating point (`min_confidence=0.7`);
- exploratory operating point (`min_confidence=0.5`).

Show that Evidence identity is unchanged. Ranks remain independent by default.

### Step 6 — register

Apply the map-to-Form transform:

- verify map and transform identities;
- drop/avoid the radial training head;
- map through the frozen 2D backbone;
- orient with exact anchors;
- emit theta and residual;
- tag radius `ADVISORY`, κ/dim `CONVENTION`;
- keep theta `candidate` unless independent freeze-gate evidence passes.

### Step 7 — replay

Repeat exact-reference observations:

- same hardware/runtime;
- second compatible runtime if available;
- after service restart;
- after index hot-swap back to the same content ID.

Compare Evidence field-by-field under map-declared numerical tolerances.

### Step 8 — project

Render genome window distributions and reference neighbors. The viewer must
consume Evidence IDs. It must not look up a predicted species name in an older
ball file.

## Gates

| Gate | Required outcome |
|---|---|
| Identity | all object and sequence digests recompute |
| Encoder/index | exact identity match on every tier |
| Self-retrieval | exact references recover their own assembly neighborhood |
| External represented | stable close neighborhood at appropriate rank |
| External novel | abstention or honest coarser evidence |
| Refusal | random/shuffled/low-complexity do not receive ordinary species commitment |
| Replay | values exact or within declared tolerance |
| Taxonomy separation | changing release creates a new Interpretation only |
| Address semantics | θ candidate/certified is correct; r advisory; origin not LUCA |
| Transform | held-out and clade-conditioned residuals reported |
| Viewer | plots query observations/regions, not caption lookup |

## Freeze-gate boundary

The following do **not** certify the frame:

- self-retrieval;
- cross-version warm-start agreement;
- taxonomy accuracy;
- SVD versus another output of the same map;
- an NJ tree reconstructed from map distances.

Certification requires the independent aligned sextant witness and declared
determinate-quartet agreement. If unavailable, the run may pass BAR-Map and
BAR-Frame while correctly failing BAR-Certified.

## Output bundle

```text
conformance-run/
  run-manifest.json
  objects/
  replay-report.json
  behavioral-report.json
  transform-report.json
  projection-manifest.json
  SHA256SUMS
  signatures/
```

The highest-value result is not a headline accuracy. It is one complete,
replayable organism-record graph crossing observation, map evidence,
interpretation, registration, and projection without semantic promotion.

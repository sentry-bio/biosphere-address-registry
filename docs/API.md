# Reference API contract

BAR distinguishes immutable resources from computations. HTTP is optional;
these semantics also apply to local and batch implementations.

## Immutable resources

### `GET /v1/objects/{content_id}`

Returns the exact BAR object. Servers MUST recompute and verify its identifier
before returning it.

### `GET /v1/forms/{content_id}`
### `GET /v1/maps/{content_id}`
### `GET /v1/references/{content_id}`
### `GET /v1/transforms/{content_id}`

Typed aliases for object retrieval. Human names MAY redirect to immutable IDs
but MUST expose the resolved ID.

## Computations

### `POST /v1/observe`

Input: FASTA, FASTQ, reads, or raw sequence plus normalization/window policy.

Output: one or more `observation` records. It performs no inference.

### `POST /v1/read`

Input:

```json
{
  "observation_id": "sha256:...",
  "map_edition_id": "sha256:..."
}
```

Output: `evidence`. This endpoint performs the version-matched encode/index
operation. It MUST fail closed on artifact mismatch.

### `POST /v1/register`

Input:

```json
{
  "evidence_id": "sha256:...",
  "transform_id": "sha256:..."
}
```

Output: `address`. It MUST verify that the Evidence map equals the transform
input map and that the transform's Form exists.

### `POST /v1/interpret`

Input: Evidence, ontology release, operating point, and optional view policy.

Output: `interpretation`. Re-running at another confidence threshold does not
re-encode the sequence.

### `POST /v1/project`

Input: records plus projection algorithm and display parameters.

Output: a `projection` manifest and view asset. It MUST identify its source map
and MUST NOT be substituted for Evidence.

### `POST /v1/replay`

Recomputes an Evidence or Address under its original artifacts and returns:

```json
{
  "exact": false,
  "within_tolerance": true,
  "field_differences": [],
  "runtime_identity": {}
}
```

### `POST /v1/compare`

Compares the same observation across map editions, Forms, or taxonomies. It
reports changes separately:

- neighborhood drift;
- evidence/calibration drift;
- Address transform residual;
- taxonomy-only relabeling.

## Error versus evidence

Malformed JSON, unavailable artifacts, or identity mismatches are errors.

These are successful Evidence responses, not errors:

- low-complexity input;
- too-short input;
- no usable windows;
- no close neighbor;
- off-manifold query;
- disagreement between taxonomic ranks.

Such responses should normally abstain from a species decision.

## Privacy

Servers SHOULD allow sequence omission after digesting and SHOULD state
retention policy before accepting unpublished genomic material. Content IDs
are identifiers, not anonymization: a known genome can be dictionary-matched
against its hash.

# Release and conformance protocol

## A. Reference-manifest release

1. Normalize every assembly identifier.
2. Record exact accession version and content digest.
3. Record inclusion/exclusion rules and source release.
4. Validate gid uniqueness and stable ordering.
5. Publish taxonomy as a separately identified annotation.
6. Sign the manifest and preserve previous releases.

## B. Map-edition build

1. Freeze tokenizer, normalization, and window policies.
2. Compose effective model weights.
3. Compute `encoder_id` from deterministic tensor names, dtypes, shapes, and
   bytes.
4. Encode the entire reference manifest.
5. Build each index tier.
6. Stamp index digest, encoder identity, reference identity, dimension, metric,
   scale, and numerical tolerance.
7. Fit calibration without test leakage.

## C. Load gates

A serving process MUST refuse a stamped map when:

- loaded encoder identity differs from index metadata;
- tokenizer/window identity differs;
- index length and gid mapping differ;
- reference or taxonomy digest differs;
- self-retrieval or domain correspondence misses its declared gate.

Legacy unstamped artifacts cannot claim BAR-Map conformance.

## D. Behavioral gates

Every map release publishes:

- exact-reference self-retrieval;
- family/genus/species retrieval, by domain and query length;
- withheld-family and external-genome evaluation;
- random, shuffled, homopolymer, simple-repeat, and too-short controls;
- neighborhood and rank calibration curves;
- deterministic replay tolerance;
- index recall and latency;
- known failure regimes.

OOD controls SHOULD usually abstain. A release that returns confident species
calls for random DNA fails the honesty gate even if in-distribution accuracy is
high.

## E. Transform release

1. Freeze exact Form and map identities.
2. Freeze exact anchor content, not names alone.
3. Fit the map-to-Form transform on a stratified panel.
4. Evaluate on held-out representatives and dense local patches.
5. Report angular residual distribution and clade-conditioned failures.
6. Run independent aligned-sequence sextant comparison.
7. Report determinate quartet agreement separately from unresolved fraction.
8. Mark inheritance (`independent` or `warm_start`).
9. Set `certified=false` unless every freeze-gate criterion passes.

## F. Publication

Publish a release bundle:

```text
release/
  map-edition.json
  reference-manifest.json
  taxonomy-interpretation.json
  calibration-manifest.json
  transform.json
  verification-report.json
  conformance-report.json
  SHA256SUMS
  signatures/
```

## G. Migration and hot-swap

1. Build beside the serving edition.
2. Pass all load and behavioral gates.
3. Shadow real traffic.
4. Replay a fixed witness set under both editions.
5. Publish cross-edition comparison and transform.
6. Require an explicit human promotion.
7. Retain the old edition and one-step rollback.
8. Maintain a dual-address window.

No warm-started successor inherits certification automatically.

## H. V1 acceptance demonstration

The first BAR-Map/Frame demonstration should include:

- both exact Form anchors;
- whole-genome representatives from all domains;
- sibling strains and species;
- a genome absent from the index;
- organisms from a newer reference release;
- shuffled and low-complexity controls;
- deterministic 5 kb and 20 kb windows.

It passes when map evidence is replayable, bad input abstains, references are
recoverable, an Address is correctly tagged, and a viewer renders the actual
query distribution rather than looking up a predicted label.

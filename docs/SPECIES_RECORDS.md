# Species recordings: regions, not pins

## Scale hierarchy

A nucleotide is not an organism and a window is not a species. BAR represents
the hierarchy explicitly:

```text
read/window observation
    ↓ grouped by deterministic window policy
genome recording = empirical distribution of window readings
    ↓ grouped under a named taxonomy release
species recording = distribution of genome recordings
```

For genome \(G\) with map vectors \(z_1,\ldots,z_m\):

\[
\mu_G=\frac1m\sum_{i=1}^m\delta_{z_i}.
\]

A species recording under taxonomy release \(T\) is a finite collection
\(\mathcal S_T=\{\mu_{G_1},\ldots,\mu_{G_n}\}\). Membership is an interpretation
under \(T\), not eternal identity.

## Required genome summary

A genome-level organism record SHOULD retain:

- assembly accession and content digest;
- deterministic window observation links;
- all Evidence links, not only their winning labels;
- representative medoid or declared barycenter;
- within-genome dispersion and quantiles;
- neighborhood stability across windows;
- contamination/chimera change points;
- optional registered Address and its residual.

## Required species summary

A species-level record SHOULD retain:

- taxonomy release and taxon identifier;
- member genome record links;
- representative medoid genome;
- within-species dispersion;
- nearest external species regions;
- overlap and boundary uncertainty;
- coverage and sampling distribution;
- map-edition and Form coverage.

The displayed species pin is a projection of the medoid or barycenter. It MUST
link to the region record and MUST NOT be presented as exact occupancy.

## Stable identity

Stability is built from:

1. sequence/assembly content hashes;
2. immutable map and reference identities;
3. neighborhoods of named accessions;
4. preserved evidence distributions;
5. explicit taxonomy membership editions;
6. registered transforms and residuals.

Coordinates may move between map editions. Records do not. A cross-edition
comparison either replays the same observation in both maps or applies a
published transform with a conformance report.

## Practical consequence for Biosphere Atlas

The v10.9 5 kb and 20 kb tiers already store multiple vectors per genome.
Those vectors should become first-class window observations. The 234,526
genomes are reference entities; the approximately 1.876 million vectors are
their map samples. Collapsing them prematurely to one species label destroys
the information needed for:

- chimera and contamination detection;
- strain and pangenome structure;
- fragment-length uncertainty;
- novelty and dark-region mapping;
- metagenomic mixtures;
- external-genome validation.

## Resolution boundary

TriangleCCS supplies a coarse relational chart. Species and strain resolution
may live primarily in the map's additional dimensions. This is not a failure:
the Address reports the stable coarse chart and residual, while the Evidence
record preserves fine-scale neighborhood structure.

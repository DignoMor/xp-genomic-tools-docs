# FAQ

## Is this a stable release?

No. **0.3.0a4** is an alpha. Pin the git tag and expect CLI/API changes in later
cuts.

## Why is it spelled “Exogenous”?

**Exogenous** is the canonical product spelling for the Python API, CLI, and
docs. Search and import with that spelling (`ExogenousSequenceTools`,
`ExogenousSequences`).

## Is CountTableTools available?

Not in **0.3.0a4**. `RGTools`, `GenomicElementTools`,
`ExogenousSequenceTools`, and `MotifTools` ship.

## Where do I find every CLI flag?

Run `--help` on the tool and subcommand. This site lists commands and nested
formats; argparse help is authoritative for flags and defaults.

```bash
GenomicElementTools pad_region --help
ExogenousSequenceTools assemble add_adapter --help
```

## Known issue: empty `filter_motif_score`

Filtering motif scores down to an empty region set can fail in this alpha
(empty region table edge case). Avoid empty outputs or catch the failure until a
later release.

## NumPy 2?

Not supported in this release. The package requires `numpy>=1.24,<2`.

## Contributor notes (optional)

Large-file sequence / BigWig unit tests need fixtures under
`RGTOOLS_LARGE_FILES`. Ensembl SNP tests need network access; set
`RGTOOLS_SKIP_NETWORK_TESTS=1` to skip them. These env vars matter for
developers running the test suite, not for normal CLI use.

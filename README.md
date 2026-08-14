# xp-genomic-tools docs

Public user documentation for **xp-genomic-tools** release **0.1.0a1**.

Covers the pip-installable `RGTools` library and the `GenomicElementTools` /
`ExogeneousSequenceTools` CLIs from the
[code repository](https://github.com/DignoMor/xp-genomic-tools) tag `0.1.0a1`.

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve
```

## Build

```bash
mkdocs build
```

## Release acceptance build

Install `requirements.txt` into this repository's `.venv`, create the prescribed
`code/.venv` from the sibling code checkout, then run:

```bash
.venv/bin/python scripts/build_release_docs.py \
  --code-root ../code \
  --site-dir site
```

The command regenerates representative CLI syntax from the real argparse tree,
builds MkDocs in strict mode, and verifies the built static references and
`llms.txt` entry point.

Pushing `main` deploys the site via GitHub Pages (see `.github/workflows/pages.yml`).

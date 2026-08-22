# xp-genomic-tools docs

Public user documentation for **xp-genomic-tools** release **0.3.0a1**.

Covers the pip-installable `RGTools` library and the `GenomicElementTools`,
`ExogeneousSequenceTools`, and `MotifTools` CLIs from the
[code repository](https://github.com/DignoMor/xp-genomic-tools) tag `0.3.0a1`.

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
  --site-dir site \
  --code-revision <40-character-code-commit-sha> \
  --docs-revision <40-character-docs-commit-sha> \
  --raw-source-root <checkout-containing-that-docs-commit>
```

The command regenerates representative CLI syntax from the real argparse tree,
builds MkDocs in strict mode, and verifies the built static references and
`llms.txt` and `llms-full.txt` entry points. The code revision must be the exact
release commit. The docs revision must be an immutable commit containing every
raw fallback target, including generated agent resources; commit the docs
content, then rerun this command with that commit SHA (and checkout) before
publishing. The command verifies every referenced raw file exists in that
immutable revision.

Pushing `main` deploys the site via GitHub Pages (see `.github/workflows/pages.yml`).

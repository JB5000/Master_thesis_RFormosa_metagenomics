# Reproduction quickstart

These commands regenerate the retained figure assets from the files in this
repository. Run them from the repository root after creating an isolated
Python environment.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r 02_REPRODUCIBILITY/requirements.txt
```

The main figure scripts write to
`02_REPRODUCIBILITY/regenerated_output/` by default. To use another output
directory, set `RIA_FIGURE_OUTPUT` before running an individual script:

```bash
RIA_FIGURE_OUTPUT=/tmp/ria-figures \
  python 02_REPRODUCIBILITY/scripts/make_Fig_3.12_perkinsus.py
```

The authoritative input/output relationship for each retained figure is in
`ASSET_MANIFEST.tsv`; the complete script inventory is in
`02_REPRODUCIBILITY/SCRIPT_INDEX.tsv`.

Supplementary workflows have their own documented input and output folders.
The relevant commands are recorded in `METHOD_COMMANDS.md` and in the
README files beside each analysis. Large raw FASTQ files and external
software/database resources are intentionally not copied into this bundle;
their portable filenames and required versions are retained as metadata.

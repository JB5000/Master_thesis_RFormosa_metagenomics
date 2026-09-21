# Portability and path inventory

The scripts contain commands, flags, software versions, sample identifiers, random seeds and analytical values recorded in the retained files.

- Machine-specific paths are represented by documented variables such as `${PROJECT_HOME}`, `${RAW_DATA_ROOT}`, `${HPC_DATA_ROOT}` and `${HPC_SOFTWARE_ROOT}`.
- Active public copies contain no detected usernames, private storage locations, compute-node hostnames or nonessential scheduler identifiers.
- Recruitment scripts use environment variables while preserving minimap2 `-ax map-ont` and the retained samtools filtering flags.
- The recruitment coverage helper path is represented by `${RIA_COVERAGE_HELPER}`; the helper file state is `UNAVAILABLE_HISTORICAL_RUNTIME`.
- Supplementary Figure S3 uses identifier S3 in its filename, script, caption and indexes.
- Provenance documents record source files, commands, versions, outputs and unavailable items.
- Paths under `/vol/data/...` and `/vol/tmp/...` in the retained porTraits/CloWM workflow evidence are workflow- or container-internal paths preserved for provenance. They are not private user/HPC paths and are not portable rerun configuration. Portable reruns require site-specific variables or configuration.
- KrakenUniq report headers retained under `16_RECENT_ANALYSES` are primary
  tool output and may contain the original runtime working-directory field.
  That header field is provenance, not active or portable configuration.
- `${CETA_RESULTS}` in recent-analysis documentation is a site-specific source
  locator. The scripts that regenerate bundle figures use paths relative to
  their own analysis directory.

The validation report records the scientific-invariant comparisons performed after path substitution.

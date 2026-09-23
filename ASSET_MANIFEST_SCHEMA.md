# Asset manifest schema

`ASSET_MANIFEST.tsv` is the machine-readable index of retained figures and
result tables. It uses tab-separated fields and repository-relative paths.

| Field | Meaning |
|---|---|
| `asset_filename` | Path to the retained figure or table. |
| `asset_type` | `final_figure`, `candidate_figure` or `result_table`. |
| `description` | Short factual description of the asset. |
| `source_data` | One or more source paths, separated by `;`. External inputs are marked `external:`. |
| `generation_script` | Repository-relative generation script, or `-` where the asset is a direct reference/resource. |
| `upstream_analysis` | Analysis producing the source values. |
| `status` | `final`, `candidate` or `retained`. |
| `notes` | Additional factual provenance note, when needed. |

The manifest records relationships; it does not impose thesis numbering or
serve as a substitute for the scientific result tables.

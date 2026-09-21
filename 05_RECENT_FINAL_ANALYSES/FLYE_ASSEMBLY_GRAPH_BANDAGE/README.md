# Flye coassembly graph — Bandage global view

`figures/Flye_coassembly_graph_full_Bandage.png` is an exploratory global rendering of the complete Flye assembly graph from the four-sample coassembly. It is not a filtered MAG graph and should not be interpreted as a genome map.

## Source graph

Institutional CETA source:

The original private CETA work-path is intentionally not distributed. The
portable retained input is `input/Flye_coassembly_top100_connected_components.gfa`.

The local interactive copy is retained in Downloads as `Ria_Formosa_Flye_coassembly_graph_final.gfa` (487 MB), rather than duplicated into this bundle.

## Reproduction

Bandage version 0.9.0 was used:

```bash
Bandage info Ria_Formosa_Flye_coassembly_graph_final.gfa
Bandage image Ria_Formosa_Flye_coassembly_graph_final.gfa Flye_coassembly_graph_full_Bandage.png --width 4000 --height 4000
```

Graph summary: 31,218 nodes, 1,363 edges, total graph length 485,788,782 bp, and 30,338 connected components. The dense global appearance is expected because most nodes are isolated contigs.

For interactive inspection use:

```bash
Bandage load Ria_Formosa_Flye_coassembly_graph_final.gfa
```

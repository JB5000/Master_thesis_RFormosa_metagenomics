# Flye co-assembly graph — 100 largest connected components

`01_FIGURES/final/Fig_S5_Flye_Bandage_top100_components.png` is the retained Bandage rendering. It was made from the Flye co-assembly graph after retaining the 100 largest connected components (rather than displaying every component in the full graph). This removes the very large collection of isolated, small structures while retaining the largest assembly-graph contexts.

The derived input GFA is stored beside the image as `input/Flye_coassembly_top100_connected_components.gfa`.  The filtering logic is documented in `scripts/extract_largest_component.py`; Bandage was then used to render the retained graph.

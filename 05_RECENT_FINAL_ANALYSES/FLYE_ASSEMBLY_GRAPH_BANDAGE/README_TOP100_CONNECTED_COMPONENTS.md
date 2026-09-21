# Flye co-assembly graph — 100 largest connected components

`figures/Flye_coassembly_top100_connected_components_Bandage.png` is the Bandage rendering selected for thesis review.  It was made from the Flye co-assembly graph after retaining the 100 largest connected components (rather than displaying every component in the full graph).  This removes the very large collection of isolated, small structures while retaining the largest assembly-graph contexts.

The derived input GFA is stored beside the image as `input/Flye_coassembly_top100_connected_components.gfa`.  The filtering logic is documented in `scripts/extract_largest_component.py`; Bandage was then used to render the retained graph.

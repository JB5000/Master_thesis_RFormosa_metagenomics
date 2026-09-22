#!/usr/bin/env python3
"""Extract the largest connected component from a GFA1 assembly graph."""

from __future__ import annotations

import argparse
from pathlib import Path


def segment_length(fields: list[str]) -> int:
    length = 0 if fields[2] == "*" else len(fields[2])
    for field in fields[3:]:
        if field.startswith("LN:i:"):
            return int(field.split(":", 2)[2])
    return length


def find(parent: dict[str, str], node: str) -> str:
    while parent[node] != node:
        parent[node] = parent[parent[node]]
        node = parent[node]
    return node


def union(parent: dict[str, str], left: str, right: str) -> None:
    left_root, right_root = find(parent, left), find(parent, right)
    if left_root != right_root:
        parent[right_root] = left_root


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_gfa", type=Path)
    parser.add_argument("output_gfa", type=Path)
    parser.add_argument(
        "--components",
        type=int,
        default=1,
        help="Number of largest connected components to retain (default: 1).",
    )
    args = parser.parse_args()

    parent: dict[str, str] = {}
    lengths: dict[str, int] = {}
    with args.input_gfa.open() as handle:
        for line in handle:
            fields = line.rstrip("\n").split("\t")
            if fields[0] == "S":
                parent[fields[1]] = fields[1]
                lengths[fields[1]] = segment_length(fields)
            elif fields[0] == "L":
                # Segment records precede links in standard Flye GFA output.
                union(parent, fields[1], fields[3])

    component_bp: dict[str, int] = {}
    component_nodes: dict[str, set[str]] = {}
    for node, length in lengths.items():
        root = find(parent, node)
        component_bp[root] = component_bp.get(root, 0) + length
        component_nodes.setdefault(root, set()).add(node)

    selected_roots = sorted(
        component_bp, key=component_bp.get, reverse=True
    )[: args.components]
    keep = set().union(*(component_nodes[root] for root in selected_roots))
    args.output_gfa.parent.mkdir(parents=True, exist_ok=True)
    with args.input_gfa.open() as source, args.output_gfa.open("w") as output:
        for line in source:
            fields = line.rstrip("\n").split("\t")
            if fields[0] == "H":
                output.write(line)
            elif fields[0] == "S" and fields[1] in keep:
                output.write(line)
            elif fields[0] == "L" and fields[1] in keep and fields[3] in keep:
                output.write(line)

    print(
        f"components_retained={len(selected_roots)} nodes_retained={len(keep)} "
        f"largest_component_bp={component_bp[selected_roots[0]]} "
        f"total_bp_retained={sum(component_bp[root] for root in selected_roots)}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""Generate evidence-derived figures for the IEEEtran working manuscript."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "network" / "canonical-network.geojson"
OUT = ROOT / "manuscript" / "figures"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    features = json.loads(DATA.read_text(encoding="utf-8"))["features"]
    buses = [f for f in features if f["geometry"]["type"] == "Point"]
    branches = [f for f in features if f["geometry"]["type"] == "LineString"]

    fig, ax = plt.subplots(figsize=(7.1, 4.9), constrained_layout=True)
    for feature in branches:
        coords = feature["geometry"]["coordinates"]
        style = {"line": ("#537a91", 0.9, 1.0), "link": ("#d68a22", 1.35, 1.0)}[feature["properties"]["branch_type"]]
        ax.plot([p[0] for p in coords], [p[1] for p in coords], color=style[0], lw=style[1], alpha=style[2], zorder=1)
    colors = {"GEN": "#b23a48", "SUBSTATION": "#222222", "NODE": "#f0c14b"}
    for type_name, color in colors.items():
        subset = [f for f in buses if f["properties"]["type"] == type_name]
        ax.scatter([f["geometry"]["coordinates"][0] for f in subset], [f["geometry"]["coordinates"][1] for f in subset], c=color, s=24, edgecolors="white", linewidths=0.35, zorder=2)
    ax.set_xlabel("Longitude (degrees, EPSG:4326)")
    ax.set_ylabel("Latitude (degrees, EPSG:4326)")
    ax.set_title("Project-authored synthetic spatial layer (not real infrastructure)")
    ax.grid(color="#dddddd", linewidth=0.5)
    handles = [Line2D([0], [0], color="#537a91", lw=1.5, label="34 line routes"), Line2D([0], [0], color="#d68a22", lw=1.5, label="7 link routes")]
    handles += [Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markeredgecolor="white", markersize=6, label=label) for label, color in colors.items()]
    ax.legend(handles=handles, loc="best", fontsize=8, frameon=True)
    fig.savefig(OUT / "spatial-layer-map.png", dpi=300)
    fig.savefig(OUT / "spatial-layer-map.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.1, 2.5), constrained_layout=True)
    ax.axis("off")
    labels = ["Canonical\nGeoJSON", "Schema +\nmanifest", "Spatial QA\n(EPSG:3310)", "Release archive\n+ checksums", "Reusable spatial\nbenchmark"]
    for i, label in enumerate(labels):
        center = 0.11 + i * 0.195
        ax.text(center, 0.5, label, ha="center", va="center", fontsize=8.5, bbox={"boxstyle": "round,pad=0.45", "facecolor": "#eaf2f8", "edgecolor": "#537a91"})
        if i < len(labels) - 1:
            ax.annotate("", xy=(center + 0.085, 0.5), xytext=(center + 0.12, 0.5), arrowprops={"arrowstyle": "->", "color": "#555555"})
    fig.savefig(OUT / "release-workflow.png", dpi=300)
    fig.savefig(OUT / "release-workflow.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import h5py


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "metadata" / "manifest.csv"
SUMMARY_PATH = ROOT / "metadata" / "summary.json"
CASE_RE = re.compile(r"^(?P<mask_id>\d+)_Pigbt(?P<Pigbt>\d+)_Pfwd(?P<Pfwd>\d+)_h(?P<h_value>\d+)$")


def iter_samples():
    for split in ["TrainData", "ValData", "TestData"]:
        split_dir = ROOT / split
        if not split_dir.exists():
            continue
        for h5_path in sorted(split_dir.rglob("data.h5")):
            rel = h5_path.relative_to(ROOT)
            topology = rel.parts[1]
            case_name = rel.parts[2]
            match = CASE_RE.match(case_name)
            if match is None:
                raise ValueError(f"Unexpected sample folder name: {case_name}")

            labels = match.groupdict()
            with h5py.File(h5_path, "r") as f:
                n_instances = int(f["row_ids"].shape[0])
                h_normalized = float(f["h_normalized"][0])

            yield {
                "split": split,
                "topology": topology,
                "mask_id": labels["mask_id"],
                "Pigbt": int(labels["Pigbt"]),
                "Pfwd": int(labels["Pfwd"]),
                "h_value": int(labels["h_value"]),
                "h_normalized": h_normalized,
                "n_instances": n_instances,
                "bytes": h5_path.stat().st_size,
                "path": rel.as_posix(),
            }


def main() -> None:
    rows = list(iter_samples())
    MANIFEST_PATH.parent.mkdir(exist_ok=True)

    fieldnames = [
        "split",
        "topology",
        "mask_id",
        "Pigbt",
        "Pfwd",
        "h_value",
        "h_normalized",
        "n_instances",
        "bytes",
        "path",
    ]
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    split_counts = Counter(row["split"] for row in rows)
    topology_counts = Counter(row["topology"] for row in rows)
    topology_instances = {}
    layout_ids = defaultdict(set)
    for row in rows:
        topology_instances.setdefault(row["topology"], row["n_instances"])
        layout_ids[row["topology"]].add(row["mask_id"])

    summary = {
        "total_samples": len(rows),
        "total_size_bytes": sum(row["bytes"] for row in rows),
        "splits": dict(sorted(split_counts.items())),
        "topologies": dict(sorted(topology_counts.items())),
        "topology_instances": dict(sorted(topology_instances.items())),
        "unique_layout_ids": {
            topology: len(ids) for topology, ids in sorted(layout_ids.items())
        },
        "Pigbt_values": sorted({row["Pigbt"] for row in rows}),
        "Pfwd_values": sorted({row["Pfwd"] for row in rows}),
        "h_values": sorted({row["h_value"] for row in rows}),
    }
    with SUMMARY_PATH.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT)} with {len(rows)} rows")
    print(f"Wrote {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

import h5py
import numpy as np


def summarize_dataset(name: str, data: np.ndarray) -> str:
    summary = f"{name}: shape={data.shape}, dtype={data.dtype}"
    if np.issubdtype(data.dtype, np.number):
        summary += (
            f", min={np.nanmin(data):.6g}, max={np.nanmax(data):.6g}, "
            f"mean={np.nanmean(data):.6g}"
        )
    return summary


def plot_sample(h5_path: Path, output_path: Path) -> None:
    import matplotlib.pyplot as plt

    with h5py.File(h5_path, "r") as f:
        panels = [
            ("temperature", f["temperature"][:], "inferno"),
            ("power_map", f["power_map"][:], "magma"),
            ("instance_map", f["instance_map"][:], "tab20"),
            ("copper_mask", f["copper_mask"][:], "gray"),
            ("ceramic_mask", f["ceramic_mask"][:], "gray"),
            ("baseplate_mask", f["baseplate_mask"][:], "gray"),
        ]

    fig, axes = plt.subplots(2, 3, figsize=(10, 6), constrained_layout=True)
    for ax, (title, arr, cmap) in zip(axes.flat, panels):
        im = ax.imshow(arr, cmap=cmap)
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect one dataset HDF5 sample.")
    parser.add_argument("sample", type=Path, help="Path to a data.h5 sample.")
    parser.add_argument("--plot", type=Path, help="Optional output PNG path.")
    args = parser.parse_args()

    with h5py.File(args.sample, "r") as f:
        print(f"File: {args.sample}")
        print("Attributes:")
        for key, value in f.attrs.items():
            print(f"  {key}: {value}")
        print("Datasets:")
        for key in sorted(f.keys()):
            print("  " + summarize_dataset(key, f[key][:]))

    if args.plot:
        plot_sample(args.sample, args.plot)
        print(f"Plot written to: {args.plot}")


if __name__ == "__main__":
    main()

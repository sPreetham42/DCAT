"""CLI script for running DCAT dataset exploration.

Usage:
    python -m dcat.scripts.explore_dataset --input data/processed/records.parquet
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dcat.data.exploration import DatasetExplorer
from dcat.data.parquet import ParquetDatasetReader


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Explore DCAT dataset statistics.")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to Parquet dataset file to explore",
    )
    parser.add_argument(
        "--output-json",
        "-o",
        default="artifacts/data_exploration.json",
        help="Path to save machine-readable JSON exploration report",
    )
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: dataset file '{input_path}' does not exist.", file=sys.stderr)
        return 1

    records = ParquetDatasetReader.load_records(input_path)
    explorer = DatasetExplorer()
    report = explorer.explore(records)

    print(report.render_text())

    # Save JSON artifact
    out_json = Path(opts.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(report.to_dict(), fh, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())

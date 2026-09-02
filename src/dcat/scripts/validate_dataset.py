"""CLI script for validating DCAT Parquet datasets.

Usage:
    python -m dcat.scripts.validate_dataset --input data/processed/records.parquet
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dcat.data.parquet import ParquetDatasetReader
from dcat.data.validation import DatasetValidator


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate DCAT dataset records.")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to Parquet dataset file to validate",
    )
    parser.add_argument(
        "--output-json",
        "-o",
        default="artifacts/dataset_validation.json",
        help="Path to save machine-readable JSON validation report",
    )
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: dataset file '{input_path}' does not exist.", file=sys.stderr)
        return 1

    records = ParquetDatasetReader.load_records(input_path)
    validator = DatasetValidator()
    report = validator.validate(records)

    print(report.render_text())

    # Write machine-readable artifact
    out_path = Path(opts.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report.to_dict(), fh, indent=2)

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())

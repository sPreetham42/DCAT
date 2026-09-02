"""CLI script for running DCAT pre-publication leakage audits.

Usage:
    python -m dcat.scripts.audit_leakage --input data/processed/records.parquet
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dcat.data.leakage import LeakageAuditor
from dcat.data.parquet import ParquetDatasetReader


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit DCAT dataset for cross-split leakage.")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to Parquet dataset file to audit",
    )
    parser.add_argument(
        "--output-json",
        "-o",
        default="artifacts/leakage_audit.json",
        help="Path to save machine-readable JSON leakage report",
    )
    parser.add_argument(
        "--output-md",
        "-m",
        default="artifacts/leakage_audit.md",
        help="Path to save Markdown report suitable for MLflow artifacts",
    )
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: dataset file '{input_path}' does not exist.", file=sys.stderr)
        return 1

    records = ParquetDatasetReader.load_records(input_path)
    auditor = LeakageAuditor()
    report = auditor.audit(records)

    md_text = report.render_markdown()
    print(md_text)

    # Save JSON artifact
    out_json = Path(opts.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(report.to_dict(), fh, indent=2)

    # Save Markdown artifact
    out_md = Path(opts.output_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    with open(out_md, "w", encoding="utf-8") as fh:
        fh.write(md_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())

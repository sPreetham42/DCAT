"""Dataset exploration suite for DCAT.

Computes comprehensive, reproducible dataset statistics:
- Label distribution (ham/spam counts & percentages)
- Modality distribution (TEXT/IMAGE/MULTIMODAL/EMPTY)
- Modality x Label cross-tabulation matrix
- Text length distribution statistics
- Image statistics (counts, dimensions, filter reasons)
- Sender & campaign distribution statistics
- Dataset split distribution
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Sequence

from dcat.data.records import EmailRecord


def _stats(values: list[int | float]) -> dict[str, float]:
    if not values:
        return {"count": 0, "min": 0, "mean": 0, "median": 0, "p95": 0, "max": 0}
    sorted_v = sorted(values)
    n = len(sorted_v)
    mean = sum(sorted_v) / n
    median = sorted_v[n // 2] if n % 2 != 0 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2
    p95_idx = int(math.ceil(0.95 * n)) - 1
    p95 = sorted_v[max(0, min(p95_idx, n - 1))]
    return {
        "count": float(n),
        "min": float(sorted_v[0]),
        "mean": float(mean),
        "median": float(median),
        "p95": float(p95),
        "max": float(sorted_v[-1]),
    }


@dataclass
class ExplorationReport:
    """Complete summary of dataset statistics."""

    total_records: int
    splits: dict[str, int]
    label_distribution: dict[str, int]
    modality_distribution: dict[str, int]
    modality_x_label: dict[str, dict[str, int]]
    text_length_stats: dict[str, float]
    image_stats: dict[str, Any]
    sender_campaign_stats: dict[str, Any]

    def to_dict(self) -> dict:
        return asdict(self)

    def render_text(self) -> str:
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("DCAT Dataset Exploration Report")
        lines.append("=" * 60)
        lines.append(f"Total Records: {self.total_records}")
        lines.append(f"Splits       : {self.splits}")
        lines.append("-" * 60)
        lines.append("[Label Distribution]")
        for k, v in self.label_distribution.items():
            pct = (v / self.total_records * 100) if self.total_records > 0 else 0
            lines.append(f"  {k:<12}: {v:>6} ({pct:5.1f}%)")

        lines.append("\n[Modality Distribution]")
        for k, v in self.modality_distribution.items():
            pct = (v / self.total_records * 100) if self.total_records > 0 else 0
            lines.append(f"  {k:<12}: {v:>6} ({pct:5.1f}%)")

        lines.append("\n[Modality x Label Cross-Tabulation]")
        lines.append(f"  {'Modality':<12} {'Ham (0)':<10} {'Spam (1)':<10} {'Unknown':<10}")
        lines.append("  " + "-" * 42)
        for mod, row in self.modality_x_label.items():
            lines.append(
                f"  {mod:<12} {row.get('ham', 0):<10} {row.get('spam', 0):<10} {row.get('unknown', 0):<10}"
            )

        lines.append("\n[Text Length Stats (characters)]")
        for k, v in self.text_length_stats.items():
            lines.append(f"  {k:<10}: {v:.1f}")

        lines.append("\n[Image Stats]")
        lines.append(f"  Total Images Extracted   : {self.image_stats['total_images']}")
        lines.append(f"  Filtered Images          : {self.image_stats['filtered_images']}")
        lines.append(f"  Meaningful Images        : {self.image_stats['meaningful_images']}")
        lines.append("  Filter Reasons Breakdown :")
        for reason, cnt in self.image_stats["filter_reasons"].items():
            lines.append(f"    - {reason}: {cnt}")

        lines.append("\n[Sender & Campaign Stats]")
        lines.append(f"  Unique Senders   : {self.sender_campaign_stats['unique_senders']}")
        lines.append(f"  Unique Campaigns : {self.sender_campaign_stats['unique_campaigns']}")
        lines.append("=" * 60)
        return "\n".join(lines)


class DatasetExplorer:
    """Engine for generating dataset exploration reports."""

    def explore(self, records: Sequence[EmailRecord]) -> ExplorationReport:
        total = len(records)
        splits: dict[str, int] = {}
        labels: dict[str, int] = {"ham": 0, "spam": 0, "unknown": 0}
        modalities: dict[str, int] = {"text": 0, "image": 0, "multimodal": 0, "empty": 0}
        mod_x_label: dict[str, dict[str, int]] = {
            "text": {"ham": 0, "spam": 0, "unknown": 0},
            "image": {"ham": 0, "spam": 0, "unknown": 0},
            "multimodal": {"ham": 0, "spam": 0, "unknown": 0},
            "empty": {"ham": 0, "spam": 0, "unknown": 0},
        }

        text_lengths: list[int] = []
        total_images = 0
        filtered_images = 0
        meaningful_images = 0
        filter_reasons: dict[str, int] = {}

        senders: set[str] = set()
        campaigns: set[str] = set()

        for r in records:
            sp = r.split or "unassigned"
            splits[sp] = splits.get(sp, 0) + 1

            lbl_key = "ham" if r.label == 0 else ("spam" if r.label == 1 else "unknown")
            labels[lbl_key] += 1

            mod_key = r.modality.value
            modalities[mod_key] = modalities.get(mod_key, 0) + 1
            mod_x_label[mod_key][lbl_key] += 1

            if r.text:
                text_lengths.append(len(r.text))

            total_images += len(r.images)
            for img in r.images:
                if img.filtered:
                    filtered_images += 1
                    reason = img.filter_reason or "unknown"
                    filter_reasons[reason] = filter_reasons.get(reason, 0) + 1
                else:
                    meaningful_images += 1

            if r.sender_hash:
                senders.add(r.sender_hash)
            if r.campaign_id:
                campaigns.add(r.campaign_id)

        t_stats = _stats(text_lengths)

        return ExplorationReport(
            total_records=total,
            splits=splits,
            label_distribution=labels,
            modality_distribution=modalities,
            modality_x_label=mod_x_label,
            text_length_stats=t_stats,
            image_stats={
                "total_images": total_images,
                "filtered_images": filtered_images,
                "meaningful_images": meaningful_images,
                "filter_reasons": filter_reasons,
            },
            sender_campaign_stats={
                "unique_senders": len(senders),
                "unique_campaigns": len(campaigns),
            },
        )


__all__ = ["DatasetExplorer", "ExplorationReport"]

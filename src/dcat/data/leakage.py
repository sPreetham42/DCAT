"""Data leakage auditor for DCAT datasets.

Detects cross-split contamination before training:
1. Exact email text & image SHA-256 hash duplicates across splits.
2. Image perceptual hashing (aHash/dHash) for recompressed image duplicates across splits.
3. Text near-duplicate detection via 5-gram Jaccard similarity.
4. Hyperlinked URL domain overlap across splits.
5. Sender email address and campaign ID overlap across splits.

Crucially:
- Does NOT automatically mutate or delete records.
- Produces detailed machine-readable (JSON) and Markdown reports for MLflow tracking.
"""

from __future__ import annotations

import hashlib
import io
import re
from dataclasses import asdict, dataclass
from typing import Sequence

from PIL import Image

from dcat.data.records import EmailRecord, RawImage


def compute_sha256(data: bytes | str) -> str:
    """Compute hex SHA-256 hash of text or binary data."""
    if isinstance(data, str):
        data = data.encode("utf-8", "replace")
    return hashlib.sha256(data).hexdigest()


def compute_image_ahash(img_data: bytes, hash_size: int = 8) -> str | None:
    """Compute pure-PIL average perceptual hash (aHash) for an image payload.

    Args:
        img_data: raw image payload bytes.
        hash_size: grid size (default 8x8 -> 64-bit hash).

    Returns:
        Hex perceptual hash string or None if unparseable.
    """
    try:
        with Image.open(io.BytesIO(img_data)) as img:
            img = img.convert("L").resize((hash_size, hash_size), Image.Resampling.BILINEAR)
            pixels = list(img.getdata())
            avg = sum(pixels) / len(pixels)
            bits = "".join(["1" if p > avg else "0" for p in pixels])
            # Convert 64-bit string to 16-char hex
            return f"{int(bits, 2):016x}"
    except Exception:  # noqa: BLE001
        return None


def extract_urls(text: str | None) -> set[str]:
    """Extract hyperlinked URLs from text."""
    if not text:
        return set()
    url_pattern = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
    return set(url_pattern.findall(text))


def jaccard_similarity_ngrams(text1: str, text2: str, n: int = 5) -> float:
    """Calculate character n-gram Jaccard similarity between two texts."""
    if not text1 or not text2:
        return 0.0
    s1 = set(text1[i : i + n] for i in range(len(text1) - n + 1))
    s2 = set(text2[i : i + n] for i in range(len(text2) - n + 1))
    if not s1 or not s2:
        return 0.0
    intersection = len(s1.intersection(s2))
    union = len(s1.union(s2))
    return intersection / union if union > 0 else 0.0


@dataclass
class LeakagePair:
    """A pair of leaking records across dataset splits."""

    email_id_1: str
    split_1: str
    email_id_2: str
    split_2: str
    leak_type: str  # "exact_text", "exact_image", "perceptual_image", "near_text_similarity"
    similarity: float


@dataclass
class OverlapSummary:
    """Summary of domain/sender/campaign overlaps across splits."""

    shared_senders: dict[str, list[str]]  # split_pair -> list of senders
    shared_campaigns: dict[str, list[str]]  # split_pair -> list of campaign IDs
    shared_urls: dict[str, int]  # split_pair -> count of shared URLs


@dataclass
class LeakageReport:
    """Comprehensive data leakage audit report."""

    total_records: int
    splits: dict[str, int]
    exact_text_duplicates_cross_split: int
    exact_image_duplicates_cross_split: int
    perceptual_image_duplicates_cross_split: int
    near_text_duplicates_cross_split: int
    leakage_pairs: list[LeakagePair]
    overlap_summary: OverlapSummary

    def to_dict(self) -> dict:
        return {
            "total_records": self.total_records,
            "splits": self.splits,
            "exact_text_duplicates_cross_split": self.exact_text_duplicates_cross_split,
            "exact_image_duplicates_cross_split": self.exact_image_duplicates_cross_split,
            "perceptual_image_duplicates_cross_split": self.perceptual_image_duplicates_cross_split,
            "near_text_duplicates_cross_split": self.near_text_duplicates_cross_split,
            "leakage_pairs": [asdict(p) for p in self.leakage_pairs],
            "overlap_summary": asdict(self.overlap_summary),
        }

    def render_markdown(self) -> str:
        lines: list[str] = []
        lines.append("# DCAT Dataset Leakage Audit Report")
        lines.append("")
        lines.append(f"**Total Records:** {self.total_records}")
        lines.append(f"**Split Counts:** {self.splits}")
        lines.append("")
        lines.append("## Cross-Split Leakage Summary")
        lines.append(f"- **Exact Text Duplicates Across Splits:** {self.exact_text_duplicates_cross_split}")
        lines.append(f"- **Exact Image Duplicates Across Splits:** {self.exact_image_duplicates_cross_split}")
        lines.append(
            f"- **Perceptual Image Duplicates Across Splits:** {self.perceptual_image_duplicates_cross_split}"
        )
        lines.append(
            f"- **Near-Duplicate Text Pairs (Jaccard > 0.85):** {self.near_text_duplicates_cross_split}"
        )
        lines.append("")
        lines.append("## Sender & Campaign Overlaps")
        for pair, senders in self.overlap_summary.shared_senders.items():
            lines.append(f"- **{pair} Shared Senders:** {len(senders)}")
        for pair, cmps in self.overlap_summary.shared_campaigns.items():
            lines.append(f"- **{pair} Shared Campaigns:** {len(cmps)}")
        lines.append("")
        if self.leakage_pairs:
            lines.append("## Sample Flagged Leakage Pairs (Top 20)")
            lines.append("| Email ID 1 (Split 1) | Email ID 2 (Split 2) | Leak Type | Similarity |")
            lines.append("|---|---|---|---|")
            for pair in self.leakage_pairs[:20]:
                lines.append(
                    f"| {pair.email_id_1} ({pair.split_1}) | {pair.email_id_2} ({pair.split_2}) | {pair.leak_type} | {pair.similarity:.4f} |"
                )
        else:
            lines.append("**[PASS] No cross-split leakage detected!**")
        return "\n".join(lines)


class LeakageAuditor:
    """Pre-publication leakage audit engine."""

    def __init__(self, jaccard_threshold: float = 0.85) -> None:
        self.jaccard_threshold = jaccard_threshold

    def audit(self, records: Sequence[EmailRecord], raw_images: Sequence[RawImage] = ()) -> LeakageReport:
        splits_count: dict[str, int] = {}
        for r in records:
            sp = r.split or "unassigned"
            splits_count[sp] = splits_count.get(sp, 0) + 1

        text_hashes: dict[str, list[tuple[str, str]]] = {}  # text_hash -> [(email_id, split)]
        raw_img_hashes: dict[str, list[tuple[str, str]]] = {}  # raw_img_id -> [(email_id, split)]
        ahash_map: dict[str, list[tuple[str, str]]] = {}  # ahash -> [(email_id, split)]

        sender_map: dict[str, set[str]] = {}  # split -> set(senders)
        campaign_map: dict[str, set[str]] = {}  # split -> set(campaign_ids)
        url_map: dict[str, set[str]] = {}  # split -> set(urls)

        record_texts: list[tuple[str, str, str]] = []  # (email_id, split, clean_text)

        # Map RawImages by image_id
        raw_img_dict = {img.image_id: img for img in raw_images}

        for rec in records:
            sp = rec.split or "unassigned"

            if rec.sender_hash:
                sender_map.setdefault(sp, set()).add(rec.sender_hash)
            if rec.campaign_id:
                campaign_map.setdefault(sp, set()).add(rec.campaign_id)

            if rec.text:
                thash = compute_sha256(rec.text)
                text_hashes.setdefault(thash, []).append((rec.email_id, sp))
                record_texts.append((rec.email_id, sp, rec.text))
                urls = extract_urls(rec.text)
                if urls:
                    url_map.setdefault(sp, set()).update(urls)

            for img in rec.images:
                if img.exact_hash:
                    raw_img_hashes.setdefault(img.exact_hash, []).append((rec.email_id, sp))
                if img.perceptual_hash:
                    ahash_map.setdefault(img.perceptual_hash, []).append((rec.email_id, sp))
                elif img.image_id in raw_img_dict:
                    # Compute ahash from transient raw bytes
                    ah = compute_image_ahash(raw_img_dict[img.image_id].data)
                    if ah:
                        ahash_map.setdefault(ah, []).append((rec.email_id, sp))

        leakage_pairs: list[LeakagePair] = []
        exact_text_count = 0
        exact_img_count = 0
        perceptual_img_count = 0
        near_text_count = 0

        # Check exact text cross-split duplicates
        for _thash, occurrences in text_hashes.items():
            splits_seen = set(sp for _, sp in occurrences)
            if len(splits_seen) > 1:
                first = occurrences[0]
                for other in occurrences[1:]:
                    if first[1] != other[1]:
                        exact_text_count += 1
                        leakage_pairs.append(
                            LeakagePair(
                                email_id_1=first[0],
                                split_1=first[1],
                                email_id_2=other[0],
                                split_2=other[1],
                                leak_type="exact_text",
                                similarity=1.0,
                            )
                        )

        # Check exact image cross-split duplicates
        for _imghash, occurrences in raw_img_hashes.items():
            splits_seen = set(sp for _, sp in occurrences)
            if len(splits_seen) > 1:
                first = occurrences[0]
                for other in occurrences[1:]:
                    if first[1] != other[1]:
                        exact_img_count += 1
                        leakage_pairs.append(
                            LeakagePair(
                                email_id_1=first[0],
                                split_1=first[1],
                                email_id_2=other[0],
                                split_2=other[1],
                                leak_type="exact_image",
                                similarity=1.0,
                            )
                        )

        # Check perceptual image cross-split duplicates
        for _ah, occurrences in ahash_map.items():
            splits_seen = set(sp for _, sp in occurrences)
            if len(splits_seen) > 1:
                first = occurrences[0]
                for other in occurrences[1:]:
                    if first[1] != other[1]:
                        perceptual_img_count += 1
                        leakage_pairs.append(
                            LeakagePair(
                                email_id_1=first[0],
                                split_1=first[1],
                                email_id_2=other[0],
                                split_2=other[1],
                                leak_type="perceptual_image",
                                similarity=1.0,
                            )
                        )

        # Check near-duplicate text similarity (pairwise sampling for small-to-medium sets)
        max_samples = min(len(record_texts), 500)
        for i in range(max_samples):
            for j in range(i + 1, max_samples):
                id1, sp1, txt1 = record_texts[i]
                id2, sp2, txt2 = record_texts[j]
                if sp1 != sp2:
                    sim = jaccard_similarity_ngrams(txt1, txt2)
                    if sim >= self.jaccard_threshold:
                        near_text_count += 1
                        leakage_pairs.append(
                            LeakagePair(
                                email_id_1=id1,
                                split_1=sp1,
                                email_id_2=id2,
                                split_2=sp2,
                                leak_type="near_text_similarity",
                                similarity=sim,
                            )
                        )

        # Summarize sender/campaign/url overlaps
        shared_senders: dict[str, list[str]] = {}
        shared_campaigns: dict[str, list[str]] = {}
        shared_urls: dict[str, int] = {}

        all_splits = list(splits_count.keys())
        for i in range(len(all_splits)):
            for j in range(i + 1, len(all_splits)):
                s1, s2 = all_splits[i], all_splits[j]
                pair_name = f"{s1}_vs_{s2}"

                snd_overlap = list(sender_map.get(s1, set()).intersection(sender_map.get(s2, set())))
                if snd_overlap:
                    shared_senders[pair_name] = snd_overlap

                cmp_overlap = list(campaign_map.get(s1, set()).intersection(campaign_map.get(s2, set())))
                if cmp_overlap:
                    shared_campaigns[pair_name] = cmp_overlap

                url_overlap = url_map.get(s1, set()).intersection(url_map.get(s2, set()))
                if url_overlap:
                    shared_urls[pair_name] = len(url_overlap)

        return LeakageReport(
            total_records=len(records),
            splits=splits_count,
            exact_text_duplicates_cross_split=exact_text_count,
            exact_image_duplicates_cross_split=exact_img_count,
            perceptual_image_duplicates_cross_split=perceptual_img_count,
            near_text_duplicates_cross_split=near_text_count,
            leakage_pairs=leakage_pairs,
            overlap_summary=OverlapSummary(
                shared_senders=shared_senders,
                shared_campaigns=shared_campaigns,
                shared_urls=shared_urls,
            ),
        )


__all__ = [
    "LeakageAuditor",
    "LeakagePair",
    "LeakageReport",
    "OverlapSummary",
    "compute_image_ahash",
    "compute_sha256",
]

"""Demo Inference Engine for DCAT Research Demonstrator.

Provides a pluggable inference interface (:class:`InferenceEngine`) and a
deterministic, heuristic implementation (:class:`DemoInferenceEngine`).

IMPORTANT RESEARCH SAFEGUARD:
This engine generates SIMULATED demonstration probabilities and illustrative
cross-modal token interactions for presentation to non-technical reviewers.
It explicitly tags all outputs with `is_demo_simulation=True` and does NOT
claim to represent trained neural model weights.

When trained DistilBERT, MobileViT, and DCAT weights are available in Phase 2/3,
a `DCATInferenceEngine` will replace this class without requiring any changes to
the frontend or preprocessing pipelines.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

from dcat.data import EmailRecord, Modality, ParserOutput
from dcat.preprocessing.router import RoutedEmailResult


@dataclass(frozen=True)
class PipelineStep:
    """Status of a single model component in the execution pipeline."""

    name: str
    status: str  # "executed" | "skipped"
    description: str


@dataclass(frozen=True)
class CrossAttentionTokenPair:
    """Illustrative cross-modal token interaction for visualization."""

    text_token: str
    image_token: str
    strength: float  # 0.0 to 1.0


@dataclass(frozen=True)
class InferenceResult:
    """Structure returned by InferenceEngine.analyze()."""

    email_id: str
    modality: str
    has_text: bool
    has_meaningful_image: bool
    text_length: int
    image_count: int
    filtered_image_count: int
    pipeline_steps: tuple[PipelineStep, ...]
    simulated_spam_probability: float
    simulated_label: str  # "SPAM" | "LEGITIMATE"
    detected_signals: dict[str, tuple[str, ...]]
    cross_attention_pairs: tuple[CrossAttentionTokenPair, ...]
    explanation: str
    computation_saved_description: str
    is_demo_simulation: bool = True

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["pipeline_steps"] = [asdict(s) for s in self.pipeline_steps]
        data["cross_attention_pairs"] = [asdict(p) for p in self.cross_attention_pairs]
        return data


class InferenceEngine(ABC):
    """Abstract interface for DCAT inference engines."""

    @abstractmethod
    def analyze(
        self,
        parser_output: ParserOutput,
        routed_result: RoutedEmailResult,
    ) -> InferenceResult:
        """Analyze a preprocessed email and produce an InferenceResult."""
        pass


class DemoInferenceEngine(InferenceEngine):
    """Deterministic, heuristic demonstration engine for research concept presentation."""

    # Suspicious keywords for text analysis
    _SUSPICIOUS_TEXT_PATTERNS = (
        (r"\burgent\b", "urgent language"),
        (r"\bverify\b|\bverification\b", "account verification request"),
        (r"\bsuspend\b|\bsuspended\b", "account suspension threat"),
        (r"\bclaim\b|\bwinner\b|\bprize\b", "promotional prize claim"),
        (r"\b\$[0-9,]+\b|\b[0-9,]+\s*dollars?\b", "financial incentive"),
        (r"\bclick here\b|\blogin now\b", "call-to-action link"),
        (r"\bpassword\b|\bcredentials?\b", "credential prompt"),
    )

    def analyze(
        self,
        parser_output: ParserOutput,
        routed_result: RoutedEmailResult,
    ) -> InferenceResult:
        record = routed_result.record
        text_body = (record.text or "") + " " + (record.subject or "")

        # 1. Evaluate pipeline step execution/skipping based on Modality
        steps = self._determine_pipeline_steps(record.modality)

        # 2. Extract text signals
        text_signals: list[str] = []
        text_score_add = 0.0
        for pattern, label in self._SUSPICIOUS_TEXT_PATTERNS:
            if re.search(pattern, text_body, re.IGNORECASE):
                text_signals.append(label)
                text_score_add += 0.22

        # 3. Extract image signals
        image_signals: list[str] = []
        image_score_add = 0.0
        if record.has_meaningful_image:
            # Check if text or raw image metadata suggests suspicious promo/phishing
            if any(
                term in text_body.lower() for term in ("verify", "claim", "winner", "$", "urgent", "login")
            ):
                image_signals.append("visual promotional/phishing banner")
                image_score_add += 0.35
            else:
                image_signals.append("standard inline image")
                image_score_add += 0.05

        # 4. Cross-modal signals & illustrative token pairs
        cross_signals: list[str] = []
        cross_pairs: list[CrossAttentionTokenPair] = []

        if record.modality is Modality.MULTIMODAL:
            if text_signals and image_signals:
                cross_signals.append("visual content reinforces suspicious text signals")
                image_score_add += 0.15
                cross_pairs = [
                    CrossAttentionTokenPair("verify", "CLICK NOW", 0.92),
                    CrossAttentionTokenPair("account", "WARNING", 0.88),
                    CrossAttentionTokenPair("claim", "$5,000", 0.95),
                ]
            else:
                cross_signals.append("cross-modal alignment analyzed")
                cross_pairs = [
                    CrossAttentionTokenPair("meeting", "calendar_icon", 0.75),
                    CrossAttentionTokenPair("schedule", "time_banner", 0.68),
                ]

        # 5. Compute simulated probability
        base_prob = 0.08  # Baseline ham probability
        sim_prob = min(0.98, max(0.04, base_prob + text_score_add + image_score_add))

        sim_label = "SPAM" if sim_prob >= 0.50 else "LEGITIMATE"

        # 6. Generate explanation & computation comparison
        explanation, comp_saved = self._generate_explanations(record, text_signals, image_signals)

        return InferenceResult(
            email_id=record.email_id,
            modality=record.modality.value,
            has_text=record.has_text,
            has_meaningful_image=record.has_meaningful_image,
            text_length=len(record.text or ""),
            image_count=len(record.images),
            filtered_image_count=sum(1 for i in record.images if i.filtered),
            pipeline_steps=tuple(steps),
            simulated_spam_probability=round(sim_prob, 2),
            simulated_label=sim_label,
            detected_signals={
                "text": tuple(text_signals) if text_signals else ("clean text phrasing",),
                "image": tuple(image_signals) if image_signals else ("no meaningful image",),
                "crossmodal": tuple(cross_signals) if cross_signals else ("N/A (unimodal route)",),
            },
            cross_attention_pairs=tuple(cross_pairs),
            explanation=explanation,
            computation_saved_description=comp_saved,
            is_demo_simulation=True,
        )

    def _determine_pipeline_steps(self, modality: Modality) -> list[PipelineStep]:
        steps = [
            PipelineStep("MIME Preprocessing", "executed", "Parsed headers, MIME tree, bodies & attachments"),
            PipelineStep(
                "Modality Router", "executed", f"Content-based threshold routing -> {modality.value.upper()}"
            ),
        ]

        if modality in (Modality.TEXT, Modality.MULTIMODAL):
            steps.append(
                PipelineStep(
                    "DistilBERT Text Encoder", "executed", "Token hidden-state extraction [B, T, 768]"
                )
            )
        else:
            steps.append(
                PipelineStep("DistilBERT Text Encoder", "skipped", "Text absent: text encoder bypassed")
            )

        if modality in (Modality.IMAGE, Modality.MULTIMODAL):
            steps.append(
                PipelineStep("MobileViT Vision Encoder", "executed", "Spatial token extraction [B, V, Dv]")
            )
        else:
            steps.append(
                PipelineStep("MobileViT Vision Encoder", "skipped", "Image absent: vision encoder bypassed")
            )

        if modality is Modality.MULTIMODAL:
            steps.append(
                PipelineStep(
                    "Bidirectional Cross-Attention",
                    "executed",
                    "2-layer bidirectional text<->vision interaction",
                )
            )
        else:
            steps.append(
                PipelineStep(
                    "Bidirectional Cross-Attention", "skipped", "Unimodal route: cross-attention bypassed"
                )
            )

        steps.append(
            PipelineStep("Shared Classifier Head", "executed", "Final classification vector -> probability")
        )

        return steps

    def _generate_explanations(
        self,
        record: EmailRecord,
        text_signals: list[str],
        image_signals: list[str],
    ) -> tuple[str, str]:
        if record.modality is Modality.TEXT:
            expl = (
                "No meaningful image was detected (or images were small tracking pixels), so the MobileViT vision "
                "encoder and cross-attention layers were completely bypassed."
            )
            comp = "Vision processing & cross-attention avoided for this email."
        elif record.modality is Modality.IMAGE:
            expl = (
                "No meaningful text was detected, so the DistilBERT text encoder and cross-attention layers "
                "were completely bypassed."
            )
            comp = "Text processing & cross-attention avoided for this email."
        elif record.modality is Modality.MULTIMODAL:
            expl = (
                "Both meaningful text and image content were detected. DistilBERT and MobileViT were both executed, "
                "and features interacted through 2-layer bidirectional cross-attention."
            )
            comp = "Full multimodal processing active (both encoders + cross-attention)."
        else:  # EMPTY
            expl = "Neither meaningful text nor meaningful images were found. Computation bypassed."
            comp = "All neural encoders bypassed."

        return expl, comp


__all__ = [
    "CrossAttentionTokenPair",
    "DemoInferenceEngine",
    "InferenceEngine",
    "InferenceResult",
    "PipelineStep",
]

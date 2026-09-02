"""Unit tests for DemoInferenceEngine and server scenarios."""

from __future__ import annotations

from dcat.data import ImageDisposition, ParserOutput, RawImage
from dcat.demo.engine import DemoInferenceEngine
from dcat.demo.server import BUILTIN_SCENARIOS
from dcat.preprocessing.router import ModalityRouter


def test_demo_engine_text_only_route():
    po = ParserOutput(
        email_id="demo_t1",
        subject="Meeting confirmation",
        text="Your meeting is confirmed for tomorrow at 10:00 AM.",
        images=(),
    )
    router = ModalityRouter()
    routed = router.route(po)

    engine = DemoInferenceEngine()
    result = engine.analyze(po, routed)

    assert result.modality == "text"
    assert result.has_text is True
    assert result.has_meaningful_image is False
    assert result.simulated_label == "LEGITIMATE"
    assert result.is_demo_simulation is True

    # MobileViT & Cross-Attention must be marked skipped
    steps = {s.name: s.status for s in result.pipeline_steps}
    assert steps["DistilBERT Text Encoder"] == "executed"
    assert steps["MobileViT Vision Encoder"] == "skipped"
    assert steps["Bidirectional Cross-Attention"] == "skipped"


def test_demo_engine_multimodal_route():
    from dcat.demo.server import _generate_synthetic_image

    img_bytes = _generate_synthetic_image("TEST BANNER")
    raw_img = RawImage(
        image_id="demo_img1",
        data=img_bytes,
        content_type="image/png",
        disposition=ImageDisposition.ATTACHMENT,
    )
    po = ParserOutput(
        email_id="demo_mm1",
        subject="URGENT: Financial Claim Pending $5,000",
        text="Your claim of $5,000 is ready for immediate withdrawal. Enter your password and credentials now.",
        images=(raw_img,),
    )
    # Use router config with low min_image_bytes for synthetic test
    from dcat.preprocessing.router import RouterConfig

    router = ModalityRouter(config=RouterConfig(min_image_bytes=10))
    routed = router.route(po)

    engine = DemoInferenceEngine()
    result = engine.analyze(po, routed)

    assert result.modality == "multimodal"
    assert result.simulated_label == "SPAM"
    assert result.simulated_spam_probability >= 0.50
    assert len(result.cross_attention_pairs) > 0

    steps = {s.name: s.status for s in result.pipeline_steps}
    assert steps["DistilBERT Text Encoder"] == "executed"
    assert steps["MobileViT Vision Encoder"] == "executed"
    assert steps["Bidirectional Cross-Attention"] == "executed"


def test_builtin_scenarios_exist():
    assert len(BUILTIN_SCENARIOS) == 4
    for scenario in BUILTIN_SCENARIOS:
        assert "id" in scenario
        assert "subject" in scenario
        assert "expected_route" in scenario

"""Lightweight REST server connecting real Phase 1 preprocessing to the demo UI.

Uses Python standard library `http.server` to expose JSON API endpoints:
- GET /api/scenarios: returns built-in demo scenarios.
- POST /api/analyze: accepts email inputs, runs REAL Phase 1 parsing & routing,
  and returns DemoInferenceResult.
- GET /api/health: healthcheck endpoint.

Usage:
    python -m dcat.demo.server [--port 8000]
"""

from __future__ import annotations

import base64
import io
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from PIL import Image, ImageDraw

from dcat.data import ImageDisposition, ParserOutput, RawImage
from dcat.demo.engine import DemoInferenceEngine
from dcat.preprocessing import ModalityRouter

logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(message)s")
logger = logging.getLogger("dcat.demo.server")


def _generate_synthetic_image(text: str, bg_color: str = "#DC2626", fg_color: str = "#FFFFFF") -> bytes:
    """Generate a synthetic promotional/phishing banner image with text."""
    img = Image.new("RGB", (400, 150), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Simple centered text draw
    draw.rectangle([10, 10, 390, 140], outline=fg_color, width=3)
    draw.text((30, 60), text, fill=fg_color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


_SYNTHETIC_PROMO_IMAGE_B64 = base64.b64encode(_generate_synthetic_image("CLAIM $5,000 NOW!")).decode("ascii")
_SYNTHETIC_CALENDAR_IMAGE_B64 = base64.b64encode(
    _generate_synthetic_image("Calendar Event", bg_color="#2563EB")
).decode("ascii")


BUILTIN_SCENARIOS = [
    {
        "id": "scenario_1",
        "title": "Scenario 1 — Legitimate Text Only",
        "subtitle": "Meeting Confirmation",
        "sender": "colleague@company.com",
        "subject": "Meeting confirmation",
        "body": "Your meeting is confirmed for tomorrow at 10:00 AM.",
        "image_b64": None,
        "expected_route": "TEXT ONLY",
    },
    {
        "id": "scenario_2",
        "title": "Scenario 2 — Suspicious Text Only",
        "subtitle": "Urgent Account Suspension Threat",
        "sender": "security-alert@example.com",
        "subject": "URGENT: Verify your account",
        "body": "Your account will be suspended unless you verify your account immediately. Click login now.",
        "image_b64": None,
        "expected_route": "TEXT ONLY",
    },
    {
        "id": "scenario_3",
        "title": "Scenario 3 — Text + Suspicious Image",
        "subtitle": "Benign Text Phrasing + Promotional Banner Image",
        "sender": "rewards-notice@promo-site.com",
        "subject": "Your account status update",
        "body": "Your account has been successfully verified. Please see the attached image for your notice.",
        "image_b64": _SYNTHETIC_PROMO_IMAGE_B64,
        "expected_route": "MULTIMODAL",
    },
    {
        "id": "scenario_4",
        "title": "Scenario 4 — Suspicious Text + Image",
        "subtitle": "Urgent Text + Promotional CTA Banner",
        "sender": "claims-department@financial-win.org",
        "subject": "URGENT: Financial Claim Pending $5,000",
        "body": "Your claim of $5,000 is ready for immediate withdrawal. Enter your password and credentials now.",
        "image_b64": _SYNTHETIC_PROMO_IMAGE_B64,
        "expected_route": "MULTIMODAL",
    },
]


class DemoApiHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for DCAT Demo API."""

    def _set_headers(self, status: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._set_headers(200)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/api/scenarios", "/api/scenarios/"):
            self._set_headers(200)
            self.wfile.write(json.dumps({"scenarios": BUILTIN_SCENARIOS}).encode("utf-8"))
        elif self.path in ("/api/health", "/api/health/"):
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "ok", "version": "0.1.0"}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "not found"}).encode("utf-8"))

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in ("/api/analyze", "/api/analyze/"):
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "not found"}).encode("utf-8"))
            return

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": f"invalid json: {exc}"}).encode("utf-8"))
            return

        # 1. Parse/Construct raw inputs
        sender = payload.get("sender", "")
        subject = payload.get("subject", "")
        body_text = payload.get("body", "")
        image_b64 = payload.get("image_b64")

        images: list[RawImage] = []
        if image_b64:
            try:
                img_data = base64.b64decode(image_b64)
                images.append(
                    RawImage(
                        image_id="demo_upload_img1",
                        data=img_data,
                        content_type="image/png",
                        disposition=ImageDisposition.ATTACHMENT,
                        filename="attached_image.png",
                    )
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to decode image_b64: %s", exc)

        # Build ParserOutput using real Phase 1 dataclass
        parser_output = ParserOutput(
            email_id=f"demo_{str(abs(hash(body_text + subject)))[:8]}",
            subject=subject or None,
            text=body_text or None,
            html=f"<html><body><p>{body_text}</p></body></html>" if body_text else None,
            images=tuple(images),
            metadata={"from": sender},
        )

        # 2. Run REAL Phase 1 Modality Router & Image Preprocessor
        router = ModalityRouter()
        routed_result = router.route(
            parser_output,
            sender_hash=sender,
        )

        # 3. Run Demo Inference Engine
        engine = DemoInferenceEngine()
        result = engine.analyze(parser_output, routed_result)

        self._set_headers(200)
        self.wfile.write(json.dumps(result.to_dict()).encode("utf-8"))


def run_server(port: int = 8000) -> None:
    server_address = ("", port)
    httpd = HTTPServer(server_address, DemoApiHandler)
    logger.info("DCAT Demo API server listening on http://localhost:%d", port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped.")
        httpd.server_close()


if __name__ == "__main__":
    import sys

    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)

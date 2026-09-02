"""Deterministic MIME parser for DCAT.

Extracts, from a raw ``.eml`` / MIME message:

- subject (RFC 2047-encoded-word aware)
- plain-text body (text/plain preferred)
- raw HTML body (text/html)
- inline / CID / attachment images (as transient :class:`RawImage`)
- selected metadata headers
- non-fatal parsing issues

Design constraints:

- Uses only the Python standard library (``email``) — no ML deps.
- Deterministic: same bytes in, same :class:`ParserOutput` out.
- Bounded: configurable size limits prevent pathological messages from
  exhausting memory. Oversized messages raise :class:`ParserLimitError`; an
  oversized *part* within an in-range message is skipped and recorded.
- Safe: content is parsed as data only. Scripts, macros and JavaScript in the
  HTML are never executed; they are simply part of the extracted raw HTML.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from email import policy
from email.header import decode_header
from email.parser import BytesParser
from email.policy import Policy
from email.utils import parseaddr
from typing import Any

from dcat.data import ImageDisposition, ParserOutput, RawImage

# Content types we treat as in-message images.
_IMAGE_MAIN_TYPES = frozenset({"image"})

# Content-transfer-encodings and their decoded-size expansion ratios
# (upper bounds used to refuse decoding before allocating).
_TRANSFER_ENCODING_MULTIPLIERS = {
    "base64": 3 / 4 + 0.01,  # base64 expands decoded payload by ~4/3
    "quoted-printable": 1.0,
    "7bit": 1.0,
    "8bit": 1.0,
    "binary": 1.0,
}


class ParserLimitError(RuntimeError):
    """Raised when a raw message exceeds the configured hard size limit."""


class MimeParseError(RuntimeError):
    """Raised for a fatal inability to parse a message."""


@dataclass(frozen=True)
class ParserLimits:
    """Resource bounds for MIME parsing. All values are in bytes unless noted."""

    max_message_bytes: int = 52_428_800  # 50 MiB
    max_part_bytes: int = 10_485_760  # 10 MiB
    max_images: int = 32
    max_text_chars: int = 1_000_000
    max_depth: int = 32

    def __post_init__(self) -> None:
        if self.max_message_bytes <= 0 or self.max_part_bytes <= 0:
            raise ValueError("parser size limits must be positive")
        if self.max_images <= 0:
            raise ValueError("max_images must be positive")
        if self.max_depth <= 0:
            raise ValueError("max_depth must be positive")


@dataclass
class ParsedMessage:
    """Internal mutable accumulation while walking the MIME tree."""

    email_id: str
    subject: str | None = None
    text_parts: list[str] = field(default_factory=list)
    html_parts: list[tuple[str, int]] = field(default_factory=list)  # (html, size_chars)
    images: list[RawImage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def _decode_part_text(part: Any, limits: ParserLimits) -> tuple[str, str | None]:
    """Decode a leaf part's payload to text.

    Returns ``(text, error)`` where ``error`` is None on success or a short
    description when the declared charset could not be honored strictly.
    """
    charset = part.get_content_charset() or "utf-8"
    raw = part.get_payload(decode=True)
    if raw is None:
        # Non-encoded text body parsed from str — use as-is.
        payload = part.get_payload(decode=False)
        text = payload if isinstance(payload, str) else payload.decode(charset, errors="replace")
        return text[: limits.max_text_chars], None
    try:
        text = raw.decode(charset if charset.lower() not in {"", "unknown-8bit"} else "utf-8")
    except (LookupError, UnicodeDecodeError):
        # Unknown or invalid charset: fall back to UTF-8 with replacement so the
        # pipeline stays deterministic, but record the event.
        text = raw.decode("utf-8", errors="replace")
        return text[: limits.max_text_chars], f"charset_decode_fallback:{charset}"
    return text[: limits.max_text_chars], None


def _decode_subject(value: str | None) -> str | None:
    if not value:
        return None
    pieces: list[str] = []
    try:
        for data, charset in decode_header(value):
            if isinstance(data, bytes):
                cs = charset or "utf-8"
                try:
                    pieces.append(data.decode(cs))
                except (LookupError, UnicodeDecodeError):
                    pieces.append(data.decode("utf-8", errors="replace"))
            else:
                pieces.append(str(data))
    except Exception:  # noqa: BLE001 - survive pathological header encodings
        return str(value)
    subject = "".join(pieces).strip()
    return subject or None


def _collect_addresses(headers: list[Any]) -> list[str]:
    """Extract address strings from raw header values."""
    addrs: list[str] = []
    for val in headers:
        _, addr = parseaddr(str(val))
        if addr:
            addrs.append(addr)
    return addrs


def _payload_size_estimate(part: Any) -> int:
    """Upper-bound estimate of a leaf part's decoded payload size in bytes.

    Uses the content-transfer-encoding multiplier so we can refuse to decode a
    part before allocating a large buffer.
    """
    raw = part.get_payload(decode=False)
    if raw is None:
        return 0
    if isinstance(raw, bytes):
        size = len(raw)
    else:
        size = len(raw.encode("utf-8", "surrogatepass"))
    cte = (part.get("Content-Transfer-Encoding") or "7bit").strip().lower()
    multiplier = _TRANSFER_ENCODING_MULTIPLIERS.get(cte, 1.0)
    return int(size * multiplier) + 1


def _image_id(email_id: str, index: int, part: Any) -> str:
    """Deterministic, collision-resistant image id for a part."""
    key = part.get("Content-ID") or part.get_filename() or f"part-{index}"
    digest = hashlib.sha1(f"{email_id}::{index}::{key}".encode("utf-8", "replace")).hexdigest()[:12]
    return f"{email_id}__img{index}_{digest}"


def _extract_image(email_id: str, index: int, part: Any) -> RawImage:
    data = part.get_payload(decode=True)
    content_type = part.get_content_type()
    disposition = part.get_content_disposition() or "unknown"
    disp = {
        "inline": ImageDisposition.INLINE,
        "attachment": ImageDisposition.ATTACHMENT,
        "unknown": ImageDisposition.UNKNOWN,
    }.get(disposition.lower(), ImageDisposition.UNKNOWN)
    cid = (part.get("Content-ID") or "").strip()
    if cid.startswith("<") and cid.endswith(">"):
        cid = cid[1:-1]
    return RawImage(
        image_id=_image_id(email_id, index, part),
        data=data or b"",
        content_type=content_type,
        disposition=disp,
        cid=cid or None,
        filename=part.get_filename(),
    )


class MimeParser:
    """Deterministic, bounded MIME→:class:`ParserOutput` extraction."""

    def __init__(self, limits: ParserLimits | None = None, policy: Policy = policy.default) -> None:
        self.limits = limits or ParserLimits()
        self._parser = BytesParser(policy=policy)

    # -- public API --------------------------------------------------------

    def parse_bytes(self, data: bytes, email_id: str | None = None) -> ParserOutput:
        """Parse raw MIME bytes into a :class:`ParserOutput`.

        Raises:
            ParserLimitError: if the message is larger than ``max_message_bytes``.
            MimeParseError: if the bytes cannot be parsed at all.
        """
        if len(data) > self.limits.max_message_bytes:
            raise ParserLimitError(
                f"message {len(data)} bytes exceeds max_message_bytes={self.limits.max_message_bytes}"
            )
        try:
            msg = self._parser.parsebytes(data)
        except Exception as exc:  # noqa: BLE001 - pathological bytes
            raise MimeParseError(f"could not parse message: {exc}") from exc
        acc = ParsedMessage(email_id=email_id or _message_id(msg))
        self._extract_root_meta(msg, acc)
        self._walk(msg, acc, depth=0)
        return self._finalize(acc)

    def parse_file(self, path: str, email_id: str | None = None) -> ParserOutput:
        """Parse a raw ``.eml`` file from disk with the same size protection."""
        import os

        size = os.path.getsize(path)
        if size > self.limits.max_message_bytes:
            raise ParserLimitError(
                f"file {size} bytes exceeds max_message_bytes={self.limits.max_message_bytes}"
            )
        with open(path, "rb") as fh:
            return self.parse_bytes(fh.read(), email_id=email_id or _basename_id(path))

    # -- internals ---------------------------------------------------------

    def _extract_root_meta(self, msg: Any, acc: ParsedMessage) -> None:
        """Pull deterministic root headers into the accumulation object."""
        acc.subject = _decode_subject(msg.get("Subject"))
        from_name, from_addr = parseaddr(msg.get("From") or "")
        to_addrs = _collect_addresses(msg.get_all("To") or [])
        cc_addrs = _collect_addresses(msg.get_all("Cc") or [])
        acc.metadata = {
            "from": from_addr or None,
            "from_name": from_name or None,
            "to": to_addrs,
            "cc": cc_addrs,
            "date": msg.get("Date") or None,
            "message_id": msg.get("Message-ID") or None,
            "in_reply_to": msg.get("In-Reply-To") or None,
            "received_count": len(msg.get_all("Received") or []),
        }

    def _walk(self, msg: Any, acc: ParsedMessage, depth: int = 0) -> None:
        if depth > self.limits.max_depth:
            acc.errors.append(f"max_depth_exceeded:{depth}")
            return

        if msg.is_multipart():
            for child in msg.iter_parts():
                self._walk(child, acc, depth=depth + 1)
            return

        maintype = msg.get_content_maintype()
        if maintype in _IMAGE_MAIN_TYPES:
            self._handle_image_part(msg, acc)
            return

        ctype = msg.get_content_type()
        if ctype == "text/plain":
            text, err = _decode_part_text(msg, self.limits)
            if err:
                acc.errors.append(f"part:{msg.get_content_type()}:{err}")
            if text:
                acc.text_parts.append(text)
        elif ctype == "text/html":
            text, err = _decode_part_text(msg, self.limits)
            if err:
                acc.errors.append(f"part:{msg.get_content_type()}:{err}")
            if text:
                acc.html_parts.append((text, len(text)))

    def _handle_image_part(self, msg: Any, acc: ParsedMessage) -> None:
        if len(acc.images) >= self.limits.max_images:
            acc.errors.append(f"too_many_images:skipped:{msg.get_content_type()}")
            return
        if _payload_size_estimate(msg) > self.limits.max_part_bytes:
            acc.errors.append(
                f"part:{msg.get_content_type()}:decoded_size_exceeds_limit:{self.limits.max_part_bytes}"
            )
            return
        try:
            raw = _extract_image(acc.email_id, len(acc.images), msg)
        except Exception as exc:  # noqa: BLE001 - keep pipeline alive on bad parts
            acc.errors.append(f"image_extract:{type(exc).__name__}")
            return
        if raw.data:
            acc.images.append(raw)

    def _finalize(self, acc: ParsedMessage) -> ParserOutput:
        text = "\n\n".join(acc.text_parts) or None
        html: str | None = None
        if acc.html_parts:
            # Preserve all HTML parts combined
            html = "\n\n".join(part[0] for part in acc.html_parts)

        # Fallback: if plaintext is absent but HTML exists, extract visible text
        if not text and html:
            from dcat.preprocessing.html_processor import HtmlProcessor

            hp = HtmlProcessor(max_html_chars=self.limits.max_text_chars)
            res = hp.process(html)
            text = res.visible_text

        return ParserOutput(
            email_id=acc.email_id,
            subject=acc.subject,
            text=text,
            html=html,
            images=tuple(acc.images),
            metadata=dict(acc.metadata),
            errors=tuple(acc.errors),
        )


def _message_id(msg: Any) -> str:
    value = msg.get("Message-ID")
    if not value:
        return hashlib.sha1(str(msg).encode("utf-8", "replace")).hexdigest()
    return value.strip()


def _basename_id(path: str) -> str:
    import os

    return os.path.splitext(os.path.basename(path))[0]

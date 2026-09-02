"""Safe, offline HTML processing for DCAT emails.

Extracts:
- visible text (stripping scripts, styles, metadata tags)
- link information (href, link text, title)
- CID image references (from src, background, and inline styles)

Design constraints:
- Strictly offline: never fetches external URLs or resources.
- Safe: never executes scripts or macros.
- Bounded: defensive against malformed, deeply nested, or oversized HTML inputs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from html import unescape

from bs4 import BeautifulSoup, Comment


@dataclass(frozen=True)
class ExtractedLink:
    """Structure representing a hyperlink extracted from HTML."""

    href: str
    text: str | None = None
    title: str | None = None


@dataclass(frozen=True)
class HtmlProcessResult:
    """Result of processing an HTML string."""

    visible_text: str | None
    links: tuple[ExtractedLink, ...] = ()
    cid_references: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


class HtmlProcessor:
    """Offline, defensive HTML parser and feature extractor."""

    _UNWANTED_TAGS = frozenset(
        {
            "script",
            "style",
            "head",
            "title",
            "meta",
            "[document]",
            "noscript",
            "template",
            "link",
        }
    )

    # Pattern to match url(cid:...) or url('cid:...') in CSS / inline styles
    _CID_CSS_PATTERN = re.compile(r"url\(\s*['\"]?cid:([^'\")\s]+)['\"]?\s*\)", re.IGNORECASE)

    def __init__(self, max_html_chars: int = 2_000_000) -> None:
        self.max_html_chars = max_html_chars

    def process(self, html_content: str | None) -> HtmlProcessResult:
        """Process an HTML string safely and extract text, links, and CIDs.

        Args:
            html_content: raw HTML string (or None).

        Returns:
            HtmlProcessResult containing visible text, links, CIDs, and errors.
        """
        if not html_content or not html_content.strip():
            return HtmlProcessResult(visible_text=None)

        errors: list[str] = []
        truncated_html = html_content[: self.max_html_chars]
        if len(html_content) > self.max_html_chars:
            errors.append(f"html_truncated:{len(html_content)}_exceeds_{self.max_html_chars}")

        # Try lxml parser first for performance, fall back to standard html.parser
        soup = None
        for parser in ("lxml", "html.parser"):
            try:
                soup = BeautifulSoup(truncated_html, parser)
                break
            except Exception as exc:  # noqa: BLE001
                errors.append(f"parser_fallback:{parser}:{type(exc).__name__}")

        if soup is None:
            return HtmlProcessResult(
                visible_text=None,
                errors=tuple(errors + ["html_parse_failed"]),
            )

        # 1. Extract CIDs before modifying the tree
        cids = self._extract_cids(soup, truncated_html)

        # 2. Extract links
        links = self._extract_links(soup)

        # 3. Extract visible text (strip unwanted tags & comments)
        visible_text = self._extract_visible_text(soup)

        return HtmlProcessResult(
            visible_text=visible_text or None,
            links=tuple(links),
            cid_references=tuple(cids),
            errors=tuple(errors),
        )

    def _extract_cids(self, soup: BeautifulSoup, raw_html: str) -> list[str]:
        cids: list[str] = []
        seen: set[str] = set()

        def _add_cid(val: str | None) -> None:
            if not val:
                return
            val = val.strip()
            if val.lower().startswith("cid:"):
                val = val[4:]
            if val.startswith("<") and val.endswith(">"):
                val = val[1:-1]
            if val and val not in seen:
                seen.add(val)
                cids.append(val)

        # Attributes that may carry cid: references
        for tag in soup.find_all(True):
            for attr in ("src", "background", "data-src", "poster"):
                val = tag.get(attr)
                if isinstance(val, str) and "cid:" in val.lower():
                    _add_cid(val)
            # Inline styles
            style_val = tag.get("style")
            if isinstance(style_val, str) and "cid:" in style_val.lower():
                for match in self._CID_CSS_PATTERN.finditer(style_val):
                    _add_cid(match.group(1))

        # Also regex sweep raw HTML for any missed CSS url(cid:...) references
        for match in self._CID_CSS_PATTERN.finditer(raw_html):
            _add_cid(match.group(1))

        return cids

    def _extract_links(self, soup: BeautifulSoup) -> list[ExtractedLink]:
        links: list[ExtractedLink] = []
        for anchor in soup.find_all("a", href=True):
            href = str(anchor["href"]).strip()
            if not href:
                continue
            text = anchor.get_text(strip=True) or None
            title = anchor.get("title")
            links.append(
                ExtractedLink(
                    href=href,
                    text=text,
                    title=str(title).strip() if title else None,
                )
            )
        return links

    def _extract_visible_text(self, soup: BeautifulSoup) -> str | None:
        # Create a deep copy to avoid destroying original tree if reused
        try:
            tree = BeautifulSoup(str(soup), "html.parser")
        except Exception:  # noqa: BLE001
            tree = soup

        # Remove comments
        for comment in tree.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Remove unwanted tags
        for element in tree.find_all(self._UNWANTED_TAGS):
            element.decompose()

        # Insert newlines before/after block-level elements
        block_tags = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "br", "hr", "blockquote"}
        for tag in tree.find_all(block_tags):
            tag.insert_before("\n")
            tag.insert_after("\n")

        text = tree.get_text(separator=" ")
        # Normalize whitespace line by line
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
        # Remove empty lines while preserving paragraph separation
        non_empty = [line for line in lines if line]
        cleaned = "\n\n".join(non_empty).strip()
        return unescape(cleaned) if cleaned else None


__all__ = ["ExtractedLink", "HtmlProcessResult", "HtmlProcessor"]

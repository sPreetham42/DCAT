"""Regression tests for MIME parser bugs identified during audit."""

from __future__ import annotations

from dcat.preprocessing.mime_parser import MimeParser, ParserLimits


def test_mime_parser_max_depth_exceeded():
    """Verify that deeply nested MIME structures do not cause recursion error."""
    parser = MimeParser(limits=ParserLimits(max_depth=3))

    # Build a deeply nested MIME structure (depth = 5)
    raw = (
        b"Content-Type: multipart/mixed; boundary=b0\n\n"
        b"--b0\n"
        b"Content-Type: multipart/mixed; boundary=b1\n\n"
        b"--b1\n"
        b"Content-Type: multipart/mixed; boundary=b2\n\n"
        b"--b2\n"
        b"Content-Type: multipart/mixed; boundary=b3\n\n"
        b"--b3\n"
        b"Content-Type: multipart/mixed; boundary=b4\n\n"
        b"--b4\n"
        b"Content-Type: text/plain\n\n"
        b"Deeply nested text\n"
        b"--b4--\n"
        b"--b3--\n"
        b"--b2--\n"
        b"--b1--\n"
        b"--b0--\n"
    )

    output = parser.parse_bytes(raw, email_id="depth_test")
    assert any("max_depth_exceeded" in err for err in output.errors)


def test_mime_parser_combines_multiple_html_parts():
    """Verify that multiple HTML parts are preserved rather than discarded."""
    parser = MimeParser()
    raw = (
        b"Content-Type: multipart/mixed; boundary=b1\n\n"
        b"--b1\n"
        b"Content-Type: text/html\n\n"
        b"<p>HTML Part 1</p>\n"
        b"--b1\n"
        b"Content-Type: text/html\n\n"
        b"<p>HTML Part 2</p>\n"
        b"--b1--\n"
    )
    output = parser.parse_bytes(raw, email_id="multi_html")
    assert output.html is not None
    assert "<p>HTML Part 1</p>" in output.html
    assert "<p>HTML Part 2</p>" in output.html


def test_mime_parser_html_only_fallback_text():
    """Verify that HTML-only emails produce usable extracted visible text."""
    parser = MimeParser()
    raw = (
        b"Content-Type: text/html; charset=utf-8\n\n"
        b"<html><body><h1>Important Spam Notice</h1><p>Click here immediately!</p></body></html>"
    )
    output = parser.parse_bytes(raw, email_id="html_only")
    assert output.html is not None
    assert output.text is not None
    assert "Important Spam Notice" in output.text
    assert "Click here immediately!" in output.text

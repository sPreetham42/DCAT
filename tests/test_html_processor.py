"""Unit tests for HtmlProcessor."""

from __future__ import annotations

from dcat.preprocessing.html_processor import HtmlProcessor


def test_html_processor_visible_text_extraction():
    processor = HtmlProcessor()
    html = """
    <html>
        <head>
            <title>Title to Ignore</title>
            <style>body { color: red; }</style>
            <script>alert('malicious');</script>
        </head>
        <body>
            <!-- Comment to ignore -->
            <h1>Hello World</h1>
            <p>This is <b>visible</b> text content.</p>
        </body>
    </html>
    """
    res = processor.process(html)
    assert res.visible_text is not None
    assert "Hello World" in res.visible_text
    assert "This is visible text content." in res.visible_text
    assert "alert" not in res.visible_text
    assert "Title to Ignore" not in res.visible_text
    assert "Comment to ignore" not in res.visible_text


def test_html_processor_link_extraction():
    processor = HtmlProcessor()
    html = """
    <html>
        <body>
            <a href="https://example.com/login" title="Login Link">Click Here to Login</a>
            <a href="http://phishing.site">Verify Account</a>
        </body>
    </html>
    """
    res = processor.process(html)
    assert len(res.links) == 2
    assert res.links[0].href == "https://example.com/login"
    assert res.links[0].text == "Click Here to Login"
    assert res.links[0].title == "Login Link"
    assert res.links[1].href == "http://phishing.site"


def test_html_processor_cid_extraction():
    processor = HtmlProcessor()
    html = """
    <html>
        <body>
            <img src="cid:header_logo_123" alt="Logo">
            <div style="background-image: url('cid:bg_banner_456');">Banner</div>
            <img src="https://external.com/tracking.gif">
        </body>
    </html>
    """
    res = processor.process(html)
    assert "header_logo_123" in res.cid_references
    assert "bg_banner_456" in res.cid_references
    assert len(res.cid_references) == 2


def test_html_processor_defensive_truncation():
    processor = HtmlProcessor(max_html_chars=50)
    html = "<html><body>" + "x" * 100 + "</body></html>"
    res = processor.process(html)
    assert any("html_truncated" in err for err in res.errors)

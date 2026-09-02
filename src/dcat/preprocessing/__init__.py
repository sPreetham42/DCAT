"""Preprocessing modules for DCAT email extraction and routing."""

from dcat.preprocessing.html_processor import ExtractedLink, HtmlProcessor, HtmlProcessResult
from dcat.preprocessing.image_processor import ImageProcessor, ImageProcessorConfig, ProcessedImageResult
from dcat.preprocessing.mime_parser import MimeParseError, MimeParser, ParserLimitError, ParserLimits
from dcat.preprocessing.router import ModalityRouter, RoutedEmailResult, RouterConfig

__all__ = [
    "ExtractedLink",
    "HtmlProcessResult",
    "HtmlProcessor",
    "ImageProcessor",
    "ImageProcessorConfig",
    "MimeParseError",
    "MimeParser",
    "ModalityRouter",
    "ParserLimitError",
    "ParserLimits",
    "ProcessedImageResult",
    "RoutedEmailResult",
    "RouterConfig",
]

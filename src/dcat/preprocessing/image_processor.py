"""Image preprocessing and filtering pipeline for DCAT.

Operates on transient :class:`RawImage` objects extracted by the MIME parser:

- Validates binary image headers defensively (Pillow).
- Rejects corrupted images, decompression bombs, and unsupported formats safely.
- Filters tracking pixels / decorative icons against configurable size/dimension thresholds.
- Preserves explicit filter metadata on :class:`ImageRecord`.
- Preprocesses selected meaningful images to normalized PyTorch tensors [3, 224, 224].
"""

from __future__ import annotations

import io
from dataclasses import dataclass
from typing import TYPE_CHECKING

import torch
from PIL import Image, ImageFile

if TYPE_CHECKING:
    from dcat.data import ImageRecord, RawImage

# Allow loading truncated images defensively up to safe limit
ImageFile.LOAD_TRUNCATED_IMAGES = False
# Max image pixels (default ~89 MP to prevent decompression bombs)
Image.MAX_IMAGE_PIXELS = 89_478_485


@dataclass(frozen=True)
class ImageProcessorConfig:
    """Thresholds and target dimensions for image processing."""

    min_image_width: int = 20
    min_image_height: int = 20
    min_image_bytes: int = 1024
    target_size: tuple[int, int] = (224, 224)  # (height, width)
    max_image_pixels: int = 89_478_485

    def __post_init__(self) -> None:
        if self.min_image_width <= 0 or self.min_image_height <= 0:
            raise ValueError("image minimum dimensions must be positive")
        if self.min_image_bytes <= 0:
            raise ValueError("min_image_bytes must be positive")


@dataclass(frozen=True)
class ProcessedImageResult:
    """Outcome of processing a single RawImage."""

    record: ImageRecord
    tensor: torch.Tensor | None = None  # FloatTensor [3, H, W] normalized when selected


class ImageProcessor:
    """Defensive, deterministic image filtering and tensor normalization engine."""

    # ImageNet mean & std for PyTorch vision models
    _IMAGENET_MEAN = (0.485, 0.456, 0.406)
    _IMAGENET_STD = (0.229, 0.224, 0.225)

    def __init__(self, config: ImageProcessorConfig | None = None) -> None:
        self.config = config or ImageProcessorConfig()

    def process_raw_image(
        self,
        raw: RawImage,
        select: bool = False,
    ) -> ProcessedImageResult:
        """Decode, filter, and optionally convert a RawImage into a PyTorch tensor.

        Args:
            raw: the transient RawImage from the MIME parser.
            select: whether this image should be preprocessed to a tensor.

        Returns:
            ProcessedImageResult containing the ImageRecord metadata and optional tensor.
        """
        from dcat.data import ImageRecord

        byte_size = raw.byte_size
        if byte_size < self.config.min_image_bytes:
            rec = ImageRecord(
                image_id=raw.image_id,
                mime_type=raw.content_type,
                byte_size=byte_size,
                cid=raw.cid,
                filtered=True,
                filter_reason=f"byte_size_{byte_size}_below_min_{self.config.min_image_bytes}",
                selected=False,
            )
            return ProcessedImageResult(record=rec, tensor=None)

        try:
            with Image.open(io.BytesIO(raw.data)) as img:
                # Verify header integrity without decoding entire raster
                img.verify()

            # Re-open for actual reading (verify() alters file pointer)
            with Image.open(io.BytesIO(raw.data)) as img:
                width, height = img.size
                mime_type = Image.MIME.get(img.format, raw.content_type)

                # Check dimensions against tracking pixel thresholds
                if width < self.config.min_image_width or height < self.config.min_image_height:
                    rec = ImageRecord(
                        image_id=raw.image_id,
                        mime_type=mime_type,
                        width=width,
                        height=height,
                        byte_size=byte_size,
                        cid=raw.cid,
                        filtered=True,
                        filter_reason=f"dimensions_{width}x{height}_below_min_{self.config.min_image_width}x{self.config.min_image_height}",
                        selected=False,
                    )
                    return ProcessedImageResult(record=rec, tensor=None)

                # Image is meaningful (passed filters)
                tensor: torch.Tensor | None = None
                if select:
                    tensor = self._to_normalized_tensor(img)

                rec = ImageRecord(
                    image_id=raw.image_id,
                    mime_type=mime_type,
                    width=width,
                    height=height,
                    byte_size=byte_size,
                    cid=raw.cid,
                    filtered=False,
                    filter_reason=None,
                    selected=select,
                )
                return ProcessedImageResult(record=rec, tensor=tensor)

        except Image.DecompressionBombError:
            rec = ImageRecord(
                image_id=raw.image_id,
                mime_type=raw.content_type,
                byte_size=byte_size,
                cid=raw.cid,
                filtered=True,
                filter_reason="decompression_bomb_detected",
                selected=False,
            )
            return ProcessedImageResult(record=rec, tensor=None)
        except Exception as exc:  # noqa: BLE001 - catch corrupted/unsupported formats
            rec = ImageRecord(
                image_id=raw.image_id,
                mime_type=raw.content_type,
                byte_size=byte_size,
                cid=raw.cid,
                filtered=True,
                filter_reason=f"decode_error:{type(exc).__name__}",
                selected=False,
            )
            return ProcessedImageResult(record=rec, tensor=None)

    def _to_normalized_tensor(self, img: Image.Image) -> torch.Tensor:
        """Convert a PIL image to a normalized FloatTensor [3, target_h, target_w]."""
        # Convert paletted/RGBA/grayscale to RGB
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize to target size (height, width) with BICUBIC
        target_h, target_w = self.config.target_size
        resized = img.resize((target_w, target_h), resample=Image.Resampling.BICUBIC)

        # Convert to tensor [3, H, W] in range [0.0, 1.0]
        # Pure PyTorch / NumPy conversion without torchvision dependency
        import numpy as np

        arr = np.array(resized, dtype=np.float32) / 255.0  # [H, W, 3]
        tensor = torch.from_numpy(arr).permute(2, 0, 1)  # [3, H, W]

        # Apply ImageNet normalization
        mean = torch.tensor(self._IMAGENET_MEAN, dtype=torch.float32).view(3, 1, 1)
        std = torch.tensor(self._IMAGENET_STD, dtype=torch.float32).view(3, 1, 1)
        return (tensor - mean) / std


__all__ = ["ImageProcessor", "ImageProcessorConfig", "ProcessedImageResult"]

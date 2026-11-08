from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError

from app.exceptions.item import InvalidPhotoError, PhotoTooLargeError


MAX_PHOTO_BYTES = 5 * 1024 * 1024
MAX_PHOTO_PIXELS = 25_000_000

# Long edge of the stored photo. Phone cameras capture far more detail than an
# item listing ever shows, so anything larger is scaled down before storage.
MAX_STORED_EDGE = 1600

JPEG_QUALITY = 85
WEBP_QUALITY = 85

ACCEPTED_FORMATS = frozenset({"JPEG", "PNG", "WEBP"})

CONTENT_TYPES = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
}

# Let Pillow refuse absurd dimensions on its own, before a full decode.
Image.MAX_IMAGE_PIXELS = MAX_PHOTO_PIXELS


def process_photo(image_data: bytes) -> tuple[bytes, str]:
    """Validate photo bytes, scale them down, and return (data, content_type).

    Re-encoding normalises the stored photo and drops EXIF metadata, which on a
    lost-and-found photo can carry the GPS coordinates of where it was taken.
    """
    if not image_data:
        raise InvalidPhotoError("Photo must not be empty.")

    if len(image_data) > MAX_PHOTO_BYTES:
        raise PhotoTooLargeError("Photo must be 5 MiB or smaller.")

    try:
        with Image.open(BytesIO(image_data)) as source:
            source_format = source.format
            if source_format not in ACCEPTED_FORMATS:
                raise InvalidPhotoError("Use a JPEG, PNG, or WebP image.")

            if source.width * source.height > MAX_PHOTO_PIXELS:
                raise InvalidPhotoError("Photo resolution is too large.")

            # Decoding happens here, so a truncated or corrupt file fails below.
            image = ImageOps.exif_transpose(source)
            image.thumbnail(
                (MAX_STORED_EDGE, MAX_STORED_EDGE),
                Image.Resampling.LANCZOS,
            )
            return _encode(image, source_format)
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        SyntaxError,
        Image.DecompressionBombError,
    ) as error:
        raise InvalidPhotoError("Photo is not a valid image.") from error


def _encode(image: Image.Image, source_format: str) -> tuple[bytes, str]:
    """Encode the photo, keeping transparency only when it is actually used.

    A PNG photo without transparency is stored as JPEG, which is dramatically
    smaller for the same picture.
    """
    buffer = BytesIO()

    if source_format == "WEBP":
        target = "WEBP"
    elif _has_alpha(image):
        target = "PNG"
    else:
        target = "JPEG"

    match target:
        case "JPEG":
            image.convert("RGB").save(
                buffer,
                "JPEG",
                quality=JPEG_QUALITY,
                optimize=True,
                progressive=True,
            )
        case "WEBP":
            mode = "RGBA" if _has_alpha(image) else "RGB"
            image.convert(mode).save(buffer, "WEBP", quality=WEBP_QUALITY, method=4)
        case _:
            image.save(buffer, "PNG", optimize=True)

    return buffer.getvalue(), CONTENT_TYPES[target]


def _has_alpha(image: Image.Image) -> bool:
    return image.mode in {"RGBA", "LA", "PA"} or "transparency" in image.info

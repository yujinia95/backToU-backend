from io import BytesIO

from PIL import Image, UnidentifiedImageError

from app.exceptions.item import InvalidPhotoError, PhotoTooLargeError


MAX_PHOTO_BYTES = 5 * 1024 * 1024
MAX_PHOTO_PIXELS = 25_000_000

PHOTO_CONTENT_TYPES = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
}


def validate_photo(image_data: bytes) -> str:
    """Validate image bytes and return the detected content type."""
    if not image_data:
        raise InvalidPhotoError("Photo must not be empty.")

    if len(image_data) > MAX_PHOTO_BYTES:
        raise PhotoTooLargeError("Photo must be 5 MiB or smaller.")

    try:
        with Image.open(BytesIO(image_data)) as image:
            format_name = image.format
            if format_name is None or format_name not in PHOTO_CONTENT_TYPES:
                raise InvalidPhotoError("Use a JPEG, PNG, or WebP image.")

            if image.width * image.height > MAX_PHOTO_PIXELS:
                raise InvalidPhotoError("Photo resolution is too large.")

            content_type = PHOTO_CONTENT_TYPES[format_name]
            image.verify()

        with Image.open(BytesIO(image_data)) as image:
            image.load()
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        SyntaxError,
        Image.DecompressionBombError,
    ) as error:
        raise InvalidPhotoError("Photo is not a valid image.") from error

    return content_type

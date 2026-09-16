from app.api.routes.uploads import (
    ALLOWED_IMAGE_TYPES,
    MAX_IMAGE_SIZE,
)


def test_allowed_image_types():
    assert "image/jpeg" in ALLOWED_IMAGE_TYPES
    assert "image/png" in ALLOWED_IMAGE_TYPES
    assert "image/webp" in ALLOWED_IMAGE_TYPES


def test_max_image_size():
    assert MAX_IMAGE_SIZE == 10 * 1024 * 1024
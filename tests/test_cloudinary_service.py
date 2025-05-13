import pytest
from src.services.image import cloudinary_service
from fastapi import UploadFile
from io import BytesIO
from PIL import Image

@pytest.mark.asyncio
async def test_upload_image():
    # Create a valid in-memory image using Pillow
    image = Image.new("RGB", (100, 100), color="red")
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    file = UploadFile(filename="test.jpg", file=image_bytes)
    url = await cloudinary_service.upload(file, "test@example.com")
    assert url is not None

@pytest.mark.asyncio
async def test_resize_image():
    url = await cloudinary_service.resize("http://example.com/image.jpg", 100, 100, "fit")
    assert "http://example.com/image.jpg" in url
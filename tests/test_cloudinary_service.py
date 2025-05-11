import pytest
from src.services.image import cloudinary_service
from fastapi import UploadFile
from io import BytesIO

@pytest.mark.asyncio
async def test_upload_image():
    file = UploadFile(filename="test.jpg", file=BytesIO(b"fake image data"))
    url = await cloudinary_service.upload(file, "test@example.com")
    assert url is not None

@pytest.mark.asyncio
async def test_resize_image():
    url = await cloudinary_service.resize("http://example.com/image.jpg", 100, 100, "fit")
    assert "http://example.com/image.jpg" in url
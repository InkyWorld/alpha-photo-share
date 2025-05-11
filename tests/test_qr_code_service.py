import pytest
from src.services.qr_code import qrcode_service

@pytest.mark.asyncio
async def test_generate_svg():
    svg = await qrcode_service.generateSvgAsync("http://example.com")
    assert svg.startswith("<svg")

@pytest.mark.asyncio
async def test_generate_image():
    image = await qrcode_service.generatePilImageAsync("http://example.com")
    assert image is not None
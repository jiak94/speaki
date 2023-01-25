import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_download(mock_file):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/download/test.txt")
    assert response.status_code == 200
    assert response.text == "Hello World"


@pytest.mark.asyncio
async def test_speak_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/speak", json={"text": "Hello World"})
    assert response.status_code == 422

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/speak", json={"ssml": "Hello World"})
    assert response.status_code == 422

    body = {
        "text": "Hello World",
        "ssml": "Hello World",
        "voice": "en-US-AriaNeural",
        "speed": "medium",
        "service": "azure",
        "language": "en-US",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/speak", json=body)
    assert response.status_code == 400

    text = ["Hello"] * 3001
    body = {
        "text": " ".join(text),
        "voice": "en-US-AriaNeural",
        "speed": "medium",
        "service": "azure",
        "language": "en-US",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/speak", json=body)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_voices_async(azure):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/voices", params={"service": "azure", "language": "en-US"}
        )
    assert response.status_code == 200
    assert response.json().get("voices") is not None

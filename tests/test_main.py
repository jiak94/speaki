def test_echo_handler(test_client):
    response = test_client.get("/echo")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_voices(test_client, azure):
    response = test_client.get(
        "/voices", params={"service": "azure", "language": "en-US"}
    )
    assert response.status_code == 200
    assert response.json().get("voices") is not None


def test_download(test_client, mock_file):
    response = test_client.get("/download/test.txt")
    assert response.status_code == 200
    assert response.text == "Hello World"


def test_speak_invalid(test_client):
    response = test_client.post("/speak", json={"text": "Hello World"})
    assert response.status_code == 422

    response = test_client.post("/speak", json={"ssml": "Hello World"})
    assert response.status_code == 422

    body = {
        "text": "Hello World",
        "ssml": "Hello World",
        "voice": "en-US-AriaNeural",
        "speed": "medium",
        "service": "azure",
        "language": "en-US",
    }
    response = test_client.post("/speak", json=body)
    assert response.status_code == 400

    text = ["Hello"] * 3001
    body = {
        "text": " ".join(text),
        "voice": "en-US-AriaNeural",
        "speed": "medium",
        "service": "azure",
        "language": "en-US",
    }
    response = test_client.post("/speak", json=body)
    assert response.status_code == 400

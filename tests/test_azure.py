from app.controllers.speak import _wrap_with_ssml


def test_azure_without_voice(azure):
    ssml = _wrap_with_ssml("Hello World", "medium", "en-US", "en-US-AriaNeural")

    try:
        azure.speak(ssml)
    except Exception:
        assert False


def test_azure_get_voices(azure):
    voices = azure.get_voices("en-US")
    assert len(voices) > 0

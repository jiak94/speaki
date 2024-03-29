from app.utils import count_text_size


def test_count_text_size():
    text = "Hello World"
    count = count_text_size(text)
    assert count == 2

    text = "Hello"
    count = count_text_size(text)
    assert count == 1

    text = ""
    count = count_text_size(text)
    assert count == 0

    text = "World, "
    count = count_text_size(text)
    assert count == 1

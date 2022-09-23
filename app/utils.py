def count_text_size(text: str) -> int:
    text = text.strip()
    if len(text) == 0:
        return 0

    word_list = text.split(" ")
    return len(word_list)


class ValueNotExistsError(Exception):
    pass

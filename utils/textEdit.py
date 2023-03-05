

def remove_chars(text, chars_to_remove):
    """
    文字列から指定された文字を取り除く関数。

    Args:
        text (str): 文字列。
        chars_to_remove (str): 取り除く文字列。

    Returns:
        str: 取り除かれた文字列。
    """
    for char in chars_to_remove:
        text = text.replace(char, "")
    return text
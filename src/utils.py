import json


def preserve_last(old: any, new: any) -> any:
    """
    Merges two values, preserving the last one if it exists.

    Args:
        old (any): The original value.
        new (any): The new value to merge.
    """
    return new

def remove_thinking(text: str) -> str:
    """
    Removes the thinking part from the text.

    Args:
        text (str): The text containing the thinking part.

    Returns:
        str: The text without the thinking part.
    """
    thinking_suffix = "</thinking>"
    end = text.index(thinking_suffix) + len(thinking_suffix)

    # Get the rest of the text without the thinking part
    text = text[end:]

    return text.strip()

def load_md_file(path: str):
    """
    Docstring para load_md_file
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def write_to_md_file(path: str, content: str):
    """
    Docstring para write_to_md_file
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def load_json_file(path: str):
    """
    Docstring para load_json_file
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


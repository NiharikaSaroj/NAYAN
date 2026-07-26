import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text by removing unnecessary whitespace
    while preserving the original content.
    """

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{2,}", "\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text
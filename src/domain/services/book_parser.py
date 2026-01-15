from lark import Lark, Transformer

from domain.book_aggregate.book import Book
from domain.book_aggregate.content import Content, ContentType
from domain.book_aggregate.image import Image
from domain.book_aggregate.page import Page


class BookDomainTransformer(Transformer):
    """
    Transforms the Lark syntax tree directly into Domain Objects.
    This acts as an Adapter between the raw text structure and your strict Pydantic models.
    """

    def TEXT(self, token):
        """
        Terminal rule: Converts raw text tokens into Content objects.
        Detects 'Pregunta:' to set the correct ContentType.

        Args:
            token (str): The raw text token from the parser.

        Returns:
            Content: A domain Content object (TEXT or QUESTION type).
        """
        text = str(token).strip()

        # Business Rule: Detect Questions
        if text.lower().startswith("pregunta:"):
            # Clean strict parsing: remove prefix and whitespace
            clean_text = text.split(":", 1)[1].strip()
            return Content(type=ContentType.QUESTION, text=clean_text)

        return Content(type=ContentType.TEXT, text=text)

    def IMAGE_LINE(self, token):
        """
        Terminal rule: Parses custom image syntax `![caption]:(url)` into Image objects.

        Args:
            token (str): The raw token string containing the image markdown.

        Returns:
            Image: A domain Image object with data (url) and caption.
        """
        raw = str(token).strip()

        try:
            # Robustly parse the custom format: ![Caption]:(Url)
            # 1. Split by ']:(' to separate caption part from url part
            parts = raw.split("]:(")
            if len(parts) != 2:
                raise ValueError("Malformed image tag")

            # 2. Clean artifacts (![ and ))
            caption = parts[0].replace("![", "", 1).strip()
            url = parts[1].rstrip(")").strip()

            return Image(data=url, caption=caption)
        except Exception:
            # Graceful fallback for parser errors
            return Image(data="", caption="Invalid Image Format")

    def line(self, items):
        """
        Unwraps a single line item from the parse tree.

        Args:
            items (list): A list containing a single Content or Image object.

        Returns:
            Content | Image: The unwrapped domain object.
        """
        return items[0]

    def page_block(self, items):
        """
        Aggregates a sequence of mixed Content and Images into a Page.
        Separates them into distinct lists as required by the Page model.

        Args:
            items (list): A mixed list of Content and Image objects found in one page block.

        Returns:
            Page: A constructed Page object with separated contents and images.
        """
        contents = []
        images = []

        for item in items:
            if isinstance(item, Content):
                contents.append(item)
            elif isinstance(item, Image):
                images.append(item)

        return Page(contents=contents, images=images)

    def title_line(self, items):
        """
        Extracts the title text from a header line.

        Args:
            items (list): A list containing a single Content object (wrapped TEXT).

        Returns:
            str: The raw string title.
        """
        return items[0].text

    def front_image(self, items):
        """
        Extracts the front cover image object.

        Args:
            items (list): A list containing a single Image object.

        Returns:
            Image: The Image object representing the book cover.
        """
        return items[0]

    def header(self, items):
        """
        Collects optional title and front image into a temporary dictionary.

        Args:
            items (list): A list that may contain a title string, an Image object, or both.

        Returns:
            dict: A dictionary with keys 'title' (str) and 'front_page_image' (Image | None).
        """
        header_data = {"title": "Untitled", "front_page_image": None}

        for item in items:
            if isinstance(item, str):
                header_data["title"] = item
            elif isinstance(item, Image):
                header_data["front_page_image"] = item

        return header_data

    def start(self, items):
        """
        Root rule: Assembles the final Book object.

        Args:
            items (list): List containing an optional header dict followed by Page objects.

        Returns:
            Book: The fully constructed Book domain object.
        """
        first_item = items[0]

        # Logic: If the first item is a dict, it's the header. Otherwise, it's the first Page.
        if isinstance(first_item, dict):
            header = first_item
            pages = items[1:]  # All items after header are Pages
            return Book(
                title=header["title"],
                front_page_image=header["front_page_image"],
                pages=pages
            )
        else:
            # No header provided
            return Book(
                title="Untitled",
                front_page_image=None,
                pages=items
            )


class BookParser:
    """
    Service Facade for parsing text into Book objects.
    Hides the grammar complexity from the rest of the application.
    """

    # Defined here or imported from a grammar.py file
    _GRAMMAR = r"""
        start: header? page_block+

        header: title_line? front_image?
        title_line: "#" TEXT
        front_image: IMAGE_LINE

        page_block: SEP line*
        line: IMAGE_LINE | TEXT

        // Custom Image Format matching user's specific syntax: ![...]:(...)
        IMAGE_LINE: /!\[.*\]:\([^\)]+\)/

        SEP: "---"
        TEXT: /[^\n]+/

        %import common.WS_INLINE
        %ignore WS_INLINE
        %ignore /\n+/
    """

    def __init__(self):
        """
        Initializes the Parser service.
        Compiles the Lark grammar and instantiates the Transformer once to save resources.
        """
        self._lark = Lark(self._GRAMMAR, parser="lalr")
        self._transformer = BookDomainTransformer()

    def parse(self, text):
        """
        Parses raw string input into a fully hydrated Book object.

        Args:
            text (str): The raw text content to be parsed.

        Returns:
            Book: The resulting domain object tree.

        Raises:
            UnexpectedToken: If the text does not match the grammar.
        """
        tree = self._lark.parse(text)
        return self._transformer.transform(tree)

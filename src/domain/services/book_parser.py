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
        """
        text = str(token).strip()

        # Business Rule: Detect Questions
        if text.lower().startswith("pregunta:"):
            clean_text = text.split(":", 1)[1].strip()
            return Content(type=ContentType.QUESTION, text=clean_text)

        return Content(type=ContentType.TEXT, text=text)

    def IMAGE_LINE(self, token):
        """
        Parses custom image syntax `![caption]:(url)` into Image objects.
        """
        raw = str(token).strip()

        try:
            parts = raw.split("]:(")
            if len(parts) != 2:
                raise ValueError("Malformed image tag")

            caption = parts[0].replace("![", "", 1).strip()
            url = parts[1].rstrip(")").strip()

            return Image(data=url, caption=caption)
        except Exception:
            return Image(data="", caption="Invalid Image Format")

    def line(self, items):
        return items[0]

    def page_block(self, items):
        contents = []
        images = []

        for item in items:
            if isinstance(item, Content) and item.text.strip():
                contents.append(item)
            elif isinstance(item, Image):
                images.append(item)

        return Page(contents=contents, images=images)

    def title_line(self, items):
        return items[0].text

    def front_image(self, items):
        return items[0]

    def header(self, items):
        header_data = {"title": "Untitled", "front_page_image": None}

        for item in items:
            if isinstance(item, str):
                header_data["title"] = item
            elif isinstance(item, Image):
                header_data["front_page_image"] = item

        return header_data

    def start(self, items):
        first_item = items[0]

        if isinstance(first_item, dict):
            header = first_item
            pages = items[1:]
            return Book(
                title=header["title"],
                front_page_image=header["front_page_image"],
                pages=pages,
            )

        return Book(
            title="Untitled",
            front_page_image=None,
            pages=items,
        )


class BookParser:
    """
    Service Facade for parsing text into Book objects.
    """

    _GRAMMAR = r"""
        start: header? page_block+

        header: title_line? front_image?
        title_line: "#" TEXT
        front_image: IMAGE_LINE

        page_block: SEP line*
        line: IMAGE_LINE | TEXT

        IMAGE_LINE: /!\[.*?\]:\([^)]+\)/

        SEP.2: "---"
        TEXT.1: /[^\n]+/

        %import common.WS_INLINE
        %ignore WS_INLINE
        %ignore /\n+/
    """

    def __init__(self):
        self._lark = Lark(self._GRAMMAR, parser="lalr")
        self._transformer = BookDomainTransformer()

    def parse(self, text: str) -> Book:
        tree = self._lark.parse(text)
        return self._transformer.transform(tree)

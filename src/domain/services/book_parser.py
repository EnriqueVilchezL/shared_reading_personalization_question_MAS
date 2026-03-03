from lark import Lark, Transformer
from typing import List, Union

# Domain Imports (Assumed existing)
from domain.book_aggregate.book import Book
from domain.book_aggregate.content import Content, ContentType
from domain.book_aggregate.image import Image
from domain.book_aggregate.page import Page

class BookDomainTransformer(Transformer):
    """
    Transforms the Lark syntax tree into Domain Objects.
    Merges lines into paragraphs but preserves the inner newlines.
    """

    def TEXT(self, token):
        """Returns the string. We do not strip here to preserve potential spacing."""
        return str(token)

    def PARA_SEP(self, _):
        """Marker for double-newline paragraph breaks."""
        return "__PARA_BREAK__"

    def text_block(self, items: List[str]) -> List[Content]:
        """
        Groups lines. Merges them with '\n' to preserve the internal structure.
        Splits into separate Content objects only at __PARA_BREAK__.
        """
        paragraphs = []
        current_buffer = []

        for item in items:
            if item == "__PARA_BREAK__":
                if current_buffer:
                    paragraphs.append(self._create_content_object(current_buffer))
                    current_buffer = []
            else:
                current_buffer.append(item)

        if current_buffer:
            paragraphs.append(self._create_content_object(current_buffer))

        return paragraphs

    def _create_content_object(self, buffer: List[str]) -> Content:
        """
        Joins the lines using '\n' to keep the user's formatting 
        within the Content object.
        """
        # Join using newline to satisfy the requirement
        full_text = "\n".join(buffer).strip()
        
        # Business Rule: Detect Questions
        if full_text.lower().startswith("pregunta:"):
            clean_text = full_text.split(":", 1)[1].strip()
            return Content(type=ContentType.QUESTION, text=clean_text)
            
        return Content(type=ContentType.TEXT, text=full_text)

    def image_entry(self, items) -> Image:
        raw = str(items[0]).strip()
        try:
            parts = raw.split("]:(")
            caption = parts[0].replace("![", "", 1).strip()
            url = parts[1].rstrip(")").strip()
            return Image(data=url, caption=caption)
        except Exception:
            return Image(data="", caption="Invalid Image Format")

    def page_block(self, items: List[Union[List[Content], Image]]) -> Page:
        contents = []
        images = []

        for item in items:
            if isinstance(item, list):
                contents.extend(item)
            elif isinstance(item, Image):
                images.append(item)

        return Page(contents=contents, images=images)

    def title_line(self, items):
        return str(items[0]).strip()

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
                pages=pages
            )
        return Book(title="Untitled", front_page_image=None, pages=items)


class BookParser:
    """
    Service Facade for parsing text into Book objects.
    """

    _GRAMMAR = r"""
        start: header? page_block+

        header: title_line? front_image?
        title_line: "#" TEXT
        front_image: image_entry

        page_block: SEP (image_entry | text_block)*
        
        text_block: (TEXT | PARA_SEP)+
        image_entry: IMAGE_LINE

        IMAGE_LINE: /!\[.*?\]:\([^)]+\)/
        SEP.2: "---"
        
        TEXT.1: /[^\n]+/
        PARA_SEP: /\n{2,}/

        %import common.WS_INLINE
        %ignore WS_INLINE
        # We ignore single newlines globally for the tree structure,
        # but our transformer manual join puts them back in.
        %ignore /\n/
    """

    def __init__(self):
        self._lark = Lark(self._GRAMMAR, parser="lalr")
        self._transformer = BookDomainTransformer()

    def parse(self, text: str) -> Book:
        tree = self._lark.parse(text)
        return self._transformer.transform(tree)
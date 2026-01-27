from domain.book_aggregate.book import Book
from domain.book_aggregate.content import Content, ContentType
from domain.book_aggregate.image import Image
from domain.book_aggregate.page import Page


class BookMarkdownRenderer:
    """
    Service responsible for converting Book domain objects into Markdown.
    Follows the Single Responsibility Principle.
    """

    def __init__(
        self,
        include_images: bool = False,
        include_images_data: bool = False,
        ignore_content_types: list[ContentType] = None
    ):
        self.include_images = include_images
        self.include_images_data = include_images_data
        self.ignore_types = ignore_content_types or []

    def render(self, book: Book) -> str:
        """Orchestrates the rendering of the entire book."""
        md_output = [f"# {book.title}\n"]

        if self.include_images and book.front_page_image:
            md_output.append(self._render_image(book.front_page_image))
            md_output.append("\n")

        for page in book.pages:
            md_output.append("---")
            md_output.append(self._render_page(page))

        return "\n".join(md_output)

    def _render_page(self, page: Page) -> str:
        """
        Renders a page.
        Retains the logic of interleaving content and images by index.
        """
        page_md = []

        # Enumerate gives us the index to find the matching image
        for i, content in enumerate(page.contents):
            if content.type in self.ignore_types:
                continue

            page_md.append(self._render_content(content))

            # Logic: If there is a corresponding image for this content block index
            if self.include_images and i < len(page.images):
                image = page.images[i]
                page_md.append(self._render_image(image))

        return "\n\n".join(page_md) + "\n"

    def _render_content(self, content: Content) -> str:
        match content.type:
            case ContentType.QUESTION:
                return f"**Pregunta:** {content.text}"
            case ContentType.TEXT:
                return content.text
            case _:
                return content.text

    def _render_image(self, image: Image) -> str:
        if self.include_images_data:
            # Assumes data is base64
            return f"![{image.caption}](data:image/png;base64,{image.data})"
        else:
            # Fallback to a placeholder or filename if URL isn't available in data
            return f"![{image.caption}](image.png)"

import base64
from pathlib import Path

from shared_reading_mas.domain.book_aggregate.book import Book
from shared_reading_mas.domain.book_aggregate.content import Content, ContentType
from shared_reading_mas.domain.book_aggregate.image import Image
from shared_reading_mas.domain.book_aggregate.page import Page


class BookMarkdownRenderer:
    """
    Service responsible for converting Book domain objects into Markdown.
    Follows the Single Responsibility Principle.
    """

    def __init__(
        self,
        to_path: Path | None = None,
        include_images: bool = False,
        include_images_data: bool = False,
        include_num_pages: bool = False,
        ignore_content_types: list[ContentType] = None
    ):
        self.to_path = to_path
        self.include_images = include_images
        self.include_images_data = include_images_data
        self.include_num_pages = include_num_pages
        self.ignore_types = ignore_content_types or []

    def render(self, book: Book) -> str:
        """Orchestrates the rendering of the entire book."""

        if self.include_num_pages:
            book_title = f"{book.title} (Total Pages: {len(book.pages)})"
        else:
            book_title = book.title

        md_output = [f"# {book_title}\n"]

        if self.include_images and book.front_page_image:
            md_output.append(self._render_image(book.front_page_image, name="front"))

        for i, page in enumerate(book.pages):
            md_output.append("---")
            md_output.append(self._render_page(page, page_number=i + 1))

        book_md = "\n".join(md_output)
        if self.to_path:
            # Do an mkdir
            self.to_path.mkdir(parents=True, exist_ok=True)

            story_path = self.to_path / "story.md"
            story_path.write_text(book_md, encoding="utf-8")

        return book_md

    def _render_page(self, page: Page, page_number: int) -> str:
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
            if self.include_images and i == len(page.contents) - 1:
                image = page.images[0]
                    # If there's only one image on the page, use the page number for naming
                page_md.append(self._render_image(image, name=page_number))

        return "\n\n".join(page_md) + "\n"

    def _render_content(self, content: Content) -> str:
        match content.type:
            case ContentType.QUESTION:
                return f"**Pregunta:** {content.text}"
            case ContentType.TEXT:
                return content.text
            case _:
                return content.text

    def _render_image(self, image: Image, name: str | None = None) -> str:
        if self.to_path:
            if name is None:
                name = image.caption.replace(" ", "_") if image.caption else name
            # If we have a path to save, we can use relative paths for images
            # Do an mkdir for images if it doesn't exist

            images_dir = self.to_path / "images"
            images_dir.mkdir(parents=True, exist_ok=True)

            image_path = self.to_path / "images" / f"{name}.png"
            image_path.write_bytes(base64.b64decode(image.data))
            return f"![{image.caption}]({Path('images') / f'{name}.png'})"

        if self.include_images_data:
            # Assumes data is base64
            return f"![{image.caption}](data:image/png;base64,{image.data})"
        else:
            # Fallback to a placeholder or filename if URL isn't available in data
            return f"Image Description: {image.caption}"

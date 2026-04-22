from concurrent.futures import ThreadPoolExecutor

from langchain.messages import HumanMessage

from shared_reading_mas.agents.core.base_agent import Agent
from shared_reading_mas.agents.core.base_lm_config import LMConfiguration
from shared_reading_mas.domain.book_aggregate.book import Book
from shared_reading_mas.domain.book_aggregate.image import Image
from shared_reading_mas.domain.services.book_parser import BookParser
from shared_reading_mas.domain.services.book_renderer import BookMarkdownRenderer
from shared_reading_mas.domain.services.image_editor import (
    BaseImageEditor,
    base64_to_pil,
    pil_to_base64,
)
from shared_reading_mas.roles.personalization.image_editor import ImageEditorRole


class ImageEditorAgent(Agent):
    """
    Agent that edits images.
    """

    def __init__(
        self,
        image_editing_service: BaseImageEditor,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="image_editor",
            roles=[ImageEditorRole()],
            lm_config=lm_config,
        )

        self.base_image_editor: BaseImageEditor = image_editing_service

    def _create_images_messages(self, book: Book) -> list[HumanMessage]:
        images_parts = []
        for i, page in enumerate(book.pages):
            for image in page.images:
                images_parts.extend(
                    [
                        {"type": "text", "text": f"\nImágen de **Página {i + 1}**:\n"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image.data}"},
                        },
                    ]
                )

        return images_parts

    def pre_core(self, data: dict) -> dict:
        renderer_with_captions = BookMarkdownRenderer(
            include_images=False, include_images_data=False
        )
        renderer = BookMarkdownRenderer()

        contents = [
            {"type": "text", "text": "Hazlo para este cuento:"},
            {
                "type": "text",
                "text": "\n\n**Cuento original**:\n"
                + renderer_with_captions.render(data.get("original_book", "")),
            },
        ]
        contents.extend(self._create_images_messages(data.get("original_book")))
        contents.append(
            {
                "type": "text",
                "text": "\n\n**Cuento personalizado**:\n"
                + renderer.render(data.get("modified_book", "")),
            }
        )

        request = HumanMessage(content=contents)

        return {"messages": request}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)
        last_message = data.get("messages", [])[-1].content
        editing_requests = BookParser().parse(last_message)

        tasks = []

        with ThreadPoolExecutor(max_workers=6) as executor:
            for i, (original_page, modified_page, editing_request_page) in enumerate(
                zip(
                    data.get("original_book", []).pages,
                    data.get("modified_book", []).pages,
                    editing_requests.pages,
                )
            ):
                parsed_request = editing_request_page.contents[0].text

                for image in original_page.images:
                    pil_image = base64_to_pil(image.data)
                    future = executor.submit(
                        self.base_image_editor.edit_image, pil_image, parsed_request, "512x512"
                    )

                    tasks.append((future, i))

            for future, i in tasks:
                edited_image = future.result()
                book = data.get("modified_book", "")
                modified_page = book.pages[i]

                modified_page.images.append(
                    Image(
                        data=pil_to_base64(edited_image),
                        caption=f"Imágen de Página {i + 1}",
                    )
                )

        return {"modified_book": data.get("modified_book", "")}

from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.book_aggregate.image import Image
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from domain.services.evaluation_parser import EvaluationParser
from domain.services.image_editor import BaseImageEditor, base64_to_pil, pil_to_base64


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
            roles=[],
            lm_config=lm_config,
        )

        self.base_image_editor: BaseImageEditor = image_editing_service

    def pre_core(self, data: dict) -> dict:
        renderer_with_captions = BookMarkdownRenderer(include_images=True, include_images_data=False)
        renderer = BookMarkdownRenderer()

        request = HumanMessage(
            "Hazlo para este cuento: \n"
            + "\n\n**Cuento original**:\n"
            + renderer_with_captions.render(data.get("original_book", ""))
            + "\n\n**Cuento personalizado**:\n"
            + renderer.render(data.get("modified_book", ""))
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)
        last_message = data.get("messages", [])[-1].content
        editing_requests = BookParser().parse(last_message)

        for original_page, modified_page, editing_request in zip(
            data.get("original_book", []).pages, data.get("modified_book", []).pages, editing_requests
        ):
            parsed_request = EvaluationParser().parse(editing_request)
            for image in original_page.images:
                pil_image = base64_to_pil(image.data)
                image = self.base_image_editor.edit_image(
                    pil_image, parsed_request.changes
                )
                modified_page.images.append(Image(
                    data=pil_to_base64(image),
                    caption=parsed_request.label
                ))

        return {"modified_book": data.get("modified_book", "")}

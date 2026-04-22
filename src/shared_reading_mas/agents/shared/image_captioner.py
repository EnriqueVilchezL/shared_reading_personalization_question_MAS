from langchain.messages import HumanMessage

from shared_reading_mas.agents.core.base_agent import Agent
from shared_reading_mas.agents.core.base_lm_config import LMConfiguration
from shared_reading_mas.roles.shared.image_captioner import ImageCaptionerRole


class ImageCaptionerAgent(Agent):
    """
    Agent that captions images.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="image_captioner",
            roles=[ImageCaptionerRole()],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        image = data.get("image").data
        request = HumanMessage(
            content=[
                {"type": "text", "text": "Hazlo para esta imagen:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image}"
                    }
                }
            ]
        )

        return {"messages": [request]}


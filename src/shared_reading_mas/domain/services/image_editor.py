import base64
import io
import os
from abc import ABC, abstractmethod

from openai import OpenAI
from PIL import Image


def pil_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Encode a PIL image to a base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def base64_to_pil(data: str) -> Image.Image:
    """Decode a base64 string (with or without data URI prefix) to a PIL image."""
    if data.startswith("data:"):
        data = data.split(",", 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(data)))

def image_editor_factory(editor: str, configuration: dict) -> "BaseImageEditor":
    if editor == "openrouter":
        return OpenRouterImageEditor(model=configuration["base_model"])
    else:
        raise ValueError(f"Unknown image editor: {editor}")

class BaseImageEditor(ABC):
    """
    Service class for editing images. This class provides methods for performing various image editing operations using AI
    """

    @abstractmethod
    def edit_image(self, image: Image, prompt: str, size: str = "1024x1024") -> Image:
        """
        Edits the given image based on the provided prompt.

        Args:
            image (Image): The image to be edited.
            prompt (str): The prompt describing the desired edits.
            size (str): The size of the edited image.

        Returns:
            Image: The edited image.
        """
        pass

class OpenRouterImageEditor(BaseImageEditor):
    """
    Service class for editing images using a cloud-based AI model. This class implements the BaseImageEditor interface and provides methods for performing various image editing operations using a cloud-based AI model.
    """

    def __init__(self, model: str, api_key: str = None):
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key if api_key else os.environ.get("OPENROUTER_API_KEY", api_key),
        )

    def edit_image(self, image: Image, prompt: str, size: str = "1024x1024") -> Image:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{pil_to_base64(image)}"},
                        },
                    ],
                }
            ],
            extra_body={
                "modalities": ["image"],
                "image_config": {"size": size},
            },
        )

        message = response.choices[0].message

        if not getattr(message, "images", None):
            raise ValueError(f"No image returned in model response: {message}")

        return base64_to_pil(message.images[0]["image_url"]["url"])

import base64
import io
import json
import os
import random
import time
from abc import ABC, abstractmethod

from google import genai
from google.genai import types
from openai import OpenAI
from PIL import Image
from vertexai import init
from vertexai.generative_models import GenerativeModel, Part

# ----------------------------
# Utils
# ----------------------------

def pil_to_base64(image: Image.Image, format: str = "PNG") -> str:
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def base64_to_pil(data: str) -> Image.Image:
    if data.startswith("data:"):
        data = data.split(",", 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(data)))


def retry_until_valid(fn, is_valid, max_retries=3, base_delay=1.0):
    last_result = None
    last_error = None

    for attempt in range(max_retries):
        try:
            result = fn()
            last_result = result

            if is_valid(result):
                return result

        except Exception as e:
            last_error = e

        time.sleep(min(20, base_delay * (2 ** attempt)) + random.uniform(0, 0.5))

    if last_result is not None:
        return last_result

    if last_error:
        raise last_error

    raise ValueError("All retries failed with no valid result")


# ----------------------------
# Base interface
# ----------------------------

class BaseImageEditor(ABC):
    @abstractmethod
    def edit_image(self, image: Image, prompt: str, size: str = "1024x1024", max_retries: int = 3):
        pass


# ----------------------------
# Factory
# ----------------------------

def image_editor_factory(editor: str, configuration: dict):
    if editor == "openrouter":
        return OpenRouterImageEditor(model=configuration["base_model"])

    elif editor == "google":
        return GoogleImageEditor(model=configuration["base_model"], vertex_ai=False)

    elif editor == "vertex":
        return GoogleImageEditor(model=configuration["base_model"], vertex_ai=True)

    else:
        raise ValueError(f"Unknown image editor: {editor}")


# ----------------------------
# Google / Gemini API (AI Studio or Vertex via genai client)
# ----------------------------

class GoogleImageEditor(BaseImageEditor):

    def __init__(self, model: str, vertex_ai: bool = False):
        self.model = model
        self.client = genai.Client(
            vertexai=vertex_ai,
            project=os.environ.get("GOOGLE_PROJECT_ID"),
            api_key=os.environ.get("GOOGLE_API_KEY"),
        )

    def edit_image(self, image, prompt, size="1024x1024", max_retries=3):

        def call():
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()

            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    prompt,
                    types.Part.from_bytes(
                        data=img_bytes,
                        mime_type="image/png",
                    ),
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
                ),
            )

            parts = response.candidates[0].content.parts
            print(parts)
            for part in parts:
                if getattr(part, "inline_data", None):
                    return Image.open(io.BytesIO(part.inline_data.data))

            return None

        return retry_until_valid(
            call,
            is_valid=lambda img: img is not None,
            max_retries=max_retries,
        )


# ----------------------------
# OpenRouter Image Editor
# ----------------------------

class OpenRouterImageEditor(BaseImageEditor):

    def __init__(self, model: str, api_key: str = None):
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or os.environ.get("OPENROUTER_API_KEY"),
        )

    def edit_image(self, image, prompt, size="1024x1024", max_retries=3):

        def call():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{pil_to_base64(image)}"
                                },
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
            images = getattr(message, "images", None)

            if not images:
                return None

            return base64_to_pil(images[0]["image_url"]["url"])

        return retry_until_valid(
            call,
            is_valid=lambda img: img is not None,
            max_retries=max_retries,
        )


# ----------------------------
# Vertex AI Image Editor
# ----------------------------

class VertexImageEditor(BaseImageEditor):

    def __init__(self, model: str, location: str = "us-central1"):
        self.model_name = model
        self.location = location

        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set")

        with open(credentials_path, "r") as f:
            credentials = json.load(f)

        self.project_id = credentials["project_id"]

        init(project=self.project_id, location=self.location)

        self.model = GenerativeModel(self.model_name)

    def edit_image(self, image, prompt, size="1024x1024", max_retries=3):

        def call():
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()

            image_part = Part.from_data(
                mime_type="image/png",
                data=img_bytes,
            )

            response = self.model.generate_content(
                [prompt, image_part],
                generation_config={"temperature": 0.4},
            )

            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if getattr(part, "inline_data", None):
                        if "image" in part.inline_data.mime_type:
                            return Image.open(
                                io.BytesIO(part.inline_data.data)
                            )

            return None

        return retry_until_valid(
            call,
            is_valid=lambda img: img is not None,
            max_retries=max_retries,
        )

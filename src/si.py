from openai import OpenAI
import base64, io
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_b64 = encode_image("input.png")

response = client.chat.completions.create(
    model="google/gemini-3.1-flash-image-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Make this a cat instead of a dog"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_b64}"
                    }
                }
            ]
        }
    ],
    extra_body={
        "modalities": ["image"],
        "image_config": {
            "size": "1024x1024"
        }
    }
)

msg = response.choices[0].message

image_data = msg.images[0]["image_url"]["url"]
image_data = image_data.split(",")[1]

image = Image.open(io.BytesIO(base64.b64decode(image_data)))
image.show()
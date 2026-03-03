import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from langchain_openrouter import ChatOpenRouter

load_dotenv()

model = ChatOpenRouter(
    model="google/gemini-2.5-pro",
    temperature=1,
    max_retries=3
)
response = model.invoke([{"role": "user", "content": "What is the capital of France?"}])
print(response)

from langchain.chat_models import init_chat_model

model = init_chat_model(
    model_provider="ollama",
    model="cogito:8b",
)

messages = model.invoke([
    {"role": "system", "content": "You are a pirate. Enable deep thinking subroutine."},
    {"role": "user", "content": "Explain why primes matter in cryptography."},
])
print(messages.content)
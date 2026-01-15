from pydantic import BaseModel, Field


class LMConfiguration(BaseModel):
    """
    Configuration for a generic language model.
    """

    base_provider: str = Field(
        default="ollama",
        description="The name of the provider to use for the language model's query generation."
    )

    base_model: str = Field(
        default="gemma3:4b",
        description="The name of the language model to use for the language model's query generation."
    )

    temperature: float = Field(
        default=1,
        description="The temperature to use for the language model's query generation."
    )

    reasoning: bool = Field(
        default=False,
        description="Whether to enable reasoning capabilities in the language model."
    )

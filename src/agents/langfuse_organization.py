from langfuse.langchain import CallbackHandler

from agents.core.base_organization import Information, Organization


class LangFuseOrganization(Organization):
    """Represents a LangFuse organization."""

    def __init__(self, name: str, information_schema: type[Information] = Information):
        super().__init__(
            name=name, information_schema=information_schema
        )
        self.configuration['callbacks'] = [CallbackHandler()]

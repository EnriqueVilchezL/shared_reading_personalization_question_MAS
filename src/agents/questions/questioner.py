import copy

from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from agents.personalization.information import Information
from domain.book_aggregate.content import Content, ContentType
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from roles.core.base_role import Role, RoleCollection
from roles.questions.questioner import (
    CompletionQuestionerRole,
    DistancingQuestionerRole,
    OpenEndedQuestionerRole,
    QuestionerEditorRole,
    RecallQuestionerRole,
    WhQuestionerRole,
)


class QuestionerAgent(Agent):
    """
    Agent that creates questions for a story.
    """

    def __init__(
        self,
        name: str,
        roles: list[Role] | RoleCollection | None = None,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name=name, roles=roles, lm_config=lm_config, information_schema=Information
        )

    def pre_core(self, data: dict) -> dict:
        super().pre_core(data)
        last_message = data.get("messages", [])[-1].content
        renderer = BookMarkdownRenderer()

        request = HumanMessage(
            "Porfavor, genera para el siguiente cuento:\n\n"
            + renderer.render(data.get("original_book", ""))
            + "\n\n**Debes usar este análisis del cuento original, para las preguntas**:\n"
            + last_message
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)

        last_message = data["messages"][-1].content

        parser = BookParser()
        book = parser.parse(last_message)
        book.title = next(iter(self.roles)).prompt.type

        # Complete questions are refined by the CompletionRefinerAgent, so we do not want to return them as part of the questions_books, since they will be returned in a modified form after being refined.
        if book.title != "C: Completion":
            return {"questions_books": [book]}
        else:
            return {}


class CompletionQuestionerAgent(QuestionerAgent):
    """
    Agent that creates completion questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="completion_questioner",
            roles=[CompletionQuestionerRole()],
            lm_config=lm_config,
        )


class RecallQuestionerAgent(QuestionerAgent):
    """
    Agent that creates recall questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="recall_questioner",
            roles=[RecallQuestionerRole()],
            lm_config=lm_config,
        )


class OpenEndedQuestionerAgent(QuestionerAgent):
    """
    Agent that creates open-ended questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="open_ended_questioner",
            roles=[OpenEndedQuestionerRole()],
            lm_config=lm_config,
        )


class WhQuestionerAgent(QuestionerAgent):
    """
    Agent that creates WH questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="wh_questioner",
            roles=[WhQuestionerRole()],
            lm_config=lm_config,
        )


class DistancingQuestionerAgent(QuestionerAgent):
    """
    Agent that creates distancing questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="distancing_questioner",
            roles=[DistancingQuestionerRole()],
            lm_config=lm_config,
        )


class QuestionerEditorAgent(Agent):
    """
    Agent that edits questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="questioner_editor",
            roles=[QuestionerEditorRole()],
            lm_config=lm_config,
            information_schema=Information,
        )

    def pre_core(self, data: dict) -> dict:
        super().pre_core(data)
        renderer = BookMarkdownRenderer()
        last_evaluation = data["evaluations"][-1]

        request = HumanMessage(
            "Después de hacer una evaluación de las intervenciones de un cuento, se solicitaron las siguientes ediciones a las preguntas: \n"
            + "\n\n**Cuento original**:\n"
            + renderer.render(data.get("original_book", ""))
            + "\n\n**Intervenciones CROWD**:\n"
            + renderer.render(data.get("questions_book", ""))
            + "\n\n**Ediciones solicitadas**:\n"
            + last_evaluation.changes
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)
        last_message = data.get("messages", [])[-1].content
        book = BookParser().parse(last_message)

        modified_book = copy.deepcopy(data["original_book"])
        for original_page, output_page in zip(modified_book.pages, book.pages):
            original_page.contents.append(
                Content(type=ContentType.QUESTION, text=output_page.contents[0].text)
            )

        return {"questions_book": book, "modified_book": modified_book}

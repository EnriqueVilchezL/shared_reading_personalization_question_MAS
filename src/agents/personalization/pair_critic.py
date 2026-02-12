import random

from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.evaluation_aggregate.criteria import Criteria
from domain.evaluation_aggregate.evaluation import Evaluation
from domain.services.book_renderer import BookMarkdownRenderer
from roles.personalization.pair_critic import PairCriticRole


class PairCriticAgent(Agent):
    """
    Agent that evaluates responses based on user preferences.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="pair_critic",
            roles=[
                PairCriticRole(),
            ],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        renderer = BookMarkdownRenderer()

        if len(data.get("intermediate_books", [])) == 2:
            book_1 = data["intermediate_books"][0]
            book_2 = data["intermediate_books"][1]

        else:
            book_1, book_2 = random.sample(data.get("intermediate_books", []), 2)

        self.book_1 = book_1.uid
        self.book_2 = book_2.uid

        message = HumanMessage(
            "Porfavor, indica con una etiqueta (A o B) cuál cuento es mejor. Da tu respuesta **sin explicaciones adicionales**.\n\n**Cuento original**:\n"
            + renderer.render(data.get("original_book", ""))
            + "\n\n**Cuento personalizado A**:\n"
            + renderer.render(book_1)
            + "\n\n**Cuento personalizado B**:\n"
            + renderer.render(book_2)
        )

        return {"messages": [message]}

    def post_core(self, data: dict) -> dict:
        last_message = data["messages"][-1].content

        lines = last_message.replace("*", "").splitlines()

        evaluation = Evaluation(label="", reasoning="", changes="")
        finish = False
        i = 0

        while i < len(lines) and not finish:
            words = lines[i].strip().split(" ")
            j = 0

            while j < len(words) and not finish:
                word = words[j]

                if word == "A":
                    print(f"Agent {self.name} selected book A as better.")
                    evaluation.label = str(self.book_1)
                    finish = True

                elif word == "B":
                    print(f"Agent {self.name} selected book B as better.")
                    evaluation.label = str(self.book_2)
                    finish = True

                j += 1

            i += 1

        evaluation.criteria = Criteria(
            type="Pairwise Comparison",
            description="Comparison between two personalized versions of the book.",
            indicators=[],
            importance="high",
        )
        return_dict = {"evaluations": [evaluation]}

        return return_dict

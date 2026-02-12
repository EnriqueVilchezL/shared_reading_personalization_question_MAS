import copy
from typing import Annotated, Literal

from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import InjectedState

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from agents.personalization.coherence_critic import CoherenceCriticAgent
from agents.personalization.emotion_critic import EmotionCriticAgent
from agents.personalization.information import CriticInformation
from agents.personalization.moral_critic import MoralCriticAgent
from agents.personalization.naturalness_critic import NaturalnessCriticAgent
from agents.personalization.style_critic import StyleCriticAgent
from agents.personalization.value_critic import ValueCriticAgent
from domain.evaluation_aggregate.criteria import Criteria
from domain.services.book_renderer import BookMarkdownRenderer
from domain.services.evaluation_parser import EvaluationParser
from domain.services.evaluation_renderer import EvaluationMarkdownRenderer
from domain.services.preference_renderer import PreferenceMarkdownRenderer
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole


@tool
def request_deep_report_from_critics(
    aspects_to_evaluate: list[
        Literal[
            "coherence",
            "naturalness",
            "style",
            "the moral",
            "added narrative value",
            "emotional impact",
        ]
    ],
    state: Annotated[dict, InjectedState],
    config: RunnableConfig,
) -> str:
    """
    Requests an in-depth report from the critics on the specified aspects of a story personalization.

    Args:
        aspects_to_evaluate (list[str]): List of aspects to evaluate. It may include:
            - coherence
            - naturalness
            - style
            - the moral
            - added narrative value
            - emotional impact

    Returns:
        str: The critics’ comments on the evaluated aspects.
    """
    config = config["configurable"]

    agents_dict = {
        "coherence": CoherenceCriticAgent(
            LMConfiguration.model_validate(config["agents"]["coherence_critic"])
        ),
        "naturalness": NaturalnessCriticAgent(
            LMConfiguration.model_validate(config["agents"]["naturalness_critic"])
        ),
        "style": StyleCriticAgent(
            LMConfiguration.model_validate(config["agents"]["style_critic"])
        ),
        "the moral": MoralCriticAgent(
            LMConfiguration.model_validate(config["agents"]["moral_critic"])
        ),
        "added narrative value": ValueCriticAgent(
            LMConfiguration.model_validate(config["agents"]["value_critic"])
        ),
        "emotional impact": EmotionCriticAgent(
            LMConfiguration.model_validate(config["agents"]["emotion_critic"])
        ),
    }
    report_graph = StateGraph(state_schema=CriticInformation)

    for aspect in aspects_to_evaluate:
        agent = agents_dict.get(aspect)

        if agent:
            agent.roles.activate(DeepReviewCriticRole)
            agent.set_role_variables(
                {
                    "preferences": PreferenceMarkdownRenderer().render(
                        state.get("preferences", [])
                    )
                }
            )
            report_graph.add_node(agent.name, agent.instanciate())
            report_graph.add_edge(START, agent.name)

    report_graph_compiled = report_graph.compile()
    report_state = report_graph_compiled.invoke(
        input={
            "original_book": state.get("original_book", ""),
            "modified_book": state.get("modified_book", ""),
            "evaluations": [],
        }
    )

    renderer = EvaluationMarkdownRenderer()
    aggregated_evaluations = "# Reporte de evaluación de críticos:\n"
    for eval in report_state.get("evaluations", []):
        aggregated_evaluations += "---\n" + renderer.render(eval) + "\n"

    return aggregated_evaluations


@tool
def ask_critic(
    question: str,
    aspect: Literal[
        "coherence",
        "naturalness",
        "style",
        "the moral",
        "added narrative value",
        "emotional impact",
    ],
    state: Annotated[dict, InjectedState],
    config: RunnableConfig,
) -> str:
    """
    Asks a specific critic a question about one aspect of a story personalization.

    Args:
        question (str): The question to ask the critic.
        aspect (str): The critic’s aspect the question refers to. It can be one of:
            - coherence
            - naturalness
            - style
            - the moral
            - added narrative value
            - emotional impact

    Returns:
        str: The critic’s response to the question.
    """
    agents_dict = {
        "coherence": CoherenceCriticAgent(
            LMConfiguration.model_validate(config["agents"]["coherence_critic"])
        ),
        "naturalness": NaturalnessCriticAgent(
            LMConfiguration.model_validate(config["agents"]["naturalness_critic"])
        ),
        "style": StyleCriticAgent(
            LMConfiguration.model_validate(config["agents"]["style_critic"])
        ),
        "the moral": MoralCriticAgent(
            LMConfiguration.model_validate(config["agents"]["moral_critic"])
        ),
        "added narrative value": ValueCriticAgent(
            LMConfiguration.model_validate(config["agents"]["value_critic"])
        ),
        "emotional impact": EmotionCriticAgent(
            LMConfiguration.model_validate(config["agents"]["emotion_critic"])
        ),
    }

    deep_copy_state = copy.deepcopy(state)

    agent = agents_dict.get(aspect)

    if agent:
        agent.roles.activate(ConsultantCriticRole)
        agent.set_role_variables(
            {
                "preferences": PreferenceMarkdownRenderer().render(
                    state.get("preferences", {})
                )
            }
        )
        instantiated_agent = agent.instanciate()
        deep_copy_state = instantiated_agent.invoke(
            input=deep_copy_state | {"query": question}
        )

    return deep_copy_state["messages"][-1].content


class TriageCriticAgent(Agent):
    """
    Agent that evaluates responses based on user preferences.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="triage_critic",
            roles=[
                TriageCriticRole(
                    activities=[request_deep_report_from_critics, ask_critic]
                )
            ],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        super().pre_core(data)

        renderer = BookMarkdownRenderer()

        data["messages"].append(
            HumanMessage(
                "Porfavor, asigna una etiqueta a la personalización de este cuento.\n\n**Cuento original**:\n"
                + renderer.render(data.get("original_book", ""))
                + "\n\n**Cuento personalizado**:\n"
                + renderer.render(data.get("modified_book", ""))
            )
        )

        return data

    def post_core(self, data: dict) -> dict:
        super().post_core(data)
        last_message = data["messages"][-1].content

        evaluation = EvaluationParser().parse(last_message)
        evaluation.criteria = Criteria(
            type="calidad general de personalización",
            description="Evaluación general de la calidad de la personalización del cuento en función de las preferencias del usuario, considerando aspectos como coherencia, naturalidad, estilo, enseñanza, valor narrativo e impacto emocional.",
            indicators=[],
            importance="high",
        )
        return_dict = {"evaluations": [evaluation]}

        return return_dict

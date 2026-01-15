import copy
from typing import Annotated, Literal

from langchain.messages import HumanMessage
from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from agents.personalization.coherence_critic import CoherenceCriticAgent
from agents.personalization.emotion_critic import EmotionCriticAgent
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
from roles.personalization.triage_critic import TriageCriticRole


@tool
def pedir_reporte_profundo_a_criticos(
    aspectos_a_evaluar: list[
        Literal[
            "la coherencia",
            "la naturalidad",
            "el estilo",
            "la enseñanza",
            "el valor narrativo añadido",
            "el impacto emocional",
        ]
    ],
    state: Annotated[dict, InjectedState],
) -> str:
    """
    Pide un reporte profundo a los críticos sobre los aspectos especificados de una personalización de un cuento.

    Args:
        aspectos_a_evaluar (list[str]): Lista de aspectos a evaluar. Puede incluir:
            - la coherencia
            - la naturalidad
            - el estilo
            - la enseñanza
            - el valor narrativo añadido
            - el impacto emocional

    Returns:
        str: Los comentarios de los críticos sobre los aspectos evaluados.
    """
    agents_dict = {
        "la coherencia": CoherenceCriticAgent(),
        "la naturalidad": NaturalnessCriticAgent(),
        "el estilo": StyleCriticAgent(),
        "la enseñanza": MoralCriticAgent(),
        "el valor narrativo añadido": ValueCriticAgent(),
        "el impacto emocional": EmotionCriticAgent(),
    }

    evaluations = []

    deep_copy_state = copy.deepcopy(state)

    for aspecto in aspectos_a_evaluar:
        agent = agents_dict.get(aspecto)

        if agent:
            agent.roles.activate(DeepReviewCriticRole)
            agent.configure(
                {
                    "preferences": PreferenceMarkdownRenderer().render(
                        state.get("preferences", {})
                    )
                }
            )
            instanciated_agent = agent.instanciate()
            evaluation = instanciated_agent.invoke(input=deep_copy_state)
            evaluations.extend(evaluation.get("evaluations", []))

    renderer = EvaluationMarkdownRenderer()
    aggregated_evaluations = "# Reporte de evaluaciones de críticos:\n"
    for eval in evaluations:
        aggregated_evaluations += "---\n" + renderer.render(eval) + "\n"

    return aggregated_evaluations


@tool
def preguntar_a_critico(
    pregunta: str,
    aspecto: Literal[
        "la coherencia",
        "la naturalidad",
        "el estilo",
        "la enseñanza",
        "el valor narrativo añadido",
        "el impacto emocional",
    ],
    state: Annotated[dict, InjectedState],
) -> str:
    """
    Hace una pregunta a un crítico específico sobre un aspecto de la personalización de un cuento.

    Args:
        pregunta (str): La pregunta a hacer al crítico.
        aspecto (str): El aspecto del crítico al que se dirige la pregunta. Puede ser uno de:
            - la coherencia
            - la naturalidad
            - el estilo
            - la enseñanza
            - el valor narrativo añadido
            - el impacto emocional

    Returns:
        str: La respuesta del crítico a la pregunta.
    """
    agents_dict = {
        "la coherencia": CoherenceCriticAgent(),
        "la naturalidad": NaturalnessCriticAgent(),
        "el estilo": StyleCriticAgent(),
        "la enseñanza": MoralCriticAgent(),
        "el valor narrativo añadido": ValueCriticAgent(),
        "el impacto emocional": EmotionCriticAgent(),
    }

    deep_copy_state = copy.deepcopy(state)

    agent = agents_dict.get(aspecto)

    if agent:
        agent.roles.activate(ConsultantCriticRole)
        agent.configure(
            {
                "preferences": PreferenceMarkdownRenderer().render(
                    state.get("preferences", {})
                )
            }
        )
        instanciated_agent = agent.instanciate()
        deep_copy_state = instanciated_agent.invoke(
            input=deep_copy_state | {"query": pregunta}
        )

    return deep_copy_state["messages"][-1].content


class TriageCriticAgent(Agent):
    """
    Agent that evaluates responses based on user preferences.
    """

    def __init__(self):
        super().__init__(
            name="triage_critic",
            roles=[
                TriageCriticRole(
                    activities=[pedir_reporte_profundo_a_criticos, preguntar_a_critico]
                )
            ],
            lm_config=LMConfiguration(base_model="llama3.1:8b"),
        )

    def pre_core(self, data: dict) -> dict:
        data = super().pre_core(data)

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
        data = super().post_core(data)
        last_message = data["messages"][-1].content

        evaluation = EvaluationParser().parse(last_message)
        evaluation.criteria = Criteria(
            type="calidad general de personalización",
            description="Evaluación general de la calidad de la personalización del cuento en función de las preferencias del usuario, considerando aspectos como coherencia, naturalidad, estilo, enseñanza, valor narrativo e impacto emocional.",
            indicators=[],
        )
        return_dict = {"evaluations": [evaluation]}

        return return_dict

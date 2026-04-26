import itertools
import random
from collections import Counter
from typing import override

import numpy as np
from langgraph.graph.state import END, START
from langgraph.types import Send

from shared_reading_mas.agents.core.base_lm_config import LMConfiguration
from shared_reading_mas.agents.langfuse_organization import LangFuseOrganization
from shared_reading_mas.agents.personalization.edition_critic import EditionCriticAgent
from shared_reading_mas.agents.personalization.extractor import ExtractorAgent
from shared_reading_mas.agents.personalization.image_editor import ImageEditorAgent
from shared_reading_mas.agents.personalization.information import Information
from shared_reading_mas.agents.personalization.pair_critic import PairCriticAgent
from shared_reading_mas.agents.personalization.personalizer import PersonalizerAgent
from shared_reading_mas.agents.personalization.planner import PlannerAgent
from shared_reading_mas.domain.book_aggregate.book import Book
from shared_reading_mas.domain.services.image_editor import image_editor_factory
from shared_reading_mas.exceptions import OrganizationException
from shared_reading_mas.roles.personalization.personalizer import (
    PersonalizerEditorRole,
    PersonalizerRole,
)


class Organization(LangFuseOrganization):
    def __init__(self, configuration: dict = None):
        super().__init__(
            name="personalization_organization",
            information_schema=Information,
            configuration=configuration or {},
        )

    def _prepare_eval_payload(self, state: dict, book1: Book, book2: Book) -> dict:
        """Isolated payload for a single pair critic."""
        return {
            "preferences": state.get("preferences", []),
            "original_book": state.get("original_book"),
            "intermediate_books": [book1, book2],
        }

    def get_number_of_evaluations(self) -> int:
        """
        Determines the number of evaluations based on the evaluation mode.

        Returns:
            int: The number of evaluations to be performed.
        """
        num_generations = self.configuration.get("num_generations", 0)
        num_evals = self.configuration.get("num_evaluations", 0)
        mode = self.configuration.get("evaluation_mode", "random")

        # If exhaustive evaluation is requested
        match mode:
            case "product" | "products":
                num_evals = num_generations * num_generations

            case "permutation" | "permutations":
                num_evals = num_generations * (num_generations - 1)

            case "combination" | "combinations":
                num_evals = num_generations * (num_generations - 1) // 2

            case "random" | "randoms":
                pass

            case _:
                raise OrganizationException(f"Unknown evaluation mode: {mode}")

        return num_evals

    def get_evaluation_pairs(self, books: list[Book]) -> list[tuple[Book, Book]]:
        """
        Generates book pairs based on the evaluation mode.

        Args:
            books (list[Book]): List of books to generate pairs from.

        Returns:
            list[tuple[Book, Book]]: List of book pairs for evaluation.
        """
        num_evals = self.configuration.get("num_evaluations", 0)
        mode = self.configuration.get("evaluation_mode", "random")

        book_pairs = []
        # If exhaustive evaluation is requested
        match mode:
            case "product" | "products":
                book_pairs = list(itertools.product(books, repeat=2))

            case "permutation" | "permutations":
                book_pairs = list(itertools.permutations(books, 2))

            case "combination" | "combinations":
                book_pairs = list(itertools.combinations(books, 2))

            case "random" | "randoms":
                while len(book_pairs) < num_evals:
                    pair = tuple(random.sample(books, 2))
                    if pair not in book_pairs:
                        book_pairs.append(pair)

            case _:
                raise OrganizationException(f"Unknown evaluation mode: {mode}")

        return book_pairs

    def route_edition(self, state: dict) -> str:
        """Routes to the personalization editor after evaluations."""

        last_evaluation = state.get("evaluations", [])[-1]
        if not (
            "cumple parcialmente" in last_evaluation.label.lower()
            or "no cumple" in last_evaluation.label.lower()
        ):
            return "end_text_personalization"

        else:
            return "personalizer_editor"

    def collect_books(self, state: dict):
        return {"original_book": state.get("original_book")}

    def distribute_evaluations(self, state: dict) -> list[Send]:
        """A conditional router that dispatches isolated book pairs to critics."""
        books = state.get("intermediate_books", [])

        book_pairs = self.get_evaluation_pairs(books)
        final_routing = [
            Send(f"pair_critic_eval_{i + 1}", self._prepare_eval_payload(state, b1, b2))
            for i, (b1, b2) in enumerate(book_pairs)
        ]
        return final_routing

    def merge_evaluations(self, state: dict) -> dict:
        """Aggregates results from all parallel evaluations."""
        evaluations = state.get("evaluations", [])
        intermediate_books = state.get("intermediate_books", [])

        if not evaluations:
            return {"modified_book": None}

        win_counts = Counter(e.label for e in evaluations)
        print(win_counts)
        winning_uid = win_counts.most_common(1)[0][0]

        winning_book = next(
            (book for book in intermediate_books if str(book.uid) == winning_uid), None
        )
        return {"modified_book": winning_book}

    def end_text_personalization(self, state: dict) -> dict:
        """Final node of the organization, returns the modified book."""
        return {"modified_book": state.get("modified_book")}

    def route_images_personalization(self, state: dict) -> dict:
        """Final node of the organization, returns the modified book."""
        # Verify if it has images
        original_book = state.get("original_book")

        if original_book.has_images(include_front_page_image=True):
            return "image_editor"

        else:
            return END

    @override
    def instantiate(self):
        agents_config = self.configuration["agents"]
        num_generations = self.configuration["num_generations"]
        num_evals = self.get_number_of_evaluations()

        self._add_core_nodes()

        self._add_personalizers(
            agents_config["personalizer"],
            num_generations,
        )

        critic_names = self._add_pair_critics(
            agents_config["pair_critic"],
            num_evals,
        )

        self._wire_collector_to_critics(critic_names)
        self._add_post_evaluation_pipeline(agents_config)
        self._add_image_editing_pipeline(agents_config)

        return self._core_graph.compile()

    def _add_image_editing_pipeline(self, agents_config):
        # Image editor
        editor_config = LMConfiguration.model_validate(agents_config["image_editor"])
        editing_service_config = LMConfiguration.model_validate(agents_config["image_editing_service"])

        image_editing_service = image_editor_factory(
            editor=editing_service_config.base_provider, configuration=editing_service_config.model_dump()
        )
        image_editor = ImageEditorAgent(image_editing_service, editor_config)
        image_editor.name = "image_editor"
        self.add_agent(image_editor)

        # Connect it to the edition critic
        self._core_graph.add_edge("image_editor", END)

    def _add_core_nodes(self):
        self._core_graph.add_node("collector", self.collect_books)
        self._core_graph.add_node("merge_evaluations", self.merge_evaluations)
        self._core_graph.add_node("end_text_personalization", self.end_text_personalization)

    def _add_personalizers(self, personalizer_cfg, num_generations):
        temperatures = self._sample_temperatures(num_generations)

        # extractor_agent = self._build_extractor(
        #     extractor_cfg,
        #     name="extractor",
        # )
        # self.add_agent(extractor_agent)
        # self._core_graph.add_edge(START, extractor_agent.name)

        agents = []
        for i, temp in enumerate(temperatures):
            # planner_agent = self._build_planner(
            #     planner_cfg,
            #     temperature=float(temp),
            #     name=f"planner_gen_{i + 1}",
            # )

            agent = self._build_personalizer(
                personalizer_cfg,
                temperature=float(temp),
                name=f"personalizer_gen_{i + 1}",
            )

            self.add_agent(agent)
            # self.add_agent(planner_agent)
            # self._core_graph.add_edge(extractor_agent.name, agent.name)
            # self._core_graph.add_edge(planner_agent.name, agent.name)
            self._core_graph.add_edge(START, agent.name)
            agents.append(agent.name)

        self._core_graph.add_edge(agents, "collector")

    def _build_planner(self, cfg, temperature, name):
        config = LMConfiguration.model_validate(cfg)
        config.temperature = temperature

        agent = PlannerAgent(config)
        agent.name = name
        agent.set_role_variables(self._agents_variables.get("planner", {}))
        return agent

    def _build_personalizer(self, cfg, temperature, name):
        config = LMConfiguration.model_validate(cfg)
        config.temperature = temperature

        agent = PersonalizerAgent(config)
        agent.name = name
        agent.set_role_variables(self._agents_variables.get("personalizer", {}))
        agent.roles.activate(PersonalizerRole)
        return agent

    def _build_extractor(self, cfg, name):
        config = LMConfiguration.model_validate(cfg)

        agent = ExtractorAgent(config)
        agent.name = name
        agent.set_role_variables(self._agents_variables.get("extractor", {}))
        return agent

    def _sample_temperatures(self, num_generations):
        min_temp, max_temp = self.configuration.get("temperatures", [0.5, 1.5])
        return np.random.normal(
            np.linspace(min_temp, max_temp, num_generations),
            (1 / (2 ** (num_generations - 1))),
        ).clip(0, 2)

    def _add_pair_critics(self, pair_critic_cfg, num_evals):
        critic_names = []

        for i in range(num_evals):
            agent = self._build_pair_critic(
                pair_critic_cfg,
                name=f"pair_critic_eval_{i + 1}",
            )
            critic_names.append(agent.name)

            self.add_agent(agent)
            self._core_graph.add_edge(agent.name, "merge_evaluations")

        return critic_names

    def _build_pair_critic(self, cfg, name):
        config = LMConfiguration.model_validate(cfg)

        agent = PairCriticAgent(config)
        agent.name = name
        agent.set_role_variables(self._agents_variables.get("pair_critic", {}))
        return agent

    def _wire_collector_to_critics(self, critic_names):
        self._core_graph.add_conditional_edges(
            "collector",
            self.distribute_evaluations,
            {name: name for name in critic_names},
        )

    def _add_post_evaluation_pipeline(self, agents_config):
        # Edition critic
        edition_critic_config = LMConfiguration.model_validate(
            agents_config["edition_critic"]
        )
        self.add_agent(EditionCriticAgent(edition_critic_config))

        # Personalization editor
        editor_config = LMConfiguration.model_validate(agents_config["personalizer"])
        editor = PersonalizerAgent(editor_config)
        editor.name = "personalizer_editor"
        editor.roles.activate(PersonalizerEditorRole)
        editor.set_role_variables(self._agents_variables.get("personalizer", {}))
        self.add_agent(editor)

        self._core_graph.add_edge("merge_evaluations", "edition_critic")

        self._core_graph.add_conditional_edges(
            "edition_critic",
            self.route_edition,
            {
                "personalizer_editor": "personalizer_editor",
                "end_text_personalization": "end_text_personalization",
            },
        )

        self._core_graph.add_conditional_edges(
            "end_text_personalization",
            self.route_images_personalization,
            {
                "image_editor": "image_editor",
                END: END,
            },
        )

        self._core_graph.add_edge("personalizer_editor", "end_text_personalization")

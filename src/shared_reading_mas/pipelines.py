from shared_reading_mas.agents.combined.organization import (
    Organization as CombinedOrganization,
)
from shared_reading_mas.agents.personalization.organization import (
    Organization as PersonalizationOrganization,
)
from shared_reading_mas.agents.questions.organization import (
    Organization as QuestionsOrganization,
)
from shared_reading_mas.domain.book_aggregate.book import Book
from shared_reading_mas.domain.preference_aggregate.preference import Preference
from shared_reading_mas.domain.services.preference_renderer import (
    PreferenceMarkdownRenderer,
)


async def run_personalization_pipeline(
    story: Book, preferences: list[Preference], configuration: dict = {}, verbose: bool = False
) -> Book:
    """
    Runs the personalization pipeline on a given story with user preferences.

    Args:
        story (Book): The original story to be personalized.
        preferences (list[Preference]): The user reading preferences.
        configuration (dict): Configuration for the organization.
        verbose (bool): If True, prints detailed output during the process.

    Returns:
        Book: The personalized version of the story.
    """
    organization = PersonalizationOrganization(configuration=configuration)
    organization.set_agents_variables(
        {
            "personalizer": {
                "preferences": PreferenceMarkdownRenderer().render(preferences)
            },
            "pair_critic": {
                "preferences": PreferenceMarkdownRenderer().render(preferences)
            },
            "edition_critic": {
                "preferences": PreferenceMarkdownRenderer().render(preferences)
            },
        }
    )

    graph = organization.instantiate()

    final_state = {}

    async for step in graph.astream(
        input={"original_book": story, "preferences": preferences},
        config=organization.configuration,
    ):
        for update in step.values():
            final_state.update(update)
            if verbose:
                for message in update.get("messages", []):
                    message.pretty_print()

    return final_state["modified_book"]

async def run_questions_pipeline(story: Book, configuration: dict = {}, verbose: bool = False) -> Book:
    """
    Runs the question generation pipeline on a given story.

    Args:
        story (Book): The story for which to generate questions.
        configuration (dict): Configuration for the organization.
        verbose (bool): If True, prints detailed output during the process.

    Returns:
        Book: The story with generated questions.
    """
    organization = QuestionsOrganization(configuration=configuration)

    graph = organization.instantiate()

    final_state = {}

    async for step in graph.astream(
        input={"original_book": story},
        config=organization.configuration,
    ):
        for update in step.values():
            final_state.update(update)
            if verbose:
                for message in update.get("messages", []):
                    message.pretty_print()

    return final_state["modified_book"]

async def run_combined_pipeline(
        story: Book, preferences: list[Preference], configuration: dict = {}, verbose: bool = False
    ) -> Book:
    """
    Runs the combined generation pipeline on a given story.

    Args:
        story (Book): The original story to be personalized.
        preferences (list[Preference]): The user reading preferences.
        configuration (dict): Configuration for the organization.
        verbose (bool): If True, prints detailed output during the process.

    Returns:
        Book: The story with generated questions.
    """
    organization = CombinedOrganization(configuration=configuration)

    organization.set_agents_variables(
        {
            "combined": {
                "preferences": PreferenceMarkdownRenderer().render(preferences)
            }
        }
    )

    graph = organization.instantiate()

    final_state = {}

    async for step in graph.stream(
        input={"original_book": story},
        config=organization.configuration,
    ):
        for update in step.values():
            final_state.update(update)
            if verbose:
                for message in update.get("messages", []):
                    message.pretty_print()

    return final_state["modified_book"]

async def run_pipelines(
    story: Book, preferences: list[Preference], pipeline: str, configuration: dict = {},verbose: bool = False
) -> Book:
    """
    Runs the specified pipelines on a given story with user preferences.

    Args:
        story (Book): The original story to be processed.
        preferences (list[Preference]): The user reading preferences.
        pipeline (str): The pipeline to run. It can be "ALL", "PERSONALIZATION", or "QUESTIONS".
        configuration (dict): Configuration for the organizations.
        verbose (bool): If True, prints detailed output during the process.

    Returns:
        Book: The processed version of the story.
    """
    if pipeline == "ALL":
        story = await run_personalization_pipeline(story, preferences, configuration["organizations"]["personalization"], verbose)
        story = await run_questions_pipeline(story, configuration["organizations"]["questions"], verbose)
    elif pipeline == "PERSONALIZATION":
        story = await run_personalization_pipeline(story, preferences, configuration["organizations"]["personalization"], verbose)
    elif pipeline == "QUESTIONS":
        story = await run_questions_pipeline(story, configuration["organizations"]["questions"], verbose)
    elif pipeline == "SINGLE":
        story = await run_combined_pipeline(story, preferences, configuration["organizations"]["combined"], verbose)

    return story

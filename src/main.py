from argparse import ArgumentParser

from dotenv import load_dotenv

from agents.personalization.organization import (
    Organization as PersonalizationOrganization,
)
from agents.questions.organization import Organization as QuestionsOrganization
from domain.book_aggregate.book import Book
from domain.preference_aggregate.preference import Preference
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from domain.services.preference_parser import PreferenceParser
from domain.services.preference_renderer import PreferenceMarkdownRenderer
from utils import load_json_file, load_md_file, write_to_md_file

load_dotenv()


def run_personalization_pipeline(
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
        }
    )

    graph = organization.instantiate()

    final_state = {}

    for step in graph.stream(
        input={"original_book": story, "preferences": preferences},
        config=organization.configuration,
    ):
        for update in step.values():
            final_state.update(update)
            if verbose:
                for message in update.get("messages", []):
                    message.pretty_print()

    return final_state["modified_book"]

def run_questions_pipeline(story: Book, configuration: dict = {}, verbose: bool = False) -> Book:
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

    for step in graph.stream(
        input={"original_book": story},
        config=organization.configuration,
    ):
        for update in step.values():
            final_state.update(update)
            if verbose:
                for message in update.get("messages", []):
                    message.pretty_print()

    return final_state["modified_book"]


def run_pipelines(
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
        story = run_personalization_pipeline(story, preferences, configuration["organizations"]["personalization"], verbose)
        story = run_questions_pipeline(story, configuration["organizations"]["questions"], verbose)
    elif pipeline == "PERSONALIZATION":
        story = run_personalization_pipeline(story, preferences, configuration["organizations"]["personalization"], verbose)
    elif pipeline == "QUESTIONS":
        story = run_questions_pipeline(story, configuration["organizations"]["questions"], verbose)

    return story


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--story_path", help="The path to the MD file with the story", required=True
    )
    parser.add_argument(
        "--preferences_path",
        help="The path to the MD file with the preferences",
        required=True,
    )
    parser.add_argument("--output_path", help="The output path", default="output.md")
    parser.add_argument(
        "--pipelines",
        help="The pipelines to run",
        choices=["ALL", "PERSONALIZATION", "QUESTIONS"],
        default="ALL",
        type=str.upper,
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output", default=False
    )

    args = parser.parse_args()

    story_str = load_md_file(args.story_path)
    preferences_str = load_md_file(args.preferences_path)
    configuration = load_json_file("config.json")

    story = BookParser().parse(story_str)
    preferences = PreferenceParser().parse(preferences_str)
    modified_story = run_pipelines(story, preferences, args.pipelines, configuration, args.verbose)

    write_to_md_file(args.output_path, BookMarkdownRenderer().render(modified_story))

main()

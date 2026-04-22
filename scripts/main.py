from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv

from shared_reading_mas.domain.services.book_parser import BookParser
from shared_reading_mas.domain.services.book_renderer import BookMarkdownRenderer
from shared_reading_mas.domain.services.preference_parser import PreferenceParser
from shared_reading_mas.pipelines import run_pipelines
from shared_reading_mas.utils import load_json_file

load_dotenv()

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
        choices=["ALL", "PERSONALIZATION", "QUESTIONS", "SINGLE"],
        default="ALL",
        type=str.upper,
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output", default=False
    )

    args = parser.parse_args()

    story_path = Path(args.story_path)
    profile_path = Path(args.preferences_path)
    output_path = Path(args.output_path)
    configuration = load_json_file("config.json")["cloud"]

    story = BookParser(from_path=story_path).parse()
    preferences = PreferenceParser(from_path=profile_path).parse()
    modified_story = run_pipelines(story, preferences, args.pipelines, configuration, args.verbose)

    BookMarkdownRenderer(to_path=output_path, include_images=True).render(modified_story)

main()

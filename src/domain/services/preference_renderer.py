from domain.preference_aggregate.preference import Preference


class PreferenceMarkdownRenderer:
    """
    Service responsible for converting Preference domain objects into Markdown.
    Follows the Single Responsibility Principle.
    """

    def render(self, preferences: list[Preference]) -> str:
        """Orchestrates the rendering of the entire preferences list.

        Args:
            preferences (list[Preference]): List of user preferences.

        Returns:
            str: Markdown representation of the preferences.
        """
        dictionary = {pref.type: [] for pref in preferences}
        for preference in preferences:
            dictionary[preference.type].append(preference.value)

        md_output = [""]

        for preference_type, values in dictionary.items():
            md_output.append(f"- **{preference_type}**: {', '.join(values)}")

        md_output.append("\n")
        return "\n".join(md_output)

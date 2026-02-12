from domain.evaluation_aggregate.evaluation import Criteria


class CriteriaMarkdownRenderer:
    """
    Service responsible for converting Evaluation domain objects into Markdown.
    Follows the Single Responsibility Principle.
    """

    def __init__(self):
        pass

    def render(self, criteria: Criteria, indicators: bool = True) -> str:
        """Orchestrates the rendering of the entire evaluation."""
        md_output = f"**Criteria**: {criteria.type} -> {criteria.description} (importance: {criteria.importance})\n"

        if indicators:
            for indicator in criteria.indicators:
                md_output += f"   - {indicator}\n"

        return md_output

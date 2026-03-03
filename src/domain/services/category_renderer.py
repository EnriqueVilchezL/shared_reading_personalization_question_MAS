from domain.evaluation_aggregate.evaluation import Category


class CategoriesMarkdownRenderer:
    """
    Service responsible for converting Category domain objects into Markdown.
    """

    def __init__(self):
        pass

    def render(self, category: Category, indicators: bool = True) -> str:
        """Orchestrates the rendering of the entire category.

        Args:
            category (Category): The category to render.
            indicators (bool): Whether to include indicators in the rendering.

        Returns:
            str: The rendered Markdown string for the category.
        """
        md_output = f"**{category.type.capitalize()}**: {category.description} (importance: {category.importance})\n"

        if indicators:
            for indicator in category.indicators:
                md_output += f"   - {indicator}\n"

        return md_output

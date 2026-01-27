from lark import Lark, Transformer

from domain.preference_aggregate.preference import Preference


class PreferenceTransformer(Transformer):
    """
    Transforms a Lark parse tree into a list of Preference objects.
    """

    def preference_line(self, items):
        """
        items[0] -> TYPE token
        items[1] -> LINE token (optional)
        """
        pref_type = items[0].value.strip()
        values_str = items[1].value.strip() if len(items) > 1 else ""
        if not values_str:
            return []  # skip lines with no values
        # Split by comma and remove empty entries
        values = [v.strip() for v in values_str.split(",") if v.strip()]
        return [Preference(type=pref_type, value=v) for v in values]

    def start(self, items):
        # Flatten list of lists into a single list
        return [pref for sublist in items for pref in sublist]


# -------------------- Preference Parser --------------------
class PreferenceParser:
    """
    Parser for Markdown preference lists into Preference objects.
    Example Markdown input:
        - **Animal**: Gato, Conejo
        - **Color**: Azul, Verde
        - **Deporte**: Futbol
    """

    _GRAMMAR = r"""
        start: preference_line+

        # Matches lines like: - **Animal**: Gato, Conejo
        # LINE is optional
        preference_line: "- " "**" TYPE "**" ":" WS* [LINE]

        TYPE: /[^\*]+/
        LINE: /[^\n]+/

        %import common.WS
        %ignore WS
    """

    def __init__(self):
        self._lark = Lark(self._GRAMMAR, parser="earley")
        self._transformer = PreferenceTransformer()

    def parse(self, text: str) -> list[Preference]:
        """
        Parse the markdown text and return a list of Preference objects.
        """
        tree = self._lark.parse(text)
        return self._transformer.transform(tree)

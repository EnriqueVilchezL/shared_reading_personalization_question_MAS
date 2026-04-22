from pathlib import Path

from lark import Lark, Transformer

from domain.preference_aggregate.preference import Preference


class PreferenceTransformer(Transformer):
    """
    Transforms a Lark parse tree into a list of Preference objects.
    """

    def preference_line(self, items):
        # items[0] -> TYPE
        # items[1] -> LINE
        pref_type = items[0].value.strip()
        values_str = items[1].value.strip()

        if not values_str:
            return []

        values = [v.strip() for v in values_str.split(",") if v.strip()]
        return [Preference(type=pref_type, preference=v) for v in values]

    def start(self, items):
        # Flatten list of lists
        return [pref for sublist in items for pref in sublist]


# -------------------- Parser --------------------
class PreferenceParser:
    """
    Parser for Markdown preference lists.

    Example input:
        - **Animal**: Gato, Conejo
        - **Color**: Azul, Verde
        - **Deporte**: Futbol
    """

    _GRAMMAR = r"""
        start: preference_line+

        preference_line: "- **" TYPE "**:" LINE

        TYPE: /[^*\n]+/
        LINE: /[^\n]+/

        %import common.NEWLINE
        %ignore NEWLINE
        %ignore " "
    """

    def __init__(self, from_path: Path | None = None):
        self._lark = Lark(self._GRAMMAR, parser="earley")
        self._transformer = PreferenceTransformer()
        self.from_path = from_path

    def parse(self, text: str | None = None) -> list[Preference]:
        if not text and self.from_path:
            text = self.from_path.read_text(encoding="utf-8")

        tree = self._lark.parse(text)
        return self._transformer.transform(tree)

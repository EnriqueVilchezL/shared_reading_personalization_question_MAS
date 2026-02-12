from lark import Lark, Transformer

from domain.evaluation_aggregate.evaluation import Evaluation


class EvaluationTransformer(Transformer):
    def label(self, items):
        # items[1:] = content lines
        return ("Label", "\n".join(line.value.strip() for line in items[1:]))

    def reasoning(self, items):
        return ("Reasoning", "\n".join(line.value.strip() for line in items[1:]))

    def changes(self, items):
        return ("Changes", "\n".join(line.value.strip() for line in items[1:]))

    def evaluation_block(self, items):
        label_val = ""
        reasoning_val = ""
        changes_val = ""
        for item in items:
            key, value = item
            if key == "Label":
                label_val = value
            elif key == "Reasoning":
                reasoning_val = value
            elif key == "Changes":
                changes_val = value
        return Evaluation(
            label=label_val,
            reasoning=reasoning_val,
            changes=changes_val,
            criteria=None,
        )

    def start(self, items):
        return items[0] if items else None

class EvaluationParser:
    _GRAMMAR = r"""
        start: evaluation_block

        evaluation_block: label reasoning? changes?

        label: LABEL_HEADER LINE+
        reasoning: REASONING_HEADER LINE+
        changes: CHANGES_HEADER LINE+

        LABEL_HEADER: BOLD? ("Etiqueta" | "Calidad" | "Etiqueta asignada" | "Respuesta" | "Answer") BOLD? ":"
        REASONING_HEADER: BOLD? "Razonamiento" BOLD? ":"
        CHANGES_HEADER: BOLD? ("Cambios" | "Cambios sugeridos" | "Cambios requeridos" | "Cambios recomendados") BOLD? ":"

        BOLD: "**"

        LINE: /[^\n]+/

        %import common.WS
        %ignore WS
    """

    def __init__(self):
        self._lark = Lark(self._GRAMMAR, parser="earley")
        self._transformer = EvaluationTransformer()

    def parse(self, text: str) -> Evaluation:
        tree = self._lark.parse(text)
        return self._transformer.transform(tree)

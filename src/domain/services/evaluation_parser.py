from lark import Lark, Transformer

from domain.evaluation_aggregate.evaluation import Evaluation


class EvaluationTransformer(Transformer):
    """
    Convierte el árbol de Lark en un objeto Evaluation.
    Extrae los valores de cada sección y elimina la primera línea de encabezado.
    """

    def reasoning(self, items):
        # items: first element = header, rest = LINE tokens
        lines = [line.value.strip() for line in items[1:]]  # skip header
        return "\n".join(lines).strip()

    def label(self, items):
        lines = [line.value.strip() for line in items[1:]]  # skip header
        return "\n".join(lines).strip()

    def changes(self, items):
        lines = [line.value.strip() for line in items[1:]]  # skip header
        return "\n".join(lines).strip()

    def evaluation_block(self, items):
        """
        items = [label, reasoning?, changes?]
        """
        label_val = items[0] if len(items) > 0 else ""
        reasoning_val = items[1] if len(items) > 1 else ""
        changes_val = items[2] if len(items) > 2 else ""

        return Evaluation(
            label=label_val,
            reasoning=reasoning_val,
            changes=changes_val,
            criteria=None
        )

    def start(self, items):
        return items[0] if items else None


class EvaluationParser:
    """
    Parser de texto a Evaluation usando Lark.
    Label primero, luego reasoning opcional y changes opcional.
    """

    _GRAMMAR = r"""
        start: evaluation_block

        evaluation_block: label reasoning? changes?

        reasoning: REASONING_HEADER LINE+
        label: LABEL_HEADER LINE+
        changes: CHANGES_HEADER LINE+

        STARSTAR: "**"
        REASONING_HEADER: STARSTAR? "Razonamiento" STARSTAR? ":"
        LABEL_HEADER: STARSTAR? ("Calidad" | "Etiqueta" | "Etiqueta asignada") STARSTAR? ":"
        CHANGES_HEADER: STARSTAR? "Cambios sugeridos" STARSTAR? ":"

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

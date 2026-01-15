from domain.evaluation_aggregate.evaluation import Evaluation


class EvaluationMarkdownRenderer:
    """
    Service responsible for converting Evaluation domain objects into Markdown.
    Follows the Single Responsibility Principle.
    """

    def __init__(self):
        pass

    def render(self, evaluation: Evaluation) -> str:
        """Orchestrates the rendering of the entire evaluation."""
        md_output = f"**Criterio**: {evaluation.criteria.type}\n\n"
        md_output += f"- Descripción de criterio: {evaluation.criteria.description}\n"
        md_output += f"- Etiqueta: {evaluation.label}\n"

        if evaluation.changes or evaluation.changes != "":
            md_output += f"- Cambios recomendados: {evaluation.changes or 'Ninguno'}\n"

        if evaluation.reasoning or evaluation.reasoning != "":
            md_output += f"- Razonamiento: {evaluation.reasoning or 'Ninguno'}\n"
        return md_output

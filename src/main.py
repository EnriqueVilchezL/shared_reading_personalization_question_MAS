from dotenv import load_dotenv

from agents.personalization.organization import Organization
from domain.preference_aggregate.preference import Preference
from domain.services.book_parser import BookParser
from domain.services.preference_renderer import PreferenceMarkdownRenderer

load_dotenv()

organization = Organization()
preferences = [
    Preference(type="Animal", preference="Gato"),
    Preference(type="Animal", preference="Conejo"),
    Preference(type="Color", preference="Azul"),
    Preference(type="Color", preference="Verde"),
    Preference(type="Juego", preference="Pelota"),
    Preference(type="Juego", preference="Rompecabezas"),
]
book_str = """
# El zorro de fuego
---
Érase una vez un joven y fuerte agricultor que una noche volvía tarde del mercado. Su camino le llevó junto a los jardines de un rico caballero, en los que se alzaban varios edificios altos. De repente vio algo brillante flotando en el aire dentro de los jardines, algo que brillaba como una bola de cristal. Asombrado, escaló el muro que rodeaba los jardines, pero no había ningún ser humano a la vista; todo lo que vio fue, a lo lejos, algo que parecía ser un perro, mirando a la luna. Y cada vez que exhalaba el aliento, una bola de fuego salía de su boca y se elevaba hacia la luna. Y cuando inspiraba, la bola se hundía de nuevo y la atrapaba entre sus fauces. Y así siguió sin parar.
---
Entonces el granjero se dio cuenta de que era un zorro, que estaba preparando el elixir de la vida. Se escondió entre la hierba y esperó a que la bola de fuego volviera a bajar, a la altura de su propia cabeza. Entonces salió apresuradamente de su escondite, se la llevó y se la tragó de inmediato. La sintió brillar mientras bajaba por su garganta hasta el estómago. Cuando el zorro vio lo que había ocurrido, se enfureció. Miró furioso al granjero, pero temía su fuerza. Por eso no se atrevió a atacarle, sino que siguió furioso su camino.
---
A partir de entonces, el campesino podía hacerse invisible, ver fantasmas y demonios y relacionarse con el mundo de los espíritus. En caso de enfermedad, cuando la gente yacía inconsciente, podía llamar a sus almas, y si alguien había cometido un pecado, podía abogar por ellos. Gracias a estos dones ganaba mucho dinero.
---
Cuando llegó a los cincuenta años, se retiró de todo y ya no quiso ejercer sus artes. Una noche de verano estaba sentado en su patio, disfrutando del aire fresco. Bebió varias copas de vino y a medianoche se quedó profundamente dormido. De repente se despertó, sintiéndose mal. Parecía como si alguien le diera una palmada en la espalda y, antes de que se diera cuenta, la bola de fuego había saltado de su garganta.
---
En seguida una mano lo alcanzó y una voz dijo: "Durante treinta largos años me ocultaste mi tesoro, y de pobre campesino has pasado a ser un hombre rico. Ahora ya tienes bastante, y me gustaría volver a tener mi bola de fuego". Entonces el hombre supo lo que había pasado, pero el zorro se había ido.

"""

book = BookParser().parse(book_str)

organization.set_agents_configuration(
    {
        "personalizer": {
            "preferences": PreferenceMarkdownRenderer().render(preferences)
        },
        "triage_critic": {
            "preferences": PreferenceMarkdownRenderer().render(preferences)
        },
    }
)

graph = organization.instantiate()

for step in graph.stream(
    input={"original_book": book, "preferences": preferences},
    config=organization.configuration,
):
    for update in step.values():
        for message in update.get("messages", []):
            message.pretty_print()

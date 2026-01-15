from domain.services.evaluation_parser import EvaluationParser

parser = EvaluationParser()
evaluation = parser.parse("""Calidad: De acuerdo
Razonamiento: El cuento personalizado mantiene la estructura narrativa coherente del original, integrando los elementos personalizados (gato azul, coneja verde, pelota verde y rompecabezas). El desarrollo tiene inicio, nudo y desenlace definidos, con una secuencia causa-efecto clara (Azul toma la bola verde, gana dones, los usa y luego la pierde). Sin embargo, la repetición de la última escena (el final del cuento se presenta dos veces) introduce una redundancia que podría confundir al lector. Además, la descripción del movimiento de la bola verde y las acciones de los personajes son consistentes con el contexto establecido. La coherencia general es sólida, aunque el final repetido sugiere una mejora mínima para evitar ambigüedad.
Cambios sugeridos: Eliminar una de las dos repeticiones del final del cuento para evitar redundancia y asegurar que el desenlace sea único y claro.
""")
print(evaluation)

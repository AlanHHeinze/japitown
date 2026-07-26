# Elecciones dentro de quests que NO pasan por el `menu:` de Ren'Py.
#
# Las opciones de un `menu:` normal las extrae `renpy translate` sola. Estas NO:
#
#   1. SCREENS de elección propios (textbutton dentro de un `screen`).
#      Ren'Py sí las traduce al mostrarlas, pero hay que declarar el `old` acá
#      porque el comando `translate` no las genera.
#
#   2. Opciones armadas en PYTHON (listas de strings).
#      Ver VQ9A_PEDIDOS en violet_quest_09_a.rpy: el valor elegido se GUARDA en el
#      save y se usa como clave de comparación en varios labels, asi que la variable
#      queda siempre en español y solo se traduce al mostrarla (vq9a_pedido_texto()).
#      NO traducir el valor guardado: rompe las comparaciones.

translate english strings:

    # =========================================================================
    # Selector de respuesta del chat (hud_mensajes.rpy)
    # =========================================================================

    old "✖ Cancelar"
    new "✖ Cancel"

    # =========================================================================
    # Evento 03 de Violet — qué pensaba mientras limpiaba
    # =========================================================================

    old "En qué me estoy acostumbrando a volver a vivir aquí"
    new "About how I'm getting used to living here again"

    old "Me acordaba cuando inventábamos excusas para no ordenar y Monica se enojaba"
    new "I was remembering how we'd make up excuses to avoid tidying up and Monica would get mad"

    old "Pensaba en que te queda muy sexy ese pijama"
    new "I was thinking about how sexy you look in those pajamas"

    # =========================================================================
    # Quest 05 de Violet — golpear la puerta
    # =========================================================================

    old "Golpear"
    new "Knock"

    # =========================================================================
    # Quest 05_c de Violet — la disculpa
    # =========================================================================

    old "Espero que en algún momento me creas"
    new "I hope you'll believe me at some point"

    old "Confesión  💬 (3 de carisma)"
    new "Confession  💬 (3 Charisma)"

    # =========================================================================
    # Quest 06_b de Violet — la prueba del cosplay
    # =========================================================================

    old "Bajar el cierre"
    new "Pull the zipper down"

    old "Forzar el cierre  💪 (3 de fuerza)"
    new "Force the zipper  💪 (3 Strength)"

    # =========================================================================
    # Quest 08_a de Violet — el baño
    # =========================================================================

    old "Dejar la ropa aca"
    new "Leave the clothes here"

    old "Acercarse  🎯 (3 de destreza)"
    new "Get closer  🎯 (3 Dexterity)"

    # =========================================================================
    # Quest 09_a de Violet — los pedidos de Violet enferma (VQ9A_PEDIDOS)
    # OJO: son CLAVES de comparación. Traducir solo la visualización.
    # =========================================================================

    old "Quiero algo de comer"
    new "I want something to eat"

    old "Necesito tomar el medicamento"
    new "I need to take my medicine"

    old "Un poco de agua"
    new "Some water"

    old "Dile a Monica que venga"
    new "Tell Monica to come"

    old "Tráeme una toalla"
    new "Bring me a towel"

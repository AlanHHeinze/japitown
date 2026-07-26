# Mensaje de entrada a una locación durante el recorrido de la Quest 0 del MC.
# Se arma en mc_q0_mensaje_ubicacion() / mc_q0_mensaje_faltantes() (mc_quest_0_a.rpy)
# via renpy.translate_string().
#
# OJO: el área de texto muestra 4 renglones. Las pistas de "cómo llegar" tienen que
# entrar en UNA línea cada una — si se alargan, envuelven y el mensaje se corta.
#
# NOTA: "Patio" ya está traducida en tl/english/script/core/locations/locations_house.rpy
# (un mismo `old` duplicado hace crashear a Ren'Py), por eso no está acá.

translate english strings:

    old "Esto es"
    new "This is"

    old "Locaciones faltantes a visitar, todas desde el Living:"
    new "Locations left to visit, all from the Living Room:"

    old "Pasillo arriba"
    new "Upstairs Hallway"

    old "Pasillo abajo"
    new "Downstairs Hallway"

    old "por la escalera"
    new "through the stairs"

    old "por la flecha de abajo a la izquierda"
    new "through the arrow at the bottom left"

    old "por el ventanal del centro"
    new "through the large window in the center"

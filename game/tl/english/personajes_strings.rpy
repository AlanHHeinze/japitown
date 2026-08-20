# Nombres de personajes que NO son nombres propios (esos quedan igual en inglés).
#
# El nombre de un Character se traduce automáticamente por Ren'Py vía este bloque
# `strings`, sin tocar la definición (definition_repartidor.rpy).

translate english strings:

    old "Repartidor"
    new "Delivery Guy"

    # Pensamientos. El nombre completo (con el sufijo) es UN solo string, asi
    # que va uno por personaje. El del MC lleva [mc_name], que Ren'Py sustituye
    # DESPUES de traducir — se conserva tal cual en el `new`.
    old "[mc_name] (Pensamiento)"
    new "[mc_name] (Thought)"

    old "Violet (Pensamiento)"
    new "Violet (Thought)"

    old "Mónica (Pensamiento)"
    new "Monica (Thought)"

    old "Jasmine (Pensamiento)"
    new "Jasmine (Thought)"

translate english strings:

    ############################################################################
    ## Nombres de acciones de locación (botón)
    ############################################################################

    old "Cocinar"
    new "Cook"

    old "Ver TV"
    new "Watch TV"

    ############################################################################
    ## Mensajes de reintento
    ############################################################################

    old "Estoy cansado hoy, quizás debería intentarlo mañana."
    new "I'm tired today, maybe I should try tomorrow."

    # La accion "Buscar" (Violet Amor 15, altillo) NO necesita entrada acá:
    # "Buscar" ya esta traducido en quest_strings_acc_items.rpy y un `old`
    # repetido rompe el lint.

    # Violet Deseo 10 — el vaso de agua de madrugada
    old "Tomar agua"
    new "Drink water"

    # Violet Amor 20 — las dos acciones de la habitacion del MC.
    # El nombre de la compra es una PLANTILLA: el {} lo rellena el precio
    # (VA20_PRECIO_JUEGO) despues de traducir, asi que el `new` debe conservarlo.
    old "Comprar juego (${})"
    new "Buy game (${})"

    old "Jugar"
    new "Play"

    # Violet Amor 50: la ducha del MC. Existe solo durante esa fase de la quest.
    old "Bañarse"
    new "Take a shower"

# Botones de interacción que inician una quest o un evento.
#
# Se definen como dicts {"texto": ..., "label": ...} en:
#   - script/characters/<npc>/interaction/interactions_<npc>.rpy  → menú de interacción
#   - script/core/locations/door_access_system.rpy                → opciones de puerta
#   - script/characters/monica/screens/monica_quest01_screens.rpy → instalador (quest 01)
#
# Ambas pantallas los pasan por renpy.translate_string() al mostrarlos, asi que
# alcanza con declarar el `old` acá. El menú de interacción ADEMAS le concatena un
# tag " (Quest)" / " (Evento)", que se traduce por separado: el texto ya concatenado
# nunca matchearia un `old`.
#
# Varios textos se repiten entre el menú de interacción y el door access (ej.
# "Tengo las entradas"): un solo `old` cubre los dos — declararlo dos veces
# hace crashear a Ren'Py.

translate english strings:

    # =========================================================================
    # Tags que el menú de interacción agrega al final del botón
    # =========================================================================

    old " (Quest)"
    new " (Quest)"

    # Variante con el icono de la linea de la quest (⭐ principal, ❤️ amor,
    # 💋 deseo). La arma tag_opcion_quest() en questsystem_core; el {icono} se
    # sustituye DESPUES de traducir, asi que el `new` tiene que conservarlo.
    old " ({icono} Quest)"
    new " ({icono} Quest)"

    old " (Evento)"
    new " (Event)"

    # =========================================================================
    # Violet — menú de interacción y puerta
    # =========================================================================

    old "Hablar"
    new "Talk"

    old "Hablar (quest)"
    new "Talk (quest)"

    old "Pedir mangas"
    new "Ask for manga"

    # Lineas de relacion (amor / deseo): el mismo texto sirve para las 6 quests
    # de cada linea — el boton es generico, la quest concreta la elige el motor.
    old "Charlar un rato"
    new "Chat for a while"

    old "Buscar un momento a solas"
    new "Find a moment alone"

    old "Pedir mangas prestados"
    new "Ask to borrow manga"

    old "Preguntar por el cosplay"
    new "Ask about the cosplay"

    old "Ya compré los cosplay"
    new "I already bought the cosplays"

    old "Llegaron los cosplay"
    new "The cosplays arrived"

    old "Pedirle perdón"
    new "Apologize to her"

    old "Tengo las entradas"
    new "I have the tickets"

    old "Ya hablé con la tienda"
    new "I already talked to the store"

    old "Me pediste que pasara"
    new "You asked me to come by"

    old "Invitar a jugar VR"
    new "Invite her to play VR"

    # -------------------------------------------------------------------------
    # Botones de las quests que antes se auto-disparaban al clickear a Violet
    # (2026-07-31). Al sacar ese atajo, cada quest necesitó su propio botón.
    # "Pedirle perdón" no está acá: ya existía más arriba y se reutiliza.
    # -------------------------------------------------------------------------

    old "Preguntarle qué le pasa"
    new "Ask her what's wrong"

    old "Preguntarle por el cosplay"
    new "Ask her about the cosplay"

    old "Preguntarle por las fotos"
    new "Ask her about the photos"

    old "¿Puedo hacer algo por vos?"
    new "Can I do something for you?"

    # Arco de los favores (04_d3 → 04_d6)
    old "Preguntarle si necesita algo"
    new "Ask if she needs anything"

    # Mismo boton que el anterior, ya con el pedido hecho
    old "¿Que necesitabas?"
    new "What was it you needed?"

    old "Darle las golosinas"
    new "Give her the candy"

    old "Ya está la comida"
    new "Dinner's ready"

    old "Ya terminé de limpiar"
    new "I'm done cleaning"

    old "Mostrarle los cosplays"
    new "Show her the cosplays"

    old "Vine como me pediste"
    new "I came like you asked"

    # =========================================================================
    # Jasmine — menú de interacción
    # =========================================================================

    old "Saludar"
    new "Say hi"

    old "¿Hay algo más que quieras decirme?"
    new "Is there anything else you want to tell me?"

    old "¿Quería mostrarme algo?"
    new "Did you want to show me something?"

    old "Volver a ver el conjunto"
    new "See the outfit again"

    old "Preguntar por Violet"
    new "Ask about Violet"

    # =========================================================================
    # Mónica — menú de interacción
    # =========================================================================

    old "Agradecerle"
    new "Thank her"

    old "Ofrecerle un masaje"
    new "Offer her a massage"

    old "¿Me das un masaje?"
    new "Would you give me a massage?"

    old "Te llama Violet"
    new "Violet is calling you"

    # =========================================================================
    # Puerta — opciones en desarrollo
    # =========================================================================

    old "Espiar"
    new "Peek"

    old "Espiar (Contenido en desarrollo)"
    new "Peek (Content in development)"

    old "Entrar (Contenido en desarrollo)"
    new "Enter (Content in development)"

    # =========================================================================
    # Quest 01 de Mónica — el instalador con software basura
    # Las opciones "trampa" imitan los instaladores reales: se traducen igual de
    # sospechosas, sin corregir la falta de tildes del original (es parte del chiste).
    # =========================================================================

    old "Instalar barra de herramientas WebSearch Plus"
    new "Install WebSearch Plus toolbar"

    old "Instalar solo el programa solicitado"
    new "Install only the requested program"

    old "Instalar pack de optimizacion del sistema"
    new "Install system optimization pack"

    old "Establecer QuickBrowser como navegador predeterminado"
    new "Set QuickBrowser as the default browser"

    old "Instalar extension de busqueda rapida"
    new "Install quick search extension"

    old "No realizar cambios en el navegador"
    new "Make no changes to the browser"

    old "Mantener la configuracion actual"
    new "Keep the current settings"

    old "Cambiar pagina de inicio a SearchMaster"
    new "Change home page to SearchMaster"

    old "Agregar SearchMaster como pagina secundaria"
    new "Add SearchMaster as a secondary page"

    old "Instalar CleanPC Pro (versión de prueba)"
    new "Install CleanPC Pro (trial version)"

    old "Instalar MediaPlayer Ultimate"
    new "Install MediaPlayer Ultimate"

    old "Omitir instalación de software adicional"
    new "Skip installing additional software"

    old "Completar instalación y agregar accesos directos al escritorio"
    new "Finish installation and add desktop shortcuts"

    old "Completar instalación sin modificaciones adicionales"
    new "Finish installation with no additional changes"

    old "Completar instalación e iniciar diagnostico del sistema"
    new "Finish installation and run a system diagnostic"

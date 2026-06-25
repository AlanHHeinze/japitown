################################################################################
## Quest 0_b de Jasmine — Mensaje de Carl
################################################################################
## El MC recibe un mensaje de Carl y debe responder
## Sistema de restricción: Solo puede acceder al celular/chat

label quest_jasmine_questprincipal_0_b:
    # Ocultar HUD temporalmente
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Mostrar piensa sobre el mensaje
    piensa "Acabo de recibir un mensaje. Debería revisar mi celular"

    tutorial "En varios momentos del juego recibiremos [colorear_quest('Mensajes')] de los personajes atravez del [colorear_quest('Celular')] y podremos interactuar con ellos"
    tutorial "Por el momento solo lo haremos de forma pasiva, respondiendo mensajes que nos llegan y completando la cadena. En futuras actualizaciones este sistema se expandera y traera funciones nuevas"
    tutorial "Darnos cuenta que recibimos un mensaje sera simple, veremos una [colorear_quest('Notificacion')] moviendose sobre el icono del celular"
    tutorial "Esta notificacion la veremos tambien sobre la [colorear_quest('App Chat')] y sobre los personajes que tengan [colorear_quest('Mensajes Pendientes')]"
    tutorial "Al entrar en su conversacion, debajo tendremos la opcion de [colorear_quest('Responder')], esta estara en [colorear_quest('Verde')] si hay respuestas disponibles y en [colorear_quest('Gris')] si no las hay"
    tutorial "Al interactuar con el boton se respondera un mensaje de [colorear_quest('Manera Automatica')] salvo que tengamos [colorear_quest('Opciones para Elegir')]. En ese caso las mismas saldran como una lista"
    tutorial "Al igual que dentro de una quest las distintas elecciones traeran cambios narrativos, se guardaran en los [colorear_quest('Recuerdos del Personaje')] y puede darnos distintas recompensas siempre que corresponda"
    tutorial "El sistema de mensajes esta conectado con el resto de los sistemas del juego por lo que en algunos casos la respuesta del mensaje o la respuesta recibida por el personaje puede verse afectada por elementos externos"
    tutorial "Ahora [colorear_quest('Respondamos el Mensaje')] pendiente para continuar"


    window hide

    # Activar restricción que bloquea TODO movimiento
    # Pasamos una locacion ficticia que no existe para bloquear todos los movimientos
    $ activar_restriccion(
        locaciones_permitidas=["__ninguna__"],  # Locación ficticia bloquea todos los movimientos
        acciones_bloqueadas=["entrenar", "trabajar", "avanzar_tiempo", "dormir", "usar_item", "comprar",
                            "relaciones", "pistas", "stats", "galeria", "hot", "banco", "configuracion", "cheats"],
        mensaje_movimiento="Me llego un mensaje debo responderlo",
        mensaje_npc_bloqueado="Me llego un mensaje debo responderlo",
        mensaje_accion_default="Me llego un mensaje debo responderlo",
        celular_bloqueado=False,
    )

    # Mostrar HUD nuevamente
    $ mostrar_hud()

    # Volver al game loop. El chat se completa en el HUD bajo restricción.
    # Cuando se completa, el sistema automáticamente completa esta quest.
    jump game_loop

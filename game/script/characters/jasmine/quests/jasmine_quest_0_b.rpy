################################################################################
## Quest 0_b de Jasmine — Mensaje de Carl
################################################################################
## El MC recibe un mensaje de Carl y debe responder
## Sistema de restricción: Solo puede acceder al celular/chat

# ── Trigger de game_loop ────────────────────────────────────────────────────
# Dispara la escena apenas la quest se inicia (una sola vez): manda el mensaje
# de Carl y salta al tutorial. El flag _jasmine_0b_iniciada evita repetirlo.

init python:

    def _gl_trigger_jasmine_0b():
        if (quest_lista_para_boton("jasmine_questprincipal_0_b")
                and not getattr(store, '_jasmine_0b_iniciada', False)):
            store._jasmine_0b_iniciada = True
            store.sistema_mensajes.disparar_por_trigger(
                "quest", "carl_quest_j0b", "carl")
            return "quest_jasmine_questprincipal_0_b"
        return None

init 5 python:
    registrar_trigger_game_loop("jasmine_0b", _gl_trigger_jasmine_0b, prioridad=30)


label quest_jasmine_questprincipal_0_b:
    # Ocultar HUD temporalmente
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Mostrar piensa sobre el mensaje
    piensa "Acabo de recibir un mensaje. Debería revisar mi celular"

    tutorial "Dentro del celular tendremos una App para chatear con los distintos personajes del juego. Dentro de cada conversación en algunos casos vamos a tener distintas elecciones de respuesta"
    tutorial "Cada vez que recibamos un mensaje vamos a tener una notificación sobre el icono del celular"
    tutorial "Algunas respuestas por parte de los personajes pueden estar ligadas a momentos, lugares, tiempo y disponibilidad"


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

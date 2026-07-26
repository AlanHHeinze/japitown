################################################################################
## Quest 0b del MC — Conociendo el celular
################################################################################
## Se dispara automáticamente el dia 2 estando en la habitacion del MC.
## Enseña al jugador a usar el celular y la app de Pistas.
## Flujo:
## 1. Mensajes de tutorial (sin HUD)
## 2. Mostrar HUD (jugador debe entrar a pistas)
## 3. Validar que entró a pistas
## 4. Mostrar mensajes finales
## 5. Desactivar restricción y completar quest

# ── Estado de la quest ──────────────────────────────────────────────────────
default mc_q0b_disparada = False
default mc_q0b_esperando = False
default mc_q0b_pistas_visitada = False


################################################################################
## Label principal — disparo automático en la habitacion del MC (dia 2+)
################################################################################

label mc_q0b_trigger:

    $ mc_q0b_disparada = True
    $ actualizar_bg_master()

    # Mostrar la escena sin HUD para que se lean los mensajes de tutorial
    $ ocultar_hud()
    hide screen hud_navegacion

    # Mensajes de tutorial SIN HUD (se muestran correctamente ahora)
    window show

    tutorial "Durante el juego tendrás acceso a una [colorear_quest('Guia')] que te ayudará a saber qué hacer en cada momento"
    tutorial "Dentro del [colorear_quest('Celular')] encontrarás la [colorear_quest('App Pistas')], ahí podrás ver el estado actual de la quest"
    tutorial "Y en la pestaña [colorear_quest('Que Hacer')] te dira exactamente como avanzar en la misma\nNOTA: Los presonajes tienen [colorear_quest('Rutinas Fijas')], [colorear_quest('Dinamicas')] y [colorear_quest('Especiales')], por lo que no siempre encontrara al personaje en la locacion y horario que se te indica"
    tutorial "Ahora vamos a probarlo, [colorear_quest('Abri el celilar y entra a la App Pistas')]"

    window hide

    # Activar restricción: bloquear todo excepto el celular
    $ activar_restriccion(
        locaciones_permitidas=["__ninguna__"],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar",
            "trabajar", "comprar", "ver_tv", "usar_item",
            "relaciones", "stats", "mensajes", "galeria",
            "hot", "banco", "configuracion", "cheats",
        ],
        mensaje_movimiento="Primero vamos a revisar el celular y revisar la app de pistas.",
        mensaje_accion_default="Primero vamos a revisar el celular y revisar la app de pistas.",
        celular_bloqueado=False,
        mensaje_celular="",
    )

    # Mostrar HUD para que el jugador pueda usar el celular
    $ mostrar_hud()

    # Activar flag para validar cuando el jugador entre a pistas
    $ mc_q0b_esperando = True
    jump game_loop


################################################################################
## Completar la quest (se ejecuta cuando el jugador cierra pistas)
################################################################################

label mc_q0b_completar:

    # Desactivar flag de espera
    $ mc_q0b_esperando = False
    $ mc_q0b_pistas_visitada = False

    # Ocultar HUD nuevamente para los mensajes finales
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Mensajes finales de tutorial
    tutorial "Perfecto, así de fácil"
    tutorial "Durante el juego podrás consultar la app de Pistas en el celular para saber cuál es tu siguiente objetivo"
    tutorial "Cada vez que completes una quest o avances en la historia, las pistas se actualizarán automáticamente"

    window hide

    # Desactivar restricción
    $ desactivar_restriccion()

    # Completar la quest
    $ sistema_quests_mc.completar_activa()

    # `return` (no `jump game_loop`): se llega por _validar_estado_tras_celular,
    # que el celular invoca con Call(...) — ese frame hay que cerrarlo.
    $ mostrar_hud()
    return

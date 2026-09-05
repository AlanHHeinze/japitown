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


# ── Trigger de game_loop ────────────────────────────────────────────────────
# Tutorial del celular en la habitacion del MC (dia 2+). Dispara en la
# habitacion y no en el pasillo porque con el viaje rapido el pasillo se puede
# saltear; la habitacion del MC no (es donde despierta cada dia).

init python:

    def _gl_trigger_mc_q0b():
        q = store.sistema_quests_mc.quests.get("mc_quest_0b")
        if not (q and q.activa and not q.completada
                and not getattr(store, "mc_q0b_disparada", False)):
            return None
        loc = store.sistema_locaciones.locacion_actual
        if loc and loc.id == "casa_hmc" and store.dia_actual >= 2:
            return "mc_q0b_trigger"
        return None

    def _cel_trigger_mc_q0b():
        """
        Trigger de salir del celular: cierra la quest si el jugador ya paso por
        la app de Pistas. Antes esto era un `if` hardcodeado en el label
        _validar_estado_tras_celular; vive acá desde que ese punto de enganche
        tiene registro propio.
        """
        if (getattr(store, "mc_q0b_esperando", False)
                and getattr(store, "mc_q0b_pistas_visitada", False)):
            return "mc_q0b_completar"
        return None

init 5 python:
    registrar_trigger_game_loop("mc_q0b", _gl_trigger_mc_q0b, prioridad=10)
    registrar_trigger_salir_celular("mc_q0b_pistas", _cel_trigger_mc_q0b)


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

    tutorial "Durante el juego tendrás acceso a una [colorear_quest('Guía')] que te ayudará a saber qué hacer en cada momento"
    tutorial "Dentro del [colorear_quest('Celular')] encontrarás la [colorear_quest('App Pistas')], ahí podrás ver el estado actual de la quest"
    tutorial "Y en la pestaña [colorear_quest('Qué Hacer')] te dirá exactamente cómo avanzar en la misma\nNOTA: Los personajes tienen [colorear_quest('Rutinas Fijas')], [colorear_quest('Dinámicas')] y [colorear_quest('Especiales')], por lo que no siempre encontrarás al personaje en la locación y horario que se te indica"
    tutorial "Ahora vamos a probarlo, [colorear_quest('abre el celular y entra a la App Pistas')]"

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

    # Terminal de contenido: jump game_loop (si el camino hasta aca vino con
    # frames, los drena el inicio del game_loop).
    $ mostrar_hud()
    jump game_loop

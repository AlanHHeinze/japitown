################################################################################
## Violet — Deseo 10 · "Encuentro nocturno"
################################################################################
## Segunda quest de la linea de deseo. Es la primera de la linea que otorga
## HITO (ver characters/violet/hitos_violet.rpy).
##
##     archivo   violet_deseo_10.rpy
##     quest     violet_deseo_02          (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_02    (lo fija el motor: "quest_" + id)
##
## DISPARADOR UNICO: dormir. Con la quest lista, acostarse NO pasa el dia: el
## MC se despierta de madrugada muerto de sed y la partida sigue en el mismo
## dia, de trasnoche. Por eso la quest esta excluida del boton generico
## "Buscar un momento a solas" del menu de interaccion.
##
## LA ESCENA TIENE DOS MITADES, y por eso hay dos labels:
##
##   1. violet_deseo_10_despertar — el trigger de dormir. Despierta al MC,
##      deja el mundo en modo "salida a la cocina" (recorrido acotado, tiempo
##      frenado) y devuelve el control. El jugador camina hasta la cocina.
##
##   2. quest_violet_deseo_02 — lo dispara la accion "Tomar agua" de la cocina.
##      Es la escena en si: aparece Violet y se cierra la quest.
##
## Entre las dos el jugador esta suelto, asi que el estado vive en un flag
## `default` (vd10_sed_activa) y no en variables de escena: tiene que
## sobrevivir a que guarde la partida en el medio.


################################################################################
## Estado
################################################################################

# True entre el despertar y el vaso de agua. Prende la accion "Tomar agua" de
# la cocina y marca que la restriccion de recorrido esta puesta.
default vd10_sed_activa = False


init python:

    def _vd10_trigger_dormir():
        """
        Trigger de dormir, fase "antes": corre con la animacion de dormir ya
        mostrada y ANTES de que dormir() cambie el dia.

        La fase importa. En "despues" el dia ya avanzo y el despertar de
        madrugada caeria en la noche siguiente; en "antes" se devuelve un label
        que mueve el horario a mano y el dia queda donde estaba.
        """
        if not quest_lista_para_boton("violet_deseo_02"):
            return None
        return "violet_deseo_10_despertar"

    def _vd10_tomar_agua_visible():
        """Condicion de la AccionLocacion 'Tomar agua' (actions_catalog)."""
        return getattr(store, 'vd10_sed_activa', False)


init 5 python:

    registrar_trigger_dormir("violet_deseo_10_sed", "antes",
                             _vd10_trigger_dormir)


################################################################################
## 1 · EL DESPERTAR — el MC se levanta de madrugada con sed
################################################################################
## Mismo recurso que usa el motor para el despertar por mensaje prioritario
## (timesystem_core, accion_dormir): la animacion de dormir ya corrio, se
## empuja el horario hasta trasnoche y NO se llama a dormir(), asi que el dia
## no cambia.

label violet_deseo_10_despertar:

    # HORARIO_TRASNOCHE - horario_actual en vez de un "+1" fijo: dormir tambien
    # se puede desde la mañana o la tarde. Si ya era trasnoche la resta da 0 y
    # avanzar_horario_multiple no hace nada, que es lo correcto — ya estamos en
    # el horario de la escena.
    $ avanzar_horario_multiple(HORARIO_TRASNOCHE - horario_actual)

    $ ocultar_hud()
    window show

    piensa "Estoy muerto de sed, voy a ir a la cocina por algo para tomar"

    # Recorrido acotado al camino habitacion → cocina y tiempo frenado.
    #
    # casa_hmc NO va en la lista y no es un olvido: la restriccion filtra el
    # DESTINO de un movimiento, no donde estas parado. El MC arranca en su
    # habitacion, puede salir, y hasta tomar el agua no puede volver a
    # meterse en la cama. Es el mismo recorte que usan la quest 0_b y la 04_d4.
    #
    # Los NPCs se ocultan porque a esta hora estan durmiendo: si alguna rutina
    # dejara a alguien parado en el living, la escena de Violet perderia todo
    # el efecto de aparecer de la nada.
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba", "casa_living",
                               "casa_pasilloabajo", "casa_cocina"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Primero voy a tomar algo, me estoy muriendo de sed"),
        mensaje_accion_default=_("Primero voy a tomar algo, me estoy muriendo de sed"),
        npcs_ocultos=["violet", "monica", "jasmine"],
    )

    # Recien acá: la accion "Tomar agua" aparece en la cocina y el flag marca
    # que hay una restriccion puesta que alguien tiene que sacar.
    $ vd10_sed_activa = True

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA ESCENA — la dispara la accion "Tomar agua" de la cocina
################################################################################

label quest_violet_deseo_02:

    # Apagar el flag y la restriccion es lo PRIMERO. Si la escena se cortara
    # mas adelante, el jugador quedaria encerrado en el recorrido de la cocina
    # sin forma de volver a dormir (mismo criterio que violet_q4d4_avisar).
    $ vd10_sed_activa = False
    $ desactivar_restriccion()

    $ ocultar_hud()
    window show

    # La cocina de trasnoche. Se llega acá desde la accion de esa locacion, asi
    # que la locacion actual ya es la correcta.
    $ _vd10_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd10_bg

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # =========================================================================
    # CONTENIDO — acá va la narrativa
    # =========================================================================
    # Violet entra en tanga. c_tanga_base con ca_base (la cabeza de la ropa de
    # siempre) y NO ca_pijama: no viene de dormir vestida.

    piensa "..."

    show violet_parada c_tanga_base ca_base o_base b_none at right with sprite_normal

    show violet_parada b_hablando
    violet "..."
    show violet_parada b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide violet_parada with dissolve

    $ completar_quest_actual("violet", quest_id="violet_deseo_02")

    # El jugador vuelve al loop donde estaba: la cocina, de trasnoche y ya sin
    # restriccion, asi que puede subir a dormir cuando quiera.
    window hide
    $ mostrar_hud()
    jump game_loop

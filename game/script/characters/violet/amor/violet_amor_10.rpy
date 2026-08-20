################################################################################
## Violet — Amor 10 · "Buena relación"
################################################################################
##     archivo   violet_amor_10.rpy
##     quest     violet_amor_02          (quests_amor_violet.rpy)
##     label     quest_violet_amor_02    (lo fija el motor: "quest_" + id)
##
## Es la quest que otorga el HITO "Buena relación" (violet_hito_amor_01).
##
## DISPARADOR UNICO: un trigger de game_loop. La escena salta sola al entrar al
## living por la mañana con Violet y Monica ahi. Por eso esta quest esta
## excluida del boton generico "Charlar un rato" del menu de interaccion.
##
## LAS DOS ESTAN EN EL LIVING porque la quest les cambia la rutina mientras esta
## activa (_VIOLET_AMOR_RUTINAS en quests_amor_violet.rpy). En la practica casi
## no se nota —al entrar al living salta la escena y no da tiempo a ver el
## fondo— pero hace que el mundo sea coherente: si el jugador pasa antes por la
## cocina, no las encuentra ahi para despues verlas aparecer en el living.
##
## PUESTA EN ESCENA: Monica en right, Violet en center mirando hacia ella
## (flip), el MC en su posicion de siempre. Cuando Monica se va, Violet se corre
## a right y se da vuelta para hablar de frente con el MC.


init python:

    def _gl_trigger_violet_amor_10():
        """
        Trigger de game_loop: la escena arranca al ENTRAR al living por la
        mañana, con las dos presentes.

        Se piden las dos en casa_living y no "en la casa": la rutina de la quest
        ya las pone ahi, asi que si alguna falta es porque algo la saco (una
        restriccion, otra quest) y en ese caso la escena no deberia dispararse.
        """
        if not quest_lista_para_boton("violet_amor_02"):
            return None
        if store.horario_actual != 0:
            return None

        _loc_a10 = store.sistema_locaciones.locacion_actual
        if _loc_a10 is None or _loc_a10.id != "casa_living":
            return None

        for _npc_id_a10 in ("violet", "monica"):
            _npc_a10 = obtener_npc(_npc_id_a10)
            if not _npc_a10 or not _npc_a10.esta_en_locacion("casa_living"):
                return None
            if npc_esta_oculto(_npc_id_a10):
                return None

        return "quest_violet_amor_02"


init 5 python:

    registrar_trigger_game_loop("violet_amor_10_encuentro",
                                _gl_trigger_violet_amor_10)


label quest_violet_amor_02:

    $ ocultar_hud()
    window show

    # Living con el fondo del horario actual: el trigger solo salta estando ahi.
    $ _va10_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va10_bg

    # Las dos ya estaban charlando cuando el MC sube: entran sin transicion.
    show monica_parada c_rbase_base o_base b_none at right

    # Violet al centro, espejada para quedar mirando hacia Monica.
    show violet_parada c_rbase_base ca_base o_base b_none at center:
        xzoom -1.0

    # El MC con sprite_normal: es el que acaba de entrar.
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    # =========================================================================
    # CONTENIDO — conversación entre los tres
    # =========================================================================

    # Monica se va.
    hide monica_parada with dissolve

    # Violet se corre del centro a right y gira: deja de mirar hacia donde
    # estaba Monica y queda de frente al MC.
    show violet_parada at centro_a_right_y_giro

    # =========================================================================
    # CONTENIDO — conversación entre Violet y el MC
    # =========================================================================

    # Se van los dos.
    hide violet_parada
    hide mc_parado_base
    with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_02")

    window hide
    $ mostrar_hud()
    jump game_loop

################################################################################
## Violet — Deseo 5 · "Atracción"
################################################################################
## Primera quest de la linea de deseo.
##
##     archivo   violet_deseo_5.rpy
##     quest     violet_deseo_01          (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_01    (lo fija el motor: "quest_" + id)
##
## DISPARADOR UNICO: un trigger de game_loop. No hay boton — la escena salta
## sola al entrar al pasillo de arriba con la quest lista y Violet en la casa.
## Por eso esta quest esta excluida del boton generico "Buscar un momento a
## solas" del menu de interaccion.
##
## LA IDEA DE LA ESCENA: Violet YA estaba en el pasillo, de espaldas y con el
## celular. El que llega es el MC. Por eso ella entra sin transicion (ya estaba
## ahi) y el MC con sprite_normal (acaba de aparecer). Cuando se da vuelta, el
## sprite de espaldas se cambia por el de frente.


init python:

    def _gl_trigger_violet_deseo_5():
        """
        Trigger de game_loop: la escena arranca al ENTRAR al pasillo de arriba
        POR LA TARDE.

        La tarde no es un capricho: la pista del panel se lo promete al jugador
        ("Ingresar en el pasillo arriba por la tarde"), y ademas los sprites de
        la escena son de ropa base — de noche Violet esta en pijama y se la
        veria vestida de dia.

        Violet solo tiene que estar en la casa, no necesariamente en el pasillo:
        la escena la pone ahi. tracker_locacion_npc() devuelve None si esta
        afuera o si una restriccion de quest la escondio, asi que cubre las dos
        cosas de una.
        """
        if not quest_lista_para_boton("violet_deseo_01"):
            return None

        if store.horario_actual != 1:
            return None

        _loc_d5 = store.sistema_locaciones.locacion_actual
        if _loc_d5 is None or _loc_d5.id != "casa_pasilloarriba":
            return None

        if tracker_locacion_npc("violet") is None:
            return None

        return "quest_violet_deseo_01"


init 5 python:

    registrar_trigger_game_loop("violet_deseo_5_encuentro",
                                _gl_trigger_violet_deseo_5)


label quest_violet_deseo_01:

    $ ocultar_hud()
    window show

    # Pasillo de arriba con el fondo del horario actual: el trigger solo salta
    # estando ahi, asi que la locacion actual ya es la correcta.
    $ _vd5_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd5_bg

    # Violet SIN transicion: ya estaba en el pasillo antes de que el MC llegara.
    # El xzoom -1.0 la espeja para que mire hacia el otro lado.
    show violet_espalda sb_celular at right:
        xzoom -1.0

    # El MC con sprite_normal: es el que acaba de entrar, y la transicion le da
    # esa sensacion de movimiento.
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    piensa "Si hay algo que me esta llamando mucho la atencion desde que llegue es el trasero de Violet"
    piensa "De a poco me esta empezando a tentar y cada vez me cuesta mas dejar de mirarlo"
    piensa "..."

    hide violet_espalda
    show violet_parada c_rbase_celu ca_base o_base b_none at right with sprite_normal

    show violet_parada b_hablando
    violet "¿Que pasa?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Nada ¿Por?"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablando c_rbase_base with sprite_fast
    violet "Subiste y te quedaste ahi paralizado"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Es que justo me acorde de algo y me puse a pensar en ello"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_pensando with sprite_fast
    violet "¿En que?"
    show violet_parada b_none c_rbase_base with sprite_fast

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Jejeje no te lo puedo decir"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablando 
    violet "Raro..."
    show violet_parada b_none

    hide violet_parada with dissolve

    show mc_parado_base c_rbase_brazoscruzados with sprite_fast
    piensa "Tengo que tratar de ser menos evidente, en algun momento se va a dar cuenta que no puedo dejar de mirarle el trasero"
   

    $ completar_quest_actual("violet", quest_id="violet_deseo_01")

    window hide
    $ mostrar_hud()
    jump game_loop

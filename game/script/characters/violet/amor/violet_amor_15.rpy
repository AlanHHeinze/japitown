################################################################################
## Violet — Amor 15 · "La visita"
################################################################################
##     archivo   violet_amor_15.rpy
##     quest     violet_amor_03          (quests_amor_violet.rpy)
##     label     quest_violet_amor_03    (lo fija el motor: "quest_" + id)
##
## Violet va a la habitacion del MC por la tarde. El MC ya esta ahi —es SU
## habitacion, no tiene que ir a ningun lado— asi que la escena arranca sola en
## cuanto se dan las condiciones.
##
## DISPARADOR UNICO: un trigger de game_loop. No hay boton, y por eso la quest
## esta en la lista _VA_SIN_BOTON de interactions_violet.rpy: si tuviera boton
## quedaria inalcanzable igual (nunca llegarias a clickearla antes de que salte
## la escena).
##
## LAS CUATRO CONDICIONES, y por que cada una:
##   1. La quest lista (ETAPA_BOTON_LISTO), o sea 15 de amor cumplidos.
##   2. Horario TARDE.
##   3. El MC en su habitacion. Es la locacion del jugador, no la de Violet:
##      ella VIENE, asi que de donde salga da igual.
##   4. Violet libre: en la casa, sin rutina especial y sin bloqueos. Sin esto
##      podria "visitarlo" mientras esta afuera o bañandose, que es justo lo
##      que no tiene que pasar.
##
## PUESTA EN ESCENA: el MC ya esta en su posicion cuando arranca —entra sin
## transicion, porque no acaba de llegar— y Violet aparece con sprite_normal,
## que es la que se usa para "alguien entra". Ella lleva su ropa de siempre
## pero con el cuerpo `c_rbase_live` en vez del base.


init python:

    def _gl_trigger_violet_amor_15():
        """
        Trigger de game_loop: Violet visita al MC en su habitacion.

        Devuelve el label o None. Las condiciones van de la mas barata a la mas
        cara: primero los dos enteros (etapa y horario) y recien despues las
        consultas al sistema de NPCs.
        """
        if not quest_lista_para_boton("violet_amor_03"):
            return None

        if store.horario_actual != 1:          # Tarde
            return None

        _loc_a15 = store.sistema_locaciones.locacion_actual
        if _loc_a15 is None or _loc_a15.id != "casa_hmc":
            return None

        _v_a15 = obtener_npc("violet")
        if _v_a15 is None:
            return None

        # En la casa. "fuera" es el valor que usa el motor para "salio", asi que
        # alcanza con descartarlo: cualquier otra locacion es adentro.
        if not _v_a15.locacion_actual or _v_a15.locacion_actual == "fuera":
            return None

        # Libre. La rutina especial cubre de una la ducha y la salida — las dos
        # son "esta ocupada con otra cosa".
        if _v_a15.obtener_rutina_especial_actual() is not None:
            return None

        # Y que no la esté tapando otro contenido: una restriccion de quest
        # puede tenerla oculta o no interactuable aunque este en casa y libre.
        if npc_esta_oculto("violet") or not npc_interactuable("violet"):
            return None

        return "quest_violet_amor_03"


init 5 python:

    registrar_trigger_game_loop("violet_amor_15_visita",
                                _gl_trigger_violet_amor_15)


################################################################################
## LA ESCENA
################################################################################

label quest_violet_amor_03:

    $ ocultar_hud()
    window show

    # La habitacion del MC con el fondo de la tarde: el trigger solo salta
    # estando ahi y a esa hora, asi que la locacion actual ya es la correcta.
    $ _va15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va15_bg

    # El MC ya estaba: entra sin transicion.
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    "Tok Tok Tok"

    show mc_parado_base b_hablando
    mc "Pasa"
    show mc_parado_base b_none

    # Violet llega. sprite_normal es la transicion de "alguien entra en escena".
    # Cuerpo `c_rbase_live` (no el base) con su cabeza y ojos de siempre.
    show violet_parada c_rbase_live ca_base o_base b_none at right with sprite_normal


    show violet_parada b_hablando
    violet "Estaba en el altillo buscando mi vieja Pocket Boy y mira lo que encontré"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Uhhh... el LIVE... debe ser uno de los primeros juegos que jugué"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "¿Jugamos?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Mmmm no sé si hoy en día lo jugaría, si quieres jugar un juego de mesa tengo muchas opciones"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Pero yo quería jugar este, antes te encantaba"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "La verdad nunca me gustó mucho ese juego jajaja"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Recuerdo que siempre me decías de jugarlo"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando o_arribanm with sprite_normal
    mc "Supongo que era para pasar un tiempo juntos ya que era tu juego favorito y siempre decías que sí"
    show mc_parado_base b_none c_rbase_base o_base with sprite_normal

    show violet_parada b_hablando
    violet "Siempre pensé que te gustaba mucho"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando o_arribanm with sprite_normal
    mc "La verdad es que me daba un poco de vergüenza porque siempre terminábamos casados y teníamos hijos"
    show mc_parado_base b_none c_rbase_base o_base with sprite_normal

    violet "..."

    show mc_parado_base b_hablando
    mc "Pero si tienes muchas ganas de que nos volvamos a casar y tener hijos, puedo hacer un sacrificio jajaja"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "No era por eso... idiota"
    show violet_parada b_hablandochica
    violet "Me dio nostalgia y quería jugar"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_normal
    mc "Y bueno vamos a jugar"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Creo que ahora eso de casarnos y tener hijos me da vergüenza a mí"
    show violet_parada b_hablandochica
    violet "Mejor no jugamos"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Bueno, si te arrepientes y quieres que vivamos felices por siempre me avisas"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    hide violet_parada with dissolve

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "Jajajaja ahora le dan vergüenza ese tipo de cosas"
    piensa "Pensando en los juegos de mesa quizás podría ver de unir a Violet al club jajaja"
    piensa "Tendría que buscar alguno bueno como para empezar"

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_03")

    window hide
    $ mostrar_hud()
    jump game_loop

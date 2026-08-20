################################################################################
## Violet — Deseo 15 · "Anime en estreno"
################################################################################
##     archivo   violet_deseo_15.rpy
##     quest     violet_deseo_03          (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_03    (lo fija el motor: "quest_" + id)
##
## DISPARADOR UNICO: la accion "Ver TV" del SOTANO, que existe solo mientras
## esta quest esta lista. Por eso la quest esta excluida del boton generico
## "Buscar un momento a solas" del menu de interaccion.
##
## POR QUE NO HACE FALTA NINGUN FLAG `default`: la quest no tiene fases
## intermedias — se dispara y se cierra en la misma escena. La condicion de la
## accion es directamente `quest_lista_para_boton`, asi que aparece y
## desaparece sola sin que ningun label tenga que prender nada.
##
## DE DIA LA ACCION SE VE PERO AVISA, no se esconde: un boton que no esta (o
## que esta en gris sin explicacion) se lee como un bug. El mismo criterio que
## usan el "Ver TV" del living y las limpiezas de la 04_d5.


init python:

    def _vd15_ver_tv_quest():
        """La accion del sotano esta puesta por la QUEST."""
        return quest_lista_para_boton("violet_deseo_03")

    def _vd15_ver_tv_ventaja():
        """
        La accion del sotano esta puesta por la VENTAJA del hito de deseo 20.

        Es la vida despues de la quest: la misma accion queda para siempre, pero
        en vez de disparar la escena de cierre tira los dados a ver si Violet se
        engancha (ver violet_ver_anime_suelto).
        """
        return npc_tiene_ventaja("violet", "accion_ver_anime")

    def _vd15_ver_tv_visible():
        """
        Condicion de la AccionLocacion del sotano (actions_catalog).

        Dos dueños posibles, y no se pisan: cuando la quest la tiene puesta
        todavia no existe el hito, y cuando existe el hito la quest ya se
        completo.
        """
        return _vd15_ver_tv_quest() or _vd15_ver_tv_ventaja()


################################################################################
## Router de la accion — decide si se puede ver o todavia no
################################################################################
## Es el `label_generico` de la accion, o sea una SUBRUTINA del executor: si no
## se puede ver, termina en `return` y el executor sigue su curso. Cuando si se
## puede, salta a la escena, que ya es contenido y cierra con jump game_loop.

label violet_deseo_15_ver_tv:

    # La serie se emite de noche. Trasnoche tambien queda afuera: a esa hora ya
    # termino, y ademas la escena necesita a Violet despierta. Vale para los dos
    # dueños de la accion, asi que el chequeo va antes de repartir.
    if horario_actual != 2:
        $ _blk_guardar_toque()
        piensa "Todavia no lo dan, la serie se emite por la noche"
        return

    # Ya no esta la quest: manda la ventaja del hito y se ve igual, con o sin
    # ella. Va antes del jump porque cuando existe el hito la quest ya se cerro.
    if not _vd15_ver_tv_quest():
        jump violet_ver_anime_suelto

    jump quest_violet_deseo_03


################################################################################
## LA VENTAJA "Ver Anime" — vida despues de la quest
################################################################################
## Espejo de violet_jugar_suelto (amor 20): se ve igual siempre, si Violet esta
## disponible tiene la mitad de chances de bajar al sotano, y en los dos casos se
## gasta el horario y la accion queda usada por hoy.
##
## El "una vez por dia" y su mensaje de reintento los resuelve la AccionLocacion
## con reseteo="diario" + mensaje_reintento (ver actions_catalog); acá solo hay
## que marcarla usada.

label violet_ver_anime_suelto:

    $ sistema_acciones.marcar_usada("vd15_ver_tv_sotano")

    # tracker_locacion_npc es la fuente de verdad de "se puede ubicar al NPC":
    # devuelve None si esta fuera de casa o si una restriccion la escondio.
    $ _va_disponible = (tracker_locacion_npc("violet") is not None)
    $ _va_se_une = _va_disponible and renpy.random.random() < 0.5

    $ ocultar_hud()
    window show

    if _va_se_une:
        $ obtener_npc("violet").modificar_stat2(2)
        piensa "Violet se unio y vimos un par de capitulos juntos"
    else:
        piensa "Ver anime solo no es lo mismo"

    window hide
    $ mostrar_hud()
    $ avanzar_horario()
    jump game_loop


################################################################################
## La escena
################################################################################

label quest_violet_deseo_03:

    $ ocultar_hud()
    window show

    # El sotano de noche: se llega acá desde su propia accion de locacion, asi
    # que la locacion actual ya es la correcta.
    $ _vd15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd15_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    # =========================================================================
    # CONTENIDO — PARTE A · el MC solo, antes de que ella baje
    # =========================================================================

    piensa "..."

    # =========================================================================
    # CONTENIDO — PARTE B · entra Violet en pijama
    # =========================================================================
    # ca_pijama junto con c_pijama_*: la cabeza tiene su propia version de
    # pijama y dejarla en ca_base le pondria el peinado de la ropa de siempre.

    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right with sprite_normal

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ completar_quest_actual("violet", quest_id="violet_deseo_03")

    # Se les fue la noche viendo el estreno: el horario avanza y el jugador
    # queda en el sotano, donde estaba.
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop

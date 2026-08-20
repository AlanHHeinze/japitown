################################################################################
## Violet — VENTAJA "Beso (Deseo)"
################################################################################
## Ventaja del hito de deseo 30. Agrega una opcion al menu de Violet para
## besarla, una vez por dia.
##
## GEMELO DE beso_violet.rpy (el de amor). Son DOS ventajas y DOS botones
## separados, cada uno con su propio limite diario: teniendo los dos hitos se
## pueden hacer los dos el mismo dia. Lo unico que comparten es la forma.
##
## DOS CORTES ANTES DE LA ESCENA, en este orden:
##   1. hay otro NPC delante  → no adelante de otras personas
##   2. ya la beso hoy        → una por dia
## El de la compañia va primero a proposito: es el que tiene explicacion
## narrativa, y seria raro que te diga "ya me besaste hoy" estando Monica al lado.


# Ultimo dia (dias_totales) en que la beso. Se compara contra dias_totales, que
# es el contador absoluto, asi que no hay nada que resetear al dormir.
default violet_beso_deseo_ultimo_dia = None


init python:

    def _violet_beso_deseo_disponible():
        """Condicion del boton del menu (interactions_violet.rpy)."""
        return npc_tiene_ventaja("violet", "accion_beso_deseo")

    def _violet_beso_deseo_usado_hoy():
        return store.violet_beso_deseo_ultimo_dia == getattr(store, 'dias_totales', 0)

    def _violet_beso_deseo_hay_companiia():
        """
        True si hay OTRO NPC en la locacion, ademas de Violet.

        Se recorren los NPCs y se pregunta por tracker_locacion_npc en vez de
        usar obtener_npcs_en_locacion(): esa devuelve tambien a los que una
        restriccion de quest escondio, y el jugador no los ve. tracker_ es la
        fuente de verdad del proyecto para "se puede ubicar al NPC".
        """
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None:
            return False
        for _nid in store.sistema_npcs.npcs:
            if _nid == "violet":
                continue
            if tracker_locacion_npc(_nid) == _loc.id:
                return True
        return False


################################################################################
## La escena
################################################################################

label violet_beso_deseo:

    $ ocultar_hud()
    window show

    if _violet_beso_deseo_hay_companiia():
        violet "Acá no, no delante de otras personas"
        window hide
        $ mostrar_hud()
        jump game_loop

    if _violet_beso_deseo_usado_hoy():
        violet "Ya me besaste hoy, no abuses"
        window hide
        $ mostrar_hud()
        jump game_loop

    $ violet_beso_deseo_ultimo_dia = getattr(store, 'dias_totales', 0)
    $ obtener_npc("violet").modificar_stat2(1)

    # Pasa donde esten y con la ropa que tengan: la opcion no tiene condicion de
    # locacion, asi que no se puede asumir ni el lugar ni el atuendo.
    $ _vbd_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vbd_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_cerca

    # cuerpo_activo() para no asumir la ropa: de noche esta en pijama.
    $ _vbd_cuerpo = cuerpo_activo("violet")
    if _vbd_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at npc_cerca
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at npc_cerca
    with sprite_normal

    # =========================================================================
    # CONTENIDO — el beso
    # =========================================================================

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

    window hide
    $ mostrar_hud()
    jump game_loop

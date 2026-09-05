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
## DONDE Y CUANDO: en su habitacion (casa_hviolet) y de noche (horario 2), que es
## el mismo escenario de la quest de deseo 25 — de ahi salen los cuadros de la
## secuencia, que estan dibujados para ese lugar. Fuera de ahi la opcion sigue
## apareciendo en el menu, pero Violet contesta con la pista de donde y cuando.
##
## TRES CORTES ANTES DE LA ESCENA, en este orden:
##   1. no es su habitacion de noche → la pista de donde y cuando
##   2. hay otro NPC delante         → no adelante de otras personas
##   3. ya la beso hoy               → una por dia
## El de lugar/horario va primero porque es el que define toda la escena: los
## otros dos recien tienen sentido una vez que estan en el sitio correcto. Y el
## de la compañia va antes que el diario porque seria raro que te diga "ya me
## besaste hoy" estando Monica al lado.


# Ultimo dia (dias_totales) en que la beso. Se compara contra dias_totales, que
# es el contador absoluto, asi que no hay nada que resetear al dormir.
default violet_beso_deseo_ultimo_dia = None


init python:

    def _violet_beso_deseo_disponible():
        """Condicion del boton del menu (interactions_violet.rpy)."""
        return npc_tiene_ventaja("violet", "accion_beso_deseo")

    def _violet_beso_deseo_usado_hoy():
        return store.violet_beso_deseo_ultimo_dia == getattr(store, 'dias_totales', 0)

    def _violet_beso_deseo_visto():
        """
        True si ya la beso asi alguna vez. Predicado del catalogo de contenido
        (el ojo del panel de Desbloqueos).

        Mismo truco que en el beso de amor: `violet_beso_deseo_ultimo_dia`
        arranca en None y solo se escribe al besarla.
        """
        return getattr(store, 'violet_beso_deseo_ultimo_dia', None) is not None

    def _violet_beso_deseo_lugar_ok():
        """
        True si estan donde y cuando corresponde: su habitacion, de noche.

        Es la condicion de la ESCENA, no la del boton: el boton aparece igual
        en cualquier lado y ella responde con la pista. Asi el jugador se entera
        de que la ventaja existe y de que tiene un momento, en vez de ver una
        opcion que aparece y desaparece sin explicacion.
        """
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_hviolet":
            return False
        return store.horario_actual == 2          # Noche

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

init 5 python:

    registrar_contenido_ventaja(
        "accion_beso_deseo", "beso_deseo", "violet",
        "El otro beso",
        "Elige Beso (Deseo) en su menú, en su habitación por la noche y a solas. Una vez por día.",
        vista=_violet_beso_deseo_visto,
        orden=10,
    )


label violet_beso_deseo:

    $ ocultar_hud()
    window show

    # LA ESCENA SE ARMA PRIMERO, antes de los cortes. Las cuatro salidas —las
    # tres negativas y el beso— muestran el mismo cuadro: los dos parados en sus
    # lugares. Antes los cortes iban arriba y una negativa salia como texto
    # suelto, sin fondo y sin nadie en escena.
    $ _vbd_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vbd_bg

    # Arrancan SEPARADOS —mc_izquierda y right— porque de ahi parten
    # mc_acercarse / npc_acercarse: si empezaran ya en el centro, el
    # acercamiento haria saltar los sprites hacia atras en el primer frame.
    #
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # cuerpo_activo() para no asumir la ropa: de noche esta en pijama, pero una
    # skin de quest o de evento puede haberla cambiado — y ademas las negativas
    # pasan en cualquier lado y a cualquier hora.
    $ _vbd_cuerpo = cuerpo_activo("violet")
    if _vbd_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # ── Las tres negativas ───────────────────────────────────────────────────
    if not _violet_beso_deseo_lugar_ok():
        show violet_parada b_hablando
        violet "Si quieres un beso, sabes dónde y cuándo te lo puedo dar"
        jump deseo_beso_salir

    if _violet_beso_deseo_hay_companiia():
        show violet_parada b_hablando
        violet "Acá no, no delante de otras personas"
        jump deseo_beso_salir

    if _violet_beso_deseo_usado_hoy():
        show violet_parada b_hablando
        violet "Ya me besaste hoy, no abuses"
        jump deseo_beso_salir

    $ violet_beso_deseo_ultimo_dia = getattr(store, 'dias_totales', 0)
    $ obtener_npc("violet").modificar_stat2(1)

    # =========================================================================
    # CONTENIDO — el beso
    # =========================================================================
    #
    # La misma secuencia de la quest de deseo 25 (violet_deseo_25.rpy), en tres
    # tramos:
    #   1. los dos sprites normales CAMINAN hasta el centro (mc_acercarse /
    #      npc_acercarse, que terminan justo en mc_cerca / npc_cerca)
    #   2. se cambian por el layeredimage de la secuencia, que ya trae a los dos
    #      dibujados juntos
    #   3. la secuencia avanza cuadro por cuadro
    #
    # El `pause` despues del acercamiento es por el transform: dura 0.8s y sin
    # esperarlo el cambio de sprites lo cortaria a la mitad.
    #
    # Los cuadros son 1920x1080 CON transparencia, o sea la pareja recortada: el
    # `scene` de la habitacion sigue puesto detras y no hay que volver a
    # pintarlo.

    show mc_parado_base c_rbase_base o_base b_none at mc_acercarse
    show violet_parada b_none at npc_acercarse
    pause 1.2

    # Los sprites sueltos se van y entra el layeredimage, que arranca solo en
    # `bs_frenteafrente` (es el default de su unico grupo).
    hide mc_parado_base
    hide violet_parada
    show beso_deseo_violet with dissolve
    pause 0.5

    # De acá en adelante cada `show` reemplaza el cuadro anterior: el grupo es
    # uno solo, asi que los atributos son excluyentes y no hay que apagar nada.
    #
    # SIN DIALOGO Y SIN CLICKS: cada cuadro entra con sprite_normal (Dissolve de
    # 0.5) y se sostiene otro medio segundo. Los `pause` van con duracion, asi
    # que corren solos y el jugador mira la secuencia de corrido.
    show beso_deseo_violet bs_1 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_2 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_3 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_4 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_5 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_6 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_7 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_8 with sprite_normal
    pause 0.5

    show beso_deseo_violet bs_9 with sprite_normal
    pause 0.5

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide beso_deseo_violet with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## La salida de las negativas
################################################################################
## Los tres cortes terminan igual: se van los dos y vuelve el juego. Va como
## label y no repetido tres veces para que no se puedan desincronizar.

label deseo_beso_salir:

    show violet_parada b_none
    hide mc_parado_base
    hide violet_parada
    with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop

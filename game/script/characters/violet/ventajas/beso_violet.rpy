################################################################################
## Violet — VENTAJA "Beso (Amor)"
################################################################################
## Ventaja del hito de amor 30. Agrega una opcion al menu de Violet para
## besarla, una vez por dia.
##
## ARCHIVO SUELTO Y NO CARPETA PROPIA: es una ventaja con UNA escena, no un
## sistema con piezas de contenido. La carpeta se justifica cuando hay un
## controlador mas un archivo por item (juegosnuevos/, mensajear/, ropanueva/).
##
## DONDE Y CUANDO: en su habitacion (casa_hviolet) y de tarde (horario 1). Es el
## gemelo del de deseo, que va en la misma habitacion pero de NOCHE — cada beso
## tiene su momento, asi que teniendo los dos hitos no se pisan. Fuera de ahi la
## opcion sigue apareciendo en el menu, pero Violet contesta con la pista de
## donde y cuando.
##
## TRES CORTES ANTES DE LA ESCENA, en este orden:
##   1. no es su habitacion de tarde → la pista de donde y cuando
##   2. hay otro NPC delante         → no adelante de otras personas
##      (la condicion es `npc_a_solas`, en ui/hud/hud_tracker.rpy: la
##      comparten los dos besos y la regla que Violet enuncia en amor 45)
##   3. ya la beso hoy               → una por dia
## El de lugar/horario va primero porque es el que define toda la escena: los
## otros dos recien tienen sentido una vez que estan en el sitio correcto. Y el
## de la compañia va antes que el diario porque seria raro que te diga "ya me
## besaste hoy" estando Monica al lado.


# Ultimo dia (dias_totales) en que la beso. Se compara contra dias_totales, que
# es el contador absoluto, asi que no hay nada que resetear al dormir.
default violet_beso_ultimo_dia = None


init python:

    def _violet_beso_disponible():
        """Condicion del boton del menu (interactions_violet.rpy)."""
        return npc_tiene_ventaja("violet", "accion_beso_amor")

    def _violet_beso_usado_hoy():
        return store.violet_beso_ultimo_dia == getattr(store, 'dias_totales', 0)

    def _violet_beso_visto():
        """
        True si ya la beso alguna vez. Predicado del catalogo de contenido (el
        ojo del panel de Desbloqueos).

        No hace falta un flag nuevo: `violet_beso_ultimo_dia` arranca en None y
        solo se escribe al besarla, asi que "distinto de None" ya es "lo vio".
        """
        return getattr(store, 'violet_beso_ultimo_dia', None) is not None

    def _violet_beso_lugar_ok():
        """
        True si estan donde y cuando corresponde: su habitacion, de tarde.

        Es la condicion de la ESCENA, no la del boton: el boton aparece igual
        en cualquier lado y ella responde con la pista. Asi el jugador se entera
        de que la ventaja existe y de que tiene un momento, en vez de ver una
        opcion que aparece y desaparece sin explicacion.
        """
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_hviolet":
            return False
        return store.horario_actual == 1          # Tarde



################################################################################
## La escena
################################################################################

init 5 python:

    registrar_contenido_ventaja(
        "accion_beso_amor", "beso_amor", "violet",
        "El beso",
        "Elige Beso (Amor) en su menú, en su habitación por la tarde y a solas. Una vez por día.",
        vista=_violet_beso_visto,
        orden=10,
    )


label violet_beso_amor:

    $ ocultar_hud()
    window show

    # LA ESCENA SE ARMA PRIMERO, antes de los cortes. Las cuatro salidas
    # —las tres negativas y el beso— muestran el mismo cuadro: los dos
    # parados en sus lugares. Antes los cortes iban arriba y una negativa
    # salia como texto suelto, sin fondo y sin nadie en escena.
    $ _vb_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vb_bg

    # Arrancan SEPARADOS —mc_izquierda y right— porque de ahi parten
    # mc_acercarse / npc_acercarse: si empezaran ya en el centro, el
    # acercamiento haria saltar los sprites hacia atras en el primer frame.
    #
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # cuerpo_activo() para no asumir la ropa: una skin de quest o de evento
    # puede haberla cambiado, y ademas las negativas pasan en cualquier
    # lado y a cualquier hora — de noche esta en pijama.
    $ _vb_cuerpo = cuerpo_activo("violet")
    if _vb_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # ── Las tres negativas ───────────────────────────────────────────────
    if not _violet_beso_lugar_ok():
        show violet_parada b_hablando
        violet "Si quieres un beso, sabes dónde y cuándo te lo puedo dar"
        jump amor_beso_salir

    if not npc_a_solas("violet"):
        show violet_parada b_hablando
        violet "Acá no, no delante de otras personas"
        jump amor_beso_salir

    if _violet_beso_usado_hoy():
        show violet_parada b_hablando
        violet "Ya me besaste hoy, no abuses"
        jump amor_beso_salir

    $ violet_beso_ultimo_dia = getattr(store, 'dias_totales', 0)
    $ obtener_npc("violet").modificar_stat1(1)

    # =========================================================================
    # CONTENIDO — el beso
    # =========================================================================
    #
    # El tramo final de la secuencia de la quest de amor 25
    # (violet_amor_25.rpy), en tres tramos:
    #   1. los dos sprites normales CAMINAN hasta el centro (mc_acercarse /
    #      npc_acercarse, que terminan justo en mc_cerca / npc_cerca)
    #   2. se cambian por el layeredimage de la secuencia, que ya trae a los dos
    #      dibujados juntos
    #   3. la secuencia avanza cuadro por cuadro
    #
    # ENTRA DIRECTO EN `ab_5` y no en el default `ab_1`: los cuatro cuadros que
    # faltan son la construccion del abrazo, que en la quest venia del susto del
    # apagon. Acá el beso es a proposito, asi que arranca ya abrazados.
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

    # Los sprites sueltos se van y entra el layeredimage.
    #
    # De acá en adelante cada `show` reemplaza el cuadro anterior: el grupo
    # `secuencia` es uno solo, asi que los atributos son excluyentes y no hay
    # que apagar nada. Las bocas del layeredimage quedan en Null: acá no se
    # habla.
    #
    # SIN DIALOGO Y SIN CLICKS: cada cuadro entra con sprite_normal (Dissolve de
    # 0.5) y se sostiene otro medio segundo. Los `pause` van con duracion, asi
    # que corren solos y el jugador mira la secuencia de corrido.
    hide mc_parado_base
    hide violet_parada
    show beso_amor_violet ab_5 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_1 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_2 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_3 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_4 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_3 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_4 with sprite_normal
    pause 0.5

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide beso_amor_violet with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## La salida de las negativas
################################################################################
## Los tres cortes terminan igual: se van los dos y vuelve el juego. Va como
## label y no repetido tres veces para que no se puedan desincronizar.

label amor_beso_salir:

    show violet_parada b_none
    hide mc_parado_base
    hide violet_parada
    with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop

################################################################################
## Violet — Amor 20 · "Jugando juntos"
################################################################################
##     archivo   violet_amor_20.rpy
##     quest     violet_amor_04           (quests_amor_violet.rpy)
##     label     quest_violet_amor_04     (lo fija el motor: "quest_" + id)
##
## La quest tiene TRES tramos y cada uno tiene su propio disparador. La quest
## se queda en ETAPA_BOTON_LISTO todo el tiempo; el que distingue el tramo es
## el flag `va20_fase`, y la pista del panel va cambiando con el:
##
##   fase 0 · boton en el menu de Violet — "Pedirle recomendacion de juegos"
##   fase 1 · accion en casa_hmc — "Comprar juego ($200)"
##   fase 2 · accion en casa_hmc — "Jugar" (de noche y con Violet en casa)
##   fase 3 · quest completada
##
## ESTO NO ROMPE LA REGLA DE "UN SOLO DISPARADOR": los tres son excluyentes —
## cada uno solo existe en su fase, asi que en ningun momento hay dos formas de
## avanzar la quest al mismo tiempo.
##
## POR QUE LAS ACCIONES SE REGISTRAN EN EL CATALOGO Y NO ACA: sistema_acciones
## es `define` y no se guarda; un registro hecho en runtime desde un label
## desaparece al cargar la partida y deja la quest trabada. Los labels solo
## mueven `va20_fase`.


################################################################################
## Parametros
################################################################################

# Precio del juego. Vive en un solo lugar: lo usan el nombre del boton, el
# chequeo de saldo y el descuento.
define VA20_PRECIO_JUEGO = 200


################################################################################
## Estado
################################################################################

# 0 = falta la recomendacion · 1 = falta comprarlo · 2 = falta jugar · 3 = listo
default va20_fase = 0


init python:

    # ── Textos de la quest (los usa quests_amor_violet.rpy) ──────────────────

    def _pista_va20_listo():
        """Pista de ETAPA_BOTON_LISTO — cambia con el tramo."""
        _f = getattr(store, 'va20_fase', 0)
        if _f == 0:
            return renpy.translate_string("No se que jugar podria preguntarle a Violet")
        if _f == 1:
            return renpy.translate_string("Violet me recomendo un juego, tendria que conseguirlo")
        return renpy.translate_string("Ya tengo el juego, ahora falta jugarlo con ella")

    def _quehacer_va20_listo():
        """Que hacer en ETAPA_BOTON_LISTO — idem."""
        _f = getattr(store, 'va20_fase', 0)
        if _f == 0:
            return renpy.translate_string("Hablar con Violet")
        if _f == 1:
            return renpy.translate_string("Comprar el juego en mi habitacion")
        return renpy.translate_string("Jugar de noche en mi habitacion")

    # ── Condiciones de los disparadores ──────────────────────────────────────

    def _va20_boton_recomendacion():
        """Boton del menu de Violet (interactions_violet.rpy)."""
        return (quest_lista_para_boton("violet_amor_04")
                and getattr(store, 'va20_fase', 0) == 0)

    def _va20_comprar_visible():
        """Condicion de la AccionLocacion 'Comprar juego' (actions_catalog)."""
        return (quest_lista_para_boton("violet_amor_04")
                and getattr(store, 'va20_fase', 0) == 1)

    def _va20_jugar_quest():
        """La accion 'Jugar' esta puesta por la QUEST (tramo 3)."""
        return (quest_lista_para_boton("violet_amor_04")
                and getattr(store, 'va20_fase', 0) == 2)

    def _va20_jugar_ventaja():
        """
        La accion 'Jugar' esta puesta por la VENTAJA del hito de amor 20.

        Es la vida despues de la quest: la misma accion queda para siempre, pero
        en vez de disparar la escena de cierre tira los dados a ver si Violet se
        engancha (ver violet_jugar_suelto).
        """
        return npc_tiene_ventaja("violet", "accion_jugar")

    def _va20_jugar_visible():
        """
        Condicion de la AccionLocacion 'Jugar' (actions_catalog).

        Dos dueños posibles, la quest y la ventaja — y no se pisan: cuando la
        quest la tiene puesta todavia no existe el hito, y cuando existe el hito
        la quest ya se completo.

        De TRASNOCHE la accion directamente no esta — es la unica hora en que
        se esconde. En mañana y tarde SI se ve y avisa que Violet no se conecta
        a esa hora: un boton que aparece y desaparece solo se lee como un bug,
        y el aviso ademas le enseña al jugador cuando tiene que volver.
        """
        if getattr(store, 'horario_actual', 0) == HORARIO_TRASNOCHE:
            return False
        return _va20_jugar_quest() or _va20_jugar_ventaja()

    def _va20_nombre_comprar():
        """
        Nombre del boton de compra, con el precio metido desde la constante.

        Va como nombre_dinamico y no como texto fijo para que el precio viva en
        un solo lugar. translate_string traduce la PLANTILLA, asi que el `new`
        del tl tiene que conservar el {}.
        """
        return renpy.translate_string("Comprar juego (${})").format(VA20_PRECIO_JUEGO)

    def _va20_violet_conectada():
        """
        True si Violet esta en casa y disponible para jugar.

        tracker_locacion_npc es LA fuente de verdad de "se puede ubicar al NPC":
        devuelve None si esta fuera de casa o si una restriccion de quest la
        escondio, asi que cubre los dos casos de una sola consulta.
        """
        return tracker_locacion_npc("violet") is not None


################################################################################
## 1 · LA RECOMENDACION — boton del menu de Violet
################################################################################
## Pasa donde este el jugador, asi que la escena toma la locacion actual y la
## ropa de Violet con cuerpo_activo() en vez de asumir ninguna de las dos.

label violet_amor_20_recomendacion:

    $ ocultar_hud()
    window show

    $ _va20_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va20_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # cuerpo_activo() para no asumir la ropa: de noche esta en pijama.
    $ _va20_cuerpo = cuerpo_activo("violet")
    if _va20_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — le pide una recomendacion y ella le nombra un juego
    # =========================================================================

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    # Se va el boton de Violet y aparece el de comprar en la habitacion.
    $ va20_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA COMPRA — accion de casa_hmc
################################################################################
## Es el `label_generico` de la accion, o sea una SUBRUTINA del executor: sin
## plata termina en `return` y el executor sigue su curso.

label violet_amor_20_comprar:

    if dinero < VA20_PRECIO_JUEGO:
        $ _blk_guardar_toque()
        piensa "No tengo el dinero para comprarlo"
        return

    $ dinero -= VA20_PRECIO_JUEGO

    $ ocultar_hud()
    window show

    # Su habitacion en el horario en que este: la accion es de casa_hmc, asi
    # que la locacion actual ya es la correcta.
    $ _va20_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va20_bg

    # (Mc cuerpo pensando ojos base boca neutral)
    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    # =========================================================================
    # CONTENIDO — lo compra y piensa en como proponerselo
    # =========================================================================

    piensa "..."
    piensa "..."

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # Se va el boton de comprar y aparece el de jugar.
    $ va20_fase = 2

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · JUGAR — router de la accion de casa_hmc
################################################################################
## Dos filtros antes de la escena: la hora y que Violet este disponible. Los
## dos avisan con un pensamiento en vez de esconder el boton, para que el
## jugador entienda que le falta. (De trasnoche el boton ni aparece: eso lo
## resuelve la condicion de la accion.)

label violet_amor_20_jugar:

    # Ya no esta la quest: manda la ventaja del hito y se juega igual, con o sin
    # ella. Va PRIMERO porque cuando existe el hito la quest ya se completo.
    if not _va20_jugar_quest():
        jump violet_jugar_suelto

    if horario_actual != 2:
        $ _blk_guardar_toque()
        piensa "Violet no suele estar conectada a esta hora, podria intentarlo de noche"
        return

    if not _va20_violet_conectada():
        $ _blk_guardar_toque()
        piensa "Violet no esta conectada ahora"
        return

    jump quest_violet_amor_04


################################################################################
## LA VENTAJA "Jugar" — vida despues de la quest
################################################################################
## Se juega SIEMPRE: si Violet esta disponible tiene la mitad de chances de
## engancharse, y si no, el MC juega solo. En los dos casos se gasta el horario
## y la accion queda usada por hoy.
##
## El "una vez por dia" y su mensaje de reintento NO son flags propios: los
## resuelve la AccionLocacion con reseteo="diario" + mensaje_reintento (ver
## actions_catalog). Por eso acá solo hay que marcarla usada.

label violet_jugar_suelto:

    $ sistema_acciones.marcar_usada("va20_jugar")

    # tracker_locacion_npc es la fuente de verdad de "se puede ubicar al NPC":
    # devuelve None si esta fuera de casa o si una restriccion la escondio.
    $ _vj_disponible = (tracker_locacion_npc("violet") == "casa_hviolet")
    $ _vj_se_une = _vj_disponible and renpy.random.random() < 0.5

    $ ocultar_hud()
    window show

    if _vj_se_une:
        $ obtener_npc("violet").modificar_stat1(2)
        piensa "Violet se unio y jugamos algunas partidas juntos"
    else:
        piensa "Jugar solo no es lo mismo"

    window hide
    $ mostrar_hud()
    $ avanzar_horario()
    jump game_loop


################################################################################
## 4 · LA PARTIDA — cierre de la quest
################################################################################

label quest_violet_amor_04:

    $ va20_fase = 3

    $ ocultar_hud()
    window show

    # =========================================================================
    # CONTENIDO — LA ESCENA ENTERA VA ACA (todavia sin escribir)
    # =========================================================================
    # Juegan juntos, cada uno en su habitacion. Al escribirla, arrancar con el
    # `scene` que corresponda: la locacion actual es casa_hmc de noche.

    piensa "..."

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    $ completar_quest_actual("violet", quest_id="violet_amor_04")

    # Se les fue la noche jugando: el horario avanza uno (noche → trasnoche).
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop

################################################################################
## Quest 04_d5 — La limpieza (favor 3 de 3)
################################################################################
## Violet le pide al MC que limpie el living, el comedor y la cocina.
##
## Recorrido:
##   1. "Preguntarle si necesita algo"  → _pedido   (prende vq4d5_pedido_hecho)
##   2. mismo boton, con limpieza a medias → _recordatorio ("¿terminaste?" "no")
##   3. accion "Limpiar" en cada una de las 3 locaciones → un label por lugar.
##      Cada uno avanza el horario. El TERCERO completa la quest.
##
## Las tres acciones son AccionLocacion propias (vq4d5_limpiar_* en
## actions_catalog.rpy), registradas en init y con condicion por flag: cada una
## desaparece cuando su lugar ya esta limpio.
##
## El orden en que se limpia no importa: el cierre lo decide el contador, no
## una locacion en particular.
##
## LOS DIALOGOS ESTAN VACIOS A PROPOSITO: los escribe Alan.


################################################################################
## DISPARO AUTOMÁTICO — Violet busca al MC
################################################################################
## Esta quest no la arranca un botón: la arranca ELLA. Pasados los dos días de
## espera, Violet pasa la tarde en el pasillo de arriba (rutina_quest de la
## quest) y la escena salta sola en cuanto el MC entra a donde ella esté.
##
## Dos entradas segun donde se crucen:
##   - en casa_pasilloarriba  → directo a violet_q4d5_pedido
##   - en cualquier otro lado → violet_q4d5_encuentro ("acá no") y de ahí al
##     pedido, ya en el pasillo
##
## El botón "Preguntarle si necesita algo" sigue existiendo y lleva al mismo
## lugar: es la red por si el trigger no llegara a dispararse.

init python:

    def _gl_trigger_violet_04d5_encuentro():
        """
        Trigger de game_loop: devuelve el label del encuentro cuando el MC entra
        a la locación donde está Violet con la quest lista.

        Se apaga solo: violet_q4d5_pedido prende vq4d5_pedido_hecho, que es lo
        primero que se chequea acá.
        """
        if getattr(store, 'vq4d5_pedido_hecho', False):
            return None
        if not quest_lista_para_boton("violet_questprincipal_04_d5"):
            return None

        _loc_gl = store.sistema_locaciones.locacion_actual
        if _loc_gl is None:
            return None

        # esta_en_locacion + el chequeo de oculto: si una restriccion la
        # escondio, no corresponde que aparezca de la nada.
        _v_gl = obtener_npc("violet")
        if not _v_gl or not _v_gl.esta_en_locacion(_loc_gl.id):
            return None
        if npc_esta_oculto("violet"):
            return None

        if _loc_gl.id == "casa_pasilloarriba":
            return "violet_q4d5_pedido"
        return "violet_q4d5_encuentro"


init 5 python:

    registrar_trigger_game_loop("violet_04d5_encuentro",
                                _gl_trigger_violet_04d5_encuentro)


################################################################################
## ENCUENTRO — se cruzan fuera del pasillo: "acá no"
################################################################################
## Violet le dice que quiere hablar, el MC pregunta qué, ella corta con un "acá
## no" y la escena se va en disolvencia al pasillo de arriba, donde sigue.

label violet_q4d5_encuentro:

    $ ocultar_hud()
    window show

    $ _bg_enc = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_enc

    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablando
    violet "¿Cómo estás?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Bien, ¿y tú?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bien..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Bueno, nos vemos luego"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Espera..."
    show violet_parada b_hablando
    violet "Ven conmigo"
    show violet_parada b_none

    # Corte al pasillo de arriba: se va todo en disolvencia y la charla sigue
    # allá. Se mueve al MC de verdad, no solo el fondo, para que al terminar la
    # escena quede parado donde corresponde.
    scene black with dissolve
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    jump violet_q4d5_pedido


################################################################################
## PEDIDO — Violet pide que limpie los tres lugares
################################################################################

label violet_q4d5_pedido:

    $ ocultar_hud()
    window show

    # Fondo del pasillo de arriba EN EL HORARIO ACTUAL: se entra acá de mañana
    # (por el encuentro) o de tarde (cruzándola en el pasillo), y el fondo tiene
    # que acompañar. Violet siempre de dia — a estas horas nunca esta en pijama,
    # asi que no hace falta la rama de vq4dfav_cuerpo.
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv with dissolve

    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "¿Qué pasa?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_rbase_pensando o_arribanm with sprite_normal
    violet "Estabas muy servicial últimamente y me pareció raro que ya no lo estés"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Me rendí"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_normal
    violet "Entonces sí querías algo"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No nada, no te preocupes"
    show mc_parado_base b_abiertachica
    mc "Nos vemos luego"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_rbase_pensando o_juzgandonm with sprite_normal
    violet "Entonces... ¿No querías ver las otras fotos que no te mandé?"
    show violet_parada b_none o_base c_rbase_base with sprite_normal

    show mc_parado_base c_rbase_avergonzado with sprite_normal
    piensa "Ella sabía lo que quería desde un principio y me estaba manipulando para que le haga favores"
    piensa "Y yo caí como un tonto"
    piensa "Podría hacerme el desentendido, pero si lo hago nunca las voy a ver..."


    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "¿Qué quieres que haga?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Directo.... Quiero que limpies el living, el comedor y la cocina"
    show violet_parada b_hablando
    violet "Mónica me pidió que me encargue y sabes que no me gusta limpiar"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando o_arribanm with sprite_normal
    mc "Mmmm me parece que es mucho"
    show mc_parado_base b_none o_base c_rbase_base with sprite_normal

    show violet_parada b_hablandochica
    violet "Tu trabajo va a ser recompensado, créeme"
    show violet_parada b_hablando
    violet "¿Aceptas?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Está bien, acepto"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Avísame cuando esté todo listo"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Está bien..."
    show mc_parado_base b_abiertachica
    mc "Nos vemos luego"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Nos vemos luego"
    show violet_parada b_none

    hide violet_parada

    piensa "Caí completamente en su juego, sabe cómo manipularme"
    piensa "Pero no me arrepiento. Si es por ver esas fotos, vale la pena"


    # =========================================================================
    # CONTENIDO — Violet pide living, comedor y cocina
    # =========================================================================

    # Desde acá aparecen las tres acciones Limpiar en sus locaciones, y se apaga
    # el trigger del encuentro.
    $ vq4d5_pedido_hecho = True

    # La rutina especial ya cumplió su función (traerla al pasillo a buscarte),
    # asi que Violet vuelve a su horario normal. Si no, se quedaria plantada en
    # el pasillo todas las tardes hasta terminar la limpieza: el motor recien la
    # restaura al COMPLETAR la quest.
    python:
        _q_d5 = sistema_quests.obtener_quest("violet_questprincipal_04_d5")
        if _q_d5:
            _q_d5._restaurar_rutina_normal()
        actualizar_rutinas_npcs()

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## RECORDATORIO — Violet pregunta si terminó y el MC dice que no
################################################################################

label violet_q4d5_recordatorio:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "¿Ya terminaste de limpiar?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No, todavía estoy en eso"
    show mc_parado_base b_abiertachica
    mc "Vuelvo luego cuando termine"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Nos vemos luego"
    show violet_parada b_none

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LIMPIAR — un label por locación, solo el MC
################################################################################
## Los tres terminan en violet_q4d5_fin_limpieza, que avanza el horario y, si
## era el ultimo lugar, completa la quest. Asi la logica de cierre vive en un
## solo lugar y no hay que repetirla tres veces.

label violet_q4d5_limpiar_living:

    if horario_actual == 3:
        jump violet_q4d5_muy_tarde

    $ vq4d5_limpio_living = True

    $ ocultar_hud()
    window show

    $ _bg_limpieza = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_limpieza
    show mc_parado_base c_rbase_base o_base b_none at mc_cerca

    # =========================================================================
    # CONTENIDO — el MC limpia el living
    # =========================================================================

    jump violet_q4d5_fin_limpieza


label violet_q4d5_limpiar_comedor:

    if horario_actual == 3:
        jump violet_q4d5_muy_tarde

    $ vq4d5_limpio_comedor = True

    $ ocultar_hud()
    window show

    $ _bg_limpieza = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_limpieza
    show mc_parado_base c_rbase_base o_base b_none at mc_cerca

    # =========================================================================
    # CONTENIDO — el MC limpia el comedor
    # =========================================================================

    jump violet_q4d5_fin_limpieza


label violet_q4d5_limpiar_cocina:

    if horario_actual == 3:
        jump violet_q4d5_muy_tarde

    $ vq4d5_limpio_cocina = True

    $ ocultar_hud()
    window show

    $ _bg_limpieza = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_limpieza
    show mc_parado_base c_rbase_base o_base b_none at mc_cerca

    # =========================================================================
    # CONTENIDO — el MC limpia la cocina
    # =========================================================================

    jump violet_q4d5_fin_limpieza


################################################################################
## MUY TARDE — de trasnoche no se limpia
################################################################################
## Los tres labels entran acá si es trasnoche, ANTES de prender su flag: no se
## limpia nada y no se avanza el tiempo.
##
## Por que un mensaje y no esconder el boton: avanzar_horario() es un no-op en
## trasnoche (timesystem_core:79), asi que sin esta guarda el jugador podia
## hacer las tres limpiezas seguidas sin que pasara el tiempo. Y el boton en gris
## sin explicacion se lee como un bug — mismo criterio que "Es muy tarde para
## entrenar" en hud_stats.

label violet_q4d5_muy_tarde:

    $ _blk_guardar_toque()
    piensa "Es muy tarde para ponerme a limpiar."

    jump game_loop


################################################################################
## FIN DE CADA LIMPIEZA — avanza el tiempo y reparte por número de limpieza
################################################################################
## Los tres labels de limpiar caen acá. El comentario de después NO depende del
## LUGAR sino de CUÁNTAS van: primera, segunda o tercera. Así el MC puede
## arrancar quejándose y terminar resignado sin importar en qué orden limpió.

label violet_q4d5_fin_limpieza:

    # Limpiar lleva tiempo: cada lugar cuesta un horario. Va ANTES del
    # comentario para que la escena de después use el horario ya avanzado.
    $ avanzar_horario()

    if violet_favores_limpiezas_hechas() >= 3:
        jump violet_q4d5_tras_limpiar_3
    elif violet_favores_limpiezas_hechas() >= 2:
        jump violet_q4d5_tras_limpiar_2

    jump violet_q4d5_tras_limpiar_1


################################################################################
## DESPUÉS DE LIMPIAR — el MC solo, pensando
################################################################################
## Los tres son iguales de estructura: fondo de la locación en el horario que
## quedó tras avanzar, y el MC al centro en pose de pensar. El texto lo escribe
## Alan; si en alguno no va nada, se puede dejar el bloque vacío y pasa de largo.

label violet_q4d5_tras_limpiar_1:

    $ ocultar_hud()
    window show

    $ _bg_tras = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_tras
    show mc_parado_base c_rbase_pensando o_base b_none at center

    piensa "Estoy agotado y recién empiezo a limpiar"
    piensa "Me estoy cuestionando si hice bien en aceptar esto..."

    window hide
    $ mostrar_hud()
    jump game_loop


label violet_q4d5_tras_limpiar_2:

    $ ocultar_hud()
    window show

    $ _bg_tras = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_tras
    show mc_parado_base c_rbase_pensando o_base b_none at center

    piensa "Dos de tres y no quiero saber más nada..."
    piensa "Esta debilidad por Violet me está costando caro"

    window hide
    $ mostrar_hud()
    jump game_loop


label violet_q4d5_tras_limpiar_3:

    $ ocultar_hud()
    window show

    $ _bg_tras = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_tras
    show mc_parado_base c_rbase_pensando o_base b_none at center

    piensa "Al fin terminé"
    piensa "Pero aprendí algo, no puedo dejar que Violet controle la situación, voy a salir perdiendo siempre"

    # Al completar arranca sola la 04_d6, que espera un día antes de habilitarse.
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_d5")

    window hide
    $ mostrar_hud()
    jump game_loop

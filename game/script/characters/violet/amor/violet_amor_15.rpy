################################################################################
## Violet — Amor 15 · "La visita"
################################################################################
##     archivo   violet_amor_15.rpy
##     quest     violet_amor_03          (quests_amor_violet.rpy)
##     label     quest_violet_amor_03    (lo fija el motor: "quest_" + id)
##
## Violet va a la habitacion del MC por la NOCHE (hasta el 2026-10-01 era de
## tarde: el horario lo decide la declaracion del planificador, Rec locacion
## horario=2 en planificacion_violet.rpy). El MC ya esta ahi —es SU
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
##   2. Horario NOCHE.
##   3. El MC en su habitacion. Es la locacion del jugador, no la de Violet:
##      ella VIENE, asi que de donde salga da igual.
##   4. Violet libre: en la casa, sin rutina especial y sin bloqueos. Sin esto
##      podria "visitarlo" mientras esta afuera o bañandose, que es justo lo
##      que no tiene que pasar.
##
## PUESTA EN ESCENA: el MC ya esta en su posicion cuando arranca —entra sin
## transicion, porque no acaba de llegar— y Violet aparece con sprite_normal,
## que es la que se usa para "alguien entra". Es de noche: viene EN PIJAMA
## (cuerpo `c_pijama_live`, con el juego en la mano, y la cabeza `ca_pijama`).
##
## EL HORARIO AVANZA A LA TRASNOCHE en "Un tiempo más tarde", despues del
## altillo. De noche en la habitacion del MC tambien arrancan deseo 20 y deseo
## 30: sin el avance, si alguna estaba lista saltaba justo detrás.


init python:

    def _gl_trigger_violet_amor_15():
        """
        Trigger de game_loop: Violet visita al MC en su habitacion.

        Devuelve el label o None. Las condiciones van de la mas barata a la mas
        cara: primero los dos enteros (etapa y horario) y recien despues las
        consultas al sistema de NPCs.
        """
        # Noche, MC en su pieza, Violet en casa, libre y no oculta: demandas de
        # la quest (Rec npc en="casa", libre=True), las aplica la capa 2.
        if not quest_lista_para_boton("violet_amor_03"):
            return None
        return "quest_violet_amor_03"


init 5 python:

    registrar_trigger_game_loop("violet_amor_15_visita",
                                _gl_trigger_violet_amor_15,
                                quest_id="violet_amor_03")


# La caida en el altillo: un fondo de pantalla completa y la boca de Violet,
# que se superpone mientras habla. Por RUTA EXPLICITA y con prefijo propio:
# la carpeta amor15 tambien tiene los assets de la Pocket Boy (jn_pocketboy).
# Van en master sin prefijo de personaje: la escena no se tiñe por horario.
image va15_caida = "images/quest/violet/amor15/violet_caida.jpg"
image va15_caida_boca = "images/quest/violet/amor15/violet_caida_boca.webp"

# El beso: un sprite de los DOS juntos (756x1080, apoyado abajo) que reemplaza a
# los dos sprites sueltos. Lleva el prefijo `violet_` para ir a la capa de
# personajes y tenirse con el horario igual que los sprites que reemplaza.
image violet_va15_beso = "images/quest/violet/amor15/beso.webp"

# Violet camina hasta el MC. Parte de donde esta (right) — el `ease` no fija el
# punto de partida — y frena con su sprite pegado al de el.
transform va15_violet_acercarse:
    ease 1.0 xpos 0.30 xanchor 0.5

# El beso, en el lugar donde estaban los dos (entre mc_izquierda y donde llego
# Violet).
transform va15_beso_pos:
    xpos 0.22
    xanchor 0.5
    yanchor 1.0
    ypos 1.0

# Despues del beso: Violet al lado del MC, cerca pero SIN encimarse. 0.40 sale
# de medir los sprites: el dibujo de Violet arranca ~204 px a la izquierda de su
# centro, y el del MC (en mc_izquierda) termina antes de los ~520 px.
transform va15_violet_al_lado:
    xpos 0.40
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom 1.0


################################################################################
## LA ESCENA
################################################################################

label quest_violet_amor_03:

    $ ocultar_hud()
    window show

    # La habitacion del MC con el fondo de la noche: el trigger solo salta
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
    # En pijama, con el LIVE en la mano.
    show violet_parada c_pijama_live ca_pijama o_base b_none at right with sprite_normal


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
    violet "Mejor me voy a seguir buscando la Pocket Boy"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Bueno, si te arrepientes y quieres que vivamos felices por siempre me avisas"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    hide violet_parada with dissolve

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "Jajajaja ahora le dan vergüenza ese tipo de cosas"
    piensa "Pensando en los juegos de mesa quizás podría ver de unir a Violet al club jajaja"
    piensa "Tendría que buscar alguno bueno como para empezar"

    # ── EL RUIDO ─────────────────────────────────────────────────────────────
    # Algo se cae arriba: Violet volvio al altillo a buscar la Pocket Boy.
    "¡CRASH!" with hpunch

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "Eso sonó arriba"
    piensa "¿Estará bien Violet?"

    # ── EL PASILLO DE ARRIBA ─────────────────────────────────────────────────
    # Sale de su habitacion. `escena=True`: lo mueve la escena, no el jugador.
    window hide
    hide mc_parado_base
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba", escena=True)
    $ _va15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va15_bg
    show mc_parado_base c_rbase_base o_arribanm b_none at center
    with fade
    window show

    show mc_parado_base b_hablando
    mc "Violet, ¿está todo bien?"
    show mc_parado_base b_none

    # Contesta desde el altillo: sin sprite.
    violet "No, se me cayó todo"

    show mc_parado_base b_hablando o_base
    mc "Ahí subo y te ayudo"
    show mc_parado_base b_none

    # ── EL ALTILLO: la escena de la caida ────────────────────────────────────
    # El MC no se ve: habla desde fuera del cuadro. Violet habla con la boca de
    # la escena.
    window hide
    hide mc_parado_base
    scene va15_caida with fade
    window show

    mc "¿Qué te pasó?"

    show va15_caida_boca
    violet "Nada..."
    hide va15_caida_boca

    mc "No lo parece, ¿te lastimaste?"

    show va15_caida_boca
    violet "No, solo me duele el trasero de la caída"
    hide va15_caida_boca

    piensa "Tengo una vista privilegiada del accidente"

    mc "¿Cómo terminaste así?"

    show va15_caida_boca
    violet "Cuando pienses que sacar una caja de abajo sin sacar las de arriba es buena idea, no lo hagas"
    hide va15_caida_boca

    mc "Eso te pasó por buscar el camino corto, ahora ordenar esto te va a llevar un buen rato"

    show va15_caida_boca
    violet "¿Me ayudas a levantarme y a ordenar esto, por favor?"
    hide va15_caida_boca

    piensa "Supongo que aunque se lo merezca, no la puedo dejar así"

    mc "Está bien, vamos a ordenar esto"

    # ── UN TIEMPO MAS TARDE ───────────────────────────────────────────────────
    # Ordenar el altillo se comio el resto de la noche: el horario avanza a la
    # trasnoche ACA y no al final. El trigger exige la noche, asi que siempre
    # cae en la trasnoche y nunca topa con el limite de avanzar_horario. Asi
    # tampoco pueden saltar detras deseo 20 o deseo 30, que son de noche en la
    # habitacion del MC.
    window hide
    scene black with fade
    show text Text(renpy.translate_string("Un tiempo más tarde"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause
    hide text with dissolve

    $ avanzar_horario()

    # El pasillo de arriba de trasnoche: el fondo se pide DESPUES de avanzar.
    $ _va15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va15_bg
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with fade
    window show

    show violet_parada b_hablando
    violet "Gracias por ayudarme"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No hay problema, ¿ya estás mejor?"
    show mc_parado_base b_none

    ## ⚠️ FALTA EL ASSET: Violet no tiene cuerpo de PIJAMA agarrandose la cola
    ## (`c_rbase_cola` es con la ropa de siempre). Hasta que exista
    ## violet_parada_cuerpo_pijama_cola.webp va el de pijama base.
    show violet_parada b_hablando c_pijama_base
    violet "Me sigue doliendo el trasero"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Debe ser mucho dolor entonces"
    show mc_parado_base b_none

    show violet_parada b_hablando c_pijama_base
    violet "Jajaja no funciona así, a más trasero no es más dolor"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Tengo mis dudas jajaja"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "De nuevo gracias por ayudarme, cuando termino necesitando algo siempre estás"
    show violet_parada b_none

    # ── EL BESO ──────────────────────────────────────────────────────────────
    # Violet camina hasta el MC.
    window hide
    show violet_parada at va15_violet_acercarse
    pause 1.0

    # Los dos sprites se van y entra el beso, en el mismo fundido.
    hide mc_parado_base
    hide violet_parada
    show violet_va15_beso at va15_beso_pos
    with dissolve
    pause 2.0

    # Vuelven los dos, uno al lado del otro pero sin encimarse.
    hide violet_va15_beso
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show violet_parada c_pijama_base ca_pijama o_base b_none at va15_violet_al_lado
    with dissolve
    window show

    show violet_parada b_hablando
    violet "Tu recompensa"
    show violet_parada b_none

    # Se va a su habitacion.
    show violet_parada at salir_derecha_mirando
    pause 1.5
    hide violet_parada

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "Ayudarla valió la pena"
    piensa "Poco a poco Violet va cambiando su actitud y cada vez nos estamos volviendo más cercanos"

    

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # El horario ya avanzo a la trasnoche ("Un tiempo más tarde"). El jugador
    # queda libre en el pasillo de arriba.
    $ completar_quest_actual("violet", quest_id="violet_amor_03")

    window hide
    $ mostrar_hud()
    jump game_loop

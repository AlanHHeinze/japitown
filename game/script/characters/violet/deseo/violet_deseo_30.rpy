################################################################################
## Violet — Deseo 30 · "Noche de amigas"
################################################################################
##     archivo   violet_deseo_30.rpy
##     quest     violet_deseo_06           (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_06     (lo fija el motor: "quest_" + id)
##
## LAS CUATRO FASES (flag `vd30_fase`):
##
##   0  esperando la noche   → trigger de game_loop: llega la noche en casa
##   1  buscando el sotano   → trigger de game_loop: entrar al sotano
##   2  encerrado en su pieza→ trigger de DORMIR: acostarse
##   3  terminada
##
## LA QUEST NO SE CIERRA CON LA ESCENA DEL SOTANO. De ahi el MC se va a su
## habitacion con la cabeza llena, y lo unico que puede hacer es acostarse —
## dormir es el disparador de la ultima parte, que pasa de madrugada.
##
## COMO ESTAN PUESTAS EN EL SOTANO: por `rutina_quest` (Violet) y
## `rutinas_adicionales` (las otras dos), declaradas en quests_deseo_violet.rpy.
## El motor las pone y las saca solo; ningun label toca ubicaciones. Importa
## para el camino de ida: el jugador que pasa por el sotano antes de que salte
## el aviso tiene que encontrarlas ahi.
##
## ⚠️ LAS OTRAS DOS SON PLACEHOLDER. Se usan Monica y Jasmine — sus sprites y
## sus idles ya existen, asi que la escena y la presencia ambiente funcionan sin
## inventar nada. Al llegar los personajes reales hay que cambiar: los `show` de
## la escena (acá abajo) y las dos entradas de `rutinas_adicionales`.


################################################################################
## Posiciones del grupo
################################################################################
## Las tres de la intro (0.58 / 0.70 / 0.82), con Violet en el medio. El MC va
## en su mc_izquierda de siempre, asi que los cuatro entran sin encimarse.
## El ORDEN de los `show` es el orden de profundidad: el ultimo queda al frente.

transform vd30_grupo_izq:
    xpos 0.58
    xanchor 0.5
    yanchor 1.0
    ypos 1.0

transform vd30_grupo_centro:
    xpos 0.70
    xanchor 0.5
    yanchor 1.0
    ypos 1.0

transform vd30_grupo_der:
    xpos 0.82
    xanchor 0.5
    yanchor 1.0
    ypos 1.0


################################################################################
## Estado
################################################################################

# 0 espera · 1 va al sotano · 2 en su pieza, solo puede dormir · 3 fin
default vd30_fase = 0


init python:

    # Toda la casa MENOS casa_frente, que es la vereda. Es a la vez el "donde
    # puede saltar el aviso" y el "por donde se puede mover" de la fase 1: el
    # jugador se mueve libre por adentro, lo unico que no puede es salir.
    VD30_DENTRO_CASA = [
        "casa_hmc", "casa_pasilloarriba", "casa_pasilloabajo", "casa_living",
        "casa_comedor", "casa_cocina", "casa_banioarriba", "casa_banioabajo",
        "casa_baniomonica", "casa_hviolet", "casa_hmonica", "casa_hjasmine",
        "casa_gym", "casa_patio", "casa_garage", "casa_sotano", "casa_altillo",
    ]

    def _vd30_activa():
        return quest_lista_para_boton("violet_deseo_06")

    def _gl_trigger_violet_deseo_30():
        """
        Trigger de game_loop. Las tres transiciones de la quest, cada una en su
        fase.

        La de la noche va por game_loop y no por registrar_trigger_avanzar
        porque el horario tambien lo mueven las acciones y el talk, que llaman a
        avanzar_horario() directo sin pasar por el label del boton. Lo mismo
        para la del trasnoche.
        """
        if not _vd30_activa():
            return None

        _loc = store.sistema_locaciones.locacion_actual
        _loc_id = _loc.id if _loc else None

        if (store.vd30_fase == 0 and store.horario_actual == 2
                and _loc_id in VD30_DENTRO_CASA):
            return "violet_deseo_30_aviso"

        if store.vd30_fase == 1 and _loc_id == "casa_sotano":
            return "quest_violet_deseo_06"

        return None

    def _vd30_trigger_dormir():
        """
        Trigger de dormir, fase "antes": corre con la animacion ya mostrada y
        ANTES de que dormir() cambie el dia.

        La fase importa. En "despues" el dia ya avanzo y el despertar de
        madrugada caeria en la noche siguiente; en "antes" se devuelve un label
        que mueve el horario a mano y el dia queda donde estaba. Es el mismo
        recurso que usa el despertar por mensaje prioritario.
        """
        if not _vd30_activa():
            return None
        if store.vd30_fase != 2:
            return None
        return "violet_deseo_30_madrugada"


init 5 python:

    registrar_trigger_game_loop("violet_deseo_30_fases",
                                _gl_trigger_violet_deseo_30)

    registrar_trigger_dormir("violet_deseo_30_madrugada", "antes",
                             _vd30_trigger_dormir)


################################################################################
## 1 · EL AVISO — llega la noche, este donde este
################################################################################

label violet_deseo_30_aviso:

    $ ocultar_hud()
    window show

    $ _vd30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd30_bg

    # (Mc cuerpo celular ojos base boca neutral)
    show mc_parado_base c_rbase_celular o_base b_none at center with sprite_normal

    piensa "Violet me pidio ayuda con algo en el sotano"

    hide mc_parado_base with dissolve

    # Se mueve libre por la casa pero no hace nada mas hasta bajar al sotano.
    # No se le recorta el recorrido al camino directo a proposito: la gracia es
    # que vaya, no que lo lleven de la mano.
    $ activar_restriccion(
        locaciones_permitidas=VD30_DENTRO_CASA,
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Violet me esta esperando, no me voy a ir de casa"),
        mensaje_accion_default=_("Primero voy a ver que necesita Violet"),
        npcs_interactuables=["violet"],
    )

    $ vd30_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · EL SOTANO — la escena de la quest
################################################################################

label quest_violet_deseo_06:

    # Se levanta la de la fase 1; la escena sigue en su habitacion y ahi se pone
    # otra distinta (solo puede dormir).
    $ desactivar_restriccion()

    $ ocultar_hud()
    window show

    $ _vd30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd30_bg

    # Las tres ya estaban abajo; el que llega es el MC.
    # ⚠️ Monica y Jasmine son PLACEHOLDER de los dos personajes nuevos.
    # (Placeholder cuerpo base ojos base boca neutral)
    show monica_parada c_rbase_base o_base b_none at vd30_grupo_izq
    # (Violet cuerpo base ojos base boca neutral)
    show violet_parada c_rbase_base ca_base o_base b_none at vd30_grupo_centro
    # (Placeholder cuerpo base ojos base boca neutral)
    show jasmine_parada c_rbase_base o_base b_none at vd30_grupo_der
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    # =========================================================================
    # CONTENIDO — la noche de amigas
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

    hide monica_parada
    hide jasmine_parada
    hide violet_parada
    hide mc_parado_base
    with dissolve

    # La quest NO se completa acá: sigue en su habitacion.
    jump violet_deseo_30_habitacion


################################################################################
## 3 · SU HABITACION — la cabeza llena, y a la cama
################################################################################
## Se llega por el jump del sotano, asi que la escena arranca plantando la
## habitacion: el jugador todavia estaba abajo.

label violet_deseo_30_habitacion:

    $ sistema_locaciones.mover_a_locacion("casa_hmc")

    $ ocultar_hud()
    window show

    $ _vd30_loc_hmc = sistema_locaciones.obtener_locacion("casa_hmc")
    $ _vd30_bg = _vd30_loc_hmc.background if _vd30_loc_hmc else "#1a1a1a"
    scene expression _vd30_bg with fade

    # (Mc cuerpo pensando ojos base boca neutral)
    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    # =========================================================================
    # CONTENIDO — lo que le quedo dando vueltas del sotano
    # =========================================================================

    piensa "..."
    piensa "..."

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # Encerrado en su pieza: lo unico que puede hacer es acostarse, y dormir es
    # el disparador de la ultima parte (_vd30_trigger_dormir).
    #
    # `dormir` NO va en acciones_bloqueadas a proposito — es la unica que queda
    # habilitada. Todo lo demas cae en el mensaje_accion_default.
    $ activar_restriccion(
        locaciones_permitidas=["casa_hmc"],
        acciones_bloqueadas=["avanzar_tiempo", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("No tengo ganas de nada, mejor me acuesto"),
        mensaje_accion_default=_("No tengo ganas de nada, mejor me acuesto"),
    )

    $ vd30_fase = 2

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 4 · LA MADRUGADA — el cierre de la quest
################################################################################
## Lo dispara DORMIR (trigger fase "antes"). Mismo recurso que el despertar por
## mensaje prioritario: la animacion de dormir ya corrio, se empuja el horario
## hasta trasnoche y NUNCA se llama a dormir(), asi que el dia no cambia.

label violet_deseo_30_madrugada:

    # HORARIO_TRASNOCHE - horario_actual en vez de un "+1" fijo: la fase 2
    # empieza de noche, pero si por lo que fuera se llegara acá a otra hora la
    # cuenta sigue dando bien. Si ya era trasnoche, la resta da 0 y no pasa nada.
    $ avanzar_horario_multiple(HORARIO_TRASNOCHE - horario_actual)

    # Se levanta la restriccion antes de la escena: si se cortara a la mitad, el
    # jugador quedaria encerrado en su pieza sin poder dormir de nuevo.
    $ desactivar_restriccion()
    $ vd30_fase = 3

    $ ocultar_hud()
    window show

    $ _vd30_loc_hmc = sistema_locaciones.obtener_locacion("casa_hmc")
    $ _vd30_bg = _vd30_loc_hmc.background if _vd30_loc_hmc else "#1a1a1a"
    scene expression _vd30_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # =========================================================================
    # CONTENIDO — PARTE A · se despierta solo
    # =========================================================================

    piensa "..."

    # =========================================================================
    # CONTENIDO — PARTE B · entra Violet en pijama
    # =========================================================================

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
    # CONTENIDO — PARTE C · Violet se va y el MC queda solo
    # =========================================================================

    hide violet_parada with dissolve

    # (Mc cuerpo pensando)
    show mc_parado_base c_rbase_pensando with sprite_fast
    piensa "..."

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_deseo_06")

    # Y se vuelve a acostar. dormir() acá es el de verdad: cambia el dia y
    # amanece. El autoguardado va justo despues, como en accion_dormir — nunca
    # adentro de dormir(), para que el checkpoint no caiga sobre esa linea.
    call screen animacion_dormir with dissolve
    $ dormir()
    $ autoguardar_partida()

    window hide
    $ mostrar_hud()
    jump game_loop

################################################################################
## Violet — Deseo 10 · "Encuentro nocturno"
################################################################################
## Segunda quest de la linea de deseo. Es la primera de la linea que otorga
## HITO (ver characters/violet/hitos_violet.rpy).
##
##     archivo   violet_deseo_10.rpy
##     quest     violet_deseo_02          (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_02    (lo fija el motor: "quest_" + id)
##
## DISPARADOR UNICO: dormir. Con la quest lista, acostarse NO pasa el dia: el
## MC se despierta de madrugada muerto de sed y la partida sigue en el mismo
## dia, de trasnoche. Por eso la quest esta excluida del boton generico
## "Buscar un momento a solas" del menu de interaccion.
##
## LA ESCENA TIENE DOS MITADES, y por eso hay dos labels:
##
##   1. violet_deseo_10_despertar — el trigger de dormir. Despierta al MC,
##      deja el mundo en modo "salida a la cocina" (recorrido acotado, tiempo
##      frenado) y devuelve el control. El jugador camina hasta la cocina.
##
##   2. quest_violet_deseo_02 — lo dispara la accion "Tomar agua" de la cocina.
##      Es la escena en si: aparece Violet y se cierra la quest.
##
## Entre las dos el jugador esta suelto, asi que el estado vive en un flag
## `default` (vd10_sed_activa) y no en variables de escena: tiene que
## sobrevivir a que guarde la partida en el medio.


################################################################################
## Estado
################################################################################

# True entre el despertar y el vaso de agua. Prende la accion "Tomar agua" de
# la cocina y marca que la restriccion de recorrido esta puesta.
default vd10_sed_activa = False


init python:

    def _vd10_trigger_dormir():
        """
        Trigger de dormir, fase "antes": corre con la animacion de dormir ya
        mostrada y ANTES de que dormir() cambie el dia.

        La fase importa. En "despues" el dia ya avanzo y el despertar de
        madrugada caeria en la noche siguiente; en "antes" se devuelve un label
        que mueve el horario a mano y el dia queda donde estaba.
        """
        if not quest_lista_para_boton("violet_deseo_02"):
            return None
        return "violet_deseo_10_despertar"

    def _vd10_tomar_agua_visible():
        """Condicion de la AccionLocacion 'Tomar agua' (actions_catalog)."""
        return getattr(store, 'vd10_sed_activa', False)


init 5 python:

    registrar_trigger_dormir("violet_deseo_10_sed", "antes",
                            _vd10_trigger_dormir)


################################################################################
## 1 · EL DESPERTAR — el MC se levanta de madrugada con sed
################################################################################
## Mismo recurso que usa el motor para el despertar por mensaje prioritario
## (timesystem_core, accion_dormir): la animacion de dormir ya corrio, se
## empuja el horario hasta trasnoche y NO se llama a dormir(), asi que el dia
## no cambia.

label violet_deseo_10_despertar:

    # HORARIO_TRASNOCHE - horario_actual en vez de un "+1" fijo: dormir tambien
    # se puede desde la mañana o la tarde. Si ya era trasnoche la resta da 0 y
    # avanzar_horario_multiple no hace nada, que es lo correcto — ya estamos en
    # el horario de la escena.
    $ avanzar_horario_multiple(HORARIO_TRASNOCHE - horario_actual)

    $ ocultar_hud()
    window show

    piensa "Estoy muerto de sed, voy a ir a la cocina por algo para tomar"

    # Recorrido acotado al camino habitacion → cocina y tiempo frenado.
    #
    # casa_hmc NO va en la lista y no es un olvido: la restriccion filtra el
    # DESTINO de un movimiento, no donde estas parado. El MC arranca en su
    # habitacion, puede salir, y hasta tomar el agua no puede volver a
    # meterse en la cama. Es el mismo recorte que usan la quest 0_b y la 04_d4.
    #
    # Los NPCs se ocultan porque a esta hora estan durmiendo: si alguna rutina
    # dejara a alguien parado en el living, la escena de Violet perderia todo
    # el efecto de aparecer de la nada.
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba", "casa_living",
                            "casa_pasilloabajo", "casa_cocina"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                            "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Primero voy a tomar algo, me estoy muriendo de sed"),
        mensaje_accion_default=_("Primero voy a tomar algo, me estoy muriendo de sed"),
        npcs_ocultos=["violet", "monica", "jasmine"],
    )

    # Recien acá: la accion "Tomar agua" aparece en la cocina y el flag marca
    # que hay una restriccion puesta que alguien tiene que sacar.
    $ vd10_sed_activa = True

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA ESCENA — la dispara la accion "Tomar agua" de la cocina
################################################################################

label quest_violet_deseo_02:

    # Apagar el flag y la restriccion es lo PRIMERO. Si la escena se cortara
    # mas adelante, el jugador quedaria encerrado en el recorrido de la cocina
    # sin forma de volver a dormir (mismo criterio que violet_q4d4_avisar).
    $ vd10_sed_activa = False
    $ desactivar_restriccion()

    $ ocultar_hud()
    window show

    # La cocina de trasnoche. Se llega acá desde la accion de esa locacion, asi
    # que la locacion actual ya es la correcta.
    $ _vd10_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd10_bg

    show violet_tanga_qd10 c_tanga b_none at right with sprite_normal

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Ehhh... Hola"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_tanga_qd10 b_hablando
    violet "Hola"
    show violet_tanga_qd10 b_hablandochica
    violet "¿Tambien con sed?"
    show violet_tanga_qd10 b_none
    
    piensa "Se ve que esta dormida y no se dio que esta en tanga"


    show violet_tanga_qd10 c_tomando with sprite_fast
    pause 0.5
    show violet_tanga_qd10 c_tanga with sprite_fast
    pause 0.5

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Si, me tengo que acostumbrar a llevarme agua antes de dormir"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_tanga_qd10 b_hablando
    violet "Yo tengo una botella pero siempre olvido de llenarmela"
    show violet_tanga_qd10 b_none

    show mc_parado_base b_hablando 
    mc "No es una mala idea, pero tampoco es tanto problema levantarse"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "Para mi si porque me puedo desvelar y me cuesta mucho volver a dormir"
    show violet_tanga_qd10 b_hablandochica
    violet "¿Sabes que hora es?"
    show violet_tanga_qd10 b_none
    
    piensa "Esta mas habladora de lo habitual tambien, parece otra persona"

    show mc_parado_base b_hablando c_rbase_celu o_abajonm with sprite_fast
    mc "Son las 5 am"
    show mc_parado_base b_none c_rbase_base o_base with sprite_fast

    show violet_tanga_qd10 b_hablando
    violet "¿A ti te cuesta dormirte tambien cuando te levantas?"
    show violet_tanga_qd10 b_none

    show violet_tanga_qd10 c_tomando with sprite_fast
    pause 0.5
    show violet_tanga_qd10 c_tanga with sprite_fast
    pause 0.5

    show mc_parado_base b_hablando c_rbase_pensando o_arribanm with sprite_fast
    mc "En la mayoria de los casos me vuelvo a dormir rapido"
    show mc_parado_base b_none c_rbase_base o_base with sprite_fast

    show violet_tanga_qd10 b_hablando
    violet "Que envidia"
    show violet_tanga_qd10 b_hablandochica
    violet "¿Te puedo hacer una pregunta?"
    show violet_tanga_qd10 b_none

    show mc_parado_base b_hablando
    mc "Si, ¿Que pasa?"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "¿Por que me estas mirando tanto?"
    show violet_tanga_qd10 b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Ehh... no te estaba mirando"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    piensa "Me es imposible no mirarla, no se que espera"

    show violet_tanga_qd10 b_hablando ot_colorada
    violet "Aunque me imagino..."
    show violet_tanga_qd10 b_hablandochica
    violet "Si me dices que miras y por que te puedo dar una recompensa"
    show violet_tanga_qd10 b_sonrisa

    piensa "Sabe por que la estoy mirando, no se a donde quiere llegar y no conozco esta faceta suya"
    piensa "No le quiero decir, pero me voy a arrepentir mas de perderme esa recompensa"

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Te estoy mirando a vos"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "¿Y por que?"
    show violet_tanga_qd10 b_sonrisa

    show mc_parado_base b_hablando
    mc "Porque tenerte adelante en tanga me calienta un poco, no voy a mentirte"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "Asi que te volviste un pervertido"
    show violet_tanga_qd10 b_sonrisa

    show mc_parado_base b_hablando
    mc "Es una reaccion natural, soy un hombre"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "¿Te pones asi asi solo por una tanga o cambia porque sea yo?"
    show violet_tanga_qd10 b_sonrisa

    show mc_parado_base b_hablando
    mc "Creo que ya te respondi lo que me preguntaste y no vi mi recompensa"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "Depende de tu respuesta ahora puede mejorar o empeorar"
    show violet_tanga_qd10 b_sonrisa

    show mc_parado_base b_hablando
    mc "Supongo que es por la situacion y por que seas vos"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "Muy bien... honesto"
    show violet_tanga_qd10 b_hablandochica
    violet "Bueno, me voy a dormir antes de terminar de desvelarme"
    show violet_tanga_qd10 b_sonrisa

    show mc_parado_base b_hablando
    mc "¿Y mi recompensa?"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "Nunca dije que iba a ser ahora"
    show violet_tanga_qd10 b_hablandochica
    violet "¿Que estabas esperando?"
    show violet_tanga_qd10 b_sonrisa

    piensa "Cai completamente... no le voy a seguir mas el juego"

    show mc_parado_base b_hablando
    mc "Nada, me voy a dormir, tampoco me quiero desvelar"
    show mc_parado_base b_none

    show violet_tanga_qd10 b_hablando
    violet "Nos vemos"
    show violet_tanga_qd10 b_sonrisa

    hide violet_tanga_qd10
    hide mc_parado_base
    with dissolve


    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    $ _vd10_bg_final = sistema_locaciones.locacion_actual.background
    scene expression _vd10_bg_final with fade

    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    piensa "Violet siempre me atrajo, quizas porque teniamos miles de cosas en comun"
    piensa "Pero ahora es distinto, me cuesta no mirarla con otros ojos y este tipo de situaciones no ayudan"
    piensa "Que ella lo sepa no se si es bueno o es malo, pero ahora no voy a ganar nada con pensarlo"
    piensa "Mejor me voy a dormir"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_deseo_02")

    # El jugador vuelve al loop en su habitacion, de trasnoche y ya sin
    # restriccion, asi que puede dormir cuando quiera.
    window hide
    $ mostrar_hud()
    jump game_loop

################################################################################
## Quest 0_b de Mónica — La notebook de Mónica
################################################################################
## Inicia al dia siguiente de completar la quest 0_a.
## Mientras está activa se bloquea avanzar tiempo y dormir.
## Al entrar al living se dispara la conversacion automáticamente.

init python:

    def setup_restriccion_monica_quest0b():
        """
        accion_al_entrar de ETAPA_BOTON_LISTO: bloquea avanzar tiempo y dormir.
        El movimiento y la interaccion con NPCs siguen permitidos.

        OJO: aca NO se registra el disparo de la quest. Antes terminaba con
        `r.registrar_label_locacion("casa_living", ...)` y eso era el bug —
        ver el comentario del trigger, abajo.
        """
        activar_restriccion(
            acciones_bloqueadas=["avanzar_tiempo", "dormir"],
            mensajes_acciones={
                "avanzar_tiempo": "Deberia ver que le pasa a Monica",
                "dormir": "Deberia ver que le pasa a Monica",
            },
            npcs_interactuables=["violet", "monica", "jasmine"],
        )


    ############################################################################
    ## DISPARO DE LA QUEST
    ############################################################################
    ## Trigger de game_loop registrado en init, y NO colgado del objeto de
    ## restriccion, que era como estaba antes:
    ##
    ##     r.registrar_label_locacion("casa_living", "monica_q0b_check_living")
    ##
    ## POR QUE ROMPIA: `restriccion_quest_activa` es UN SOLO slot global.
    ## `activar_restriccion` lo reemplaza entero y `desactivar_restriccion` lo
    ## borra — y en el proyecto hay 32 llamadas a la primera y 22 a la segunda.
    ## Como `accion_al_entrar` corre UNA sola vez (en la transicion de etapa),
    ## cualquier contenido que corriera despues se llevaba puesto el disparo y la
    ## quest quedaba muerta para siempre en el panel de pistas. Era facil de
    ## alcanzar: la restriccion bloquea dormir y avanzar tiempo pero NO el
    ## movimiento, asi que el jugador se iba a hacer contenido de Violet o
    ## Jasmine y ese contenido terminaba con desactivar_restriccion(). Bug real
    ## reportado por jugadores: a algunos la 0_b no les arrancaba nunca al dia
    ## siguiente de la 0_a.
    ##
    ## La restriccion se mantiene (bloquear dormir/avanzar): perderla es
    ## inofensivo. Lo que no puede depender de ella es el disparo.
    ##
    ## Efecto secundario bueno: el trigger tambien dispara si el jugador YA esta
    ## en el living cuando la quest queda lista. El registro por locacion pedia
    ## salir y volver a entrar.

    def _gl_trigger_monica_q0b():
        q = store.sistema_quests.obtener_quest("monica_questprincipal_0_b")
        if not (q and q.activa and not q.completada
                and q.etapa_actual == ETAPA_BOTON_LISTO):
            return None
        loc = store.sistema_locaciones.locacion_actual
        if loc and loc.id == "casa_living":
            return "quest_monica_questprincipal_0_b"
        return None


init 5 python:
    # 25: por encima del tutorial de exploracion (20), para que un gate que
    # bloquea dormir no quede postergado, y por debajo de jasmine_0b (30).
    registrar_trigger_game_loop("monica_q0b", _gl_trigger_monica_q0b, prioridad=25)


################################################################################
## QUEST 0_B — Label principal
################################################################################

label quest_monica_questprincipal_0_b:

    # Levantar la restricción que bloqueaba avanzar tiempo / dormir
    $ desactivar_restriccion()
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Fondo del living actual (robusto a cualquier horario)
    $ _bg_mq0b = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_mq0b with fade

    # Mónica con el celular a la derecha, MC normal a la izquierda
    show monica_parada c_rbase_celu o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    show mc_parado_base b_hablando
    mc "Mónica, ¿está todo bien? Te escuché desde arriba"
    show mc_parado_base b_none

    show monica_parada b_hablando o_aburridosnm
    monica "Ay, no me hagas caso... Es esta computadora, que dejó de andar de la nada"
    show monica_parada b_none o_base

    show monica_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    monica "Llamé al servicio técnico y me dijeron que recién pueden pasar a buscarla la semana que viene"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "¿Y es muy urgente?"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Bastante. Me pedí unos días para hacer home office hasta que te acomodes..."
    show monica_parada b_hablandochica
    monica "...y la necesito para trabajar. Sin computadora no puedo hacer nada"
    show monica_parada b_none c_rbase_base with sprite_normal

    show mc_parado_base b_hablando c_rbase_pensando o_arribanm with sprite_normal
    mc "Si quieres la puedo revisar, no soy un experto, pero capaz es algo que puedo arreglar yo"
    show mc_parado_base b_none c_rbase_base o_base with sprite_normal

    show monica_parada b_hablando
    monica "¿En serio? ¡Ay, eres un amor! Te la traigo ya mismo"
    show monica_parada b_feliz

    # Mónica se retira hacia la izquierda
    show monica_parada at personaje_salir_izquierda
    pause 1.0
    hide monica_parada with dissolve

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "Ojalá sea algo fácil y la pueda arreglar..."
    show mc_parado_base c_rbase_base o_base with sprite_normal

    # Mónica vuelve: entra desde la izquierda hasta right, flipeada, y gira al llegar
    show monica_parada o_base b_none at reentrar_izquierda_a_right
    pause 1.6
    # Y se la planta en el destino. Si el jugador clickeo y corto el `pause`, el
    # ease quedo a mitad y sin esto Monica se queda parada en el medio toda la
    # escena que sigue.
    show monica_parada at reentrar_izquierda_a_right_final

    #insertar sprite con la comunpatora y se la da, agregar al mc con la computadora y que la guarda en la mochila

    show monica_parada b_hablando o_felicesnm
    monica "De verdad, te lo agradezco un montón"
    show monica_parada b_none o_base

    show mc_parado_base b_hablando
    mc "Tranquila. Apenas tenga alguna novedad, te aviso"
    show mc_parado_base b_none

    show monica_parada b_feliz o_felicesnm
    monica "Gracias. Te dejo trabajar entonces, cualquier cosa estoy por aquí"
    show monica_parada b_none o_base

    # Mónica se va de nuevo hacia la izquierda
    show monica_parada at personaje_salir_izquierda
    pause 1.0
    hide monica_parada with dissolve

    # El MC recibe la notebook
    $ agregar_al_inventario("notebook_monica")

    # Tutorial de inventario / items
    tutorial "Los objetos que consigues se guardan en tu inventario (el icono de la mochila en la parte superior derecha de la pantalla)"
    tutorial "Para usar uno, solo tendrás que hacer click sobre su icono"

    window hide

    # Completar la quest
    $ completar_quest_actual("monica", quest_id="monica_questprincipal_0_b")

    $ mostrar_hud()
    jump game_loop

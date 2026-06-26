################################################################################
## Quest 0_b de Mónica — La notebook de Mónica
################################################################################
## Inicia al dia siguiente de completar la quest 0_a.
## Mientras está activa se bloquea avanzar tiempo y dormir.
## Al entrar al living se dispara la conversacion automáticamente.

init python:

    def setup_restriccion_monica_quest0b():
        """
        accion_al_entrar de ETAPA_BOTON_LISTO: bloquea avanzar tiempo y dormir,
        y registra el auto-trigger de la quest al entrar al living.
        El movimiento y la interacción con NPCs siguen permitidos.
        """
        r = activar_restriccion(
            acciones_bloqueadas=["avanzar_tiempo", "dormir"],
            mensajes_acciones={
                "avanzar_tiempo": "Deberia ver que le pasa a Monica",
                "dormir": "Deberia ver que le pasa a Monica",
            },
            npcs_interactuables=["violet", "monica", "jasmine"],
        )
        r.registrar_label_locacion("casa_living", "monica_q0b_check_living")


################################################################################
## CHECK LOCACIÓN — Auto-trigger al entrar al living
################################################################################

label monica_q0b_check_living:
    $ _q_m0b = sistema_quests.obtener_quest("monica_questprincipal_0_b")
    if (_q_m0b and _q_m0b.activa and not _q_m0b.completada and
            _q_m0b.etapa_actual == ETAPA_BOTON_LISTO):
        jump quest_monica_questprincipal_0_b
    return


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
    mc "Monica, ¿Está todo bien? Te escuché desde arriba"
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
    tutorial "Acabás de [colorear_quest('Recibir Objeto')]: la notebook de Monica. Los objetos que consigues se guardan en tu [colorear_quest('Inventario')]"
    tutorial "Puedes abrir el inventario desde el [colorear_quest('Icono de la Mochila')] en la parte superiro derecha, desde ahí, revisar y usar los objetos que tengas [colorear_quest('Haciendo Click')] en ellos"
    tutorial "Algunos objenos no se pueden usar desde el inventario, sirven para ser utilizados en algún momento especifico del juego"
    tutorial "Mientras que otros si puedes usarlos desde el mismo. Al usarlos disparara su acción relacionada o te indicara si hay algún requisito adicional para hacer, como una locacion o horario"
    tutorial "Probá [colorear_item('Notebook de Monica')] desde el inventario cuando estés en [colorear_locacion('Tu Habitacion')]"

    window hide

    # Completar la quest
    $ completar_quest_actual("monica")

    $ mostrar_hud()
    jump game_loop

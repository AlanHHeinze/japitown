################################################################################
## Violet — LINEA DE AMOR · labels PLACEHOLDER
################################################################################
## ⚠️ CONTENIDO DE PRUEBA. Sirve para testear el circuito completo del sistema
## de hitos (tope de stat → quest → hito → ventajas) sin escribir la narrativa.
## Cada label se reemplaza por su escena real cuando toque.
##
## Los 6 labels son stubs de 3 lineas que saltan a un cuerpo comun: asi se puede
## reemplazar una quest a la vez sin tocar las otras. Para escribir la escena
## real de una, se borra su `jump` y se escribe la escena en su lugar.
##
## El nombre del label lo fija el motor: Quest.label_quest = "quest_<id>".

label quest_violet_amor_01:
    $ _vqa_quest_id = "violet_amor_01"
    $ _vqa_titulo = "amor 5"
    jump _violet_amor_placeholder

label quest_violet_amor_02:
    $ _vqa_quest_id = "violet_amor_02"
    $ _vqa_titulo = "amor 10"
    jump _violet_amor_placeholder

label quest_violet_amor_03:
    $ _vqa_quest_id = "violet_amor_03"
    $ _vqa_titulo = "amor 15"
    jump _violet_amor_placeholder

label quest_violet_amor_04:
    $ _vqa_quest_id = "violet_amor_04"
    $ _vqa_titulo = "amor 20"
    jump _violet_amor_placeholder

label quest_violet_amor_05:
    $ _vqa_quest_id = "violet_amor_05"
    $ _vqa_titulo = "amor 25"
    jump _violet_amor_placeholder

label quest_violet_amor_06:
    $ _vqa_quest_id = "violet_amor_06"
    $ _vqa_titulo = "amor 30"
    jump _violet_amor_placeholder


################################################################################
## Cuerpo comun de la escena de prueba
################################################################################

label _violet_amor_placeholder:

    $ ocultar_hud()
    window show

    # Locacion y horario actuales: la escena arranca donde esta el jugador.
    $ _vqa_loc = sistema_locaciones.locacion_actual
    if _vqa_loc and _vqa_loc.background:
        scene expression _vqa_loc.background with fade

    # mc_cerca / npc_cerca: los dos se encuentran en x=960, cara a cara.
    # (Mc cuerpo base ojos base boca hablando)
    show mc_parado_base c_rbase_base o_base b_hablando at mc_cerca

    # cuerpo_activo() para no asumir la ropa que tiene puesta.
    $ _vqa_cuerpo = cuerpo_activo("violet")
    # (Violet cuerpo base ojos base boca sonrisa leve)
    if _vqa_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_sonrisaleve at npc_cerca
    else:
        show violet_parada c_rbase_base ca_base o_base b_sonrisaleve at npc_cerca
    with sprite_normal

    mc "Esto es una prueba de que la quest de [_vqa_titulo] anda."

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Sí, anda."

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ completar_quest_actual("violet", quest_id=_vqa_quest_id)

    window hide
    $ mostrar_hud()
    jump game_loop

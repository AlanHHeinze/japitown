################################################################################
## Quest 09_b — [Pendiente de diseno]
################################################################################
## Se dispara al despertar del tercer dia de quest 09_a si violet_enferma_atencion >= 3.
## Interrumpe el flujo de accion_dormir (como hace quest 08_a).
################################################################################

label violet_quest09b_despertar:
    # OJO: el archivo se llama 09_b pero la quest que cierra es la 09_a — este
    # label es su desenlace, no hay ninguna quest "09_b" registrada.
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_09_a")
    call mensajes_al_despertar from _call_quest09b_despertar_msgs
    $ renpy.restart_interaction()
    $ mostrar_hud()
    jump game_loop

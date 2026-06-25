################################################################################
## Quest 09_b — [Pendiente de diseno]
################################################################################
## Se dispara al despertar del tercer dia de quest 09_a si violet_enferma_atencion >= 3.
## Interrumpe el flujo de accion_dormir (como hace quest 08_a).
################################################################################

label violet_quest09b_despertar:
    $ completar_quest_actual("violet")
    call mensajes_al_despertar from _call_quest09b_despertar_msgs
    $ renpy.restart_interaction()
    $ mostrar_hud()
    jump game_loop

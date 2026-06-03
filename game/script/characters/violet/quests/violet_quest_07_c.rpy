################################################################################
## Quest 07_c — Cosplay de reemplazo
################################################################################
## La narrativa de esta quest ocurre íntegramente en el chat (violet_q7c_g1).
## Este label solo cierra la quest cuando el jugador interactúa con Violet
## tras completar el chat.
################################################################################

label quest_violet_questprincipal_07_c:
    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop

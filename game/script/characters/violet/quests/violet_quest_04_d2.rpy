################################################################################
## Quest 04_d2 — Algo por ella
################################################################################
## Paso intermedio entre la 04_d y la 04_e.
##
## Disparador unico: el boton "¿Puedo hacer algo por vos?" del menu de
## interaccion de Violet (ver interactions_violet.rpy).
##
## La conversacion pasa en la LOCACION y el HORARIO actuales — no mueve a nadie
## ni fuerza un fondo. Misma estructura que violet_quest05b_hablar.
##
## EL DIALOGO ESTA VACIO A PROPOSITO: lo escribe Alan.

# Ropa de Violet al momento de hablar (pijama o ropa base). Se lee una sola vez
# al entrar para no consultar cuerpo_activo() en cada show.
default vq4d2_cuerpo = "c_rbase"


################################################################################
## LABEL PRINCIPAL — llamado por el botón del menú de interacción
################################################################################

label quest_violet_questprincipal_04_d2:
    # De noche Violet no acepta pedidos: contesta y listo. Vale para toda la
    # cadena 04_d2 → 04_d6 (ver violet_quest_04_favores.rpy).
    if violet_favores_es_de_noche():
        jump violet_q4dfav_de_noche
    jump violet_quest04d2_hablar


################################################################################
## HABLAR — conversación en la locación y el horario actuales
################################################################################

label violet_quest04d2_hablar:

    $ vq4d2_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv



    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda


    show mc_parado_base b_hablando
    mc "Hola, Violet. ¿Cómo estás?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_normal
    violet "¿Qué pasa?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Nada, solo quería saber cómo estás"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica
    violet "Estoy bien..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Y no necesitas nada?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_juzgandonm c_rbase_pensando with sprite_normal
    violet "¿Cómo qué?"
    show violet_parada b_none o_base c_rbase_base with sprite_normal

    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_normal
    mc "No sé, solo preguntaba, capaz había algo con lo que te podía ayudar o hacer por ti"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_normal
    violet "¿Qué es lo que quieres?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "De verdad nada, si en algún momento necesitas algo, no dudes en pedírmelo"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica
    violet "Lo voy a tener en cuenta, gracias"
    show violet_parada b_none

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    # =========================================================================

    # Al completar arranca sola la 04_d3 (encadenada por quest_anterior).
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_d2")

    window hide
    $ mostrar_hud()
    jump game_loop

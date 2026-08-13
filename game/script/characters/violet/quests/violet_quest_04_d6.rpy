################################################################################
## Quest 04_d6 — El cierre del arco de los favores
################################################################################
## Apenas termina la tercera limpieza, el MC va a cobrarse el favor y se cierra
## todo el arco. Al completarse se abre la 04_e.
##
## LA ESCENA PASA SIEMPRE DENTRO DE LA HABITACION DE VIOLET. Dos caminos:
##   - boton "Ya terminé de limpiar" del menu, que solo aparece si ya estás
##     adentro
##   - opcion de puerta con el mismo texto, que es como entrás si ella está en
##     su cuarto y vos afuera
## Por eso el label mueve al MC a casa_hviolet: viniendo de la puerta todavia
## esta en el pasillo, y la conversacion no puede arrancar ahi.


label violet_q4d6_cierre:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    # Adentro de la habitacion, con el fondo del horario actual.
    $ sistema_locaciones.mover_a_locacion("casa_hviolet")
    $ _loc_d6 = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_conv = _loc_d6.background if _loc_d6 else "#1a1a1a"
    scene expression _bg_conv with fade

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda


    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "Listo ya hice todo lo que me pediste"
    show mc_parado_base b_abiertachica 
    mc "Ahora quiero mi recompensa"
    show mc_parado_base b_none 

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada b_hablando o_arribanm c_pijama_pensando with sprite_fast
    else:
        show violet_parada b_hablando o_arribanm c_rbase_pensando with sprite_fast
    violet "Lo se... no estabas haciendo las cosas porque eres un buen chico como decias"
    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada b_none o_base c_pijama_base with sprite_fast
    else:
        show violet_parada b_none o_base c_rbase_base with sprite_fast

    show mc_parado_base b_hablando 
    mc "A ver esas fotos..."
    show mc_parado_base b_none 

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_verguenza with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_verguenza with sprite_fast
    violet "¿Tantas ganas de verlas tenes?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Despues de limpiar toda la casa y hacer todo lo que me pediste, si"
    show mc_parado_base b_none

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_dedolabio with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_dedolabio with sprite_fast
    violet "Te volvist un pervertido"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "No se que es pero si ser un perverito, o ser una pervertidas que manipula a otros"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_brazoscruzados with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_fast
    violet "No soy una pervertida..."
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "Si no lo fueras no estarias manipulandome con esas fotos, queres mostrarmelas, solo que quierias aprovechar para obtener algo a cambio"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Basta"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_base with sprite_fast
    mc "Bueno, yo ya cumpli, ahora te toca a vos"
    show mc_parado_base b_abiertachica
    mc "A ver..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No te las voy a mostar ahora"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_fast
    mc "¿Y entonces?"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica
    violet "Te lo mando despues por mensaje"
    show violet_parada b_none

    show mc_parado_base b_hablando 
    mc "Confio en vos"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Chau"
    show violet_parada b_none

    hide violet_parada 

    show mc_parado_base c_rbase_pensando with sprite_fast
    piensa "Bueno ahora solo queda esperar"


    # Si va alguna recompensa de stat, acá:
    #     $ cambiar_stat1("violet", N, reserva=True)
    #     $ cambiar_stat2("violet", N, reserva=True)

    # Al completar se abre la 04_e (El cosplay de Violet IV).
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_d6")

    window hide
    $ mostrar_hud()
    jump game_loop

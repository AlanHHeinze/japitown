################################################################################
## Quest 04_d3 — Las golosinas (favor 1 de 3)
################################################################################
## Violet le pide golosinas al MC. Las golosinas se compran en la tienda
## (CATALOGO_ITEMS["golosinas"], $20, entrega en 1 dia), asi que la espera es
## parte del favor.
##
## Recorrido:
##   1. "Preguntarle si necesita algo"  → _pedido        (prende vq4d3_pedido_hecho)
##      Al final del pedido se evalua el inventario:
##        - con golosinas   → menu: _pedido_dar (completa) / _pedido_no_dar
##        - sin golosinas   → _pedido_sin_golosinas
##   2. mismo boton, sin golosinas      → _recordatorio
##   3. boton extra "Darle las golosinas" (aparece con el item en el inventario)
##                                      → _entregar      (completa la quest)
##
## Hay DOS puntos de entrega (_pedido_dar y _entregar) porque son momentos
## narrativos distintos: dárselas en el acto o volver después con ellas. Los dos
## hacen lo mismo a nivel sistema — quitar el item y completar la quest.
##
## El ruteo de los pasos 1 y 2 lo hace violet_favores_boton
## (violet_quest_04_favores.rpy); el paso 3 tiene su propio boton en el menu.
##
## LOS DIALOGOS ESTAN VACIOS A PROPOSITO: los escribe Alan.


################################################################################
## PEDIDO — Violet le pide las golosinas
################################################################################

label violet_q4d3_pedido:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "Veo que todavía estás con ganas de ser servicial"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿Cuándo no lo soy?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica
    violet "Lo que digas..."
    show violet_parada b_hablando
    violet "Estoy con ganas de comer algunas golosinas"
    show violet_parada b_none

    $ vq4d3_pedido_hecho = True

    # Si el MC ya tiene golosinas encima puede resolverlo en el momento, sin
    # tener que ir a comprarlas. Las tres ramas siguen con la escena YA montada
    # (Violet y el MC en pantalla), asi que no vuelven a hacer scene ni show.
    if inventario.get("golosinas", 0) > 0:
        menu:
            "Darle unas golosinas":
                jump violet_q4d3_pedido_dar

            "Quedarse con las golosinas":
                jump violet_q4d3_pedido_no_dar
    else:
        jump violet_q4d3_pedido_sin_golosinas


################################################################################
## PEDIDO → DAR — se las da en el momento y cierra el favor
################################################################################

label violet_q4d3_pedido_dar:

    show mc_parado_base b_hablando
    mc "Tengo algunas golosinas"
    show mc_parado_base b_none

    # (Mc cuerpo mochila 1)
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 2)
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 3)
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 4)
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3

    # (Mc cuerpo regalo violet)
    show mc_parado_base c_rbase_bolsamadera with sprite_normal
    pause 0.3
    # (Mc boca hablando cuerpo base)
    show mc_parado_base b_hablando c_rbase_base with sprite_normal

    $ quitar_del_inventario("golosinas")

    # (Violet cuerpo recibiendo regalo)
    show violet_parada c_rbase_bolsamadera with sprite_normal
    mc "Toma"
    # (Mc boca neutral)
    show mc_parado_base b_none

    show violet_parada o_abajonm
    violet "..."
    show violet_parada b_hablandochica o_base
    violet "¿Desde hace cuánto las tienes ahí?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Las quieres o no?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bueno, está bien"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Necesitas algo más?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No, por ahora no, gracias"
    show violet_parada b_none

    hide violet_parada

    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "No creo que con esto sea suficiente, tendré que hacer más cosas por ella si quiero que me mande la otra foto"
    piensa "Mañana podría seguir intentándolo"


    # Al completar arranca sola la 04_d4, que espera un día antes de habilitarse.
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_d3")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## PEDIDO → NO DAR — se las guarda
################################################################################
## No completa nada: la quest sigue y el favor queda pendiente. El jugador puede
## dárselas después con el botón "Darle las golosinas".

label violet_q4d3_pedido_no_dar:

    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "Mmmm... Mejor le doy las golosinas en otro momento"

    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Bueno, cuando las tenga te aviso"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Está bien, espero que no te olvides"
    show violet_parada b_none

    hide violet_parada

    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "En algún momento le voy a tener que dar las golosinas si quiero progresar con esto"

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## PEDIDO → SIN GOLOSINAS — no tiene ninguna encima
################################################################################

label violet_q4d3_pedido_sin_golosinas:

    show mc_parado_base b_hablando
    mc "Ahora no tengo, pero puedo comprarte algunas"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Está bien, espero que no te olvides"
    show violet_parada b_none

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## RECORDATORIO — vuelve a preguntar y Violet le recuerda el pedido
################################################################################

label violet_q4d3_recordatorio:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "¿Ya conseguiste las golosinas?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Cierto, las golosinas, me había olvidado"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bueno, voy a estar esperándolas"
    show violet_parada b_none

    hide violet_parada

    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "En algún momento le voy a tener que dar las golosinas si quiero progresar con esto"


    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## ENTREGAR — el MC le da las golosinas y cierra el favor
################################################################################

label violet_q4d3_entregar:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Tengo algunas golosinas"
    show mc_parado_base b_none

    # (Mc cuerpo mochila 1)
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 2)
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 3)
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 4)
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3

    # (Mc cuerpo regalo violet)
    show mc_parado_base c_rbase_bolsamadera with sprite_normal
    pause 0.3
    # (Mc boca hablando cuerpo base)
    show mc_parado_base b_hablando c_rbase_base with sprite_normal

    $ quitar_del_inventario("golosinas")

    # (Violet cuerpo recibiendo regalo)
    # Cada cambio de cuerpo de Violet va con la rama de vq4dfav_cuerpo: la
    # escena pasa en el horario actual, asi que de noche esta en pijama y un
    # show a c_rbase_* la cambiaria de ropa en medio de la conversacion.
    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada c_pijama_bolsamadera with sprite_normal
    else:
        show violet_parada c_rbase_bolsamadera with sprite_normal
    mc "Toma"
    # (Mc boca neutral)
    show mc_parado_base b_none

    show violet_parada o_abajonm
    violet "..."
    show violet_parada b_hablandochica o_base
    violet "¿Desde hace cuánto las tienes ahí?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Las quieres o no?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bueno, está bien"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Necesitas algo más?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No, por ahora no, gracias"
    show violet_parada b_none

    hide violet_parada

    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "No creo que con esto sea suficiente, tendré que hacer más cosas por ella si quiero que me mande la otra foto"
    piensa "Mañana podría seguir intentándolo"

    # Al completar arranca sola la 04_d4, que espera un día antes de habilitarse.
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_d3")

    window hide
    $ mostrar_hud()
    jump game_loop

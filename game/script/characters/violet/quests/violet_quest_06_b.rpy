################################################################################
## Quest 06_b — La prueba del cosplay
################################################################################

# Imágenes de la quest 06 — un solo grupo para alternar sin hide ni reposicionar.
# Uso: show quest06 uno  /  show quest06 dos  /  show quest06 tres  /  show quest06 roto
layeredimage quest06:
    group cierre:
        attribute uno default:
            "images/quest/violet/quest06/quest06_1.png"
        attribute dos:
            "images/quest/violet/quest06/quest06_2.png"
        attribute tres:
            "images/quest/violet/quest06/quest06_3.png"
        attribute roto:
            "images/quest/violet/quest06/quest06_roto.png"

default violet_06b_eleccion = None

################################################################################
## Screen — Menú del cierre
################################################################################

screen vq6b_menu_cierre():
    modal True

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Bajar el cierre":
            style "choice_button"
            action Return("A")

        # Opción especial: siempre visible; en gris cuando no se cumple el requisito.
        textbutton "Forzar el cierre  💪 (3 de fuerza)":
            style "choice_button"
            action Return("C")
            sensitive (mc_fuerza >= 3)


################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_06_b:
    jump violet_quest06b_puerta


################################################################################
## PUERTA — Violet pide que espere, varios minutos despues la invita a pasar
################################################################################

label violet_quest06b_puerta:

    $ ocultar_hud()
    
    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    show mc_parado_base c_rbase_avergonzado o_base b_none at mc_izquierda
    
    window show

    show mc_parado_base b_hablando
    mc "Violet, me pediste que pasara"
    show mc_parado_base b_none
    piensa "Estoy muy nervioso, no menciono nada de lo que paso el otro día"
    piensa "Supongo que me quiere hablar de eso"

    violet "Sí, espera un momento"

    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Varios minutos más tarde...{/color}"
    pause 1.0

    violet "Pasa"

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet with fade

    #Introducir a violet con el cosplay y generar el quite del cierre

    show violet_parada cc_eva_base c_none o_base b_none ca_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "¿Qué te parece?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Wooooow"
    show mc_parado_base c_rbase_avergonzado with sprite_fast
    piensa "Tenía razón, es muy llamativo, pensé que era algo de las fotos"
    piensa "Pero en persona es otra cosa..."
    show mc_parado_base b_abiertachica
    mc "Me encanta"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica o_arribanm
    violet "¿Puedo ir al evento con esto?"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando o_arribanm c_rbase_pensando with sprite_fast
    mc "Sí... ¿Por qué no podrías?"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast

    show violet_parada b_hablandochica
    violet "Ya sabes el por qué..."
    show violet_parada b_none

    hide violet_parada with sprite_normal
    pause 0.5
    show violet_espalda e_base at right with sprite_normal
    pause 0.5

    violet "Por esto"
    show violet_espalda e_cola1 at right with sprite_normal
    pause 0.5
    show violet_espalda e_cola2 at right with sprite_normal
    pause 0.5

    violet "Me queda muy apretado aquí abajo"

    show violet_espalda e_cola1 at right with sprite_normal
    pause 0.5
    show violet_espalda e_cola2 at right with sprite_normal
    pause 0.5
    show violet_espalda e_base at right with sprite_normal


    show mc_parado_base c_rbase_facepalm o_cerrados with sprite_fast
    piensa "No lo puedo creer, es una obra de arte"
    show mc_parado_base o_base c_rbase_base with sprite_fast


    hide violet_espalda with sprite_fast
    show violet_parada cc_eva_base c_none o_base b_none ca_none at right


    show violet_parada b_hablando
    violet "Dime la verdad. No lo hagas solo porque a ti te gusta"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Lo puedes usar sin problema"
    show mc_parado_base b_abiertachica c_rbase_cuestionando with sprite_fast
    mc "Es un poco llamativo, si no te voy a mentir. Pero es algo de lo que no te tienes que preocupar"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica
    violet "Sabes que nunca me gusto llamar la atención"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Te pongas un cosplay o no, vas a llamar la atención igual"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Por qué?"
    show violet_parada b_none

    show mc_parado_base b_hablando o_arribanm c_rbase_pensando with sprite_fast
    mc "Porque eso no se va a ir a ningún lado"
    show mc_parado_base b_abiertachica o_base c_rbase_brazoscruzados with sprite_fast
    mc "Pero el motivo principal es porque eres una chica linda yendo a la Japicon jajajaja"
    show mc_parado_base b_hablando
    mc "¿No te parece suficiente?"
    show mc_parado_base b_none

    pause 0.5

    show violet_parada b_hablando
    violet "Tienes un buen punto"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Bueno, nos costo pero estamos de acuerdo"
    show mc_parado_base b_none

    piensa "Me gustaría hablar del beso, sé que ella no lo va a hacer"
    piensa "Pero tengo miedo de arruinar el momento, al fin las cosas me están saliendo bien"

    show violet_parada at mover_al_centro_lento 
    pause 1.0

    show violet_parada b_hablando
    violet "¿Te puedo pedir un favor?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí..."
    show mc_parado_base b_none

    hide violet_parada with sprite_fast
    show violet_espalda e_base at center with sprite_fast

    violet "¿Me puedes bajar un poco el cierre? Se traba y es muy molesto de sacar"

    show violet_espalda e_pelo with sprite_normal
    pause 0.5
    show violet_espalda e_lista with sprite_normal
    

    show mc_parado_base b_hablando
    mc "Emmm sí, claro"
    show mc_parado_base b_none
    piensa "Si fuese un juego para adultos, este es el momento en donde la cosa se descontrolaria"
    piensa "Pero no suelo tener esa suerte en la vida"

    hide violet_espalda
    hide mc_parado_base

    show quest06 uno at center with fade

    mc "Si esta un poco trabado, no te preocupes que lo voy a arreglar"

    violet "Cada vez que me lo intento sacar, es un problema"
    violet "Si no puedes no hay problema"

    mc "Si voy a poder"

    show quest06 dos with sprite_fast
    pause 0.3
    show quest06 tres with sprite_fast
    pause 0.3
    show quest06 dos with sprite_fast

    piensa "Que cierre de porquería"

    violet "¿Seguro que puedes?"

    call screen vq6b_menu_cierre

    if _return == "A":
        jump violet_quest06b_cierre_a
    else:
        jump violet_quest06b_cierre_c


################################################################################
## Fin compartido — completa la quest y devuelve al pasillo con tiempo +1
################################################################################

label violet_quest06b_fin:

    $ completar_quest_actual("violet")
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade
    $ avanzar_horario()
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OPCIÓN A — Bajar el cierre (siempre disponible)
################################################################################

label violet_quest06b_cierre_a:

    mc "Realmente estaba trabado, no lo puedo bajar"
    mc "Voy a hacer un poco de fuerza"

    show quest06 tres with sprite_fast
    pause 0.3
    show quest06 dos with sprite_fast

    violet "Con cuidado..."

    show quest06 uno with sprite_fast

    mc "Creo que lo trabe más, no lo puedo ni subir ahora"

    violet "Es un problema ese cierre, me costo mucho sacarmelo la otra vez"

    show quest06 tres with sprite_fast
    pause 0.3
    show quest06 dos with sprite_fast

    mc "¿Y ahora que hacemos?"

    violet "Le voy a pedir a Monica que me lo quite"

    mc "Seguro que ella lo puede arreglar"

    violet "Sí, le voy a decir ahora, antes que se haga más tarde"

    hide quest06
    show mc_parado_base c_rbase_brazoscruzados at mc_izquierda with fade
    
    piensa "Vaya, eso no salió como esperaba..."

    $ violet_06b_eleccion = "A"
    jump violet_quest06b_fin


################################################################################
## OPCIÓN C — Forzar el cierre (requiere mc_fuerza >= 3)
################################################################################

label violet_quest06b_cierre_c:


    mc "Voy a hacer un poco de fuerza"

    show quest06 tres with sprite_fast
    pause 0.3
    show quest06 dos with sprite_fast
    
    pause 0.5

    vozoff "¡CRACK! ¡CRACK! ¡CRACK!"
    vozoff "Cjjjjjj"

    show quest06 roto with fade
    pause 1.0
    
    mc "Creo que hice demasiada fuerza"

    violet "..."

    mc "..."

    violet "[mc_name] Este es el momento en que sin decir nada te vas..."


    $ violet_06b_eleccion = "C"
    jump violet_quest06b_fin

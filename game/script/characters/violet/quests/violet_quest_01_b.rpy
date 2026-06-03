################################################################################
## Violet Quest 02 Nueva — El contenido del paquete
################################################################################
## Despues de completar quest 1, el jugador tiene el item "mangas_violet".
## Puede abrirlo en su habitacion o darselo directamente a Violet.
## Segun si lo abrio o no, el dialogo cambia con 3 finales posibles.

# =============================================================================
# VARIABLES
# =============================================================================

# True cuando el jugador abrio el paquete en su habitacion
default violet_quest2n_paquete_abierto = False

# Ruta elegida al entregar el paquete (para evitar exploit de rollback)
default _ruta_vq01b = ""


################################################################################
## LABEL: Usar item mangas_violet (abrir paquete en habitacion MC)
################################################################################

label usar_mangas_violet:

    $ ocultar_hud()
    window show

    # BG segun horario
    $ _horarios_bg_vq2n = ["tarde", "tarde", "noche", "noche"]
    $ _bg_h_vq2n = _horarios_bg_vq2n[horario_actual]
    scene expression "images/bg/casa/bg_casa_" + _bg_h_vq2n + "_hmc.png" with fade

    # (Mc cuerpo regalo violet ojos abajo boca neutral)
    show mc_parado_base c_rbase_regaloviolet o_abajonm b_none at center with dissolve

    piensa "Me da algo de curiosidad que habra comprado Violet"
    piensa "Sí sé que le gusta, podría usarlo para mejorar la relación, es un buen plan... y una buena justificacion"
    piensa "Aunque quizas puede que se enoje porque lo abrí"

    menu:
        "No abrirlo":
            piensa "No quiero lidiar con Violet enojada"

            hide mc_parado_base with dissolve
            window hide
            $ mostrar_hud()
            jump game_loop

        "Abrirlo":
            piensa "Bueno... ya esta aca, no pierdo nada con ver que tiene."

            $ store.violet_quest2n_paquete_abierto = True

            piensa "A ver..."
            # (Mc cuerpo regalo violet abierto ojos abajo)
            show mc_parado_base c_rbase_regalovioletabierto o_abajonm with sprite_normal
            piensa "Hay de todo un poco, Isekai, Novelas Ligeras, Shonen..."
            # (Mc cuerpo manga yamete boca asustada)
            show mc_parado_base c_rbase_mangayamete b_asustada with sprite_normal
            piensa "Pero qué carajos es esto..."
            # (Mc cuerpo manga yamete pp)
            show mc_parado_base c_rbase_mangayametepp with sprite_normal
            pause 0.3
            # (Mc cuerpo manga yamete)
            show mc_parado_base c_rbase_mangayamete with sprite_normal
            piensa "Esto es turbio... "
            # (Mc cuerpo manga yamete pp)
            show mc_parado_base c_rbase_mangayametepp with sprite_normal
            pause 0.3
            # (Mc cuerpo manga yamete)
            show mc_parado_base c_rbase_mangayamete with sprite_normal
            pause 0.3
            # (Mc cuerpo pensando ojos arriba boca seria)
            show mc_parado_base c_rbase_pensando o_arribanm b_seria with sprite_normal
            piensa "Ahora sí sé que si Violet se entera de que revisé sus cosas va a ser un problema"
            piensa "Puedo fingir que no vi nada o usar lo que vi a mi favor"
            piensa "Dependera de como reaccione cuando le de sus cosas"

            hide mc_parado_base with dissolve
            window hide
            $ mostrar_hud()
            jump game_loop


################################################################################
## LABEL: Entry point del quest system
################################################################################

label quest_violet_questprincipal_01_b:

################################################################################
## LABEL: Dar paquete a Violet (router)
################################################################################

label dar_paquete_quest02_violet:

    $ ocultar_hud()
    window show

    # Sábado por la mañana: Violet duerme, no responde
    if dia_semana_actual == 5 and horario_actual == 0:
        piensa "Violet no responde, debe estar durmiendo"
        window hide
        $ mostrar_hud()
        jump game_loop

    # Verificar si hay otro NPC en la locacion (excluyendo a Violet)
    $ _loc_actual_id = sistema_locaciones.locacion_actual.id
    $ _npcs_aqui = sistema_npcs.obtener_npcs_en_locacion(_loc_actual_id)
    $ _otro_npc_presente = [n for n in _npcs_aqui if n.id != "violet"]

    if _otro_npc_presente:
        jump dar_paquete_quest02_violet_rechaza

    if not violet_quest2n_paquete_abierto:
        jump dar_paquete_quest02_violet_a
    else:
        jump dar_paquete_quest02_violet_b


################################################################################
## LABEL: Violet rechaza el paquete porque hay otro NPC presente
################################################################################

label dar_paquete_quest02_violet_rechaza:

    $ _bg_actual = sistema_locaciones.locacion_actual.background
    scene expression _bg_actual with fade

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo base ojos base boca neutral)
    show violet_parada c_rbase_base o_base b_none at right

    pause 0.5
    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Violet, tengo un paquete para vos"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "¿Me lo podras llevar despues a mi habitacion?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Emmm... claro no hay problema"
    # (Mc boca neutral)
    show mc_parado_base b_none

    hide mc_parado_base with dissolve
    hide violet_parada with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LABEL A: No abrio el paquete — Entrega limpia
################################################################################

label dar_paquete_quest02_violet_a:

    $ _bg_actual = sistema_locaciones.locacion_actual.background
    scene expression _bg_actual with fade

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo base ojos base boca neutral)
    show violet_parada c_rbase_base o_base b_none at right

    pause 0.5
    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Violet aca esta tu paquete"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "Gracias"
    # (Violet boca neutral)
    show violet_parada b_none

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
    show mc_parado_base c_rbase_regaloviolet with sprite_normal
    pause 0.3
    # (Mc boca hablando cuerpo base)
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    # (Violet cuerpo regalo)
    show violet_parada c_rbase_regalo with sprite_normal
    mc "Toma"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando chica ojos abajo)
    show violet_parada b_hablandochica o_abajonm
    violet "¿Lo abriste?"
    # (Violet boca neutral ojos neutral)
    show violet_parada b_none o_none

    # (Mc boca hablando cuerpo asustado)
    show mc_parado_base b_hablando c_rbase_asustado with sprite_fast
    mc "No, solo vi que en la etiqueta decia MundoMangas, asi que supuse que eran tuyos"
    # (Mc boca neutral cuerpo base)
    show mc_parado_base b_none c_rbase_base with sprite_fast

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "Gracias por traermelo"
    # (Violet boca neutral)
    show violet_parada b_none

    # Remover item del inventario
    $ del store.inventario["mangas_violet"]

    $ _ruta_vq01b = "a"

    hide violet_parada with dissolve

    # (Mc cuerpo pensando)
    show mc_parado_base c_rbase_pensando with sprite_fast
    piensa "Fue buena idea no abrirlo parece"

    hide mc_parado_base with dissolve

    jump dar_paquete_violet_cierre


################################################################################
## LABEL B: Abrio el paquete — Violet se da cuenta
################################################################################

label dar_paquete_quest02_violet_b:

    $ _bg_actual = sistema_locaciones.locacion_actual.background
    scene expression _bg_actual with fade

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo base ojos base boca neutral)
    show violet_parada c_rbase_base o_base b_none at right

    pause 0.5
    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Violet aca esta tu paquete"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "Gracias"
    # (Violet boca neutral)
    show violet_parada b_none

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
    show mc_parado_base c_rbase_regaloviolet with sprite_normal
    pause 0.3
    # (Mc boca hablando cuerpo base)
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    # (Violet cuerpo regalo)
    show violet_parada c_rbase_regalo with sprite_normal
    mc "Toma"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "¿Lo abriste?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "No, no lo abrí"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet ojos abajo)
    show violet_parada o_abajonm
    pause 0.5
    # (Violet ojos base boca hablando)
    show violet_parada o_base b_hablando
    violet "La caja esta abierta..."
    # (Violet boca neutral ojos base)
    show violet_parada b_none o_base

    # (Mc boca hablando cuerpo avergonzado)
    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Lo dejaron en mi habitacion y no sabia que era"
    # (Mc boca abierta chica)
    show mc_parado_base b_abiertachica
    mc "Quizás era algo que me había mandado mi papá"
    # (Mc boca neutral)
    show mc_parado_base b_none


    # (Violet boca hablando chica ojos enojados)
    show violet_parada b_hablandochica o_enojados
    violet "No puedo creerlo..."
    # (Violet boca neutral)
    show violet_parada b_none

    menu:
        "Mentir (Decir que no viste lo que había)":
            jump dar_paquete_quest02_violet_b1
        "Provocarla (Hablarle del tipo de mangas que viste)":
            jump dar_paquete_quest02_violet_b2


################################################################################
## LABEL B1: Mentira — No vi nada
################################################################################

label dar_paquete_quest02_violet_b1:

    # (Mc boca hablando cuerpo asustado)
    show mc_parado_base b_hablando c_rbase_asustado with sprite_normal
    mc "Tranquila, solo vi que eran unos mangas, pero nada mas"
    # (Mc boca neutral cuerpo base)
    show mc_parado_base b_none c_rbase_base with sprite_normal

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "Mas te vale..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "¿Por que tanto problema por unos mangas?"
    # (Mc boca abierta chica)
    show mc_parado_base b_abiertachica
    mc "¿Habia algo mas ahi?"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando ojos enojados)
    show violet_parada b_hablando o_enojados
    violet "No es asunto tuyo"
    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "La próxima vez no toques mis cosas."
    # (Violet boca neutral)
    show violet_parada b_none

    # Remover item del inventario
    $ del store.inventario["mangas_violet"]

    $ _ruta_vq01b = "b1"

    hide violet_parada with dissolve

    # (Mc cuerpo pensando)
    show mc_parado_base c_rbase_pensando with sprite_fast
    piensa "Ahora Violet va a estar con la duda de si vi o no sus cosas, seguramente esté a la defensiva"
    piensa "Tengo que ver de aprovechar eso a mi favor de alguna manera"

    hide mc_parado_base with dissolve

    jump dar_paquete_violet_cierre


################################################################################
## LABEL B2: Provocacion — Se burla del contenido
################################################################################

label dar_paquete_quest02_violet_b2:

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Miré que había unos mangas y pensé que podía ser mío"
    # (Mc boca abierta chica cuerpo pensando ojos arriba)
    show mc_parado_base b_abiertachica c_rbase_pensando o_arribanm with sprite_fast
    mc "Luego vi uno que se llamaba algo Yamette Oni-chan y supe que mío no era"
    # (Mc boca neutral cuerpo base ojos base)
    show mc_parado_base b_none c_rbase_base o_base with sprite_fast

    # (Violet boca hablando ojos abiertos)
    show violet_parada b_hablando o_abiertos
    violet "¡¿Que?!"
    # (Violet boca hablando chica ojos enojados)
    show violet_parada b_hablandochica o_enojados
    violet "¡Revisaste mis cosas!"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Era una caja llena de mangas que llamó mi curiosidad"
    # (Mc boca abierta chica)
    show mc_parado_base b_abiertachica
    mc "Voy a decir que tienes gustos... Interesantes..."
    # (Mc boca neutral ojos base)
    show mc_parado_base b_none o_base

    # (Violet boca hablando ojos abiertos sonrojo)
    show violet_parada b_hablando o_abiertos ot_avergonzada
    violet "Eres un idiota..."
    # (Violet boca aburrida)
    show violet_parada b_aburrida


    # (Mc boca hablando cuerpo pensando)
    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "Creo que la línea sería algo como te odio oni-chan "
    # (Mc boca neutral cuerpo base)
    show mc_parado_base b_none c_rbase_base with sprite_fast

    # (Violet ojos enojados cuerpo enojada)
    show violet_parada o_enojados ot_none 
    violet "Creo que la linea es voy a matarte y a enterrarte"
    # (Violet ojos base boca neutral)
    show violet_parada o_base b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "No seria un buen final para la novela..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando cuerpo brazos cruzados)
    show violet_parada b_hablando 
    violet "Me canse, me voy"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando cuerpo cuestionando)
    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_fast
    mc "Espera... No voy a molestarte con esto, pero quiero que hagas algo por mi"
    # (Mc boca neutral cuerpo base)
    show mc_parado_base b_none c_rbase_base

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "¿Que cosa?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Quiero que me digas oni-chan"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet ojos abiertos cuerpo sorprendida)
    show violet_parada o_abiertos c_rbase_sorprendido with sprite_fast
    pause 0.5
    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "¿Por que quieres que te diga eso?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Porque es divertido jajaja"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "¿No me vas a molestar mas verdad?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "No, no te molestaré más"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando sonrojo)
    show violet_parada b_hablando ot_avergonzada
    mc "Oni... "
    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "No puedo decirte eso, me voy"
    # (Violet boca neutral)
    show violet_parada b_none

    # Remover item del inventario
    $ del store.inventario["mangas_violet"]

    $ _ruta_vq01b = "b2"

    hide violet_parada with dissolve

    # (Mc ojos felices cerrados)
    show mc_parado_base o_felicescerrados
    piensa "Jajaja eso fue divertido"
    # (Mc cuerpo pensando ojos arriba)
    show mc_parado_base c_rbase_pensando o_arribanm with sprite_fast
    piensa "Voy entendiendo más a Violet, si la presiono se vuelve más fácil de tratar"

    hide mc_parado_base with dissolve

    jump dar_paquete_violet_cierre


################################################################################
## LABEL CIERRE: Evalua ruta y completa quest (punto de convergencia)
################################################################################

label dar_paquete_violet_cierre:

    if _ruta_vq01b == "a":
        $ obtener_npc("violet").modificar_stat1(5)
    elif _ruta_vq01b == "b1":
        $ obtener_npc("violet").modificar_stat1(3)
        $ obtener_npc("violet").modificar_stat2(1)
    elif _ruta_vq01b == "b2":
        $ obtener_npc("violet").modificar_stat2(2)

    # Completar quest
    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
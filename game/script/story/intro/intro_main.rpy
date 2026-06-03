

# =========================================================
# INICIO + INTRO + GAME LOOP + AFTER LOAD (REN'PY 8.4 FIX)
# =========================================================

# Variable para controlar si ya se mostró la intro
default intro_mostrada = False


# ---------------------------------------------------------
# AFTER LOAD (Ren'Py 8.4): usar config.after_load_callbacks
# ---------------------------------------------------------
init python:

    def _jp_after_load_callback():
        """
        Se ejecuta automáticamente luego de cargar una partida.
        Acá reconstruimos lo que haga falta (si algo no es serializable),
        recalculamos rutinas y re-mostramos HUD.
        """

        # Si tu sistema_locaciones es un objeto python no serializable,
        # al cargar puede quedar None. Reconstrucción segura:
        try:
            if store.sistema_locaciones is None:
                store.inicializar_locaciones_casa()
        except Exception:
            # Si la variable no existe o falla, no cortamos el load
            pass

        # NO inicializar NPCs aquí - los objetos NPC se guardan con el save
        # Solo recalcular rutinas según el tiempo guardado
        try:
            store.actualizar_rutinas_npcs()
        except Exception:
            pass
        
        # Sincronizar variables default con objetos NPC
        try:
            store.sincronizar_relaciones_npcs()
        except Exception:
            pass
        
        # Cargar estados de eventos
        try:
            if hasattr(store, 'cargar_eventos'):
                store.cargar_eventos()
        except Exception:
            pass

        # Asegurar HUD visible
        try:
            renpy.show_screen("navegacion_locaciones_con_hud")
        except Exception:
            pass
        
        # Inicializar sistema de mensajes si no existe (saves antiguos)
        try:
            if not hasattr(store, 'sistema_mensajes') or store.sistema_mensajes is None:
                store.sistema_mensajes = SistemaMensajes()
                store.inicializar_chats()
        except Exception:
            pass


    # Registrar callback (evitar duplicados)
    if not hasattr(config, "after_load_callbacks"):
        config.after_load_callbacks = [ ]

    if _jp_after_load_callback not in config.after_load_callbacks:
        config.after_load_callbacks.append(_jp_after_load_callback)



# ---------------------------------------------------------
# START
# ---------------------------------------------------------
screen advertencia_adultos():
    modal True

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        background None
        xmaximum 900
        padding (60, 50)

        vbox:
            spacing 30
            xalign 0.5

            text _("⚠ ADVERTENCIA: CONTENIDO PARA ADULTOS"):
                size 28
                color "#FF4444"
                bold True
                xalign 0.5

            null height 10

            text _("Este juego contiene material explícito no apto para menores de 18 años. Todos los personajes, nombres y eventos retratados en esta obra son completamente ficticios. Cualquier parecido con personas reales, vivas o muertas, es pura coincidencia.\n\nTodos los personajes involucrados en escenas de contenido sexual tienen 18 años o más al momento de los hechos representados."):
                size 18
                color "#cccccc"
                xalign 0.5
                text_align 0.5
                line_spacing 6

            null height 10

            text _("¿Tenés 18 años o más?"):
                size 22
                color "#ffffff"
                bold True
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 40

                textbutton _("Sí, tengo 18 años o más"):
                    action Return(True)
                    text_size 18
                    text_color "#ffffff"
                    background "#2E7D32"
                    hover_background "#43A047"
                    padding (30, 14)

                textbutton "No":
                    action Function(renpy.quit)
                    text_size 18
                    text_color "#ffffff"
                    background "#B71C1C"
                    hover_background "#E53935"
                    padding (30, 14)


screen menu_intro_choice():
    modal True

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        background None
        xmaximum 900
        padding (60, 50)

        vbox:
            spacing 30
            xalign 0.5

            text _("INTRODUCCIÓN"):
                size 28
                color "#4FC3F7"
                bold True
                xalign 0.5

            null height 10

            text _("La introducción del juego presenta la situación actual del jugador y a los personajes involucrados."):
                size 18
                color "#cccccc"
                xalign 0.5
                text_align 0.5
                line_spacing 6

            null height 20

            hbox:
                xalign 0.5
                spacing 40

                textbutton _("Ver introducción"):
                    action Return(True)
                    text_size 18
                    text_color "#ffffff"
                    background "#2E7D32"
                    hover_background "#43A047"
                    padding (30, 14)

                textbutton _("Omitir"):
                    action Return(False)
                    text_size 18
                    text_color "#ffffff"
                    background "#1565C0"
                    hover_background "#1976D2"
                    padding (30, 14)


screen menu_tutorial_choice():
    modal True

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        background None
        xmaximum 900
        padding (60, 50)

        vbox:
            spacing 30
            xalign 0.5

            text _("TUTORIAL"):
                size 28
                color "#4FC3F7"
                bold True
                xalign 0.5

            null height 10

            text _("Este tutorial está pensado para abarcar los conceptos más importantes del juego.\nTe recomendamos que si no estás familiarizado con este tipo de juegos, lo veas."):
                size 18
                color "#cccccc"
                xalign 0.5
                text_align 0.5
                line_spacing 6

            null height 20

            hbox:
                xalign 0.5
                spacing 40

                textbutton _("Sí"):
                    action Return(True)
                    text_size 18
                    text_color "#ffffff"
                    background "#2E7D32"
                    hover_background "#43A047"
                    padding (30, 14)

                textbutton _("No"):
                    action Return(False)
                    text_size 18
                    text_color "#ffffff"
                    background "#1565C0"
                    hover_background "#1976D2"
                    padding (30, 14)


label start:

    # Mostrar advertencia de contenido adulto en cada nueva partida
    if not intro_mostrada:
        $ renpy.call_screen("advertencia_adultos")

    # Inicializar SOLO en nuevo juego (si no está ya inicializado)
    if not intro_mostrada:
        # Elección de intro
        $ _jugar_intro = renpy.call_screen("menu_intro_choice")

        # Pedir nombre al jugador
        call choose_name from _call_choose_name

        # Si canceló sin escribir nada, usar nombre por defecto
        if not mc_name or mc_name.strip() == "":
            $ mc_name = "MC"

        $ intro_mostrada = True
        $ inicializar_locaciones_casa()
        $ inicializar_npcs_casa()
        $ inicializar_todas_las_quests()
        $ inicializar_stock()
        $ inicializar_skins_jasmine()
        $ inicializar_chats()

        # Configurar tiempo inicial
        $ dia_semana_actual = 0
        $ horario_actual = 0
        $ dia_actual = 1
        $ estacion_actual = 0
        $ año_actual = 1
        $ actualizar_rutinas_npcs()

        if _jugar_intro:
            $ sistema_locaciones.mover_a_locacion("casa_frente")
            jump intro_principal
        else:
            jump menu_tutorial

    jump intro_principal



# ---------------------------------------------------------
# INTRO
# ---------------------------------------------------------
label intro_principal:

    scene bg_intro_edificio
    show mc_parado_base ddimensiones ca_cabeza o_abajonm b_aburrida xnone c_rbase_celular at center

    piensa "Otra vez debo mudarme... Esta es la quinta vez..."
    piensa "Cada vez que mi padre se enamora, toda mi vida cambia por completo."
    piensa "Pero esta vez es diferente, ya soy mayor y puedo tomar mis propias decisiones."
    piensa "Toca que cada uno haga su propio camino."
    show mc_parado_base o_arribanm
    piensa "Aunque todavía estoy molesto con él, quiero verlo antes de que se vaya."
    show mc_parado_base o_base
    piensa "Es hora de apurarme"
    

    # Viaje al aeropuerto
    scene black with fade
    show text Text(renpy.translate_string("30 minutos más tarde"), size=50, color="#FFFFFF",
        outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause 2.0
    hide text with dissolve

    jump intro_conversacion_padre

    return



# ---------------------------------------------------------
# LOOP PRINCIPAL DEL JUEGO (SIN LABELS ANIDADOS)
# ---------------------------------------------------------
label game_loop:

    window hide

    # Asegurar que el HUD esté visible al devolver control al jugador
    $ mostrar_hud()

    # Validar eventos en cada iteración del loop
    $ validar_eventos()

    # Quest 09_a: disparar piensa "Debería avisarle a Violet" al llegar a ETAPA_BOTON_LISTO
    $ _quest_v09a_gl = store.sistema_quests.obtener_quest("violet_questprincipal_09_a")
    if (_quest_v09a_gl and _quest_v09a_gl.activa and not _quest_v09a_gl.completada and
            _quest_v09a_gl.etapa_actual == ETAPA_BOTON_LISTO and
            not getattr(store, 'violet_9a_piensa_mostrado', True)):
        jump violet_quest09a_piensa_avisarle

    if not renpy.get_screen("navegacion_locaciones_con_hud"):
        show screen navegacion_locaciones_con_hud

    # Sincronizar background en master layer (cubre el caso de saves cargados)
    $ actualizar_bg_master()

    pause
    jump game_loop


label after_load:
    $ actualizar_bg_master()
    return


# ---------------------------------------------------------
# TEST: Label que crea checkpoint (como dormir)
# ---------------------------------------------------------
label test_checkpoint:
    
    # Return crea un checkpoint guardable
    return

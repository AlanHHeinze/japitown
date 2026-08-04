

# =========================================================
# INICIO + INTRO + GAME LOOP + AFTER LOAD (REN'PY 8.4 FIX)
# =========================================================
# Variable para controlar si ya se mostró la intro
default intro_mostrada = False

# Elección del menú de intro. Va con `default` y no solo con la asignación de
# `$ _jugar_intro = renpy.call_screen(...)` porque si ESA línea crashea y el
# jugador toca "Continuar" en la pantalla de error, la ejecución sigue en el
# statement siguiente y la variable nunca llega a existir — 33 líneas después el
# `if _jugar_intro:` reventaba con NameError (visto en 0.1.8f, tras la muerte del
# renderer en web). Con el default, el peor caso es entrar al juego sin la intro.
default _jugar_intro = False

# DIAGNÓSTICO de "Possible infinite loop" en el game_loop (S11).
# Guarda cuál de los 4 disparadores del loop hizo el último `jump`, y se limpia
# al llegar al `pause` (o sea, cuando la vuelta se completó sin ciclar). Si el
# guard de Ren'Py salta, este valor viaja a Sentry como tag `gl_trigger` y dice
# QUÉ estaba ciclando — con dos reportes no se pudo deducir porque los cuatro
# disparadores limpian su condición correctamente.
default _gl_ultimo_trigger = ""

# Fondos de la intro (definidos aqui desde que se unificó el archivo)
image bg_intro_edificio       = "images/intro/backgrounds/bg_intro_edificio.jpg"
image bg_intro_aeropuerto     = "images/intro/backgrounds/bg_intro_aeropuerto.jpg"
image bg_intro_aeropuerto_zoom = "images/intro/backgrounds/bg_intro_aeropuerto_zoom.jpg"


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

        # NO inicializar NPCs aqui - los objetos NPC se guardan con el save
        # Solo recalcular rutinas según el tiempo guardado
        try:
            store.actualizar_rutinas_npcs()
        except Exception:
            pass

        # Repoblar los diccionarios de sprite/posición por rutina (violet_/
        # monica_/jasmine_rutinas_visuales). Viven en memoria, no en el save,
        # y solo se llenan en inicializar_npcs_casa() (partida nueva) — sin
        # esto, tras cargar o recargar el script quedan vacíos y todos los
        # NPCs caen al sprite genérico de emergencia (ruta vieja, mal ubicado).
        # Repoblar es seguro: solo reescribe estos diccionarios, no toca a
        # los objetos NPC guardados ni los re-registra en sistema_npcs.
        try:
            store.poblar_rutinas_visuales_violet()
            store.poblar_rutinas_visuales_monica()
            store.poblar_rutinas_visuales_jasmine()
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

    $ _aa_k = 2.0 if renpy.variant("small") else 1.0

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        background None
        xmaximum int(900 * _aa_k)
        padding (int(60 * _aa_k), int(50 * _aa_k))

        vbox:
            spacing int(30 * _aa_k)
            xalign 0.5

            text _("⚠ ADVERTENCIA: CONTENIDO PARA ADULTOS"):
                size int(28 * _aa_k)
                color "#FF4444"
                bold True
                xalign 0.5

            null height int(10 * _aa_k)

            text _("Este juego contiene material explícito no apto para menores de 18 años. Todos los personajes, nombres y eventos retratados en esta obra son completamente ficticios. Cualquier parecido con personas reales, vivas o muertas, es pura coincidencia.\n\nTodos los personajes involucrados en escenas de contenido sexual tienen 18 años o más al momento de los hechos representados"):
                size int(18 * _aa_k)
                color "#cccccc"
                xalign 0.5
                text_align 0.5
                line_spacing 6

            null height int(10 * _aa_k)

            text _("¿Tenés 18 años o más?"):
                size int(22 * _aa_k)
                color "#ffffff"
                bold True
                xalign 0.5

            hbox:
                xalign 0.5
                spacing int(40 * _aa_k)

                textbutton _("Sí, tengo 18 años o más"):
                    action Return(True)
                    text_size int(18 * _aa_k)
                    text_color "#ffffff"
                    background "#2E7D32"
                    hover_background "#43A047"
                    padding (int(30 * _aa_k), int(14 * _aa_k))

                textbutton "No":
                    action Function(renpy.quit)
                    text_size int(18 * _aa_k)
                    text_color "#ffffff"
                    background "#B71C1C"
                    hover_background "#E53935"
                    padding (int(30 * _aa_k), int(14 * _aa_k))


screen menu_intro_choice():
    modal True

    $ _mic_k = 2.0 if renpy.variant("small") else 1.0

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        background None
        xmaximum int(900 * _mic_k)
        padding (int(60 * _mic_k), int(50 * _mic_k))

        vbox:
            spacing int(30 * _mic_k)
            xalign 0.5

            text _("INTRODUCCIÓN"):
                size int(28 * _mic_k)
                color "#4FC3F7"
                bold True
                xalign 0.5

            null height int(10 * _mic_k)

            text _("La misma presenta el comienzo de la historia, presentacion de personajes iniciales y incluye el tutorial de las funciones mas basicas.\n\nSi es tu primera vez en Japitonw te recomendamos jugar la introduccion "):
                size int(18 * _mic_k)
                color "#cccccc"
                xalign 0.5
                text_align 0.5
                line_spacing 6

            null height int(20 * _mic_k)

            hbox:
                xalign 0.5
                spacing int(40 * _mic_k)

                textbutton _("Ver introducción"):
                    action Return(True)
                    text_size int(18 * _mic_k)
                    text_color "#ffffff"
                    background "#2E7D32"
                    hover_background "#43A047"
                    padding (int(30 * _mic_k), int(14 * _mic_k))

                textbutton _("Omitir"):
                    action Return(False)
                    text_size int(18 * _mic_k)
                    text_color "#ffffff"
                    background "#1565C0"
                    hover_background "#1976D2"
                    padding (int(30 * _mic_k), int(14 * _mic_k))


screen disclaimer_ficcion():
    modal True

    $ _disc_k = 1.8 if renpy.variant("small") else 1.0

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        background None
        xmaximum int(950 * _disc_k)
        padding (int(70 * _disc_k), int(60 * _disc_k))

        vbox:
            spacing int(25 * _disc_k)
            xalign 0.5

            if _preferences.language == "spanish":
                text "AVISO LEGAL":
                    size int(26 * _disc_k)
                    color "#FFB74D"
                    bold True
                    xalign 0.5

                null height int(15 * _disc_k)

                text "Este juego es una obra de ficción. Todos los personajes, situaciones, eventos y diálogos presentados son completamente imaginarios y creados con fines de entretenimiento. Cualquier similitud con personas reales, vivas o fallecidas, es pura coincidencia.\n\nTodos los personajes involucrados en cualquier escena de contenido explícito o romántico son mayores de 18 años. Los desarrolladores no respaldan ni promueven ningún contenido que tenga lugar en este juego como aceptable en la realidad.":
                    size int(16 * _disc_k)
                    color "#E0E0E0"
                    xalign 0.5
                    text_align 0.5
                    line_spacing 7

            else:
                text "LEGAL NOTICE":
                    size int(26 * _disc_k)
                    color "#FFB74D"
                    bold True
                    xalign 0.5

                null height int(15 * _disc_k)

                text "This game is a work of fiction. All characters, situations, events, and dialogues presented are completely imaginary and created for entertainment purposes. Any resemblance to real persons, living or deceased, is purely coincidental.\n\nAll characters involved in any scene of explicit or romantic content are 18 years of age or older. The developers do not endorse or promote any content that takes place in this game as acceptable in reality.":
                    size int(16 * _disc_k)
                    color "#E0E0E0"
                    xalign 0.5
                    text_align 0.5
                    line_spacing 7

            null height int(20 * _disc_k)

            hbox:
                xalign 0.5

                textbutton _("Continuar"):
                    action Return(True)
                    text_size int(18 * _disc_k)
                    text_color "#ffffff"
                    background "#1565C0"
                    hover_background "#1976D2"
                    padding (int(50 * _disc_k), int(16 * _disc_k))


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

        # Mostrar disclaimer de ficción y mayoría de edad
        $ renpy.call_screen("disclaimer_ficcion")

        $ intro_mostrada = True
        $ inicializar_locaciones_casa()
        $ inicializar_npcs_casa()
        $ inicializar_todas_las_quests()
        $ sistema_quests_mc.iniciar("mc_quest_0")
        # El MC trae un perfume de regalo para Monica (dispara su quest 0)
        $ inventario["perfume"] = inventario.get("perfume", 0) + 1
        # Regalos de bienvenida para Violet y Jasmine (se consumen en su quest 0)
        $ inventario["regalo_violet"] = inventario.get("regalo_violet", 0) + 1
        $ inventario["regalo_jasmine"] = inventario.get("regalo_jasmine", 0) + 1
        # Golosinas para la quest 0_a de Violet
        $ inventario["golosinas"] = inventario.get("golosinas", 0) + 1
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
            jump mc_q0_inicio_directo

    jump intro_principal



# ---------------------------------------------------------
# INTRO
# ---------------------------------------------------------
label intro_principal:

    scene bg_intro_edificio
    show mc_parado_base ddimensiones ca_cabeza o_abajonm b_aburrida xnone c_rbase_celular at center

    piensa "Otra vez debo mudarme... Esta es la quinta vez..."
    piensa "Cada vez que mi padre se enamora, toda mi vida cambia por completo"
    piensa "Pero esta vez es diferente, ya soy mayor y puedo tomar mis propias decisiones"
    piensa "Toca que cada uno haga su propio camino"
    show mc_parado_base o_arribanm
    piensa "Aunque todavía estoy molesto con él, quiero verlo antes de que se vaya"
    show mc_parado_base o_base
    piensa "Es hora de apurarme"
    

    # Viaje al aeropuerto
    scene black with fade
    show text Text(renpy.translate_string("30 minutos más tarde"), size=50, color="#FFFFFF",
        outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause 2.0
    hide text with dissolve

    jump intro_conversacion_padre


label intro_conversacion_padre:

    scene bg_intro_aeropuerto_zoom
    show mc_parado_base ddimensiones ca_cabeza o_base b_aburrida xnone c_rbase_base at mc_izquierda

    show padre_intro ddimensiones cbase omirando bnone pbase at right
    pause 0.5
    show padre_intro bhablando
    padre "Pensé que no ibas a venir"
    show padre_intro bnone
    
    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Una parte de mí no quería venir, pero aquí estoy"
    show mc_parado_base b_seria
    
    show padre_intro bhablando
    padre "Jajaja vamos, no seas así, vas a extrañar a tu padre"
    show padre_intro bnone
    
    show mc_parado_base o_serios b_hablando
    mc "Sí sí, te voy a extrañar un montón"
    show mc_parado_base b_seria
    
    show padre_intro bhablando 
    padre "Jajaja lo sabía"
    show padre_intro bnone
    
    show mc_parado_base b_hablando
    mc "Te conformas con poco..."
    show mc_parado_base b_seria
    
    show padre_intro bhablando 
    padre "Así somos los padres, jajaja"
    show padre_intro bnone
    
    terminal_micros "Los pasajeros del vuelo 91218 con destino a Argentonia por favor acercarse a la puerta número 4"
    
    show padre_intro bhablando pbrazoscruzados
    padre "Bueno, ese es mi vuelo. ¿Estás seguro que no quieres venir?"
    show padre_intro bnone
    
    show mc_parado_base b_hablando
    mc "Te seguí siempre... pero ir a Argentonia, es una locura"
    show mc_parado_base b_seria
    
    show padre_intro bhablando
    padre "Es un país lleno de gente alegre y mujeres hermosas"
    show padre_intro bnone

    piensa "Se nota que este hombre jamás vio una noticia internacional..."
    
    show mc_parado_base b_hablando
    mc "Gracias, pero realmente prefiero ir a Japitown que a Argentonia"
    show mc_parado_base b_seria

    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Igual deseo que Eva y tú sean muy felices allí"
    show mc_parado_base o_base b_none
    
    show padre_intro bhablando pbase
    padre "Bueno, ya terminé de arreglar todo con Mónica para que te reciba en su casa, no vayas a causarles muchos problemas"
    show padre_intro bnone
    
    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Causar problemas es lo tuyo, no lo mío"
    show mc_parado_base b_seria
    
    vozoff "Brrrr Brrrr"
    
    show mc_parado_base o_abajonm c_rbase_celular with sprite_normal
    piensa "El micro sale en 20 minutos"
    show mc_parado_base o_base b_hablando 
    mc "Bueno, yo también debería irme o voy a perder mi viaje"
    show mc_parado_base b_seria
    
    show padre_intro bhablando 
    padre "Espero verte en Argentonia en el verano"
    show padre_intro bnone
    
    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Supongo que podría ir en plan turístico..."
    show mc_parado_base c_rbase_base with sprite_normal
    mc "Avísame cuando llegues y mándale saludos a Eva de mi parte"
    show mc_parado_base b_none
    
    show padre_intro bhablando 
    padre "Tú también avísame cuando llegues a Japitown"
    show padre_intro bnone

    show mc_parado_base b_hablando
    mc "Nos vemos, papá"  
    show mc_parado_base b_seria

    show mc_parado_base at mc_salir_izquierda
    pause 1.0

    show padre_intro bhablando 
    padre "Adiós..."
    show padre_intro bnone
    
    pause 1.0

    hide padre_intro with dissolve
    hide mc_parado_base with dissolve

    jump intro_llegada_casa


################################################################################
## LLEGADA A LA CASA
################################################################################

label intro_llegada_casa:

    scene black with fade

    show text Text(renpy.translate_string("Más tarde..."), size=50, color="#FFFFFF",
        outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause 2.0
    hide text with dissolve

    # Frente de la casa — horario mañana (inicio del juego)
    scene expression "images/bg/casa/bg_casa_manana_frente.jpg" with fade

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base c_rbase_brazoscruzados with sprite_fast
    piensa "Qué nostalgia estar aquí de nuevo, pasaron muchos años..."
    piensa "Aquí viví una parte importante de mi infancia. Mi papá conoció a Mónica en uno de sus viajes de trabajo"
    piensa "Y a los pocos meses nos estábamos mudando de la capital a esta casa"
    show mc_parado_base c_rbase_pensando o_arribanm with sprite_fast
    piensa "En ese momento Japitown era solo una pequeña ciudad, pasar de la metrópoli a aquí fue horrible"
    piensa "Pero me adapté rápido. Mónica me ayudó mucho y sus hijas fueron de gran compañía"
    show mc_parado_base o_base c_rbase_brazoscruzados with sprite_fast
    piensa "Cada vez que lo pienso, fueron los mejores años de mi vida"
    piensa "Momento de dar el paso y entrar"

    scene expression "images/bg/casa/bg_casa_manana_living.jpg" with fade

    # Posicionar a las tres a la derecha, ligeramente montadas
    # Orden de show = orden de profundidad (ultimo = al frente)
    show violet_parada c_rbase_base o_base b_none:
        xpos 0.58
        xanchor 0.5
        yanchor 1.0
        ypos 1.0
    show jasmine_parada c_rbase_base o_base b_none:
        xpos 0.70
        xanchor 0.5
        yanchor 1.0
        ypos 1.0
    show monica_parada c_rbase_base o_base b_none:
        xpos 0.82
        xanchor 0.5
        yanchor 1.0
        ypos 1.0

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve  

    # Monica da la bienvenida
    show monica_parada b_hablando
    monica "Bienvenido [mc_name], ¿Cómo estuvo el viaje?"
    show monica_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Bien pero agotador, fueron muchas horas arriba del micro"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show monica_parada b_hablando
    monica "Me alegra mucho que estés de nuevo en casa"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "Yo también me siento muy feliz de estar de vuelta"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Bueno, tu habitación está casi lista, solo falta lo que enviaste en las cajas, esta todo en el [colorear_locacion('Garage')]"
    show monica_parada b_hablandochica
    monica "No queríamos tocar tus cosas"
    show monica_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "No te preocupes por eso, hicieron mucho por mí. No sé dónde estaría en este momento si no me hubieras dado un lugar aquí"
    show mc_parado_base b_none c_rbase_base with sprite_fast
    
    show monica_parada b_hablando c_rbase_brazoscruzados with sprite_fast
    monica "No tienes que agradecerme por nada, esta fue y será siempre tu casa"
    show monica_parada b_none
    
    show mc_parado_base b_hablando
    mc "De verdad me alegra mucho volver a verlas a todas. Estuve todo el viaje preocupado por este momento"
    show mc_parado_base b_abiertachica
    mc "Pero sigue siendo como lo fue siempre"
    show mc_parado_base b_none

    show jasmine_parada b_hablando
    jasmine "¿Cómo pensaste que iba a ser?"
    show jasmine_parada b_sorprendida
    jasmine "Esta fue y será siempre tu casa"
    show jasmine_parada b_none

    show mc_parado_base b_hablando
    mc "De nuevo, muchas gracias por recibirme después de tanto tiempo"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bueno, esto fue mucho del reencuentro feliz para mí..."
    show violet_parada b_none

    show violet_parada at personaje_salir_izquierda
    pause 1.0
    hide violet_parada with dissolve

    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "¿Qué le pasa a [colorear_npc('violet', 'Violet')]?"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show jasmine_parada b_hablando c_rbase_dedolabio with sprite_fast
    jasmine "Ella es así, le toma más tiempo procesar los cambios"
    show jasmine_parada b_sorprendida c_rbase_base with sprite_fast
    jasmine "No te preocupes"
    show jasmine_parada b_none

    # Monica propone entrar
    show monica_parada b_hablando
    monica "Voy a hablar con ella luego."
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "No te preocupes Mónica, después yo hablo con ella"
    show mc_parado_base b_none

    show monica_parada b_hablandochica
    monica "A la noche vamos a salir a cenar a algún restaurante"
    show monica_parada b_hablando
    monica "Pero ahora encargate tranquilo de tus cosas, Jasmine dejemmos que [mc_name] se acomode. Cualquier cosa me avisas"
    show monica_parada b_none

    hide monica_parada with dissolve

    show jasmine_parada b_sorprendida
    jasmine "Voy a estar en mi habitación por si me necesitas"
    show jasmine_parada b_none

    hide jasmine_parada with dissolve

    jump quest_mc_quest_0


# ---------------------------------------------------------
# LOOP PRINCIPAL DEL JUEGO (SIN LABELS ANIDADOS)
# ---------------------------------------------------------
label game_loop:

    # Red de seguridad anti-leak de frames: si llegamos aca con frames vivos en
    # el call stack, son basura por definicion (nada "retorna a traves" del
    # game_loop — es el loop raiz). Un label de contenido que termina en
    # jump game_loop desde un contexto con frame (accion, puerta, listener)
    # los dejaria acumulados, y en sesiones largas eso crashea. Drenarlos aca
    # hace validos AMBOS finales: return (subrutina del motor) y
    # jump game_loop (terminal de escena/quest/evento).
    python:
        while renpy.call_stack_depth() > 0:
            renpy.pop_call()

    window hide

    # Etiqueta de los slots de guardado ("Día N"). Se refresca acá ademas de en
    # dormir() para que un guardado manual del dia 1 (todavia sin dormir nunca)
    # tambien salga etiquetado.
    $ save_name = jp_nombre_guardado()

    # Asegurar que el HUD esté visible al devolver control al jugador
    $ mostrar_hud()

    # Revalidar las quests en cada vuelta del loop (o sea, tras CADA acción del
    # jugador). Antes esto solo pasaba al avanzar horario/dormir, así que una
    # quest cuyo requisito se cumplía en el momento (ej. recibir un item) se
    # quedaba trabada en ETAPA_CONDICIONES hasta que el jugador durmiera.
    # Es barato y seguro: solo procesa el avance de etapas (ninguna quest define
    # config_fallo, así que verificar_fallo() retorna de inmediato).
    $ actualizar_quests()

    # Revisar la entrega de los mensajes en espera. Antes esto solo se hacía al
    # moverse, al avanzar horario y al dormir: si las condiciones de entrega se
    # cumplían en cualquier otro momento (o si actualizar_quests acababa de
    # disparar el trigger de un mensaje), el grupo quedaba en espera sin que
    # nadie lo revisara hasta el próximo movimiento o cambio de horario.
    $ sistema_mensajes.verificar_mensajes_en_espera()

    # Validar eventos en cada iteración del loop
    $ validar_eventos()

    # Triggers de contenido del loop (registro TRIGGERS_GAME_LOOP, refactor C6):
    # cada quest registra su trigger desde SU archivo con
    # registrar_trigger_game_loop(id, funcion, prioridad). El primero que
    # devuelve label gana y se salta con jump frameless (por eso viven aca y no
    # en labels de entrada que llegan por call expression y deben retornar).
    # ejecutar_triggers_game_loop deja el id en _gl_ultimo_trigger (tag de
    # Sentry, diagnostico S11) y lo limpia si ninguno disparo.
    $ _gl_trigger_label = ejecutar_triggers_game_loop()
    if _gl_trigger_label:
        jump expression _gl_trigger_label

    if not renpy.get_screen("navegacion_locaciones_con_hud"):
        show screen navegacion_locaciones_con_hud

    # Sincronizar background en master layer (cubre el caso de saves cargados)
    $ actualizar_bg_master()

    pause
    jump game_loop


label after_load:
    $ actualizar_bg_master()
    return




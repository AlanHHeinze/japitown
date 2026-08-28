################################################################################
## HUD de Navegación
################################################################################
## Interfaz visual para el sistema de navegación con informacion de tiempo


# Variable para controlar visibilidad del modo debug/desarrollo
default mostrar_debug_hud = False

# Variable para controlar si el contenido del HUD se renderiza.
# El screen siempre esta activo (para que las teclas funcionen),
# pero el contenido visual se oculta/muestra con esta variable.
default hud_contenido_visible = True

# Delay para ocultar sprites de NPCs durante la transicion de bg al cambiar horario
default hud_npc_delay_horario = False

# Labels especiales para el panel de debug (eventos y labels no registrados en sistema_events)
define _debug_labels_especiales = [
    {"nombre": "Violet: Evento 1 (primera vez)", "label": "evento1_violet"},
    {"nombre": "Violet: Evento 1 (repetir)", "label": "evento1_violet_repetir"},
    {"nombre": "Violet: Evento 2 (primera vez)", "label": "evento2_violet"},
    {"nombre": "Violet: Evento 2 (repetir)", "label": "evento2_violet_repetir"},
    {"nombre": "Violet: Invitar VR", "label": "invitar_violet_vr"},
    {"nombre": "Casco VR: Usar", "label": "usar_casco_vr"},
    {"nombre": "Casco VR: Repetir", "label": "usar_casco_vr_repetir"},
]

# Variable para el botón de test simple
default test_contador = 0

# Variable de compatibilidad: siempre False (las pantallas de quest la usan como guardia)
default modo_posicionamiento = False

# Hotspot con flecha actualmente en hover (para mostrar flecha al pasar el mouse)
default _hs_hover_id = None

################################################################################
## Imágenes de movimiento por hotspot
################################################################################

# Hotspots con imagen propia (visible en hover, invisible en idle)
define _IDLE_MOV_IMGS = {
    "casa_frente_casa_living":             "images/bg/casa/idle_movimiento/idle_frente_living.png",
    "casa_frente_casa_garage":             "images/bg/casa/idle_movimiento/idle_frente_garage.png",
    "casa_frente_casa_patio":              "images/bg/casa/idle_movimiento/idle_frente_patio.png",
    "casa_living_casa_garage":             "images/bg/casa/idle_movimiento/idle_living_garage.png",
    "casa_living_casa_patio":              "images/bg/casa/idle_movimiento/idle_living_patio.png",
    "casa_living_casa_pasilloarriba":      "images/bg/casa/idle_movimiento/idle_living_pasilloarriba.png",
    "casa_cocina_casa_comedor":            "images/bg/casa/idle_movimiento/idle_cocina_comedor.png",
    "casa_comedor_casa_patio":             "images/bg/casa/idle_movimiento/idle_comedor_patio.png",
    "casa_patio_casa_gym":                 "images/bg/casa/idle_movimiento/idle_patio_gym.png",
    "casa_pasilloabajo_casa_banioabajo":   "images/bg/casa/idle_movimiento/idle_pasilloabajo_banioabajo.png",
    "casa_pasilloabajo_casa_hmonica":      "images/bg/casa/idle_movimiento/idle_pasilloabajo_hmonica.png",
    "casa_pasilloabajo_casa_cocina":       "images/bg/casa/idle_movimiento/idle_pasilloabajo_cocina.png",
    "casa_pasilloarriba_casa_living":      "images/bg/casa/idle_movimiento/idle_pasilloarriba_living.png",
    "casa_pasilloarriba_casa_hmc":         "images/bg/casa/idle_movimiento/idle_pasilloarriba_hmc.png",
    "casa_pasilloarriba_casa_banioarriba": "images/bg/casa/idle_movimiento/idle_pasilloarriba_banioarriba.png",
    "casa_pasilloarriba_casa_hviolet":     "images/bg/casa/idle_movimiento/idle_pasilloarriba_violet.png",
    "casa_pasilloarriba_casa_hjasmine":    "images/bg/casa/idle_movimiento/idle_pasilloarriba_hjasmine.png",
    "casa_gym_casa_patio":                 "images/bg/casa/idle_movimiento/idle_gym_patio.png",
    "casa_sotano_casa_garage":             "images/bg/casa/idle_movimiento/idle_sotano_garage.png",
    "casa_altillo_casa_pasilloarriba":     "images/bg/casa/idle_movimiento/idle_altillo_pasilloarriba.png",
    "casa_garage_casa_frente":             "images/bg/casa/idle_movimiento/idle_garage_frente.png",
    "casa_hmonica_casa_baniomonica":       "images/bg/casa/idle_movimiento/idle_hmonica_baniomonica.png",
}

# Hotspots sin imagen propia → flecha centrada en el área al hacer hover
define _IDLE_MOV_FLECHAS = {
    "casa_living_casa_pasilloabajo":       "images/bg/casa/idle_movimiento/idle_flecha_izquierda.png",
    "casa_living_casa_frente":             "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_cocina_casa_pasilloabajo":       "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_comedor_casa_cocina":            "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_patio_casa_frente":              "images/bg/casa/idle_movimiento/idle_flecha_derecha.png",
    "casa_patio_casa_living":              "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_patio_casa_comedor":             "images/bg/casa/idle_movimiento/idle_flecha_izquierda.png",
    "casa_pasilloabajo_casa_living":       "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_pasilloarriba_casa_altillo":     "images/bg/casa/idle_movimiento/idle_flecha_arriba.png",
    "casa_garage_casa_sotano":             "images/bg/casa/idle_movimiento/idle_flecha_izquierda.png",
    "casa_garage_casa_living":             "images/bg/casa/idle_movimiento/idle_flecha_derecha.png",
    "casa_hmc_casa_pasilloarriba":         "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_hmonica_casa_pasilloabajo":      "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_hviolet_casa_pasilloarriba":     "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_hjasmine_casa_pasilloarriba":    "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_banioabajo_casa_pasilloabajo":   "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_banioarriba_casa_pasilloarriba": "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
    "casa_baniomonica_casa_hmonica":       "images/bg/casa/idle_movimiento/idle_flecha_abajo.png",
}


init python:
    def ocultar_hud():
        """
        Oculta el contenido visual del HUD sin destruir el screen.

        EL hide_screen NO ES REDUNDANTE. `hud_navegacion` puede estar en pantalla
        por DOS vias:

          1. `use hud_navegacion` dentro de navegacion_locaciones_con_hud, que
             cuelga de `if hud_contenido_visible` — esa la apaga la linea de
             abajo.
          2. `show screen hud_navegacion` SUELTO, que hacen una decena de
             archivos de contenido al cerrar sus escenas (el repartidor, los
             eventos de Monica y Jasmine, varias quests de Violet). Esa copia es
             independiente del flag y sobrevive a todo.

        Sin el hide, bastaba con haber jugado cualquiera de esos contenidos para
        que la barra superior quedara pegada en TODAS las escenas posteriores
        que solo llamaran a ocultar_hud(). Se veia como un bug puntual de una
        quest, pero afectaba a las ~8 que no acompañan el ocultar_hud con un
        `hide screen` a mano.

        No rompe a los que la muestran sueltos: cuando el HUD tiene que volver,
        lo dibuja igual el `use` de navegacion_locaciones_con_hud.
        """
        store.hud_contenido_visible = False
        renpy.hide_screen("hud_navegacion")
        renpy.restart_interaction()

    def mostrar_hud():
        """Muestra el contenido visual del HUD."""
        store.hud_contenido_visible = True
        renpy.restart_interaction()



################################################################################
## Transforms de animación para el HUD
################################################################################

# Cuanto se agranda el HUD superior en pantalla chica (variante `small`).
# Es el unico numero a tocar para ajustar el tamaño del HUD en celular.
define HUD_ESCALA_SMALL = 2.0

# Hexágonos (dia, estación): Escalan sutilmente al hover
transform hud_hex_hover:
    zoom 0.75
    on idle:
        ease 0.3 zoom 0.75
    on hover:
        ease 0.3 zoom 0.80

# Botón de horario (centro): escala sutil al hover
# Los transforms del HUD reciben la escala `k` (1.0 en PC, HUD_ESCALA_SMALL en
# celular) y la multiplican por su zoom base. Se hace asi —y no apilando un
# segundo `at` con zoom— porque estos transforms YA controlan el zoom en sus
# estados idle/hover: dos zooms encadenados se multiplicarian y las animaciones
# de hover quedarian descalibradas.
transform hud_horario_hover(k=1.0):
    zoom (0.75 * k) alpha 1.0
    on idle:
        ease 0.2 zoom (0.75 * k) alpha 1.0
    on hover:
        ease 0.2 zoom (0.80 * k) alpha 1.0
    on insensitive:
        ease 0.2 alpha 0.6 zoom (0.75 * k)

# Botones de accion (cama, mochila, celu, mapa): suben al hover
transform hud_action_hover(k=1.0):
    zoom (0.75 * k) yoffset 0
    on idle:
        ease 0.2 yoffset 0 zoom (0.75 * k)
    on hover:
        ease 0.2 yoffset (-6 * k) zoom (0.78 * k)

# Badge de notificaciones: bounce infinito
transform hud_badge_bounce:
    yoffset 0
    block:
        ease 0.4 yoffset -5
        ease 0.4 yoffset 0
        pause 1.0
        repeat

# Panel de entrenamiento: fade-in con slide
transform hud_panel_fadein:
    alpha 0.0 yoffset -15
    easein 0.4 alpha 1.0 yoffset 0

# Botones de entrenamiento: suben al hover
transform hud_train_hover(k=1.0):
    yoffset 0
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset (-4 * k)


default _hud_horario_hover = False
default _hud_estacion_hover = False

screen hud_navegacion():
    """HUD que se muestra durante la navegación por locaciones"""

    # ⚠️ NUNCA PONER EFECTOS SECUNDARIOS EN EL CUERPO DE UNA SCREEN.
    #
    # Acá vivía un `$ renpy.hide_screen("say")` para sacar el cuadro de diálogo
    # al navegar. Se quitó el 2026-08-20: rompía el textbox en todo flujo de
    # diálogo que corriera con el HUD escondido (mensajes al despertar, tutorial
    # de la app de pistas, mensajes de bloqueo).
    #
    # Ren'Py PREDICE las screens que podrían mostrarse pronto para precargarles
    # las imágenes, y predecir una screen significa EJECUTAR SU CUERPO — esté o
    # no en pantalla. La predicción corre en `idle_frame`, o sea cuando la
    # interacción queda ociosa: justo después de que el texto termina de
    # tipearse. Resultado: la screen `say` viva se destruía sola a mitad de la
    # línea, y con ella todo lo que cuelga de `screen say` (la botonera del
    # textbox, en ui/hud/textbox_control.rpy). Lo que quedaba en pantalla era un
    # render viejo, y el primer click lo borraba.
    #
    # Solo pasaba con el HUD escondido porque Ren'Py no predice lo que ya está
    # mostrado: con el HUD visible la línea nunca se disparaba.
    #
    # Es redundante ademas: el `game_loop` ya hace `window hide` en su primera
    # instrucción (characters/mc/quests/intro_main.rpy). Si alguna vez queda un
    # cuadro colgado, la solución va en el LABEL que corresponda (`window hide`),
    # nunca acá adentro.
    #
    # Registro completo de la investigación y cómo revertir: fix_textbox_say.md

    # Escala del HUD superior. En celular los iconos de 96 px son casi
    # intocables, asi que se agrandan; en PC/tablet queda 1.0 (sin cambios).
    # NO hay un contenedor unico que escale a todos: cada bloque esta anclado a
    # un borde distinto con offsets en px, asi que la escala se aplica al tamaño
    # Y a los offsets de cada uno (si no, crecerian pero quedarian superpuestos).
    $ _hud_k = HUD_ESCALA_SMALL if renpy.variant("small") else 1.0



    # Teclas T, C, P — movidas a boton_posicionamiento_overlay
    # para que funcionen incluso con el HUD oculto

    # =========================================================================
    # CENTRO SUPERIOR - Icono de horario (click para avanzar)
    # =========================================================================
    $ _horario_imgs = {
        0: "images/hud/horario_manana.png",
        1: "images/hud/horario_tarde.png",
        2: "images/hud/horario_noche.png",
        3: "images/hud/horario_trasnoche.png"
    }
    $ _horario_img = _horario_imgs.get(horario_actual, "images/hud/horario_manana.png")
    $ _horario_img_next = _horario_imgs.get(horario_actual + 1, _horario_img)
    $ _horario_nombres = ["Mañana", "Tarde", "Noche", "Trasnoche"]
    $ _horario_texto_actual = renpy.translate_string(_horario_nombres[horario_actual]) if horario_actual < len(_horario_nombres) else ""
    $ _horario_texto_next = renpy.translate_string(_horario_nombres[horario_actual + 1]) if horario_actual + 1 < len(_horario_nombres) else _horario_texto_actual
    fixed:
        # En pantalla chica el HUD se agranda y centrado en pantalla (xalign 0.5)
        # el horario invade al botón cama (movimiento rápido): cama queda con su
        # borde izquierdo en 1920 - 344*k - 96*k (offset -344 + su propio ancho
        # 96, ambos escalados). En small se centra a mitad de camino entre el
        # borde derecho del ícono "día actual" (izquierda, ancho ~96*k) y ese
        # borde de cama, en vez de en el centro de la pantalla.
        if renpy.variant("small"):
            xpos int(((96 * _hud_k) + (1920 - 440 * _hud_k)) / 2) + int(60 * _hud_k)
            xanchor 0.5
        else:
            xalign 0.5
        yalign 0.0
        yoffset int(5 * _hud_k)
        xsize int(96 * _hud_k)
        ysize int(96 * _hud_k)

        button:
            xysize (int(96 * _hud_k), int(96 * _hud_k))
            xalign 0.5
            yalign 0.5
            action Call("accion_avanzar_tiempo")
            if horario_actual == 3:
                sensitive False
            hovered SetVariable("_hud_horario_hover", True)
            unhovered SetVariable("_hud_horario_hover", False)
            at hud_horario_hover(_hud_k)

            fixed:
                xysize (int(96 * _hud_k), int(96 * _hud_k))
                # Icono idle o siguiente en hover
                if not _hud_horario_hover:
                    add _horario_img xalign 0.5 yalign 0.5
                else:
                    add _horario_img_next xalign 0.5 yalign 0.5

                # Texto del horario centrado sobre el icono. En pantalla chica
                # el texto interior se reduce un 30% respecto al resto del HUD
                # (que ya escala con _hud_k), para que no compita tanto con el
                # ícono.
                $ _horario_texto_k = _hud_k * (0.7 if renpy.variant("small") else 1.0)
                frame:
                    xalign 0.5
                    xoffset int(-5 * _hud_k)
                    yalign 0.5
                    background None
                    padding (0, 0)
                    if not _hud_horario_hover:
                        text _horario_texto_actual size int(26 * _horario_texto_k) color "#ffffff" bold True xalign 0.5 outlines [(2, "#000000", 0, 0)] font "fonts/neotoxic-neotoxic-regular-400.otf"
                    else:
                        text _horario_texto_next size int(26 * _horario_texto_k) color "#ffffff" bold True xalign 0.5 outlines [(2, "#000000", 0, 0)] font "fonts/neotoxic-neotoxic-regular-400.otf"


    # =========================================================================
    # SUPERIOR IZQUIERDO - Dia actual con nombre bilingüe
    # =========================================================================
    $ _dias_es = {0:"Lunes", 1:"Martes", 2:"Miércoles", 3:"Jueves", 4:"Viernes", 5:"Sábado", 6:"Domingo"}
    $ _dias_en = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
    $ _dia_nombre = _dias_en.get(dia_semana_actual, "Monday") if _preferences.language == "english" else _dias_es.get(dia_semana_actual, "Lunes")

    fixed:
        xalign 0.0
        yalign 0.0
        yoffset int(10 * _hud_k)
        fit_first True

        add "images/hud/dia_actual.png" zoom (0.65 * _hud_k) xalign 0.5 yalign 0.5

        frame:
            xalign 0.5
            yalign 0.5
            background None
            padding (0, 0)

            text _dia_nombre:
                xalign 0.5
                font "fonts/neotoxic-neotoxic-regular-400.otf"
                size int(39 * _hud_k)
                color "#0e77fe"
                outlines [(2, "#000000", 0, 0)]
    
    # =========================================================================
    # SUPERIOR DERECHO - Iconos de acceso rapido (independientes)
    # =========================================================================
    # Cada botón en su propio frame para que las animaciones no afecten a los demás
    # Imágenes originales: 128x128px, zoom 0.75 = 96x96px. Spacing: 12px
    # Posiciones desde la derecha: mapa(0), celu(108), mochila(216), cama(324)

    # Cama - Viaje rápido: despliega las sublocaciones de la locación madre actual
    imagebutton:
        idle "images/hud/cama_base.png"
        hover "images/hud/cama_hover.png"
        action ToggleScreen("menu_viaje_rapido")
        xalign 1.0 yalign 0.0
        xoffset int(-344 * _hud_k) yoffset int(10 * _hud_k)
        at hud_action_hover(_hud_k)

    # Mochila - Inventario
    imagebutton:
        idle "images/hud/mochila_base.png"
        hover "images/hud/mochila_hover.png"
        action Show("panel_inventario")
        xalign 1.0 yalign 0.0
        xoffset int(-236 * _hud_k) yoffset int(10 * _hud_k)
        at hud_action_hover(_hud_k)

    # Celular - Menú del celular (con badge de mensajes)
    fixed:
        xalign 1.0 yalign 0.0
        xoffset int(-128 * _hud_k) yoffset int(10 * _hud_k)
        xsize int(96 * _hud_k) ysize int(96 * _hud_k)

        imagebutton:
            if celular_esta_bloqueado():
                action Call("pensar_mensaje", celular_esta_bloqueado())
            else:
                action [SetVariable("menu_celular_abierto", True), Show("menu_celular")]
            idle "images/hud/celu_base.png"
            hover "images/hud/celu_hover.png"
            at hud_action_hover(_hud_k)

        $ _total_msg_sin_leer = sistema_mensajes.obtener_pendientes_total()
        if _total_msg_sin_leer > 0:
            frame:
                xalign 1.0
                yalign 0.0
                xoffset int(-4 * _hud_k)
                yoffset int(6 * _hud_k)
                background "#FF4444"
                xsize int(32 * _hud_k) ysize int(32 * _hud_k)
                padding (0, 0)
                at hud_badge_bounce
                text "[_total_msg_sin_leer]" size int(20 * _hud_k) color "#ffffff" bold True xalign 0.5 yalign 0.5

    # Mapa - Contenido en desarrollo
    imagebutton:
        idle "images/hud/mapa_base.png"
        hover "images/hud/mapa_hover.png"
        action Call("narrar_mensaje", "Contenido en desarrollo")
        xalign 1.0 yalign 0.0
        xoffset int(-20 * _hud_k) yoffset int(10 * _hud_k)
        at hud_action_hover(_hud_k)
    
    # =========================================================================
    # PANEL DEBUG UNIFICADO (inferior izquierdo) - Solo visible cuando debug activo
    # =========================================================================
    if MODO_DEV and mostrar_debug_hud:
        frame:
            xalign 0.0
            yalign 1.0
            xoffset 10
            yoffset -10
            background "#2E7D32DD"
            padding (15, 10)
            
            viewport:
                xysize (320, 400)
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 4
                    xsize 300
                    
                    # --- Ubicación ---
                    text "📍 Ubicación" size 14 color "#888888"
                    
                    if sistema_locaciones.locacion_actual:
                        text "[sistema_locaciones.locacion_actual.nombre]" size 20 color "#ffffff" bold True
                        text "ID: [sistema_locaciones.locacion_actual.id]" size 11 color "#aaaaaa"
                    else:
                        text "Desconocida" size 20 color "#ffffff"
                    
                    # --- Tiempo ---
                    null height 8
                    text "DEBUG Tiempo:" size 13 color "#ffff00"
                    if hasattr(store, 'DIAS_SEMANA') and hasattr(store, 'dia_semana_actual'):
                        text "Día: [DIAS_SEMANA[dia_semana_actual]] ([dia_semana_actual])" size 11 color "#ffffff"
                    else:
                        text "Día: N/A" size 11 color "#ffffff"
                    
                    if hasattr(store, 'HORARIOS') and hasattr(store, 'horario_actual'):
                        text "Horario: [HORARIOS[horario_actual]] ([horario_actual])" size 11 color "#ffffff"
                    else:
                        text "Horario: N/A" size 11 color "#ffffff"
                    
                    text "Día del mes: [dia_actual]" size 11 color "#ffffff"
                    
                    # --- Quest ---
                    null height 8
                    text "DEBUG Quest:" size 13 color "#ffff00"
                    text "Quest actual: [quest_actual]" size 11 color "#ffffff"
                    
                    $ quest_activa = sistema_quests.obtener_quest_activa()
                    if quest_activa:
                        text "Quest activa: [quest_activa.nombre]" size 11 color "#00ff00"
                        text "Quest activa ID: [quest_activa.id]" size 11 color "#00ff00"
                    else:
                        text "Quest activa: Ninguna" size 11 color "#ffffff"
                    
                    $ quests_monica = sistema_quests.obtener_quests_disponibles("monica")
                    text "Quests disponibles Mónica: [len(quests_monica)]" size 11 color "#ffffff"
                    
                    $ pista = obtener_pista_quest()
                    if pista:
                        text "Pista: [pista['npc_nombre']] en [pista['locacion']]" size 11 color "#ffff00"
                    else:
                        text "Pista: No disponible" size 11 color "#ffffff"
                    
                    # --- Relaciones ---
                    null height 8
                    text "DEBUG Relaciones:" size 13 color "#ffff00"
                    text "Mónica: A[monica_amor] D[monica_deseo] P[monica_progreso]" size 11 color "#ffffff"
                    text "Jasmine: A[jasmine_amor] D[jasmine_deseo] P[jasmine_progreso]" size 11 color "#ffffff"
                    text "Violet: A[violet_amor] D[violet_deseo] P[violet_progreso]" size 11 color "#ffffff"
    
    # Herramientas de debug (esquina inferior derecha) - Solo visible cuando debug está activo
    if MODO_DEV and mostrar_debug_hud:
        frame:
            xalign 1.0
            yalign 1.0
            xoffset -10
            yoffset -10
            background "#4FC3F7DD"
            padding (15, 10)
            
            vbox:
                spacing 8
                
                # Botón de TEST SIMPLE
                textbutton "🔢 TEST Simple ([test_contador])":
                    action SetVariable("test_contador", test_contador + 1)
                    style "hud_button"
                    text_color "#00ff00"
                
                null height 5
                
                # Botón para herramienta de posicionamiento (tambien: tecla P)
                textbutton ("📐 Posicionar [[ON]]" if renpy.get_screen("herramienta_pos_simple") else "📐 Posicionar"):
                    action ToggleScreen("herramienta_pos_simple")
                    style "hud_button"
                    text_color ("#00ff00" if renpy.get_screen("herramienta_pos_simple") else "#ffffff")
                
                # Botón para saltar a labels de quests/events
                textbutton "🎯 Saltar a Label":
                    action Show("panel_debug_labels")
                    style "hud_button"
                    text_color "#FFD700"

                # Botón para completar quests
                textbutton "📋 Completar Quest":
                    action Show("menu_completar_quests")
                    style "hud_button"
                    text_color "#FFD700"

################################################################################
## Panel de Debug: Salto a Labels
################################################################################

screen panel_debug_labels():
    """Panel para saltar directamente a labels de quests y eventos."""
    
    modal True
    
    # Fondo semi-transparente
    add Solid("#000000AA")
    
    # Panel central
    frame:
        xalign 0.5
        yalign 0.5
        xysize (500, 600)
        background "#1E1E1EEE"
        padding (20, 20)
        
        vbox:
            spacing 10
            xfill True
            
            # Header
            hbox:
                xfill True
                text "🎯 Saltar a Label" size 24 color "#FFD700" bold True
                textbutton "× Cerrar":
                    action Hide("panel_debug_labels")
                    xalign 1.0
                    text_size 16
                    text_color "#FF5722"
                    background None
            
            null height 10
            
            # Contenido scrollable
            viewport:
                xysize (460, 500)
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 8
                    xsize 440
                    
                    # === SECCIÓN QUESTS ===
                    text "📜 QUESTS" size 18 color "#4CAF50" bold True
                    null height 5
                    
                    # Obtener quests del sistema
                    for quest_id, quest in sistema_quests.quests.items():
                        $ estado_icon = "✅" if quest.completada else ("▶️" if quest.activa else "⬜")
                        $ label_name = quest.label_quest
                        
                        hbox:
                            spacing 5
                            xfill True
                            
                            text estado_icon size 14
                            
                            textbutton "[quest.npc_id.capitalize()]: [quest.nombre]":
                                action [Hide("panel_debug_labels"), Hide("navegacion_locaciones_con_hud"), Hide("hud_navegacion"), Jump(label_name)]
                                text_size 14
                                text_color "#FFFFFF"
                                background "#333333"
                                hover_background "#4CAF50"
                                padding (8, 4)
                                xsize 380
                    
                    null height 15
                    
                    # === SECCIÓN EVENTS ===
                    text "⚡ EVENTS" size 18 color "#2196F3" bold True
                    null height 5
                    
                    # Obtener events del sistema
                    for event_id, event in sistema_events.events.items():
                        if event.label_efecto:
                            $ estado_icon = "✅" if event.estado == ESTADO_EVENT_COMPLETADO else ("▶️" if event.estado == ESTADO_EVENT_ACTIVO else "⬜")
                            $ label_name = event.label_efecto
                            
                            hbox:
                                spacing 5
                                xfill True
                                
                                text estado_icon size 14
                                
                                textbutton "[event.nombre]":
                                    action [Hide("panel_debug_labels"), Hide("navegacion_locaciones_con_hud"), Hide("hud_navegacion"), Jump(label_name)]
                                    text_size 14
                                    text_color "#FFFFFF"
                                    background "#333333"
                                    hover_background "#2196F3"
                                    padding (8, 4)
                                    xsize 380

                    null height 15

                    # === SECCIÓN LABELS ESPECIALES ===
                    text "🔧 LABELS ESPECIALES" size 18 color "#FF9800" bold True
                    null height 5

                    for _label_info in _debug_labels_especiales:
                        $ _sl_nombre = _label_info["nombre"]
                        $ _sl_label = _label_info["label"]

                        hbox:
                            spacing 5
                            xfill True

                            text "🔹" size 14

                            textbutton "[_sl_nombre]":
                                action [Hide("panel_debug_labels"), Hide("navegacion_locaciones_con_hud"), Hide("hud_navegacion"), Jump(_sl_label)]
                                text_size 14
                                text_color "#FFFFFF"
                                background "#333333"
                                hover_background "#FF9800"
                                padding (8, 4)
                                xsize 380


################################################################################
## Screen de animación de dormir
################################################################################

screen animacion_dormir():
    """Animación que se muestra al dormir"""
    
    # Bloquear interacción con elementos de fondo
    modal True
    
    # Timer para cerrar automáticamente la pantalla y retornar
    timer 2.0 action Return()
    
    # Fondo negro con fade
    add Solid("#000000")
    
    # Texto central
    frame:
        xalign 0.5
        yalign 0.5
        background None
        
        vbox:
            spacing 20
            xalign 0.5
            
            text "💤" size 80 xalign 0.5
            text _("Durmiendo...") size 40 color "#ffffff" xalign 0.5
            text "Zzz..." size 30 color "#888888" xalign 0.5

################################################################################
## Estilos para el HUD
################################################################################

style hud_button is button:
    background "#0288D1"  # Azul profundo veraniego
    hover_background "#FFB74D"  # Naranja atardecer al hover
    padding (12, 8)
    
style hud_button_text is button_text:
    size 18
    color "#FFFFFF"
    hover_color "#5D4037"  # Marrón al hover para contraste
    bold True

################################################################################
## Efectos decorativos de locación
################################################################################

# Vapor que asoma por la puerta del baño de arriba cuando hay alguien adentro.
# Es DECORATIVO: se dibuja con `add` y no como imagebutton (a diferencia de los
# idles de _IDLE_MOV_IMGS) justamente para que no sea focusable y no le robe el
# click al hotspot de la puerta, que queda debajo.
image idle_vapor_pasilloarriba = "images/bg/casa/idle_otros/idle_vapor_pasilloarriba.webp"


################################################################################
## Screen de navegación actualizado con HUD
################################################################################

screen navegacion_locaciones_con_hud():
    """Screen de navegación con HUD integrado"""

    # Sin modal — se usa un boton fullscreen dentro del if para capturar clicks
    # Esto permite que cuando el contenido esta oculto, los clicks pasen al say/otros screens

    # Tecla de debug: F1 activa/desactiva el panel de herramientas de desarrollo
    if MODO_DEV:
        key "K_F1" action ToggleVariable("mostrar_debug_hud")

    # Contenido visual del HUD (se oculta con ocultar_hud())
    if hud_contenido_visible and sistema_locaciones.locacion_actual:
        # Boton fullscreen invisible — captura clicks en areas sin interaccion (reemplaza modal)
        button:
            xpos 0
            ypos 0
            xsize 1920
            ysize 1080
            background None
            action NullAction()

        # Vapor del baño de arriba: sale por la puerta mientras haya alguien
        # adentro. Va acá, antes de los hotspots, para quedar por detrás de
        # ellos; igual no puede robarles el click porque `add` no crea un
        # displayable focusable (ver la definición de la imagen más arriba).
        # La imagen tiene el alto de la pantalla: pegada al borde izquierdo
        # (xpos 0) y centrada en vertical (yalign 0.5).
        if sistema_locaciones.locacion_actual.id == "casa_pasilloarriba" and obtener_npc_en_banio("casa_banioarriba"):
            add "idle_vapor_pasilloarriba" xpos 0 yalign 0.5

        # Obtener NPCs presentes (necesario antes de hotspots y sprites)
        $ npcs_aqui = npcs_en_locacion_actual()
        
        # =====================================================================
        # CAPA 1: Hotspots interactivos (se renderizan primero, quedan detras)
        # =====================================================================
        
        # En modo posicionamiento de hotspots, usar draggroup para hotspots arrastrables
        if modo_posicionamiento and modo_posicionamiento_tipo == "hotspots":
            # Filtrar hotspots según el sub-filtro: MOVE, ACTION o TODOS
            if pos_hotspot_tipo_filtro == "TODOS":
                $ hotspots_filtrados = sistema_locaciones.locacion_actual.obtener_hotspots_habilitados()
            else:
                $ hotspots_filtrados = [h for h in sistema_locaciones.locacion_actual.obtener_hotspots_habilitados() if h.tipo == pos_hotspot_tipo_filtro]
            
            draggroup:
                for hotspot in hotspots_filtrados:
                    # Determinar posición y tamaño (usa valores editados si está seleccionado)
                    $ h_x = hotspot_posicion_actual["x"] if hotspot.id == hotspot_seleccionado_id else hotspot.x
                    $ h_y = hotspot_posicion_actual["y"] if hotspot.id == hotspot_seleccionado_id else hotspot.y
                    $ h_w = hotspot_posicion_actual["w"] if hotspot.id == hotspot_seleccionado_id else hotspot.w
                    $ h_h = hotspot_posicion_actual["h"] if hotspot.id == hotspot_seleccionado_id else hotspot.h
                    $ is_selected = hotspot.id == hotspot_seleccionado_id
                    $ hotspot_name = hotspot.nombre if hotspot.nombre else hotspot.id
                    
                    # Hotspot arrastrable con visualización
                    drag:
                        drag_name hotspot.id
                        xpos h_x
                        ypos h_y
                        xysize (h_w, h_h)
                        draggable True
                        droppable False
                        dragged actualizar_posicion_hotspot
                        clicked Function(seleccionar_hotspot, hotspot)
                        
                        # Visualización del hotspot: fondo semi-transparente con texto
                        frame:
                            xysize (h_w, h_h)
                            padding (0, 0)
                            
                            # Fondo según estado: dorado seleccionado, azul MOVE, verde ACTION
                            if is_selected:
                                background "#FFD70088"  # Dorado para seleccionado
                            elif hotspot.tipo == "MOVE":
                                background "#2196F366"  # Azul para MOVE
                            else:
                                background "#4CAF5066"  # Verde para ACTION
                            
                            # Nombre del hotspot centrado
                            text hotspot_name:
                                size 14
                                color "#FFFFFF"
                                outlines [(2, "#000000", 0, 0)]
                                xalign 0.5
                                yalign 0.5
            
            # Panel lateral izquierdo: Lista de hotspots de la locación
            frame:
                xpos 10
                ypos 180
                xysize (180, 200)
                background "#1E1E1ECC"
                padding (8, 8)
                
                vbox:
                    spacing 4
                    xsize 164
                    
                    # Título con filtro activo
                    text "📋 Hotspots ([pos_hotspot_tipo_filtro]):" size 11 color "#FFD700" bold True
                    
                    # Lista scrollable de hotspots (filtrada por tipo)
                    viewport:
                        xysize (164, 150)
                        scrollbars "vertical"
                        mousewheel True
                        
                        vbox:
                            spacing 3
                            xsize 150
                            
                            for hotspot in hotspots_filtrados:
                                $ h_bg = "#FFD70044" if hotspot.id == hotspot_seleccionado_id else "#33333388"
                                $ h_tipo_icon = "🚪" if hotspot.tipo == "MOVE" else "⚡"
                                
                                hbox:
                                    spacing 3
                                    
                                    frame:
                                        background h_bg
                                        padding (4, 2)
                                        xsize 120
                                        
                                        hbox:
                                            spacing 3
                                            text h_tipo_icon size 10
                                            text hotspot.id size 10 color "#FFFFFF"
                                    
                                    # Botón centrar
                                    textbutton "📍":
                                        action Function(centrar_hotspot_en_pantalla, hotspot)
                                        text_size 10
                                        background "#2196F3"
                                        hover_background "#64B5F6"
                                        padding (4, 2)
            
            # Panel selector de locaciones destino (cuando modo_crear_hotspot está activo)
            if modo_crear_hotspot:
                frame:
                    xpos 1700
                    ypos 300
                    xysize (200, 380)
                    background "#1E1E1EEE"
                    padding (8, 8)
                    
                    vbox:
                        spacing 4
                        xsize 184
                        
                        hbox:
                            spacing 5
                            text "✏️ Nombre:" size 11 color "#FFD700" bold True
                            textbutton "×":
                                action SetVariable("modo_crear_hotspot", False)
                                text_size 10
                                background "#F44336"
                                padding (4, 2)
                        
                        # Input para nombre del hotspot
                        input:
                            value VariableInputValue("hotspot_nuevo_nombre")
                            size 12
                            color "#FFFFFF"
                            pixel_width 170
                        
                        null height 5
                        text "🎯 Destino:" size 11 color "#FFD700" bold True
                        
                        # Lista scrollable de locaciones
                        viewport:
                            xysize (184, 260)
                            scrollbars "vertical"
                            mousewheel True
                            
                            vbox:
                                spacing 2
                                xsize 170
                                
                                $ lista_locs = obtener_lista_locaciones()
                                for loc_id in lista_locs:
                                    $ loc_obj = sistema_locaciones.obtener_locacion(loc_id)
                                    $ loc_nombre = loc_obj.nombre if loc_obj else loc_id
                                    $ is_dest = hotspot_nuevo_datos.get("destino", "") == loc_id
                                    $ loc_bg = "#4CAF5088" if is_dest else "#33333388"
                                    
                                    textbutton "[loc_nombre]":
                                        action [Function(actualizar_destino_hotspot, loc_id), SetVariable("modo_crear_hotspot", False)]
                                        text_size 10
                                        background loc_bg
                                        hover_background "#66BB6A"
                                        padding (4, 2)
                                        xsize 170
        else:
            for hotspot in sistema_locaciones.locacion_actual.obtener_hotspots_habilitados():

                $ _hs_img    = _IDLE_MOV_IMGS.get(hotspot.id) if hotspot.tipo == "MOVE" else None
                $ _hs_flecha = _IDLE_MOV_FLECHAS.get(hotspot.id) if hotspot.tipo == "MOVE" else None
                $ _hs_cx     = hotspot.x + hotspot.w // 2
                $ _hs_cy     = hotspot.y + hotspot.h // 2

                if hotspot.tipo == "MOVE" and _hs_img:
                    # Hotspot con imagen propia: invisible en idle, visible en hover
                    imagebutton:
                        idle Transform(_hs_img, alpha=0.0)
                        hover Transform(_hs_img, alpha=0.5)
                        xpos hotspot.x
                        ypos hotspot.y
                        xanchor 0.0
                        yanchor 0.0
                        if modo_posicionamiento:
                            action NullAction()
                        else:
                            action [SetVariable("_hotspot_temp", hotspot), Call("accion_hotspot_move")]
                        if hotspot.nombre:
                            tooltip renpy.translate_string(hotspot.nombre)
                else:
                    # Hotspot sin imagen: área invisible + flecha centrada en hover
                    button:
                        xpos hotspot.x
                        ypos hotspot.y
                        xysize (hotspot.w, hotspot.h)
                        background None
                        hover_background None
                        if modo_posicionamiento:
                            action NullAction()
                        elif hotspot.tipo == "MOVE":
                            action [SetVariable("_hotspot_temp", hotspot), Call("accion_hotspot_move")]
                            hovered SetVariable("_hs_hover_id", hotspot.id)
                            unhovered SetVariable("_hs_hover_id", None)
                        elif hotspot.tipo == "ACTION":
                            action [SetVariable("_hotspot_temp", hotspot), Call("accion_hotspot_action")]
                        if hotspot.nombre:
                            tooltip renpy.translate_string(hotspot.nombre)
                        else:
                            tooltip hotspot.id

                    if _hs_flecha and _hs_hover_id == hotspot.id:
                        if "flecha_abajo" in _hs_flecha and _hs_cy > 900:
                            add _hs_flecha xpos _hs_cx ypos 1070 xanchor 0.5 yanchor 1.0
                        elif hotspot.id == "casa_living_casa_pasilloabajo":
                            add _hs_flecha xpos _hs_cx ypos 1022 xanchor 0.5 yanchor 0.5
                        else:
                            add _hs_flecha xpos _hs_cx ypos _hs_cy xanchor 0.5 yanchor 0.5
        
        # =====================================================================
        # CAPA 2: Sprites de NPCs (se renderizan despues, quedan arriba)
        # =====================================================================

        # Timer que revela los NPCs al terminar la transicion del bg
        if hud_npc_delay_horario:
            timer 1.5 action SetVariable("hud_npc_delay_horario", False)

        if npcs_aqui and not hud_npc_delay_horario:
            # Obtener posiciones para los NPCs
            $ posiciones = obtener_posiciones_npcs(len(npcs_aqui))
            
            # Modo normal: sprites estáticos
            # Filtrar NPCs ocultos por restricción de quest/evento
            $ _npcs_visibles = [n for n in npcs_aqui if not npc_esta_oculto(n.id)]
            for i, npc in enumerate(_npcs_visibles):
                # Determinar sprite y posición (rutina específica o default)
                if npc.id == "monica":
                    # Prioridad 1: Sprite de quest activa
                    $ sprite_actual = obtener_sprite_quest_npc("monica")
                    $ posicion_rutina = obtener_posicion_quest_npc("monica")
                    
                    # Prioridad 2: Sprite de rutina visual
                    if not sprite_actual:
                        $ sprite_actual = obtener_sprite_rutina_monica()
                        $ posicion_rutina = obtener_posicion_rutina_monica()
                    
                    # Fallback al sprite default si no hay rutina visual
                    if not sprite_actual:
                        $ sprite_actual = npc.sprite
                    
                    # Usar posición de rutina o calcular posición default
                    if posicion_rutina:
                        $ pos_x = posicion_rutina[0]
                        $ pos_y = posicion_rutina[1]
                    elif i < len(posiciones):
                        $ pos = posiciones[i]
                        $ pos_x = int(pos[0] * 1920)
                        $ pos_y = 1080
                    else:
                        $ pos_x = 960
                        $ pos_y = 1080
                elif npc.id == "violet":
                    # Prioridad 1: Sprite de quest activa
                    $ sprite_actual = obtener_sprite_quest_npc("violet")
                    $ posicion_rutina = obtener_posicion_quest_npc("violet")
                    
                    # Prioridad 2: Sprite de rutina visual
                    if not sprite_actual:
                        $ sprite_actual = obtener_sprite_rutina_violet()
                        $ posicion_rutina = obtener_posicion_rutina_violet()
                    
                    # Fallback al sprite default si no hay rutina visual
                    if not sprite_actual:
                        $ sprite_actual = npc.sprite
                    
                    # Usar posición de rutina o calcular posición default
                    if posicion_rutina:
                        $ pos_x = posicion_rutina[0]
                        $ pos_y = posicion_rutina[1]
                    elif i < len(posiciones):
                        $ pos = posiciones[i]
                        $ pos_x = int(pos[0] * 1920)
                        $ pos_y = 1080
                    else:
                        $ pos_x = 960
                        $ pos_y = 1080
                elif npc.id == "jasmine":
                    # Prioridad 1: Sprite de quest activa
                    $ sprite_actual = obtener_sprite_quest_npc("jasmine")
                    $ posicion_rutina = obtener_posicion_quest_npc("jasmine")
                    
                    # Prioridad 2: Sprite de rutina visual
                    if not sprite_actual:
                        $ sprite_actual = obtener_sprite_rutina_jasmine()
                        $ posicion_rutina = obtener_posicion_rutina_jasmine()
                    
                    # Fallback al sprite default si no hay rutina visual
                    if not sprite_actual:
                        $ sprite_actual = npc.sprite
                    
                    # Usar posición de rutina o calcular posición default
                    if posicion_rutina:
                        $ pos_x = posicion_rutina[0]
                        $ pos_y = posicion_rutina[1]
                    elif i < len(posiciones):
                        $ pos = posiciones[i]
                        $ pos_x = int(pos[0] * 1920)
                        $ pos_y = 1080
                    else:
                        $ pos_x = 960
                        $ pos_y = 1080
                else:
                    # NPCs sin rutina visual: usar sprite y posición default
                    $ sprite_actual = npc.sprite
                    if i < len(posiciones):
                        $ pos = posiciones[i]
                        $ pos_x = int(pos[0] * 1920)
                        $ pos_y = 1080
                    else:
                        $ pos_x = 960
                        $ pos_y = 1080
                
                if sprite_actual:
                    # Imagebutton: el área clickeable coincide con el tamaño del sprite
                    imagebutton:
                        idle sprite_actual
                        hover sprite_actual
                        xpos pos_x
                        ypos pos_y
                        xanchor 0.5  # Centrar horizontalmente
                        yanchor 1.0  # Alinear desde la parte inferior
                        mouse "hand"
                        # Bloquear interacción mientras la herramienta de posicionamiento esté activa
                        if modo_posicionamiento:
                            action NullAction()
                        elif npc_interactuable(npc.id):
                            action Call("interaccion_" + npc.id)
                        else:
                            # Se pasa el npc_id para que el mensaje distinga
                            # "esta durmiendo" de un bloqueo de quest.
                            action Call("pensar_mensaje", mensaje_npc_bloqueado(npc.id))
        
        # =====================================================================
        # CAPA 2.5: Elementos dinámicos de quest/evento
        # =====================================================================
        if hay_restriccion_activa() and sistema_locaciones.locacion_actual:
            $ _elems_quest = obtener_elementos_escena(sistema_locaciones.locacion_actual.id)
            for _elem in _elems_quest:
                if _elem.get("tipo") == "imagebutton":
                    imagebutton:
                        idle _elem["imagen"]
                        hover _elem["imagen"]
                        xpos _elem["pos"][0]
                        ypos _elem["pos"][1]
                        if _elem.get("anchor"):
                            xanchor _elem["anchor"][0]
                            yanchor _elem["anchor"][1]
                        mouse "hand"
                        # En modo posicionamiento no ejecutar el label (para poder arrastrar)
                        if modo_posicionamiento:
                            action NullAction()
                        else:
                            action Call(_elem["label"])
        
        # =====================================================================
        # CAPA 2.8: Overlay del visualizador de hotspots de movimiento
        # =====================================================================
        use visualizador_hotspot_overlay()

        # =====================================================================
        # CAPA 3: Elementos "Otros" del sistema_pos — modo normal (idles, props)
        # NOTA: el drag de posicionamiento se gestiona en boton_posicionamiento_overlay
        # (zorder 200) para funcionar incluso dentro de screens de quest.
        # =====================================================================

        # Repartidor en frente de la casa (mañana de entrega)
        if repartidor_presente and sistema_locaciones.locacion_actual.id == "casa_frente":
            $ _rep = sistema_pos.obtener("casa_frente_repartidor")
            $ _rep_x = _rep.x if _rep else 1270
            $ _rep_y = _rep.y if _rep else 540
            imagebutton:
                idle "idle_repartidor_puerta"
                hover "idle_repartidor_puerta"
                xpos _rep_x
                ypos _rep_y
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action Jump("interaccion_repartidor")

        # Cajas de mudanza en el garage (quest 0 del MC)
        if getattr(store, 'mc_q0_cajas_en_garage', False):
            if sistema_locaciones.locacion_actual.id == "casa_garage":
                $ _cajas = sistema_pos.obtener("mc_q0_cajas_intro")
                $ _cajas_x = _cajas.x if _cajas else 629
                $ _cajas_y = _cajas.y if _cajas else 422
                add "images/quest/mc/quest0/idle_cajas_intro.webp" xpos _cajas_x ypos _cajas_y xanchor 0.0 yanchor 0.0

        # Paquete en la habitacion del MC (entrega perdida)
        if paquete_en_habitacion and sistema_locaciones.locacion_actual.id == "casa_hmc":
            $ _paq = sistema_pos.obtener("casa_hmc_paquete")
            $ _paq_x = _paq.x if _paq else 1000
            $ _paq_y = _paq.y if _paq else 530
            imagebutton:
                idle "idle_paquete_hmc"
                hover "idle_paquete_hmc"
                xpos _paq_x
                ypos _paq_y
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action Jump("recoger_paquete_habitacion")
        
        # Debug info unificado en el panel inferior izquierdo del HUD
        # (se eliminó el panel superpuesto aqui para evitar conflicto con el panel de fecha)
    
    if hud_contenido_visible:
        # Mostrar panel de entrenamiento — oculto solo hasta completar la quest 0
        # del MC ("De nuevo en casa"). Una vez completada, reaparece (aunque haya
        # otras quests del MC activas, como la del celular o el reencuentro).
        $ _mc_q0_panel = sistema_quests_mc.quests.get("mc_quest_0")
        if _mc_q0_panel and _mc_q0_panel.completada:
            use panel_entrenamiento

        # Panel de acciones de locación (cocinar, ver TV, etc.)
        use acciones_locacion

        # Mostrar el HUD
        use hud_navegacion

################################################################################
## Labels de control actualizados
################################################################################

# Este label ya no se usa - el loop principal está en intro.rpy
# Se mantiene por compatibilidad pero redirige al loop principal
label iniciar_navegacion_con_hud:
    jump game_loop


################################################################################
## Screen overlay permanente — Botón de posicionamiento
## Siempre visible, incluso dentro de screens de quest
################################################################################

init python:
    if "boton_posicionamiento_overlay" not in config.overlay_screens:
        config.overlay_screens.append("boton_posicionamiento_overlay")

screen boton_posicionamiento_overlay():
    zorder 300

    if MODO_DEV:
        # Tecla P: herramienta de posicionamiento
        key "p" action ToggleScreen("herramienta_pos_simple")
        # Tecla O: herramienta de completar quests
        key "o" action ToggleScreen("herramienta_quests")

    # Botón flotante — solo visible cuando el panel de debug está abierto (F1)
    if MODO_DEV and mostrar_debug_hud:
        frame:
            xalign 1.0
            yalign 1.0
            xoffset -20
            yoffset -20
            background None

            textbutton ("📐 Posicionar [ON]" if renpy.get_screen("herramienta_pos_simple") else "📐 Posicionar"):
                action ToggleScreen("herramienta_pos_simple")
                text_size 15
                text_color ("#00ff00" if renpy.get_screen("herramienta_pos_simple") else "#cccccc")
                background "#1a1a1aCC"
                hover_background "#2a2a2aCC"
                padding (12, 8)



################################################################################
## Screen: Mensaje de restricción (auto-dismiss 1.5s)
################################################################################
## Muestra un mensaje en el cuadro de texto del juego sin requerir click.
## Se usa en lugar de renpy.notify() para mensajes del sistema de restricciones.

default _msg_restriccion_texto = ""

screen mensaje_restriccion():
    zorder 150
    
    # Fondo del cuadro de diálogo (parte inferior de pantalla)
    frame:
        xalign 0.5
        yalign 0.98
        xsize 1400
        ypadding 20
        xpadding 40
        background "#1a1a1aCC"
        
        text _msg_restriccion_texto:
            xalign 0.5
            color "#CCCCCC"
            italic True
            size 32
            outlines [(2, "#000000", 0, 0)]
    
    # Timer: cierra el screen automáticamente despues de 1.5 segundos
    timer 1.5 action [Hide("mensaje_restriccion"), Return()]


################################################################################
## Label helper: mostrar mensaje de restricción
################################################################################

label mostrar_mensaje_restriccion(texto):
    $ store._msg_restriccion_texto = texto
    show screen mensaje_restriccion
    $ renpy.pause(1.5, hard=True)
    hide screen mensaje_restriccion
    return

################################################################################
## Fix táctil: mensajes de bloqueo que se cierran solos en celular
################################################################################
## En pantalla táctil, un solo toque puede generar un evento de mouse extra
## que llega justo cuando se abre el diálogo (el mismo bind "mouseup_1" que
## dispara el botón es el que usa Ren'Py para cerrar el cuadro de texto).
## Como estos mensajes son de una sola línea, ese evento sobrante los cierra
## al instante. after_longpress() es el mecanismo que el propio Ren'Py usa
## para tragarse ese evento sobrante (ver renpy/display/core.py); en PC
## renpy.variant("touch") es False y esta función no hace nada.
init python:
    def _blk_guardar_toque():
        if renpy.variant("touch"):
            renpy.game.interface.after_longpress()

################################################################################
## Label helper: pensar un mensaje (usa piensa)
################################################################################

label pensar_mensaje(msg):
    $ _blk_guardar_toque()
    $ msg = renpy.translate_string(msg)
    piensa "[msg]"
    return

################################################################################
## Label helper: narrar un mensaje (usa narrator)
################################################################################

label narrar_mensaje(msg):
    $ _blk_guardar_toque()
    $ msg = renpy.translate_string(msg)
    "[msg]"
    return

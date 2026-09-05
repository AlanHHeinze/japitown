################################################################################
## Screen de Acciones de Locación
################################################################################
## Panel con los botones de accion disponibles en la locación actual.
## Misma estructura visual que panel_entrenamiento.
##
## ⚠️ EN LA HABITACION DEL MC NO DIBUJA SU PROPIO PANEL. Ahi ya esta
## `panel_entrenamiento` (ui/hud/hud_stats.rpy) y los dos frames tienen la MISMA
## posicion —xalign 0.5, yalign 0.0, yoffset 120— asi que se encimaban: una
## accion de locacion en casa_hmc aparecia pisada contra los botones de entrenar
## y trabajar. Ahora los botones se comparten: `acciones_locacion_botones` es el
## bloque suelto y cada panel lo mete adentro del suyo.
##
##     casa_hmc con panel de entrenamiento  → los botones van DENTRO de ese panel
##     cualquier otra locacion              → frame propio, como siempre


init python:

    def panel_entrenamiento_visible():
        """
        True si `panel_entrenamiento` se esta dibujando ahora.

        La consultan los DOS paneles: el de entrenamiento para saber si tiene
        que albergar las acciones de locacion, y el de acciones para saber si
        tiene que abstenerse de dibujar su frame. Vive en un solo lugar para que
        no se puedan desincronizar y quede el panel doble o ninguno.

        La condicion es la misma que el `use` de hud_navigation: estar en la
        habitacion del MC y tener completa la quest 0 del MC (antes de eso el
        panel de entrenamiento todavia no existe).
        """
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_hmc":
            return False
        _q0 = store.sistema_quests_mc.quests.get("mc_quest_0")
        return bool(_q0 and _q0.completada)


## Los botones sueltos, SIN frame: los usan los dos paneles.
##
## `k` entra por parametro en vez de calcularse acá porque cada panel ya tiene
## el suyo y tienen que ser el mismo numero: si el bloque calculara uno propio,
## un cambio en la escala de un panel dejaria los iconos de distinto tamaño
## dentro de la misma fila.
screen acciones_locacion_botones(k=1.0):

    $ _alb_loc = sistema_locaciones.locacion_actual
    $ _alb_lista = sistema_acciones.obtener_acciones_locacion(_alb_loc.id) if _alb_loc else []

    for _als_ac in _alb_lista:
        $ _als_disp = sistema_acciones.esta_disponible(_als_ac.id)
        $ _als_click = _als_disp or bool(_als_ac.mensaje_reintento)

        vbox:
            spacing int(4 * k)
            xalign 0.5

            button:
                xsize int(48 * k) ysize int(48 * k)
                background _als_ac.color
                hover_background _als_ac.color_hover
                insensitive_background "#2A2A2A"
                xalign 0.5
                sensitive _als_click
                at hud_train_hover(k)
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action [
                        SetVariable("_accion_locacion_temp_id", _als_ac.id),
                        Call("accion_locacion_ejecutar")
                    ]
                text "[_als_ac.icono]" size int(22 * k) xalign 0.5 yalign 0.5

            $ _als_nombre_tr = _als_ac.obtener_nombre()
            text "[_als_nombre_tr]":
                # +50% de tamaño (independiente de k, asi que aplica tanto en PC
                # como en small) y blanco cuando esta disponible; el gris oscuro
                # deshabilitado se mantiene para no perder la distincion visual.
                size int(10 * 1.5 * k)
                color ("#FFFFFF" if _als_click else "#555555")
                bold True
                xalign 0.5


# forzar=True: renderiza aunque el HUD esté oculto — lo usa el minijuego de
# espiar (screen espiar_minijuego), que oculta el HUD y muestra este panel por
# su cuenta para que sus botones mantengan la estética del juego. Tambien saltea
# la cesion a panel_entrenamiento: si alguien pide el panel explicitamente, lo
# tiene que recibir.
screen acciones_locacion(forzar=False):

    # Misma escala que el HUD superior (HUD_ESCALA_SMALL, en hud_navigation.rpy):
    # los dos paneles viven pegados arriba, asi que tienen que crecer juntos o el
    # de acciones quedaria tapado por el HUD agrandado.
    $ _als_k = HUD_ESCALA_SMALL if renpy.variant("small") else 1.0

    if (hud_contenido_visible or forzar) and sistema_locaciones.locacion_actual:
        $ _als_loc_id = sistema_locaciones.locacion_actual.id
        $ _als_lista = sistema_acciones.obtener_acciones_locacion(_als_loc_id)

        # Si el panel de entrenamiento esta en pantalla, las acciones van
        # adentro de ese y acá no se dibuja nada: los dos frames comparten
        # posicion y se encimarian.
        if _als_lista and (forzar or not panel_entrenamiento_visible()):
            frame:
                xalign 0.5
                yalign 0.0
                yoffset int(120 * _als_k)
                background "#1e112180"
                padding (int(20 * _als_k), int(12 * _als_k))
                at hud_panel_fadein

                has hbox
                spacing int(15 * _als_k)
                yalign 0.5

                use acciones_locacion_botones(_als_k)

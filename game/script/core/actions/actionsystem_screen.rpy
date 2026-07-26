################################################################################
## Screen de Acciones de Locación
################################################################################
## Panel con los botones de accion disponibles en la locación actual.
## Misma estructura visual que panel_entrenamiento.

# forzar=True: renderiza aunque el HUD esté oculto — lo usa el minijuego de
# espiar (screen espiar_minijuego), que oculta el HUD y muestra este panel por
# su cuenta para que sus botones mantengan la estética del juego.
screen acciones_locacion(forzar=False):

    # Misma escala que el HUD superior (HUD_ESCALA_SMALL, en hud_navigation.rpy):
    # los dos paneles viven pegados arriba, asi que tienen que crecer juntos o el
    # de acciones quedaria tapado por el HUD agrandado.
    $ _als_k = HUD_ESCALA_SMALL if renpy.variant("small") else 1.0

    if (hud_contenido_visible or forzar) and sistema_locaciones.locacion_actual:
        $ _als_loc_id = sistema_locaciones.locacion_actual.id
        $ _als_lista = sistema_acciones.obtener_acciones_locacion(_als_loc_id)

        if _als_lista:
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

                for _als_ac in _als_lista:
                    $ _als_disp = sistema_acciones.esta_disponible(_als_ac.id)
                    $ _als_click = _als_disp or bool(_als_ac.mensaje_reintento)

                    vbox:
                        spacing int(4 * _als_k)
                        xalign 0.5

                        button:
                            xsize int(48 * _als_k) ysize int(48 * _als_k)
                            background _als_ac.color
                            hover_background _als_ac.color_hover
                            insensitive_background "#2A2A2A"
                            xalign 0.5
                            sensitive _als_click
                            at hud_train_hover(_als_k)
                            if modo_posicionamiento:
                                action NullAction()
                            else:
                                action [
                                    SetVariable("_accion_locacion_temp_id", _als_ac.id),
                                    Call("accion_locacion_ejecutar")
                                ]
                            text "[_als_ac.icono]" size int(22 * _als_k) xalign 0.5 yalign 0.5

                        $ _als_nombre_tr = _als_ac.obtener_nombre()
                        text "[_als_nombre_tr]":
                            # +50% de tamaño (independiente de _als_k, asi que
                            # aplica tanto en PC como en small) y blanco cuando
                            # esta disponible; el gris oscuro deshabilitado se
                            # mantiene para no perder la distincion visual.
                            size int(10 * 1.5 * _als_k)
                            color ("#FFFFFF" if _als_click else "#555555")
                            bold True
                            xalign 0.5

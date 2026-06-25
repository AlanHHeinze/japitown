################################################################################
## Screen de Acciones de Locación
################################################################################
## Panel con los botones de accion disponibles en la locación actual.
## Misma estructura visual que panel_entrenamiento.

screen acciones_locacion():

    if hud_contenido_visible and sistema_locaciones.locacion_actual:
        $ _als_loc_id = sistema_locaciones.locacion_actual.id
        $ _als_lista = sistema_acciones.obtener_acciones_locacion(_als_loc_id)

        if _als_lista:
            frame:
                xalign 0.5
                yalign 0.0
                yoffset 120
                background "#1e112180"
                padding (20, 12)
                at hud_panel_fadein

                has hbox
                spacing 15
                yalign 0.5

                for _als_ac in _als_lista:
                    $ _als_disp = sistema_acciones.esta_disponible(_als_ac.id)
                    $ _als_click = _als_disp or bool(_als_ac.mensaje_reintento)

                    vbox:
                        spacing 4
                        xalign 0.5

                        button:
                            xsize 48 ysize 48
                            background _als_ac.color
                            hover_background _als_ac.color_hover
                            insensitive_background "#2A2A2A"
                            xalign 0.5
                            sensitive _als_click
                            at hud_train_hover
                            if modo_posicionamiento:
                                action NullAction()
                            else:
                                action [
                                    SetVariable("_accion_locacion_temp_id", _als_ac.id),
                                    Call("accion_locacion_ejecutar")
                                ]
                            text "[_als_ac.icono]" size 22 xalign 0.5 yalign 0.5

                        $ _als_nombre_tr = renpy.translate_string(_als_ac.nombre)
                        text "[_als_nombre_tr]":
                            size 10
                            color ("#CCCCCC" if _als_click else "#555555")
                            bold True
                            xalign 0.5

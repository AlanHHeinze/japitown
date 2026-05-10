################################################################################
## Menú de Skins de NPC
################################################################################
## Screen para seleccionar y activar/desactivar skins de un NPC

screen menu_skins_npc(npc):
    """
    Menú que muestra los skins disponibles de un NPC.
    Permite activar o desactivar skins.
    """
    
    modal True
    
    # Fondo semi-transparente
    button:
        style "empty_button"
        xfill True
        yfill True
        action Hide("menu_skins_npc")
    
    # Panel de skins
    frame:
        xalign 0.5
        yalign 0.5
        background "#9C27B0EE"  # Púrpura
        padding (30, 20)
        
        vbox:
            spacing 15
            
            # Título
            text "Skins de [npc.nombre]" size 32 color "#FFF8E1" bold True xalign 0.5 outlines [(2, "#6A1B9A", 0, 0)]
            
            # Línea separadora
            null height 5
            frame:
                xsize 320
                ysize 2
                background "#CE93D8"
            null height 10
            
            # Obtener skin activo actual
            $ skin_activo = sistema_skins.obtener_skin_activo(npc.id)
            
            # Mostrar skin actual
            if skin_activo:
                text "Actual: [skin_activo.nombre]" size 18 color "#E1BEE7" xalign 0.5
            else:
                text "Actual: Skin Base" size 18 color "#E1BEE7" xalign 0.5
            
            null height 10
            
            # Lista de skins disponibles
            vbox:
                spacing 10
                xsize 320
                
                # Opción: Skin Base (desactivar skin)
                button:
                    xfill True
                    if skin_activo is None:
                        background "#4CAF50"  # Verde si activo
                    else:
                        background "#7B1FA2"
                    hover_background "#8E24AA"
                    padding (15, 10)
                    action [Function(desactivar_skin, npc.id),
                            Hide("menu_skins_npc")]
                    
                    hbox:
                        spacing 10
                        if skin_activo is None:
                            text "✓" size 20 color "#ffffff"
                        else:
                            text "○" size 20 color "#CE93D8"
                        vbox:
                            text "Skin Base" size 18 color "#ffffff" bold True
                            text "Apariencia original" size 14 color "#E1BEE7"
                
                # Separador
                null height 5
                
                # Skins desbloqueados
                $ skins_disponibles = sistema_skins.obtener_skins_desbloqueados(npc.id)
                
                for skin in skins_disponibles:
                    $ es_activo = (skin_activo and skin_activo.id == skin.id)
                    
                    button:
                        xfill True
                        if es_activo:
                            background "#4CAF50"  # Verde si activo
                        else:
                            background "#7B1FA2"
                        hover_background "#8E24AA"
                        padding (15, 10)
                        action [Function(activar_skin, npc.id, skin.id),
                                Hide("menu_skins_npc")]
                        
                        hbox:
                            spacing 10
                            if es_activo:
                                text "✓" size 20 color "#ffffff"
                            else:
                                text "○" size 20 color "#CE93D8"
                            vbox:
                                text "[skin.nombre]" size 18 color "#ffffff" bold True
                                if skin.descripcion:
                                    text "[skin.descripcion]" size 14 color "#E1BEE7"
            
            null height 15
            
            # Botón cerrar
            textbutton "Cerrar":
                xalign 0.5
                action Hide("menu_skins_npc")
                style "menu_choice_button"

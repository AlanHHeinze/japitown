################################################################################
## Screen de Navegación por Locaciones
################################################################################
## Screen que muestra la locación actual y permite interactuar con hotspots

screen navegacion_locaciones():
    
    # Modal para capturar todos los clicks
    modal True
    
    # Background de la locación actual
    if sistema_locaciones.locacion_actual:
        add sistema_locaciones.locacion_actual.background
        
        # Hotspots interactivos
        for hotspot in sistema_locaciones.locacion_actual.obtener_hotspots_habilitados():
            
            # Área clickeable del hotspot
            button:
                xpos hotspot.x
                ypos hotspot.y
                xysize (hotspot.w, hotspot.h)
                background None
                hover_background None
                
                # Accion según tipo de hotspot
                if hotspot.tipo == "MOVE":
                    action [SetVariable("_hotspot_temp", hotspot), Call("accion_hotspot_move")]
                elif hotspot.tipo == "ACTION":
                    action [SetVariable("_hotspot_temp", hotspot), Call("accion_hotspot_action")]
                
                # Mostrar nombre del hotspot al hacer hover (opcional, para debug)
                # Hover deshabilitado por el usuario
                
                if hotspot.nombre:
                    tooltip hotspot.nombre
                else:
                    tooltip hotspot.id
        
        # ========== REPARTIDOR EN FRENTE DE CASA ==========
        # Mostrar idle del repartidor si está presente y estamos en casa_frente
        if repartidor_presente and sistema_locaciones.locacion_actual.id == "casa_frente":
            imagebutton:
                idle "idle_repartidor_puerta"
                hover "idle_repartidor_puerta"
                xalign 0.7
                yalign 1.0
                action Jump("interaccion_repartidor")
        
        # ========== PAQUETE EN HABITACIÓN DEL MC ==========
        # Mostrar idle del paquete si está en la habitacion
        if paquete_en_habitacion and sistema_locaciones.locacion_actual.id == "casa_hmc":
            imagebutton:
                idle "idle_paquete_hmc"
                hover "idle_paquete_hmc"
                xalign 0.3
                yalign 0.8
                action Jump("recoger_paquete_habitacion")
        
        # Informacion de la locación (opcional, para debug)
        if config.developer:
            frame:
                xalign 0.0
                yalign 0.0
                background "#000000CC"
                padding (10, 10)
                vbox:
                    text "Locación: [sistema_locaciones.locacion_actual.nombre]" size 20
                    text "ID: [sistema_locaciones.locacion_actual.id]" size 16
                    text "Hotspots: [len(sistema_locaciones.locacion_actual.obtener_hotspots_habilitados())]" size 16
                    
                    $ tooltip_text = GetTooltip()
                    if tooltip_text:
                        text "Hotspot: [tooltip_text]" size 16 color "#00ff00"


init python:
    
    def manejar_hotspot_move(hotspot):
        """
        Maneja el click en un hotspot de tipo MOVE.
        Ejecuta el flujo completo de cambio de locación.
        """
        if hotspot.destino:
            sistema_locaciones.mover_a_locacion(hotspot.destino)
    
    def manejar_hotspot_action(hotspot):
        """
        Maneja el click en un hotspot de tipo ACTION.
        Ejecuta la accion sin cambiar de locación.
        """
        sistema_locaciones.ejecutar_accion_hotspot(hotspot)
        


################################################################################
## Labels de control
################################################################################

label iniciar_navegacion:
    
    # Verificar que hay una locación actual
    if not sistema_locaciones.locacion_actual:
        "Error: No hay locación inicial definida"
        return
    
    # Mostrar el screen de navegación
    show screen navegacion_locaciones
    
    # Loop infinito para mantener la navegación activa
    label loop_navegacion:
        pause
        jump loop_navegacion

label ir_a(locacion_id):
    
    $ sistema_locaciones.mover_a_locacion(locacion_id)
    return

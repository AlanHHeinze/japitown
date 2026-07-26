################################################################################
## Sistema de Mensajes al Despertar
################################################################################
## Verifica novedades al despertar y muestra mensajes del MC

# Set de textos de mensajes_despertar ya mostrados (no se repiten)
default mensajes_despertar_mostrados = set()

init python:
    
    def _agregar_mensajes_despertar(mensajes, msg):
        """
        Agrega uno o varios mensajes de despertar a la lista, evitando repetir.
        `msg` puede ser un string (un solo pensamiento) o una lista/tupla de
        strings: asi una misma etapa de quest puede mostrar varios piensa
        seguidos (ej: la reflexion + un comentario). Cada linea se traduce al
        mostrarse (piensa "[_(...)]" en el label), asi que aca van en español.
        """
        if not msg:
            return
        piezas = msg if isinstance(msg, (list, tuple)) else [msg]
        for pieza in piezas:
            if pieza and pieza not in store.mensajes_despertar_mostrados:
                mensajes.append(pieza)
                store.mensajes_despertar_mostrados.add(pieza)

    def obtener_mensajes_despertar():
        """
        Detecta quests, eventos y pedidos nuevos que tengan mensaje_despertar.

        Returns:
            list: Lista de strings con los mensajes a mostrar
        """
        mensajes = []

        # Validar eventos para que los que cumplan condición pasen a VISIBLE
        if hasattr(store, 'validar_eventos'):
            store.validar_eventos()

        # 1. Quests activas — mensaje dinámico por etapa
        if hasattr(store, 'sistema_quests'):
            for quest in store.sistema_quests.obtener_quests_activas():
                _agregar_mensajes_despertar(mensajes, quest.obtener_mensaje_despertar_actual())

        # 2. Eventos visibles/activos — mensaje dinámico por estado
        if hasattr(store, 'sistema_events'):
            for evento in store.sistema_events.obtener_events_visibles():
                _agregar_mensajes_despertar(mensajes, evento.obtener_mensaje_despertar_actual())
        
        # 3. Pedidos que llegan hoy (siempre se muestra, no se trackea)
        if hasattr(store, 'sistema_compras') and store.repartidor_presente:
            msg = obtener_mensaje_despertar_pedido()
            if msg:
                mensajes.append(msg)
        
        return mensajes
    
    def obtener_mensaje_despertar_pedido():
        """
        Genera mensaje de pedido según nivel de confianza del repartidor.
        Incluye lista de items al final.
        
        Returns:
            str: Mensaje completo o None
        """
        entregas = store.sistema_compras.verificar_entregas_hoy()
        if not entregas:
            return None
        
        # Mensaje base según confianza
        confianza = store.repartidor_confianza
        
        if confianza == 0:
            base = _("Creo que escuche que alguien toco la puerta...")
        elif confianza <= 5:
            base = _("Me llego un pedido, tendria que ir a buscarlo.")
        else:
            base = _("Ah me llego el pedido, voy a ir a buscarlo.")
        
        # Agregar lista de items
        items_unificados = store.sistema_compras.unificar_entregas_hoy()
        if items_unificados:
            lineas_items = []
            for item_id, cantidad in items_unificados.items():
                if item_id in CATALOGO_ITEMS:
                    nombre = CATALOGO_ITEMS[item_id]["nombre"]
                    emoji = CATALOGO_ITEMS[item_id]["emoji"]
                    lineas_items.append(f"  {emoji} {nombre} x{cantidad}")
            
            if lineas_items:
                base += "\n" + "\n".join(lineas_items)
        
        return base


################################################################################
## Label de Mensajes al Despertar
################################################################################

label mensajes_al_despertar:
    
    # Obtener mensajes pendientes
    $ lista_mensajes_despertar = obtener_mensajes_despertar()
    
    # Si no hay mensajes, retornar inmediatamente
    if not lista_mensajes_despertar:
        return
    
    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Mostrar habitacion del MC (horario actual, normalmente mañana tras dormir)
    $ _bg_despertar = sistema_locaciones.obtener_locacion("casa_hmc").background
    scene expression _bg_despertar with fade
    
    # Mostrar MC parado
    show mc_parado_base c_rbase_pensando o_arribanm b_none at center with dissolve
    
    # Mostrar cada mensaje como pensamiento individual
    $ idx_despertar = 0
    while idx_despertar < len(lista_mensajes_despertar):
        $ msg_despertar_actual = _(lista_mensajes_despertar[idx_despertar])
        piensa "[msg_despertar_actual]"
        $ idx_despertar += 1
    
    # Ocultar MC
    hide mc_parado_base with dissolve
    
    return

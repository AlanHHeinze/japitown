################################################################################
## Sistema de Compras - Core
################################################################################
## Sistema de compras con entrega a domicilio, tracking de órdenes y 
## calculación de dias hábiles

init python:
    
    class OrdenCompra:
        """
        Representa una orden de compra con sus items y fecha de entrega.
        """
        
        def __init__(self, numero, items, dia_entrega, dia_semana_entrega, estacion_entrega, año_entrega, dia_creacion=0):
            self.numero = numero  # Numero único de orden
            self.items = items  # Dict {item_id: cantidad}
            self.dia_entrega = dia_entrega
            self.dia_semana_entrega = dia_semana_entrega
            self.estacion_entrega = estacion_entrega
            self.año_entrega = año_entrega
            self.dia_creacion = dia_creacion  # dias_totales al momento de crear
            self.entregada = False
        
        def obtener_dias_restantes(self):
            """Calcula los días hábiles restantes hasta la entrega (igual que calcular_fecha_entrega)."""
            dia      = store.dia_actual
            dia_sem  = store.dia_semana_actual
            estacion = store.estacion_actual
            año      = store.año_actual

            if (dia == self.dia_entrega and estacion == self.estacion_entrega and año == self.año_entrega):
                return 0

            habiles = 0
            for _ in range(60):
                dia += 1
                dia_sem = (dia_sem + 1) % 7
                if dia > 31:
                    dia = 1
                    estacion += 1
                    if estacion >= 4:
                        estacion = 0
                        año += 1
                if dia_sem < 5:
                    habiles += 1
                if (dia == self.dia_entrega and estacion == self.estacion_entrega and año == self.año_entrega):
                    break

            return max(0, habiles)
        
        def es_dia_entrega(self):
            """Verifica si hoy es el día de entrega."""
            return (store.dia_actual == self.dia_entrega and 
                    store.estacion_actual == self.estacion_entrega and
                    store.año_actual == self.año_entrega)
        
        def obtener_texto_dias(self):
            """Retorna texto descriptivo de días restantes."""
            dias = self.obtener_dias_restantes()
            if dias == 0:
                return renpy.translate_string("Llega hoy")
            elif dias == 1:
                return renpy.translate_string("Llega mañana")
            else:
                tmpl = renpy.translate_string("Llega en {dias} días")
                return tmpl.format(dias=dias)

        def obtener_contenido_texto(self):
            """Retorna lista formateada de items."""
            from store import CATALOGO_ITEMS
            lineas = []
            for item_id, cantidad in self.items.items():
                if item_id in CATALOGO_ITEMS:
                    nombre = renpy.translate_string(CATALOGO_ITEMS[item_id]["nombre"])
                    emoji = CATALOGO_ITEMS[item_id]["emoji"]
                    lineas.append(f"{emoji} {nombre} x{cantidad}")
            return lineas
    
    
    class SistemaCompras:
        """
        Gestor central del sistema de compras.
        Maneja órdenes, entregas y cálculo de dias hábiles.
        """
        
        def __init__(self):
            pass
        
        def calcular_fecha_entrega(self, dias_espera):
            """
            Calcula la fecha de entrega considerando solo dias hábiles.
            Los paquetes no llegan sábados ni domingos.
            
            Args:
                dias_espera: Dias base de espera del item
            
            Returns:
                tuple: (dia, dia_semana, estacion, año)
            """
            dia = store.dia_actual
            dia_semana = store.dia_semana_actual
            estacion = store.estacion_actual
            año = store.año_actual
            
            dias_contados = 0
            
            while dias_contados < dias_espera:
                # Avanzar un dia
                dia += 1
                dia_semana = (dia_semana + 1) % 7
                
                # Verificar cambio de estación
                if dia > 31:
                    dia = 1
                    estacion += 1
                    if estacion >= 4:
                        estacion = 0
                        año += 1
                
                # Solo contar dias hábiles (Lunes=0 a Viernes=4)
                if dia_semana < 5:
                    dias_contados += 1
            
            return (dia, dia_semana, estacion, año)
        
        def crear_orden(self, items, dia_entrega, dia_semana_entrega, estacion_entrega, año_entrega):
            """
            Crea una nueva orden de compra con fecha pre-calculada.

            Args:
                items: Dict {item_id: cantidad}
                dia_entrega, dia_semana_entrega, estacion_entrega, año_entrega: fecha de entrega

            Returns:
                OrdenCompra: La orden creada
            """
            store.ultimo_numero_orden += 1
            orden = OrdenCompra(
                numero=store.ultimo_numero_orden,
                items=dict(items),
                dia_entrega=dia_entrega,
                dia_semana_entrega=dia_semana_entrega,
                estacion_entrega=estacion_entrega,
                año_entrega=año_entrega,
                dia_creacion=store.dias_totales
            )
            store.ordenes_compra.append(orden)
            return orden

        def comprar_item(self, item_id):
            """
            Compra un item. Si ya existe una orden abierta de la misma sesión
            con la misma fecha de entrega, agrega el item a esa orden.
            Si no, crea una nueva orden.

            Args:
                item_id: ID del item a comprar

            Returns:
                bool: True si se pudo comprar
            """
            from store import CATALOGO_ITEMS

            if item_id not in CATALOGO_ITEMS:
                return False

            # Verificar stock
            stock_actual = store.stock_tienda.get(item_id, 0)
            if stock_actual <= 0:
                return False

            precio = CATALOGO_ITEMS[item_id]["precio"]
            if store.dinero < precio:
                return False

            # Descontar dinero y stock
            store.dinero -= precio
            store.stock_tienda[item_id] = stock_actual - 1

            # Notificación visual de gasto
            if hasattr(store, 'notificar_cambio_stat'):
                notificar_cambio_stat("dinero", -precio)

            # Calcular fecha de entrega para este item
            dias_item = CATALOGO_ITEMS[item_id].get("dias_entrega", 1)
            dia, dia_semana, estacion, año = self.calcular_fecha_entrega(dias_item)

            # Buscar orden abierta de la misma sesión (mismo dia_creacion) con misma fecha entrega
            orden_existente = None
            for orden in store.ordenes_compra:
                if (not orden.entregada and
                        getattr(orden, 'dia_creacion', -1) == store.dias_totales and
                        orden.dia_entrega == dia and
                        orden.estacion_entrega == estacion and
                        orden.año_entrega == año):
                    orden_existente = orden
                    break

            if orden_existente:
                # Agregar al orden existente
                orden_existente.items[item_id] = orden_existente.items.get(item_id, 0) + 1
            else:
                # Crear nueva orden
                self.crear_orden({item_id: 1}, dia, dia_semana, estacion, año)

            return True
        
        def obtener_ordenes_pendientes(self):
            """Retorna lista de órdenes no entregadas."""
            return [o for o in store.ordenes_compra if not o.entregada]
        
        def verificar_entregas_hoy(self):
            """
            Verifica si hay entregas programadas para hoy.
            
            Returns:
                list: Lista de órdenes que llegan hoy
            """
            entregas_hoy = []
            for orden in store.ordenes_compra:
                if not orden.entregada and orden.es_dia_entrega():
                    entregas_hoy.append(orden)
            return entregas_hoy
        
        def unificar_entregas_hoy(self):
            """
            Unifica todas las órdenes que llegan hoy en una sola entrega.
            
            Returns:
                dict: Items unificados {item_id: cantidad}
            """
            items_unificados = {}
            entregas = self.verificar_entregas_hoy()
            
            for orden in entregas:
                for item_id, cantidad in orden.items.items():
                    if item_id not in items_unificados:
                        items_unificados[item_id] = 0
                    items_unificados[item_id] += cantidad
            
            return items_unificados
        
        def marcar_entregas_hoy_como_entregadas(self):
            """Marca todas las órdenes de hoy como entregadas."""
            for orden in store.ordenes_compra:
                if not orden.entregada and orden.es_dia_entrega():
                    orden.entregada = True
        
        def entregar_items_a_inventario(self, items):
            """
            Agrega items al inventario del jugador.
            
            Args:
                items: Dict {item_id: cantidad}
            """
            for item_id, cantidad in items.items():
                if item_id not in store.inventario:
                    store.inventario[item_id] = 0
                store.inventario[item_id] += cantidad
                if hasattr(store, 'notificar_item_obtenido'):
                    notificar_item_obtenido(item_id)
        
        def hay_entrega_pendiente_hoy(self):
            """Verifica si hay entregas pendientes para hoy (mañana) y no hay paquete esperando."""
            # No mostrar repartidor si ya hay paquete en la habitacion
            if store.paquete_en_habitacion:
                return False
            return len(self.verificar_entregas_hoy()) > 0 and store.horario_actual == 0
        
        def hay_paquete_bloqueante(self):
            """Verifica si hay un paquete en la habitación bloqueando dormir."""
            return store.paquete_en_habitacion
        
        def colocar_paquete_en_habitacion(self):
            """Coloca el paquete en la habitación del MC. Si ya hay paquete, agrega los items."""
            items = self.unificar_entregas_hoy()
            
            # Si ya hay paquete, agregar items en lugar de reemplazar
            if store.paquete_en_habitacion:
                for item_id, cantidad in items.items():
                    if item_id not in store.items_paquete_pendiente:
                        store.items_paquete_pendiente[item_id] = 0
                    store.items_paquete_pendiente[item_id] += cantidad
            else:
                store.items_paquete_pendiente = items
                store.paquete_en_habitacion = True
            
            self.marcar_entregas_hoy_como_entregadas()
        
        def recoger_paquete_habitacion(self):
            """
            El jugador recoge el paquete de la habitacion.
            Solo entrega los items del dia actual, como hace el repartidor.
            """
            if store.paquete_en_habitacion:
                # Usar la misma lógica que el repartidor - solo items de hoy
                items = self.unificar_entregas_hoy()
                
                # Si no hay items de hoy pero hay paquete, entregar lo que quedó pendiente
                if not items and store.items_paquete_pendiente:
                    items = store.items_paquete_pendiente
                    store.items_paquete_pendiente = {}
                    store.paquete_en_habitacion = False
                elif items:
                    # Entregar items de hoy y marcar órdenes
                    self.marcar_entregas_hoy_como_entregadas()
                    
                    # Verificar si aún hay órdenes pendientes para otros dias
                    ordenes_pendientes = self.obtener_ordenes_pendientes()
                    if not ordenes_pendientes:
                        store.items_paquete_pendiente = {}
                        store.paquete_en_habitacion = False
                
                # Entregar al inventario
                if items:
                    self.entregar_items_a_inventario(items)
                    return True
            return False
        
        def mostrar_resumen_ordenes(self):
            """Genera texto con resumen de órdenes pendientes."""
            from store import CATALOGO_ITEMS
            
            ordenes = self.obtener_ordenes_pendientes()
            if not ordenes:
                return None
            
            lineas = []
            for orden in ordenes:
                lineas.append(f"Orden de compra N°{orden.numero}")
                lineas.append(orden.obtener_texto_dias())
                lineas.append("Contenido:")
                for texto in orden.obtener_contenido_texto():
                    lineas.append(f"  {texto}")
                lineas.append("")
            
            return "\n".join(lineas)


# Instancia global del sistema de compras
default sistema_compras = SistemaCompras()

# Variables persistentes del sistema de compras
default ordenes_compra = []  # Lista de OrdenCompra
default ultimo_numero_orden = 0  # Contador de órdenes (nunca se reinicia)
default paquete_en_habitacion = False  # Si hay paquete en la habitacion del MC
default items_paquete_pendiente = {}  # Items del paquete pendiente
default repartidor_presente = False  # Si el repartidor está en la puerta

# Stock de la tienda
default stock_tienda = {}  # {item_id: cantidad_en_stock}

# Mensaje temporal para uso de items
default msg_uso_item = ""

################################################################################
## Funciones de utilidad
################################################################################

init python:
    
    def inicializar_stock():
        """Inicializa el stock de la tienda desde el catálogo."""
        for item_id, info in CATALOGO_ITEMS.items():
            if item_id not in store.stock_tienda:
                store.stock_tienda[item_id] = info.get("stock", 99)
    
    def reponer_stock():
        """
        Repone stock de la tienda. Se llama al inicio de cada semana (Lunes).
        Suma el valor de reposición sin exceder el stock máximo del catálogo.
        """
        for item_id, info in CATALOGO_ITEMS.items():
            reposicion = info.get("reposicion", 0)
            if reposicion > 0:
                stock_max = info.get("stock", 99)
                actual = store.stock_tienda.get(item_id, 0)
                store.stock_tienda[item_id] = min(stock_max, actual + reposicion)
    
    def obtener_dias_para_reposicion():
        """Calcula días que faltan para el próximo Lunes (reposición)."""
        dia_semana = store.dia_semana_actual  # 0=Lunes, 6=Domingo
        if dia_semana == 0:
            return 7  # Si hoy es lunes, la próxima es en 7 dias
        return 7 - dia_semana
    
    def hay_entregas_hoy():
        """Helper: verifica si hay entregas hoy."""
        return sistema_compras.hay_entrega_pendiente_hoy()
    
    def obtener_ordenes_pendientes():
        """Helper: obtiene órdenes pendientes."""
        return sistema_compras.obtener_ordenes_pendientes()
    
    def comprar_item_tienda(item_id):
        """Helper: compra un item de la tienda."""
        return sistema_compras.comprar_item(item_id)
    
    def recoger_paquete():
        """Helper: recoge el paquete de la habitación."""
        return sistema_compras.recoger_paquete_habitacion()
    
    def usar_item(item_id):
        """
        Intenta usar un item del inventario.
        Cierra el panel, muestra mensaje o llama al label correspondiente.
        
        Args:
            item_id: ID del item a usar
        """
        # Verificar restricción de quest/evento
        _msg = accion_bloqueada("usar_item")
        if _msg:
            store.msg_uso_item = _msg
            renpy.jump("mostrar_mensaje_uso_item")
            return
        
        item_info = CATALOGO_ITEMS.get(item_id)
        if not item_info:
            return
        
        # Cerrar panel de inventario
        renpy.hide_screen("panel_inventario")
        
        # Verificar si es usable
        if not item_info.get("usable", False):
            store.msg_uso_item = renpy.translate_string("No puedo usar esto")
            renpy.jump("mostrar_mensaje_uso_item")
            return

        # Verificar condición de uso
        condicion = item_info.get("condicion_uso")
        if condicion and not condicion():
            store.msg_uso_item = renpy.translate_string(item_info.get("instruccion_uso", "No puedo usar esto ahora"))
            renpy.jump("mostrar_mensaje_uso_item")
            return
        
        # Consumir si es consumible
        if item_info.get("consumible", True):
            if item_id in store.inventario:
                store.inventario[item_id] -= 1
                if store.inventario[item_id] <= 0:
                    del store.inventario[item_id]
        
        # Saltar al label de uso
        label_uso = item_info.get("label_uso")
        if label_uso:
            renpy.jump(label_uso)


################################################################################
## Labels del sistema de compras
################################################################################

label verificar_entrega_mañana:
    # Se llama despues de dormir, cuando es mañana
    
    $ entregas_hoy = sistema_compras.verificar_entregas_hoy()
    
    if entregas_hoy:
        # Hay entregas - colocar repartidor en puerta
        $ repartidor_presente = True
        "El repartidor debería estar en la puerta con el pedido."
    
    return


label repartidor_se_fue:
    # Se llama cuando el jugador avanza el tiempo sin interactuar con el repartidor
    
    if repartidor_presente:
        $ repartidor_presente = False
        $ sistema_compras.colocar_paquete_en_habitacion()
    
    return


label intentar_dormir_con_paquete:
    # Se llama cuando el jugador intenta dormir con paquete en habitacion
    
    "Debería sacar esto de la cama antes de acostarme."
    
    return


label recoger_paquete_habitacion:
    # Se llama cuando el jugador interactúa con el paquete en su habitacion

    # Verificar si es un paquete de quest
    if violet_quest1_en_cama:
        jump paquetecama_quest01_violet

    # Ocultar HUD temporalmente
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Mostrar escena de la habitacion del MC según horario
    $ _horarios_bg = ["tarde", "tarde", "noche", "noche"]
    $ _bg_horario = _horarios_bg[horario_actual]
    scene expression "images/bg/casa/bg_casa_" + _bg_horario + "_hmc.png" with fade
    
    # Mostrar MC a la izquierda sosteniendo el paquete
    show mc_parado_base c_rbase_regaloviolet o_abajonm b_none at mc_izquierda with dissolve
    
    piensa "Alguna de las chicas recibió mi pedido y me lo dejó aquí."
    
    # Recoger items
    $ recoger_paquete()
    
    show mc_parado_base c_rbase_regaloviolet o_felicescerrados b_felizcerrada with sprite_normal
    
    piensa "Bien, voy a guardar todo."
    
    # Ocultar MC
    hide mc_parado_base with dissolve
    
    # Volver al game loop
    jump game_loop


label mostrar_mensaje_uso_item:
    # Cerrar panel si quedo abierto
    hide screen panel_inventario
    # Absorber el evento de clic pendiente del boton que disparo el jump
    $ renpy.pause(0)
    # Muestra un mensaje del MC cuando intenta usar un item
    window show
    piensa "[msg_uso_item]"
    window hide
    jump game_loop

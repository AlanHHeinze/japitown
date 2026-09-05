################################################################################
## Sistema de Compras - Core
################################################################################
## Sistema de compras con entrega a domicilio, tracking de órdenes y 
## calculación de dias hábiles

init python:

    def _sc_avanzar_un_dia(fecha):
        """
        Avanza una fecha (dia, dia_semana, estacion, año) un dia de calendario,
        resolviendo el cambio de mes/estación/año. Funcion de modulo (no se guarda).
        """
        dia, dia_semana, estacion, año = fecha
        dia += 1
        dia_semana = (dia_semana + 1) % 7
        if dia > 31:
            dia = 1
            estacion += 1
            if estacion >= 4:
                estacion = 0
                año += 1
        return (dia, dia_semana, estacion, año)

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
            """
            Días de CALENDARIO que faltan hasta la entrega. Como la fecha de entrega
            ya nunca cae en fin de semana (calcular_fecha_entrega la mueve al lunes),
            esto muestra, por ejemplo, los dias que faltan hasta el lunes por la mañana.
            """
            fecha = (store.dia_actual, store.dia_semana_actual, store.estacion_actual, store.año_actual)

            def _es_entrega(f):
                return f[0] == self.dia_entrega and f[2] == self.estacion_entrega and f[3] == self.año_entrega

            if _es_entrega(fecha):
                return 0

            dias = 0
            for _ in range(60):
                fecha = _sc_avanzar_un_dia(fecha)
                dias += 1
                if _es_entrega(fecha):
                    break

            return max(0, dias)
        
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
            Calcula la fecha de entrega.

            Los dias de espera cuentan como dias de CALENDARIO (los fines de semana
            cuentan igual que cualquier otro dia). Lo único que no puede pasar es
            entregar sábado o domingo: si la fecha cae en fin de semana, se mueve al
            lunes. Así una espera con un finde en el medio no suma dias extra;
            solo se difiere la entrega cuando el propio dia de llegada es finde.

            Args:
                dias_espera: Dias base de espera del item

            Returns:
                tuple: (dia, dia_semana, estacion, año)
            """
            fecha = (store.dia_actual, store.dia_semana_actual, store.estacion_actual, store.año_actual)

            # 1. Avanzar los dias de espera contando TODOS los dias.
            for _ in range(dias_espera):
                fecha = _sc_avanzar_un_dia(fecha)

            # 2. Si la entrega cae en fin de semana (5=Sábado, 6=Domingo),
            #    moverla al lunes siguiente.
            while fecha[1] >= 5:
                fecha = _sc_avanzar_un_dia(fecha)

            return fecha
        
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
                lineas.append(renpy.translate_string("Orden de compra N°{numero}").format(numero=orden.numero))
                lineas.append(orden.obtener_texto_dias())
                lineas.append(renpy.translate_string("Contenido:"))
                for texto in orden.obtener_contenido_texto():
                    lineas.append("  {}".format(texto))
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
    
    def cantidad_en_camino(item_id):
        """Cuántas unidades de un item hay compradas pero todavía sin entregar."""
        total = 0
        try:
            for orden in sistema_compras.obtener_ordenes_pendientes():
                total += orden.items.get(item_id, 0)
        except Exception:
            pass
        return total

    def cantidad_comprada(item_id):
        """Inventario + pedidos en camino. Sirve para que las pistas de quest
        distingan 'todavía hay que comprarlo' de 'ya lo compré, está por llegar'."""
        try:
            en_inventario = store.inventario.get(item_id, 0)
        except Exception:
            en_inventario = 0
        return en_inventario + cantidad_en_camino(item_id)

    def comprar_item_tienda(item_id):
        """Helper: compra un item de la tienda."""
        exito = sistema_compras.comprar_item(item_id)
        # Revalidar las quests en el acto: varias tienen un Requisito("item") o
        # una pista que depende de la compra. El game_loop también las revalida,
        # pero solo corre al cerrar el celular — y la tienda y la app de Pistas
        # están DENTRO del celular, así que sin esto la pista no se actualizaría
        # hasta salir.
        if exito:
            try:
                store.actualizar_quests()
            except Exception:
                pass
        return exito
    
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

# NOTA: acá vivían `verificar_entrega_mañana` y `repartidor_se_fue`. Se
# eliminaron porque estaban MUERTOS: nadie los invocaba (ni por call/jump ni por
# string), y su lógica ya había sido movida al sistema de tiempo —
# `verificar_entrega_mañana` está inlineada en `accion_dormir` y
# `repartidor_se_fue` en `avanzar_horario()` (colocar_paquete_en_habitacion).
# Además ambos terminaban en `return`, así que si alguien los hubiera cableado
# con un Jump habrían mandado al menú principal. Recuperables por git.


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
    
    # Mostrar escena de la habitacion del MC según horario.
    # El bg lo resuelve el sistema de locaciones, que ya sabe el horario
    # (y respeta horario_visual_override). Antes se armaba con una lista a
    # mano que estaba desalineada con la canonica de locationsystem_core.
    $ _bg_horario = sistema_locaciones.obtener_locacion("casa_hmc").background
    scene expression _bg_horario with fade
    
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

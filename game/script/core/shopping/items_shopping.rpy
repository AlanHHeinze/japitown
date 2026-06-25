################################################################################
## Catálogo de Items - Sistema de Compras
################################################################################
## Definición de todos los items disponibles para comprar
## Agregar nuevos items es simple: solo agregar una entrada al diccionario

init python:

    def _item_en_habitacion_mc():
        """Condición de uso: el MC debe estar en su habitación (casa_hmc)."""
        loc = store.sistema_locaciones.locacion_actual
        return loc is not None and loc.id == "casa_hmc"

    def _bateria_nt520_disponible():
        """La batería aparece en la tienda recién al completar la quest 0_c de Monica."""
        q = store.sistema_quests.obtener_quest("monica_questprincipal_0_c")
        return q is not None and q.completada

    # Catálogo de items disponibles para comprar
    # Formato: "id": {"nombre": str, "emoji": str, "precio": int, "dias_entrega": int}
    # dias_entrega: Días hábiles (no incluye fines de semana)

    CATALOGO_ITEMS = {
        # Comida - Entrega rápida
        "golosinas": {
            "nombre": "Golosinas",
            "emoji": "🍭",
            "precio": 20,
            "dias_entrega": 1,
            "descripcion": "Una bolsa con varias golosinas",
            "usable": True,
            "vendible": True,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Podría usarlo en alguien con hambre",
            "consumible": False,
            "stock": 10,
            "reposicion": 5,
        },
        "vino": {
            "nombre": "Vino",
            "emoji": "🍷",
            "precio": 20,
            "dias_entrega": 1,
            "descripcion": "Vino tinto de buena calidad",
            "usable": False,
            "vendible": True,
            "stock": 5,
            "reposicion": 3,
        },
        
        # Lociones - Entrega media
        "locion_masajes": {
            "nombre": "Locion de masajes",
            "emoji": "🧴",
            "precio": 20,
            "dias_entrega": 1,
            "descripcion": "Loción de masajes para relajar los músculos",
            "usable": True,
            "vendible": True,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Podría usarlo en alguien cansado",
            "consumible": False,
            "stock": 10,
            "reposicion": 5,
        },

        "bebida_energetica": {
            "nombre": "Bebida energética",
            "emoji": "🥤",
            "precio": 20,
            "dias_entrega": 1,
            "descripcion": "Una bebida energética",
            "usable": True,
            "vendible": True,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Podría usarlo en alguien agotada",
            "consumible": False,
            "stock": 10,
            "reposicion": 5,
        },
        
        # Equipamiento - Entrega media
        "pesas": {
            "nombre": "Pesas",
            "emoji": "🏋️",
            "precio": 100,
            "dias_entrega": 2,
            "descripcion": "Set de pesas para entrenar",
            "usable": False,
            "vendible": True,
            "stock": 2,
            "reposicion": 1,
        },
        
        "casco_realidad_virtual": {
            "nombre": "Casco realidad virtual",
            "emoji": "🎮",
            "precio": 250,
            "dias_entrega": 4,
            "descripcion": "Un casco de realidad virtual para jugar videojuegos",
            "usable": True,
            "vendible": True,
            "condicion_uso": lambda: (
                hasattr(store, 'sistema_locaciones') and
                store.sistema_locaciones.locacion_actual and
                store.sistema_locaciones.locacion_actual.id == "casa_hmc" and
                store.horario_actual == 2
            ),
            "instruccion_uso": "Debería usar esto en mi habitación por la noche",
            "label_uso": "usar_casco_vr",
            "consumible": False,
            "stock": 0,
            "reposicion": 0,
        },
        
        # Ropa - Entrega media
        "conjunto_cosplays": {
            "nombre": "Conjunto de cosplays",
            "emoji": "👗",
            "precio": 200,
            "dias_entrega": 2,
            "descripcion": "Quizás a Violet le guste alguno de estos",
            "usable": False,
            "vendible": False,
            "stock": 1,
            "reposicion": 0,
            "icono": "images/ui/shopping/caja_cerrada.png", # Se asume una imagen genérica si no existe
        },

        # Entrada Japicon — disponible en tienda, stock 0 hasta completar quest 05_c
        "entrada_japicon": {
            "nombre": "Entrada Japicon",
            "emoji": "🎟️",
            "precio": 150,
            "dias_entrega": 2,
            "descripcion": "Entradas para la Japicon.",
            "usable": True,
            "vendible": True,
            "consumible": False,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Entradas para la Japicon",
            "stock": 0,
            "reposicion": 0,
        },

        # Coxplay Box — llega por delivery de la quest 05_a
        "coxplay_box": {
            "nombre": "Coxplay Box",
            "emoji": "📦",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Una caja con tres cosplay. Debería dársela a Violet.",
            "usable": True,
            "vendible": False,
            "consumible": False,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Debería darle esto a Violet",
            "stock": 0,
            "reposicion": 0,
            "icono": "images/ui/shopping/caja_cerrada.png",
        },

        # Perfume — regalo de quest para Monica (no comprable)
        # Ya no se "usa" desde el inventario: la quest 0 se inicia con el botón
        # "Agradecerle" del menú de Mónica (que consume el perfume).
        "perfume": {
            "nombre": "Perfume",
            "emoji": "🌸",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "El regalo que le traje a Monica.",
            "usable": True,
            "vendible": False,
            "consumible": True,
            "condicion_uso": lambda: False,
            "instruccion_uso": "El regalo que le traje a Monica. Debería agradecerle en persona cuando esté sola.",
            "stock": 0,
            "reposicion": 0,
        },

        # Notebook de Monica — item de quest (se revisa en la habitación del MC)
        "notebook_monica": {
            "nombre": "Notebook de Monica",
            "emoji": "💻",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "La notebook de Monica. Dijo que no le anda, voy a ver si puedo arreglarla.",
            "usable": True,
            "vendible": False,
            "consumible": False,
            "condicion_uso": _item_en_habitacion_mc,
            "instruccion_uso": "Deberia revisarlo en mi habitacion",
            "label_uso": "revisar_notebook_monica",
            "stock": 0,
            "reposicion": 0,
        },

        # Batería NT520 — repuesto para la notebook de Monica (quest 0_c)
        # Aparece en la tienda recién al completar la quest 0_c. 1 unidad, 2 días.
        "bateria_nt520": {
            "nombre": "Bateria NT520",
            "emoji": "🔋",
            "precio": 150,
            "dias_entrega": 2,
            "descripcion": "Una batería nueva para la notebook de Monica.",
            "usable": True,
            "vendible": True,
            "consumible": False,
            "condicion_visible": _bateria_nt520_disponible,
            "condicion_uso": _item_en_habitacion_mc,
            "instruccion_uso": "Deberia hacer esto en mi habitacion",
            "label_uso": "usar_bateria_nt520",
            "stock": 1,
            "reposicion": 0,
        },

        # Quest 0 del MC — cajas de mudanza
        "mis_cosas": {
            "nombre": "Mis cosas",
            "emoji": u"📦",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Las cajas con mis cosas de la mudanza.",
            "usable": False,
            "vendible": False,
            "consumible": True,
            "stock": 0,
            "reposicion": 0,
        },

        # Regalos de bienvenida — se consumen durante la quest 0 de cada NPC
        # (no comprables, no usables; solo reflejan la narrativa de entregarlos)
        "regalo_violet": {
            "nombre": "Regalo Violet",
            "emoji": "🎁",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Un regalo que le traje a Violet.",
            "usable": False,
            "vendible": False,
            "consumible": True,
            "stock": 0,
            "reposicion": 0,
        },
        "regalo_jasmine": {
            "nombre": "Regalo Jasmine",
            "emoji": "🎁",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Un regalo que le traje a Jasmine.",
            "usable": False,
            "vendible": False,
            "consumible": True,
            "stock": 0,
            "reposicion": 0,
        },

        # Items de quest (no comprables, se obtienen durante quests)
        "jabon_quest": {
            "nombre": "Jabon",
            "emoji": "🧼",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Un jabón que encontré en el baño",
            "usable": True,
            "vendible": False,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Podría intentar ayudar a Violet con esto",
            "consumible": False,
            "stock": 0,
            "reposicion": 0,
        },
        "aceite_quest": {
            "nombre": "Aceite",
            "emoji": "🫗",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Un aceite que encontré en la cocina",
            "usable": True,
            "vendible": False,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Podría intentar ayudar a Violet con esto",
            "consumible": False,
            "stock": 0,
            "reposicion": 0,
        },
        "silicona_quest": {
            "nombre": "Silicona",
            "emoji": "🧴",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Silicona que encontré en el garage",
            "usable": True,
            "vendible": False,
            "condicion_uso": lambda: False,
            "instruccion_uso": "Podría intentar ayudar a Violet con esto",
            "consumible": False,
            "stock": 0,
            "reposicion": 0,
        },

        # Quest items — no comprables
        "mangas_violet_mc": {
            "nombre": "Mangas de Violet",
            "emoji": "📚",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Las mangas de Violet. Debería leerlas en mi habitación.",
            "usable": True,
            "vendible": False,
            "consumible": False,
            "condicion_uso": lambda: (
                hasattr(store, 'sistema_locaciones') and
                store.sistema_locaciones.locacion_actual and
                store.sistema_locaciones.locacion_actual.id == "casa_hmc"
            ),
            "instruccion_uso": "Debería estar en mi habitación para leer más tranquilo",
            "label_uso": "usar_mangas_violet_mc",
            "stock": 0,
            "reposicion": 0,
        },

        "mangas_violet": {
            "nombre": "Mangas para Violet",
            "emoji": "📦",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Un paquete con mangas para Violet",
            "usable": True,
            "vendible": False,
            "consumible": False,
            "condicion_uso": lambda: (
                hasattr(store, 'sistema_locaciones') and
                store.sistema_locaciones.locacion_actual and
                store.sistema_locaciones.locacion_actual.id == "casa_hmc"
            ),
            "instruccion_uso": "Si voy a abrirlo debería estar en mi habitación",
            "label_uso": "usar_mangas_violet",
            "stock": 0,
            "reposicion": 0,
        },

        "tanga_violet": {
            "nombre": "Tanga de Violet",
            "emoji": "🩲",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "La tanga de Violet",
            "usable": True,
            "vendible": False,
            "consumible": False,
            "condicion_uso": lambda: (
                hasattr(store, 'sistema_locaciones') and
                store.sistema_locaciones.locacion_actual and
                store.sistema_locaciones.locacion_actual.id == "casa_hmc"
            ),
            "instruccion_uso": "No debo sacar esto acá",
            "label_uso": "usar_tanga_violet",
            "stock": 0,
            "reposicion": 0,
        },

        "elementos_limpieza": {
            "nombre": "Elementos de Limpieza",
            "emoji": "🧹",
            "precio": 0,
            "dias_entrega": 0,
            "descripcion": "Elementos para limpiar el pasillo.",
            "usable": False,
            "vendible": False,
            "stock": 0,
            "reposicion": 0,
        },
    }


################################################################################
## Funciones de utilidad para items
################################################################################

init python:
    
    def obtener_item_info(item_id):
        """
        Obtiene la información de un item.
        
        Args:
            item_id: ID del item
        
        Returns:
            dict: Info del item o None si no existe
        """
        return CATALOGO_ITEMS.get(item_id, None)
    
    def obtener_precio_item(item_id):
        """Obtiene el precio de un item."""
        item = obtener_item_info(item_id)
        return item["precio"] if item else 0
    
    def obtener_dias_entrega_item(item_id):
        """Obtiene los días de entrega de un item."""
        item = obtener_item_info(item_id)
        return item.get("dias_entrega", 1) if item else 1
    
    def obtener_todos_los_items():
        """Retorna lista de todos los IDs de items."""
        return list(CATALOGO_ITEMS.keys())
    
    def obtener_items_por_precio(max_precio):
        """Retorna items con precio menor o igual al especificado."""
        return {k: v for k, v in CATALOGO_ITEMS.items() if v["precio"] <= max_precio}

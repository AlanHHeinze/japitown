################################################################################
## Catálogo de Items - Sistema de Compras
################################################################################
## Definición de todos los items disponibles para comprar
## Agregar nuevos items es simple: solo agregar una entrada al diccionario

init python:
    
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
            "precio": 200,
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

################################################################################
## Sistema de Talk — Core
################################################################################

init python:

    OPCIONES_BASE_IDS = ["complacerla", "provocarla", "escucharla", "hablarle", "adularla"]

    OPCIONES_BASE_TEXTO = {
        "complacerla": "Complacerla",
        "provocarla":  "Provocarla",
        "escucharla":  "Escucharla",
        "hablarle":    "Hablarle",
        "adularla":    "Adularla",
    }

    # Mapeo resultado_id → (stat, cantidad)
    RESULTADO_A_STAT = {
        "+1_amor":  ("amor",  1),
        "+2_amor":  ("amor",  2),
        "+4_amor":  ("amor",  4),
        "+1_deseo": ("deseo", 1),
        "+2_deseo": ("deseo", 2),
        "-2_amor":  ("amor", -2),
        "-1_deseo": ("deseo", -1),
        "nada":     None,
    }

    RESULTADO_TEXTO = {
        "+1_amor":  "+1 amor ❤️",
        "+2_amor":  "+2 amor ❤️",
        "+4_amor":  "+4 amor ❤️",
        "+1_deseo": "+1 deseo 💋",
        "+2_deseo": "+2 deseo 💋",
        "-2_amor":  "-2 amor ❤️",
        "-1_deseo": "-1 deseo 💋",
        "nada":     "sin efecto",
    }

    _TALK_HORARIO_NOMBRES = {
        0: "mañana",
        1: "tarde",
        2: "noche",
        3: "trasnoche",
    }

    _TALK_LOCACIONES_NOMBRES = {
        "casa_frente":        "el frente",
        "casa_living":        "el living",
        "casa_cocina":        "la cocina",
        "casa_comedor":       "el comedor",
        "casa_patio":         "el patio",
        "casa_pasilloabajo":  "el pasillo de abajo",
        "casa_pasilloarriba": "el pasillo de arriba",
        "casa_gym":           "el gym",
        "casa_sotano":        "el sótano",
        "casa_altillo":       "el altillo",
        "casa_garage":        "el garage",
        "casa_banioabajo":    "el baño de abajo",
        "casa_banioarriba":   "el baño de arriba",
        "casa_baniomonica":   "el baño de Mónica",
    }

    _TALK_HABITACIONES_DUENO = {
        "casa_hmonica":  "monica",
        "casa_hviolet":  "violet",
        "casa_hjasmine": "jasmine",
    }

    _TALK_HORARIO_NOMBRES_EN = {
        0: "morning",
        1: "afternoon",
        2: "night",
        3: "late night",
    }

    _TALK_LOCACIONES_NOMBRES_EN = {
        "casa_frente":        "the front of the house",
        "casa_living":        "the living room",
        "casa_cocina":        "the kitchen",
        "casa_comedor":       "the dining room",
        "casa_patio":         "the patio",
        "casa_pasilloabajo":  "the downstairs hallway",
        "casa_pasilloarriba": "the upstairs hallway",
        "casa_gym":           "the gym",
        "casa_sotano":        "the basement",
        "casa_altillo":       "the attic",
        "casa_garage":        "the garage",
        "casa_banioabajo":    "the downstairs bathroom",
        "casa_banioarriba":   "the upstairs bathroom",
        "casa_baniomonica":   "Mónica's bathroom",
    }

    # (npc_id, resultado_id) → (b_attr, o_attr)
    _TALK_EXPRESION_FACIAL = {
        ("violet",  "+2_amor"):  ("b_feliz",    "o_felices"),
        ("violet",  "+1_deseo"): ("b_sexy",     "o_sexys"),
        ("violet",  "-2_amor"):  ("b_aburrida", "o_enojados"),
        ("violet",  "-1_deseo"): ("b_aburrida", "o_enojados"),
        ("monica",  "+2_amor"):  ("b_feliz",    "o_felicesnm"),
        ("monica",  "+1_deseo"): ("b_sexy",     "o_sexysnm"),
        ("monica",  "-2_amor"):  ("b_enojada",  "o_enojadosnm"),
        ("monica",  "-1_deseo"): ("b_enojada",  "o_enojadosnm"),
        ("jasmine", "+2_amor"):  ("b_feliz",    "o_sexysnm"),
        ("jasmine", "+1_deseo"): ("b_sexy",     "o_sexysnm"),
        ("jasmine", "-2_amor"):  ("b_aburrida", "o_enojadosnm"),
        ("jasmine", "-1_deseo"): ("b_aburrida", "o_enojadosnm"),
    }

    # skin_id → (imagen_layered, c_neutral, c_caliente)
    _TALK_SKIN_CUERPO = {
        "violet_base_base":                ("violet_parada",           "c_rbase_base",  "c_rbase_dedolabio"),
        "violet_pijama_base":              ("violet_parada",           "c_pijama_base", "c_pijama_base"),
        "monica_base_base":                ("monica_parada",            "c_rbase_base",  "c_rbase_dedolabio"),
        "monica_bikini_base":              ("monica_parada",            "c_rbase_base",  "c_rbase_dedolabio"),
        "jasmine_base_base":               ("jasmine_parada",           "c_rbase_base",  "c_rbase_dedolabio"),
        "jasmine_bikini_base":             ("jasmine_parada",           "c_rbase_base",  "c_rbase_dedolabio"),
        "jasmine_entrenamiento_base":      ("jasmine_parada",           "c_rbase_base",  "c_rbase_dedolabio"),
        "jasmine_entrenamiento_deportiva": ("jasmine_paradadeportiva",  "c_base",        "c_expectativa"),
    }


    class EstadoTalkActivo:
        """Rastrea un estado especial activo con su propio contador de días."""
        def __init__(self, estado_id, jerarquia, dias_restantes):
            self.id = estado_id
            self.jerarquia = jerarquia
            self.dias_restantes = dias_restantes
            self.consumido = False


    class EstadoTalk:
        """
        Estado del NPC que determina cómo responde a cada opción de talk.

        efectos: dict opcion_id → resultado_id
            Ej: {"complacerla": "-2_amor", "hablarle": "+2_amor", ...}
            Cada estado distribuye los 5 resultados posibles entre las 5 opciones.

        estados_posteriores: dict resultado_id → estado_id
            Estado que se asigna al NPC tras la interacción (para otros sistemas).

        es_especial: si True, tiene jerarquía y contador de dias.
        """
        def __init__(self, id, nombre, intro, efectos, mensaje,
                    es_especial=False, jerarquia=0, dias_duracion=1,
                    estados_posteriores=None, condicion=None):
            self.id = id
            self.nombre = nombre
            self.intro = intro              # Narración mostrada antes del menú
            self.es_especial = es_especial
            self.jerarquia = jerarquia
            self.dias_duracion = dias_duracion
            self.efectos = efectos
            self.mensaje = mensaje
            self.estados_posteriores = estados_posteriores or {}
            self.condicion = condicion      # callable → bool; None = siempre disponible

        def obtener_resultado(self, opcion_id):
            return self.efectos.get(opcion_id, "nada")


    class OpcionEspecialTalk:
        """
        Opción adicional de talk disponible bajo condiciones específicas.
        Puede requerir un ítem, provenir de una quest, evento, etc.

        Los callables (condicion, recompensa_extra) se excluyen del pickle
        para no crashear al guardar durante una interacción de talk.
        Como este objeto solo vive en sistema_talk (define), se reconstruye
        correctamente en cada inicio de sesión.
        """
        def __init__(self, id, texto, condicion, mensaje_opcion,
                    resultado_id=None, item_requerido=None, item_consumible=False,
                    estado_posterior_npc=None, recompensa_extra=None):
            self.id = id
            self.texto = texto
            self.condicion = condicion          # callable → bool
            self.mensaje_opcion = mensaje_opcion
            self.resultado_id = resultado_id    # resultado_id o None si no modifica stats
            self.item_requerido = item_requerido
            self.item_consumible = item_consumible
            self.estado_posterior_npc = estado_posterior_npc
            self.recompensa_extra = recompensa_extra  # callable, para disparadores futuros

        def __getstate__(self):
            state = self.__dict__.copy()
            # Los callables no son serializables — se excluyen del save.
            # Como este objeto vive en sistema_talk (define), se recrea al inicio.
            state['condicion'] = None
            state['recompensa_extra'] = None
            return state

        def __setstate__(self, state):
            self.__dict__.update(state)

        def esta_disponible(self):
            if not self.condicion:
                return False
            try:
                return bool(self.condicion())
            except Exception:
                return False


    class ConfigTalkNPC:
        """
        Configuración completa del sistema de talk para un NPC.

        mensaje_general   — parte 1: texto fijo que aparece siempre.
        mensajes_opciones — parte 2: un texto por opción base elegida.
        estados           — lista de EstadoTalk (generales + especiales).
        estados_generales_ids — IDs que se asignan aleatoriamente al despertar.
        opciones_especiales   — lista de OpcionEspecialTalk.
        resoluciones          — parte 4: un texto por resultado_id.
        resoluciones_especiales — parte 4 alternativa: texto por opcion_especial.id.
        """
        def __init__(self, npc_id, mensaje_general, mensajes_opciones, resoluciones,
                    estados=None, estados_generales_ids=None,
                    opciones_especiales=None, resoluciones_especiales=None):
            self.npc_id = npc_id
            self.mensaje_general = mensaje_general
            self.mensajes_opciones = mensajes_opciones
            self.resoluciones = resoluciones
            self.resoluciones_especiales = resoluciones_especiales or {}
            self._estados = {e.id: e for e in (estados or [])}
            self.estados_generales_ids = estados_generales_ids or []
            self.opciones_especiales = opciones_especiales or []

        def obtener_estado(self, estado_id):
            return self._estados.get(estado_id)

        def obtener_opciones_especiales_disponibles(self):
            return [o for o in self.opciones_especiales if o.esta_disponible()]


    class SistemaTalk:
        """Gestor central del sistema de talk."""

        def __init__(self):
            self._configs = {}

        def registrar_config(self, config):
            self._configs[config.npc_id] = config

        def obtener_config(self, npc_id):
            return self._configs.get(npc_id)

        # ------------------------------------------------------------------
        # Estados generales

        def asignar_estado_aleatorio(self, npc_id):
            """Asigna un estado general aleatorio. Llamar al despertar."""
            config = self.obtener_config(npc_id)
            npc = store.sistema_npcs.obtener_npc(npc_id)
            if not config or not npc or not config.estados_generales_ids:
                return
            disponibles = []
            for estado_id in config.estados_generales_ids:
                estado = config.obtener_estado(estado_id)
                condicion = getattr(estado, 'condicion', None) if estado else None
                if condicion is None or condicion():
                    disponibles.append(estado_id)
            if not disponibles:
                return
            estado_id = renpy.random.choice(disponibles)
            npc.talk_estado_id = estado_id

        # ------------------------------------------------------------------
        # Estados especiales

        def activar_estado_especial(self, npc_id, estado_id, dias_duracion=None):
            """
            Activa un estado especial en el NPC con efecto inmediato.
            Puede llamarse desde quests, eventos, items, o cualquier label.
            Si el estado ya está activo, reinicia su contador.
            """
            config = self.obtener_config(npc_id)
            npc = store.sistema_npcs.obtener_npc(npc_id)
            if not config or not npc:
                return
            estado = config.obtener_estado(estado_id)
            if not estado or not estado.es_especial:
                return
            dias = dias_duracion if dias_duracion is not None else estado.dias_duracion
            if not hasattr(npc, 'talk_estados_especiales'):
                npc.talk_estados_especiales = []
            # Reemplazar si ya existe
            npc.talk_estados_especiales = [
                e for e in npc.talk_estados_especiales if e.id != estado_id
            ]
            npc.talk_estados_especiales.append(
                EstadoTalkActivo(estado_id, estado.jerarquia, dias)
            )

        def obtener_estado_activo(self, npc_id):
            """
            Retorna el EstadoTalk activo.
            Prioridad: estado especial de mayor jerarquía > estado general.
            Si no hay estado, asigna uno aleatorio como fallback.
            """
            config = self.obtener_config(npc_id)
            npc = store.sistema_npcs.obtener_npc(npc_id)
            if not config or not npc:
                return None

            especiales = getattr(npc, 'talk_estados_especiales', [])
            if especiales:
                mejor = max(especiales, key=lambda e: e.jerarquia)
                return config.obtener_estado(mejor.id)

            estado_id = getattr(npc, 'talk_estado_id', None)
            if estado_id:
                return config.obtener_estado(estado_id)

            # Fallback: asignar estado ahora
            self.asignar_estado_aleatorio(npc_id)
            estado_id = getattr(npc, 'talk_estado_id', None)
            return config.obtener_estado(estado_id) if estado_id else None

        def decrementar_estados_especiales(self, npc_id):
            """Decrementa contadores de estados especiales al dormir."""
            npc = store.sistema_npcs.obtener_npc(npc_id)
            if not npc:
                return
            if not hasattr(npc, 'talk_estados_especiales'):
                npc.talk_estados_especiales = []
                return
            for e in npc.talk_estados_especiales:
                if getattr(e, 'consumido', False):
                    e.dias_restantes = 0
                else:
                    e.dias_restantes -= 1
            npc.talk_estados_especiales = [
                e for e in npc.talk_estados_especiales if e.dias_restantes > 0
            ]

        def consumir_estado_especial(self, npc_id):
            """Marca el estado especial activo como consumido. Se eliminará al dormir."""
            npc = store.sistema_npcs.obtener_npc(npc_id)
            if not npc:
                return
            especiales = getattr(npc, 'talk_estados_especiales', [])
            if especiales:
                mejor = max(especiales, key=lambda e: e.jerarquia)
                mejor.consumido = True

        # ------------------------------------------------------------------
        # Post-interacción

        def asignar_estado_posterior(self, npc_id, resultado_id, estado_activo, opcion_especial=None):
            """
            Asigna el estado posterior al NPC tras la interacción.
            Prioridad: opcion_especial.estado_posterior_npc > estado_activo.estados_posteriores.
            """
            npc = store.sistema_npcs.obtener_npc(npc_id)
            if not npc:
                return
            if not hasattr(npc, 'estado_posterior_id'):
                npc.estado_posterior_id = None
            posterior_id = None
            if opcion_especial and opcion_especial.estado_posterior_npc:
                posterior_id = opcion_especial.estado_posterior_npc
            elif estado_activo and resultado_id:
                posterior_id = estado_activo.estados_posteriores.get(resultado_id)
            npc.estado_posterior_id = posterior_id

        # ------------------------------------------------------------------
        # Memoria del MC

        def actualizar_memoria_mc(self, npc_id, estado_id, opcion_id, resultado_id):
            """
            Guarda la interacción en la memoria del MC.
            Límite: mc_inteligencia entradas por NPC.
            """
            if not hasattr(store, 'talk_memoria'):
                store.talk_memoria = {}
            if npc_id not in store.talk_memoria:
                store.talk_memoria[npc_id] = []
            limite = max(1, getattr(store, 'mc_inteligencia', 1))
            # Remover entrada previa para este (estado, opcion)
            store.talk_memoria[npc_id] = [
                e for e in store.talk_memoria[npc_id]
                if not (e["estado"] == estado_id and e["opcion"] == opcion_id)
            ]
            store.talk_memoria[npc_id].insert(0, {
                "estado": estado_id,
                "opcion": opcion_id,
                "resultado": resultado_id,
            })
            store.talk_memoria[npc_id] = store.talk_memoria[npc_id][:limite]

        def consultar_memoria_mc(self, npc_id, estado_id, opcion_id):
            """Retorna el resultado_id recordado para (npc, estado, opción) o None."""
            if not hasattr(store, 'talk_memoria'):
                return None
            for e in store.talk_memoria.get(npc_id, []):
                if e["estado"] == estado_id and e["opcion"] == opcion_id:
                    return e["resultado"]
            return None


define sistema_talk = SistemaTalk()
default talk_memoria = {}


init python:

    def activar_estado_especial_npc(npc_id, estado_id, dias_duracion=None):
        """Helper accesible desde quests, eventos, items, o cualquier label."""
        if hasattr(store, 'sistema_talk'):
            store.sistema_talk.activar_estado_especial(npc_id, estado_id, dias_duracion)

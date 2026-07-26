################################################################################
## Sistema de Quests del MC
################################################################################
## Las quests del MC son independientes del sistema de NPCs: no tienen etapas
## de espera/condiciones/rutina ni stats de relacion. Son objetivos propios
## del protagonista que se muestran en el panel de Pistas bajo su propia seccion.

init python:
    class QuestMC:
        """Quest propia del MC, independiente del sistema de NPCs."""

        def __init__(self, id, nombre, pista, locaciones_pendientes=None,
            que_hacer_fn=None, condicion_completada=None, siguiente_quest_id=None):
            """
            id:                    ID unico de la quest.
            nombre:                Nombre visible en el panel de pistas.
            pista:                 Texto de pista (str o callable → str).
            locaciones_pendientes: Lista de strings visibles que se van retirando.
            que_hacer_fn:          callable → str. Si se provee, reemplaza
                la generacion basada en locaciones_pendientes.
            condicion_completada:  callable → bool. Si retorna True, la quest
                se completa automaticamente al llamar a actualizar().
            siguiente_quest_id:    ID de la quest MC que se inicia al completar esta.
            """
            self.id = id
            self.nombre = nombre
            self._pista = pista
            self.locaciones_pendientes = list(locaciones_pendientes) if locaciones_pendientes else []
            self._que_hacer_fn = que_hacer_fn
            self._condicion_completada = condicion_completada
            self.siguiente_quest_id = siguiente_quest_id
            self.activa = False
            self.completada = False
            # dias_totales del día en que se completó (None si todavía no).
            # Lo usan las quests que deben esperar al día siguiente de completarse
            # otra (ej. la 01_a de Violet espera a mc_quest_1 para traer el paquete).
            self.dia_completada = None

        def _traducir(self, valor):
            """
            Traduce el texto resuelto. Mismo criterio que ConfigEtapa._resolver en
            questsystem_core: la traduccion se aplica ACA y no en el panel de Pistas,
            asi cualquier consumidor recibe el texto ya traducido.
            """
            if valor and isinstance(valor, str):
                try:
                    return renpy.translate_string(valor)
                except Exception:
                    pass
            return valor

        def obtener_pista(self):
            valor = self._pista if isinstance(self._pista, str) else self._pista()
            return self._traducir(valor)

        def obtener_que_hacer(self):
            if self._que_hacer_fn:
                return self._traducir(self._que_hacer_fn())

            items = [self._traducir(i) for i in self.locaciones_pendientes]
            if not items:
                return renpy.translate_string("Has recorrido toda la casa.")

            # La lista se COMPONE, asi que se traducen las piezas por separado:
            # la plantilla "Visitar: {lista}", el conector " y " y cada nombre.
            if len(items) == 1:
                lista = items[0]
            else:
                lista = ", ".join(items[:-1]) + renpy.translate_string(" y ") + items[-1]
            return renpy.translate_string("Visitar: {lista}").format(lista=lista)

        def marcar_locacion_visitada(self, nombre_locacion):
            """Retira una locacion de la lista pendiente al ser visitada."""
            if nombre_locacion in self.locaciones_pendientes:
                self.locaciones_pendientes.remove(nombre_locacion)

        def verificar_condicion_completada(self):
            """Retorna True si la condicion de completado se cumple."""
            if self._condicion_completada:
                return self._condicion_completada()
            return False

    class SistemaQuestsMC:
        """Gestor de quests propias del MC."""

        def __init__(self):
            self.quests = {}
            self._quest_activa_id = None

        def registrar(self, quest):
            self.quests[quest.id] = quest

        def iniciar(self, quest_id):
            q = self.quests.get(quest_id)
            if q and not q.activa and not q.completada:
                q.activa = True
                self._quest_activa_id = quest_id

        def obtener_activa(self):
            if self._quest_activa_id:
                return self.quests.get(self._quest_activa_id)
            return None

        def completar_activa(self):
            q = self.obtener_activa()
            if q:
                q.activa = False
                q.completada = True
                q.dia_completada = getattr(store, 'dias_totales', 1)
                self._quest_activa_id = None
                # Auto-iniciar la siguiente quest del MC si está definida
                if q.siguiente_quest_id:
                    self.iniciar(q.siguiente_quest_id)

        def actualizar(self):
            """Verifica si la quest activa cumple su condicion de completado."""
            q = self.obtener_activa()
            if q and q.verificar_condicion_completada():
                self.completar_activa()


# Instancia creada en init 4 (los registros de init 5-11 la llenan) y declarada
# con default para que se guarde en el save: el progreso vive dentro del sistema y debe guardarse.
init 4 python:
    sistema_quests_mc = SistemaQuestsMC()
# OJO: el default se re-evalúa en CADA partida nueva. Debe devolver una COPIA
# del catálogo poblado en init — una instancia vacía (SistemaQuestsMC()) borraría todo
# el contenido registrado. Ver _ps_copia_fresca en persistencia_sistemas.rpy.
default sistema_quests_mc = _ps_copia_fresca("sistema_quests_mc")


################################################################################
## Quest 0 — De nuevo en casa
################################################################################

init python:

    # Quests finales de cada NPC que liberan la quest 1 del MC.
    _MC_Q1_QUESTS_REQUERIDAS = {
        "monica_questprincipal_0_c":  "La batería de la notebook (Mónica)",
        "violet_questprincipal_0_b":  "¿Que le pasa a Violet? (Violet)",
        "jasmine_questprincipal_0_c": "Reencuentro con Jasmine (Jasmine)",
    }

    def _mc_q1_que_hacer():
        """Genera la lista de quests de NPC pendientes de completar."""
        # La lista se COMPONE, asi que cada nombre de quest y la cabecera se
        # traducen por separado: el texto ya armado nunca matchearia un `old`.
        pendientes = []
        for qid, label in _MC_Q1_QUESTS_REQUERIDAS.items():
            q = store.sistema_quests.obtener_quest(qid)
            if not (q and q.completada):
                pendientes.append(renpy.translate_string(label))
        if not pendientes:
            return renpy.translate_string("¡Todas completadas!")
        return renpy.translate_string("Completar:") + "\n" + "\n".join(pendientes)

    def _mc_q1_condicion_completada():
        """True cuando las 3 quests finales de los NPC están completas."""
        for qid in _MC_Q1_QUESTS_REQUERIDAS:
            q = store.sistema_quests.obtener_quest(qid)
            if not (q and q.completada):
                return False
        return True


init 5 python:
    _quest_mc_0 = QuestMC(
        id="mc_quest_0",
        nombre="De nuevo en casa",
        pista="Recorrer la casa",
        # Deben coincidir con MC_Q0_OBJETIVOS (mc_quest_0_a.rpy): se van retirando
        # via mc_q0_registrar_exploracion() al entrar a cada una.
        locaciones_pendientes=["Pasillo arriba", "Pasillo abajo", "Patio"],
        siguiente_quest_id="mc_quest_0b",
    )
    sistema_quests_mc.registrar(_quest_mc_0)

    _quest_mc_0b = QuestMC(
        id="mc_quest_0b",
        nombre="App de Pistas",
        pista="Revisar el celular y la app de pistas",
        siguiente_quest_id="mc_quest_1",
    )
    sistema_quests_mc.registrar(_quest_mc_0b)

    _quest_mc_1 = QuestMC(
        id="mc_quest_1",
        nombre="Reencuentro",
        pista="Tengo que ponerme al día con Monica, Jasmine y Violet",
        que_hacer_fn=_mc_q1_que_hacer,
        condicion_completada=_mc_q1_condicion_completada,
    )
    sistema_quests_mc.registrar(_quest_mc_1)

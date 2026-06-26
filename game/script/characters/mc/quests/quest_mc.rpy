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

        def obtener_pista(self):
            return self._pista if isinstance(self._pista, str) else self._pista()

        def obtener_que_hacer(self):
            if self._que_hacer_fn:
                return self._que_hacer_fn()
            items = self.locaciones_pendientes
            if not items:
                return "Has recorrido toda la casa."
            if len(items) == 1:
                return "Visitar: " + items[0]
            return "Visitar: " + ", ".join(items[:-1]) + " y " + items[-1]

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
                self._quest_activa_id = None
                # Auto-iniciar la siguiente quest del MC si está definida
                if q.siguiente_quest_id:
                    self.iniciar(q.siguiente_quest_id)

        def actualizar(self):
            """Verifica si la quest activa cumple su condicion de completado."""
            q = self.obtener_activa()
            if q and q.verificar_condicion_completada():
                self.completar_activa()


define sistema_quests_mc = SistemaQuestsMC()


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
        pendientes = []
        for qid, label in _MC_Q1_QUESTS_REQUERIDAS.items():
            q = store.sistema_quests.obtener_quest(qid)
            if not (q and q.completada):
                pendientes.append(label)
        if not pendientes:
            return "¡Todas completadas!"
        return "Completar:\n" + "\n".join(pendientes)

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
        locaciones_pendientes=["Living", "Pasillo Abajo", "Cocina", "Patio", "Pasillo Arriba"],
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

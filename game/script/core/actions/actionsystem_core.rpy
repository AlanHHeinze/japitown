################################################################################
## Sistema de Acciones de Locación — Core
################################################################################
## Las AccionLocacion definen qué puede hacer el jugador en cada locación
## (cocinar, ver TV, entrenar, etc.). Los ListenerAccion permiten que quests
## y eventos intercepten esas acciones y disparen sus propios labels.

init python:

    class AccionLocacion(object):
        """
        Una acción disponible para el jugador en una locación específica.
        """
        def __init__(self, id, nombre, icono, locacion_id,
                     label_generico=None, reseteo="diario",
                     condicion=None, mensaje_reintento=None,
                     color="#0288D1", color_hover="#4FC3F7"):
            self.id = id
            self.nombre = nombre
            self.icono = icono
            self.locacion_id = locacion_id
            self.label_generico = label_generico      # Label si no hay listeners
            self.reseteo = reseteo                    # "diario" | "semanal_lunes" | None
            self._condicion = condicion               # callable → bool (visibilidad extra)
            # Si es None: button insensitive cuando usada
            # Si es str: button siempre clickeable, muestra piensa cuando ya usada
            self.mensaje_reintento = mensaje_reintento
            self.color = color
            self.color_hover = color_hover

        def esta_visible(self):
            if self._condicion is None:
                return True
            return self._condicion()

        def __getstate__(self):
            d = self.__dict__.copy()
            d['_condicion'] = None
            return d


    class ListenerAccion(object):
        """
        Registrado por una quest o evento para interceptar una AccionLocacion.
        Cuando la acción se ejecuta y el listener es válido, llama a su label.
        """
        def __init__(self, accion_id, label, nombre_menu,
                     prioridad="quest", condicion=None, unico=True):
            self.accion_id = accion_id      # Qué acción intercepta
            self.label = label              # Label a ejecutar
            self.nombre_menu = nombre_menu  # Texto en el menú de elección (si hay conflicto)
            self.prioridad = prioridad      # "quest" | "evento" | "generico"
            self._condicion = condicion     # callable → bool adicional
            self.unico = unico             # Auto-remove al dispararse

        def es_valido(self):
            if self._condicion is None:
                return True
            return self._condicion()

        def __getstate__(self):
            d = self.__dict__.copy()
            d['_condicion'] = None
            return d


    _AL_PRIORIDAD = {"quest": 0, "evento": 1, "generico": 2}


    class SistemaAcciones(object):

        def __init__(self):
            self.acciones = {}          # {accion_id: AccionLocacion}
            self.listeners = []         # [ListenerAccion]
            self._usados_hoy = set()    # IDs usados hoy (reset en dormir)
            self._usados_semana = set() # IDs usados esta semana (reset el lunes)

        def registrar_accion(self, accion):
            self.acciones[accion.id] = accion

        def registrar_listener(self, listener):
            self.listeners.append(listener)

        def remover_listener(self, accion_id, label=None):
            self.listeners = [
                l for l in self.listeners
                if not (l.accion_id == accion_id and (label is None or l.label == label))
            ]

        def obtener_acciones_locacion(self, locacion_id):
            return [
                a for a in self.acciones.values()
                if a.locacion_id == locacion_id and a.esta_visible()
            ]

        def esta_disponible(self, accion_id):
            if not hasattr(self, '_usados_hoy'):
                self._usados_hoy = set()
            if not hasattr(self, '_usados_semana'):
                self._usados_semana = set()
            accion = self.acciones.get(accion_id)
            if accion is None:
                return False
            if not accion.esta_visible():
                return False
            if accion.reseteo == "diario" and accion_id in self._usados_hoy:
                return False
            if accion.reseteo == "semanal_lunes" and accion_id in self._usados_semana:
                return False
            return True

        def preparar_ejecucion(self, accion_id):
            """Retorna los listeners válidos para la acción, ordenados por prioridad."""
            validos = [
                l for l in self.listeners
                if l.accion_id == accion_id and l.es_valido()
            ]
            validos.sort(key=lambda l: _AL_PRIORIDAD.get(l.prioridad, 99))
            return validos

        def post_ejecutar(self, accion_id, listener):
            """Marca la acción como usada y limpia el listener si es unico."""
            self.marcar_usada(accion_id)
            if listener and listener.unico:
                self.listeners = [l for l in self.listeners if l is not listener]

        def marcar_usada(self, accion_id):
            if not hasattr(self, '_usados_hoy'):
                self._usados_hoy = set()
            if not hasattr(self, '_usados_semana'):
                self._usados_semana = set()
            accion = self.acciones.get(accion_id)
            if accion:
                if accion.reseteo == "diario":
                    self._usados_hoy.add(accion_id)
                elif accion.reseteo == "semanal_lunes":
                    self._usados_semana.add(accion_id)

        def resetear_diario(self):
            self._usados_hoy = set()

        def resetear_semanal(self):
            self._usados_semana = set()


# Instancia global
define sistema_acciones = SistemaAcciones()

# Variable temporal para pasar el ID de acción al label ejecutor
default _accion_locacion_temp_id = None

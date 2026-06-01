################################################################################
## Sistema de Elementos Posicionables — Stub mínimo
################################################################################
## El sistema de posicionamiento complejo fue reemplazado por la herramienta
## herramienta_pos_simple (activar/desactivar con la tecla P en modo debug).
##
## Este stub provee el objeto sistema_pos con métodos no-op para que las
## pantallas de quest que lo referencian no fallen en tiempo de ejecución.

init -1 python:

    class _SistemaPosStub:
        def obtener(self, elem_id):
            return None
        def obtener_por_grupo(self, grupo):
            return []
        def todos_editables(self):
            return []
        def registrar(self, *args, **kwargs):
            pass
        def actualizar_posicion(self, *args, **kwargs):
            pass
        def obtener_screens_disponibles(self):
            return []
        def obtener_por_screen(self, screen):
            return []
        def tomar_snapshot(self):
            pass

    sistema_pos = _SistemaPosStub()

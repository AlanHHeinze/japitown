################################################################################
## Sistema de Desbloqueos por Relación
################################################################################
## Cada NPC registra su lista de desbloqueos en su definition_*.rpy usando
## npc.agregar_desbloqueo(stat, umbral, icono, nombre, desc).
## Este archivo provee las funciones de consulta usadas por el screen de Relaciones.

init python:

    def obtener_desbloqueos_stat(npc_id, stat):
        """
        Retorna (desbloqueados, bloqueados) para un NPC y stat dado,
        ordenados por umbral ascendente.

        Soporta condicion_extra: callable adicional que debe ser True para desbloquear.
        Mientras condicion_extra falla, el ítem muestra nombre_pendiente en su lugar.
        """
        npc = obtener_npc(npc_id)
        if not npc:
            return [], []
        stat_actual = npc.obtener_estado(stat, 0)
        todos = sorted(
            [d for d in getattr(npc, "desbloqueos", []) if d["stat"] == stat],
            key=lambda d: d["umbral"]
        )
        desbloqueados = []
        bloqueados    = []
        for d in todos:
            condicion_extra = d.get("condicion_extra")
            extra_ok = condicion_extra() if condicion_extra else True
            stat_ok  = stat_actual >= d["umbral"]

            if extra_ok and stat_ok:
                desbloqueados.append(d)
            else:
                item = dict(d)
                if not extra_ok and d.get("nombre_pendiente"):
                    item["nombre"] = d["nombre_pendiente"]
                bloqueados.append(item)
        return desbloqueados, bloqueados

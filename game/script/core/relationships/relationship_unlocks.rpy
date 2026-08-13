################################################################################
## Consulta de Hitos para el panel de Relaciones
################################################################################
## Capa fina entre el sistema de Hitos (core/hitos/) y el screen de Relaciones.
##
## ANTES: este archivo consultaba `npc.desbloqueos`, una lista de carteles que
## cada NPC declaraba con agregar_desbloqueo() y que NO estaba conectada a nada.
## Los umbrales vivian ahi Y ademas en el sistema que realmente decidia (la vieja
## TABLA_ACCESO_HABITACION), asi que se desfasaron: el panel prometia ingreso a
## la habitacion con amor 30 cuando la tabla pedia 50.
##
## AHORA lee los Hitos, que son la fuente de verdad de lo que el jugador tiene
## habilitado. El panel no puede volver a mentir porque mira exactamente lo mismo
## que consultan las puertas y el resto de los sistemas.
##
## El contrato de la funcion NO cambia: devuelve (desbloqueados, bloqueados) con
## dicts que traen "icono", "nombre", "desc" y "umbral", que es lo que dibuja
## _rel_item en ui/hud/hud_relaciones.rpy.

init python:

    def obtener_desbloqueos_stat(npc_id, stat):
        """
        Retorna (desbloqueados, bloqueados) de un NPC para un stat, ordenados
        por umbral ascendente.

        Un hito cuenta como desbloqueado cuando fue ALCANZADO, no cuando el stat
        llega al umbral. La diferencia importa: los hitos son permanentes, asi
        que si el stat baja despues el hito sigue conseguido y el panel lo
        muestra como tal.

        Args:
            npc_id: NPC a consultar
            stat: "amor" o "deseo"

        El nombre y la descripcion salen YA TRADUCIDOS: el catalogo de hitos los
        declara en español y el panel los pinta tal cual, asi que la traduccion
        tiene que pasar por acá. Van por `translate english strings:` (ver
        tl/english/relaciones_strings.rpy) y no por bloques con hash, porque no
        son diálogo sino datos de un objeto.

        Cada hito trae ademas la lista de sus VENTAJAS, que es lo que el panel
        de Desbloqueos muestra indentado debajo. Se arma desde el catalogo
        (VENTAJAS_HITO) en vez de dejar que la screen lo resuelva: asi la UI no
        conoce ninguna ventaja por nombre y una ventaja nueva aparece sola.
        Una ventaja con id inexistente se saltea — ya la reporta
        verificar_coherencia_hitos(), el panel no tiene por que romperse.

        Returns:
            (list[dict], list[dict]) — cada dict con icono/nombre/desc/umbral/id
            y "ventajas": [{"id", "nombre", "desc"}, ...]
        """
        desbloqueados = []
        bloqueados    = []

        for _h in obtener_hitos_npc(npc_id, stat):
            _ventajas = []
            for _vid in _h.ventajas:
                _v = obtener_ventaja(_vid)
                if not _v:
                    continue
                _ventajas.append({
                    "id":     _vid,
                    "nombre": renpy.translate_string(_v["nombre"]),
                    "desc":   renpy.translate_string(_v["descripcion"]) if _v.get("descripcion") else "",
                })

            _item = {
                "icono":    _h.icono,
                "nombre":   renpy.translate_string(_h.nombre),
                "desc":     renpy.translate_string(_h.descripcion) if _h.descripcion else "",
                "umbral":   _h.umbral,
                "id":       _h.id,
                "ventajas": _ventajas,
            }
            if tiene_hito(npc_id, _h.id):
                desbloqueados.append(_item)
            else:
                bloqueados.append(_item)

        return desbloqueados, bloqueados

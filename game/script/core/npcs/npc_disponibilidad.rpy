################################################################################
## Disponibilidad de un NPC — el interruptor general del personaje
################################################################################
## Un NPC NO DISPONIBLE esta fuera de juego: no se lo puede ver, ni hablar, ni
## escribir, ni empezarle una quest, ni meterlo en una accion. Sirve para que el
## contenido no se mezcle — mientras una quest lo tiene ocupado con algo, nada
## mas puede engancharse a el.
##
## LO PRENDE Y LO APAGA EL CONTENIDO:
##
##     $ marcar_npc_no_disponible("violet", "Violet no esta por ahora")
##     $ marcar_npc_disponible("violet")
##
## El motivo es OPCIONAL y se muestra como pensamiento cuando el jugador
## insiste. Sin motivo sale el generico.
##
## ⚠️ QUIEN LO APAGA TIENE QUE VOLVER A PRENDERLO. Un NPC que queda no
## disponible para siempre desaparece del juego: no hay ningun reseteo
## automatico, ni al dormir ni al cargar. Es a proposito — el estado dura lo que
## dure el contenido que lo puso, aunque sean varios dias.
##
##
## DONDE SE APLICA — no hace falta que cada escena pregunte. La disponibilidad
## se consulta en los EMBUDOS que el juego ya tenia, que es lo que hace que
## cubra tambien el contenido que todavia no existe:
##
##   1. `npc_interactuable`      (restriccion_quest_system)
##        → clickearlo. Cubre TODO su menu: talk, besos, juegos nuevos, ropa
##          nueva, botones de quest, ventajas.
##   2. `tracker_locacion_npc`   (hud_tracker)
##        → "¿donde esta?". Devuelve None, o sea que para el resto del juego no
##          esta en ningun lado. Cubre el tracker, el viaje rapido, las puertas,
##          las acciones compartidas (Jugar / Ver Anime / Ver TV) y todas las
##          condiciones de contenido que preguntan por su locacion.
##   3. `quest_lista_para_boton` (questsystem_core)
##        → EL predicado de todo disparador de quest. Con el NPC no disponible
##          ninguna de sus quests puede arrancar ni avanzar de etapa.
##   4. `obtener_locacion_rutina` (npcsystem_core)
##        → las rutinas de QUEST y de EVENTO no se aplican. La rutina base
##          sigue: el NPC tiene que estar en algun lado, simplemente no se lo ve.
##   5. `ChatNPC.puede_responder` y `_intentar_entrega` (messagesystem_core)
##        → ni contesta ni le llegan mensajes nuevos.
##   6. `mensajear_puede_hablar`  (mensajear_system)
##        → tampoco se le puede escribir primero.
##
## QUE NO BLOQUEA, a proposito: los stats, los hitos y el panel de Relaciones.
## Son datos de la ficha, no interaccion — esconderlos confundiria mas de lo que
## aclara.


# {npc_id: motivo}. El motivo puede ser "" si el contenido no quiso dar uno.
# Un id que NO esta en el dict esta disponible: el default es estar.
default npcs_no_disponibles = {}


init -1 python:

    # Lo que piensa el MC al insistir con un NPC que no esta disponible y cuyo
    # contenido no dio un motivo propio.
    NPC_NO_DISPONIBLE_GENERICO = "No es momento para eso"


init python:

    def marcar_npc_no_disponible(npc_id, motivo=None):
        """
        Saca al NPC de juego.

        Args:
            npc_id: a quien.
            motivo: que piensa el MC si insiste. En español; se traduce al
                mostrarlo. None = el generico.
        """
        if not npc_id:
            return
        store.npcs_no_disponibles[npc_id] = motivo or ""

    def marcar_npc_disponible(npc_id):
        """Lo devuelve al juego. Sin efecto si ya estaba disponible."""
        store.npcs_no_disponibles.pop(npc_id, None)

    def npc_disponible(npc_id):
        """
        True si se puede interactuar con este NPC.

        Es la consulta barata que hacen los embudos, asi que no valida nada mas
        — un id inexistente cuenta como disponible y lo rebota quien
        corresponda.
        """
        return npc_id not in getattr(store, 'npcs_no_disponibles', {})

    def motivo_npc_no_disponible(npc_id):
        """
        Motivo YA TRADUCIDO, o None si el NPC esta disponible.

        Lo usa mensaje_npc_bloqueado() para que el jugador que insiste reciba
        una explicacion en vez de un click muerto.
        """
        _motivos = getattr(store, 'npcs_no_disponibles', {})
        if npc_id not in _motivos:
            return None
        return renpy.translate_string(
            _motivos.get(npc_id) or NPC_NO_DISPONIBLE_GENERICO)

################################################################################
## Violet — Deseo 20 · "Pensando en Violet"
################################################################################
##     archivo   violet_deseo_20.rpy
##     quest     violet_deseo_04          (quests_deseo_violet.rpy)
##     grupo     violet_deseo04_chat      (chat/chat_violet.rpy)
##
## LA QUEST ENTERA PASA EN EL CHAT. No hay escena ni boton: al llegar a 20 de
## deseo el `trigger_mensaje` de ETAPA_BOTON_LISTO habilita el grupo, el jugador
## le escribe desde el celular, y al terminar la conversacion el
## `accion_al_completar` del grupo cierra la quest. Mismo esquema que la 07_c.
##
## EL JUGADOR ES EL QUE ESCRIBE PRIMERO: por eso el grupo va con
## mensaje_inicial="" — con el mensaje inicial vacio el sistema no muestra
## ninguna burbuja del NPC y arranca directo con las opciones del jugador
## (messagesystem_core, _entregar_grupo).
##
## CONDICION DE ENTREGA — Violet en su habitacion y el MC en otra parte. Va
## partida en dos porque cada mitad tiene su mecanismo:
##   - `momento_locacion="casa_hviolet"` — la via declarativa para "el NPC tiene
##     que estar acá"; la chequea el motor.
##   - `condicion_entrega=_vd20_mc_afuera` — para el MC no hay parametro, va
##     como callable.
## Mientras no se cumplan las dos, el grupo queda EN ESPERA y la conversacion
## no aparece en el celular. El motor las re-evalua en cada vuelta del loop, al
## moverse, al avanzar el horario y al dormir.


init python:

    def _vd20_mc_afuera():
        """
        condicion_entrega del chat: que el MC NO este en la habitacion de Violet.

        La otra mitad de la condicion (que ella SI este ahi) la cubre
        momento_locacion, asi que acá solo se mira al jugador.
        """
        _loc_mc = store.sistema_locaciones.locacion_actual
        if _loc_mc is None:
            return False
        return _loc_mc.id != "casa_hviolet"

    def _vd20_chat_completado():
        """
        accion_al_completar del chat: cierra la quest. No hay que ir a hablar
        con Violet despues — la conversacion ES la quest.

        Funcion de MODULO (no lambda ni def anidada): se guarda en el save via
        el grupo de mensajes.
        """
        if hasattr(store, 'completar_quest_actual'):
            store.completar_quest_actual("violet", quest_id="violet_deseo_04")


################################################################################
## Label de cierre — red de seguridad, no se usa en el flujo normal
################################################################################
## El motor le asigna a toda Quest el label "quest_<id>". Este flujo no lo
## invoca nunca (la cierra el chat), pero existe por las dudas de que algun
## camino futuro salte acá: cierra la quest sin dejar nada colgado, igual que
## el de la 07_c. La quest esta excluida del boton generico del menu de Violet
## justo para que este label NO sea alcanzable saltandose el chat.

label quest_violet_deseo_04:
    $ completar_quest_actual("violet", quest_id="violet_deseo_04")
    window hide
    $ mostrar_hud()
    jump game_loop

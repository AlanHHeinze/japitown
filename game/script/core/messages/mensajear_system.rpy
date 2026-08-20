################################################################################
## Mensajear — enganche generico
################################################################################
## El chat del juego es REACTIVO: llega un GrupoMensajes y el jugador responde.
## "Mensajear" es la ventaja que lo vuelve ACTIVO — el jugador le escribe primero
## al NPC y el contenido decide que conversacion se arma.
##
## Este archivo es SOLO la maquinaria: un registro por NPC y las dos funciones
## que consulta la UI del celular. No conoce a ningun NPC ni ninguna
## conversacion; todo eso lo aporta el contenido desde
## characters/<npc>/ventajas/mensajear/.
##
## LA UI (hud_mensajes) pregunta dos cosas:
##   mensajear_puede_hablar(npc_id)  → ¿pinto el boton amarillo?
##   mensajear_iniciar(npc_id)       → el jugador lo toco
##
## El boton de RESPONDER siempre le gana al de hablar: si hay una conversacion
## abierta —de quest o de este sistema— no se puede empezar otra. Eso lo resuelve
## la UI por orden, no hace falta chequearlo acá.

init python:

    # {npc_id: (fn_puede, fn_iniciar)}
    MENSAJEAR_REGISTRO = {}

    def registrar_mensajear(npc_id, fn_puede, fn_iniciar):
        """
        Habilita el "Mensajear" para un NPC.

        Args:
            npc_id: a quien se le puede escribir
            fn_puede: funcion de MODULO sin argumentos → bool. True si AHORA se
                le puede escribir (ventaja otorgada, disponible, sin usar hoy...).
            fn_iniciar: funcion de MODULO sin argumentos. Arma la conversacion:
                mete el mensaje del jugador, elige el grupo y lo deja activo.
        """
        MENSAJEAR_REGISTRO[npc_id] = (fn_puede, fn_iniciar)

    def mensajear_habilitado(npc_id):
        """True si este NPC tiene el sistema registrado (tenga o no turno hoy)."""
        return npc_id in MENSAJEAR_REGISTRO

    def mensajear_puede_hablar(npc_id):
        """
        True si el boton "Hablar" tiene que estar activo para este NPC.

        Envuelto en try: lo llama una screen, y una excepcion ahi rompe el
        celular entero. Ante la duda, el boton queda apagado.
        """
        _reg = MENSAJEAR_REGISTRO.get(npc_id)
        if not _reg:
            return False
        try:
            return bool(_reg[0]())
        except Exception:
            return False

    def mensajear_iniciar(npc_id):
        """Arranca la conversacion. La llama el boton "Hablar" de la UI."""
        _reg = MENSAJEAR_REGISTRO.get(npc_id)
        if not _reg:
            return
        _reg[1]()
        renpy.restart_interaction()

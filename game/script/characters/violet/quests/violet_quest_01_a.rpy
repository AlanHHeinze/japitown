################################################################################
## Violet Quest 01 — Un paquete misterioso
################################################################################
## 3 dias despues de completar quest 0, llega un paquete.
## El jugador puede recibirlo del repartidor (mañana) o de la cama (tarde).
## Corresponde a: quest_violet_01_a (id: violet_questprincipal_01_a)


# =============================================================================
# VARIABLES
# =============================================================================

# True cuando el sistema de delivery de quest esta activo (repartidor en puerta o paquete en cama)
default violet_quest1_entrega_pendiente = False

# True cuando el paquete fue dejado en la cama (jugador no atendio al repartidor)
default violet_quest1_en_cama = False


# =============================================================================
# FUNCIONES
# =============================================================================

init python:

    def setup_entrega_quest1_violet():
        """
        Se ejecuta via accion_al_entrar cuando quest 1 entra en ETAPA_BOTON_LISTO.
        Configura el repartidor para que aparezca en la puerta.
        """
        store.repartidor_presente = True
        store.violet_quest1_entrega_pendiente = True

    def manejar_quest1_violet_no_recibido():
        """
        Se llama desde avanzar_horario() cuando el repartidor se va
        sin que el jugador lo atendiera. Coloca el paquete en la cama
        y dispara el mensaje de Monica.
        """
        if not store.violet_quest1_entrega_pendiente:
            return

        # El paquete va a la cama
        store.paquete_en_habitacion = True
        store.violet_quest1_en_cama = True

        # Notificación de Monica (mensaje directo, sin respuesta)
        if hasattr(store, 'sistema_mensajes'):
            store.sistema_mensajes.inicializar_chat("monica")
            store.sistema_mensajes.chats["monica"].agregar_mensaje(
                "monica",
                "Llegó un paquete, creo que es tuyo lo dejé en tu habitación"
            )

    def _pista_quest1_violet():
        """Retorna la pista dinamica segun el estado de la entrega."""
        if not store.violet_quest1_entrega_pendiente:
            return "Todo tranquilo por ahora"

        # Paquete en la cama
        if store.violet_quest1_en_cama:
            # Verificar si leyo el mensaje de Monica
            if hasattr(store, 'sistema_mensajes') and store.sistema_mensajes.grupo_completado("monica_chat_violet_quest1_paquete"):
                return "Revisar el paquete"
            else:
                return "Tengo un mensaje por ver"

        # Repartidor en la puerta (mañana)
        return "Parece que hay alguien afuera"

    def _quehacer_quest1_violet():
        """Retorna el que hacer dinamico segun el estado de la entrega."""
        if not store.violet_quest1_entrega_pendiente:
            return "Esperar"

        # Paquete en la cama
        if store.violet_quest1_en_cama:
            if hasattr(store, 'sistema_mensajes') and store.sistema_mensajes.grupo_completado("monica_chat_violet_quest1_paquete"):
                return "Ir a la habitación por el paquete"
            else:
                return "Responder el mensaje de Monica"

        # Repartidor en la puerta
        return "Ir al frente"

    def _limpiar_flags_quest1_violet():
        """Limpia todos los flags de la quest 1 después de completarla."""
        store.violet_quest1_entrega_pendiente = False
        store.violet_quest1_en_cama = False


################################################################################
## LABEL: Recibir paquete del repartidor
################################################################################

label paqueterepartidor_quest01_violet:

    hide screen hud_navegacion
    $ ocultar_hud()
    window show

    scene bg_casa_mañana_frente with fade

    show repartidor_parado c_base at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show repartidor_parado c_hablando
    repartidor "Buen día, tengo un paquete para esta dirección."
    show repartidor_parado c_base

    piensa "Debe ser de alguna de las chicas, yo no pedi nada"
    show mc_parado_base b_hablando
    mc "Yo lo recibo, gracias"
    show mc_parado_base b_none

    show repartidor_parado c_hablando
    repartidor "Aquí tiene, que tenga un buen día."
    show repartidor_parado c_base

    show mc_parado_base b_hablando
    mc "Igualmente para usted"
    show mc_parado_base b_none

    hide repartidor_parado with dissolve

    # MC mira el paquete
    show mc_parado_base c_rbase_regaloviolet o_abajonm
    piensa "La etiqueta está dañada, no puedo ver el nombre..."
    piensa "Pero se llega a ver el nombre de la tienda MundoMangas"
    piensa "Debe ser de Violet, luego se lo doy"

    # Dar item al inventario
    $ agregar_al_inventario("mangas_violet")

    # Limpiar flags y aumentar confianza del repartidor
    $ _limpiar_flags_quest1_violet()
    $ aumentar_confianza_repartidor()
    $ store.repartidor_presente = False

    hide mc_parado_base with dissolve

    # Completar quest
    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LABEL: Recoger paquete de la cama
################################################################################

label paquetecama_quest01_violet:

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Mostrar habitacion del MC segun horario
    $ _horarios_bg_vq1 = ["tarde", "tarde", "noche", "noche"]
    $ _bg_horario_vq1 = _horarios_bg_vq1[horario_actual]
    scene expression "images/bg/casa/bg_casa_" + _bg_horario_vq1 + "_hmc.png" with fade

    show mc_parado_base c_rbase_regaloviolet o_abajonm b_none at mc_izquierda with dissolve

    piensa "Este debe ser el paquete que Monica me dijo"
    piensa "La etiqueta está dañada y no se llega a ver el nombre, pero dice MundoMangas"
    piensa "Debe ser de Violet, luego se lo doy"

    # Dar item al inventario
    $ agregar_al_inventario("mangas_violet")

    # Limpiar flags
    $ _limpiar_flags_quest1_violet()
    $ store.paquete_en_habitacion = False

    hide mc_parado_base with dissolve

    # Completar quest
    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop

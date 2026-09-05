################################################################################
## Eventos de Jasmine
################################################################################
## Definición de todos los eventos de Jasmine

# Día en que se completó la quest 0_c. Lo escribe el cierre de esa quest
# (jasmine_quest_0_c.rpy) y lo lee condicion_aparicion_event1_jasmine para
# esperar 1 día antes de mostrar el evento.
default jasmine_quest_0c_dia_completada = 0

init 10 python:

    # ===========================================================================
    # NOTA: La PRIMERA parte del evento 1 ("Ropa Nueva") se convirtió en la quest
    # jasmine_questprincipal_0_c. La cadena de quests es: 0_a → 0_b → 0_c.
    # El evento formal de abajo es solo la REPETICIÓN ("Volver a ver"): aparece en
    # el panel de pistas tras completar la 0_c y se dispara con el botón del menú.
    # ===========================================================================

    def condicion_aparicion_event1_jasmine():
        """
        Aparece (VISIBLE) 1 día después de completar la quest 0_c de Jasmine y
        con 10 de deseo.

        La espera evita que el evento de "volver a ver" aparezca el mismo día en
        que acabás de ver el conjunto. Mismo patrón que el evento 1 de Mónica.

        El requisito de relación va en la APARICIÓN y no en la activación: asi el
        evento tampoco figura en el panel de pistas hasta que el vínculo esté al
        nivel.
        """
        q = sistema_quests.obtener_quest("jasmine_questprincipal_0_c")
        if not q or not q.completada:
            return False

        dia_completada = getattr(store, 'jasmine_quest_0c_dia_completada', 0)
        dias_totales = getattr(store, 'dias_totales', 1)
        if dias_totales - dia_completada < 1:
            return False

        return obtener_stat2("jasmine") >= 10

    def condicion_activacion_event1_jasmine():
        """El evento NO se auto-activa por tiempo: lo dispara el botón
        'Volver a ver el conjunto' (ver interaccion_jasmine → check_replay).
        Devolver False evita que validar_eventos() lo saque de VISIBLE."""
        return False

    def inicializar_events_jasmine():
        """Inicializa todos los eventos de Jasmine."""

        # =====================================================================
        # EVENTO 1: Volver a ver (repetición del conjunto deportivo)
        # =====================================================================
        event_jasmine_01 = Event(
            id="jasmine_event_01",
            nombre="Volver a ver",
            tipo=TIPO_EVENT_ESPORADICO,
            prioridad=10,
            condicion_aparicion=condicion_aparicion_event1_jasmine,
            condicion_activacion=condicion_activacion_event1_jasmine,
            label_efecto="event_jasmine_01_check_replay",
            descripcion="Jasmine estrenó un conjunto deportivo nuevo.",
            npc_id="jasmine",
            mensaje_pista="Podría volver a ver el conjunto de Jasmine en el Gym por la tarde.",
            mensaje_que_hacer="Habla con Jasmine en el Gym por la tarde.",
            condicion_cierre_texto="",
            mensaje_despertar="Podría volver a ver el conjunto nuevo de Jasmine si la encuentro en el Gym por la tarde.",
            config_etapas={
                ESTADO_EVENT_VISIBLE: ConfigEtapa(
                    pista="Podría volver a ver el conjunto de Jasmine en el Gym por la tarde.",
                    que_hacer="Habla con Jasmine en el Gym por la tarde.",
                    mensaje_despertar="Podría volver a ver el conjunto nuevo de Jasmine si la encuentro en el Gym por la tarde.",
                ),
            },
        )

        sistema_events.registrar_event(event_jasmine_01)


# Inicializar eventos de Jasmine al cargar el juego
init 11 python:
    inicializar_events_jasmine()


################################################################################
## Funciones auxiliares para eventos de Jasmine
################################################################################

init python:

    def jasmine_event_01_completado():
        """Verifica si la quest 0_c de Jasmine está completada (conversión de evento 1)."""
        q = sistema_quests.obtener_quest("jasmine_questprincipal_0_c")
        return q and q.completada

    def jasmine_en_gym_tarde():
        """Verifica si Jasmine está en el gym por la tarde."""
        dia = getattr(store, 'dia_semana_actual', 0)
        horario = getattr(store, 'horario_actual', 0)

        # Obtener locación actual correctamente
        locacion_id = ""
        if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
            locacion_id = store.sistema_locaciones.locacion_actual.id

        return dia in [0, 1, 2, 3, 4] and horario == 1 and locacion_id == "casa_gym"

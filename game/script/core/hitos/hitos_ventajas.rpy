################################################################################
## Hitos — Catálogo de ventajas
################################################################################
## Una "ventaja" es una capacidad concreta que un Hito le otorga al jugador con
## un NPC. Acá se registran TODAS las ventajas posibles con su id; los hitos las
## referencian por ese id (ver characters/<npc>/hitos_<npc>.rpy).
##
## Registrarlas en un catálogo y no usar strings sueltos tiene una razón:
## verificar_coherencia_hitos() puede detectar un id mal escrito. Sin catálogo,
## un typo daría una ventaja que nunca se cumple y el bug seria invisible.
##
## HAY DOS CLASES DE VENTAJA:
##
##   CONSULTABLE (aplicar=None) — el sistema pregunta en el momento:
##       if npc_tiene_ventaja("violet", "puerta_dejar_pasar"): ...
##     Sirve para todo lo que se evalua cada vez: puertas, estados de talk,
##     aparicion de eventos, requisitos de quest, botones. Es la mayoria.
##
##   APLICABLE (aplicar=funcion) — corre UNA vez, al alcanzar el hito:
##       registrar_ventaja("skin_x", "...", aplicar=_dar_skin_x)
##     Sirve para lo que hay que otorgar activamente y queda hecho: un skin,
##     activar un estado especial de talk.
##
## Los handlers `aplicar` DEBEN ser funciones de modulo (regla 3 del skill):
## quedan referenciados desde el catalogo, que vive en init y no se guarda, pero
## la regla se respeta por consistencia y para no romper si eso cambia.
##
## Este archivo define la MAQUINARIA y las ventajas del motor. Las ventajas
## propias de una quest o evento se registran desde el archivo de ese contenido.

init python:

    # {ventaja_id: {"nombre": str, "descripcion": str, "aplicar": callable|None}}
    VENTAJAS_HITO = {}

    def registrar_ventaja(ventaja_id, nombre, descripcion="", aplicar=None):
        """
        Registra una ventaja otorgable por un hito.

        Args:
            ventaja_id: id unico (ej. "puerta_dejar_pasar")
            nombre: nombre legible, para paneles y debug. Se traduce al mostrar.
            descripcion: que hace la ventaja, en una frase. La muestra el panel
                de Desbloqueos al pasar el mouse (o al tocarla, en tactil). Va
                en español; se traduce al mostrarla.
            aplicar: None para las CONSULTABLES (el sistema pregunta cuando
                necesita). Funcion de modulo para las APLICABLES: recibe el
                npc_id y corre una sola vez, al otorgarse el hito.

        `descripcion` va tercero y con default a proposito: las llamadas que
        pasan `aplicar=` por keyword siguen andando sin tocarse.
        """
        VENTAJAS_HITO[ventaja_id] = {
            "nombre": nombre,
            "descripcion": descripcion,
            "aplicar": aplicar,
        }

    def obtener_ventaja(ventaja_id):
        """Config de una ventaja, o None si el id no existe."""
        return VENTAJAS_HITO.get(ventaja_id)


    # =========================================================================
    # VENTAJAS DEL MOTOR — acceso a habitaciones
    # =========================================================================
    # Los 4 niveles que antes vivian en TABLA_ACCESO_HABITACION. Todas son
    # CONSULTABLES: verificar_nivel_acceso_habitacion() las consulta al golpear
    # o al entrar (ver core/locations/door_relation_system.rpy).
    #
    # El orden de mayor a menor privilegio importa: la funcion de puertas
    # devuelve el primero que se cumple.

    registrar_ventaja(
        "puerta_ingreso_noche",
        "Entrar a la habitación de trasnoche",
        "Podés entrar a su habitación de madrugada sin golpear. Es el nivel de confianza más alto.",
    )

    registrar_ventaja(
        "puerta_ingreso_diurno",
        "Entrar a la habitación durante el día",
        "Podés entrar a su habitación de día sin golpear ni pedir permiso.",
    )

    registrar_ventaja(
        "puerta_dejar_pasar",
        "Te deja pasar al golpear la puerta",
        "Si golpeás, te abre y te deja pasar a su habitación.",
    )

    registrar_ventaja(
        "puerta_sale_pasillo",
        "Sale al pasillo cuando golpeás la puerta",
        "Si golpeás, sale a hablar al pasillo, pero todavía no te deja entrar.",
    )

    # Variantes acotadas por momento del dia. Sirven para que una linea abra el
    # acceso de a poco: primero sale de tarde, mas adelante tambien de noche.
    # verificar_nivel_acceso_habitacion() las cruza con el horario actual.
    registrar_ventaja(
        "puerta_sale_pasillo_tarde",
        "Sale al pasillo si golpeás por la tarde",
        "Por la tarde sale a hablar al pasillo cuando golpeás. A otras horas no atiende.",
    )

    registrar_ventaja(
        "puerta_sale_pasillo_noche",
        "Sale al pasillo si golpeás por la noche",
        "Por la noche sale a hablar al pasillo cuando golpeás. A otras horas no atiende.",
    )

    # De trasnoche todos los NPC duermen y no se los puede clickear (ver
    # npc_durmiendo en core/quests/restriccion_quest_system.rpy). Esta ventaja
    # levanta ese bloqueo para un NPC. Todavia no la otorga ningun hito.
    registrar_ventaja(
        "npc_interaccion_trasnoche",
        "Podés hablarle de madrugada",
        "Aunque sea de madrugada te atiende en vez de estar durmiendo.",
    )


    # =========================================================================
    # VENTAJAS DEL MOTOR — sistema de conversación (talk)
    # =========================================================================
    # Todas CONSULTABLES: el sistema de talk pregunta cuando arma la charla.

    # Estados de animo que entran al pool diario. El id del estado va en el
    # nombre de la ventaja para que la relacion sea evidente al leer el hito.
    registrar_ventaja(
        "talk_estado_buen_humor",
        "Puede estar de buen humor",
        "Se suma «Buen Humor» a sus estados de ánimo posibles del día. En ese estado las conversaciones dan más puntos.",
    )

    registrar_ventaja(
        "talk_estado_muy_buen_humor",
        "Puede estar de muy buen humor",
        "Se suma «Muy Buen Humor» a sus estados posibles. Es el estado que más recompensa da al conversar.",
    )

    registrar_ventaja(
        "talk_estado_caliente",
        "Puede estar en un estado de ánimo especial",
        "Se suma un estado de ánimo nuevo, con opciones de conversación que antes no aparecían.",
    )

    # Muestra el resultado de una opcion al azar antes de elegir. El motor ya
    # tenia esto atado a mc_carisma >= 2; ahora tambien lo puede dar un hito.
    registrar_ventaja(
        "talk_preview_resultado",
        "Intuís el resultado de una de las opciones",
        "Antes de elegir, una de las opciones de la conversación te muestra qué resultado va a dar.",
    )

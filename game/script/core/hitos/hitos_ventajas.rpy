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

    # Variantes acotadas por horario, calcadas de las de sale_pasillo de mas
    # abajo. Amor abre el dia, deseo abre la noche: las otorgan los hitos de
    # amor 20 y deseo 20.
    registrar_ventaja(
        "puerta_dejar_pasar_tarde",
        "Pasar (Tarde)",
        "Podremos ingresar a su habitación por la tarde.",
    )

    registrar_ventaja(
        "puerta_dejar_pasar_noche",
        "Pasar (Noche)",
        "Podremos ingresar a su habitación por la noche.",
    )

    registrar_ventaja(
        "puerta_sale_pasillo",
        "Sale al pasillo cuando golpeás la puerta",
        "Si golpeás, sale a hablar al pasillo, pero todavía no te deja entrar.",
    )

    # Variantes acotadas por momento del dia. Sirven para que una linea abra el
    # acceso de a poco: primero sale de tarde, mas adelante tambien de noche.
    # verificar_nivel_acceso_habitacion() las cruza con el horario actual.
    #
    # EL MARCADOR {npc}: obtener_desbloqueos_stat lo reemplaza por el nombre del
    # NPC al pintar el panel (core/relationships/relationship_unlocks.rpy), asi
    # que UNA entrada sirve para los tres — "Violet no me ignora", "Mónica no me
    # ignora". Se conserva tal cual en el `new` de la traduccion.
    registrar_ventaja(
        "puerta_sale_pasillo_tarde",
        "{npc} no me ignora (Tarde)",
        "Al interactuar con su puerta por la tarde, {npc} responde y sale al pasillo a hablar.",
    )

    registrar_ventaja(
        "puerta_sale_pasillo_noche",
        "{npc} no me ignora (Noche)",
        "Al interactuar con su puerta por la noche, {npc} responde y sale al pasillo a hablar.",
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
        "Estado Buen Humor",
        "Al hablar con ella puede tener este estado asignado, que garantiza +1 ❤️ en todas las opciones.",
    )

    registrar_ventaja(
        "talk_estado_muy_buen_humor",
        "Estado Muy Buen Humor",
        "Al hablar con ella puede tener este estado asignado, que garantiza ❤️ en todas las opciones: algunas dan +1 y otras +2.",
    )

    # Los dos estados de deseo son un escalon: primero "Insinuante", que da lo
    # mismo elijas lo que elijas, y despues "Hot", que rinde mas y ademas
    # premia provocarla. Por eso los otorgan hitos distintos (deseo 10 y 30).
    registrar_ventaja(
        "talk_estado_insinuante",
        "Estado Insinuante",
        "Al hablar con ella puede tener este estado asignado, que garantiza +1 💋 en todas las opciones.",
    )

    registrar_ventaja(
        "talk_estado_caliente",
        "Estado Hot",
        "Al hablar con ella puede tener este estado asignado, que garantiza 💋 en todas las opciones: algunas dan +1 y otras +2.",
    )

    # Muestra el resultado de una opcion al azar antes de elegir. El motor ya
    # tenia esto atado a mc_carisma >= 2; ahora tambien lo puede dar un hito.
    registrar_ventaja(
        "talk_preview_resultado",
        "Conocerla",
        "Al hablar con ella siempre vemos el resultado de una de las respuestas.",
    )

    # Memoria sin tope para ese NPC. Sin esta ventaja el MC recuerda
    # max(1, mc_inteligencia) combinaciones (estado, opcion) — y mc_inteligencia
    # arranca en 0, o sea UNA. La consulta actualizar_memoria_mc()
    # (core/talk/talksystem_core.rpy), que es donde se hace el recorte.
    #
    # Se lleva bien con "Conocerla" en vez de pisarla: el preview solo elige
    # entre las opciones que NO estan en memoria, asi que a medida que el
    # jugador prueba las cinco de un estado deja de haber algo que adivinar.
    registrar_ventaja(
        "talk_memoria_total",
        "Recordar",
        "Al hablar con ella siempre vemos el resultado de nuestra elección pasada con ese estado.",
    )


    # =========================================================================
    # VENTAJAS DE CONTENIDO — sistemas propios del NPC
    # =========================================================================
    # Estas dos NO las consume el motor: las consume contenido que vive en
    # characters/<npc>/ventajas/. Se registran igual acá para que el panel de
    # Desbloqueos las muestre y para que verificar_coherencia_hitos() las valide
    # como a cualquier otra.

    registrar_ventaja(
        "accion_jugar",
        "Jugar",
        "Al hacer uso de la acción Jugar, {npc} se puede unir y mejora la relación en +2 ❤️.",
    )

    registrar_ventaja(
        "juegos_nuevos",
        "Juegos Nuevos",
        "Al interactuar con {npc} tendremos la opción de jugar un juego nuevo; son escenas especiales con ella.",
    )

    registrar_ventaja(
        "accion_ver_anime",
        "Ver Anime",
        "Al hacer uso de la acción Ver Anime, {npc} se puede unir y mejora la relación en +2 💋.",
    )

    registrar_ventaja(
        "mensajear",
        "Mensajear",
        "Ahora podremos escribirle a {npc} por el chat cuando queramos y tener conversaciones especiales con ella.",
    )

    registrar_ventaja(
        "accion_beso_amor",
        "Beso (Amor)",
        "En el menú de {npc} tendremos la opción de besarla, una vez por día.",
    )

    registrar_ventaja(
        "ropa_nueva",
        "Ropa Nueva",
        "Estando en su habitación, {npc} nos puede mostrar cómo le queda algo nuevo.",
    )

    registrar_ventaja(
        "accion_beso_deseo",
        "Beso (Deseo)",
        "En el menú de {npc} tendremos otra forma de besarla, una vez por día.",
    )

    registrar_ventaja(
        "provocacion",
        "Provocación",
        "En distintos momentos {npc} nos va a estar provocando; son escenas especiales que aparecen solas.",
    )

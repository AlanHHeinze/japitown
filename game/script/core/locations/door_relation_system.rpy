################################################################################
## Sistema de Relacion — Nivel de Acceso a Habitaciones y Baño
################################################################################
## Define los umbrales de stats que determinan cómo responde el NPC
## cuando el jugador intenta entrar a su habitacion o al baño.
##
## Jerarquía de niveles para HABITACIÓN (el más alto que se cumpla aplica):
##   "ingreso_noche"   — horario 3, entra directamente sin menú      (stat2)
##   "ingreso_diurno"  — horario 0-2, entra directamente sin menú    (stat1)
##   "dejar_pasar"     — al golpear, NPC dice "Adelante" y el jugador entra (stat1)
##   "sale_pasillo"    — al golpear, NPC dice "Ahi salgo" y va al pasillo   (stat1)
##   None              — respuesta negativa ("Estoy ocupada") — sin requisito
##
## El BAÑO no usa este sistema: "Espiar" es el minijuego de core/espiar/
## (espiar_system.rpy) y "Entrar" sigue en desarrollo.

################################################################################
## De dónde salen ahora los umbrales
################################################################################
## Antes había acá una TABLA_ACCESO_HABITACION con los umbrales por NPC. Se
## eliminó: los 4 niveles pasaron a ser VENTAJAS otorgadas por los Hitos de
## relación (core/hitos/). Los umbrales viven en characters/<npc>/hitos_<npc>.rpy.
##
## El motivo del cambio: los umbrales estaban escritos dos veces —acá y en los
## `agregar_desbloqueo` que alimentaban el panel de Relaciones— y ya se habían
## desfasado (el panel prometía ingreso diurno con amor 30 y esta tabla pedía 50).
## Con una sola fuente eso no puede volver a pasar.
##
## Ids de las ventajas (registradas en core/hitos/hitos_ventajas.rpy):
##   "puerta_ingreso_noche"   ·  "puerta_ingreso_diurno"
##   "puerta_dejar_pasar"     ·  "puerta_sale_pasillo"


################################################################################
## MENSAJES DE RESPUESTA POR NPC
################################################################################
## Textos que dice cada NPC al responder en la puerta.
## Editar aqui para personalizar la voz de cada personaje.

define MENSAJES_NPC_PUERTA = {
    "violet": {
        "ocupada":   "Estoy ocupada.",
        "ahi_salgo": "Ahí salgo.",
        "adelante":  "Adelante.",
    },
    "jasmine": {
        "ocupada":   "Estoy ocupada.",
        "ahi_salgo": "Ahí salgo.",
        "adelante":  "Adelante.",
    },
    "monica": {
        "ocupada":   "Estoy ocupada.",
        "ahi_salgo": "Ahí salgo.",
        "adelante":  "Adelante.",
    },
}

# Fallback si un NPC no tiene la clave definida arriba
define MENSAJES_PUERTA_DEFAULT = {
    "ocupada":   "Estoy ocupada.",
    "ahi_salgo": "Ahí salgo.",
    "adelante":  "Adelante.",
}


init python:

    def mensaje_puerta_npc(npc_id, clave):
        """
        Respuesta TRADUCIDA del NPC en la puerta ("ocupada" / "ahi_salgo" / "adelante").

        Los mensajes se muestran por interpolacion (violet "[_msg]"), y la
        interpolacion NO traduce: hay que hacerlo aca. Centralizado a proposito —
        antes cada label lo resolvia por su cuenta y solo uno de los cuatro
        llamaba a translate_string, asi que tres salian siempre en español.
        """
        msg = MENSAJES_NPC_PUERTA.get(npc_id, {}).get(
            clave, MENSAJES_PUERTA_DEFAULT.get(clave, "")
        )
        return renpy.translate_string(msg) if msg else ""


################################################################################
## Funciones de verificación
################################################################################

init python:

    def verificar_nivel_acceso_habitacion(npc_id):
        """
        Retorna el nivel de acceso más alto que cumple el jugador para
        la habitacion del NPC, teniendo en cuenta el horario actual.

        Jerarquía evaluada de mayor a menor:
            "ingreso_noche"   → horario == 3 y tiene la ventaja
            "ingreso_diurno"  → horario in (0,1,2) y tiene la ventaja
            "dejar_pasar"     → tiene la ventaja
            "sale_pasillo"    → tiene la ventaja
            None              → ningun nivel alcanzado

        NOMBRE Y CONTRATO SIN CAMBIOS a proposito: door_access_system.rpy la
        llama en dos lugares y compara contra estos mismos strings, asi que la
        migracion a Hitos no lo toca. Lo unico que cambio es de donde sale el
        permiso: antes se leia un stat contra un umbral de TABLA_ACCESO_HABITACION,
        ahora se pregunta si el NPC tiene la ventaja otorgada por algun hito.

        La regla de HORARIO se queda acá y no en el hito: el hito dice "puede
        entrar de noche", el momento del dia es otra cosa.

        Returns:
            str | None
        """
        horario = getattr(store, "horario_actual", 0)

        # ingreso_noche — solo si es trasnoche
        if horario == 3 and npc_tiene_ventaja(npc_id, "puerta_ingreso_noche"):
            return "ingreso_noche"

        # ingreso_diurno — solo si no es trasnoche
        if horario != 3 and npc_tiene_ventaja(npc_id, "puerta_ingreso_diurno"):
            return "ingreso_diurno"

        if npc_tiene_ventaja(npc_id, "puerta_dejar_pasar"):
            return "dejar_pasar"

        # sale_pasillo: la ventaja generica vale a cualquier hora; las variantes
        # acotadas solo en su momento del dia. Asi una linea puede abrir el
        # acceso de a poco (primero de tarde, mas adelante tambien de noche).
        # Horarios: 0 mañana · 1 tarde · 2 noche · 3 trasnoche.
        if npc_tiene_ventaja(npc_id, "puerta_sale_pasillo"):
            return "sale_pasillo"
        if horario == 1 and npc_tiene_ventaja(npc_id, "puerta_sale_pasillo_tarde"):
            return "sale_pasillo"
        if horario == 2 and npc_tiene_ventaja(npc_id, "puerta_sale_pasillo_noche"):
            return "sale_pasillo"

        return None


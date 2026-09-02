################################################################################
## Espiar — Contenido de Violet
################################################################################
## Escenas que se ven por la rendija cuando Violet deja la puerta entreabierta.
## El motor esta en core/espiar/espiar_system.rpy; quien decide si la puerta esta
## abierta es la ventaja Provocación
## (characters/violet/ventajas/provocacion/provocacion_violet.rpy).
##
## Acá ya no hay reacciones al ser descubierto: eso era del viejo "espiar", donde
## el MC forzaba la puerta y podia fallar. Ahora la puerta esta abierta porque
## ella la dejo asi.
##
## Para agregar una escena: copiar el bloque registrar_secuencia_espiar y cambiar
## id/fondo. Para atarla a una quest o evento, pasar condicion=funcion_de_modulo
## (definida en init python, nunca lambda).

init python:

    def _violet_espiar_ducha_vista():
        """Predicado del catalogo de contenido (el ojo del panel de Desbloqueos)."""
        return espiar_secuencia_vista("violet_espiar_ducha")


init 6 python:

    # ── Secuencias ───────────────────────────────────────────────────────────

    registrar_secuencia_espiar(SecuenciaEspiar(
        id="violet_espiar_ducha",
        npc_id="violet",
        nombre="Violet en la ducha",
        fondo="images/minijuegos/ducha/ducha_fondo.jpg",
    ))

    registrar_contenido_ventaja(
        "provocacion", "espiar_ducha", "violet",
        "La puerta entreabierta",
        "Andá al pasillo de arriba mientras se esté bañando. No pasa siempre: depende de si ella dejó la puerta así.",
        vista=_violet_espiar_ducha_vista,
        orden=10,
    )

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

init 6 python:

    # ── Secuencias ───────────────────────────────────────────────────────────

    registrar_secuencia_espiar(SecuenciaEspiar(
        id="violet_espiar_ducha",
        npc_id="violet",
        nombre="Violet en la ducha",
        fondo="images/minijuegos/ducha/ducha_fondo.jpg",
    ))

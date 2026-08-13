################################################################################
## Violet — HITOS DE RELACIÓN
################################################################################
## Cada hito se OTORGA al completar su quest de relacion (`quest_id`), no al
## llegar al umbral. El umbral hace otras dos cosas:
##   1. habilita la quest (via el Requisito de la propia Quest)
##   2. TOPEA el stat — no sube mas hasta completar esa quest (ver tope_stat)
##
## El ciclo es: subir hasta el tope → jugar la quest → se libera el tramo
## siguiente y se otorgan las ventajas del hito.
##
## HITOS CADA 10, QUESTS CADA 5. Las quests intermedias (5, 15, 25) existen y se
## juegan, pero no otorgan hito ni mueven el tope: el tope siempre es el umbral
## del proximo hito pendiente (10 → 20 → 30 → sin tope).
##
## Los nombres de esta tanda son PROVISORIOS (version de prueba).

init 6 python:

    # =========================================================================
    # LINEA DE AMOR
    # =========================================================================

    registrar_hito(Hito(
        id="violet_hito_amor_01",
        npc_id="violet",
        stat="amor",
        umbral=10,
        quest_id="violet_amor_02",          # la quest de umbral 10
        nombre="Buena relación",
        descripcion="Violet me tiene confianza y se muestra mas abierta.",
        icono="❤️",
        ventajas=[
            "puerta_sale_pasillo_tarde",    # sale al pasillo si golpeo de tarde
            "talk_estado_buen_humor",       # puede aparecer de buen humor
            "talk_preview_resultado",       # intuyo el resultado de una opcion
        ],
    ))

    registrar_hito(Hito(
        id="violet_hito_amor_02",
        npc_id="violet",
        stat="amor",
        umbral=20,
        quest_id="violet_amor_04",          # la quest de umbral 20
        nombre="Como antes",
        descripcion="Volvimos a tener la relacion que teniamos.",
        icono="❤️",
        ventajas=[
            # "Muy Buen Humor" ya existia como EstadoTalk y su condicion vieja
            # era amor >= 15. Al migrarla a ventaja quedaba huerfana (ningun
            # hito la otorgaba) y el estado no habria aparecido nunca. Va acá
            # como escalon natural sobre "buen humor" del hito anterior;
            # moverla a otro hito es solo cambiarla de lista.
            "talk_estado_muy_buen_humor",
        ],
    ))

    registrar_hito(Hito(
        id="violet_hito_amor_03",
        npc_id="violet",
        stat="amor",
        umbral=30,
        quest_id="violet_amor_06",          # la quest de umbral 30
        nombre="Algo nos pasa",
        descripcion="Hay algo entre nosotros que ya no podemos ignorar.",
        icono="❤️",
        ventajas=[],
    ))

    # =========================================================================
    # LINEA DE DESEO
    # =========================================================================

    registrar_hito(Hito(
        id="violet_hito_deseo_01",
        npc_id="violet",
        stat="deseo",
        umbral=10,
        quest_id="violet_deseo_02",         # la quest de umbral 10
        nombre="Me atrae",
        descripcion="Hay una tension distinta entre los dos.",
        icono="💋",
        ventajas=[
            "puerta_sale_pasillo_noche",    # sale al pasillo si golpeo de noche
            "talk_estado_caliente",         # puede aparecer en ese estado
        ],
    ))

    registrar_hito(Hito(
        id="violet_hito_deseo_02",
        npc_id="violet",
        stat="deseo",
        umbral=20,
        quest_id="violet_deseo_04",         # la quest de umbral 20
        nombre="Confesión",
        descripcion="Ya nos dijimos lo que estaba pasando.",
        icono="💋",
        ventajas=[],
    ))

    registrar_hito(Hito(
        id="violet_hito_deseo_03",
        npc_id="violet",
        stat="deseo",
        umbral=30,
        quest_id="violet_deseo_06",         # la quest de umbral 30
        nombre="Un paso más allá",
        descripcion="La relacion cambio de forma definitiva.",
        icono="💋",
        ventajas=[],
    ))

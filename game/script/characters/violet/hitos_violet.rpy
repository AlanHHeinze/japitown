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
## AL FINAL DE CADA LINEA hay un hito "Próximamente" (umbral 40) con
## proximamente=True: no se otorga nunca y el panel lo pinta en gris. Es solo el
## cartel de que la linea sigue. El stat, mientras tanto, queda topeado en 35
## por el tope provisorio que registra cada archivo de quests de la linea.

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
            "puerta_dejar_pasar_tarde",     # ingresar a su habitacion de tarde
            "accion_jugar",                 # se puede unir a la accion Jugar
            "juegos_nuevos",                # opcion propia en su menu
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
        ventajas=[
            # "Muy Buen Humor" estaba en el hito de amor 20. Se subio acá al
            # darle a ese hito sus tres ventajas propias. Sigue siendo el
            # escalon sobre "Buen Humor" del 10.
            "talk_estado_muy_buen_humor",
            "accion_beso_amor",             # besarla, una vez por dia
            "ropa_nueva",                   # se prueba ropa en su habitacion
        ],
    ))

    # Marcador de que la linea sigue. NUNCA se otorga (proximamente=True), asi
    # que el panel lo muestra siempre en gris. Sin ventajas y sin quest_id.
    registrar_hito(Hito(
        id="violet_hito_amor_04",
        npc_id="violet",
        stat="amor",
        umbral=40,
        nombre="Próximamente",
        descripcion="Nuevo contenido en futuras actualizaciones.",
        icono="❤️",
        proximamente=True,
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
            "talk_estado_insinuante",       # escalon previo a "Hot"
            "talk_memoria_total",           # recuerda todo lo que probe con ella
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
        ventajas=[
            "puerta_dejar_pasar_noche",     # ingresar a su habitacion de noche
            "accion_ver_anime",             # se puede unir a la accion Ver Anime
            "mensajear",                    # escribirle por el chat cuando quiera
        ],
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
        ventajas=[
            # "Hot" (el estado que antes se llamaba "Caliente") estaba en el hito
            # de deseo 20. Se subio acá al darle a ese hito sus tres ventajas
            # propias. Sigue siendo el escalon sobre "Insinuante" del 10.
            "talk_estado_caliente",
            "accion_beso_deseo",            # besarla, una vez por dia
            "provocacion",                  # ella provoca: la puerta del baño
        ],
    ))

    registrar_hito(Hito(
        id="violet_hito_deseo_04",
        npc_id="violet",
        stat="deseo",
        umbral=40,
        nombre="Próximamente",
        descripcion="Nuevo contenido en futuras actualizaciones.",
        icono="💋",
        proximamente=True,
    ))

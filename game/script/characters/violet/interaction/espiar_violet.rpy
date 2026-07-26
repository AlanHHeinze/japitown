################################################################################
## Espiar — Contenido de Violet
################################################################################
## Secuencias espiables de Violet en el baño + reacciones al ser descubierto.
## El motor está en script/core/espiar/espiar_system.rpy.
##
## Para agregar una secuencia: copiar un bloque registrar_secuencia_espiar y
## cambiar id/fondo/fotos. Para condicionar una secuencia a una quest/evento,
## pasar condicion=funcion_de_modulo (definida en init python, nunca lambda).

init 6 python:

    # ── Secuencias ───────────────────────────────────────────────────────────

    registrar_secuencia_espiar(SecuenciaEspiar(
        id="violet_espiar_ducha",
        npc_id="violet",
        nombre="Violet en la ducha",
        fondo="images/minijuegos/ducha_test/secuencias_placeholder_ducha_fondo.jpg",
        fotos=[
            {"ruta": "images/minijuegos/ducha_test/foto_ducha_ducha_1.jpg",
             "descripcion": "Violet en la ducha"},
        ],
    ))

    registrar_secuencia_espiar(SecuenciaEspiar(
        id="violet_espiar_tanga",
        npc_id="violet",
        nombre="Violet en tanga",
        fondo="images/minijuegos/ducha_test/secuencias_placeholder_tanga_fondo.jpg",
        fotos=[
            {"ruta": "images/minijuegos/ducha_test/foto_ducha_tanga_1.jpg",
             "descripcion": "Violet en tanga"},
        ],
    ))

    registrar_secuencia_espiar(SecuenciaEspiar(
        id="violet_espiar_descambiada",
        npc_id="violet",
        nombre="Violet descambiada",
        fondo="images/minijuegos/ducha_test/secuencias_placeholder_descambiada_fondo.jpg",
        fotos=[
            {"ruta": "images/minijuegos/ducha_test/foto_ducha_descambiada_1.jpg",
             "descripcion": "Violet descambiada"},
        ],
    ))

    # ── Reacciones al ser descubierto ────────────────────────────────────────
    # La primera vez corre el label especial (sin cambio de stats). Las
    # siguientes aplican el rango segun el deseo actual de Violet.

    registrar_espiar_npc(
        "violet",
        label_primera_vez="espiar_violet_primera_vez",
        reacciones=[
            {"min": 0,  "max": 29,  "amor": -4, "deseo": -2},  # Se enfada
            {"min": 30, "max": 50},                             # No pasa nada
            {"min": 51, "max": 100, "deseo": 2},                # Le gusta
        ],
    )


################################################################################
## Label: Primera vez que Violet descubre al jugador
################################################################################
## ESCENA DE TEST — los dos cara a cara dentro del baño.
##
## Se llama con `call expression` desde espiar_descubierto, asi que DEBE
## terminar en `return` (nunca `jump game_loop`): quien llamó se encarga de
## cerrar el flujo — avanza el horario, restaura el fondo del pasillo y vuelve
## el HUD. Terminar con jump acá dejaría el frame de la llamada sin cerrar y el
## call stack creceria en cada espiada.
##
## Tampoco toca stats: la primera vez reemplaza la reacción por deseo.

label espiar_violet_primera_vez:

    # Fondo del baño donde está Violet. La property .background de la locación
    # ya resuelve el horario actual, asi que la escena queda en la hora que
    # corresponde sin armar la ruta a mano.
    $ _ev1_banio_loc = sistema_locaciones.obtener_locacion(obtener_npc("violet").locacion_actual)
    if _ev1_banio_loc and _ev1_banio_loc.background:
        scene expression _ev1_banio_loc.background with fade

    # Cara a cara: mc_cerca y npc_cerca se encuentran en x=960 (el MC mira a la
    # derecha, Violet a la izquierda).
    show mc_parado_base c_rbase_base o_base b_seria at mc_cerca

    # `show` necesita nombres de atributo literales, asi que la ropa activa se
    # resuelve ramificando (mismo patrón que las quests de Violet).
    $ _ev1_cuerpo_v = cuerpo_activo("violet")
    if _ev1_cuerpo_v == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_enojados b_gritandomucho at npc_cerca
    else:
        show violet_parada c_rbase_base ca_base o_enojados b_gritandomucho at npc_cerca

    with sprite_normal

    violet "¡¿Q-qué estás haciendo ahí?!"

    show mc_parado_base b_hablando
    mc "¡Nada! Pasaba por el pasillo y la puerta estaba así..."

    show violet_parada o_juzgandonm b_hablando
    violet "La puerta estaba cerrada. Yo la cerré."

    show mc_parado_base b_seria o_abajonm
    piensa "No tengo forma de salir bien parado de esta."

    show violet_parada o_enojados b_hablando
    violet "Andate. Y no vuelvas a hacer eso."

    return

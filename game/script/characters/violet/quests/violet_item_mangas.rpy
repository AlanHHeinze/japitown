################################################################################
## Mangas de Violet — Item de lectura
################################################################################
## Item no comprable. El jugador lo recibe durante la quest 01_b.
## Se puede leer 4 veces en la habitación del MC.
## Al terminar la 4ta lectura activa mangas_violet_terminadas = True,
## variable que las quests pueden escuchar como condición.

# =============================================================================
# VARIABLES
# =============================================================================

# Cantidad de lecturas completadas (0 a 4)
default mangas_violet_lecturas = 0

# True al completar la 4ta lectura — las quests escuchan esta variable
default mangas_violet_terminadas = False

# Dia (dias_totales) en que se hizo la ultima lectura — controla limite de 1 por dia
default mangas_violet_ultimo_dia = -1


################################################################################
## LABEL: Usar item mangas_violet_mc
################################################################################

label usar_mangas_violet_mc:

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    $ _horarios_bg_manga = ["mañana", "tarde", "noche", "noche"]
    $ _bg_h_manga = _horarios_bg_manga[horario_actual]
    scene expression "images/bg/casa/bg_casa_" + _bg_h_manga + "_hmc.png" with fade

    if horario_actual == 3:
        piensa "Es muy tarde para ponerme a leer, sera mejor hacerlo mañana"
        window hide
        $ mostrar_hud()
        jump game_loop

    if mangas_violet_terminadas:
        piensa "Ya los terminé, debería devolvérselos a Violet"
        window hide
        $ mostrar_hud()
        jump game_loop

    if mangas_violet_ultimo_dia == dias_totales:
        piensa "Ya un tomo fue suficiente por hoy, podría leer el proximo mañana"
        window hide
        $ mostrar_hud()
        jump game_loop

    $ mangas_violet_ultimo_dia = dias_totales
    $ mangas_violet_lecturas += 1

    show mc_parado_base c_rbase_leyendocyberpunk o_base b_none at Transform(xalign=0.5, yalign=1.0) with dissolve

    if mangas_violet_lecturas == 1:
        piensa "El mundo esta bien plasmado y el prota un joven bien común, al que el mundo no le da respiro, me gusta bastante"

    elif mangas_violet_lecturas == 2:
        piensa "Se puso intenso, ya está metido de lleno en el mundo y encontró un grupo donde por fin pertenece"

    elif mangas_violet_lecturas == 3:
        piensa "Bien llevado como el mundo lo absorve y convierte a media que va perdiendo cosas"

    elif mangas_violet_lecturas == 4:
        piensa "Uff... duro...  El final duele pero se siente como la única forma posible de cerrar todo"
        piensa "La verdad supero espectativas, ahora quiero hablar con Violet y seahogar algunas cosas"
        $ mangas_violet_terminadas = True
        $ completar_quest_actual("violet")

    hide mc_parado_base with dissolve
    $ avanzar_horario()
    window hide
    $ mostrar_hud()
    jump game_loop

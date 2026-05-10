################################################################################
## Sistema de Pensamientos
################################################################################
## Permite al jugador "pensar" antes de dormir, accediendo a labels narrativos
## repetibles que se desbloquean al completar ciertos eventos del juego.

################################################################################
## Registro y lógica
################################################################################

init 5 python:

    pensamientos_registrados = {}

    def registrar_pensamiento(id, npc_id, nombre, label, condicion):
        """Registra un pensamiento en el catálogo."""
        pensamientos_registrados[id] = {
            "npc_id": npc_id,
            "nombre": nombre,
            "label": label,
            "condicion": condicion,
        }

    def obtener_pensamientos_disponibles():
        """Retorna dict de pensamientos cuya condición se cumple."""
        resultado = {}
        for k, v in pensamientos_registrados.items():
            try:
                if v["condicion"]():
                    resultado[k] = v
            except:
                pass
        return resultado

################################################################################
## Registro de pensamientos por NPC
################################################################################

init 6 python:

    ## Violet - Pensamiento 1 (se desbloquea al completar Evento 2)
    registrar_pensamiento(
        id="violet_pensamiento_1",
        npc_id="violet",
        nombre="Pensar en Violet...",
        label="evento2_violet_repetir",
        condicion=lambda: store.violet_evento2_completado,
    )

################################################################################
## Screen de selección de pensamientos
################################################################################

screen menu_pensamientos(pensamientos_dict):

    modal True

    # Fondo oscuro semi-transparente
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background "#00000088"
        action Return("volver")

    # Panel central
    frame:
        xalign 0.5
        yalign 0.5
        xsize 420
        ypadding 20
        xpadding 20
        background "#1a1a2e"

        vbox:
            spacing 10
            xfill True

            text "En qué quieres pensar?" size 22 color "#ffffff" xalign 0.5

            null height 10

            # Lista de pensamientos disponibles
            for p_id, p_data in pensamientos_dict.items():
                button:
                    xfill True
                    background "#009688"
                    hover_background "#4DB6AC"
                    padding (15, 10)
                    action Return(p_data["label"])
                    text "💭 [p_data['nombre']]" size 18 color "#ffffff"

            null height 5

            # Boton volver
            button:
                xfill True
                background "#333355"
                hover_background "#444466"
                padding (15, 10)
                action Return("volver")
                text "Volver" size 18 color "#aaaaaa" xalign 0.5

################################################################################
## Screens — Quest 1 de Monica (La notebook)
################################################################################
## Pantalla del instalador con 5 pasos.
## Cada paso tiene 3 opciones, solo una es correcta (no instalar extras).

init python:

    # Datos del instalador: cada paso tiene un título, opciones y cuál es la correcta
    _mq1_pasos_instalador = [
        {
            "titulo": "Paso 1 de 5 — Componentes adicionales",
            "descripcion": "El instalador quiere agregar componentes opcionales.",
            "opciones": [
                {"texto": "Instalar barra de herramientas WebSearch Plus", "correcta": False},
                {"texto": "Instalar solo el programa solicitado", "correcta": True},
                {"texto": "Instalar pack de optimizacion del sistema", "correcta": False},
            ],
        },
        {
            "titulo": "Paso 2 de 5 — Navegador predeterminado",
            "descripcion": "El instalador quiere cambiar tu navegador.",
            "opciones": [
                {"texto": "Establecer QuickBrowser como navegador predeterminado", "correcta": False},
                {"texto": "Instalar extension de busqueda rapida", "correcta": False},
                {"texto": "No realizar cambios en el navegador", "correcta": True},
            ],
        },
        {
            "titulo": "Paso 3 de 5 — Pagina de inicio",
            "descripcion": "El instalador quiere modificar la pagina de inicio.",
            "opciones": [
                {"texto": "Mantener la configuracion actual", "correcta": True},
                {"texto": "Cambiar pagina de inicio a SearchMaster", "correcta": False},
                {"texto": "Agregar SearchMaster como pagina secundaria", "correcta": False},
            ],
        },
        {
            "titulo": "Paso 4 de 5 — Software complementario",
            "descripcion": "El instalador recomienda software adicional.",
            "opciones": [
                {"texto": "Instalar CleanPC Pro (version de prueba)", "correcta": False},
                {"texto": "Instalar MediaPlayer Ultimate", "correcta": False},
                {"texto": "Omitir instalacion de software adicional", "correcta": True},
            ],
        },
        {
            "titulo": "Paso 5 de 5 — Finalizacion",
            "descripcion": "Ultimo paso antes de completar la instalacion.",
            "opciones": [
                {"texto": "Completar instalacion y agregar accesos directos al escritorio", "correcta": False},
                {"texto": "Completar instalacion sin modificaciones adicionales", "correcta": True},
                {"texto": "Completar instalacion e iniciar diagnostico del sistema", "correcta": False},
            ],
        },
    ]


################################################################################
## Screen del instalador
################################################################################

screen monica_quest1_pantalla_instalador(paso):

    modal True

    # Fondo simulando pantalla de notebook
    add Solid("#0a0a1a")

    frame:
        xalign 0.5
        yalign 0.5
        xysize (800, 550)
        background "#e8e8f0"
        padding (0, 0)

        vbox:
            # Barra de titulo del instalador
            frame:
                xfill True
                background "#2855a0"
                padding (15, 10)

                hbox:
                    spacing 10
                    text "📦 WorkSuite Installer" size 18 color "#ffffff" bold True
                    null
                    text "v3.2.1" size 12 color "#aaccff" yalign 0.5

            # Contenido del instalador
            frame:
                xfill True
                yfill True
                background "#f5f5fa"
                padding (30, 25)

                $ _paso_data = _mq1_pasos_instalador[paso - 1]

                vbox:
                    spacing 20

                    # Titulo del paso
                    text _paso_data["titulo"] size 20 color "#333333" bold True

                    # Barra de progreso
                    frame:
                        xfill True
                        ysize 8
                        background "#ccccdd"

                        frame:
                            xsize int(800 * paso / 5)
                            ysize 8
                            background "#2855a0"

                    # Descripcion
                    text _paso_data["descripcion"] size 15 color "#555555"

                    null height 5

                    # Opciones como checkboxes
                    for _i, _opcion in enumerate(_paso_data["opciones"]):
                        button:
                            xfill True
                            if _opcion["correcta"]:
                                action Return("correcta")
                            else:
                                action Return("incorrecta")

                            frame:
                                xfill True
                                background "#ffffff"
                                hover_background "#e0e8ff"
                                padding (15, 12)

                                hbox:
                                    spacing 12
                                    yalign 0.5

                                    # Checkbox visual
                                    frame:
                                        xysize (22, 22)
                                        background "#ccccdd"
                                        yalign 0.5

                                    text _opcion["texto"] size 14 color "#333333" yalign 0.5

                    # Texto informativo
                    text "Seleccione una opcion para continuar" size 12 color "#888888" xalign 0.5

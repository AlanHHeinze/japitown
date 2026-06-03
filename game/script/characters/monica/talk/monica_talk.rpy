################################################################################
## Talk — Mónica
################################################################################

init 10 python:

    def _monica_cond_locion():
        return (
            store.inventario.get("locion_masajes", 0) > 0 and
            getattr(store.sistema_talk.obtener_estado_activo("monica"), "id", None) == "monica_cansada"
        )

    def _monica_recompensa_locion():
        npc = obtener_npc("monica")
        if npc:
            npc.modificar_stat2(1)

    def _monica_cond_tareas():
        return (
            store.mc_destreza >= 3 and
            getattr(store.sistema_talk.obtener_estado_activo("monica"), "id", None) == "monica_ocupada"
        )

    def _monica_recompensa_tareas():
        npc = obtener_npc("monica")
        if npc:
            npc.modificar_stat2(1)

    def inicializar_talk_monica():

        # ==================================================================
        # ESTADOS GENERALES
        # ==================================================================

        estados_monica = [

            EstadoTalk(
                id="monica_cansada",
                nombre="Cansada",
                intro="Mónica parece estar cansada.",
                efectos={
                    "complacerla": "+1_deseo",
                    "provocarla":  "-1_deseo",
                    "escucharla":  "nada",
                    "hablarle":    "nada",
                    "adularla":    "+2_amor",
                },
                mensaje="ella estaba cansada.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="monica_ocupada",
                nombre="Ocupada",
                intro="Mónica parece estar ocupada con algo.",
                efectos={
                    "complacerla": "+2_amor",
                    "provocarla":  "-2_amor",
                    "escucharla":  "+1_deseo",
                    "hablarle":    "nada",
                    "adularla":    "nada",
                },
                mensaje="ella estaba ocupada con sus cosas.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="monica_picante",
                nombre="Picante",
                intro="Mónica tiene un brillo picante en los ojos.",
                efectos={
                    "complacerla": "-1_deseo",
                    "provocarla":  "+1_deseo",
                    "escucharla":  "nada",
                    "hablarle":    "nada",
                    "adularla":    "+2_amor",
                },
                mensaje="ella estaba de humor picante.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="monica_alegre",
                nombre="Alegre",
                intro="Mónica parece estar de muy buen humor.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "-2_amor",
                    "escucharla":  "+1_deseo",
                    "hablarle":    "+2_amor",
                    "adularla":    "nada",
                },
                mensaje="ella estaba de muy buen humor.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="monica_energica",
                nombre="Enérgica",
                intro="Mónica está llena de energía.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "+2_amor",
                    "escucharla":  "-1_deseo",
                    "hablarle":    "nada",
                    "adularla":    "+1_deseo",
                },
                mensaje="ella estaba llena de energía.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="monica_abierta",
                nombre="Abierta",
                intro="Mónica parece estar abierta y receptiva.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "nada",
                    "escucharla":  "+2_amor",
                    "hablarle":    "+1_deseo",
                    "adularla":    "-2_amor",
                },
                mensaje="ella estaba abierta y receptiva.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            # ==================================================================
            # ESTADOS ESPECIALES (se activan desde quests, eventos, items, etc.)
            # ==================================================================

            EstadoTalk(
                id="monica_feliz",
                nombre="Feliz",
                intro="Mónica parece estar especialmente feliz hoy.",
                efectos={
                    "complacerla": "+2_amor",
                    "provocarla":  "+1_deseo",
                    "escucharla":  "+2_amor",
                    "hablarle":    "+2_amor",
                    "adularla":    "+1_deseo",
                },
                mensaje="ella estaba especialmente feliz.",
                es_especial=True,
                jerarquia=5,
                dias_duracion=2,
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                },
            ),

        ]

        estados_generales_ids = [
            "monica_cansada",
            "monica_ocupada",
            "monica_picante",
            "monica_alegre",
            "monica_energica",
            "monica_abierta",
        ]

        opciones_especiales_monica = [

            OpcionEspecialTalk(
                id="monica_locion",
                texto="Darle la loción",
                condicion=_monica_cond_locion,
                mensaje_opcion="Le ofreciste la loción de masajes.",
                resultado_id="+2_amor",
                item_requerido="locion_masajes",
                item_consumible=True,
                estado_posterior_npc="posterior_feliz",
                recompensa_extra=_monica_recompensa_locion,
            ),

            OpcionEspecialTalk(
                id="monica_tareas",
                texto="Ayudarla con cosas de la casa",
                condicion=_monica_cond_tareas,
                mensaje_opcion="Te ofreciste a ayudarla con las tareas de la casa.",
                resultado_id="+2_amor",
                item_requerido=None,
                item_consumible=False,
                estado_posterior_npc="posterior_feliz",
                recompensa_extra=_monica_recompensa_tareas,
            ),

        ]

        # ==================================================================
        # MENSAJES
        # ==================================================================

        mensaje_general = "Tuviste un momento de conversación con Mónica."

        mensajes_opciones = {
            "complacerla": "Elegiste complacerla.",
            "provocarla":  "Decidiste provocarla.",
            "escucharla":  "Te dedicaste a escucharla.",
            "hablarle":    "Fuiste directo y le hablaste.",
            "adularla":    "La adulaste.",
        }

        resoluciones = {
            "+2_amor":  "Y quedó muy satisfecha con la interacción.",
            "+1_deseo": "Y se mostró más interesada en vos.",
            "-2_amor":  "Y quedó muy molesta con la situación.",
            "-1_deseo": "Y se alejó un poco de vos.",
            "nada":     "La interacción no tuvo un efecto particular.",
        }

        # ==================================================================
        # REGISTRAR
        # ==================================================================

        config = ConfigTalkNPC(
            npc_id="monica",
            mensaje_general=mensaje_general,
            mensajes_opciones=mensajes_opciones,
            resoluciones=resoluciones,
            estados=estados_monica,
            estados_generales_ids=estados_generales_ids,
            opciones_especiales=opciones_especiales_monica,
            resoluciones_especiales={
                "monica_locion": "Y lo que le diste fue justo lo que necesitaba.",
            },
        )

        sistema_talk.registrar_config(config)

init 11 python:
    inicializar_talk_monica()

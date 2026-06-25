################################################################################
## Talk — Jasmine
################################################################################

init 10 python:

    def _jasmine_cond_bebida():
        return (
            store.inventario.get("bebida_energetica", 0) > 0 and
            getattr(store.sistema_talk.obtener_estado_activo("jasmine"), "id", None) == "jasmine_agotada"
        )

    def _jasmine_recompensa_bebida():
        npc = obtener_npc("jasmine")
        if npc:
            npc.modificar_stat2(1)

    def _jasmine_cond_entrenar():
        return (
            store.mc_fuerza >= 3 and
            getattr(store.sistema_talk.obtener_estado_activo("jasmine"), "id", None) == "jasmine_energica"
        )

    def _jasmine_recompensa_entrenar():
        npc = obtener_npc("jasmine")
        if npc:
            npc.modificar_stat2(1)

    def inicializar_talk_jasmine():

        # ==================================================================
        # ESTADOS GENERALES
        # ==================================================================

        estados_jasmine = [

            EstadoTalk(
                id="jasmine_provocativa",
                nombre="Provocativa",
                intro="Jasmine parece estar en humor provocativo.",
                efectos={
                    "complacerla": "+2_amor",
                    "provocarla":  "+1_deseo",
                    "escucharla":  "nada",
                    "hablarle":    "-1_deseo",
                    "adularla":    "nada",
                },
                mensaje="ella estaba de humor provocativo.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="jasmine_celosa",
                nombre="Celosa",
                intro="Jasmine parece estar celosa.",
                efectos={
                    "complacerla": "+1_deseo",
                    "provocarla":  "nada",
                    "escucharla":  "+2_amor",
                    "hablarle":    "-2_amor",
                    "adularla":    "nada",
                },
                mensaje="ella estaba celosa.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="jasmine_tranquila",
                nombre="Tranquila",
                intro="Jasmine parece estar tranquila y relajada.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "nada",
                    "escucharla":  "-1_deseo",
                    "hablarle":    "+2_amor",
                    "adularla":    "+1_deseo",
                },
                mensaje="ella estaba tranquila y relajada.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="jasmine_alegre",
                nombre="Alegre",
                intro="Jasmine parece estar de muy buen humor.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "nada",
                    "escucharla":  "-2_amor",
                    "hablarle":    "+1_deseo",
                    "adularla":    "+2_amor",
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
                id="jasmine_energica",
                nombre="Enérgica",
                intro="Jasmine está llena de energía.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "+2_amor",
                    "escucharla":  "-1_deseo",
                    "hablarle":    "+1_deseo",
                    "adularla":    "nada",
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
                id="jasmine_agotada",
                nombre="Agotada",
                intro="Jasmine parece estar agotada.",
                efectos={
                    "complacerla": "+1_deseo",
                    "provocarla":  "-2_amor",
                    "escucharla":  "+2_amor",
                    "hablarle":    "nada",
                    "adularla":    "nada",
                },
                mensaje="ella estaba agotada.",
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
                id="jasmine_feliz",
                nombre="Feliz",
                intro="Jasmine parece estar especialmente feliz hoy.",
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
            "jasmine_provocativa",
            "jasmine_celosa",
            "jasmine_tranquila",
            "jasmine_alegre",
            "jasmine_energica",
            "jasmine_agotada",
        ]

        opciones_especiales_jasmine = [

            OpcionEspecialTalk(
                id="jasmine_bebida",
                texto="Darle la bebida",
                condicion=_jasmine_cond_bebida,
                mensaje_opcion="Le ofreciste una bebida energética.",
                resultado_id="+2_amor",
                item_requerido="bebida_energetica",
                item_consumible=True,
                estado_posterior_npc="posterior_feliz",
                recompensa_extra=_jasmine_recompensa_bebida,
            ),

            OpcionEspecialTalk(
                id="jasmine_entrenar",
                texto="Entrenar juntos",
                condicion=_jasmine_cond_entrenar,
                mensaje_opcion="La propusiste salir a entrenar juntos.",
                resultado_id="+2_amor",
                item_requerido=None,
                item_consumible=False,
                estado_posterior_npc="posterior_feliz",
                recompensa_extra=_jasmine_recompensa_entrenar,
            ),

        ]

        # ==================================================================
        # MENSAJES
        # ==================================================================

        mensaje_general = "Tuviste un momento de conversación con Jasmine."

        mensajes_opciones = {
            "complacerla": "Elegiste complacerla.",
            "provocarla":  "Decidiste provocarla.",
            "escucharla":  "Te dedicaste a escucharla.",
            "hablarle":    "Fuiste directo y le hablaste.",
            "adularla":    "La adulaste.",
        }

        resoluciones = {
            "+2_amor":  "Y quedó muy satisfecha con la interacción.",
            "+1_deseo": "Y se mostró más interesada en ti.",
            "-2_amor":  "Y quedó muy molesta con la situación.",
            "-1_deseo": "Y se alejó un poco de ti.",
            "nada":     "La interacción no tuvo un efecto particular.",
        }

        # ==================================================================
        # REGISTRAR
        # ==================================================================

        config = ConfigTalkNPC(
            npc_id="jasmine",
            mensaje_general=mensaje_general,
            mensajes_opciones=mensajes_opciones,
            resoluciones=resoluciones,
            estados=estados_jasmine,
            estados_generales_ids=estados_generales_ids,
            opciones_especiales=opciones_especiales_jasmine,
            resoluciones_especiales={
                "jasmine_bebida": "Y lo que le diste fue justo lo que necesitaba.",
            },
        )

        sistema_talk.registrar_config(config)

init 11 python:
    inicializar_talk_jasmine()

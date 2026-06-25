################################################################################
## Talk — Violet
################################################################################

init 10 python:

    def _violet_cond_golosinas():
        return (
            store.inventario.get("golosinas", 0) > 0 and
            getattr(store.sistema_talk.obtener_estado_activo("violet"), "id", None) == "violet_hambre"
        )

    def _violet_recompensa_golosinas():
        npc = obtener_npc("violet")
        if npc:
            npc.modificar_stat2(1)

    def _violet_cond_videojuegos():
        return (
            store.mc_inteligencia >= 3 and
            getattr(store.sistema_talk.obtener_estado_activo("violet"), "id", None) == "violet_ansiosa"
        )

    def _violet_recompensa_videojuegos():
        npc = obtener_npc("violet")
        if npc:
            npc.modificar_stat2(1)

    def inicializar_talk_violet():

        # ==================================================================
        # ESTADOS GENERALES (se asignan aleatoriamente al despertar)
        # ==================================================================

        estados_violet = [

            EstadoTalk(
                id="violet_defensiva",
                nombre="Defensiva",
                intro="Violet parece estar a la defensiva hoy.",
                efectos={
                    "complacerla": "+1_deseo",
                    "provocarla":  "nada",
                    "escucharla":  "nada",
                    "hablarle":    "+2_amor",
                    "adularla":    "-1_deseo",
                },
                mensaje="ella estaba a la defensiva.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="violet_molesta",
                nombre="Molesta",
                intro="Violet parece estar molesta.",
                efectos={
                    "complacerla": "-2_amor",
                    "provocarla":  "nada",
                    "escucharla":  "+1_deseo",
                    "hablarle":    "+2_amor",
                    "adularla":    "nada",
                },
                mensaje="ella estaba molesta.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="violet_dormida",
                nombre="Dormida",
                intro="Violet parece tener sueño.",
                efectos={
                    "complacerla": "+2_amor",
                    "provocarla":  "nada",
                    "escucharla":  "nada",
                    "hablarle":    "-1_deseo",
                    "adularla":    "+1_deseo",
                },
                mensaje="ella estaba somnolienta y apenas despierta.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="violet_hambre",
                nombre="Hambre",
                intro="Violet parece tener hambre.",
                efectos={
                    "complacerla": "+1_deseo",
                    "provocarla":  "-2_amor",
                    "escucharla":  "nada",
                    "hablarle":    "+2_amor",
                    "adularla":    "nada",
                },
                mensaje="ella tenía hambre y estaba irritada.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="violet_ansiosa",
                nombre="Ansiosa",
                intro="Violet parece estar ansiosa.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "-1_deseo",
                    "escucharla":  "+2_amor",
                    "hablarle":    "+1_deseo",
                    "adularla":    "nada",
                },
                mensaje="ella estaba ansiosa y nerviosa.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            EstadoTalk(
                id="violet_sumisa",
                nombre="Sumisa",
                intro="Violet parece estar especialmente dócil hoy.",
                efectos={
                    "complacerla": "nada",
                    "provocarla":  "+1_deseo",
                    "escucharla":  "-2_amor",
                    "hablarle":    "nada",
                    "adularla":    "+2_amor",
                },
                mensaje="ella estaba inusualmente dócil.",
                estados_posteriores={
                    "+2_amor":  "posterior_feliz",
                    "+1_deseo": "posterior_hot",
                    "-2_amor":  "posterior_molesta",
                    "-1_deseo": "posterior_cerrada",
                    "nada":     "posterior_indiferente",
                },
            ),

            # ==================================================================
            # ESTADOS CONDICIONALES (se suman al pool cuando se cumplen requisitos)
            # ==================================================================

            EstadoTalk(
                id="violet_buen_humor",
                nombre="Buen Humor",
                intro="Violet parece estar de buen humor hoy.",
                efectos={
                    "complacerla": "+2_amor",
                    "provocarla":  "+1_amor",
                    "escucharla":  "+1_amor",
                    "hablarle":    "+1_amor",
                    "adularla":    "+2_amor",
                },
                mensaje="ella estaba de buen humor.",
                condicion=lambda: store.violet_amor >= 15,
                estados_posteriores={
                    "+2_amor": "posterior_feliz",
                    "+1_amor": "posterior_feliz",
                },
            ),

            EstadoTalk(
                id="violet_muy_buen_humor",
                nombre="Muy Buen Humor",
                intro="Violet parece estar de muy buen humor hoy.",
                efectos={
                    "complacerla": "+2_amor",
                    "provocarla":  "+2_amor",
                    "escucharla":  "+4_amor",
                    "hablarle":    "+4_amor",
                    "adularla":    "+2_amor",
                },
                mensaje="ella estaba de muy buen humor.",
                condicion=lambda: store.violet_amor >= 15,
                estados_posteriores={
                    "+2_amor": "posterior_feliz",
                    "+4_amor": "posterior_feliz",
                },
            ),

            EstadoTalk(
                id="violet_caliente",
                nombre="Caliente",
                intro="Violet parece estar en un estado de ánimo especial hoy.",
                efectos={
                    "complacerla": "+1_deseo",
                    "provocarla":  "+2_deseo",
                    "escucharla":  "+1_deseo",
                    "hablarle":    "+1_deseo",
                    "adularla":    "+2_deseo",
                },
                mensaje="ella estaba en un estado de ánimo especial.",
                condicion=lambda: store.violet_deseo >= 30,
                estados_posteriores={
                    "+1_deseo": "posterior_hot",
                    "+2_deseo": "posterior_hot",
                },
            ),

            # ==================================================================
            # ESTADOS ESPECIALES (se activan desde quests, eventos, items, etc.)
            # ==================================================================

            EstadoTalk(
                id="violet_feliz",
                nombre="Feliz",
                intro="Violet parece estar especialmente feliz hoy.",
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
            "violet_defensiva",
            "violet_molesta",
            "violet_dormida",
            "violet_hambre",
            "violet_ansiosa",
            "violet_sumisa",
            "violet_buen_humor",
            "violet_muy_buen_humor",
            "violet_caliente",
        ]

        # ==================================================================
        # OPCIONES ESPECIALES
        # Agregar acá cuando se definan.
        # ==================================================================

        opciones_especiales_violet = [

            OpcionEspecialTalk(
                id="violet_golosinas",
                texto="Darle golosinas",
                condicion=_violet_cond_golosinas,
                mensaje_opcion="Le ofreciste unas golosinas.",
                resultado_id="+2_amor",
                item_requerido="golosinas",
                item_consumible=True,
                estado_posterior_npc="posterior_feliz",
                recompensa_extra=_violet_recompensa_golosinas,
            ),

            OpcionEspecialTalk(
                id="violet_videojuegos",
                texto="Jugar videojuegos",
                condicion=_violet_cond_videojuegos,
                mensaje_opcion="La invitaste a jugar videojuegos.",
                resultado_id="+2_amor",
                item_requerido=None,
                item_consumible=False,
                estado_posterior_npc="posterior_feliz",
                recompensa_extra=_violet_recompensa_videojuegos,
            ),

        ]

        # ==================================================================
        # MENSAJES DEL SISTEMA (4 partes del resultado)
        # ==================================================================

        mensaje_general = "Tuviste un momento de conversación con Violet."

        mensajes_opciones = {
            "complacerla": "Elegiste complacerla.",
            "provocarla":  "Decidiste provocarla.",
            "escucharla":  "Te dedicaste a escucharla.",
            "hablarle":    "Fuiste directo y le hablaste.",
            "adularla":    "La adulaste.",
        }

        resoluciones = {
            "+1_amor":  "Y quedó satisfecha con la interacción.",
            "+2_amor":  "Y quedó muy satisfecha con la interacción.",
            "+4_amor":  "Y quedó emocionada con la interacción.",
            "+1_deseo": "Y se mostró más interesada en ti.",
            "+2_deseo": "Y se mostró bastante más interesada en ti.",
            "-2_amor":  "Y quedó muy molesta con la situación.",
            "-1_deseo": "Y se alejó un poco de ti.",
            "nada":     "La interacción no tuvo un efecto particular.",
        }

        resoluciones_especiales = {
            "violet_golosinas": "Y lo que le diste fue justo lo que necesitaba.",
        }

        # ==================================================================
        # REGISTRAR
        # ==================================================================

        config = ConfigTalkNPC(
            npc_id="violet",
            mensaje_general=mensaje_general,
            mensajes_opciones=mensajes_opciones,
            resoluciones=resoluciones,
            estados=estados_violet,
            estados_generales_ids=estados_generales_ids,
            opciones_especiales=opciones_especiales_violet,
            resoluciones_especiales=resoluciones_especiales,
        )

        sistema_talk.registrar_config(config)

init 11 python:
    inicializar_talk_violet()

# TODO: Translation updated at 2026-04-21 21:46

# game/script/core/locations/door_access_system.rpy:156
translate english interaccion_puerta_npc_4722142a:

    # piensa "[_msg_ausente]"
    piensa "[_msg_ausente]"

# game/script/core/locations/door_access_system.rpy:161
translate english interaccion_puerta_npc_bbbd1a95:

    # piensa "Debe estar durmiendo, no voy a molestar."
    piensa "She must be asleep. I won't bother her."

translate english strings:

    ############################################################################
    ## Respuestas del NPC en la puerta (MENSAJES_NPC_PUERTA, door_relation_system)
    ############################################################################
    ## Antes eran diálogo literal (monica "Adelante.") y por eso estaban en
    ## bloques de traducción por hash. Al pasarlas al dict se muestran por
    ## interpolación (monica "[_msg_adelante]"), que NO traduce: ahora las traduce
    ## mensaje_puerta_npc() y necesitan un `old` acá.

    ## Bloqueos de golpe (BLOQUEOS_GOLPE_REGISTRO, refactor C8): antes era
    ## dialogo literal (piensa "Violet debe estar dormida.") y estaba en un
    ## bloque por hash; ahora se muestra por interpolacion y lo traduce
    ## obtener_bloqueo_golpe() via translate_string — necesita un `old` aca.
    old "Violet debe estar dormida."
    new "Violet must be asleep."

    old "Estoy ocupada."
    new "I'm busy."

    old "Ahí salgo."
    new "I'll be right out."

    old "Adelante."
    new "Come in."

    ############################################################################
    ## Mensajes de ausencia (MENSAJES_AUSENTE)
    ############################################################################

    old "Violet no esta en su habitacion."
    new "Violet is not in her room."

    old "Jasmine no esta en su habitacion."
    new "Jasmine is not in her room."

    old "Monica no esta en su habitacion."
    new "Monica is not in her room."

    old "No hay nadie."
    new "Nobody's there."

    ############################################################################
    ## Opciones del menu de puerta (screen menu_puerta_npc)
    ############################################################################

    old "Intentar hablar"
    new "Try to talk"

    old "Dar paquete"
    new "Give package"

    old "Devolver mangas"
    new "Return manga"

    old "Vengo por los mangas"
    new "I'm here for the manga"

    old "Despertar a Violet para limpiar"
    new "Wake up Violet to clean"

    old "Golpear la puerta"
    new "Knock on the door"

    old "Volver"
    new "Return"

# TODO: Translation updated at 2026-05-11 16:31

# game/script/core/locations/door_access_system.rpy:169
translate english interaccion_puerta_npc_cc0f03b1:

    # piensa "Parece que [_npc_nombre_door] no está en casa, debe haber salido."
    piensa "It looks like [_npc_nombre_door] isn't home, she must have gone out."

# game/script/core/locations/door_access_system.rpy:284
translate english interaccion_banio_ocupado_7ce3ca1c:

    # violet "Me estoy bañando."
    violet "I'm in the shower."

# game/script/core/locations/door_access_system.rpy:286
translate english interaccion_banio_ocupado_edf269c3:

    # jasmine "Me estoy bañando."
    jasmine "I'm in the shower."

# game/script/core/locations/door_access_system.rpy:288
translate english interaccion_banio_ocupado_75d1d22a:

    # monica "Me estoy bañando."
    monica "I'm in the shower."

# TODO: Translation updated at 2026-06-25 23:12

# game/script/core/locations/door_access_system.rpy:351
translate english interaccion_puerta_npc_5a6d6d2b:

    # violet "[_msg_ocupada]"
    violet "[_msg_ocupada]"

# game/script/core/locations/door_access_system.rpy:353
translate english interaccion_puerta_npc_da3cfba5:

    # jasmine "[_msg_ocupada]"
    jasmine "[_msg_ocupada]"

# game/script/core/locations/door_access_system.rpy:355
translate english interaccion_puerta_npc_f51ab2e5:

    # monica "[_msg_ocupada]"
    monica "[_msg_ocupada]"

# game/script/core/locations/door_access_system.rpy:368
translate english interaccion_golpear_dejar_pasar_fd1c066b:

    # violet "[_msg_adelante]"
    violet "[_msg_adelante]"

# game/script/core/locations/door_access_system.rpy:370
translate english interaccion_golpear_dejar_pasar_1772d232:

    # jasmine "[_msg_adelante]"
    jasmine "[_msg_adelante]"

# game/script/core/locations/door_access_system.rpy:372
translate english interaccion_golpear_dejar_pasar_ed0f1ecd:

    # monica "[_msg_adelante]"
    monica "[_msg_adelante]"

# game/script/core/locations/door_access_system.rpy:382
translate english interaccion_golpear_sale_pasillo_257bbf2e:

    # violet "[_msg_ahi_salgo]"
    violet "[_msg_ahi_salgo]"

# game/script/core/locations/door_access_system.rpy:384
translate english interaccion_golpear_sale_pasillo_62c5567c:

    # jasmine "[_msg_ahi_salgo]"
    jasmine "[_msg_ahi_salgo]"

# game/script/core/locations/door_access_system.rpy:386
translate english interaccion_golpear_sale_pasillo_b2ec6ef6:

    # monica "[_msg_ahi_salgo]"
    monica "[_msg_ahi_salgo]"

# TODO: Translation updated at 2026-07-31 20:21

# game/script/core/locations/door_access_system.rpy:397
translate english interaccion_puerta_npc_76c9d030:

    # piensa "[_msg_bloqueo_golpe]"
    piensa "[_msg_bloqueo_golpe]"


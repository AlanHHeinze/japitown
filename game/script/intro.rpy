

# Intro

label start:

    #Pedir Nombre
    call choose_name


    # Micro de noche pensando
    scene bg_intro_micro_noche
    show mc_intro_micro_noche oaburrido bcerradae at mc_intro_micro_noche_transform
    with fade
    terminal_micros "Pin Pun Pin Pun"
    terminal_micros "Ultimo llamado para abordar el omnibus con destino a Timesummer en la plataforma 69 que partira en 15 minutos"
    piensa "Que afortunados, yo tengo que esperar 1 hora para que salga el mio por un desperfecto tecnico"
    show mc_intro_micro_noche ocerrados bbostezo
    ""
    show mc_intro_micro_noche obostezo bbostezog
    ""
    show mc_intro_micro_noche ocerrados bcerradae
    "Bostezo"
    show mc_intro_micro_noche oaburrido 
    piensa "Tendria que estar feliz por este viaje, pero la verdad estoy cansado de esto"
    show mc_intro_micro_noche oaburridoc
    piensa "Ya no recuerdo cuantas veces tuve que mudarme en mi vida. Y siempre por culpa del mujeriego de mi padre "
    show mc_intro_micro_noche oaburrido
    piensa "Fue a ver una obra al teatro y de lo unico que hablo fue de la actriz"
    show mc_intro_micro_noche oaburridoc
    piensa "Stalkeando encontro que daba clases de baile y se anoto... sabemos que no para aprender a bailar"
    show mc_intro_micro_noche oaburrido
    piensa "Siete meses despues se caso con ella y el proximo mes planean mudarse juntos"
    show mc_intro_micro_noche oaburridoc
    piensa "El verdadero problema es que su nuevo nidito de amor va a estar en Argentonia"
    show mc_intro_micro_noche opensativo 
    piensa "Siempre dice que hay que seguir al corazon sin escuchar al cerebro. Pero creo que esta vez directamente lo apago"
    show mc_intro_micro_noche obase
    piensa "La verdad que a mi me cuesta mucho eso por mas que lo intente"
    show mc_intro_micro_noche opensativo
    piensa "¿Que haria en su lugar?"
    show mc_intro_micro_noche bbase
    piensa "¿La podria seguir?"
    show mc_intro_micro_noche opajero bbase
    piensa "Puedo imaginarmelo... irme con ella... "
    show mc_intro_micro_noche ocerrados bfeliz


    #Pensando en eva
    show intro_nube_1 as nube1
    vozoff ""
    show intro_nube_2 as nube2
    vozoff ""
    show intro_nube_3 as nube3
    vozoff ""
    show intro_nube_4 as nube4
    vozoff ""
    show intro_nube_eva as nube5
    vozoff ""
    

    #Animacion pensamiento
    show bg_intro_pensamiento at pensamiento_intro
    vozoff ""
    

    # Soñando baile
    scene bg_intro_suenio with fade_white

    show eva intro_baile_1 with dissolve
    vozoff ""
    show eva intro_baile_2 with dissolve
    vozoff ""
    show eva intro_baile_3 with dissolve
    vozoff ""
    show eva intro_baile_4 with dissolve
    vozoff ""
    show eva intro_baile_5 with dissolve
    vozoff ""
    show eva intro_baile_6 with dissolve
    vozoff ""
    eva "Vamos..."
    eva "Ven a vivir a Argentonia conmigo"
    mc "Si mi amor me voy con vos"


    #Animacion beso
    show bg_intro_suenio_beso at beso_micro
    ""
    ""


    #Unos hermoso sueño mas tarde
    scene black with fade 
    show text Text("Un hermoso sueño mas tarde", size=50, color="#FFFFFF", outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause (2.0)
    hide text with dissolve


    #Noticias
    scene bg_intro_noticiero with fade
    rudolf "La inflacion mensual llego al 7.856.165.318.516.565 %%"
    show rudolf intro_hablando
    rudolf "Asi estan las cosas pais{p}Y se las hemos contando"
    show rudolf intro_pestaniando
    ""
    

    #Despertando
    scene bg_intro_micro_noche 
    show mc_intro_micro_noche oasustado basustado with hpunch
    mc "AHHHHHH.... Fue una pesadilla"
    piensa "Espero poder seguir durmiendo despues de esto"
    ""
    ""
    #Hacer la parte que el personaje se despierta y esta en el medio de la nada con el bondi franado porque pincho


    #En este punto quiero que comience la interaccion entre el mc y la azafata 
    call azafata_intro_interaccion
    jump intro_post_azafata


    # --- Interacción con Azafata ---
label azafata_intro_interaccion:

    show azafata intro_base at azafata_entrar with dissolve
    azafata "Buen día señor, estamos esperando que se haga el recambio de un neumático por un desperfecto."
    azafata "Vamos a estar demorados un momento.{p}¿Puedo ayudarlo en algo?"

    mc "Sí... hace un poco de calor, ¿podrías subir el aire acondicionado?"

    azafata "Sí, no hay problema."

    show azafata intro_base at azafata_vuelta
    pause 0.5
    show azafata intro_base at azafata_salir
    pause 1.0
    hide azafata intro_base

    mc "Al menos la atención es buena..."

    # Vuelve a entrar
    show azafata intro_l1 at azafata_entrar
    azafata "Disculpe la demora."
    piensa "¿Tiene levantada la pollera?"
    mc "No hay problema."
    azafata "El panel está algo alto y me cuesta alcanzarlo."
    piensa "Quizás fue por eso..."
    azafata "¿Le parece que así está bien? ¿O quiere que lo baje un poco más?"

    menu:
        "Sí, así está bien.":
            azafata "Perfecto, cualquier cosa me llama de nuevo."
            show azafata intro_l1 at azafata_vuelta
            pause 0.5
            show azafata intro_l1 at azafata_salir
            pause 1.0
            hide azafata intro_l1
            return  # ✅ vuelve al flujo del label que llamó esta escena

        "No, ¿podrías bajarlo un poco más?":
            jump azafata_vuelve


# --- Si el jugador pide que lo baje más ---
label azafata_vuelve:

    azafata "Enseguida."

    show azafata intro_l1 at azafata_vuelta
    pause 0.5
    show azafata intro_l1 at azafata_salir
    pause 1.0
    hide azafata intro_l1

    # Segunda vuelta
    show azafata intro_l2 at azafata_entrar

    azafata "Listo, señor."
    piensa "Ok... volvió a pasar."
    piensa "La temperatura está bien, pero podría pedirle que lo baje más..."
    piensa "Aunque me da un poco de miedo que se dé cuenta y se moleste."
    
    azafata "¿Así está mejor o lo bajo más todavía?"

    menu:
        "Sí, así está bien.":
            azafata "Perfecto, cualquier cosa me llama de nuevo."
            show azafata intro_l2 at azafata_vuelta
            pause 0.5
            show azafata intro_l2 at azafata_salir
            pause 1.0
            hide azafata intro_l2
            return  # ✅ cierre limpio

        "No, todavía hace calor...":
            jump azafata_final


# --- Diálogo final cuando ya no puede bajarlo más ---
label azafata_final:

    azafata "Un momento por favor."
    show azafata intro_l2 at azafata_vuelta
    pause 0.5
    show azafata intro_l2 at azafata_salir
    pause 1.0
    hide azafata intro_l2

    # Tercer regreso
    show azafata intro_l3 at azafata_entrar

    azafata "Señor, ya está en lo más bajo que se puede poner. Espero que esté bien así."
    mc "Sí, así está perfecto."
    azafata "¿Hay algo más con lo que lo pueda ayudar?"
    piensa "Me gustaría disfrutar la vista un poco más... tengo que decir algo."
    mc "¿Cuánto falta para llegar?"
    azafata "¿Hasta dónde va usted?"
    mc "Hasta Japitown."
    azafata "Es la última parada, estaremos llegando a las 18 hs, quizás un poco más por este desperfecto."
    azafata "¿Sigue teniendo calor, señor? Su cara está toda roja."
    mc "Ahora me está dando calor de nuevo."
    azafata "Jajaja, usted es muy raro, incluso ya está haciendo mucho frío, tengo las piernas congeladas."

    show azafata intro_l3 with hpunch
    azafata "¿Qué pasó con mi..."
    show azafata intro_l3 at azafata_vuelta
    ""
    show azafata intro_l3 at azafata_normal
    azafata "Disculpe."
    show azafata intro_l3 at azafata_vuelta
    show azafata intro_l3 at azafata_salir
    vozoff "Se retira sonrojada."
    
    show text "Azafata recordará esto..." at remember_text_anim style "remember_text"
    with dissolve
    pause 2.0
    hide text with dissolve




    $ azafata_recordara = True

    return  # ✅ fin correcto de toda la interacción


# --- Continúa la historia ---
label intro_post_azafata:
    # Acá sigue tu siguiente parte de la intro
    scene bg_intro_micro_noche with fade_white
    piensa "Bueno... parece que el viaje recién empieza."
    ""

    return




    # Parada de Japitown

    scene bg_parada with fade
    show mc bolso at left 

    show mc bolso_h
    mc "Fue un viaje largo pero aca estoy al fin"
    show mc bolso
    piensa "Llegue antes de lo esperado, voy a tener que esperar hasta que Monica me pase a buscar"
    piensa "Podria dar una vuelta por la playa"

    # Playa
    scene bg_playa with fade

    transform enter_from_right:
        xalign 1.5
        yalign 1.0
        linear 2.0 xalign 0.0

    show mc bolso_izquierda at enter_from_right with dissolve

    pause(2.0)
    
    show mc bolso_izquierda_h
    mc "A esta hora la playa esta vacia...{p}Las personas se pierden el mejor momento para disfutar la vista"
    show mc bolso_izquierda

    transform enter_center:
        xalign 1.5
        yalign 1.0
        linear 2.0 xalign 0.5
    show mia intro_saludando at enter_center with dissolve

    pause(2.0)

    chica "Si tienes razon"

    show mc bolso_asustado with dissolve
    mc "{size=30}AHHHHHHHH{/size}{p}Que susto"
    

    show mia intro_saludando_feliz

    chica "Jijijiji perdon"

    show mc bolso_izquierda with dissolve
    pause(1.0)
    show mc bolso with dissolve
    piensa "¿Eso lo dije en voz alta?"

    show mc bolso_h
    mc "No hay problema{p}Solo me sorprendiste"
    show mc bolso

    show mia intro with dissolve
    pause(1.0)
    show mia intro_h
    chica "Fue la emocion{p}Siempre vengo a la playa a esta hora para disfutar el atardecer"

    show mia intro_espalda
    chica "Es realmente hermoso"

    piensa "Si... la verdad es realmente hermoso"
    piensa "¿Seguimos hablando del paisaje verdad?"

    show mc bolso_h
    mc "Ahora que estoy aca nuevamente, voy a poder aprovechar esta vista mas seguido"
    show mc bolso

    show mia intro with dissolve
    pause(1.0)
    show mia intro_h 
    chica "¿Nuevamente?{p}Es verdad no recuerdo haberte visto por aca"
    chica "Y todavia no es epoca de turistas"
    show mia intro

    show mc bolso_h
    mc "Vivi muchos años aqui cuando era chico{p}Luego me fui CityNight{p}Y a varios lugares mas"
    mc "Pero no te voy a aburrir con la historia de mi vida jajaja"
    show mc bolso

    vozoff " ¡tuuuu{p}tuuuu!"
    vozoff " ¡tuuuu-tuuuu!"

    show mc bolso_h
    mc "Me vinieron a buscar{p}Seguro nos volvemos a ver"
    show mc bolso

    show mia intro_h
    chica "Bienvenido nuevamente a Japitown entoces{p}No vamos a ver muchas veces"
    show mia intro_feliz

    show mc bolso_h
    mc "Muchas gracias{p}Eso espero"
    mc "Adios"
    show mc bolso

    chica "Adios"
    show mia intro_saludando_feliz with fade
    show mia intro_espalda
    chica "Voy a disfurtar un momento mas el paisaje antes de volver"

    scene bg_parada
    show mc bolso at center 
    with fade

    piensa "Creo que yo tambien deberia disfrutar un momento mas el paisaje antes de volver"

    scene bg_playa_final

    pause(3.0)
    piensa "Voy a volver a este lugar"




    
    
    return

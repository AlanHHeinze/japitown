

#Intro variables
default azafata_recordara = False


#Intro Locutores

    #Terminal de micros
define terminal_micros = Character("Alta voz", color="#d10b0b")

    #Prota pensando
define piensa = Character(None, what_italic=True, what_prefix="«", what_suffix="»", color="#AAAAAA")

    #Mia sin presentarse
define chica = Character("Chica", color="#dfd440")

    #Descripciones
define vozoff = Character(None, what_bold=True, color="#FFFFFF", what_size=40)

    #Eva Novia Papa
define eva = Character("Eva", color="#d10b0b")

    #Rudolf 
define rudolf = Character("Rudolf", color="#330c8f")

    #Azafata
define azafata = Character("Azafata", color="#f64f56")



#Intro Sprites

    #Prota en el micro por la noche Base
layeredimage mc_intro_micro_noche:
    always:
        "images/intro/characters/mc_intro_micro_noche.png"   # El cuerpo/base sin cara ni gestos

    group ojos:
        attribute obase default:
            "images/intro/characters/mc_imn_ojos_base.png"
        attribute oaburridoc:
            "images/intro/characters/mc_imn_ojos_aburrido_costado.png"
        attribute oaburrido:
            "images/intro/characters/mc_imn_ojos_aburrido.png"
        attribute obostezo:
            "images/intro/characters/mc_imn_ojos_bostezo.png"
        attribute ocerrados:
            "images/intro/characters/mc_imn_ojos_cerrados.png"
        attribute oenojado:
            "images/intro/characters/mc_imn_ojos_enojado.png"
        attribute ofeliz:
            "images/intro/characters/mc_imn_ojos_feliz.png"
        attribute opajero:
            "images/intro/characters/mc_imn_ojos_pajero.png"
        attribute opensativo:
            "images/intro/characters/mc_imn_ojos_pensativo.png"
        attribute oasustado:
            "images/intro/characters/mc_imn_ojos_asustado.png"
        

    group boca:
        attribute bbase default:
            "images/intro/characters/mc_imn_boca_base.png"
        attribute bbostezog:
            "images/intro/characters/mc_imn_boca_bostezo_grande.png"
        attribute bbostezo:
            "images/intro/characters/mc_imn_boca_bostezo.png"
        attribute bcerradae:
            "images/intro/characters/mc_imn_boca_cerrada_enojado.png"
        attribute benojado:
            "images/intro/characters/mc_imn_boca_enojado.png"
        attribute bfeliz:
            "images/intro/characters/mc_imn_boca_feliz.png"
        attribute bhablando:
            "images/intro/characters/mc_imn_boca_hablando.png"
        attribute basustado:
            "images/intro/characters/mc_imn_boca_asustado.png"
        

    #Eva
    #Baile intro
image eva intro_baile_1 = "images/intro/characters/eva_intro_baile_1.png"
image eva intro_baile_2 = "images/intro/characters/eva_intro_baile_2.png"
image eva intro_baile_3 = "images/intro/characters/eva_intro_baile_3.png"
image eva intro_baile_4 = "images/intro/characters/eva_intro_baile_4.png"
image eva intro_baile_5 = "images/intro/characters/eva_intro_baile_5.png"
image eva intro_baile_6 = "images/intro/characters/eva_intro_baile_6.png"

    #Rudolf
    #Noticiero
image rudolf intro_pestaniando = "images/intro/characters/rudolf_intro_pestañando.png"
image rudolf intro_hablando = "images/intro/characters/rudolf_intro_hablando.png"

    #Azafata
    #Levantando la pollera
image azafata intro_base = "images/intro/characters/azafata_intro_base.png"
image azafata intro_l1 = "images/intro/characters/azafata_intro_l1.png"
image azafata intro_l2 = "images/intro/characters/azafata_intro_l2.png"
image azafata intro_l3 = "images/intro/characters/azafata_intro_l3.png"


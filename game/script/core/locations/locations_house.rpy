################################################################################
## House Locations - Definiciones de locaciones de la casa
################################################################################
## Este archivo define todas las locaciones de la casa y sus hotspots

init python:
    
    def inicializar_locaciones_casa():
        """
        Inicializa todas las locaciones de la casa.
        Esta función debe llamarse al inicio del juego.
        """
        
        # Frente de la casa
        loc_frente = Locacion(
            id="casa_frente",
            nombre="Frente de la Casa",
            background_base="images/bg/casa/bg_casa_{horario}_frente.png",
            descripcion="La entrada principal de la casa"
        )
        loc_frente.agregar_hotspot(Hotspot("casa_frente_casa_living", "MOVE", 503, 524, 170, 230, destino="casa_living", nombre="Entrar"))
        loc_frente.agregar_hotspot(Hotspot("casa_frente_casa_garage", "MOVE", 960, 539, 550, 260, destino="casa_garage", nombre="Garage"))
        loc_frente.agregar_hotspot(Hotspot("casa_frente_casa_patio", "MOVE", 1642, 588, 140, 190, destino="casa_patio", nombre="Patio"))
        sistema_locaciones.registrar_locacion(loc_frente)
        
        # Living
        loc_living = Locacion(
            id="casa_living",
            nombre="Living",
            background_base="images/bg/casa/bg_casa_{horario}_living.png",
            descripcion="La sala de estar"
        )
        loc_living.agregar_hotspot(Hotspot("casa_living_casa_pasilloabajo", "MOVE", 0, 651, 130, 435, destino="casa_pasilloabajo", nombre="Pasillo"))
        loc_living.agregar_hotspot(Hotspot("casa_living_casa_frente", "MOVE", 678, 980, 450, 100, destino="casa_frente", nombre="Salida"))
        loc_living.agregar_hotspot(Hotspot("casa_living_casa_garage", "MOVE", 1582, 302, 310, 610, destino="casa_garage", nombre="Garage"))
        loc_living.agregar_hotspot(Hotspot("casa_living_casa_patio", "MOVE", 534, 424, 630, 280, destino="casa_patio", nombre="Patio"))
        loc_living.agregar_hotspot(Hotspot("casa_living_casa_pasilloarriba", "MOVE", 0, 0, 410, 650, destino="casa_pasilloarriba", nombre="Escaleras"))
        sistema_locaciones.registrar_locacion(loc_living)
        
        # Cocina
        loc_cocina = Locacion(
            id="casa_cocina",
            nombre="Cocina",
            background_base="images/bg/casa/bg_casa_{horario}_cocina.png",
            descripcion="La cocina de la casa"
        )
        loc_cocina.agregar_hotspot(Hotspot("casa_cocina_casa_comedor", "MOVE", 460, 333, 100, 400, destino="casa_comedor", nombre="Comedor"))
        loc_cocina.agregar_hotspot(Hotspot("casa_cocina_casa_pasilloabajo", "MOVE", 730, 980, 450, 100, destino="casa_pasilloabajo", nombre="Pasillo"))
        sistema_locaciones.registrar_locacion(loc_cocina)
        
        # Comedor
        loc_comedor = Locacion(
            id="casa_comedor",
            nombre="Comedor",
            background_base="images/bg/casa/bg_casa_{horario}_comedor.png",
            descripcion="El comedor de la casa"
        )
        loc_comedor.agregar_hotspot(Hotspot("casa_comedor_casa_patio", "MOVE", 752, 342, 370, 320, destino="casa_patio", nombre="Patio"))
        loc_comedor.agregar_hotspot(Hotspot("casa_comedor_casa_cocina", "MOVE", 737, 980, 450, 100, destino="casa_cocina", nombre="Cocina"))
        sistema_locaciones.registrar_locacion(loc_comedor)
        
        # Patio
        loc_patio = Locacion(
            id="casa_patio",
            nombre="Patio",
            background_base="images/bg/casa/bg_casa_{horario}_patio.png",
            descripcion="El patio trasero"
        )
        loc_patio.agregar_hotspot(Hotspot("casa_patio_casa_frente", "MOVE", 1820, 354, 100, 740, destino="casa_frente", nombre="Frente"))
        loc_patio.agregar_hotspot(Hotspot("casa_patio_casa_gym", "MOVE", 326, 376, 150, 260, destino="casa_gym", nombre="Gym"))
        loc_patio.agregar_hotspot(Hotspot("casa_patio_casa_living", "MOVE", 748, 980, 450, 100, destino="casa_living", nombre="Living"))
        loc_patio.agregar_hotspot(Hotspot("casa_patio_casa_comedor", "MOVE", 0, 410, 150, 450, destino="casa_comedor", nombre="Comedor"))
        sistema_locaciones.registrar_locacion(loc_patio)
        
        # Pasillo de abajo
        loc_pasilloabajo = Locacion(
            id="casa_pasilloabajo",
            nombre="Pasillo",
            background_base="images/bg/casa/bg_casa_{horario}_pasilloabajo.png",
            descripcion="El pasillo de las habitaciones"
        )
        loc_pasilloabajo.agregar_hotspot(Hotspot("casa_pasilloabajo_casa_banioabajo", "MOVE", 784, 234, 310, 540, destino="casa_banioabajo", nombre="Baño"))
        loc_pasilloabajo.agregar_hotspot(Hotspot("casa_pasilloabajo_casa_hmonica", "MOVE", 83, 0, 310, 870, destino="casa_hmonica", nombre="Hab. Monica"))
        loc_pasilloabajo.agregar_hotspot(Hotspot("casa_pasilloabajo_casa_cocina", "MOVE", 1440, 0, 350, 910, destino="casa_cocina", nombre="Cocina"))
        loc_pasilloabajo.agregar_hotspot(Hotspot("casa_pasilloabajo_casa_living", "MOVE", 731, 980, 450, 100, destino="casa_living", nombre="Living"))
        sistema_locaciones.registrar_locacion(loc_pasilloabajo)
        
        # Pasillo de arriba
        loc_pasilloarriba = Locacion(
            id="casa_pasilloarriba",
            nombre="Pasillo Arriba",
            background_base="images/bg/casa/bg_casa_{horario}_pasilloarriba.png",
            descripcion="El pasillo del segundo piso"
        )
        loc_pasilloarriba.agregar_hotspot(Hotspot("casa_pasilloarriba_casa_living", "MOVE", 279, 600, 200, 270, destino="casa_living", nombre="Escaleras"))
        loc_pasilloarriba.agregar_hotspot(Hotspot("casa_pasilloarriba_casa_hmc", "MOVE", 1593, 101, 300, 770, destino="casa_hmc", nombre="Tu Habitación"))
        loc_pasilloarriba.agregar_hotspot(Hotspot("casa_pasilloarriba_casa_banioarriba", "MOVE", 1, 153, 210, 870, destino="casa_banioarriba", nombre="Baño"))
        loc_pasilloarriba.agregar_hotspot(Hotspot("casa_pasilloarriba_casa_hviolet", "MOVE", 666, 338, 170, 380, destino="casa_hviolet", nombre="Hab. Violet", label_offset_y=-32))
        loc_pasilloarriba.agregar_hotspot(Hotspot("casa_pasilloarriba_casa_hjasmine", "MOVE", 939, 338, 160, 380, destino="casa_hjasmine", nombre="Hab. Jasmine", label_offset_y=32))
        loc_pasilloarriba.agregar_hotspot(Hotspot("casa_pasilloarriba_casa_altillo", "MOVE", 255, 0, 450, 200, destino="casa_altillo", nombre="Altillo"))
        sistema_locaciones.registrar_locacion(loc_pasilloarriba)
        
        # Habitacion del MC
        loc_hmc = Locacion(
            id="casa_hmc",
            nombre="Tu Habitación",
            background_base="images/bg/casa/bg_casa_{horario}_hmc.png",
            descripcion="Tu habitación"
        )
        loc_hmc.agregar_hotspot(Hotspot("casa_hmc_casa_pasilloarriba", "MOVE", 737, 980, 450, 100, destino="casa_pasilloarriba", nombre="Salida"))
        loc_hmc.agregar_hotspot(Hotspot(
            id="dormir",
            tipo="ACTION",
            x=828, y=561, w=630, h=250,
            label="accion_dormir",
            nombre="Dormir"
        ))
        sistema_locaciones.registrar_locacion(loc_hmc)
        
        # Habitacion de Monica
        loc_hmonica = Locacion(
            id="casa_hmonica",
            nombre="Habitación de Monica",
            background_base="images/bg/casa/bg_casa_{horario}_hmonica.png",
            descripcion="La habitación de Monica"
        )
        loc_hmonica.agregar_hotspot(Hotspot("casa_hmonica_casa_pasilloabajo", "MOVE", 736, 980, 450, 100, destino="casa_pasilloabajo", nombre="Salida"))
        loc_hmonica.agregar_hotspot(Hotspot("casa_hmonica_casa_baniomonica", "MOVE", 64, 89, 200, 840, destino="casa_baniomonica", nombre="Baño"))
        sistema_locaciones.registrar_locacion(loc_hmonica)
        
        # Habitacion de Violet
        loc_hviolet = Locacion(
            id="casa_hviolet",
            nombre="Habitación de Violet",
            background_base="images/bg/casa/bg_casa_{horario}_hviolet.png",
            descripcion="La habitación de Violet"
        )
        loc_hviolet.agregar_hotspot(Hotspot("casa_hviolet_casa_pasilloarriba", "MOVE", 738, 980, 450, 100, destino="casa_pasilloarriba", nombre="Salida"))
        sistema_locaciones.registrar_locacion(loc_hviolet)
        
        # Habitacion de Jasmine
        loc_hjasmine = Locacion(
            id="casa_hjasmine",
            nombre="Habitación de Jasmine",
            background_base="images/bg/casa/bg_casa_{horario}_hjasmine.png",
            descripcion="La habitación de Jasmine"
        )
        loc_hjasmine.agregar_hotspot(Hotspot("casa_hjasmine_casa_pasilloarriba", "MOVE", 730, 980, 450, 100, destino="casa_pasilloarriba", nombre="Salida"))
        sistema_locaciones.registrar_locacion(loc_hjasmine)
        
        # Gym
        loc_gym = Locacion(
            id="casa_gym",
            nombre="Gimnasio",
            background_base="images/bg/casa/bg_casa_{horario}_gym.png",
            descripcion="El gimnasio de la casa"
        )
        loc_gym.agregar_hotspot(Hotspot(
            id="casa_gym_casa_patio",
            tipo="MOVE",
            x=1564, y=114, w=200, h=940,
            destino="casa_patio",
            nombre="Salida"
        ))
        sistema_locaciones.registrar_locacion(loc_gym)
        
        # Sótano
        loc_sotano = Locacion(
            id="casa_sotano",
            nombre="Sótano",
            background_base="images/bg/casa/bg_casa_{horario}_sotano.png",
            descripcion="El sótano de la casa"
        )
        loc_sotano.agregar_hotspot(Hotspot("casa_sotano_casa_garage", "MOVE", 1455, 227, 310, 290, destino="casa_garage", nombre="Garage"))
        sistema_locaciones.registrar_locacion(loc_sotano)
        
        # Altillo
        loc_altillo = Locacion(
            id="casa_altillo",
            nombre="Altillo",
            background_base="images/bg/casa/bg_casa_{horario}_altillo.png",
            descripcion="El altillo de la casa"
        )
        loc_altillo.agregar_hotspot(Hotspot("casa_altillo_casa_pasilloarriba", "MOVE", 625, 830, 540, 230, destino="casa_pasilloarriba", nombre="Bajar"))
        sistema_locaciones.registrar_locacion(loc_altillo)
        
        # Garage
        loc_garage = Locacion(
            id="casa_garage",
            nombre="Garage",
            background_base="images/bg/casa/bg_casa_{horario}_garage.png",
            descripcion="El garage de la casa"
        )
        loc_garage.agregar_hotspot(Hotspot("casa_garage_casa_frente", "MOVE", 560, 390, 780, 340, destino="casa_frente", nombre="Salida"))
        loc_garage.agregar_hotspot(Hotspot("casa_garage_casa_sotano", "MOVE", 0, 333, 200, 750, destino="casa_sotano", nombre="Sótano"))
        loc_garage.agregar_hotspot(Hotspot("casa_garage_casa_living", "MOVE", 1720, 330, 200, 750, destino="casa_living", nombre="Living"))
        sistema_locaciones.registrar_locacion(loc_garage)
        
        # Baño de abajo
        loc_banioabajo = Locacion(
            id="casa_banioabajo",
            nombre="Baño",
            background_base="images/bg/casa/bg_casa_{horario}_banioabajo.png",
            descripcion="El baño del primer piso"
        )
        loc_banioabajo.agregar_hotspot(Hotspot("casa_banioabajo_casa_pasilloabajo", "MOVE", 738, 980, 450, 100, destino="casa_pasilloabajo", nombre="Salida"))
        sistema_locaciones.registrar_locacion(loc_banioabajo)
        
        # Baño de arriba
        loc_banioarriba = Locacion(
            id="casa_banioarriba",
            nombre="Baño Arriba",
            background_base="images/bg/casa/bg_casa_{horario}_banioarriba.png",
            descripcion="El baño del segundo piso"
        )
        loc_banioarriba.agregar_hotspot(Hotspot("casa_banioarriba_casa_pasilloarriba", "MOVE", 735, 980, 450, 100, destino="casa_pasilloarriba", nombre="Salida"))
        sistema_locaciones.registrar_locacion(loc_banioarriba)
        
        # Baño de Monica
        loc_baniomonica = Locacion(
            id="casa_baniomonica",
            nombre="Baño de Monica",
            background_base="images/bg/casa/bg_casa_{horario}_baniomonica.png",
            descripcion="El baño privado de Monica"
        )
        loc_baniomonica.agregar_hotspot(Hotspot("casa_baniomonica_casa_hmonica", "MOVE", 732, 980, 450, 100, destino="casa_hmonica", nombre="Volver"))
        sistema_locaciones.registrar_locacion(loc_baniomonica)
        
        

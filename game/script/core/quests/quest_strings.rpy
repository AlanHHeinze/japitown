################################################################################
## Strings de Quest — archivo fuente para el sistema de traducción
################################################################################
## Este archivo existe únicamente para que Ren'Py registre las strings
## usadas en quests y restricciones, permitiendo su traducción via tl files.

init python:

    _quest_strings_registradas = [

        ## Nombres de Quests
        "¿Qué le pasa a Violet?",
        "Un paquete misterioso",
        "El contenido del paquete",
        "Limpieza del Sábado",
        "Solo en casa",
        "El cosplay de Violet",
        "El cosplay de Violet II",
        "El cosplay de Violet III",
        "El cosplay de Violet IV",
        "Los ruidos nocturnos",
        "Visita nocturna",

        ## Mensajes genéricos de Quest
        "Debo esperar [dias_restantes] días más.",
        "Esperar [dias_restantes] días",
        "Debo esperar hasta mañana.",
        "Esperar hasta mañana",
        "Debo esperar algunos días.",
        "Esperar algunos días",
        "Verificando condiciones...",
        "Verificando...",
        "Quest en progreso...",
        "Continuar la quest.",
        " y ",

        ## Requisitos Genéricos
        "Relación con [npc_id] debe ser de al menos [valor]",
        "Tener al menos [cantidad] de [item_id]",
        "Tener al menos $[valor]",

        ## Mensajes de bloqueo — movimiento
        "No puedo ir ahí ahora",
        "Debo ir a mi habitación",
        "Debería ir a la cocina a preparar la pizza",
        "Debo avisarle a Violet que esta la comida",
        "Debo encargarme de limpiar la planta baja",
        "Debo ir a ver como va Violet con la limpieza",
        "Debo buscar algo para limpiar",
        "Debo volver arriba a limpiar",
        "Debo ver como va Violet con el baño",
        "No puedo salir de la casa ahora",
        "Debería llevarle ropa a Violet",
        "Debo llevarle la ropa a Violet",

        ## Mensajes de bloqueo — acciones
        "No puedo hacer eso ahora",
        "No debo perder el tiempo",
        "No puedo perder tiempo con esto",
        "Tengo que encargarme de las pizzas antes de hacer otra cosa",
        "Tengo que cocinar primero",
        "No tengo ganas de hacer nada productivo",
        "No tengo sueño",
        "No tengo ganas de entrenar",
        "No tengo ganas de trabajar",
        "No tengo ganas de usar eso ahora",
        "No tengo ganas de comprar nada",

        ## Mensajes de bloqueo — NPC y celular
        "No tengo tiempo para eso ahora",
        "No tengo tiempo para hablar",
        "No hay nadie en la casa",
        "No hay nadie mas en la casa",
        "No es momento de usar el celular",

        ## Pistas — Quest Violet 0
        "Tengo que hablar con Violet, podría aprovechar cuando está en su habitación por la tarde.",
        "Ir a la habitación de Violet por la tarde.",
        "Tengo que encontrar algún momento para acercarme a Violet y ver qué le pasa.",

        ## Pistas — Quest Violet 1
        "Todo tranquilo por ahora",
        "Parece que hay alguien afuera",
        "Tengo un mensaje por ver",
        "Revisar el paquete",
        "Esperar",
        "Ir al frente",
        "Ir a la habitación por el paquete",
        "Responder el mensaje de Monica",
        "Escuche el timbre",

        ## Pistas — Quest Violet 2
        "Podría entregarle el paquete a Violet o podría ver bien que tiene",
        "Hablar con Violet y darle su paquete o revisar el contenido del paquete",

        ## Pistas — Quest Violet 4
        "Monica me dijo algo sobre limpiar la casa, tengo que esperar.",
        "Debería responderle a Monica.",
        "Responder mensaje de Monica.",
        "Hoy es sábado, tengo que despertar a Violet temprano.",
        "Monica me pidió que despierte a Violet temprano el sábado para limpiar la casa.",
        "Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa.",
        "El próximo sábado debería ocuparme de la limpieza.",
        "Esperar hasta el próximo sábado por la mañana.",
        "Ir a la habitación de Violet por la mañana.",
        "Esperar hasta el sabado por la mañana.",

        ## Pistas — Quest Violet 5
        "Todo tranquilo por ahora.",
        "Hoy estoy solo en la casa.",
        "Esperar al día siguiente.",

        ## Pistas — Quest Violet 6
        "Recuerdo lo del cosplay, debería esperar unos días.",
        "Cuando encuentre a Violet podría ver si se probó el cosplay",
        "Hablar con Violet",
        "Podría preguntarle a Violet si se probó el cosplay",

        ## Pistas — Quest Violet 7-9
        "Debería esperar unos días antes de hablar con Violet sobre el cosplay.",
        "Violet tiene vergüenza de mostrarme el cosplay, tengo que mejorar mi deseo con ella",
        "Subir deseo con Violet ({}/{})",
        "Debería esperar unos días.",
        "Quizás si sigo mejorando mi deseo con Violet me muestre un poco más",
        "Violet me envió un mensaje, debería responderle.",
        "Violet me envió un mensaje, debería responderle",
        "Violet ya me contestó, debería ir a hablar con ella.",
        "Ir a ver a Violet a su habitación.",
        "Responder mensaje de Violet",
        "Tengo que ir a ver a Violet por lo de su cosplay.",

        ## Pistas — Quest Violet 11
        "Todo tranquilo por ahora, debería esperar unos días.",
        "Podría conseguir algunos cosplay para que Violet se pruebe",
        "Comprar el ítem conjunto de cosplay",
        "Podría ir a la habitación de violet por la noche a ver si le gusta lo que compré",
        "Ir a la habitación de violet por la noche",
        "Podría mostrarle a violet los cosplays que conseguí.",

        ## Pistas — Quest Violet 12
        "Violet me pidió que pase por su habitación, debería ir a la noche.",
        "Ir a la habitación de Violet por la noche.",
        "Violet me pidió que pase por su habitación a la noche.",

        ## Pistas — Quests Monica
        "Tendría que encontrarme con Monica para darle las gracias, podría verla por la tarde.",
        "Ir al living por la tarde.",
        "Podría aprovechar que Monica está en casa para hablar con ella.",
        "Monica parece más ocupada por las tardes",
        "Ir a la habitación de Monica por la tarde",
        "Podría ver si Monica necesita algo",
        "Podría ver a Monica en la tarde y ofrecerle un masaje.",
        "Habla con Monica cuando esté en el living por la tarde.",
        "Mónica se quejó de dolor en sus hombros, podría hacerle un masaje en la tarde.",

        ## Pistas — Quests Jasmine
        "Podría ver a Jasmine por la tarde cuando entrena y hablar un poco.",
        "Ir al gym por la tarde.",
        "Podría buscar a Jasmine cuando este entrenando para hablar con ella.",

        ## Mensajes de Requisito
        "Violet debe estar en su habitación",
        "Violet debe estar en su habitación",
        "Debe ser sábado",
        "Debe ser por la mañana",
        "Debe ser por la tarde",
        "Debe ser por la noche",
        "Me falta el conjunto de cosplays",
        "Contestar el mensaje de Monica",
        "Responder el mensaje de Violet",
        "Monica debe estar en su habitación",
        "Necesitas mas deseo con Violet",
        "Debes estar en el gym",
        "Debes estar en el living",
        "La quest no está lista para iniciarse.",
    ]

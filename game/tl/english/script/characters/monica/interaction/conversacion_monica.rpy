# TODO: Translation updated at 2026-04-21 21:46

# game/script/characters/monica/interaction/conversacion_monica.rpy:153
translate english conversacion_hablar_monica_45dc90ff:

    # monica "[_preg['q']]"
    monica "[_preg['q']]"

# game/script/characters/monica/interaction/conversacion_monica.rpy:157
translate english conversacion_hablar_monica_e4847038:

    # monica "[_op0['resp']]"
    monica "[_op0['resp']]"

# game/script/characters/monica/interaction/conversacion_monica.rpy:160
translate english conversacion_hablar_monica_b859ee7c:

    # monica "[_op1['resp']]"
    monica "[_op1['resp']]"

# game/script/characters/monica/interaction/conversacion_monica.rpy:163
translate english conversacion_hablar_monica_662c0fe1:

    # monica "[_op2['resp']]"
    monica "[_op2['resp']]"



translate english python:
    preguntas_hablar_monica = [
        {
            "q": "How are you doing around here? Are you adapting well?",
            "ops": [
                {"texto": "Pretty well, little by little.", "resp": "I'm glad to hear that. You'll see this place has its charm.", "stat": "amor"},
                {"texto": "It's a bit hard, but I'm managing.", "resp": "That's normal. Don't push yourself too hard.", "stat": "deseo"},
                {"texto": "More or less, I'm still learning.", "resp": "That's the right attitude. One never stops learning.", "stat": "amor"},
            ]
        },
        {
            "q": "Did you have a good breakfast? I always say breakfast is the most important.",
            "ops": [
                {"texto": "Yes, thanks. I ate something earlier.", "resp": "Good. The body needs energy to start the day.", "stat": "deseo"},
                {"texto": "I sometimes skip it, to be honest.", "resp": "That's not good. But I won't scold you.", "stat": "amor"},
                {"texto": "I remembered to eat because of what you prepared yesterday.", "resp": "I'm glad it helped! I'm glad you took advantage of it.", "stat": "amor"},
            ]
        },
        {
            "q": "Is there anything in this house that seems weird to you or that you don't understand yet?",
            "ops": [
                {"texto": "Some things, but I ask as they come up.", "resp": "Well done. Better to ask than to stay in doubt.", "stat": "amor"},
                {"texto": "I'm learning how everything works over time.", "resp": "That reassures me. You know you can count on me.", "stat": "amor"},
                {"texto": "It's a bit hard for me to understand everyone's routines.", "resp": "It's natural. Each person has their ways. Take it easy.", "stat": "deseo"},
            ]
        },
        {
            "q": "Do you like cooking? Because I always need help in the kitchen.",
            "ops": [
                {"texto": "I can manage, though I'm not the best.", "resp": "That's enough. Welcome to the team.", "stat": "amor"},
                {"texto": "Not really, but I learn fast.", "resp": "That's all it takes.", "stat": "amor"},
                {"texto": "If you teach me, gladly.", "resp": "Deal! I like teaching those who want to learn.", "stat": "deseo"},
            ]
        },
        {
            "q": "How are you getting along with Violet and Jasmine so far?",
            "ops": [
                {"texto": "Well, although we are still getting to know each other.", "resp": "That's to be expected. Give it time.", "stat": "deseo"},
                {"texto": "Violet is more reserved, Jasmine more open.", "resp": "You know them well for the time you've been here. Good eye.", "stat": "amor"},
                {"texto": "I try not to meddle too much for now.", "resp": "That's also a valid option. Everyone at their own pace.", "stat": "amor"},
            ]
        },
        {
            "q": "What is the hardest part about living with other people?",
            "ops": [
                {"texto": "Adapting to the rhythm of others.", "resp": "It's one of the most common challenges. But you learn.", "stat": "amor"},
                {"texto": "Giving privacy without seeming indifferent.", "resp": "That requires a lot of sensitivity. Good point.", "stat": "deseo"},
                {"texto": "Sometimes I miss my own space.", "resp": "It's completely normal. This house is yours too.", "stat": "amor"},
            ]
        },
        {
            "q": "Do you think this house has a good atmosphere in general?",
            "ops": [
                {"texto": "Yes, it feels quite comfortable.", "resp": "I'm glad. I put a lot of effort into making it that way.", "stat": "amor"},
                {"texto": "There are good moments and more tense ones.", "resp": "That's honest. Every coexistence has its moments.", "stat": "deseo"},
                {"texto": "Depends on the day and how everyone is feeling.", "resp": "True. The atmosphere is made by all of us together.", "stat": "amor"},
            ]
        },
        {
            "q": "Is there anything I can do to make you feel more comfortable here?",
            "ops": [
                {"texto": "No, I'm good. Thanks for asking.", "resp": "You're welcome. If anything changes, let me know without hesitation.", "stat": "deseo"},
                {"texto": "Maybe know more about how everything works.", "resp": "We can talk about that calmly whenever you want.", "stat": "amor"},
                {"texto": "As long as we keep talking like this, it's enough.", "resp": "I'm very glad to hear that.", "stat": "amor"},
            ]
        },
        {
            "q": "Are you the kind who asks for help when needed, or do you prefer to solve it alone?",
            "ops": [
                {"texto": "I try to solve it alone first, but I ask if necessary.", "resp": "That's very good. Independence with sense.", "stat": "amor"},
                {"texto": "It's hard for me to ask, but I'm working on it.", "resp": "Just recognizing it is already a big step.", "stat": "amor"},
                {"texto": "Depends on the situation, to be honest.", "resp": "That's healthy. Not all situations are the same.", "stat": "deseo"},
            ]
        },
        {
            "q": "Is there anything you want to know about me or how things work here?",
            "ops": [
                {"texto": "Yes, I would like to better understand the house rules.", "resp": "With pleasure. Sit down and I'll tell you everything.", "stat": "amor"},
                {"texto": "I'm fine for now, but I'll let you know if something comes up.", "resp": "Perfect. The door is always open.", "stat": "amor"},
                {"texto": "What is the most important thing for you here?", "resp": "That everyone is well and treated with respect. That's all.", "stat": "deseo"},
            ]
        }
    ]


"""
Script de cadastro dos 6 cursos de Inglês na plataforma Vedium (Frappe LMS).

Currículo baseado no material fornecido:
  1. Beginner          (A1)  — 14 unidades
  2. Elementary        (A2)  — 12 unidades
  3. Pré-Intermediário (B1-) — 12 unidades
  4. Intermediário     (B1)  — 12 unidades
  5. Upper Intermediário (B2) — 12 unidades
  6. Avançado          (C1)  — 12 unidades

Imagens: Unsplash (free, sem autenticação, tamanho 1280x720)

Preço exibido no card: R$ 240/mês (1 aula/semana — menor barreira de entrada).
Tabela completa de frequências é exibida pela seção de Planos no site.

Uso dentro do container:
  bench --site vediums.com execute create_english_courses.execute
"""

import frappe


# ─────────────────────────────────────────────────────────────────────────────
# IMAGENS (Unsplash free, sem necessidade de API key)
# Usando source.unsplash.com com query — retorna imagem relevante
# ─────────────────────────────────────────────────────────────────────────────
IMAGES = {
    "beginner": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1280&q=80",  # crianças estudando
    "elementary": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1280&q=80",  # grupo jovens estudando
    "pre_inter": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1280&q=80",  # pessoa estudando café
    "intermediate": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1280&q=80",  # estudantes mesa
    "upper_inter": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1280&q=80",  # profissional inglês
    "advanced": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1280&q=80",  # executivo confiante
    "banner": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1920&q=80",  # sala de aula moderna
}

# ─────────────────────────────────────────────────────────────────────────────
# CURRÍCULO COMPLETO — 6 NÍVEIS
# Cada nível: lista de units com lista de topics (lições)
# ─────────────────────────────────────────────────────────────────────────────
ENGLISH_CURRICULUM = [
    # ─── 1. BEGINNER (A1) ────────────────────────────────────────────────────
    {
        "name": "ingles-beginner",
        "title": "Inglês - Beginner",
        "level_code": "A1",
        "category": "Inglês - Beginner",
        "short_description": (
            "Nível A1 | Comece do zero com vocabulário essencial, cumprimentos, "
            "família, rotina e estruturas básicas em 14 unidades progressivas."
        ),
        "long_description": (
            "<p>O curso <strong>Inglês Beginner</strong> foi projetado para quem nunca "
            "estudou inglês ou precisa retomar do início com uma base sólida.</p>"
            "<p>Em 14 unidades cuidadosamente estruturadas, você vai dominar:</p>"
            "<ul>"
            "<li>Verbos <em>to be</em>, <em>have/go/live/like</em></li>"
            "<li>Números, datas, horas e preços</li>"
            "<li>Família, profissões, rotina diária</li>"
            "<li>Presente Simples e Contínuo</li>"
            "<li>Past Simple (regular e irregular)</li>"
            "<li>Futuro com <em>going to</em> e <em>will</em></li>"
            "<li>Present Perfect introdutório</li>"
            "</ul>"
            "<p><strong>Duração estimada:</strong> 6 meses (1 a 4 aulas/semana)</p>"
            "<p><strong>Certificado:</strong> Incluso ao concluir todas as unidades.</p>"
        ),
        "image": IMAGES["beginner"],
        "course_price": 240.00,
        "units": [
            {
                "title": "Unit 1 – Hello!",
                "topics": [
                    "am/is/are e my/your",
                    "This is. How are you?",
                    "Vocabulário: Numbers 1-10 e Plurals",
                    "Everyday English: Good morning!",
                ],
            },
            {
                "title": "Unit 2 – My World",
                "topics": [
                    "he/she/they, his/her",
                    "Questions and Answers",
                    "Vocabulário: Countries, Adjectives, Numbers 11-30",
                ],
            },
            {
                "title": "Unit 3 – About You",
                "topics": [
                    "Negatives, Questions e Short Answers",
                    "Jobs e Personal Information",
                    "Social Expressions (1)",
                ],
            },
            {
                "title": "Unit 4 – Family and Friends",
                "topics": [
                    "Possessives: my/your/his/her/our",
                    "Common Verbs: have, love, like, work",
                    "The Family / On the Phone",
                ],
            },
            {
                "title": "Unit 5 – My Likes",
                "topics": [
                    "like/don't like / Present Simple (I/you/we/they)",
                    "Sports, Food and Drinks",
                    "Languages, Nationalities, Numbers and Prices",
                ],
            },
            {
                "title": "Unit 6 – Everyday",
                "topics": [
                    "The Time / Present Simple (he/she/it)",
                    "Words That Go Together",
                    "Days of the Week / Prepositions of Time",
                ],
            },
            {
                "title": "Unit 7 – Favourite Things",
                "topics": [
                    "Question Words / Pronouns and Possessives",
                    "this and that / Adjectives",
                    "Can I...?",
                ],
            },
            {
                "title": "Unit 8 – Home Sweet Home",
                "topics": [
                    "There is/There are / Prepositions of Place",
                    "Rooms and Furniture / Places in the City",
                    "Directions",
                ],
            },
            {
                "title": "Unit 9 – Past Time",
                "topics": [
                    "Past Simple: was/were",
                    "Common Verbs (2): have, do, go",
                    "Months and Dates / Saying Years",
                ],
            },
            {
                "title": "Unit 10 – Good Times!",
                "topics": [
                    "Past Simple: Regular and Irregular Verbs",
                    "Questions and Negatives / Time Expressions",
                    "Sport and Leisure / Going Sightseeing",
                ],
            },
            {
                "title": "Unit 11 – Abilities",
                "topics": [
                    "can/can't / Questions and Short Answers",
                    "Adverbs / Requests and Offers",
                    "Adjective + Noun",
                ],
            },
            {
                "title": "Unit 12 – Thank You!",
                "topics": [
                    "some and any / I'd like a... / I'd like to...",
                    "Offering Things / like and would like",
                    "Food Vocabulary",
                ],
            },
            {
                "title": "Unit 13 – Happening Now?",
                "topics": [
                    "Present Continuous / Questions and Negatives",
                    "Present Simple or Continuous?",
                    "Colours and Clothes / Opposite Verbs / What's the matter?",
                ],
            },
            {
                "title": "Unit 14 – On the Move!",
                "topics": [
                    "Future Plans: going to",
                    "Making Arrangements",
                    "Grammar Revision: All Tenses / Vocabulary Revision",
                ],
            },
        ],
    },
    # ─── 2. ELEMENTARY (A2) ──────────────────────────────────────────────────
    {
        "name": "ingles-elementary",
        "title": "Inglês - Elementary",
        "level_code": "A2",
        "category": "Inglês - Elementary",
        "short_description": (
            "Nível A2 | Consolide suas bases com Present/Past Simple, can/was/were, "
            "Present Continuous e futuro. 12 unidades temáticas."
        ),
        "long_description": (
            "<p>O curso <strong>Inglês Elementary</strong> é o segundo nível da trilha "
            "Vedium, projetado para consolidar as bases e ampliar a comunicação do dia a dia.</p>"
            "<ul>"
            "<li>am/is/are e possessivos</li>"
            "<li>Present Simple: rotina e profissões</li>"
            "<li>Present Continuous: agora e planos</li>"
            "<li>Past Simple regular e irregular</li>"
            "<li>can/can't, was/were/could</li>"
            "<li>Futuro com <em>going to</em> e <em>will</em></li>"
            "<li>Present Perfect introdutório (ever/never/yet/just)</li>"
            "<li>Count/Uncount nouns e quantidades</li>"
            "</ul>"
            "<p><strong>Duração estimada:</strong> 6 meses. <strong>Certificado</strong> incluso.</p>"
        ),
        "image": IMAGES["elementary"],
        "course_price": 240.00,
        "units": [
            {
                "title": "Unit 1 – Introduction",
                "topics": [
                    "am/is/are / my/your/his/her",
                    "Verbs: have/go/live/like",
                    "Possessive 's / Opposite Adjectives / Family",
                    "Everyday Conversations",
                ],
            },
            {
                "title": "Unit 2 – Work & Family",
                "topics": [
                    "Present Simple (3ª pessoa: he/she/it)",
                    "Questions and Negatives / Jobs",
                    "What Time Is It? / Opposites: early/late, big/small",
                ],
            },
            {
                "title": "Unit 3 – Free Time",
                "topics": [
                    "Present Simple (I/you/we/they) / Questions and Negatives",
                    "In My Free Time / Months and Seasons",
                    "Weekends Roleplay / Social Expressions (1)",
                ],
            },
            {
                "title": "Unit 4 – Place",
                "topics": [
                    "There is/are / some/any/a lot of",
                    "this/that/these/those / Adjectives",
                    "Numbers and Prices / Prepositions of Place / Describing Your Home",
                ],
            },
            {
                "title": "Unit 5 – Abilities",
                "topics": [
                    "can/can't / was/were/could",
                    "Words That Go Together / Polite Requests",
                    "Prepositions: about/of/to / Formal Email",
                ],
            },
            {
                "title": "Unit 6 – Past Simple",
                "topics": [
                    "Past Simple: Regular and Irregular Verbs",
                    "Describing Feelings / -ed/-ing Adjectives",
                    "What's the Date? / Linking Words",
                ],
            },
            {
                "title": "Unit 7 – Remember",
                "topics": [
                    "Past Simple: Questions and Negatives",
                    "Time Expressions / Adverbs",
                    "Special Occasions / Prepositions of Time",
                ],
            },
            {
                "title": "Unit 8 – Count It",
                "topics": [
                    "Count and Uncount Nouns / some/any",
                    "I like vs. I'd like / How much? How many?",
                    "Food and Drink / Shopping in the High Street",
                ],
            },
            {
                "title": "Unit 9 – City",
                "topics": [
                    "Comparative and Superlative Adjectives / have got",
                    "Preposition of Movement: along/through/over",
                    "Town and Country / Directions",
                ],
            },
            {
                "title": "Unit 10 – Up to What?",
                "topics": [
                    "Whose/who's / Present Continuous",
                    "something/nothing... / Describing People",
                    "Comparing and Contrasting / Social Expressions",
                ],
            },
            {
                "title": "Unit 11 – Future",
                "topics": [
                    "going to Future / Infinitive of Purpose",
                    "What's the Weather Like? / will",
                    "Seeing the Future / Making Suggestions",
                ],
            },
            {
                "title": "Unit 12 – Present Perfect",
                "topics": [
                    "ever, never, yet, and just",
                    "take and get / Transport and Travel",
                    "Who Is It?",
                ],
            },
        ],
    },
    # ─── 3. PRÉ-INTERMEDIÁRIO (B1-) ──────────────────────────────────────────
    {
        "name": "ingles-pre-intermediario",
        "title": "Inglês - Pré-Intermediário",
        "level_code": "B1-",
        "category": "Inglês - Pré-Intermediário",
        "short_description": (
            "Nível B1- | Present Perfect, condicionais, passiva, quantificadores. "
            "Inglês funcional para conversações do cotidiano. 12 unidades."
        ),
        "long_description": (
            "<p>O <strong>Pré-Intermediário</strong> expande sua comunicação "
            "para situações mais variadas e complexas do dia a dia.</p>"
            "<ul>"
            "<li>Revisão de tempos verbais / Perguntas e negativas</li>"
            "<li>Present Perfect (for/since, ever/never)</li>"
            "<li>Narrative tenses (Past Simple + Continuous)</li>"
            "<li>Conditionals (if + will/might/would)</li>"
            "<li>Passiva / Compound nouns / Phrasal verbs</li>"
            "<li>Modais: have to / should / must</li>"
            "<li>Question tags / Word formation</li>"
            "</ul>"
            "<p><strong>Duração estimada:</strong> 6–8 meses. <strong>Certificado</strong> incluso.</p>"
        ),
        "image": IMAGES["pre_inter"],
        "course_price": 240.00,
        "units": [
            {
                "title": "Unit 1 – Questions & Tense Revision",
                "topics": [
                    "Questions, Tense Revision",
                    "Adjectives, Prepositions / do/make / speak/talk",
                    "Right Word, Wrong Word / Social Expressions",
                ],
            },
            {
                "title": "Unit 2 – Present Tenses",
                "topics": [
                    "Questions / Present Tenses / have/have got",
                    "Things I Like Doing / Present Continuous",
                    "Short Answers / Expressing Interest: How Lovely!",
                ],
            },
            {
                "title": "Unit 3 – Past Simple & Continuous",
                "topics": [
                    "Regular and Irregular Verbs",
                    "Adverbs / Saying When",
                    "Making Conversation",
                ],
            },
            {
                "title": "Unit 4 – Expressing Quantity",
                "topics": [
                    "something/anything/no one... / Articles",
                    "A Piece of... / Can You Come for Dinner?",
                    "Requests: Can I / Could I",
                ],
            },
            {
                "title": "Unit 5 – Future Forms",
                "topics": [
                    "Verb Patterns / Future: going to/will/-ing",
                    "Phrasal Verbs: Literal and Idiomatic",
                    "Expressing Doubt and Certainty",
                ],
            },
            {
                "title": "Unit 6 – Relatives & Comparatives",
                "topics": [
                    "What ... Like? / Comparatives and Superlatives",
                    "Synonyms and Antonyms / Relative Pronouns",
                    "What's On?",
                ],
            },
            {
                "title": "Unit 7 – Present Perfect",
                "topics": [
                    "for and since / ever and never / Question Tags",
                    "Word Formation",
                    "Agree with Me!",
                ],
            },
            {
                "title": "Unit 8 – Modals & Clothes",
                "topics": [
                    "have to/don't have to / should/must",
                    "Things to Wear",
                    "At the Doctor's",
                ],
            },
            {
                "title": "Unit 9 – Narrative Tenses",
                "topics": [
                    "Past Perfect and Narrative Tenses",
                    "Joining Sentences",
                    "Feelings / Exclamations",
                ],
            },
            {
                "title": "Unit 10 – Passives",
                "topics": [
                    "Passives / Compound Nouns",
                    "Adverbs/Adjectives / Words That Go Together",
                    "On the Phone",
                ],
            },
            {
                "title": "Unit 11 – Present Perfect Continuous",
                "topics": [
                    "Present Perfect Continuous / Tense Review",
                    "Birth, Marriage, and Death",
                    "Good News, Bad News",
                ],
            },
            {
                "title": "Unit 12 – Conditionals",
                "topics": [
                    "if + will/might/would / Conditionals",
                    "Prepositions",
                    "Thank You and Goodbye!",
                ],
            },
        ],
    },
    # ─── 4. INTERMEDIÁRIO (B1) ───────────────────────────────────────────────
    {
        "name": "ingles-intermediario",
        "title": "Inglês - Intermediário",
        "level_code": "B1",
        "category": "Inglês - Intermediário",
        "short_description": (
            "Nível B1 | Todos os tempos verbais, modais, reported speech e conditionals. "
            "Comunicação fluente em situações diversas. 12 unidades."
        ),
        "long_description": (
            "<p>O <strong>Intermediário</strong> é o nível central da trilha Vedium, "
            "onde você ganha confiança para conversar em inglês em qualquer situação.</p>"
            "<ul>"
            "<li>Question forms avançadas / Narrativa complexa</li>"
            "<li>Present Perfect Simple e Continuous</li>"
            "<li>Modals: obligation, permission, probability</li>"
            "<li>Verb patterns: infinitive/gerund</li>"
            "<li>Future forms: will, going to, Present Continuous</li>"
            "<li>Conditionals 1ª, 2ª e 3ª / Past possibilities</li>"
            "<li>Reported speech / Articles / Noun phrases</li>"
            "</ul>"
            "<p><strong>Duração estimada:</strong> 8 meses. <strong>Certificado</strong> incluso.</p>"
        ),
        "image": IMAGES["intermediate"],
        "course_price": 240.00,
        "units": [
            {
                "title": "Unit 1 – Question Forms",
                "topics": [
                    "Questions with a Preposition / Questions in Context",
                    "-ed/-ing Adjectives / Antonyms and Synonyms",
                    "Phrasal Verbs in Situations / Saying Just the Right Thing!",
                ],
            },
            {
                "title": "Unit 2 – Tenses Review",
                "topics": [
                    "Asking Questions / Negatives / Short Answers / Grammar Words",
                    "Words That Go Together / Verb + Preposition",
                    "Everyday Situations: Short Remarks",
                ],
            },
            {
                "title": "Unit 3 – Present Tenses",
                "topics": [
                    "Simple or Continuous? / Present Passive / State and Activity Verbs",
                    "Work and Play / Phrasal Verbs + Noun (1)",
                    "Making Small Talk",
                ],
            },
            {
                "title": "Unit 4 – Narrative Tenses",
                "topics": [
                    "Past Simple or Past Perfect? / Past Perfect Simple or Continuous?",
                    "Past Tenses in a Narrative / Birth, Marriage, and Death",
                    "Prepositions in/at/on for Time / Expressing Opinions",
                ],
            },
            {
                "title": "Unit 5 – Modals of Obligation",
                "topics": [
                    "Should for Advice / Permission and Ability",
                    "The Criminal Justice System",
                    "Phrasal Verbs: Separable and Inseparable / Polite Requests and Offers",
                ],
            },
            {
                "title": "Unit 6 – Present Perfect or Past Simple?",
                "topics": [
                    "Time Expressions / Present Perfect Passive / Present Perfect Continuous",
                    "Adverbs / Noun + Preposition",
                    "Everyday English / Numbers",
                ],
            },
            {
                "title": "Unit 7 – Verb Patterns",
                "topics": [
                    "Verb Patterns: -ing Forms / Infinitives / Reporting Verbs + Infinitive",
                    "Using a Dictionary / Body Language",
                    "Phrasal Verbs Without a Noun / English Exclamations",
                ],
            },
            {
                "title": "Unit 8 – Future Forms",
                "topics": [
                    "will / going to for Predictions / Present Continuous for Arrangements",
                    "Sources of Energy / Prefixes and Suffixes",
                    "Adjective + Preposition / Making Arrangements",
                ],
            },
            {
                "title": "Unit 9 – Conditionals",
                "topics": [
                    "First / Second / Third Conditional / Past Possibilities",
                    "Words with Similar and Different Meanings",
                    "Prepositions with Money / Money Matters",
                ],
            },
            {
                "title": "Unit 10 – Modals of Probability",
                "topics": [
                    "The Continuous Infinitive / Modals of Probability – Past",
                    "be and have / Phrasal Verbs with out and up",
                    "Verb + Preposition / Expressing Attitude",
                ],
            },
            {
                "title": "Unit 11 – Noun Phrases",
                "topics": [
                    "Articles: Indefinite and Definite / No Article / Possessives",
                    "Compound Nouns / Count and Uncount Nouns",
                    "Phrasal Verbs + Noun (2) / I Need One of Those Things...",
                ],
            },
            {
                "title": "Unit 12 – Reported Speech",
                "topics": [
                    "Reporting Statements and Commands / Indirect Questions",
                    "speak, talk, say or tell? / 'Talking' Verbs + Infinitive",
                    "Phrasal Verbs in Situations (2) / Talking in Clichés",
                ],
            },
        ],
    },
    # ─── 5. UPPER INTERMEDIÁRIO (B2) ─────────────────────────────────────────
    {
        "name": "ingles-upper-intermediario",
        "title": "Inglês - Upper Intermediário",
        "level_code": "B2",
        "category": "Inglês - Upper Intermediário",
        "short_description": (
            "Nível B2 | Sistema de tempos, modais avançados, hipóteses, artigos "
            "e linking devices para fluência profissional. 12 unidades."
        ),
        "long_description": (
            "<p>O <strong>Upper Intermediário</strong> leva você ao nível B2 do CEFR, "
            "onde a fluência para contextos profissionais e acadêmicos se consolida.</p>"
            "<ul>"
            "<li>Sistema de tempos (tense system) e linguagem informal</li>"
            "<li>Present Perfect Simple e Continuous avançados</li>"
            "<li>Narrative tenses / Modais e verbos relacionados</li>"
            "<li>Relative clauses / Participles / Adverb collocations</li>"
            "<li>Expressing habit (used to/would)</li>"
            "<li>Modal auxiliary verbs 2 / Metáforas e idioms</li>"
            "<li>Hypothesizing / Articles / Determiners</li>"
            "<li>Linking and commenting expressions</li>"
            "</ul>"
            "<p><strong>Duração estimada:</strong> 8 meses. <strong>Certificado</strong> incluso.</p>"
        ),
        "image": IMAGES["upper_inter"],
        "course_price": 240.00,
        "units": [
            {
                "title": "Unit 1 – The Tense System",
                "topics": ["Informal Language / Compound Words", "Social Expressions"],
            },
            {
                "title": "Unit 2 – Present Perfect",
                "topics": [
                    "Simple and Continuous",
                    "Hot Verbs: make, do",
                    "Exclamations",
                ],
            },
            {
                "title": "Unit 3 – Narrative Tenses",
                "topics": ["News and Responses", "Books and Films", "Showing Interest"],
            },
            {
                "title": "Unit 4 – Questions and Negatives",
                "topics": ["Prefixes and Antonyms", "Being Polite"],
            },
            {
                "title": "Unit 5 – Future Forms",
                "topics": ["Hot Verbs: take, put", "Telephoning"],
            },
            {
                "title": "Unit 6 – Expressions of Quantity",
                "topics": [
                    "'Export and Export' (homographs)",
                    "Business Expressions and Numbers",
                ],
            },
            {
                "title": "Unit 7 – Modals and Related Verbs 1",
                "topics": ["Hot Verb: get", "Exaggeration and Understatement"],
            },
            {
                "title": "Unit 8 – Relative Clauses & Participles",
                "topics": ["Adverb Collocations", "The World Around"],
            },
            {
                "title": "Unit 9 – Expressing Habit",
                "topics": [
                    "used to do / doing",
                    "Homonyms / Homophones",
                    "Making Your Point",
                ],
            },
            {
                "title": "Unit 10 – Modal Auxiliary Verbs 2",
                "topics": ["Synonyms", "Metaphors and Idioms / the Body"],
            },
            {
                "title": "Unit 11 – Hypothesizing",
                "topics": ["Expressions with if / Word Pairs", "Moans and Groans"],
            },
            {
                "title": "Unit 12 – Articles & Determiners",
                "topics": ["Hot Words: life, time", "Linking and Commenting"],
            },
        ],
    },
    # ─── 6. AVANÇADO (C1) ────────────────────────────────────────────────────
    {
        "name": "ingles-avancado",
        "title": "Inglês - Avançado",
        "level_code": "C1",
        "category": "Inglês - Avançado",
        "short_description": (
            "Nível C1 | Inversão negativa, discourse markers, passive reporting, "
            "subjuntivo e domínio total de phrasal verbs. 12 unidades para fluência plena."
        ),
        "long_description": (
            "<p>O <strong>Avançado (C1)</strong> é o nível máximo da trilha Vedium, "
            "preparando você para comunicação sofisticada em contextos executivos, "
            "acadêmicos e culturais.</p>"
            "<ul>"
            "<li>Revisão e correção de todos os tempos / Voz ativa vs. passiva</li>"
            "<li>Reflexivos / Phrasal verbs avançados / Idioms emocionais</li>"
            "<li>Adverbs & adjectives collocations / Adjective order</li>"
            "<li>Verb patterns: gerund/infinitive com mudança de significado</li>"
            "<li>Modals avançados: especulação, presente, futuro e passado</li>"
            "<li>Emphasis structures / Negative inversion / -ever</li>"
            "<li>Real and unreal tenses / Mixed conditionals</li>"
            "<li>Relative clauses / Participle clauses / Gender-neutral pronouns</li>"
            "<li>Discourse markers / Passive reporting / Future advanced forms</li>"
            "<li>Linking devices / Contrast linkers / Idioms</li>"
            "</ul>"
            "<p><strong>Duração estimada:</strong> 8–12 meses. <strong>Certificado</strong> incluso.</p>"
        ),
        "image": IMAGES["advanced"],
        "course_price": 240.00,
        "units": [
            {
                "title": "Unit 1 – Tense Review",
                "topics": [
                    "Check Your Tenses / Correcting Mistakes",
                    "Active or Passive? / Reflexive Pronouns",
                    "Reading: Robots versus Humans",
                    "Phrasal Verbs: An Overview / Idioms of Extreme Emotion / Word Formation",
                ],
            },
            {
                "title": "Unit 2 – Adverbs and Adjectives",
                "topics": [
                    "Adverb Collocations / Adverbs with Two Forms",
                    "Reading: Writers Talk About Their Writing",
                    "Adjectives with Positive/Negative Meaning / Adjective Order / Adding Drama",
                    "Adjective + Preposition",
                ],
            },
            {
                "title": "Unit 3 – Verb Patterns",
                "topics": [
                    "Verbs + Gerund or Infinitive / Change of Meaning",
                    "Sentence Transformation",
                    "Reading: Was This a President for Our Times?",
                    "Describing Trends / Phrasal Verbs: up and down",
                ],
            },
            {
                "title": "Unit 4 – Modal Auxiliary Verbs",
                "topics": [
                    "Speculating – Present and Future / Speculating – Past",
                    "Set Expressions with Modals / Other Meanings / Misleading Adverts",
                    "Idiomatic Collocations: Adjective + Noun / Onomatopoeic Verbs",
                    "Reading: Modern-Day Magic / Verb + Preposition",
                    "Exam Practice Units 1–4",
                ],
            },
            {
                "title": "Unit 5 – Avoiding Repetition",
                "topics": [
                    "Using Auxiliaries / Reduced Infinitives",
                    "Reading: Two Ways of Travelling",
                    "Synonyms in Context / Phrasal Verbs and Their Latin-Based Synonyms",
                ],
            },
            {
                "title": "Unit 6 – Emphasis",
                "topics": [
                    "Structures Which Add Emphasis / Negative Inversion",
                    "The Use of -ever for Emphasis",
                    "Verbs to Nouns / Compound Nouns with Prepositions",
                    "Pronunciation: Stress and Intonation",
                ],
            },
            {
                "title": "Unit 7 – Real and Unreal Tenses",
                "topics": [
                    "Real or Hypothetical? / would or had?",
                    "Mixed Conditionals / Forming the Correct Tense",
                    "Expressions with if / Synonyms: happy and sad",
                    "Look on the Bright Side! / Phrasal Verbs: on and off",
                ],
            },
            {
                "title": "Unit 8 – Relative Clauses & Participles",
                "topics": [
                    "Defining and Non-Defining Relative Clauses",
                    "Common Phrases with Relative Pronouns / Participle Clauses",
                    "Gender-Neutral Pronouns / Reading: Meet the First Female Footballers",
                    "Opposite Adjectives / Verb + Preposition / Crossword",
                    "Exam Practice Units 5–8",
                ],
            },
            {
                "title": "Unit 9 – Discourse Markers",
                "topics": [
                    "Attitude Markers",
                    "Reading: Zach Sobiech / A Review",
                    "Music Vocabulary / Pronunciation: Rhyming Words / Cockney Rhyming Slang",
                    "Phrasal Verbs: Verbs with a Particle and a Preposition",
                ],
            },
            {
                "title": "Unit 10 – Passive Reporting",
                "topics": [
                    "seem and appear / Reading: Monique Van Der Vorst",
                    "Reading: Charles Eugster",
                    "Prepositions in Passive Sentences / Words to Do with the Body",
                    "Pronunciation: Intonation in Question Tags",
                ],
            },
            {
                "title": "Unit 11 – Future Forms Advanced",
                "topics": [
                    "Names and Uses / Shades of Meaning / Other Future Expressions",
                    "Future in the Past / Reading: Future Technology",
                    "Phrasal Verbs: Literal and Metaphorical Meanings",
                    "Technology Idioms / Sounds and Spelling – Homophones",
                ],
            },
            {
                "title": "Unit 12 – Linking Devices",
                "topics": [
                    "Revision of Linkers / Using Contrast Linkers",
                    "Reading: The Midlife Crisis",
                    "Expressions with Light, Weather, and Food / Idioms with like / Idioms with as...as",
                    "Finding and Correcting Mistakes / Prepositions in Set Phrases",
                    "Exam Practice Units 9–12",
                ],
            },
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# PREÇOS (tabela de frequência — usada em create_pricing_table se integrada)
# ─────────────────────────────────────────────────────────────────────────────
PRICING_TABLE = [
    {
        "frequency": "1 Aula por Semana",
        "monthly_price": 240.00,
        "teacher_hour": 18.00,
        "duration": "1h",
    },
    {
        "frequency": "2 Aulas por Semana",
        "monthly_price": 440.00,
        "teacher_hour": 18.00,
        "duration": "1h",
    },
    {
        "frequency": "3 Aulas por Semana",
        "monthly_price": 640.00,
        "teacher_hour": 18.00,
        "duration": "1h",
    },
    {
        "frequency": "4 Aulas por Semana",
        "monthly_price": 860.00,
        "teacher_hour": 18.00,
        "duration": "1h",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _get_or_create_instructor() -> str:
    """Retorna email do instrutor padrão Vedium ou cria se não existir."""
    instructor_email = "professor@vediums.com"
    if not frappe.db.exists("User", instructor_email):
        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": instructor_email,
                "first_name": "Vedium",
                "last_name": "Instructor",
                "send_welcome_email": 0,
                "user_type": "Website User",
            }
        )
        user.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  ✓ Instrutor padrão criado: {instructor_email}")
    return instructor_email


def _build_chapter_lesson(course_name: str, unit: dict, unit_idx: int) -> None:
    """Cria Course Chapter primeiro, depois Course Lesson com link ao chapter."""
    chapter_title = unit["title"]

    # Verifica se chapter já existe
    existing = frappe.get_all(
        "Course Chapter",
        filters={"course": course_name, "title": chapter_title},
        fields=["name"],
        limit=1,
    )
    if existing:
        return

    # 1. Cria o Chapter primeiro (Course Lesson precisa de chapter obrigatório)
    chapter = frappe.get_doc(
        {
            "doctype": "Course Chapter",
            "title": chapter_title,
            "course": course_name,
        }
    )
    chapter.insert(ignore_permissions=True)
    chapter_name = chapter.name

    # 2. Cria Course Lesson para cada tópico com referência ao chapter criado
    for i, topic in enumerate(unit["topics"], start=1):
        lesson = frappe.get_doc(
            {
                "doctype": "Course Lesson",
                "title": topic,
                "chapter": chapter_name,
                "course": course_name,
                "body": f"<p>{topic}</p>",
            }
        )
        lesson.insert(ignore_permissions=True)
        chapter.append("lessons", {"lesson": lesson.name})

    # 3. Salva o chapter com as referências às lições
    chapter.save(ignore_permissions=True)


def _create_course(data: dict, instructor: str) -> None:
    """Cria um LMS Course completo com chapters e lessons."""
    # Busca pelo title para obter o name real gerado pelo Frappe
    existing = frappe.get_all(
        "LMS Course",
        filters={"title": data["title"]},
        fields=["name"],
        limit=1,
    )

    if existing:
        course_name = existing[0]["name"]
        print(f"  → Já existe: {data['title']} (name={course_name})")
    else:
        # Cria o curso com campos corretos do doctype LMS Course — sem forçar name
        doc = frappe.get_doc(
            {
                "doctype": "LMS Course",
                "title": data["title"],
                "short_introduction": data["short_description"][:140],
                "description": data["long_description"],
                "image": data["image"],
                "category": data["category"],
                "paid_course": 1,
                "course_price": data["course_price"],
                "currency": "BRL",
                "published": 1,
                "enable_certification": 1,
            }
        )
        # instructors é tabela filha (Course Instructor)
        doc.append("instructors", {"instructor": instructor})
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        # Usa o name gerado pelo Frappe (pode ser diferente do slug manual)
        course_name = doc.name
        print(
            f"  ✓ Curso criado: {data['title']} ({data['level_code']}) name={course_name}"
        )

    # Cria chapters e lições
    for i, unit in enumerate(data["units"], start=1):
        try:
            _build_chapter_lesson(course_name, unit, i)
        except Exception as e:
            print(f"    ⚠ Erro no chapter '{unit['title']}': {e}")

    frappe.db.commit()
    print(f"    → {len(data['units'])} unidades configuradas")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
def execute():
    """Entry point para: bench --site vediums.com execute create_english_courses.execute"""
    print("\n📚 Cadastrando Programa de Inglês — 6 Níveis (Frappe LMS)")
    print("=" * 60)

    instructor = _get_or_create_instructor()

    for course_data in ENGLISH_CURRICULUM:
        print(f"\n[{course_data['level_code']}] {course_data['title']}")
        try:
            _create_course(course_data, instructor)
        except Exception as e:
            print(f"  ✗ Erro ao criar curso: {e}")
            frappe.log_error(str(e), "create_english_courses")

    print("\n✅ Programa de Inglês cadastrado com sucesso!")
    print(f"   Total: {len(ENGLISH_CURRICULUM)} cursos")
    print(f"   Preço base: R$ 240,00/mês (1 aula/semana)")
    print(f"   Acesse: http://localhost:8005/courses")
    print("=" * 60)


if __name__ == "__main__":
    execute()

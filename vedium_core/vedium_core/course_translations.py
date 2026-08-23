"""Traduções de cursos individuais (/en|es|fr|de/curso/<slug>).

Só os cursos de Iorubá e PLE têm entrada aqui: o público desses dois
clusters inclui gente que não fala português (diáspora, expats). O cluster
de Inglês não precisa: quem busca aprender inglês na Vedium já fala PT.

Preço, vagas, avaliações, matrícula etc. continuam vindo ao vivo do banco
via curso.py: aqui só sobrepomos os campos de texto (title/short_introduction/
description). Sem Custom Field nem migração: é só um dict em código.

Estrutura: COURSE_TRANSLATIONS[slug][lang] = {title, short_introduction, description}.
"""

COURSE_TRANSLATIONS = {
    "iorub-b-sico": {
        "en": {
            "title": "Yoruba: Basic",
            "short_introduction": "Basic Level | Greetings, alphabet, tones, pronouns, numerals and everyday dialogues across 3 modules and 9 progressive lessons.",
            "description": (
                "<p>The <strong>Yoruba Basic</strong> course introduces the fundamentals of the "
                "Yoruba language and culture, preparing you to handle everyday situations and "
                "build a solid foundation for continued learning.</p>"
                "<p>Based on <em>Beginner's Yoruba</em> by Kayode J. Fakinlede (2005), you will master:</p>"
                "<ul>"
                "<li>Greetings, farewells and courtesy expressions</li>"
                "<li>Personal introductions: name and origin</li>"
                "<li>The Yoruba alphabet and the 3 tones (high, mid, low)</li>"
                "<li>Personal pronouns and high-frequency verbs</li>"
                "<li>Simple affirmative and negative sentences</li>"
                "<li>Numbers 1 to 10 and expressions of quantity</li>"
                "<li>Common adjectives and describing people/objects</li>"
                "<li>Simple proverbs and cultural aspects</li>"
                "</ul>"
                "<p><strong>Price:</strong> starting at R$ 320/month (1 class/week). "
                "Plans of 1 to 4 classes/week available.</p>"
                "<p><strong>Certificate:</strong> included upon completing all units.</p>"
            ),
        },
        "es": {
            "title": "Yoruba: Básico",
            "short_introduction": "Nivel Básico | Saludos, alfabeto, tonos, pronombres, numerales y diálogos cotidianos en 3 módulos y 9 lecciones progresivas.",
            "description": (
                "<p>El curso <strong>Yoruba Básico</strong> presenta los fundamentos del idioma y "
                "la cultura yoruba, preparándote para manejar situaciones cotidianas y construir "
                "una base sólida para seguir aprendiendo.</p>"
                "<p>Basado en <em>Beginner's Yoruba</em> de Kayode J. Fakinlede (2005), dominarás:</p>"
                "<ul>"
                "<li>Saludos, despedidas y expresiones de cortesía</li>"
                "<li>Presentaciones personales: nombre y origen</li>"
                "<li>El alfabeto yoruba y los 3 tonos (alto, medio, bajo)</li>"
                "<li>Pronombres personales y verbos de alta frecuencia</li>"
                "<li>Oraciones simples afirmativas y negativas</li>"
                "<li>Números del 1 al 10 y expresiones de cantidad</li>"
                "<li>Adjetivos comunes y descripción de personas/objetos</li>"
                "<li>Proverbios simples y aspectos culturales</li>"
                "</ul>"
                "<p><strong>Precio:</strong> desde R$ 320/mes (1 clase/semana). "
                "Planes de 1 a 4 clases/semana disponibles.</p>"
                "<p><strong>Certificado:</strong> incluido al completar todas las unidades.</p>"
            ),
        },
        "fr": {
            "title": "Yoruba: Débutant",
            "short_introduction": "Niveau Débutant | Salutations, alphabet, tons, pronoms, chiffres et dialogues du quotidien en 3 modules et 9 leçons progressives.",
            "description": (
                "<p>Le cours <strong>Yoruba Débutant</strong> présente les fondamentaux de la langue "
                "et de la culture yoruba, pour vous préparer à gérer des situations du quotidien et "
                "bâtir une base solide pour la suite de votre apprentissage.</p>"
                "<p>Basé sur <em>Beginner's Yoruba</em> de Kayode J. Fakinlede (2005), vous maîtriserez :</p>"
                "<ul>"
                "<li>Salutations, adieux et expressions de politesse</li>"
                "<li>Présentations personnelles: nom et origine</li>"
                "<li>L'alphabet yoruba et les 3 tons (haut, moyen, bas)</li>"
                "<li>Pronoms personnels et verbes à haute fréquence</li>"
                "<li>Phrases affirmatives et négatives simples</li>"
                "<li>Les nombres de 1 à 10 et les expressions de quantité</li>"
                "<li>Adjectifs courants et description de personnes/objets</li>"
                "<li>Proverbes simples et aspects culturels</li>"
                "</ul>"
                "<p><strong>Prix :</strong> à partir de 320 R$/mois (1 cours/semaine). "
                "Formules de 1 à 4 cours/semaine disponibles.</p>"
                "<p><strong>Certificat :</strong> inclus à la fin de toutes les unités.</p>"
            ),
        },
        "de": {
            "title": "Yoruba: Grundstufe",
            "short_introduction": "Grundstufe | Begrüßungen, Alphabet, Töne, Pronomen, Zahlen und Alltagsdialoge in 3 Modulen und 9 aufeinander aufbauenden Lektionen.",
            "description": (
                "<p>Der Kurs <strong>Yoruba Grundstufe</strong> vermittelt die Grundlagen der "
                "Yoruba-Sprache und -Kultur und bereitet Sie darauf vor, Alltagssituationen zu "
                "meistern und eine solide Basis für das weitere Lernen aufzubauen.</p>"
                "<p>Basierend auf <em>Beginner's Yoruba</em> von Kayode J. Fakinlede (2005), beherrschen Sie:</p>"
                "<ul>"
                "<li>Begrüßungen, Verabschiedungen und Höflichkeitsfloskeln</li>"
                "<li>Persönliche Vorstellung: Name und Herkunft</li>"
                "<li>Das Yoruba-Alphabet und die 3 Töne (hoch, mittel, tief)</li>"
                "<li>Personalpronomen und häufig verwendete Verben</li>"
                "<li>Einfache bejahende und verneinende Sätze</li>"
                "<li>Zahlen von 1 bis 10 und Mengenangaben</li>"
                "<li>Gebräuchliche Adjektive und die Beschreibung von Personen/Gegenständen</li>"
                "<li>Einfache Sprichwörter und kulturelle Aspekte</li>"
                "</ul>"
                "<p><strong>Preis:</strong> ab R$ 320/Monat (1 Unterrichtsstunde/Woche). "
                "Pakete mit 1 bis 4 Stunden/Woche verfügbar.</p>"
                "<p><strong>Zertifikat:</strong> nach Abschluss aller Einheiten inbegriffen.</p>"
            ),
        },
        "ru": {
            "title": "Йоруба: Базовый",
            "short_introduction": "Базовый уровень | Приветствия, алфавит, тона, местоимения, числительные и повседневные диалоги в 3 модулях и 9 последовательных уроках.",
            "description": (
                "<p>Курс <strong>Йоруба Базовый</strong> знакомит с основами языка и культуры "
                "йоруба, готовя вас справляться с повседневными ситуациями и создавая прочную "
                "основу для дальнейшего обучения.</p>"
                "<p>На основе <em>Beginner's Yoruba</em> Кайоде Дж. Факинледе (2005) вы освоите:</p>"
                "<ul>"
                "<li>Приветствия, прощания и вежливые выражения</li>"
                "<li>Личное представление: имя и происхождение</li>"
                "<li>Алфавит йоруба и 3 тона (высокий, средний, низкий)</li>"
                "<li>Личные местоимения и часто употребляемые глаголы</li>"
                "<li>Простые утвердительные и отрицательные предложения</li>"
                "<li>Числа от 1 до 10 и выражения количества</li>"
                "<li>Распространённые прилагательные и описание людей/предметов</li>"
                "<li>Простые пословицы и культурные аспекты</li>"
                "</ul>"
                "<p><strong>Цена:</strong> от R$ 320/месяц (1 занятие/неделю). "
                "Доступны пакеты от 1 до 4 занятий/неделю.</p>"
                "<p><strong>Сертификат:</strong> включён по завершении всех модулей.</p>"
            ),
        },
    },
    "iorub-intermedi-rio": {
        "en": {
            "title": "Yoruba: Intermediate",
            "short_introduction": "Intermediate Level | Word classes, serial verbs, verbal aspects, idiomatic expressions and advanced conversation. 3 modules.",
            "description": (
                "<p>The <strong>Yoruba Intermediate</strong> course deepens grammar and language "
                "structure, allowing you to express more complex ideas and take part in "
                "elaborate conversations.</p>"
                "<p>Based on <em>Essentials of Yoruba Grammar</em> by Oladele Awobuluyi (1978), "
                "you will master:</p>"
                "<ul>"
                "<li>Nouns: human/non-human categories, quantity, place, compounds</li>"
                "<li>Qualifiers: numerals, demonstratives, relatives, genitives</li>"
                "<li>Serial verbs and splitting verbs</li>"
                "<li>Verbal aspects: progressive and perfective</li>"
                "<li>Complex proverbs and idiomatic expressions</li>"
                "<li>Reading short Yoruba texts (short stories, news)</li>"
                "<li>Debates, role-plays and oral presentations</li>"
                "</ul>"
                "<p><strong>Price:</strong> starting at R$ 320/month (1 class/week).</p>"
                "<p><strong>Certificate:</strong> included upon completing all units.</p>"
            ),
        },
        "es": {
            "title": "Yoruba: Intermedio",
            "short_introduction": "Nivel Intermedio | Clases de palabras, verbos seriales, aspectos verbales, expresiones idiomáticas y conversación avanzada. 3 módulos.",
            "description": (
                "<p>El curso <strong>Yoruba Intermedio</strong> profundiza en la gramática y la "
                "estructura del idioma, permitiéndote expresar ideas más complejas y participar "
                "en conversaciones elaboradas.</p>"
                "<p>Basado en <em>Essentials of Yoruba Grammar</em> de Oladele Awobuluyi (1978), dominarás:</p>"
                "<ul>"
                "<li>Sustantivos: categorías humanas/no humanas, cantidad, lugar, compuestos</li>"
                "<li>Calificadores: numerales, demostrativos, relativos, genitivos</li>"
                "<li>Verbos seriales y verbos divididos</li>"
                "<li>Aspectos verbales: progresivo y perfectivo</li>"
                "<li>Proverbios complejos y expresiones idiomáticas</li>"
                "<li>Lectura de textos cortos en yoruba (cuentos, noticias)</li>"
                "<li>Debates, juegos de rol y presentaciones orales</li>"
                "</ul>"
                "<p><strong>Precio:</strong> desde R$ 320/mes (1 clase/semana).</p>"
                "<p><strong>Certificado:</strong> incluido al completar todas las unidades.</p>"
            ),
        },
        "fr": {
            "title": "Yoruba: Intermédiaire",
            "short_introduction": "Niveau Intermédiaire | Classes de mots, verbes sériels, aspects verbaux, expressions idiomatiques et conversation avancée. 3 modules.",
            "description": (
                "<p>Le cours <strong>Yoruba Intermédiaire</strong> approfondit la grammaire et la "
                "structure de la langue, vous permettant d'exprimer des idées plus complexes et "
                "de participer à des conversations élaborées.</p>"
                "<p>Basé sur <em>Essentials of Yoruba Grammar</em> d'Oladele Awobuluyi (1978), vous maîtriserez :</p>"
                "<ul>"
                "<li>Noms : catégories humaines/non humaines, quantité, lieu, composés</li>"
                "<li>Qualificatifs : numéraux, démonstratifs, relatifs, génitifs</li>"
                "<li>Verbes sériels et verbes scindés</li>"
                "<li>Aspects verbaux : progressif et accompli</li>"
                "<li>Proverbes complexes et expressions idiomatiques</li>"
                "<li>Lecture de textes courts en yoruba (nouvelles, actualités)</li>"
                "<li>Débats, jeux de rôle et présentations orales</li>"
                "</ul>"
                "<p><strong>Prix :</strong> à partir de 320 R$/mois (1 cours/semaine).</p>"
                "<p><strong>Certificat :</strong> inclus à la fin de toutes les unités.</p>"
            ),
        },
        "de": {
            "title": "Yoruba: Mittelstufe",
            "short_introduction": "Mittelstufe | Wortarten, Serienverben, Verbalaspekte, idiomatische Ausdrücke und fortgeschrittene Konversation. 3 Module.",
            "description": (
                "<p>Der Kurs <strong>Yoruba Mittelstufe</strong> vertieft Grammatik und "
                "Sprachstruktur und ermöglicht es Ihnen, komplexere Ideen auszudrücken und an "
                "ausführlichen Gesprächen teilzunehmen.</p>"
                "<p>Basierend auf <em>Essentials of Yoruba Grammar</em> von Oladele Awobuluyi (1978), beherrschen Sie:</p>"
                "<ul>"
                "<li>Substantive: menschliche/nichtmenschliche Kategorien, Menge, Ort, Komposita</li>"
                "<li>Bestimmungswörter: Zahlwörter, Demonstrativa, Relativa, Genitive</li>"
                "<li>Serienverben und geteilte Verben</li>"
                "<li>Verbalaspekte: progressiv und perfektiv</li>"
                "<li>Komplexe Sprichwörter und idiomatische Ausdrücke</li>"
                "<li>Lesen kurzer Yoruba-Texte (Kurzgeschichten, Nachrichten)</li>"
                "<li>Debatten, Rollenspiele und mündliche Präsentationen</li>"
                "</ul>"
                "<p><strong>Preis:</strong> ab R$ 320/Monat (1 Unterrichtsstunde/Woche).</p>"
                "<p><strong>Zertifikat:</strong> nach Abschluss aller Einheiten inbegriffen.</p>"
            ),
        },
        "ru": {
            "title": "Йоруба: Средний уровень",
            "short_introduction": "Средний уровень | Части речи, серийные глаголы, глагольные аспекты, идиоматические выражения и продвинутая разговорная речь. 3 модуля.",
            "description": (
                "<p>Курс <strong>Йоруба Средний уровень</strong> углубляет грамматику и "
                "языковую структуру, позволяя вам выражать более сложные идеи и участвовать в "
                "развёрнутых беседах.</p>"
                "<p>На основе <em>Essentials of Yoruba Grammar</em> Оладеле Авобулуйи (1978) вы освоите:</p>"
                "<ul>"
                "<li>Существительные: человеческие/нечеловеческие категории, количество, место, композиты</li>"
                "<li>Определители: числительные, указательные, относительные, притяжательные</li>"
                "<li>Серийные глаголы и раздельные глаголы</li>"
                "<li>Глагольные аспекты: прогрессивный и перфективный</li>"
                "<li>Сложные пословицы и идиоматические выражения</li>"
                "<li>Чтение коротких текстов на йоруба (рассказы, новости)</li>"
                "<li>Дебаты, ролевые игры и устные презентации</li>"
                "</ul>"
                "<p><strong>Цена:</strong> от R$ 320/месяц (1 занятие/неделю).</p>"
                "<p><strong>Сертификат:</strong> включён по завершении всех модулей.</p>"
            ),
        },
    },
    "iorub-avan-ado": {
        "en": {
            "title": "Yoruba: Advanced",
            "short_introduction": "Advanced Level | Complex grammar, literature, history and Yoruba philosophy. Fluency in academic, professional and cultural contexts.",
            "description": (
                "<p>The <strong>Yoruba Advanced</strong> course is for students with a solid "
                "command of the language who are seeking full fluency and proficiency.</p>"
                "<p>Based on <em>Essentials of Yoruba Grammar</em> (Awobuluyi, 1978) and "
                "<em>A History of the Yoruba People</em> (Akintoye, 2014), you will master:</p>"
                "<ul>"
                "<li>Subordinate and coordinate clauses, active/passive voice</li>"
                "<li>Morphology and derivation: prefixes, suffixes, infixes</li>"
                "<li>Advanced modal and aspectual particles</li>"
                "<li>Analysis of literary texts (short stories, poetry, plays)</li>"
                "<li>Rhetoric, oratory and formal discourse in Yoruba</li>"
                "<li>Principles of Yoruba ↔ English translation</li>"
                "<li>History of the Yoruba kingdoms and empires</li>"
                "<li>Orishas, worldview and philosophy (Àṣẹ, Ìwà pẹ̀lẹ́)</li>"
                "<li>Contemporary Yoruba society and the diaspora</li>"
                "</ul>"
                "<p><strong>Price:</strong> starting at R$ 320/month (1 class/week).</p>"
                "<p><strong>Certificate:</strong> included upon completing all units.</p>"
            ),
        },
        "es": {
            "title": "Yoruba: Avanzado",
            "short_introduction": "Nivel Avanzado | Gramática compleja, literatura, historia y filosofía yoruba. Fluidez en contextos académicos, profesionales y culturales.",
            "description": (
                "<p>El curso <strong>Yoruba Avanzado</strong> está dirigido a estudiantes con un "
                "dominio sólido del idioma que buscan alcanzar fluidez y competencia total.</p>"
                "<p>Basado en <em>Essentials of Yoruba Grammar</em> (Awobuluyi, 1978) y "
                "<em>A History of the Yoruba People</em> (Akintoye, 2014), dominarás:</p>"
                "<ul>"
                "<li>Oraciones subordinadas y coordinadas, voz activa/pasiva</li>"
                "<li>Morfología y derivación: prefijos, sufijos, infijos</li>"
                "<li>Partículas modales y aspectuales avanzadas</li>"
                "<li>Análisis de textos literarios (cuentos, poesía, obras de teatro)</li>"
                "<li>Retórica, oratoria y discurso formal en yoruba</li>"
                "<li>Principios de traducción yoruba ↔ inglés</li>"
                "<li>Historia de los reinos e imperios yoruba</li>"
                "<li>Orishas, cosmovisión y filosofía (Àṣẹ, Ìwà pẹ̀lẹ́)</li>"
                "<li>Sociedad yoruba contemporánea y la diáspora</li>"
                "</ul>"
                "<p><strong>Precio:</strong> desde R$ 320/mes (1 clase/semana).</p>"
                "<p><strong>Certificado:</strong> incluido al completar todas las unidades.</p>"
            ),
        },
        "fr": {
            "title": "Yoruba: Avancé",
            "short_introduction": "Niveau Avancé | Grammaire complexe, littérature, histoire et philosophie yoruba. Aisance dans des contextes académiques, professionnels et culturels.",
            "description": (
                "<p>Le cours <strong>Yoruba Avancé</strong> s'adresse aux étudiants ayant une "
                "solide maîtrise de la langue et souhaitant atteindre une pleine aisance et "
                "compétence.</p>"
                "<p>Basé sur <em>Essentials of Yoruba Grammar</em> (Awobuluyi, 1978) et "
                "<em>A History of the Yoruba People</em> (Akintoye, 2014), vous maîtriserez :</p>"
                "<ul>"
                "<li>Propositions subordonnées et coordonnées, voix active/passive</li>"
                "<li>Morphologie et dérivation : préfixes, suffixes, infixes</li>"
                "<li>Particules modales et aspectuelles avancées</li>"
                "<li>Analyse de textes littéraires (nouvelles, poésie, pièces de théâtre)</li>"
                "<li>Rhétorique, art oratoire et discours formel en yoruba</li>"
                "<li>Principes de traduction yoruba ↔ anglais</li>"
                "<li>Histoire des royaumes et empires yoruba</li>"
                "<li>Orishas, vision du monde et philosophie (Àṣẹ, Ìwà pẹ̀lẹ́)</li>"
                "<li>Société yoruba contemporaine et diaspora</li>"
                "</ul>"
                "<p><strong>Prix :</strong> à partir de 320 R$/mois (1 cours/semaine).</p>"
                "<p><strong>Certificat :</strong> inclus à la fin de toutes les unités.</p>"
            ),
        },
        "de": {
            "title": "Yoruba: Fortgeschritten",
            "short_introduction": "Fortgeschrittenenstufe | Komplexe Grammatik, Literatur, Geschichte und Yoruba-Philosophie. Sprachgewandtheit in akademischen, beruflichen und kulturellen Kontexten.",
            "description": (
                "<p>Der Kurs <strong>Yoruba Fortgeschritten</strong> richtet sich an Studierende "
                "mit soliden Sprachkenntnissen, die volle Sprachgewandtheit und Kompetenz "
                "anstreben.</p>"
                "<p>Basierend auf <em>Essentials of Yoruba Grammar</em> (Awobuluyi, 1978) und "
                "<em>A History of the Yoruba People</em> (Akintoye, 2014), beherrschen Sie:</p>"
                "<ul>"
                "<li>Neben- und Hauptsätze, Aktiv/Passiv</li>"
                "<li>Morphologie und Wortbildung: Präfixe, Suffixe, Infixe</li>"
                "<li>Fortgeschrittene modale und aspektuelle Partikeln</li>"
                "<li>Analyse literarischer Texte (Kurzgeschichten, Lyrik, Theaterstücke)</li>"
                "<li>Rhetorik, Redekunst und formelle Rede auf Yoruba</li>"
                "<li>Grundlagen der Übersetzung Yoruba ↔ Englisch</li>"
                "<li>Geschichte der Yoruba-Königreiche und -Reiche</li>"
                "<li>Orishas, Weltanschauung und Philosophie (Àṣẹ, Ìwà pẹ̀lẹ́)</li>"
                "<li>Zeitgenössische Yoruba-Gesellschaft und Diaspora</li>"
                "</ul>"
                "<p><strong>Preis:</strong> ab R$ 320/Monat (1 Unterrichtsstunde/Woche).</p>"
                "<p><strong>Zertifikat:</strong> nach Abschluss aller Einheiten inbegriffen.</p>"
            ),
        },
        "ru": {
            "title": "Йоруба: Продвинутый уровень",
            "short_introduction": "Продвинутый уровень | Сложная грамматика, литература, история и философия йоруба. Беглость речи в академическом, профессиональном и культурном контексте.",
            "description": (
                "<p>Курс <strong>Йоруба Продвинутый</strong> рассчитан на студентов с "
                "прочными языковыми знаниями, стремящихся к полной беглости речи и компетенции.</p>"
                "<p>На основе <em>Essentials of Yoruba Grammar</em> (Авобулуйи, 1978) и "
                "<em>A History of the Yoruba People</em> (Акинтойе, 2014) вы освоите:</p>"
                "<ul>"
                "<li>Придаточные и главные предложения, активный/пассивный залог</li>"
                "<li>Морфология и словообразование: приставки, суффиксы, инфиксы</li>"
                "<li>Продвинутые модальные и аспектуальные частицы</li>"
                "<li>Анализ литературных текстов (рассказы, поэзия, пьесы)</li>"
                "<li>Риторика, ораторское искусство и формальная речь на йоруба</li>"
                "<li>Основы перевода йоруба ↔ английский</li>"
                "<li>История королевств и империй йоруба</li>"
                "<li>Ориша, мировоззрение и философия (Àṣẹ, Ìwà pẹ̀lẹ́)</li>"
                "<li>Современное общество йоруба и диаспора</li>"
                "</ul>"
                "<p><strong>Цена:</strong> от R$ 320/месяц (1 занятие/неделю).</p>"
                "<p><strong>Сертификат:</strong> включён по завершении всех модулей.</p>"
            ),
        },
    },
    "portugues-para-estrangeiros-basico": {
        "en": {
            "title": "Portuguese for Foreigners: Basic Level (PLE)",
            "short_introduction": "For complete beginners. Learn greetings, essential vocabulary and basic Brazilian Portuguese communication with cultural immersion from the first class.",
            "description": (
                "<p>The <strong>PLE Basic</strong> course is for those with no prior knowledge or "
                "very limited contact with Portuguese. You'll learn the essential structures and "
                "vocabulary needed to communicate in everyday situations, with strong immersion "
                "in Brazilian culture.</p>"
                "<p><strong>By the end of the course you will be able to:</strong></p>"
                "<ul>"
                "<li>Use greetings, introductions and farewells</li>"
                "<li>Give and ask for personal information (name, nationality, age, profession)</li>"
                "<li>Form simple sentences in the present indicative</li>"
                "<li>Order at restaurants, go shopping and ask for directions</li>"
                "<li>Understand basic aspects of Brazilian culture</li>"
                "</ul>"
            ),
        },
        "es": {
            "title": "Portugués para Extranjeros: Nivel Básico (PLE)",
            "short_introduction": "Para principiantes absolutos. Aprende saludos, vocabulario esencial y comunicación básica en portugués brasileño con inmersión cultural desde la primera clase.",
            "description": (
                "<p>El curso <strong>PLE Básico</strong> está dirigido a quienes no tienen "
                "conocimientos previos o tienen un contacto muy limitado con el portugués. "
                "Aprenderás las estructuras y el vocabulario esenciales para comunicarte en "
                "situaciones cotidianas, con una fuerte inmersión en la cultura brasileña.</p>"
                "<p><strong>Al finalizar el curso podrás:</strong></p>"
                "<ul>"
                "<li>Usar saludos, presentaciones y despedidas</li>"
                "<li>Dar y pedir información personal (nombre, nacionalidad, edad, profesión)</li>"
                "<li>Formar oraciones simples en presente de indicativo</li>"
                "<li>Pedir en restaurantes, ir de compras y preguntar direcciones</li>"
                "<li>Comprender aspectos básicos de la cultura brasileña</li>"
                "</ul>"
            ),
        },
        "fr": {
            "title": "Portugais pour Étrangers: Niveau Débutant (PLE)",
            "short_introduction": "Pour les grands débutants. Apprenez les salutations, le vocabulaire essentiel et la communication de base en portugais brésilien, avec une immersion culturelle dès le premier cours.",
            "description": (
                "<p>Le cours <strong>PLE Débutant</strong> s'adresse à ceux qui n'ont aucune "
                "connaissance préalable ou un contact très limité avec le portugais. Vous "
                "apprendrez les structures et le vocabulaire essentiels pour communiquer dans "
                "des situations du quotidien, avec une forte immersion dans la culture "
                "brésilienne.</p>"
                "<p><strong>À la fin du cours, vous serez capable de :</strong></p>"
                "<ul>"
                "<li>Utiliser les salutations, les présentations et les adieux</li>"
                "<li>Donner et demander des informations personnelles (nom, nationalité, âge, profession)</li>"
                "<li>Former des phrases simples au présent de l'indicatif</li>"
                "<li>Commander au restaurant, faire des courses et demander son chemin</li>"
                "<li>Comprendre les aspects de base de la culture brésilienne</li>"
                "</ul>"
            ),
        },
        "de": {
            "title": "Portugiesisch für Ausländer: Grundstufe (PLE)",
            "short_introduction": "Für absolute Anfänger. Lernen Sie Begrüßungen, wesentlichen Wortschatz und grundlegende brasilianische Portugiesisch-Kommunikation mit kultureller Immersion ab der ersten Stunde.",
            "description": (
                "<p>Der Kurs <strong>PLE Grundstufe</strong> richtet sich an Personen ohne "
                "Vorkenntnisse oder mit sehr begrenztem Kontakt zur portugiesischen Sprache. Sie "
                "lernen die wesentlichen Strukturen und den Wortschatz, um in Alltagssituationen "
                "zu kommunizieren, mit starker Immersion in die brasilianische Kultur.</p>"
                "<p><strong>Am Ende des Kurses können Sie:</strong></p>"
                "<ul>"
                "<li>Begrüßungen, Vorstellungen und Verabschiedungen verwenden</li>"
                "<li>Persönliche Informationen geben und erfragen (Name, Nationalität, Alter, Beruf)</li>"
                "<li>Einfache Sätze im Präsens bilden</li>"
                "<li>Im Restaurant bestellen, einkaufen gehen und nach dem Weg fragen</li>"
                "<li>Grundlegende Aspekte der brasilianischen Kultur verstehen</li>"
                "</ul>"
            ),
        },
        "ru": {
            "title": "Португальский для иностранцев: Базовый уровень (PLE)",
            "short_introduction": "Для абсолютных новичков. Изучите приветствия, основную лексику и базовое общение на бразильском португальском с культурным погружением с первого занятия.",
            "description": (
                "<p>Курс <strong>PLE Базовый уровень</strong> рассчитан на людей без "
                "предварительных знаний или с очень ограниченным контактом с португальским "
                "языком. Вы изучите основные структуры и лексику для общения в повседневных "
                "ситуациях, с сильным погружением в бразильскую культуру.</p>"
                "<p><strong>По завершении курса вы сможете:</strong></p>"
                "<ul>"
                "<li>Использовать приветствия, представления и прощания</li>"
                "<li>Давать и запрашивать личную информацию (имя, национальность, возраст, профессия)</li>"
                "<li>Строить простые предложения в настоящем времени</li>"
                "<li>Заказывать в ресторане, делать покупки и спрашивать дорогу</li>"
                "<li>Понимать основные аспекты бразильской культуры</li>"
                "</ul>"
            ),
        },
    },
    "portugues-para-estrangeiros-intermediario": {
        "en": {
            "title": "Portuguese for Foreigners: Intermediate Level (PLE)",
            "short_introduction": "For those who already have a base in Portuguese. Master the past tenses, expand your vocabulary and gain fluency in social and professional situations.",
            "description": (
                "<p>The <strong>PLE Intermediate</strong> course is for those who already have a "
                "solid foundation in Portuguese and want to expand their ability to communicate "
                "in more varied and complex contexts. This level deepens grammar, broadens "
                "vocabulary and develops fluency in social and professional situations.</p>"
                "<p><strong>By the end of the course you will be able to:</strong></p>"
                "<ul>"
                "<li>Take part in longer, more detailed conversations on a range of topics</li>"
                "<li>Master the past tenses (preterite, imperfect and pluperfect)</li>"
                "<li>Handle situations like planning trips, looking for housing and talking about health</li>"
                "<li>Read and understand moderately difficult texts (news, opinion articles)</li>"
                "<li>Recognize and discuss deeper cultural aspects of Brazil</li>"
                "</ul>"
            ),
        },
        "es": {
            "title": "Portugués para Extranjeros: Nivel Intermedio (PLE)",
            "short_introduction": "Para quienes ya tienen una base en portugués. Domina los tiempos del pasado, amplía tu vocabulario y gana fluidez en situaciones sociales y profesionales.",
            "description": (
                "<p>El curso <strong>PLE Intermedio</strong> está dirigido a quienes ya tienen "
                "una base sólida en portugués y quieren ampliar su capacidad de comunicarse en "
                "contextos más variados y complejos. Este nivel profundiza la gramática, amplía "
                "el vocabulario y desarrolla fluidez en situaciones sociales y profesionales.</p>"
                "<p><strong>Al finalizar el curso podrás:</strong></p>"
                "<ul>"
                "<li>Participar en conversaciones más largas y detalladas sobre diversos temas</li>"
                "<li>Dominar los tiempos del pasado (pretérito, imperfecto y pluscuamperfecto)</li>"
                "<li>Manejar situaciones como planificar viajes, buscar vivienda y hablar de salud</li>"
                "<li>Leer y comprender textos de dificultad moderada (noticias, artículos de opinión)</li>"
                "<li>Reconocer y discutir aspectos culturales más profundos de Brasil</li>"
                "</ul>"
            ),
        },
        "fr": {
            "title": "Portugais pour Étrangers: Niveau Intermédiaire (PLE)",
            "short_introduction": "Pour ceux qui ont déjà une base en portugais. Maîtrisez les temps du passé, enrichissez votre vocabulaire et gagnez en aisance dans des situations sociales et professionnelles.",
            "description": (
                "<p>Le cours <strong>PLE Intermédiaire</strong> s'adresse à ceux qui ont déjà une "
                "base solide en portugais et souhaitent élargir leur capacité à communiquer dans "
                "des contextes plus variés et complexes. Ce niveau approfondit la grammaire, "
                "enrichit le vocabulaire et développe l'aisance dans des situations sociales et "
                "professionnelles.</p>"
                "<p><strong>À la fin du cours, vous serez capable de :</strong></p>"
                "<ul>"
                "<li>Participer à des conversations plus longues et détaillées sur divers sujets</li>"
                "<li>Maîtriser les temps du passé (passé simple, imparfait et plus-que-parfait)</li>"
                "<li>Gérer des situations telles que planifier un voyage, chercher un logement et parler de santé</li>"
                "<li>Lire et comprendre des textes de difficulté modérée (actualités, articles d'opinion)</li>"
                "<li>Reconnaître et discuter des aspects culturels plus approfondis du Brésil</li>"
                "</ul>"
            ),
        },
        "de": {
            "title": "Portugiesisch für Ausländer: Mittelstufe (PLE)",
            "short_introduction": "Für alle, die bereits Grundkenntnisse in Portugiesisch haben. Beherrschen Sie die Vergangenheitsformen, erweitern Sie Ihren Wortschatz und gewinnen Sie Sicherheit in sozialen und beruflichen Situationen.",
            "description": (
                "<p>Der Kurs <strong>PLE Mittelstufe</strong> richtet sich an Personen mit soliden "
                "Grundkenntnissen in Portugiesisch, die ihre Kommunikationsfähigkeit in "
                "vielfältigeren und komplexeren Kontexten erweitern möchten. Diese Stufe vertieft "
                "die Grammatik, erweitert den Wortschatz und entwickelt Sprachgewandtheit in "
                "sozialen und beruflichen Situationen.</p>"
                "<p><strong>Am Ende des Kurses können Sie:</strong></p>"
                "<ul>"
                "<li>An längeren, ausführlicheren Gesprächen zu verschiedenen Themen teilnehmen</li>"
                "<li>Die Vergangenheitsformen beherrschen (Präteritum, Imperfekt und Plusquamperfekt)</li>"
                "<li>Situationen wie Reiseplanung, Wohnungssuche und Gesundheitsgespräche bewältigen</li>"
                "<li>Texte mittleren Schwierigkeitsgrads lesen und verstehen (Nachrichten, Meinungsartikel)</li>"
                "<li>Tiefere kulturelle Aspekte Brasiliens erkennen und diskutieren</li>"
                "</ul>"
            ),
        },
        "ru": {
            "title": "Португальский для иностранцев: Средний уровень (PLE)",
            "short_introduction": "Для тех, у кого уже есть базовые знания португальского. Освойте прошедшие времена, расширьте словарный запас и обретите уверенность в социальных и профессиональных ситуациях.",
            "description": (
                "<p>Курс <strong>PLE Средний уровень</strong> рассчитан на людей с прочными "
                "базовыми знаниями португальского, желающих расширить свои коммуникативные "
                "навыки в более разнообразных и сложных контекстах. Этот уровень углубляет "
                "грамматику, расширяет словарный запас и развивает беглость речи в социальных "
                "и профессиональных ситуациях.</p>"
                "<p><strong>По завершении курса вы сможете:</strong></p>"
                "<ul>"
                "<li>Участвовать в более длинных, развёрнутых беседах на разные темы</li>"
                "<li>Владеть прошедшими временами (претерит, имперфект и плюсквамперфект)</li>"
                "<li>Справляться с ситуациями планирования поездок, поиска жилья и разговоров о здоровье</li>"
                "<li>Читать и понимать тексты среднего уровня сложности (новости, статьи мнений)</li>"
                "<li>Распознавать и обсуждать более глубокие культурные аспекты Бразилии</li>"
                "</ul>"
            ),
        },
    },
    "portugues-para-estrangeiros-avancado": {
        "en": {
            "title": "Portuguese for Foreigners: Advanced Level (PLE)",
            "short_introduction": "For those who already have fluency and want to refine it. Master the subjunctive, authentic texts and Portuguese in academic and professional contexts.",
            "description": (
                "<p>The <strong>PLE Advanced</strong> course is for those who already have "
                "significant fluency and want to refine their use of the language in complex "
                "academic, professional and cultural contexts. This level covers the subjunctive "
                "mood, analysis of authentic texts and a deeper dive into Brazilian culture and "
                "society.</p>"
                "<p><strong>By the end of the course you will be able to:</strong></p>"
                "<ul>"
                "<li>Understand and produce complex texts: opinion pieces, essays and reports</li>"
                "<li>Master the subjunctive mood in its various forms</li>"
                "<li>Actively take part in debates on abstract and controversial topics</li>"
                "<li>Use idiomatic expressions, slang and nuances of colloquial and formal language</li>"
                "<li>Critically analyze aspects of Brazilian history, politics, literature and the arts</li>"
                "</ul>"
            ),
        },
        "es": {
            "title": "Portugués para Extranjeros: Nivel Avanzado (PLE)",
            "short_introduction": "Para quienes ya tienen fluidez y quieren perfeccionarla. Domina el subjuntivo, textos auténticos y el portugués en contextos académicos y profesionales.",
            "description": (
                "<p>El curso <strong>PLE Avanzado</strong> está dirigido a quienes ya tienen una "
                "fluidez significativa y quieren perfeccionar el uso del idioma en contextos "
                "académicos, profesionales y culturales complejos. Este nivel abarca el modo "
                "subjuntivo, el análisis de textos auténticos y una inmersión más profunda en "
                "la cultura y sociedad brasileñas.</p>"
                "<p><strong>Al finalizar el curso podrás:</strong></p>"
                "<ul>"
                "<li>Comprender y producir textos complejos: artículos de opinión, ensayos e informes</li>"
                "<li>Dominar el modo subjuntivo en sus diversas formas</li>"
                "<li>Participar activamente en debates sobre temas abstractos y controvertidos</li>"
                "<li>Usar expresiones idiomáticas, jerga y matices del lenguaje coloquial y formal</li>"
                "<li>Analizar críticamente aspectos de la historia, política, literatura y artes de Brasil</li>"
                "</ul>"
            ),
        },
        "fr": {
            "title": "Portugais pour Étrangers: Niveau Avancé (PLE)",
            "short_introduction": "Pour ceux qui ont déjà une bonne aisance et souhaitent la perfectionner. Maîtrisez le subjonctif, les textes authentiques et le portugais dans des contextes académiques et professionnels.",
            "description": (
                "<p>Le cours <strong>PLE Avancé</strong> s'adresse à ceux qui ont déjà une "
                "aisance significative et souhaitent perfectionner leur usage de la langue dans "
                "des contextes académiques, professionnels et culturels complexes. Ce niveau "
                "couvre le mode subjonctif, l'analyse de textes authentiques et une immersion "
                "plus approfondie dans la culture et la société brésiliennes.</p>"
                "<p><strong>À la fin du cours, vous serez capable de :</strong></p>"
                "<ul>"
                "<li>Comprendre et produire des textes complexes: articles d'opinion, essais et rapports</li>"
                "<li>Maîtriser le mode subjonctif sous ses différentes formes</li>"
                "<li>Participer activement à des débats sur des sujets abstraits et controversés</li>"
                "<li>Utiliser des expressions idiomatiques, l'argot et les nuances du langage familier et soutenu</li>"
                "<li>Analyser de façon critique des aspects de l'histoire, de la politique, de la littérature et des arts du Brésil</li>"
                "</ul>"
            ),
        },
        "de": {
            "title": "Portugiesisch für Ausländer: Fortgeschrittenenstufe (PLE)",
            "short_introduction": "Für alle, die bereits fließend sprechen und dies verfeinern möchten. Beherrschen Sie den Konjunktiv, authentische Texte und Portugiesisch in akademischen und beruflichen Kontexten.",
            "description": (
                "<p>Der Kurs <strong>PLE Fortgeschritten</strong> richtet sich an Personen, die "
                "bereits über beachtliche Sprachgewandtheit verfügen und ihren Sprachgebrauch in "
                "komplexen akademischen, beruflichen und kulturellen Kontexten verfeinern "
                "möchten. Diese Stufe behandelt den Konjunktiv, die Analyse authentischer Texte "
                "sowie eine tiefere Auseinandersetzung mit der brasilianischen Kultur und "
                "Gesellschaft.</p>"
                "<p><strong>Am Ende des Kurses können Sie:</strong></p>"
                "<ul>"
                "<li>Komplexe Texte verstehen und verfassen: Meinungsartikel, Essays und Berichte</li>"
                "<li>Den Konjunktiv in seinen verschiedenen Formen beherrschen</li>"
                "<li>Aktiv an Debatten über abstrakte und kontroverse Themen teilnehmen</li>"
                "<li>Idiomatische Ausdrücke, Umgangssprache und Nuancen der Alltags- und Formalsprache verwenden</li>"
                "<li>Aspekte der brasilianischen Geschichte, Politik, Literatur und Kunst kritisch analysieren</li>"
                "</ul>"
            ),
        },
        "ru": {
            "title": "Португальский для иностранцев: Продвинутый уровень (PLE)",
            "short_introduction": "Для тех, кто уже свободно говорит и хочет усовершенствовать язык. Освойте сослагательное наклонение, аутентичные тексты и португальский в академическом и профессиональном контексте.",
            "description": (
                "<p>Курс <strong>PLE Продвинутый уровень</strong> рассчитан на людей, уже "
                "обладающих значительной беглостью речи и желающих усовершенствовать владение "
                "языком в сложном академическом, профессиональном и культурном контексте. Этот "
                "уровень охватывает сослагательное наклонение, анализ аутентичных текстов, а "
                "также более глубокое погружение в бразильскую культуру и общество.</p>"
                "<p><strong>По завершении курса вы сможете:</strong></p>"
                "<ul>"
                "<li>Понимать и писать сложные тексты: статьи мнений, эссе и отчёты</li>"
                "<li>Владеть сослагательным наклонением в его различных формах</li>"
                "<li>Активно участвовать в дебатах на абстрактные и спорные темы</li>"
                "<li>Использовать идиоматические выражения, разговорную речь и нюансы повседневного и формального языка</li>"
                "<li>Критически анализировать аспекты бразильской истории, политики, литературы и искусства</li>"
                "</ul>"
            ),
        },
    },
}


# Módulos/aulas de PLE vêm do LMS (Course Chapter/Course Lesson) sempre em
# pt-BR -- não existe campo de idioma lá. Este dict mapeia o título EXATO
# em pt-BR (criado por scripts/migrations/oneshot/create_ple_courses.py,
# fonte da verdade) pra tradução, aplicado em www/curso.py depois que
# get_course_details() já trouxe a grade ao vivo do banco. Título sem
# correspondência aqui (drift, edição manual) fica em português — nunca
# desaparece.
#
# Cobertura: en/es/fr/de completos pros 3 cursos PLE (9 módulos + 51 aulas
# cada). ru ainda não tem essa tradução -- ver relatório da missão PLE.
PLE_CURRICULUM_TRANSLATIONS = {
    "portugues-para-estrangeiros-basico": {
        "en": {
            "chapters": {
                "Módulo 1 — Primeiros Contatos e Informações Pessoais": "Module 1 — First Contacts and Personal Information",
                "Módulo 2 — O Dia a Dia e o Ambiente": "Module 2 — Daily Life and Surroundings",
                "Módulo 3 — Interações e Cultura Brasileira": "Module 3 — Interactions and Brazilian Culture",
            },
            "lessons": {
                "Introdução à Língua Portuguesa — Alfabeto e pronúncia do português brasileiro": "Introduction to the Portuguese Language — Alphabet and pronunciation of Brazilian Portuguese",
                "Saudações e despedidas — Bom dia, Boa tarde, Olá, Tchau": "Greetings and farewells — Good morning, Good afternoon, Hello, Bye",
                "Apresentação pessoal — Meu nome é..., Eu sou de...": "Personal introduction — My name is..., I am from...",
                "Oi! Tudo bem? — Cumprimentos e troca de informações pessoais": "Hi! How are you? — Greetings and exchanging personal information",
                "Artigos, presente do indicativo e vocabulário de países e profissões": "Articles, present indicative and vocabulary for countries and professions",
                "Que lugar maravilhoso! — Localizar pessoas e objetos": "What a Wonderful Place! — Locating people and objects",
                "Verbos ser e estar, preposições de lugar e meios de transporte": "Verbs ser and estar, prepositions of place and means of transport",
                "Seu primo é um gato! — Família e amigos": "Your Cousin Is Really Cute! — Family and friends",
                "Descrever pessoas — características físicas e de personalidade": "Describing people — physical and personality traits",
                "Gênero e número dos adjetivos, possessivos e vocabulário de família": "Gender and number of adjectives, possessives and family vocabulary",
                "Todo Santo Dia — Rotinas diárias e horários": "Every Single Day — Daily routines and schedules",
                "Advérbios de frequência e verbos reflexivos": "Adverbs of frequency and reflexive verbs",
                "Que comidinha boa! — Pedir comida e fazer compras de alimentos": "What Delicious Food! — Ordering food and grocery shopping",
                "Imperativo básico e vocabulário de comidas, bebidas e restaurante": "Basic imperative and vocabulary for food, drinks and restaurants",
                "O verão está chegando! — Clima, estações do ano e convites": "Summer Is Coming! — Weather, seasons and invitations",
                "Estar + gerúndio e presente do indicativo com verbos irregulares": "Estar + gerund and present indicative with irregular verbs",
                "Boas compras! — Fazer compras, pechinchar e falar de dinheiro": "Happy Shopping! — Shopping, bargaining and talking about money",
                "Comparativos, demonstrativos e vocabulário de roupas e lojas": "Comparatives, demonstratives and vocabulary for clothes and shops",
                "Vire à esquerda e siga em frente! — Dar e pedir direções": "Turn Left and Go Straight Ahead! — Giving and asking for directions",
                "Imperativo avançado, preposições de movimento e pontos de referência": "Advanced imperative, prepositions of movement and landmarks",
            },
        },
        "es": {
            "chapters": {
                "Módulo 1 — Primeiros Contatos e Informações Pessoais": "Módulo 1 — Primeros Contactos e Información Personal",
                "Módulo 2 — O Dia a Dia e o Ambiente": "Módulo 2 — La Vida Cotidiana y el Entorno",
                "Módulo 3 — Interações e Cultura Brasileira": "Módulo 3 — Interacciones y Cultura Brasileña",
            },
            "lessons": {
                "Introdução à Língua Portuguesa — Alfabeto e pronúncia do português brasileiro": "Introducción a la Lengua Portuguesa — Alfabeto y pronunciación del portugués brasileño",
                "Saudações e despedidas — Bom dia, Boa tarde, Olá, Tchau": "Saludos y despedidas — Buenos días, Buenas tardes, Hola, Chau",
                "Apresentação pessoal — Meu nome é..., Eu sou de...": "Presentación personal — Me llamo..., Soy de...",
                "Oi! Tudo bem? — Cumprimentos e troca de informações pessoais": "¡Hola! ¿Todo bien? — Saludos e intercambio de información personal",
                "Artigos, presente do indicativo e vocabulário de países e profissões": "Artículos, presente de indicativo y vocabulario de países y profesiones",
                "Que lugar maravilhoso! — Localizar pessoas e objetos": "¡Qué lugar maravilloso! — Ubicar personas y objetos",
                "Verbos ser e estar, preposições de lugar e meios de transporte": "Verbos ser y estar, preposiciones de lugar y medios de transporte",
                "Seu primo é um gato! — Família e amigos": "¡Tu primo está muy guapo! — Familia y amigos",
                "Descrever pessoas — características físicas e de personalidade": "Describir personas — características físicas y de personalidad",
                "Gênero e número dos adjetivos, possessivos e vocabulário de família": "Género y número de los adjetivos, posesivos y vocabulario de familia",
                "Todo Santo Dia — Rotinas diárias e horários": "Todos los Santos Días — Rutinas diarias y horarios",
                "Advérbios de frequência e verbos reflexivos": "Adverbios de frecuencia y verbos reflexivos",
                "Que comidinha boa! — Pedir comida e fazer compras de alimentos": "¡Qué comidita rica! — Pedir comida y hacer compras de alimentos",
                "Imperativo básico e vocabulário de comidas, bebidas e restaurante": "Imperativo básico y vocabulario de comidas, bebidas y restaurante",
                "O verão está chegando! — Clima, estações do ano e convites": "¡El verano está llegando! — Clima, estaciones del año e invitaciones",
                "Estar + gerúndio e presente do indicativo com verbos irregulares": "Estar + gerundio y presente de indicativo con verbos irregulares",
                "Boas compras! — Fazer compras, pechinchar e falar de dinheiro": "¡Buenas compras! — Ir de compras, regatear y hablar de dinero",
                "Comparativos, demonstrativos e vocabulário de roupas e lojas": "Comparativos, demostrativos y vocabulario de ropa y tiendas",
                "Vire à esquerda e siga em frente! — Dar e pedir direções": "¡Gire a la izquierda y siga adelante! — Dar y pedir direcciones",
                "Imperativo avançado, preposições de movimento e pontos de referência": "Imperativo avanzado, preposiciones de movimiento y puntos de referencia",
            },
        },
        "fr": {
            "chapters": {
                "Módulo 1 — Primeiros Contatos e Informações Pessoais": "Module 1 — Premiers contacts et informations personnelles",
                "Módulo 2 — O Dia a Dia e o Ambiente": "Module 2 — Le quotidien et l'environnement",
                "Módulo 3 — Interações e Cultura Brasileira": "Module 3 — Interactions et culture brésilienne",
            },
            "lessons": {
                "Introdução à Língua Portuguesa — Alfabeto e pronúncia do português brasileiro": "Introduction à la langue portugaise — Alphabet et prononciation du portugais brésilien",
                "Saudações e despedidas — Bom dia, Boa tarde, Olá, Tchau": "Salutations et adieux — Bonjour, Bon après-midi, Salut, Au revoir",
                "Apresentação pessoal — Meu nome é..., Eu sou de...": "Présentation personnelle — Je m'appelle..., Je viens de...",
                "Oi! Tudo bem? — Cumprimentos e troca de informações pessoais": "Salut ! Ça va ? — Salutations et échange d'informations personnelles",
                "Artigos, presente do indicativo e vocabulário de países e profissões": "Articles, présent de l'indicatif et vocabulaire des pays et professions",
                "Que lugar maravilhoso! — Localizar pessoas e objetos": "Quel endroit merveilleux ! — Localiser des personnes et des objets",
                "Verbos ser e estar, preposições de lugar e meios de transporte": "Verbes ser et estar, prépositions de lieu et moyens de transport",
                "Seu primo é um gato! — Família e amigos": "Ton cousin est trop mignon ! — Famille et amis",
                "Descrever pessoas — características físicas e de personalidade": "Décrire des personnes — caractéristiques physiques et de personnalité",
                "Gênero e número dos adjetivos, possessivos e vocabulário de família": "Genre et nombre des adjectifs, possessifs et vocabulaire de la famille",
                "Todo Santo Dia — Rotinas diárias e horários": "Tous les jours que Dieu fait — Routines quotidiennes et horaires",
                "Advérbios de frequência e verbos reflexivos": "Adverbes de fréquence et verbes réfléchis",
                "Que comidinha boa! — Pedir comida e fazer compras de alimentos": "Quel bon petit plat ! — Commander à manger et faire les courses",
                "Imperativo básico e vocabulário de comidas, bebidas e restaurante": "Impératif de base et vocabulaire des aliments, boissons et restaurant",
                "O verão está chegando! — Clima, estações do ano e convites": "L'été arrive ! — Météo, saisons et invitations",
                "Estar + gerúndio e presente do indicativo com verbos irregulares": "Estar + gérondif et présent de l'indicatif avec verbes irréguliers",
                "Boas compras! — Fazer compras, pechinchar e falar de dinheiro": "Bonnes affaires ! — Faire les courses, négocier et parler d'argent",
                "Comparativos, demonstrativos e vocabulário de roupas e lojas": "Comparatifs, démonstratifs et vocabulaire des vêtements et boutiques",
                "Vire à esquerda e siga em frente! — Dar e pedir direções": "Tournez à gauche et continuez tout droit ! — Donner et demander son chemin",
                "Imperativo avançado, preposições de movimento e pontos de referência": "Impératif avancé, prépositions de mouvement et points de repère",
            },
        },
        "de": {
            "chapters": {
                "Módulo 1 — Primeiros Contatos e Informações Pessoais": "Modul 1 — Erste Kontakte und persönliche Angaben",
                "Módulo 2 — O Dia a Dia e o Ambiente": "Modul 2 — Alltag und Umfeld",
                "Módulo 3 — Interações e Cultura Brasileira": "Modul 3 — Interaktionen und brasilianische Kultur",
            },
            "lessons": {
                "Introdução à Língua Portuguesa — Alfabeto e pronúncia do português brasileiro": "Einführung in die portugiesische Sprache — Alphabet und Aussprache des brasilianischen Portugiesisch",
                "Saudações e despedidas — Bom dia, Boa tarde, Olá, Tchau": "Begrüßungen und Verabschiedungen — Guten Morgen, Guten Tag, Hallo, Tschüss",
                "Apresentação pessoal — Meu nome é..., Eu sou de...": "Persönliche Vorstellung — Ich heiße..., Ich komme aus...",
                "Oi! Tudo bem? — Cumprimentos e troca de informações pessoais": "Hallo! Wie geht's? — Begrüßungen und Austausch persönlicher Informationen",
                "Artigos, presente do indicativo e vocabulário de países e profissões": "Artikel, Präsens Indikativ und Wortschatz zu Ländern und Berufen",
                "Que lugar maravilhoso! — Localizar pessoas e objetos": "Was für ein wunderbarer Ort! — Personen und Gegenstände lokalisieren",
                "Verbos ser e estar, preposições de lugar e meios de transporte": "Verben ser und estar, Ortspräpositionen und Verkehrsmittel",
                "Seu primo é um gato! — Família e amigos": "Dein Cousin sieht gut aus! — Familie und Freunde",
                "Descrever pessoas — características físicas e de personalidade": "Personen beschreiben — körperliche Merkmale und Persönlichkeit",
                "Gênero e número dos adjetivos, possessivos e vocabulário de família": "Geschlecht und Numerus der Adjektive, Possessivpronomen und Familienwortschatz",
                "Todo Santo Dia — Rotinas diárias e horários": "Jeden lieben Tag — Tagesabläufe und Uhrzeiten",
                "Advérbios de frequência e verbos reflexivos": "Häufigkeitsadverbien und reflexive Verben",
                "Que comidinha boa! — Pedir comida e fazer compras de alimentos": "Was für ein leckeres Essen! — Essen bestellen und Lebensmittel einkaufen",
                "Imperativo básico e vocabulário de comidas, bebidas e restaurante": "Einfacher Imperativ und Wortschatz zu Speisen, Getränken und Restaurant",
                "O verão está chegando! — Clima, estações do ano e convites": "Der Sommer kommt! — Wetter, Jahreszeiten und Einladungen",
                "Estar + gerúndio e presente do indicativo com verbos irregulares": "Estar + Gerundium und Präsens Indikativ mit unregelmäßigen Verben",
                "Boas compras! — Fazer compras, pechinchar e falar de dinheiro": "Viel Spaß beim Einkaufen! — Einkaufen, feilschen und über Geld sprechen",
                "Comparativos, demonstrativos e vocabulário de roupas e lojas": "Komparative, Demonstrativpronomen und Wortschatz zu Kleidung und Geschäften",
                "Vire à esquerda e siga em frente! — Dar e pedir direções": "Biegen Sie links ab und gehen Sie geradeaus! — Wegbeschreibungen geben und erfragen",
                "Imperativo avançado, preposições de movimento e pontos de referência": "Fortgeschrittener Imperativ, Bewegungspräpositionen und Orientierungspunkte",
            },
        },
    },
    "portugues-para-estrangeiros-intermediario": {
        "en": {
            "chapters": {
                "Módulo 1 — Narrativa e Experiências Passadas": "Module 1 — Narrative and Past Experiences",
                "Módulo 2 — Saúde, Trabalho e Vida Social": "Module 2 — Health, Work and Social Life",
                "Módulo 3 — Cultura, Opinião e Variação Linguística": "Module 3 — Culture, Opinion and Language Variation",
            },
            "lessons": {
                "Enfim, Férias! — Planos de viagem, sugestões e concordâncias": "Finally, Vacation! — Travel plans, suggestions and agreement",
                "Pretérito perfeito simples e pronomes oblíquos átonos (objeto direto)": "Simple past (preterite) and unstressed object pronouns (direct object)",
                "Quanto é o aluguel? — Moradia, comparações e preferências": "How Much Is the Rent? — Housing, comparisons and preferences",
                "Pretérito mais-que-perfeito e pronomes oblíquos (objeto indireto)": "Pluperfect and object pronouns (indirect object)",
                "É hora da malhação! — Esportes e atividades físicas": "Time to Work Out! — Sports and physical activities",
                "Pretérito imperfeito do indicativo e pronomes reflexivos": "Imperfect indicative and reflexive pronouns",
                "A que horas é a consulta? — Saúde, bem-estar e consultas médicas": "What Time Is the Appointment? — Health, wellness and doctor visits",
                "Verbo doer, pronomes oblíquos em combinações e particípios passados": "The verb doer (to hurt/ache), combined object pronouns and past participles",
                "Hoje é dia de trabalho! — Profissões e entrevista de emprego": "Today's a Work Day! — Professions and job interviews",
                "Discurso direto e indireto, pronomes relativos invariáveis": "Direct and indirect speech, invariable relative pronouns",
                "Gostarias de conhecer outros países lusófonos? — Lusofonia e diversidade cultural": "Would You Like to Know Other Portuguese-Speaking Countries? — The Lusophone world and cultural diversity",
                "Futuro do pretérito e vocabulário de países lusófonos e expressões regionais": "Conditional tense and vocabulary of Portuguese-speaking countries and regional expressions",
                "Expressão de opiniões e argumentação em português": "Expressing opinions and argumentation in Portuguese",
                "Leitura e discussão de notícias e artigos de interesse geral": "Reading and discussing news and general-interest articles",
                "Produção de textos narrativos e descritivos": "Writing narrative and descriptive texts",
                "Cultura popular brasileira — música, festas e culinária": "Brazilian popular culture — music, festivals and cuisine",
            },
        },
        "es": {
            "chapters": {
                "Módulo 1 — Narrativa e Experiências Passadas": "Módulo 1 — Narrativa y Experiencias Pasadas",
                "Módulo 2 — Saúde, Trabalho e Vida Social": "Módulo 2 — Salud, Trabajo y Vida Social",
                "Módulo 3 — Cultura, Opinião e Variação Linguística": "Módulo 3 — Cultura, Opinión y Variación Lingüística",
            },
            "lessons": {
                "Enfim, Férias! — Planos de viagem, sugestões e concordâncias": "¡Por Fin, Vacaciones! — Planes de viaje, sugerencias y acuerdos",
                "Pretérito perfeito simples e pronomes oblíquos átonos (objeto direto)": "Pretérito perfecto simple y pronombres átonos (objeto directo)",
                "Quanto é o aluguel? — Moradia, comparações e preferências": "¿Cuánto es el alquiler? — Vivienda, comparaciones y preferencias",
                "Pretérito mais-que-perfeito e pronomes oblíquos (objeto indireto)": "Pretérito pluscuamperfecto y pronombres átonos (objeto indirecto)",
                "É hora da malhação! — Esportes e atividades físicas": "¡Es hora de hacer ejercicio! — Deportes y actividades físicas",
                "Pretérito imperfeito do indicativo e pronomes reflexivos": "Pretérito imperfecto de indicativo y pronombres reflexivos",
                "A que horas é a consulta? — Saúde, bem-estar e consultas médicas": "¿A qué hora es la cita? — Salud, bienestar y consultas médicas",
                "Verbo doer, pronomes oblíquos em combinações e particípios passados": "El verbo doer (doler), combinaciones de pronombres átonos y participios pasados",
                "Hoje é dia de trabalho! — Profissões e entrevista de emprego": "¡Hoy es día de trabajo! — Profesiones y entrevista de trabajo",
                "Discurso direto e indireto, pronomes relativos invariáveis": "Discurso directo e indirecto, pronombres relativos invariables",
                "Gostarias de conhecer outros países lusófonos? — Lusofonia e diversidade cultural": "¿Te gustaría conocer otros países lusófonos? — Lusofonía y diversidad cultural",
                "Futuro do pretérito e vocabulário de países lusófonos e expressões regionais": "Condicional simple y vocabulario de países lusófonos y expresiones regionales",
                "Expressão de opiniões e argumentação em português": "Expresión de opiniones y argumentación en portugués",
                "Leitura e discussão de notícias e artigos de interesse geral": "Lectura y discusión de noticias y artículos de interés general",
                "Produção de textos narrativos e descritivos": "Producción de textos narrativos y descriptivos",
                "Cultura popular brasileira — música, festas e culinária": "Cultura popular brasileña — música, fiestas y gastronomía",
            },
        },
        "fr": {
            "chapters": {
                "Módulo 1 — Narrativa e Experiências Passadas": "Module 1 — Récit et expériences passées",
                "Módulo 2 — Saúde, Trabalho e Vida Social": "Module 2 — Santé, travail et vie sociale",
                "Módulo 3 — Cultura, Opinião e Variação Linguística": "Module 3 — Culture, opinion et variation linguistique",
            },
            "lessons": {
                "Enfim, Férias! — Planos de viagem, sugestões e concordâncias": "Enfin les vacances ! — Projets de voyage, suggestions et accords",
                "Pretérito perfeito simples e pronomes oblíquos átonos (objeto direto)": "Passé simple et pronoms compléments atones (objet direct)",
                "Quanto é o aluguel? — Moradia, comparações e preferências": "Combien coûte le loyer ? — Logement, comparaisons et préférences",
                "Pretérito mais-que-perfeito e pronomes oblíquos (objeto indireto)": "Plus-que-parfait et pronoms compléments (objet indirect)",
                "É hora da malhação! — Esportes e atividades físicas": "C'est l'heure du sport ! — Sports et activités physiques",
                "Pretérito imperfeito do indicativo e pronomes reflexivos": "Imparfait de l'indicatif et pronoms réfléchis",
                "A que horas é a consulta? — Saúde, bem-estar e consultas médicas": "À quelle heure est le rendez-vous ? — Santé, bien-être et consultations médicales",
                "Verbo doer, pronomes oblíquos em combinações e particípios passados": "Le verbe doer (faire mal), combinaisons de pronoms compléments et participes passés",
                "Hoje é dia de trabalho! — Profissões e entrevista de emprego": "Aujourd'hui, c'est un jour de travail ! — Professions et entretien d'embauche",
                "Discurso direto e indireto, pronomes relativos invariáveis": "Discours direct et indirect, pronoms relatifs invariables",
                "Gostarias de conhecer outros países lusófonos? — Lusofonia e diversidade cultural": "Aimerais-tu découvrir d'autres pays lusophones ? — La lusophonie et la diversité culturelle",
                "Futuro do pretérito e vocabulário de países lusófonos e expressões regionais": "Conditionnel présent et vocabulaire des pays lusophones et expressions régionales",
                "Expressão de opiniões e argumentação em português": "Exprimer des opinions et argumenter en portugais",
                "Leitura e discussão de notícias e artigos de interesse geral": "Lecture et discussion d'actualités et d'articles d'intérêt général",
                "Produção de textos narrativos e descritivos": "Production de textes narratifs et descriptifs",
                "Cultura popular brasileira — música, festas e culinária": "Culture populaire brésilienne — musique, fêtes et gastronomie",
            },
        },
        "de": {
            "chapters": {
                "Módulo 1 — Narrativa e Experiências Passadas": "Modul 1 — Erzählung und vergangene Erlebnisse",
                "Módulo 2 — Saúde, Trabalho e Vida Social": "Modul 2 — Gesundheit, Arbeit und soziales Leben",
                "Módulo 3 — Cultura, Opinião e Variação Linguística": "Modul 3 — Kultur, Meinung und Sprachvariation",
            },
            "lessons": {
                "Enfim, Férias! — Planos de viagem, sugestões e concordâncias": "Endlich Urlaub! — Reisepläne, Vorschläge und Zustimmung",
                "Pretérito perfeito simples e pronomes oblíquos átonos (objeto direto)": "Einfache Vergangenheit (Präteritum) und unbetonte Objektpronomen (direktes Objekt)",
                "Quanto é o aluguel? — Moradia, comparações e preferências": "Wie hoch ist die Miete? — Wohnen, Vergleiche und Vorlieben",
                "Pretérito mais-que-perfeito e pronomes oblíquos (objeto indireto)": "Plusquamperfekt und Objektpronomen (indirektes Objekt)",
                "É hora da malhação! — Esportes e atividades físicas": "Zeit fürs Training! — Sport und körperliche Aktivitäten",
                "Pretérito imperfeito do indicativo e pronomes reflexivos": "Imperfekt Indikativ und Reflexivpronomen",
                "A que horas é a consulta? — Saúde, bem-estar e consultas médicas": "Um wie viel Uhr ist der Termin? — Gesundheit, Wohlbefinden und Arztbesuche",
                "Verbo doer, pronomes oblíquos em combinações e particípios passados": "Das Verb doer (schmerzen), kombinierte Objektpronomen und Partizip Perfekt",
                "Hoje é dia de trabalho! — Profissões e entrevista de emprego": "Heute ist Arbeitstag! — Berufe und Vorstellungsgespräch",
                "Discurso direto e indireto, pronomes relativos invariáveis": "Direkte und indirekte Rede, unveränderliche Relativpronomen",
                "Gostarias de conhecer outros países lusófonos? — Lusofonia e diversidade cultural": "Möchtest du andere portugiesischsprachige Länder kennenlernen? — Die lusophone Welt und kulturelle Vielfalt",
                "Futuro do pretérito e vocabulário de países lusófonos e expressões regionais": "Konditional und Wortschatz zu portugiesischsprachigen Ländern und regionalen Ausdrücken",
                "Expressão de opiniões e argumentação em português": "Meinungen äußern und argumentieren auf Portugiesisch",
                "Leitura e discussão de notícias e artigos de interesse geral": "Lesen und Diskutieren von Nachrichten und allgemeinen Artikeln",
                "Produção de textos narrativos e descritivos": "Verfassen von erzählenden und beschreibenden Texten",
                "Cultura popular brasileira — música, festas e culinária": "Brasilianische Populärkultur — Musik, Feste und Küche",
            },
        },
    },
    "portugues-para-estrangeiros-avancado": {
        "en": {
            "chapters": {
                "Módulo 1 — Opinião, Hipótese e Argumentação": "Module 1 — Opinion, Hypothesis and Argumentation",
                "Módulo 2 — Cultura, Sociedade e Mídia": "Module 2 — Culture, Society and Media",
                "Módulo 3 — Contextos Profissionais e Acadêmicos": "Module 3 — Professional and Academic Contexts",
            },
            "lessons": {
                "Expressando opiniões e dúvidas — debates sobre meio ambiente, tecnologia e sociedade": "Expressing opinions and doubts — debates on environment, technology and society",
                "Presente do subjuntivo — expressão de desejo, dúvida e emoção": "Present subjunctive — expressing wish, doubt and emotion",
                "Hipóteses e condições — cenários hipotéticos e planejamento futuro": "Hypotheses and conditions — hypothetical scenarios and future planning",
                "Pretérito imperfeito e futuro do subjuntivo — orações condicionais (Se...)": "Imperfect subjunctive and future subjunctive — conditional clauses (If...)",
                "A mídia e a informação — análise de notícias e reportagens brasileiras": "Media and information — analyzing Brazilian news and reports",
                "Voz passiva analítica e sintética, discurso indireto avançado": "Analytic and synthetic passive voice, advanced indirect speech",
                "Arte e literatura brasileira — contos, crônicas e poemas": "Brazilian art and literature — short stories, chronicles and poems",
                "Movimentos culturais brasileiros — Bossa Nova, Tropicália e outros": "Brazilian cultural movements — Bossa Nova, Tropicália and others",
                "Revisão e aprofundamento dos tempos do passado na narrativa literária": "Review and deep dive into past tenses in literary narrative",
                "O mundo do trabalho e negócios — reuniões, apresentações e negociações": "The world of work and business — meetings, presentations and negotiations",
                "Elaboração de currículos, e-mails formais e relatórios em português": "Writing résumés, formal e-mails and reports in Portuguese",
                "Pronomes relativos complexos (cujo, o qual) e regência verbal avançada": "Complex relative pronouns (whose, which) and advanced verb government",
                "Variação linguística e identidade — sotaques e dialetos do Brasil": "Language variation and identity — accents and dialects of Brazil",
                "Linguagem da internet e das redes sociais em português": "Internet and social media language in Portuguese",
                "Colocação pronominal em contextos formais e informais": "Pronoun placement in formal and informal contexts",
            },
        },
        "es": {
            "chapters": {
                "Módulo 1 — Opinião, Hipótese e Argumentação": "Módulo 1 — Opinión, Hipótesis y Argumentación",
                "Módulo 2 — Cultura, Sociedade e Mídia": "Módulo 2 — Cultura, Sociedad y Medios",
                "Módulo 3 — Contextos Profissionais e Acadêmicos": "Módulo 3 — Contextos Profesionales y Académicos",
            },
            "lessons": {
                "Expressando opiniões e dúvidas — debates sobre meio ambiente, tecnologia e sociedade": "Expresando opiniones y dudas — debates sobre medio ambiente, tecnología y sociedad",
                "Presente do subjuntivo — expressão de desejo, dúvida e emoção": "Presente de subjuntivo — expresión de deseo, duda y emoción",
                "Hipóteses e condições — cenários hipotéticos e planejamento futuro": "Hipótesis y condiciones — escenarios hipotéticos y planificación futura",
                "Pretérito imperfeito e futuro do subjuntivo — orações condicionais (Se...)": "Pretérito imperfecto y futuro de subjuntivo — oraciones condicionales (Si...)",
                "A mídia e a informação — análise de notícias e reportagens brasileiras": "Los medios y la información — análisis de noticias y reportajes brasileños",
                "Voz passiva analítica e sintética, discurso indireto avançado": "Voz pasiva analítica y sintética, discurso indirecto avanzado",
                "Arte e literatura brasileira — contos, crônicas e poemas": "Arte y literatura brasileña — cuentos, crónicas y poemas",
                "Movimentos culturais brasileiros — Bossa Nova, Tropicália e outros": "Movimientos culturales brasileños — Bossa Nova, Tropicália y otros",
                "Revisão e aprofundamento dos tempos do passado na narrativa literária": "Repaso y profundización de los tiempos del pasado en la narrativa literaria",
                "O mundo do trabalho e negócios — reuniões, apresentações e negociações": "El mundo del trabajo y los negocios — reuniones, presentaciones y negociaciones",
                "Elaboração de currículos, e-mails formais e relatórios em português": "Elaboración de currículums, correos formales e informes en portugués",
                "Pronomes relativos complexos (cujo, o qual) e regência verbal avançada": "Pronombres relativos complejos (cuyo, el cual) y régimen verbal avanzado",
                "Variação linguística e identidade — sotaques e dialetos do Brasil": "Variación lingüística e identidad — acentos y dialectos de Brasil",
                "Linguagem da internet e das redes sociais em português": "Lenguaje de internet y redes sociales en portugués",
                "Colocação pronominal em contextos formais e informais": "Colocación pronominal en contextos formales e informales",
            },
        },
        "fr": {
            "chapters": {
                "Módulo 1 — Opinião, Hipótese e Argumentação": "Module 1 — Opinion, hypothèse et argumentation",
                "Módulo 2 — Cultura, Sociedade e Mídia": "Module 2 — Culture, société et médias",
                "Módulo 3 — Contextos Profissionais e Acadêmicos": "Module 3 — Contextes professionnels et académiques",
            },
            "lessons": {
                "Expressando opiniões e dúvidas — debates sobre meio ambiente, tecnologia e sociedade": "Exprimer des opinions et des doutes — débats sur l'environnement, la technologie et la société",
                "Presente do subjuntivo — expressão de desejo, dúvida e emoção": "Présent du subjonctif — exprimer le souhait, le doute et l'émotion",
                "Hipóteses e condições — cenários hipotéticos e planejamento futuro": "Hypothèses et conditions — scénarios hypothétiques et planification future",
                "Pretérito imperfeito e futuro do subjuntivo — orações condicionais (Se...)": "Imparfait du subjonctif et futur du subjonctif — propositions conditionnelles (Si...)",
                "A mídia e a informação — análise de notícias e reportagens brasileiras": "Les médias et l'information — analyse d'actualités et de reportages brésiliens",
                "Voz passiva analítica e sintética, discurso indireto avançado": "Voix passive analytique et synthétique, discours indirect avancé",
                "Arte e literatura brasileira — contos, crônicas e poemas": "Art et littérature brésiliens — nouvelles, chroniques et poèmes",
                "Movimentos culturais brasileiros — Bossa Nova, Tropicália e outros": "Mouvements culturels brésiliens — Bossa Nova, Tropicália et autres",
                "Revisão e aprofundamento dos tempos do passado na narrativa literária": "Révision et approfondissement des temps du passé dans le récit littéraire",
                "O mundo do trabalho e negócios — reuniões, apresentações e negociações": "Le monde du travail et des affaires — réunions, présentations et négociations",
                "Elaboração de currículos, e-mails formais e relatórios em português": "Rédaction de CV, e-mails formels et rapports en portugais",
                "Pronomes relativos complexos (cujo, o qual) e regência verbal avançada": "Pronoms relatifs complexes (dont, lequel) et régime verbal avancé",
                "Variação linguística e identidade — sotaques e dialetos do Brasil": "Variation linguistique et identité — accents et dialectes du Brésil",
                "Linguagem da internet e das redes sociais em português": "Le langage d'internet et des réseaux sociaux en portugais",
                "Colocação pronominal em contextos formais e informais": "Placement des pronoms dans des contextes formels et informels",
            },
        },
        "de": {
            "chapters": {
                "Módulo 1 — Opinião, Hipótese e Argumentação": "Modul 1 — Meinung, Hypothese und Argumentation",
                "Módulo 2 — Cultura, Sociedade e Mídia": "Modul 2 — Kultur, Gesellschaft und Medien",
                "Módulo 3 — Contextos Profissionais e Acadêmicos": "Modul 3 — Berufliche und akademische Kontexte",
            },
            "lessons": {
                "Expressando opiniões e dúvidas — debates sobre meio ambiente, tecnologia e sociedade": "Meinungen und Zweifel ausdrücken — Debatten über Umwelt, Technologie und Gesellschaft",
                "Presente do subjuntivo — expressão de desejo, dúvida e emoção": "Präsens Subjunktiv — Wunsch, Zweifel und Emotion ausdrücken",
                "Hipóteses e condições — cenários hipotéticos e planejamento futuro": "Hypothesen und Bedingungen — hypothetische Szenarien und Zukunftsplanung",
                "Pretérito imperfeito e futuro do subjuntivo — orações condicionais (Se...)": "Imperfekt Subjunktiv und Futur Subjunktiv — Bedingungssätze (Wenn...)",
                "A mídia e a informação — análise de notícias e reportagens brasileiras": "Medien und Information — Analyse brasilianischer Nachrichten und Reportagen",
                "Voz passiva analítica e sintética, discurso indireto avançado": "Analytisches und synthetisches Passiv, fortgeschrittene indirekte Rede",
                "Arte e literatura brasileira — contos, crônicas e poemas": "Brasilianische Kunst und Literatur — Kurzgeschichten, Chroniken und Gedichte",
                "Movimentos culturais brasileiros — Bossa Nova, Tropicália e outros": "Brasilianische Kulturbewegungen — Bossa Nova, Tropicália und andere",
                "Revisão e aprofundamento dos tempos do passado na narrativa literária": "Wiederholung und Vertiefung der Vergangenheitsformen in der literarischen Erzählung",
                "O mundo do trabalho e negócios — reuniões, apresentações e negociações": "Die Arbeits- und Geschäftswelt — Meetings, Präsentationen und Verhandlungen",
                "Elaboração de currículos, e-mails formais e relatórios em português": "Verfassen von Lebensläufen, formellen E-Mails und Berichten auf Portugiesisch",
                "Pronomes relativos complexos (cujo, o qual) e regência verbal avançada": "Komplexe Relativpronomen (dessen, welcher) und fortgeschrittene Verbrektion",
                "Variação linguística e identidade — sotaques e dialetos do Brasil": "Sprachvariation und Identität — Akzente und Dialekte Brasiliens",
                "Linguagem da internet e das redes sociais em português": "Internet- und Social-Media-Sprache auf Portugiesisch",
                "Colocação pronominal em contextos formais e informais": "Pronomenstellung in formellen und informellen Kontexten",
            },
        },
    },
}

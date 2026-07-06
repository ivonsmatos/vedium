"""Traduções de cursos individuais (/en|es|fr|de/curso/<slug>).

Só os cursos de Iorubá e PLE têm entrada aqui — o público desses dois
clusters inclui gente que não fala português (diáspora, expats). O cluster
de Inglês não precisa: quem busca aprender inglês na Vedium já fala PT.

Preço, vagas, avaliações, matrícula etc. continuam vindo ao vivo do banco
via curso.py — aqui só sobrepomos os campos de texto (title/short_introduction/
description). Sem Custom Field nem migração: é só um dict em código.

Estrutura: COURSE_TRANSLATIONS[slug][lang] = {title, short_introduction, description}.
"""

COURSE_TRANSLATIONS = {
    "iorub-b-sico": {
        "en": {
            "title": "Yoruba — Basic",
            "short_introduction": "Basic Level | Greetings, alphabet, tones, pronouns, numerals and everyday dialogues across 3 modules and 9 progressive lessons.",
            "description": (
                "<p>The <strong>Yoruba Basic</strong> course introduces the fundamentals of the "
                "Yoruba language and culture, preparing you to handle everyday situations and "
                "build a solid foundation for continued learning.</p>"
                "<p>Based on <em>Beginner's Yoruba</em> by Kayode J. Fakinlede (2005), you will master:</p>"
                "<ul>"
                "<li>Greetings, farewells and courtesy expressions</li>"
                "<li>Personal introductions — name and origin</li>"
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
            "title": "Yoruba — Básico",
            "short_introduction": "Nivel Básico | Saludos, alfabeto, tonos, pronombres, numerales y diálogos cotidianos en 3 módulos y 9 lecciones progresivas.",
            "description": (
                "<p>El curso <strong>Yoruba Básico</strong> presenta los fundamentos del idioma y "
                "la cultura yoruba, preparándote para manejar situaciones cotidianas y construir "
                "una base sólida para seguir aprendiendo.</p>"
                "<p>Basado en <em>Beginner's Yoruba</em> de Kayode J. Fakinlede (2005), dominarás:</p>"
                "<ul>"
                "<li>Saludos, despedidas y expresiones de cortesía</li>"
                "<li>Presentaciones personales — nombre y origen</li>"
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
            "title": "Yoruba — Débutant",
            "short_introduction": "Niveau Débutant | Salutations, alphabet, tons, pronoms, chiffres et dialogues du quotidien en 3 modules et 9 leçons progressives.",
            "description": (
                "<p>Le cours <strong>Yoruba Débutant</strong> présente les fondamentaux de la langue "
                "et de la culture yoruba, pour vous préparer à gérer des situations du quotidien et "
                "bâtir une base solide pour la suite de votre apprentissage.</p>"
                "<p>Basé sur <em>Beginner's Yoruba</em> de Kayode J. Fakinlede (2005), vous maîtriserez :</p>"
                "<ul>"
                "<li>Salutations, adieux et expressions de politesse</li>"
                "<li>Présentations personnelles — nom et origine</li>"
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
            "title": "Yoruba — Grundstufe",
            "short_introduction": "Grundstufe | Begrüßungen, Alphabet, Töne, Pronomen, Zahlen und Alltagsdialoge in 3 Modulen und 9 aufeinander aufbauenden Lektionen.",
            "description": (
                "<p>Der Kurs <strong>Yoruba Grundstufe</strong> vermittelt die Grundlagen der "
                "Yoruba-Sprache und -Kultur und bereitet Sie darauf vor, Alltagssituationen zu "
                "meistern und eine solide Basis für das weitere Lernen aufzubauen.</p>"
                "<p>Basierend auf <em>Beginner's Yoruba</em> von Kayode J. Fakinlede (2005), beherrschen Sie:</p>"
                "<ul>"
                "<li>Begrüßungen, Verabschiedungen und Höflichkeitsfloskeln</li>"
                "<li>Persönliche Vorstellung — Name und Herkunft</li>"
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
    },
    "iorub-intermedi-rio": {
        "en": {
            "title": "Yoruba — Intermediate",
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
            "title": "Yoruba — Intermedio",
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
            "title": "Yoruba — Intermédiaire",
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
            "title": "Yoruba — Mittelstufe",
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
    },
    "iorub-avan-ado": {
        "en": {
            "title": "Yoruba — Advanced",
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
            "title": "Yoruba — Avanzado",
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
            "title": "Yoruba — Avancé",
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
            "title": "Yoruba — Fortgeschritten",
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
    },
    "portugues-para-estrangeiros-basico": {
        "en": {
            "title": "Portuguese for Foreigners — Basic Level (PLE)",
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
            "title": "Portugués para Extranjeros — Nivel Básico (PLE)",
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
            "title": "Portugais pour Étrangers — Niveau Débutant (PLE)",
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
            "title": "Portugiesisch für Ausländer — Grundstufe (PLE)",
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
    },
    "portugues-para-estrangeiros-intermediario": {
        "en": {
            "title": "Portuguese for Foreigners — Intermediate Level (PLE)",
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
            "title": "Portugués para Extranjeros — Nivel Intermedio (PLE)",
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
            "title": "Portugais pour Étrangers — Niveau Intermédiaire (PLE)",
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
            "title": "Portugiesisch für Ausländer — Mittelstufe (PLE)",
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
    },
    "portugues-para-estrangeiros-avancado": {
        "en": {
            "title": "Portuguese for Foreigners — Advanced Level (PLE)",
            "short_introduction": "For those who already have fluency and want to refine it. Master the subjunctive, authentic texts and Portuguese in academic and professional contexts.",
            "description": (
                "<p>The <strong>PLE Advanced</strong> course is for those who already have "
                "significant fluency and want to refine their use of the language in complex "
                "academic, professional and cultural contexts. This level covers the subjunctive "
                "mood, analysis of authentic texts and a deeper dive into Brazilian culture and "
                "society.</p>"
                "<p><strong>By the end of the course you will be able to:</strong></p>"
                "<ul>"
                "<li>Understand and produce complex texts — opinion pieces, essays and reports</li>"
                "<li>Master the subjunctive mood in its various forms</li>"
                "<li>Actively take part in debates on abstract and controversial topics</li>"
                "<li>Use idiomatic expressions, slang and nuances of colloquial and formal language</li>"
                "<li>Critically analyze aspects of Brazilian history, politics, literature and the arts</li>"
                "</ul>"
            ),
        },
        "es": {
            "title": "Portugués para Extranjeros — Nivel Avanzado (PLE)",
            "short_introduction": "Para quienes ya tienen fluidez y quieren perfeccionarla. Domina el subjuntivo, textos auténticos y el portugués en contextos académicos y profesionales.",
            "description": (
                "<p>El curso <strong>PLE Avanzado</strong> está dirigido a quienes ya tienen una "
                "fluidez significativa y quieren perfeccionar el uso del idioma en contextos "
                "académicos, profesionales y culturales complejos. Este nivel abarca el modo "
                "subjuntivo, el análisis de textos auténticos y una inmersión más profunda en "
                "la cultura y sociedad brasileñas.</p>"
                "<p><strong>Al finalizar el curso podrás:</strong></p>"
                "<ul>"
                "<li>Comprender y producir textos complejos — artículos de opinión, ensayos e informes</li>"
                "<li>Dominar el modo subjuntivo en sus diversas formas</li>"
                "<li>Participar activamente en debates sobre temas abstractos y controvertidos</li>"
                "<li>Usar expresiones idiomáticas, jerga y matices del lenguaje coloquial y formal</li>"
                "<li>Analizar críticamente aspectos de la historia, política, literatura y artes de Brasil</li>"
                "</ul>"
            ),
        },
        "fr": {
            "title": "Portugais pour Étrangers — Niveau Avancé (PLE)",
            "short_introduction": "Pour ceux qui ont déjà une bonne aisance et souhaitent la perfectionner. Maîtrisez le subjonctif, les textes authentiques et le portugais dans des contextes académiques et professionnels.",
            "description": (
                "<p>Le cours <strong>PLE Avancé</strong> s'adresse à ceux qui ont déjà une "
                "aisance significative et souhaitent perfectionner leur usage de la langue dans "
                "des contextes académiques, professionnels et culturels complexes. Ce niveau "
                "couvre le mode subjonctif, l'analyse de textes authentiques et une immersion "
                "plus approfondie dans la culture et la société brésiliennes.</p>"
                "<p><strong>À la fin du cours, vous serez capable de :</strong></p>"
                "<ul>"
                "<li>Comprendre et produire des textes complexes — articles d'opinion, essais et rapports</li>"
                "<li>Maîtriser le mode subjonctif sous ses différentes formes</li>"
                "<li>Participer activement à des débats sur des sujets abstraits et controversés</li>"
                "<li>Utiliser des expressions idiomatiques, l'argot et les nuances du langage familier et soutenu</li>"
                "<li>Analyser de façon critique des aspects de l'histoire, de la politique, de la littérature et des arts du Brésil</li>"
                "</ul>"
            ),
        },
        "de": {
            "title": "Portugiesisch für Ausländer — Fortgeschrittenenstufe (PLE)",
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
                "<li>Komplexe Texte verstehen und verfassen — Meinungsartikel, Essays und Berichte</li>"
                "<li>Den Konjunktiv in seinen verschiedenen Formen beherrschen</li>"
                "<li>Aktiv an Debatten über abstrakte und kontroverse Themen teilnehmen</li>"
                "<li>Idiomatische Ausdrücke, Umgangssprache und Nuancen der Alltags- und Formalsprache verwenden</li>"
                "<li>Aspekte der brasilianischen Geschichte, Politik, Literatur und Kunst kritisch analysieren</li>"
                "</ul>"
            ),
        },
    },
}

"""Traduções em inglês de cursos individuais (/en/curso/<slug>).

Só os cursos de Iorubá e PLE têm entrada aqui — o público desses dois
clusters inclui gente que não fala português (diáspora, expats). O cluster
de Inglês não precisa: quem busca aprender inglês na Vedium já fala PT.

Preço, vagas, avaliações, matrícula etc. continuam vindo ao vivo do banco
via curso.py — aqui só sobrepomos os campos de texto (title/short_introduction/
description). Sem Custom Field nem migração: é só um dict em código.
"""

COURSE_TRANSLATIONS = {
    "iorub-b-sico": {
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
    "iorub-intermedi-rio": {
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
    "iorub-avan-ado": {
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
    "portugues-para-estrangeiros-basico": {
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
    "portugues-para-estrangeiros-intermediario": {
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
    "portugues-para-estrangeiros-avancado": {
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
}

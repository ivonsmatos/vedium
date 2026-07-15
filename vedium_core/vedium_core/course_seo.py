"""Overrides de SEO on-page para os cursos, por LMS Course.name.

O doctype LMS Course só tem short_introduction/description como campos de
texto (sem meta_description/meta_keywords dedicados) — curso.py normalmente
deriva a <meta name="description"> truncando short_introduction em 155
caracteres. Este dict permite usar um texto de meta description escrito
especificamente para SEO, sem sobrepor o parágrafo de introdução mostrado
na própria página (ver uso em www/curso.py).

meta_keywords não tem tag <meta name="keywords"> renderizada no site (o
Google não usa isso para ranking desde ~2009) — mantido aqui só como
referência interna do time de marketing, conforme o próprio texto-fonte
("use como apoio interno da plataforma"). Não é lido por nenhum template.
"""

COURSE_SEO = {
    "ingl-s-beginner": {
        "meta_description": "Inglês Online ao Vivo A1 para iniciantes. Comece do zero com vocabulário essencial, frases simples, pronúncia e prática oral com professor.",
        "meta_keywords": "aula de inglês ao vivo, curso de inglês online A1, inglês iniciante online, inglês do zero, inglês para iniciantes, curso de inglês com professor, inglês básico",
    },
    "ingl-s-elementary": {
        "meta_description": "Inglês Online ao Vivo A2 para consolidar a base. Pratique presente, passado, futuro, vocabulário cotidiano e conversação com professor.",
        "meta_keywords": "curso de inglês online A2, inglês básico online, aula de inglês ao vivo, inglês com professor, conversação em inglês básico, curso de inglês para adultos",
    },
    "ingl-s-pr-intermedi-rio": {
        "meta_description": "Inglês Online ao Vivo B1 para destravar a comunicação. Pratique conversas do dia a dia, tempos verbais, opiniões e fluência funcional.",
        "meta_keywords": "curso de inglês online B1, inglês pré-intermediário, conversação em inglês, aula de inglês ao vivo, inglês para falar melhor, inglês funcional",
    },
    "ingl-s-intermedi-rio": {
        "meta_description": "Inglês Online ao Vivo B1+ para ganhar fluência intermediária. Pratique reported speech, conditionals, modais e conversas mais completas.",
        "meta_keywords": "curso de inglês online intermediário, inglês B1+, inglês intermediário online, conversação em inglês, curso de inglês com professor, inglês ao vivo",
    },
    "ingl-s-upper-intermedi-rio": {
        "meta_description": "Inglês Online ao Vivo B2 para fluência profissional. Aprimore argumentação, hipóteses, vocabulário avançado e comunicação com segurança.",
        "meta_keywords": "curso de inglês online B2, inglês intermediário avançado, inglês profissional, inglês para trabalho, conversação avançada em inglês, aula de inglês ao vivo",
    },
    "ingl-s-avan-ado": {
        "meta_description": "Inglês Online ao Vivo C1 para fluência avançada. Aperfeiçoe discurso, precisão gramatical, vocabulário sofisticado e comunicação profissional.",
        "meta_keywords": "curso de inglês online C1, inglês avançado online, fluência em inglês, inglês profissional avançado, conversação avançada, inglês para carreira",
    },
    "espanhol-basico": {
        "meta_description": "Espanhol Online Básico A1-A2 para brasileiros. Comece do zero, saia do portunhol e pratique conversas reais com professor ao vivo.",
        "meta_keywords": "curso de espanhol online, espanhol básico, espanhol para brasileiros, sair do portunhol, aula de espanhol ao vivo, espanhol A1 A2, espanhol para viagem",
    },
    "espanhol-intermediario": {
        "meta_description": "Espanhol Online Intermediário B1-B2.1 para conversar com opinião, narrar experiências, corrigir o portunhol e ganhar fluência.",
        "meta_keywords": "curso de espanhol intermediário, espanhol online B1, espanhol B2, conversação em espanhol, espanhol para trabalho, espanhol para brasileiros, portunhol",
    },
    "espanhol-avancado": {
        "meta_description": "Espanhol Online Avançado B2.2-C1 para fluência, carreira e cultura. Aperfeiçoe argumentação, precisão e comunicação profissional.",
        "meta_keywords": "curso de espanhol avançado, espanhol online C1, espanhol profissional, fluência em espanhol, espanhol para carreira, conversação avançada em espanhol",
    },
    "portugues-para-estrangeiros-basico": {
        "meta_description": "Português para Estrangeiros Básico. Comece do zero com saudações, vocabulário essencial e comunicação real no Brasil.",
        "meta_keywords": "português para estrangeiros, português brasileiro, PLE básico, curso de português online, português para iniciantes, Brazilian Portuguese, português do Brasil",
    },
    "portugues-para-estrangeiros-intermediario": {
        "meta_description": "Português para Estrangeiros Intermediário. Amplie vocabulário, domine tempos do passado e converse melhor em situações sociais e profissionais.",
        "meta_keywords": "português para estrangeiros intermediário, PLE intermediário, português brasileiro online, Brazilian Portuguese B1, curso de português para estrangeiros, português no Brasil",
    },
    "portugues-para-estrangeiros-avancado": {
        "meta_description": "Português para Estrangeiros Avançado. Aperfeiçoe fluência, subjuntivo, textos autênticos e comunicação acadêmica e profissional no Brasil.",
        "meta_keywords": "português para estrangeiros avançado, PLE avançado, português brasileiro avançado, Brazilian Portuguese C1, português profissional, português acadêmico",
    },
    "iorub-b-sico": {
        "meta_description": "Curso de Iorubá Básico online. Aprenda saudações, alfabeto, tons, pronomes, numerais e diálogos iniciais com contexto cultural.",
        "meta_keywords": "curso de iorubá online, iorubá básico, aprender iorubá, yorùbá online, língua iorubá, cultura iorubá, aula de iorubá ao vivo",
    },
    "iorub-intermedi-rio": {
        "meta_description": "Curso de Iorubá Intermediário online. Aprofunde classes de palavras, verbos seriais, aspectos verbais, expressões e conversação.",
        "meta_keywords": "iorubá intermediário, curso de iorubá online, aprender yorùbá, conversação em iorubá, gramática iorubá, aula de iorubá ao vivo",
    },
    "iorub-avan-ado": {
        "meta_description": "Curso de Iorubá Avançado online. Desenvolva fluência, gramática complexa, literatura, história, filosofia e uso cultural da língua.",
        "meta_keywords": "iorubá avançado, curso avançado de iorubá, yorùbá avançado, literatura iorubá, cultura iorubá, língua iorubá online, conversação avançada",
    },
    "hebraico-a0-alfabetizacao": {
        "meta_description": "Hebraico A0 Alfabetização online. Aprenda o alef-bet, reconheça sons, leia as primeiras palavras e comece com professor ao vivo.",
        "meta_keywords": "hebraico A0, alfabetização em hebraico, alef-bet, alfabeto hebraico, curso de hebraico online, hebraico para iniciantes, aprender hebraico",
    },
    "hebraico-moderno-a1": {
        "meta_description": "Hebraico Moderno A1 online. Comece do zero com leitura inicial, pronúncia, frases do dia a dia e aulas ao vivo em turma pequena.",
        "meta_keywords": "hebraico moderno A1, curso de hebraico online, aprender hebraico moderno, hebraico para iniciantes, aula de hebraico ao vivo, hebraico básico",
    },
    "hebraico-moderno-a2-b1": {
        "meta_description": "Hebraico Moderno A2/B1 online. Amplie vocabulário, leitura e conversação para narrar experiências, falar de planos e ganhar autonomia.",
        "meta_keywords": "hebraico moderno A2, hebraico B1, curso de hebraico online, conversação em hebraico, hebraico intermediário, aprender hebraico moderno",
    },
    "hebraico-biblico-leitura-guiada": {
        "meta_description": "Hebraico Bíblico online com leitura guiada. Estude textos selecionados com base linguística, vocabulário, contexto e orientação responsável.",
        "meta_keywords": "hebraico bíblico online, curso de hebraico bíblico, leitura bíblica em hebraico, hebraico antigo, textos hebraicos, hebraico com professor",
    },
    "hebraico-particular": {
        "meta_description": "Aulas particulares de hebraico online. Plano 1:1 personalizado para alfabetização, hebraico moderno, leitura, conversação ou objetivos específicos.",
        "meta_keywords": "aula particular de hebraico, hebraico online 1:1, professor de hebraico, curso particular de hebraico, hebraico personalizado, aula de hebraico ao vivo",
    },
}

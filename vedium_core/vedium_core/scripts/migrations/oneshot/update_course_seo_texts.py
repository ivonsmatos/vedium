# -*- coding: utf-8 -*-
"""Atualiza short_introduction/description (LMS Course, "Sobre o curso" no
formulário) dos 20 cursos com os textos SEO/GEO preparados em
Cliente/Vedium/Artigos/Publicar (arquivo
"textos_seo_cursos_vedium_todos_niveis.md", 2026-07-15) — substitui as
descrições antigas (foco em lista de conteúdo gramatical) por texto
comercial "para quem é / o que aprende / resultado final", como já é o
padrão usado em course_translations.py e nos cursos de Espanhol/PLE/
Hebraico criados via oneshot.

short_introduction também alimenta a <meta name="description"> real da
página pública (/curso/<slug>, truncada em 155 caracteres — ver
www/curso.py). O arquivo-fonte também tinha um texto de "Meta Description"
dedicado e um de "Meta Keywords", mas LMS Course NÃO tem esses campos (a
seção "Meta Tags" que aparece no formulário do Frappe é o doctype separado
Website Route Meta, vinculado por URL da página, não pelo curso — e
meta_keywords não tem efeito de SEO desde que o Google parou de usá-la,
~2009). Não vale a complexidade de integrar Website Route Meta só por
isso; ver decisão de 2026-07-15.

Usa frappe.db.set_value (não doc.save()) -- alguns cursos em produção têm
dado pré-existente inconsistente (paid_certificate + certificado de
conclusão marcados juntos) que faz LMSCourse.validate_certification()
lançar ValidationError em QUALQUER doc.save(), mesmo quando os campos
alterados aqui não têm nada a ver com certificado. set_value grava os
campos direto no banco sem rodar validate() (mesmo padrão já usado em
rename_english_course_titles.py, pelo mesmo motivo). Efeito colateral:
doc_events (on_update -> vedium_core.courses.bump_courses_cache_version)
não dispara -- rode `bench --site app.vediums.com clear-cache` logo depois
pra não esperar os 5 minutos do CACHE_TTL.

Rodar (idempotente — reaplica o mesmo valor, sem duplicar nada):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.update_course_seo_texts.run
"""

import frappe

COURSE_TEXTS = {
    "ingl-s-beginner": {
        "short_introduction": "Para quem está começando do zero. Aprenda cumprimentos, vocabulário essencial, frases simples e primeiras conversas em inglês com professor ao vivo.",
        "description": (
            "<p>O curso <strong>Inglês Online ao Vivo A1 – Iniciante</strong> é destinado a quem "
            "nunca estudou inglês ou precisa recomeçar com uma base clara, segura e prática. Você "
            "aprenderá vocabulário essencial, frases simples, pronúncia inicial e estruturas básicas "
            "para se comunicar em situações do dia a dia.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Usar cumprimentos, apresentações e despedidas em inglês</li>"
            "<li>Falar sobre nome, idade, nacionalidade, família, rotina e preferências</li>"
            "<li>Formular perguntas e respostas simples no presente</li>"
            "<li>Compreender diálogos curtos em situações cotidianas</li>"
            "<li>Usar vocabulário básico para compras, horários, lugares e objetos</li>"
            "<li>Participar de conversas simples com mais confiança e menos medo de errar</li>"
            "</ul>"
        ),
    },
    "ingl-s-elementary": {
        "short_introduction": "Para quem já conhece o básico e quer ganhar segurança. Consolide gramática, vocabulário cotidiano, escuta e conversação em inglês ao vivo.",
        "description": (
            "<p>O curso <strong>Inglês Online ao Vivo A2 – Básico</strong> é indicado para alunos "
            "que já tiveram contato com o inglês, mas ainda precisam consolidar estruturas essenciais "
            "antes de avançar para conversas mais longas. O foco é transformar conhecimento solto em "
            "comunicação funcional.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Falar sobre rotina, experiências simples, planos e preferências</li>"
            "<li>Usar presente, passado e futuro em situações reais</li>"
            "<li>Fazer perguntas, responder com clareza e manter diálogos curtos</li>"
            "<li>Compreender instruções, conversas simples e textos de nível básico</li>"
            "<li>Ampliar vocabulário de trabalho, estudo, viagem e vida cotidiana</li>"
            "<li>Ganhar confiança para avançar para o nível pré-intermediário</li>"
            "</ul>"
        ),
    },
    "ingl-s-pr-intermedi-rio": {
        "short_introduction": "Para quem já sabe o básico, mas trava ao falar. Desenvolva conversação, vocabulário, tempos verbais e comunicação funcional em inglês.",
        "description": (
            "<p>O curso <strong>Inglês Online ao Vivo B1 – Pré-Intermediário</strong> é destinado a "
            "quem já entende estruturas básicas, mas ainda sente dificuldade para falar com "
            "naturalidade. Você vai praticar conversas reais, organizar melhor as frases e ampliar "
            "sua capacidade de expressar ideias.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Conversar sobre rotina, experiências, planos e situações comuns</li>"
            "<li>Usar tempos verbais com mais segurança em fala e escrita</li>"
            "<li>Dar opiniões simples e justificar escolhas</li>"
            "<li>Entender diálogos mais longos em contextos familiares</li>"
            "<li>Usar conectores, quantificadores e estruturas funcionais</li>"
            "<li>Reduzir travas comuns na conversação em inglês</li>"
            "</ul>"
        ),
    },
    "ingl-s-intermedi-rio": {
        "short_introduction": "Para quem já conversa, mas precisa falar com mais estrutura. Desenvolva fluência intermediária, vocabulário e comunicação em situações diversas.",
        "description": (
            "<p>O curso <strong>Inglês Online ao Vivo B1+ – Intermediário</strong> é ideal para quem "
            "já consegue se comunicar, mas ainda precisa organizar melhor ideias, narrar situações, "
            "explicar opiniões e sustentar conversas com mais autonomia. As aulas combinam prática "
            "oral, gramática em uso e correção ao vivo.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Sustentar conversas mais longas sobre temas pessoais e profissionais</li>"
            "<li>Usar modais, conditionals e reported speech em contexto</li>"
            "<li>Narrar experiências no passado com mais precisão</li>"
            "<li>Explicar opiniões, escolhas, planos e possibilidades</li>"
            "<li>Melhorar fluência, pronúncia e escuta em situações reais</li>"
            "<li>Preparar-se para objetivos como viagem, entrevista, trabalho ou estudos</li>"
            "</ul>"
        ),
    },
    "ingl-s-upper-intermedi-rio": {
        "short_introduction": "Para quem quer falar inglês com mais precisão e presença. Desenvolva argumentação, vocabulário profissional, escuta e fluência em nível B2.",
        "description": (
            "<p>O curso <strong>Inglês Online ao Vivo B2 – Intermediário Avançado</strong> é voltado "
            "para alunos que já se comunicam em inglês, mas querem falar com mais precisão, "
            "naturalidade e maturidade. O foco é usar o idioma em contextos profissionais, acadêmicos "
            "e sociais com maior autonomia.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Argumentar, explicar pontos de vista e defender opiniões</li>"
            "<li>Usar estruturas avançadas para hipóteses, contraste e causa/consequência</li>"
            "<li>Participar de reuniões, apresentações e conversas profissionais</li>"
            "<li>Ampliar vocabulário para temas abstratos e situações formais</li>"
            "<li>Melhorar pronúncia, ritmo e clareza na fala</li>"
            "<li>Compreender materiais mais autênticos com maior independência</li>"
            "</ul>"
        ),
    },
    "ingl-s-avan-ado": {
        "short_introduction": "Para quem já fala inglês e quer refinamento. Aperfeiçoe fluência, precisão, discurso, vocabulário sofisticado e comunicação profissional.",
        "description": (
            "<p>O curso <strong>Inglês Online ao Vivo C1 – Avançado</strong> é indicado para alunos "
            "que já têm boa fluência e desejam refinar o uso do inglês em contextos exigentes. O foco "
            "está em precisão, naturalidade, argumentação, vocabulário avançado e domínio de registros "
            "formais e informais.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Comunicar ideias complexas com clareza, precisão e naturalidade</li>"
            "<li>Usar estruturas avançadas como inversão, discurso indireto e marcadores discursivos</li>"
            "<li>Participar de debates, reuniões e apresentações em alto nível</li>"
            "<li>Compreender textos, vídeos e discussões mais densas</li>"
            "<li>Refinar estilo, vocabulário e pronúncia</li>"
            "<li>Usar inglês com mais segurança em ambientes acadêmicos e profissionais</li>"
            "</ul>"
        ),
    },
    "espanhol-basico": {
        "short_introduction": "Para quem quer começar espanhol do jeito certo. Aprenda saudações, frases essenciais, pronúncia, vocabulário e conversas básicas sem cair no portunhol.",
        "description": (
            "<p>O curso <strong>Espanhol — Nível Básico (A1-A2)</strong> é destinado a brasileiros "
            "que querem começar do zero ou organizar uma base inicial sem depender do portunhol. Você "
            "aprenderá estruturas essenciais, vocabulário cotidiano, pronúncia e situações reais de "
            "comunicação.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Usar saudações, apresentações e frases essenciais em espanhol</li>"
            "<li>Falar sobre rotina, família, trabalho, gostos e necessidades básicas</li>"
            "<li>Pedir informações, fazer compras e se comunicar em viagens simples</li>"
            "<li>Reconhecer falsos cognatos e evitar erros comuns do portunhol</li>"
            "<li>Compreender diálogos curtos em espanhol falado</li>"
            "<li>Participar de conversas básicas com mais segurança e correção</li>"
            "</ul>"
        ),
    },
    "espanhol-intermediario": {
        "short_introduction": "Para quem já entende espanhol, mas precisa falar melhor. Desenvolva conversação, narrativa, opinião, passado, subjuntivo e vocabulário mais natural.",
        "description": (
            "<p>O curso <strong>Espanhol — Nível Intermediário (B1-B2.1)</strong> é indicado para "
            "quem já tem base no idioma, entende textos e conversas simples, mas precisa sustentar "
            "diálogos com mais autonomia. O foco é sair da comunicação básica para conversas com "
            "opinião, narrativa e nuance.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Narrar experiências no passado com mais clareza</li>"
            "<li>Conversar sobre trabalho, viagem, cultura, rotina e opinião</li>"
            "<li>Usar estruturas intermediárias, incluindo tempos compostos e subjuntivo inicial</li>"
            "<li>Corrigir interferências do português na fala e na escrita</li>"
            "<li>Ampliar vocabulário para situações sociais e profissionais</li>"
            "<li>Participar de conversas mais longas com confiança</li>"
            "</ul>"
        ),
    },
    "espanhol-avancado": {
        "short_introduction": "Para quem já fala espanhol e quer refinar fluência. Trabalhe precisão, argumentação, apresentações, cultura e comunicação profissional avançada.",
        "description": (
            "<p>O curso <strong>Espanhol — Nível Avançado (B2.2-C1)</strong> é voltado para alunos "
            "que já se comunicam bem em espanhol e desejam aprimorar precisão, fluência, vocabulário "
            "sofisticado e presença em contextos profissionais, acadêmicos e culturais.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Argumentar com clareza em temas complexos</li>"
            "<li>Participar de reuniões, apresentações e debates em espanhol</li>"
            "<li>Usar registros formais e informais com mais naturalidade</li>"
            "<li>Compreender variações culturais e linguísticas do mundo hispânico</li>"
            "<li>Refinar pronúncia, vocabulário e estilo de fala</li>"
            "<li>Comunicar-se com maturidade em contextos de carreira, viagem e certificação</li>"
            "</ul>"
        ),
    },
    "portugues-para-estrangeiros-basico": {
        "short_introduction": "Para quem está começando do zero. Aprenda saudações, vocabulário essencial e comunicação básica do português brasileiro com imersão cultural.",
        "description": (
            "<p>O curso <strong>Português para Estrangeiros — Nível Básico (PLE)</strong> é "
            "destinado a quem não tem nenhum conhecimento ou tem contato muito limitado com o "
            "português brasileiro. Você aprenderá estruturas essenciais e vocabulário necessário "
            "para se comunicar em situações do dia a dia no Brasil.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Usar saudações, apresentações e despedidas</li>"
            "<li>Fornecer e solicitar informações pessoais, como nome, nacionalidade, idade e profissão</li>"
            "<li>Formular frases simples no presente do indicativo</li>"
            "<li>Pedir em restaurantes, fazer compras e perguntar direções</li>"
            "<li>Compreender aspectos culturais básicos do Brasil</li>"
            "<li>Participar de interações simples com mais autonomia</li>"
            "</ul>"
        ),
    },
    "portugues-para-estrangeiros-intermediario": {
        "short_introduction": "Para estrangeiros que já têm base no português. Ganhe fluência em conversas sociais, profissionais e situações reais da vida no Brasil.",
        "description": (
            "<p>O curso <strong>Português para Estrangeiros — Nível Intermediário (PLE)</strong> é "
            "indicado para quem já consegue se apresentar e formar frases simples, mas precisa "
            "ampliar vocabulário, melhorar escuta e falar com mais segurança em situações sociais e "
            "profissionais.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Narrar experiências no passado usando tempos verbais com mais precisão</li>"
            "<li>Conversar sobre rotina, trabalho, estudos, saúde, serviços e vida no Brasil</li>"
            "<li>Entender brasileiros falando em situações cotidianas</li>"
            "<li>Usar expressões brasileiras comuns com mais naturalidade</li>"
            "<li>Escrever mensagens, e-mails simples e textos curtos</li>"
            "<li>Participar de conversas sociais e profissionais com mais autonomia</li>"
            "</ul>"
        ),
    },
    "portugues-para-estrangeiros-avancado": {
        "short_introduction": "Para estrangeiros que já falam português e querem refinamento. Aperfeiçoe fluência, vocabulário, escrita, leitura e comunicação profissional.",
        "description": (
            "<p>O curso <strong>Português para Estrangeiros — Nível Avançado (PLE)</strong> é "
            "voltado para quem já tem boa fluência e deseja aperfeiçoar precisão, vocabulário, "
            "compreensão de textos autênticos e comunicação em contextos acadêmicos, profissionais "
            "e culturais.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Usar estruturas avançadas, incluindo subjuntivo, conectores e nuances de sentido</li>"
            "<li>Compreender textos autênticos, notícias, vídeos e conversas mais rápidas</li>"
            "<li>Participar de reuniões, apresentações e discussões profissionais</li>"
            "<li>Escrever textos mais claros, formais e bem organizados</li>"
            "<li>Entender expressões idiomáticas, informalidade e contexto cultural brasileiro</li>"
            "<li>Comunicar-se com mais naturalidade e precisão em português brasileiro</li>"
            "</ul>"
        ),
    },
    "iorub-b-sico": {
        "short_introduction": "Para quem quer começar iorubá com base sólida. Aprenda sons, tons, saudações, vocabulário essencial e frases iniciais com responsabilidade cultural.",
        "description": (
            "<p>O curso <strong>Iorubá — Básico</strong> é destinado a quem deseja iniciar o estudo "
            "da língua iorubá com estrutura, pronúncia orientada e contexto cultural. O foco é "
            "construir uma base segura para entender sons, tons, saudações, vocabulário essencial e "
            "diálogos simples.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Reconhecer sons, tons e elementos básicos da pronúncia</li>"
            "<li>Usar saudações e expressões de respeito em iorubá</li>"
            "<li>Compreender vocabulário essencial de família, corpo, casa, rotina e números</li>"
            "<li>Formular frases simples para perguntar e responder</li>"
            "<li>Entender aspectos culturais ligados ao uso da língua</li>"
            "<li>Participar de diálogos iniciais com mais segurança</li>"
            "</ul>"
        ),
    },
    "iorub-intermedi-rio": {
        "short_introduction": "Para quem já tem base em iorubá. Aprofunde gramática, verbos, expressões, vocabulário cultural e conversação com orientação ao vivo.",
        "description": (
            "<p>O curso <strong>Iorubá — Intermediário</strong> é indicado para alunos que já "
            "conhecem fundamentos da língua e desejam avançar para estruturas mais completas. As "
            "aulas trabalham classes de palavras, verbos, aspectos verbais, expressões idiomáticas e "
            "conversação guiada.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Formar frases mais completas e naturais em iorubá</li>"
            "<li>Usar verbos, pronomes e estruturas com mais precisão</li>"
            "<li>Compreender aspectos verbais e verbos seriais</li>"
            "<li>Ampliar vocabulário para temas sociais, culturais e cotidianos</li>"
            "<li>Interpretar expressões com atenção ao contexto</li>"
            "<li>Sustentar conversas guiadas com maior autonomia</li>"
            "</ul>"
        ),
    },
    "iorub-avan-ado": {
        "short_introduction": "Para quem busca fluência e aprofundamento cultural. Estude gramática complexa, literatura, história, filosofia iorubá e conversação avançada.",
        "description": (
            "<p>O curso <strong>Iorubá — Avançado</strong> é voltado para estudantes que já dominam "
            "estruturas intermediárias e desejam aprofundar fluência, leitura, interpretação cultural "
            "e uso mais sofisticado da língua. O curso integra gramática complexa, literatura, "
            "história, filosofia e prática oral.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Usar estruturas gramaticais complexas com mais precisão</li>"
            "<li>Ler e interpretar textos mais densos em iorubá</li>"
            "<li>Compreender referências históricas, culturais e filosóficas</li>"
            "<li>Expressar ideias abstratas e opiniões com mais profundidade</li>"
            "<li>Ampliar vocabulário acadêmico, cultural e profissional</li>"
            "<li>Comunicar-se em contextos avançados com maior segurança</li>"
            "</ul>"
        ),
    },
    "hebraico-a0-alfabetizacao": {
        "short_introduction": "Para quem nunca leu hebraico. Aprenda o alef-bet, reconheça letras e sons, leia palavras iniciais e dê o primeiro passo com segurança.",
        "description": (
            "<p>O curso <strong>Hebraico A0 — Alfabetização</strong> é destinado a quem nunca teve "
            "contato com o alfabeto hebraico ou sente insegurança para reconhecer letras e sons. A "
            "proposta é criar uma base de leitura inicial antes de avançar para frases e comunicação "
            "em hebraico moderno.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Reconhecer as letras do alef-bet</li>"
            "<li>Identificar sons e padrões básicos de leitura</li>"
            "<li>Ler palavras e combinações simples em hebraico</li>"
            "<li>Entender a direção da escrita e características do sistema hebraico</li>"
            "<li>Corrigir dúvidas iniciais de pronúncia com professor ao vivo</li>"
            "<li>Avançar com mais segurança para o Hebraico Moderno A1</li>"
            "</ul>"
        ),
    },
    "hebraico-moderno-a1": {
        "short_introduction": "Para começar no hebraico moderno. Desenvolva leitura inicial, pronúncia, vocabulário essencial e frases simples do cotidiano com professor ao vivo.",
        "description": (
            "<p>O curso <strong>Hebraico Moderno — Nível A1</strong> é indicado para quem quer "
            "iniciar o hebraico moderno como língua viva, com leitura inicial, pronúncia, vocabulário "
            "essencial e comunicação básica. As aulas são ao vivo e ajudam o aluno a evitar travas "
            "comuns no início.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Ler palavras e frases simples em hebraico moderno</li>"
            "<li>Usar cumprimentos, apresentações e expressões do dia a dia</li>"
            "<li>Falar sobre nome, origem, família, rotina e preferências</li>"
            "<li>Reconhecer vocabulário essencial de situações cotidianas</li>"
            "<li>Praticar pronúncia com correção em tempo real</li>"
            "<li>Construir as primeiras conversas com mais confiança</li>"
            "</ul>"
        ),
    },
    "hebraico-moderno-a2-b1": {
        "short_introduction": "Para quem já tem base no hebraico. Amplie leitura, vocabulário, conversação e autonomia para falar de experiências, planos e situações reais.",
        "description": (
            "<p>O curso <strong>Hebraico Moderno — Nível A2/B1</strong> é voltado para alunos que já "
            "conhecem o alfabeto e conseguem formar frases simples, mas precisam ampliar vocabulário, "
            "leitura, escuta e conversação. O objetivo é desenvolver autonomia básica no uso do "
            "hebraico moderno.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Ler textos curtos e compreender ideias principais</li>"
            "<li>Narrar experiências, falar de rotina, planos e preferências</li>"
            "<li>Fazer perguntas e sustentar conversas mais longas</li>"
            "<li>Ampliar vocabulário de vida cotidiana, viagem, cultura e comunicação social</li>"
            "<li>Usar estruturas gramaticais intermediárias com mais segurança</li>"
            "<li>Ganhar mais fluência e independência no hebraico moderno</li>"
            "</ul>"
        ),
    },
    "hebraico-biblico-leitura-guiada": {
        "short_introduction": "Para quem deseja ler textos bíblicos com orientação. Estude vocabulário, estrutura, leitura guiada e contexto linguístico de forma responsável.",
        "description": (
            "<p>O curso <strong>Hebraico Bíblico — Leitura Guiada</strong> é destinado a estudantes "
            "interessados em ler textos selecionados em hebraico bíblico com base linguística, "
            "vocabulário, contexto e acompanhamento responsável. A proposta é priorizar leitura, "
            "compreensão e análise, sem prometer interpretações simplificadas.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p>"
            "<ul>"
            "<li>Reconhecer estruturas e vocabulário frequente em textos bíblicos selecionados</li>"
            "<li>Ler trechos guiados com apoio linguístico</li>"
            "<li>Entender diferenças entre hebraico moderno e hebraico bíblico</li>"
            "<li>Identificar elementos gramaticais importantes para a leitura</li>"
            "<li>Trabalhar contexto, forma e significado com cuidado</li>"
            "<li>Desenvolver uma base mais segura para estudos acadêmicos, culturais ou religiosos</li>"
            "</ul>"
        ),
    },
    "hebraico-particular": {
        "short_introduction": "Aulas 1:1 para quem precisa de um plano personalizado. Estude hebraico moderno, alfabetização, leitura ou conversação conforme seu objetivo.",
        "description": (
            "<p>O curso <strong>Hebraico Particular</strong> é destinado a alunos que preferem "
            "acompanhamento individual ou precisam de um plano personalizado. As aulas 1:1 podem ser "
            "ajustadas para alfabetização, hebraico moderno, leitura, conversação, revisão, "
            "preparação específica ou continuidade de estudos.</p>"
            "<p><strong>Ao final do plano você poderá desenvolver:</strong></p>"
            "<ul>"
            "<li>Leitura do alef-bet e reconhecimento de sons</li>"
            "<li>Pronúncia com correção individual</li>"
            "<li>Vocabulário e frases voltadas ao seu objetivo</li>"
            "<li>Conversação guiada em hebraico moderno</li>"
            "<li>Leitura de textos selecionados com orientação</li>"
            "<li>Um plano de estudo personalizado conforme seu nível, ritmo e necessidade</li>"
            "</ul>"
        ),
    },
}


def run():
    updated, missing = 0, []
    for course_name, texts in COURSE_TEXTS.items():
        if not frappe.db.exists("LMS Course", course_name):
            missing.append(course_name)
            print(f"  AVISO: curso '{course_name}' não existe, pulando.")
            continue
        frappe.db.set_value("LMS Course", course_name, {
            "short_introduction": texts["short_introduction"],
            "description": texts["description"],
        })
        updated += 1
        print(f"  ✓ '{course_name}' atualizado.")

    frappe.db.commit()
    print(f"\n✓ {updated}/{len(COURSE_TEXTS)} cursos atualizados.")
    if missing:
        print(f"  Não encontrados: {', '.join(missing)}")

# -*- coding: utf-8 -*-
"""Criação dos cursos de Espanhol (Básico A1-A2, Intermediário B1-B2.1,
Avançado B2.2-C1) a partir da grade pedagógica e do material de aula
fornecidos pela coordenação (docs "Vedium_Grade/Material_Espanhol_*", 2026).

Conteúdo de cada lição = "Objetivo comunicativo" + "Entrada da unidade" +
"Linguagem ativa" + "Aula ao vivo" + "Prática entre aulas" + "Tarefa final" +
"Atividades originais Vedium" (todo o material é autoral da Vedium; o livro
mencionado nas fontes serve só de referência metodológica, sem reprodução
de texto/exercícios de terceiros).

Executar UMA VEZ no servidor após o deploy:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.create_espanhol_courses.run

Depois, para os quizzes:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.seed_espanhol_quizzes.run
"""

import json

import frappe

CATEGORY = "Espanhol"
CURRENCY = "BRL"

CLOSING_NOTE = (
    "<b>Fechamento da aula:</b> pergunta final para a turma — \"O que você já "
    "consegue fazer em espanhol depois desta unidade?\" (resposta curta, sem "
    "traduzir). Registro no LMS: áudio curto, texto breve ou checklist de "
    "vocabulário ativo, conforme o perfil da turma."
)


# ---------------------------------------------------------------------------
# Conteúdo por nível — (título, objetivo, entrada, linguagem ativa,
# aula ao vivo, prática entre aulas, tarefa final, [atividades Vedium])
# ---------------------------------------------------------------------------

def _basico_modules():
    return [
        (
            "Módulo 0 — En el aula: começar a falar em espanhol",
            "Criar segurança para usar espanhol desde a primeira aula, mesmo com repertório pequeno.",
            "Mini conversa de sala: saludos, despedidas, pedidos de repetição e frases para tirar dúvida.",
            "Saludos, despedidas, alfabeto, números 1-20, objetos da sala, ¿qué significa?, ¿cómo se dice?",
            "Rodada rápida: cada aluno cumprimenta, soletra o nome e pede ajuda usando uma frase de aula.",
            "Gravar áudio de 30 segundos apresentando nome, cidade e uma frase de dúvida em espanhol.",
            "Criar o \"pacto de aula\": 5 frases que a turma vai usar sempre em espanhol.",
            [
                "Complete os comandos da aula com uma palavra adequada: repetir, despacio, significa, escribe, escucha.",
                "Em duplas, simule uma situação em que você não entende uma palavra e precisa manter a conversa.",
                "Liste 5 palavras espanholas que você já conhece e confirme a pronúncia em aula.",
            ],
        ),
        (
            "Módulo 1 — Nosotros y nosotras: identidade e dados pessoais",
            "Dar e pedir informações pessoais com naturalidade básica.",
            "Perfis curtos de estudantes internacionais e formulário de inscrição.",
            "Ser, llamarse, tener, nacionalidades, profissões, números, e-mail e telefone.",
            "Entrevista em cadeia: cada aluno entrevista um colega e apresenta a pessoa à turma.",
            "Preencher uma ficha de perfil e escrever 5 frases sobre si.",
            "Criar um perfil pessoal em espanhol para a plataforma Vedium.",
            [
                "Transforme dados soltos em frases completas: nombre, país, ciudad, profesión, contacto.",
                "Pergunte e responda: ¿De dónde eres? ¿A qué te dedicas? ¿Cuántos años tienes?",
                "Corrija interferências: \"soy brasileño\", \"tengo 32 años\", \"vivo en São Paulo\".",
            ],
        ),
        (
            "Módulo 2 — Quiero aprender español: objetivos e motivações",
            "Explicar por que estuda espanhol e definir uma meta simples de aprendizagem.",
            "Depoimentos curtos de pessoas que estudam por trabalho, viagem, família ou cultura.",
            "Presente regular, porque/para, atividades de aprendizagem, idiomas e lazer.",
            "Mapa de objetivos: cada aluno apresenta uma meta e recebe perguntas da turma.",
            "Escrever um plano de 30 dias com 3 ações pequenas.",
            "Apresentar oralmente seu plano pessoal de estudo.",
            [
                "Complete: Estudio español porque... / Quiero aprender para... / Necesito practicar...",
                "Associe objetivos a ações: escuchar, leer, hablar, escribir, revisar.",
                "Faça uma promessa realista de estudo para a próxima semana.",
            ],
        ),
        (
            "Módulo 3 — Mundo hispano: países, cidades e clima",
            "Localizar países, falar de cidades, clima e primeiras referências culturais.",
            "Mapa do mundo hispanofalante e cartões com dados de países/cidades.",
            "Hay/estar, artículos indefinidos, muy/mucho, interrogativos, clima, lugares.",
            "Quiz cultural com perguntas simples e respostas completas.",
            "Escolher uma cidade hispanofalante e gravar 5 frases sobre ela.",
            "Apresentar uma cidade em 1 minuto: onde fica, como é e por que visitar.",
            [
                "Compare duas cidades usando adjetivos simples.",
                "Pergunte: ¿Dónde está...? ¿Cómo es...? ¿Qué hay en...?",
                "Monte uma previsão do tempo de 3 dias para uma cidade.",
            ],
        ),
        (
            "Módulo 4 — ¿Cuál prefieres?: compras, objetos e preferências",
            "Perguntar preço, escolher produtos e justificar preferências.",
            "Catálogo simples de viagem: mochila, roupa, acessórios e objetos pessoais.",
            "Demonstrativos, qué/cuál, tener que, ir, preferir, cores, objetos e preços.",
            "Mercado simulado: alunos compram itens para uma viagem com orçamento limitado.",
            "Criar lista de 8 itens necessários para uma viagem curta.",
            "Defender suas escolhas: \"Prefiero este porque...\".",
            [
                "Complete diálogos de compra com precio, talla, color, quiero, prefiero.",
                "Compare: este/esta/estos/estas vs. ese/esa/esos/esas.",
                "Resolva: você tem 100 euros e precisa montar uma mala mínima.",
            ],
        ),
        (
            "Módulo 5 — Tus amigos son mis amigos: pessoas, família e gostos",
            "Descrever pessoas, relações, gostos e interesses.",
            "Árvore familiar simples e perfis de amigos com hobbies.",
            "Gustar, possessivos, también/tampoco, adjetivos de caráter, família e lazer.",
            "Apresentação de uma pessoa importante sem usar nome; turma adivinha a relação.",
            "Escrever 8 frases sobre uma pessoa próxima.",
            "Apresentar alguém da sua vida com respeito e detalhes.",
            [
                "Organize frases com gustar: A mí me gusta... / A mi hermano le gusta...",
                "Responda com también ou tampoco.",
                "Faça perguntas sobre família e hobbies para um colega.",
            ],
        ),
        (
            "Módulo 6 — Día a día: rotina, hora e frequência",
            "Falar de rotina semanal, horários e hábitos.",
            "Agenda semanal de duas pessoas com trabalhos e atividades diferentes.",
            "Verbos reflexivos, presente irregular, dias da semana, horas, frequência.",
            "Entrevista de hábitos: encontrar semelhanças e diferenças na rotina da turma.",
            "Montar sua agenda em espanhol e marcar 3 hábitos que quer melhorar.",
            "Apresentar sua rotina ideal e sua rotina real.",
            [
                "Transforme infinitivos em frases: levantarse, trabajar, comer, estudiar, dormir.",
                "Use: siempre, casi siempre, a veces, nunca.",
                "Pergunte horários: ¿A qué hora...? ¿Cuándo...?",
            ],
        ),
        (
            "Módulo 7 — ¡A comer!: comida, restaurante e cultura gastronômica",
            "Pedir comida, perguntar sobre pratos e expressar preferências alimentares.",
            "Menu autoral com pratos de países hispânicos e opções vegetarianas.",
            "Quisiera, me trae, se puede, alimentos, formas de preparo, objeto direto inicial.",
            "Roleplay restaurante: cliente, atendente e amigo com restrição alimentar.",
            "Criar um menu do dia com entrada, prato principal, bebida e sobremesa.",
            "Pedir comida em espanhol sem recorrer ao português.",
            [
                "Classifique alimentos: frutas, verduras, carnes, bebidas, postres.",
                "Complete pedidos educados: Quisiera..., ¿Me trae...?, ¿Tiene...?",
                "Discuta: que prato brasileiro você explicaria a um hispanofalante?",
            ],
        ),
        (
            "Módulo 8 — El barrio ideal: cidade e orientação",
            "Descrever bairro/cidade e pedir/dar direções.",
            "Mapa simples de bairro com praça, metrô, mercado, farmácia e escola.",
            "Preposições de lugar, hay/estar, serviços urbanos, adjetivos de bairro.",
            "Jogo de orientação: um aluno guia o outro até um ponto no mapa.",
            "Desenhar ou descrever seu bairro com 8 lugares.",
            "Apresentar o bairro ideal para morar ou visitar.",
            [
                "Use: cerca de, lejos de, al lado de, enfrente de, entre.",
                "Pergunte direções: ¿Cómo llego a...? ¿Hay una farmacia cerca?",
                "Compare bairro tranquilo, ruidoso, seguro, céntrico, verde.",
            ],
        ),
        (
            "Módulo 9 — ¿Sabes conducir?: habilidades e experiências",
            "Falar do que sabe fazer, pode fazer e já fez recentemente.",
            "Anúncio de voluntariado que pede habilidades específicas.",
            "Saber/poder + infinitivo, pretérito perfecto, habilidades, qualidades e experiências.",
            "Seleção de candidatos para uma missão: quem é melhor para cada tarefa?",
            "Escrever 5 habilidades e 3 experiências recentes.",
            "Defender por que você é uma boa pessoa para uma tarefa.",
            [
                "Complete: Sé..., puedo..., he trabajado..., he estudiado...",
                "Diferencie saber e poder em situações reais.",
                "Faça perguntas: ¿Alguna vez has...?",
            ],
        ),
        (
            "Módulo 10 — Viaje esencial: transporte, hospedagem e imprevistos",
            "Resolver situações de chegada, hotel, transporte e pedidos de ajuda.",
            "Roteiro de chegada a uma cidade: aeroporto, hotel, transporte e problema de reserva.",
            "Revisão integrada de presente, hay/estar, tener que, poder, pedir ajuda e confirmar informação.",
            "Circuito oral de viagem com 4 estações: aeroporto, táxi, hotel, loja.",
            "Preparar uma lista de frases para usar em uma viagem real.",
            "Resolver um imprevisto sem sair do espanhol.",
            [
                "Monte frases com necesito, quisiera, tengo una reserva, hay un problema.",
                "Escolha a melhor resposta para manter a conversa educada.",
                "Crie um pequeno diálogo de check-in.",
            ],
        ),
        (
            "Módulo 11 — Projeto final: sobreviver e se conectar em espanhol",
            "Integrar apresentação, compra, restaurante, orientação, rotina e experiência.",
            "Cenário: primeira semana em uma cidade hispanofalante.",
            "Revisão A1-A2, estratégias de comunicação, pronúncia personalizada.",
            "Circuito avaliativo com situações reais e feedback imediato.",
            "Revisar portfólio de áudios, textos curtos e vocabulário ativo.",
            "Apresentação final: \"Mi primera semana en...\" com perguntas da turma.",
            [
                "Organize seu roteiro final em 6 cenas.",
                "Revise 10 erros pessoais que você quer evitar.",
                "Grave a versão final e compare com o primeiro áudio do curso.",
            ],
        ),
    ]


def _intermediario_modules():
    return [
        (
            "Módulo 1 — Diagnóstico ativo: ponte do A2 ao B1",
            "Revisar repertório essencial e mapear lacunas individuais.",
            "Entrevista guiada com temas de vida, trabalho, viagem, estudos e cultura.",
            "Revisão de presente, perfecto, pronomes, gustar, hay/estar, cidade, comida e rotina.",
            "Entrevista diagnóstica em pares + feedback de fluência, precisão e vocabulário.",
            "Escrever uma autoavaliação curta: \"Lo que ya puedo hacer / lo que necesito mejorar\".",
            "Plano individual de evolução com 3 metas para 30 dias.",
            [
                "Responda sem preparação a 8 perguntas do professor.",
                "Identifique seus 5 erros mais frequentes.",
                "Reformule respostas curtas em respostas mais completas.",
            ],
        ),
        (
            "Módulo 2 — Narrar experiências: passado com clareza",
            "Contar experiências pessoais com sequência, contexto e detalhes.",
            "Relato original de uma viagem com problema e solução.",
            "Pretérito perfecto, indefinido e imperfecto; marcadores temporais; conectores narrativos.",
            "Story circle: cada aluno conta uma experiência e recebe 2 perguntas.",
            "Escrever um relato de 180 palavras e gravar a versão oral.",
            "Relato oral de uma experiência marcante, com começo, conflito e fechamento.",
            [
                "Escolha entre perfecto, indefinido e imperfecto em frases contextualizadas.",
                "Ordene eventos usando primero, después, mientras, al final.",
                "Reconte a história de um colega em terceira pessoa.",
            ],
        ),
        (
            "Módulo 3 — Viagem real: imprevistos e negociação",
            "Resolver problemas de transporte, hotel, orientação e atendimento.",
            "Troca de mensagens entre hóspede e hotel sobre uma reserva errada.",
            "Imperativo, perífrases de obrigação/possibilidade, reclamações educadas, serviços.",
            "Simulação com papéis: cliente, atendente, gerente e observador de linguagem.",
            "Preparar 10 frases para reclamar sem ser agressivo.",
            "Resolver um imprevisto de viagem em 4 minutos de roleplay.",
            [
                "Transforme ordens diretas em pedidos educados.",
                "Complete uma reclamação com conectores de causa e solução.",
                "Compare formas de cortesia em países diferentes.",
            ],
        ),
        (
            "Módulo 4 — Trabalho e estudo: reuniões, e-mails e rotina profissional",
            "Falar de responsabilidades, prazos, projetos e comunicação profissional.",
            "E-mail profissional curto e agenda de reunião.",
            "Futuro próximo, condicional de cortesia, léxico de trabalho/estudo, conectores formais.",
            "Reunião simulada para organizar um projeto com tarefas e prazos.",
            "Escrever um e-mail pedindo informação ou confirmação.",
            "Apresentar um projeto simples e distribuir responsabilidades.",
            [
                "Troque frases informais por versões profissionais.",
                "Use plazo, reunión, entrega, propuesta, acuerdo em contexto.",
                "Redija assunto, saudação, corpo e fechamento de e-mail.",
            ],
        ),
        (
            "Módulo 5 — Cultura e identidade: comparar sem estereotipar",
            "Comparar hábitos, cidades e formas de interação com cuidado cultural.",
            "Dois textos curtos sobre costumes urbanos em contextos hispânicos diferentes.",
            "Comparativos, superlativos, estruturas de contraste, vocabulário sociocultural.",
            "Debate guiado: diferenças culturais que ajudam a comunicar melhor.",
            "Escrever uma comparação respeitosa entre dois costumes.",
            "Mini apresentação cultural com fonte e reflexão, não curiosidade solta.",
            [
                "Substitua generalizações por frases cuidadosas: \"en algunos contextos...\".",
                "Use más/menos/tan... como para comparar.",
                "Liste perguntas culturais que você faria a um nativo com respeito.",
            ],
        ),
        (
            "Módulo 6 — Opinião e debate: defender ponto de vista",
            "Expressar opinião, justificar e discordar com educação.",
            "Texto opinativo curto sobre tecnologia, trabalho remoto ou aprendizagem.",
            "Creo que, me parece que, es importante que, conectores de causa e contraste, subjuntivo inicial.",
            "Debate em grupos com papéis: a favor, contra, mediador.",
            "Escrever 2 parágrafos de opinião com exemplo concreto.",
            "Defender uma opinião por 2 minutos e responder a uma objeção.",
            [
                "Transforme \"me gusta/no me gusta\" em argumento.",
                "Use porque, ya que, aunque, sin embargo.",
                "Pratique discordância: entiendo tu punto, pero...",
            ],
        ),
        (
            "Módulo 7 — Planos e hipóteses: futuro, condições e decisões",
            "Falar de planos, possibilidades, riscos e escolhas.",
            "Cenário: escolher entre estudar, viajar, mudar de cidade ou assumir novo trabalho.",
            "Futuro, condicional, si + presente/futuro, marcadores de probabilidade.",
            "Tomada de decisão em grupo com vantagens, riscos e plano B.",
            "Criar uma matriz simples de decisão em espanhol.",
            "Apresentar um plano pessoal/profissional com hipóteses e condições.",
            [
                "Complete: Si tengo tiempo..., si consigo..., probablemente...",
                "Diferencie deseo, plan e posibilidad.",
                "Faça perguntas de acompanhamento para entender melhor o plano de alguém.",
            ],
        ),
        (
            "Módulo 8 — Conselhos e experiências: saúde, hábitos e bem-estar",
            "Dar conselhos, relatar dificuldades e falar de hábitos com cuidado.",
            "Cartas curtas de leitores pedindo conselho sobre rotina e estudos.",
            "Imperativo, deberías, te recomiendo que, es mejor que, vocabulário de saúde e hábitos.",
            "Consultório linguístico: alunos dão conselhos para situações reais de estudo.",
            "Escrever uma resposta de conselho com tom acolhedor.",
            "Criar um plano de melhoria de hábito usando espanhol.",
            [
                "Transforme ordens em conselhos gentis.",
                "Use subjuntivo em fórmulas básicas: te recomiendo que...",
                "Discuta o que ajuda você a manter constância.",
            ],
        ),
        (
            "Módulo 9 — Notícias e mundo atual: compreender e resumir",
            "Ler/ouvir notícias simples, identificar ideia principal e resumir.",
            "Notícia autoral curta sobre educação, cultura ou mobilidade.",
            "Discurso reportado inicial, voz passiva/impessoal, conectores de resumo.",
            "Jornal da turma: cada grupo resume uma notícia e responde perguntas.",
            "Escrever resumo de 100 palavras com opinião final.",
            "Apresentar uma notícia em 90 segundos com contexto e comentário.",
            [
                "Separe fato, opinião e dado num texto curto.",
                "Use según, afirma, explica, destaca.",
                "Reescreva títulos sensacionalistas com tom neutro.",
            ],
        ),
        (
            "Módulo 10 — Mediação: explicar em espanhol o que veio do português",
            "Parafrasear, resumir e explicar informação brasileira para um hispanofalante.",
            "Texto curto em português sobre uma prática brasileira, transformado em explicação em espanhol.",
            "Paráfrase, conectores explicativos, falsos cognatos, equivalências culturais.",
            "Mediação oral: explicar uma notícia, costume ou serviço brasileiro em espanhol claro.",
            "Escolher um tema do Brasil e preparar explicação para estrangeiros.",
            "Gravar áudio de mediação de 2 minutos.",
            [
                "Evite tradução literal em 5 frases.",
                "Explique \"saudade\", \"jeitinho\" ou \"feriado prolongado\" com cuidado.",
                "Peça confirmação: ¿Me explico? ¿Queda claro?",
            ],
        ),
        (
            "Módulo 11 — Variedades do espanhol: escuta e repertório",
            "Reconhecer diferenças de vocabulário, pronúncia e uso sem hierarquizar variedades.",
            "Tabela autoral de variações léxicas: ônibus/autobús/camión/colectivo; computador/ordenador/computadora.",
            "Variedades regionais, marcadores conversacionais, estratégias de confirmação.",
            "Laboratório de escuta: comparar sotaques e estratégias de compreensão.",
            "Montar glossário de 20 variações úteis por contexto.",
            "Apresentar uma variedade do espanhol com respeito e exemplos.",
            [
                "Identifique variações sem dizer \"certo/errado\".",
                "Pratique: ¿A qué te refieres con...? ¿Eso significa...?",
                "Relacione país, palavra e situação de uso.",
            ],
        ),
        (
            "Módulo 12 — Projeto final: conversar, narrar e opinar",
            "Integrar narrativa, opinião, mediação, escuta e escrita funcional.",
            "Tema escolhido pelo aluno: viagem, trabalho, cultura, atualidade ou vida no Brasil.",
            "Revisão B1-B2.1, coesão, passado, opinião, conectores, registro e pronúncia.",
            "Apresentação final com perguntas da turma e feedback do professor.",
            "Preparar texto-base, roteiro oral e vocabulário-chave.",
            "Produzir apresentação oral + texto de opinião + autoavaliação.",
            [
                "Escolha uma tese e 3 argumentos.",
                "Inclua uma história pessoal e uma fonte externa.",
                "Prepare respostas para perguntas difíceis.",
            ],
        ),
    ]


def _avancado_modules():
    return [
        (
            "Módulo 1 — Diagnóstico de fluência e precisão",
            "Mapear padrões de erro, registro, vocabulário e metas de performance.",
            "Entrevista avançada com perguntas profissionais, culturais e pessoais.",
            "Revisão seletiva de tempos, pronomes, preposições, conectores, colocaciones.",
            "Entrevista gravada + análise de 3 pontos fortes e 3 pontos de lapidação.",
            "Transcrever 2 minutos da própria fala e marcar oportunidades de melhoria.",
            "Plano de lapidação individual para 8 semanas.",
            [
                "Reformule 5 frases para ficarem mais naturais.",
                "Identifique vícios de tradução do português.",
                "Crie um glossário pessoal de precisão.",
            ],
        ),
        (
            "Módulo 2 — Argumentação: tese, contra-argumento e nuance",
            "Defender ideias complexas com organização e resposta a objeções.",
            "Texto opinativo autoral sobre IA, educação, trabalho ou mobilidade.",
            "Conectores concessivos, causais, consecutivos; reformulação, modalização, contraste.",
            "Debate com réplica e tréplica; observadores registram conectores usados.",
            "Escrever tese, 3 argumentos, contra-argumento e conclusão.",
            "Debate estruturado de 6 minutos por dupla.",
            [
                "Reescreva opiniões absolutas com nuance.",
                "Use sin embargo, aun así, por consiguiente, si bien.",
                "Construa uma resposta diplomática a uma crítica.",
            ],
        ),
        (
            "Módulo 3 — Subjuntivo avançado e modalidade",
            "Usar subjuntivo para hipótese, restrição, finalidade, avaliação e concessão.",
            "Fragmentos autorais de opinião e recomendação com lacunas de modo verbal.",
            "Subjuntivo em subordinadas, aunque, cuando, para que, de ahí que, como si.",
            "Oficina de reescrita: transformar frases simples em formulações mais precisas.",
            "Criar 10 frases úteis para seu contexto usando subjuntivo.",
            "Reescrever um texto opinativo com maior precisão modal.",
            [
                "Explique a diferença entre aunque + indicativo e aunque + subjuntivo.",
                "Complete frases de desejo, dúvida, restrição e finalidade.",
                "Corrija interferências do português.",
            ],
        ),
        (
            "Módulo 4 — Registro e pragmática: falar bem em cada contexto",
            "Adaptar mensagem a contextos formais, profissionais, acadêmicos e coloquiais.",
            "Mesmo conteúdo em três situações: e-mail formal, áudio para colega, fala em reunião.",
            "Tratamento, atenuadores, marcadores conversacionais, cortesia, ironia, implicatura.",
            "Roleplay: comunicar uma decisão difícil em três registros diferentes.",
            "Reescrever uma mensagem curta em versão formal, neutra e próxima.",
            "Dossiê de registro com 3 versões da mesma mensagem.",
            [
                "Marque expressões que suavizam discordância.",
                "Transforme frases diretas em diplomáticas.",
                "Discuta quando usar tú, usted, vos e formas neutras.",
            ],
        ),
        (
            "Módulo 5 — Mídia e leitura crítica",
            "Compreender textos e áudios complexos, identificar viés e resumir com clareza.",
            "Editorial autoral e roteiro de podcast sobre tema social contemporâneo.",
            "Léxico abstrato, nominalizações, discurso reportado, marcas de subjetividade.",
            "Análise guiada: fato, interpretação, fonte, viés e ausência de informação.",
            "Produzir resumo crítico de 180 a 220 palavras.",
            "Apresentar uma leitura crítica em 3 minutos.",
            [
                "Substitua verbos genéricos por verbos de análise: sostiene, cuestiona, matiza.",
                "Diferencie argumento e evidência.",
                "Reescreva um título para reduzir viés.",
            ],
        ),
        (
            "Módulo 6 — Espanhol profissional: reunião, relatório e negociação",
            "Conduzir reuniões, negociar prazos, discordar com diplomacia e produzir sínteses.",
            "Briefing de projeto com problema de prazo, orçamento e escopo.",
            "Linguagem corporativa, modalização, condicional, conectores formais, ata e resumo executivo.",
            "Simulação de reunião com tomada de decisão e ata feita em tempo real.",
            "Escrever resumo executivo de 1 página.",
            "Negociar uma solução e entregar ata/resumo em espanhol.",
            [
                "Troque \"no puedo\" por alternativas diplomáticas.",
                "Use: acordar, plantear, posponer, priorizar, ejecutar.",
                "Escreva 5 frases de alinhamento de expectativas.",
            ],
        ),
        (
            "Módulo 7 — Cultura, sociedade e história: discutir com respeito",
            "Falar de temas culturais e históricos sem simplificação ou exotização.",
            "Dossiê com fontes curtas sobre migração, memória, identidade, língua e arte.",
            "Vocabulário sociocultural, comparação, análise, cautela discursiva e contextualização.",
            "Seminário cultural com perguntas abertas e mediação do professor.",
            "Selecionar uma fonte confiável e preparar comentário crítico.",
            "Seminário de 5 minutos com contexto, fonte e cuidado cultural.",
            [
                "Substitua generalizações por formulações contextualizadas.",
                "Inclua perspectiva, período, região e fonte.",
                "Pratique perguntas respeitosas sobre cultura.",
            ],
        ),
        (
            "Módulo 8 — Mediação português-espanhol",
            "Resumir, adaptar e explicar informação brasileira em espanhol natural.",
            "Texto brasileiro curto sobre serviço, notícia ou contexto cultural; adaptação para público hispanofalante.",
            "Paráfrase, equivalência pragmática, falsos cognatos, colocaciones e síntese.",
            "Mediação oral: transformar informação brasileira em explicação clara para estrangeiros.",
            "Preparar glossário de 15 expressões que não podem ser traduzidas literalmente.",
            "Mediação oral gravada + versão escrita adaptada.",
            [
                "Explique \"concurso público\", \"CLT\" ou \"SUS\" sem tradução literal.",
                "Use en otras palabras, es decir, lo esencial es.",
                "Compare precisão, naturalidade e fidelidade de sentido.",
            ],
        ),
        (
            "Módulo 9 — Narrativas sofisticadas e escrita criativa",
            "Contar histórias com estilo, ritmo, perspectiva e uso consciente de tempos verbais.",
            "Crônica curta autoral sobre deslocamento, memória ou encontro cultural.",
            "Estilo indireto livre, conectores narrativos, aspecto verbal, léxico descritivo.",
            "Oficina de reescrita: transformar relato plano em narrativa expressiva.",
            "Escrever crônica de 250 palavras e revisar com pares.",
            "Leitura oral de crônica com feedback de expressão e precisão.",
            [
                "Adicione contexto sensorial sem exagerar.",
                "Varie conectores narrativos.",
                "Controle passado e descrição: ação vs. cenário.",
            ],
        ),
        (
            "Módulo 10 — Fluência oral: mesa-redonda e perguntas difíceis",
            "Sustentar discussão espontânea, fazer perguntas, interromper educadamente e retomar ideias.",
            "Pauta de mesa-redonda com perguntas abertas e papéis discursivos.",
            "Marcadores de interação, retomada, reformulação e fechamento.",
            "Mesa-redonda gravada com rodadas de pergunta, réplica e síntese final.",
            "Preparar 8 expressões para ganhar tempo sem travar.",
            "Participar de mesa-redonda de 20 minutos com avaliação de fluência.",
            [
                "Pratique: permíteme añadir, retomando lo anterior, no quisiera desviarme.",
                "Responda perguntas inesperadas em 45 segundos.",
                "Faça síntese da fala de um colega antes de discordar.",
            ],
        ),
        (
            "Módulo 11 — Trilha de certificação e objetivos específicos",
            "Treinar tarefas de exame ou objetivos profissionais/acadêmicos conforme perfil da turma.",
            "Modelos autorais de tarefas: compreensão, produção escrita, apresentação e interação oral.",
            "Estratégias de prova, gestão de tempo, coesão textual e critérios de avaliação.",
            "Simulado adaptado: produção oral e escrita com feedback de rubrica.",
            "Revisar uma produção própria usando checklist de C1.",
            "Simulado parcial ou projeto profissional em espanhol.",
            [
                "Identifique critério, tempo e objetivo antes de responder.",
                "Planeje texto antes de escrever.",
                "Faça autoavaliação: alcance da tarefa, coesão, precisão, repertório.",
            ],
        ),
        (
            "Módulo 12 — Projeto final: dossiê, apresentação e defesa oral",
            "Integrar pesquisa, mediação, argumentação, escrita e apresentação pública.",
            "Tema escolhido com curadoria: cultura, carreira, sociedade, educação, negócios ou língua.",
            "Revisão B2.2-C1, estilo, precisão, registro, coesão e presença oral.",
            "Banca final: apresentação, perguntas, defesa e feedback individual.",
            "Preparar dossiê, roteiro, slides simples e respostas prováveis.",
            "Dossiê em espanhol + apresentação + defesa oral.",
            [
                "Formule pergunta de pesquisa e tese.",
                "Inclua fonte, contexto e posição crítica.",
                "Prepare respostas para objeções complexas.",
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# Atividade final (10 tarefas abertas por nível) — anexada à lição do
# Projeto Final de cada curso, como registro de avaliação comunicativa
# (não são múltipla escolha, por isso não viram LMS Quiz).
# ---------------------------------------------------------------------------

_BASICO_TAREFAS = [
    "Apresente-se em espanhol com nome, nacionalidade, cidade, profissão/estudo e um objetivo de aprendizagem.",
    "Escreva 5 perguntas para conhecer um colega de turma e responda a pelo menos 3 delas.",
    "Descreva sua rotina de um dia comum, incluindo horários e frequência.",
    "Imagine que você está em uma loja: peça dois produtos, pergunte preço, cor/tamanho e escolha uma opção.",
    "Descreva sua cidade ou bairro com pelo menos 6 frases usando hay, es/son e adjetivos simples.",
    "Explique seus gostos e preferências usando me gusta, me encanta, prefiero, también e tampoco.",
    "Monte um pequeno diálogo de restaurante: chegada, pedido, dúvida sobre o prato e pagamento.",
    "Dê instruções simples para chegar a um lugar: vire, siga, atravesse, fica perto/longe.",
    "Conte uma experiência simples no passado usando ontem, semana passada ou no ano passado.",
    "Fale sobre um plano para a próxima semana usando voy a + infinitivo e justificando com porque.",
]

_INTERMEDIARIO_TAREFAS = [
    "Conte uma experiência de viagem ou trabalho usando passado indefinido e imperfeito de forma clara.",
    "Escreva uma reclamação educada sobre um problema em hotel, compra ou serviço, propondo uma solução.",
    "Redija um e-mail profissional curto com assunto, saudação, objetivo, pedido e fechamento.",
    "Compare dois países, cidades ou culturas usando linguagem respeitosa e evitando estereótipos.",
    "Defenda sua opinião sobre estudar online, usando pelo menos 4 conectores argumentativos.",
    "Explique um plano futuro e o que você fará se uma condição mudar.",
    "Dê conselhos a um colega que está sem constância no estudo de espanhol.",
    "Transforme uma resposta curta em uma resposta mais completa, com justificativa e exemplo.",
    "Resuma um pequeno problema e negocie um acordo com outra pessoa em sala.",
    "Grave ou apresente uma fala de 2 minutos sobre um tema cultural hispânico, com cuidado e contexto.",
]

_AVANCADO_TAREFAS = [
    "Reformule 5 frases muito diretas para versões diplomáticas, sem perder clareza.",
    "Defenda uma tese sobre educação online, apresente um contra-argumento e responda a ele.",
    "Explique a diferença de sentido entre aunque + indicativo e aunque + subjuntivo com exemplos próprios.",
    "Analise um título de notícia: identifique possível viés e reescreva de forma mais neutra.",
    "Simule uma reunião em espanhol para negociar prazo, prioridade e responsabilidade de uma entrega.",
    "Escreva um parágrafo de relatório com objetivo, ação realizada, resultado e próximo passo.",
    "Discuta um tema cultural ou histórico do mundo hispânico com respeito, contexto e sem generalizações.",
    "Faça uma apresentação oral de 3 minutos usando conectores formais e linguagem de transição.",
    "Reescreva uma opinião absoluta em uma opinião matizada, com evidência e limite.",
    "Proponha um projeto intercultural em espanhol, explicando público, objetivo, etapas e impacto esperado.",
]


def _tarefas_extra(tarefas):
    itens = "<br>".join(f"{i}. {t}" for i, t in enumerate(tarefas, start=1))
    return (
        "<b>Atividade final do nível (avaliação comunicativa — 10 tarefas):</b><br>"
        + itens
    )


# ---------------------------------------------------------------------------
# Metadados dos 3 cursos
# ---------------------------------------------------------------------------

COURSES = [
    {
        "slug": "espanhol-basico",
        "title": "Espanhol — Nível Básico (A1-A2)",
        "short_introduction": (
            "Do primeiro hola às conversas essenciais do dia a dia. Turmas pequenas, 100% "
            "ao vivo, para sair do portunhol com segurança."
        ),
        "description": (
            "<p>O curso <strong>Espanhol Básico A1-A2</strong> é o produto de entrada da "
            "Vedium: turmas pequenas (4 a 8 alunos), 100% ao vivo, para quem nunca estudou "
            "espanhol ou tem contato fragmentado com o idioma.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
            "<li>Apresentar-se, cumprimentar e interagir em situações cotidianas</li>"
            "<li>Falar de rotina, preferências, cidade, alimentação e compras</li>"
            "<li>Fazer viagens simples e relatar experiências e habilidades básicas</li>"
            "<li>Reduzir interferências comuns do português (pronúncia, falsos cognatos, tempos verbais)</li>"
            "</ul><p>24 semanas · 48 aulas ao vivo de 60 minutos · 24 práticas guiadas entre aulas.</p>"
        ),
        "price": 297,
        "modules_fn": _basico_modules,
        "tarefas": _BASICO_TAREFAS,
    },
    {
        "slug": "espanhol-intermediario",
        "title": "Espanhol — Nível Intermediário (B1-B2.1)",
        "short_introduction": (
            "Da sobrevivência comunicativa à conversa com opinião, história e nuance. "
            "Para quem já entende espanhol e precisa sustentar conversas de verdade."
        ),
        "description": (
            "<p>O curso <strong>Espanhol Intermediário B1-B2.1</strong> é para quem já se "
            "comunica em situações cotidianas, mas ainda hesita para narrar, opinar e "
            "sustentar conversas mais longas.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
            "<li>Narrar experiências e explicar planos com clareza</li>"
            "<li>Defender opiniões e participar de conversas de trabalho e viagem</li>"
            "<li>Compreender materiais autênticos com apoio moderado</li>"
            "<li>Escrever e-mails, resumos e textos funcionais em espanhol</li>"
            "</ul><p>24 semanas · 48 aulas ao vivo de 60 minutos · 24 práticas guiadas entre aulas.</p>"
        ),
        "price": 397,
        "modules_fn": _intermediario_modules,
        "tarefas": _INTERMEDIARIO_TAREFAS,
    },
    {
        "slug": "espanhol-avancado",
        "title": "Espanhol — Nível Avançado (B2.2-C1)",
        "short_introduction": (
            "Para falar espanhol com precisão, presença e maturidade cultural. Turma "
            "reduzida (3 a 6 alunos) para carreira, cultura e certificação."
        ),
        "description": (
            "<p>O curso <strong>Espanhol Avançado B2.2-C1</strong> é o nível premium da "
            "Vedium: turmas de 3 a 6 alunos, para quem já conversa com autonomia e quer "
            "ganhar precisão, registro e presença profissional/cultural.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
            "<li>Argumentar com nuance, adaptar registro e mediar informações entre português e espanhol</li>"
            "<li>Conduzir reuniões, apresentações e negociações em espanhol</li>"
            "<li>Analisar mídia, cultura e sociedade hispânica com maturidade linguística</li>"
            "<li>Produzir um dossiê final com apresentação e defesa oral</li>"
            "</ul><p>24 semanas · 48 aulas ao vivo de 60 minutos · 24 práticas guiadas entre aulas.</p>"
        ),
        "price": 497,
        "modules_fn": _avancado_modules,
        "tarefas": _AVANCADO_TAREFAS,
    },
]


# ---------------------------------------------------------------------------
# Criação no banco
# ---------------------------------------------------------------------------

def run():
    """Cria os 3 cursos de Espanhol. Idempotente — pula o que já existir."""
    _ensure_category()
    cat_name = frappe.db.get_value("LMS Category", {"category": CATEGORY}, "name")

    for course_data in COURSES:
        _create_course(course_data, cat_name)

    frappe.db.commit()
    print("\n✓ Cursos de Espanhol criados com sucesso.")
    print("  Rode em seguida: vedium_core.scripts.migrations.oneshot.seed_espanhol_quizzes.run")


def _ensure_category():
    if frappe.db.exists("LMS Category", {"category": CATEGORY}):
        return
    frappe.get_doc({"doctype": "LMS Category", "category": CATEGORY}).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  ✓ Categoria '{CATEGORY}' criada.")


def _default_instructor():
    for candidate in ("Administrator", "contato@vediums.com"):
        if frappe.db.exists("User", candidate):
            return candidate
    user = frappe.db.get_value("User", {"enabled": 1, "user_type": "System User"}, "name")
    return user or "Administrator"


def _lesson_content(paragraphs):
    return json.dumps({
        "blocks": [{"type": "paragraph", "data": {"text": p}} for p in paragraphs],
        "version": "2.27.0",
        "time": 1000000000,
    })


def _module_paragraphs(objetivo, entrada, linguagem, aula_vivo, pratica, tarefa, atividades, extra=None):
    paragraphs = [
        f"<b>Objetivo comunicativo:</b> {objetivo}",
        f"<b>Entrada da unidade:</b> {entrada}",
        f"<b>Linguagem ativa:</b> {linguagem}",
        f"<b>Aula ao vivo:</b> {aula_vivo}",
        f"<b>Prática entre aulas:</b> {pratica}",
        f"<b>Tarefa final:</b> {tarefa}",
        "<b>Atividades Vedium:</b><br>" + "<br>".join(f"• {a}" for a in atividades),
        CLOSING_NOTE,
    ]
    if extra:
        paragraphs.append(extra)
    return paragraphs


def _create_course(data, category_name):
    slug = data["slug"]

    existing_name = frappe.db.get_value("LMS Course", {"title": data["title"]}, "name")
    if existing_name and existing_name != slug:
        print(f"  — Encontrado '{existing_name}' → renomeando para '{slug}'...")
        frappe.rename_doc("LMS Course", existing_name, slug, force=True)
        frappe.db.commit()

    if not frappe.db.exists("LMS Course", slug):
        instructor = _default_instructor()
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": data["title"],
            "short_introduction": data["short_introduction"],
            "description": data["description"],
            "paid_course": 1,
            "course_price": data["price"],
            "currency": CURRENCY,
            "published": 1,
            "category": category_name,
            "instructors": [{"instructor": instructor}],
        })
        course.insert(ignore_permissions=True)
        if course.name != slug:
            print(f"    (auto-name '{course.name}' → renomeando para '{slug}')")
            frappe.rename_doc("LMS Course", course.name, slug, force=True)
        frappe.db.commit()
        print(f"\n  ✓ Curso '{slug}' criado (instrutor back-end: {instructor}).")

    existing_chapters = frappe.db.count("Course Chapter", {"course": slug})
    if existing_chapters > 0:
        print(f"  — '{slug}' já tem {existing_chapters} módulo(s), pulando capítulos.")
        return

    modules = data["modules_fn"]()
    last_idx = len(modules) - 1
    for idx, module in enumerate(modules):
        title, objetivo, entrada, linguagem, aula_vivo, pratica, tarefa, atividades = module
        extra = _tarefas_extra(data["tarefas"]) if idx == last_idx else None

        chapter = frappe.get_doc({
            "doctype": "Course Chapter",
            "title": title,
            "course": slug,
        })
        chapter.insert(ignore_permissions=True)

        frappe.get_doc({
            "doctype": "Course Lesson",
            "title": title,
            "chapter": chapter.name,
            "course": slug,
            "content": _lesson_content(
                _module_paragraphs(objetivo, entrada, linguagem, aula_vivo, pratica, tarefa, atividades, extra)
            ),
        }).insert(ignore_permissions=True)

        print(f"    {title}")

    print(f"  ✓ '{slug}': {len(modules)} módulos criados.")

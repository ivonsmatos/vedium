# -*- coding: utf-8 -*-
"""Criação/atualização dos 5 cursos de Hebraico a partir das grades
pedagógicas entregues pela coordenação (docs "Vedium_Hebraico_*_Grade_
Conteudo_Avaliacao", 2026):

    - hebraico-a0-alfabetizacao          (8 módulos, 4 semanas, R$197)
    - hebraico-moderno-a1                (12 unidades, 24 semanas, R$397)  ← já existia como shell
    - hebraico-moderno-a2-b1             (12 unidades, 24 semanas, R$447)
    - hebraico-biblico-leitura-guiada    (12 unidades, 24 semanas, R$497)
    - hebraico-particular                (6 trilhas, 1:1 sob demanda, a partir de R$140/h)

Conteúdo de cada lição = "Objetivo" + "Conteúdo-chave" + "Tarefa/prática ao
vivo" da unidade, no modelo pedagógico Vedium (aula ao vivo, cultura tratada
com respeito e sem promessa religiosa/política — exigência explícita dos docs).

Supersede o antigo create_hebraico_course.py (singular, que só criava o shell
do A1). Este cria os 5 e popula a grade; para o A1 ele encontra o curso
existente, atualiza título/descrição (o A1 deixou de "incluir alfabetização"
porque agora o A0 é um produto separado) e adiciona os módulos.

Executar UMA VEZ no servidor após o deploy:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.create_hebraico_courses.run

Depois, para os quizzes:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.seed_hebraico_quizzes.run
"""

import json

import frappe

CATEGORY = "Hebraico"
CURRENCY = "BRL"

CLOSING_NOTE = (
    "<b>Aula ao vivo (modelo Vedium):</b> entrada humana curta para ativar "
    "repertório, conteúdo-alvo com exemplos originais, prática guiada (leitura, "
    "repetição, pares ou roleplay), produção do aluno com feedback imediato e "
    "tarefa curta entre aulas. Cultura judaica/israelense e textos tratados com "
    "respeito, sem generalização e sem transformar a aula em debate religioso ou "
    "político."
)


# ---------------------------------------------------------------------------
# Grades — cada módulo é (título, objetivo, conteúdo-chave, tarefa/prática)
# ---------------------------------------------------------------------------

def _a0_modules():
    return [
        ("Módulo 1 — O que é o hebraico e como se lê",
         "Entender a direção de leitura e a diferença entre som, letra e transliteração.",
         "Leitura da direita para a esquerda; nomes e sons iniciais.",
         "Leitura guiada de cartões de letras e reconhecimento visual."),
        ("Módulo 2 — Alef-Bet I",
         "Reconhecer as primeiras consoantes e praticar a escrita com apoio.",
         "Alef, Bet/Vet, Guimel, Dalet, He, Vav, Zayin.",
         "Ditado visual: o professor mostra letras e o aluno nomeia."),
        ("Módulo 3 — Alef-Bet II",
         "Completar o conjunto de consoantes e distinguir letras parecidas.",
         "Het, Tet, Yod, Kaf/Khaf, Lamed, Mem, Nun.",
         "Jogo de pares: letra impressa, nome e som."),
        ("Módulo 4 — Alef-Bet III e letras finais",
         "Ler letras finais e entender sua posição na palavra.",
         "Samekh, Ayin, Pe/Fe, Tsade, Qof, Resh, Shin/Sin, Tav; formas finais.",
         "Mini-leitura de palavras curtas com transliteração."),
        ("Módulo 5 — Vogais e sons essenciais",
         "Reconhecer vogais básicas e ler sílabas simples.",
         "A, E, I, O, U em sinais vocálicos; sílaba aberta e fechada.",
         "Leitura em voz alta de sílabas criadas em aula."),
        ("Módulo 6 — Cumprimentos e primeiras frases",
         "Usar frases sociais simples com pronúncia inteligível.",
         "Shalom, toda, bevakasha, slicha, boker tov, erev tov.",
         "Roleplay de chegada à aula ao vivo."),
        ("Módulo 7 — Números e nomes próprios",
         "Ler números básicos, nomes e palavras de alta frequência.",
         "Números 1-10; nomes, família e sala de aula.",
         "Cada aluno lê e soletra o próprio nome em hebraico."),
        ("Módulo 8 — Projeto A0: eu já consigo ler",
         "Integrar leitura, som e primeira comunicação.",
         "Revisão geral do alfabeto, vogais e frases sociais.",
         "Apresentação oral curta + leitura guiada individual."),
    ]


def _a1_modules():
    return [
        ("Unidade 1 — Primeiro encontro em hebraico",
         "Cumprimentar, despedir-se e perguntar como alguém está.",
         "Shalom, ma nishma, toda, bevakasha; pronomes pessoais.",
         "Simulação de primeiro encontro."),
        ("Unidade 2 — Quem sou eu",
         "Apresentar nome, origem, idioma e objetivo de estudo.",
         "Ani..., ata/at..., hu/hi; frases nominais simples.",
         "Apresentação de 30 segundos."),
        ("Unidade 3 — Família e pessoas próximas",
         "Falar de família, relações e pessoas importantes.",
         "Vocabulário de família; masculino/feminino; singular/plural.",
         "Mapa familiar oral simples."),
        ("Unidade 4 — Números, horários e rotina",
         "Dizer números, horários e partes do dia.",
         "Números 0-100; dias, manhã/tarde/noite; rotina básica.",
         "Agenda semanal em hebraico simples."),
        ("Unidade 5 — Cidade, lugares e direção",
         "Perguntar e responder onde fica algo.",
         "Aqui/ali, direita/esquerda, perto/longe; lugares da cidade.",
         "Roleplay: pedir informação."),
        ("Unidade 6 — Comida e pedidos simples",
         "Pedir comida, agradecer e expressar preferência.",
         "Verbos comuns no presente; quero/gosto/tem.",
         "Pedido em café/restaurante."),
        ("Unidade 7 — Compras e valores",
         "Perguntar preço, quantidade e necessidade.",
         "Quanto custa? Eu preciso de...; números e objetos.",
         "Feira simulada."),
        ("Unidade 8 — Casa, objetos e descrição",
         "Descrever objetos, casa e sala de aula.",
         "Adjetivos básicos; concordância; há/não há.",
         "Descrição de foto ou ambiente."),
        ("Unidade 9 — Verbos do cotidiano",
         "Falar de ações frequentes com segurança básica.",
         "Comer, beber, estudar, trabalhar, morar, ir, vir.",
         "Entrevista em pares sobre rotina."),
        ("Unidade 10 — Viagem e deslocamento",
         "Resolver situações de chegada e transporte.",
         "Estação, ônibus, hotel, documento, ajuda.",
         "Chegada ao aeroporto/hotel."),
        ("Unidade 11 — Cultura e comunicação respeitosa",
         "Usar fórmulas de cortesia e reconhecer variações culturais.",
         "Pedidos educados, desculpas, agradecimento, títulos sociais.",
         "Cena de atendimento formal/informal."),
        ("Unidade 12 — Projeto A1: minha vida em hebraico simples",
         "Integrar leitura, fala, vocabulário e interação.",
         "Revisão geral do A1.",
         "Apresentação oral + perguntas da turma."),
    ]


def _a2b1_modules():
    return [
        ("Unidade 1 — Retomada e nivelamento",
         "Revisar o A1 e diagnosticar lacunas de leitura, fala e vocabulário.",
         "Pronomes, frases nominais, presente e vocabulário básico.",
         "Entrevista de nivelamento em duplas."),
        ("Unidade 2 — Narrar o passado",
         "Contar experiências simples e eventos recentes.",
         "Passado de verbos frequentes; marcadores temporais.",
         "Relato: uma viagem, uma semana ou uma memória."),
        ("Unidade 3 — Falar do futuro e planos",
         "Expressar intenção, planos e próximos passos.",
         "Futuro/estrutura de intenção; amanhã, semana que vem, depois.",
         "Planejamento de viagem/estudo."),
        ("Unidade 4 — Opinião e preferência",
         "Concordar, discordar e justificar de modo simples.",
         "Acho que, prefiro, porque, mas, também.",
         "Debate leve: cidade, comida, rotina, estudo."),
        ("Unidade 5 — Serviços e problemas",
         "Resolver problemas de atendimento, saúde, transporte e compras.",
         "Vocabulário funcional; pedidos e reclamações educadas.",
         "Roleplay de problema real."),
        ("Unidade 6 — Leitura de textos curtos",
         "Extrair informação de mensagens, avisos e pequenos textos.",
         "Estratégias de leitura; cognatos, contexto e palavras-chave.",
         "Leitura guiada de aviso, e-mail ou mensagem."),
        ("Unidade 7 — Trabalho e estudos",
         "Falar de profissão, tarefas e rotina acadêmica/profissional.",
         "Vocabulário de trabalho, estudos e competências.",
         "Miniapresentação profissional."),
        ("Unidade 8 — Narrativa cultural",
         "Comentar música, comida, festa ou hábito cultural com respeito.",
         "Conectores narrativos; passado + opinião.",
         "Relato cultural breve."),
        ("Unidade 9 — Conversa social mais longa",
         "Manter conversa por mais de 3 minutos.",
         "Perguntas de acompanhamento, reformulação e confirmação.",
         "Conversa gravada com feedback."),
        ("Unidade 10 — Texto escrito funcional",
         "Escrever mensagem, e-mail curto e relato simples.",
         "Saudações, fechamento, coesão básica, revisão.",
         "E-mail para professor, colega ou serviço."),
        ("Unidade 11 — Preparação do projeto final",
         "Planejar produção oral/escrita integrada.",
         "Revisão de passado, futuro, opinião, vocabulário ativo.",
         "Roteiro individual com feedback."),
        ("Unidade 12 — Projeto A2/B1: comunicação real",
         "Apresentar, interagir e responder perguntas com autonomia básica.",
         "Revisão integrada.",
         "Apresentação + perguntas + autoavaliação."),
    ]


def _biblico_modules():
    return [
        ("Unidade 1 — Entrada no texto hebraico bíblico",
         "Entender o escopo: ler com base linguística, sem prometer interpretação religiosa.",
         "Alfabeto, direção de leitura e sinais básicos.",
         "Leitura guiada de palavras isoladas."),
        ("Unidade 2 — Vogais, sílabas e acentuação",
         "Ler com apoio de vogais e reconhecer sílabas.",
         "Vogais, sheva, dagesh, sílaba aberta/fechada.",
         "Marcação de sílabas em palavras selecionadas."),
        ("Unidade 3 — Substantivos e gênero",
         "Identificar substantivos, gênero e número.",
         "Masculino/feminino, singular/plural, formas frequentes.",
         "Análise morfológica simples."),
        ("Unidade 4 — Artigo e preposições",
         "Ler estruturas com artigo e preposições inseparáveis.",
         "Artigo definido; em/de/para/com; vav conjuntivo.",
         "Leitura de pequenas sequências."),
        ("Unidade 5 — Pronomes e adjetivos",
         "Reconhecer pronomes e adjetivos em frases curtas.",
         "Pronomes pessoais/demonstrativos; concordância de adjetivos.",
         "Tradução orientada de frases curtas."),
        ("Unidade 6 — Relação de construto",
         "Entender posse e ligação entre substantivos.",
         "Construto singular/plural; cadeia nominal.",
         "Montagem de cadeias: casa do rei, palavra de Deus etc."),
        ("Unidade 7 — Sufixos pronominais",
         "Identificar sufixos em substantivos e preposições.",
         "Meu/teu/seu; sufixos frequentes; análise por partes.",
         "Separar radical + sufixo + função."),
        ("Unidade 8 — Verbo Qal: completo",
         "Reconhecer ações completas no Qal.",
         "Raiz triconsonantal; perfeito/completo; pessoa, gênero, número.",
         "Análise de verbos frequentes."),
        ("Unidade 9 — Verbo Qal: incompleto e formas simples",
         "Reconhecer ação incompleta/futura e leitura contextual.",
         "Imperfeito/incompleto; infinitivo/particípio em nível introdutório.",
         "Comparar formas verbais."),
        ("Unidade 10 — Leitura guiada I: narrativa",
         "Ler narrativa curta com apoio de léxico e glossário.",
         "Estratégia: identificar verbo, sujeito, complemento e conectores.",
         "Leitura comentada de excerto selecionado pelo professor."),
        ("Unidade 11 — Leitura guiada II: poesia e oração",
         "Perceber paralelismo, repetição e vocabulário teológico.",
         "Poesia hebraica, palavras-chave, limites de tradução.",
         "Leitura comentada de salmo/poesia selecionada."),
        ("Unidade 12 — Projeto final: leitura responsável",
         "Apresentar análise linguística básica de uma passagem curta.",
         "Revisão geral: forma, função, vocabulário e tradução própria comentada.",
         "Apresentação oral com quadro de análise."),
    ]


def _particular_modules():
    return [
        ("Módulo 1 — Diagnóstico e plano individual",
         "Mapear o objetivo: moderno, bíblico, viagem, família, leitura ou acadêmico.",
         "Entrevista, teste breve, meta mensurável e cronograma.",
         "Plano de 8, 12 ou 24 encontros."),
        ("Módulo 2 — Trilha A: Alfabetização acelerada",
         "Para quem precisa ler letras e sons rapidamente.",
         "Alef-Bet, vogais, leitura guiada, nomes próprios.",
         "Leitura individual com correção."),
        ("Módulo 3 — Trilha B: Hebraico moderno funcional",
         "Para comunicação cotidiana, viagem, família ou Israel.",
         "Cumprimentos, pronomes, números, rotina, serviços.",
         "Roleplays personalizados."),
        ("Módulo 4 — Trilha C: Hebraico bíblico",
         "Para leitura orientada de textos e uso de ferramentas.",
         "Morfologia básica, vocabulário, léxico, leitura interlinear.",
         "Análise de passagem curta."),
        ("Módulo 5 — Trilha D: objetivo específico",
         "Preparar o aluno para uma necessidade concreta.",
         "Viagem, cerimônia, pesquisa, família, entrevista, projeto cultural.",
         "Simulações e entregáveis reais."),
        ("Módulo 6 — Ciclo de feedback",
         "Medir progresso e ajustar a rota a cada 4 aulas.",
         "Registro de erros recorrentes, repertório ativo e autonomia.",
         "Plano de continuidade."),
    ]


# ---------------------------------------------------------------------------
# Metadados dos 5 cursos
# ---------------------------------------------------------------------------

COURSES = [
    {
        "slug": "hebraico-a0-alfabetizacao",
        "title": "Hebraico A0 — Alfabetização",
        "short_introduction": (
            "Ler as letras, reconhecer sons e dar o primeiro passo com confiança. "
            "4 semanas, ao vivo, para quem nunca leu o alfabeto hebraico."
        ),
        "description": (
            "<p>O <strong>Hebraico A0 — Alfabetização</strong> é o curso de entrada "
            "para quem nunca leu o alfabeto hebraico. A meta não é fluência: é criar "
            "segurança para reconhecer letras, sons, vogais básicas, direção de "
            "leitura e frases sociais simples.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
            "<li>Ler letras e sílabas simples e reconhecer as formas finais</li>"
            "<li>Usar cumprimentos básicos com pronúncia inteligível</li>"
            "<li>Compreender como continuar no A1 ou na leitura bíblica</li>"
            "</ul><p>4 semanas · 8 aulas ao vivo de 60 minutos · turma de 4 a 8 alunos. "
            "Pode ser feito avulso ou como bônus para quem já é matriculado.</p>"
        ),
        "price": 197,
        "modules_fn": _a0_modules,
    },
    {
        "slug": "hebraico-moderno-a1",
        "title": "Hebraico Moderno — Nível A1",
        "short_introduction": (
            "Sair do zero com leitura inicial, pronúncia e frases de uso real. "
            "Comunicação moderna do dia a dia, ao vivo e em turma pequena."
        ),
        "description": (
            "<p>O <strong>Hebraico Moderno A1</strong> é a trilha inicial de "
            "comunicação. O aluno aprende a se apresentar, perguntar, agradecer e "
            "falar de rotina, família, cidade, comida, compras e viagem simples.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
            "<li>Interagir em situações simples do dia a dia</li>"
            "<li>Ler palavras e frases curtas e construir vocabulário ativo</li>"
            "<li>Se apresentar e sustentar uma conversa básica</li>"
            "</ul><p>24 semanas · 48 aulas ao vivo de 60 minutos · turma de 4 a 8 alunos. "
            "Indicado para quem concluiu o A0 (Alfabetização) ou já reconhece o alfabeto "
            "hebraico.</p>"
        ),
        "price": 397,
        "modules_fn": _a1_modules,
    },
    {
        "slug": "hebraico-moderno-a2-b1",
        "title": "Hebraico Moderno — Nível A2/B1",
        "short_introduction": (
            "Ampliar vocabulário, leitura e conversação. Narrar experiências, falar "
            "de planos e sustentar conversas mais longas com autonomia básica."
        ),
        "description": (
            "<p>O <strong>Hebraico Moderno A2/B1</strong> é a continuidade da primeira "
            "turma. O foco é ampliar a autonomia: narrar experiências, falar de planos, "
            "resolver problemas, ler mensagens curtas e sustentar conversas mais longas.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
            "<li>Manter conversa social simples e contar experiências</li>"
            "<li>Escrever mensagens curtas e compreender textos funcionais</li>"
            "<li>Expressar opinião com justificativa e resolver situações de serviço</li>"
            "</ul><p>24 semanas · 48 aulas ao vivo de 60 minutos · abertura sob demanda. "
            "Indicado para quem concluiu o A1 ou passou por nivelamento equivalente.</p>"
        ),
        "price": 447,
        "modules_fn": _a2b1_modules,
    },
    {
        "slug": "hebraico-biblico-leitura-guiada",
        "title": "Hebraico Bíblico — Leitura Guiada",
        "short_introduction": (
            "Ler textos selecionados com base linguística e contexto. Trilha de "
            "leitura responsável para público acadêmico, cultural ou religioso."
        ),
        "description": (
            "<p>O <strong>Hebraico Bíblico — Leitura Guiada</strong> é uma trilha "
            "separada, de leitura linguística responsável: alfabetização de apoio, "
            "gramática essencial, vocabulário e análise guiada de passagens curtas. "
            "O foco é a língua e o texto — sem prometer interpretação religiosa nem "
            "transformar a aula em debate.</p>"
            "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
            "<li>Identificar formas básicas (substantivos, verbos no Qal, construto, sufixos)</li>"
            "<li>Consultar léxico e ler passagens curtas com apoio</li>"
            "<li>Explicar decisões de tradução com base linguística</li>"
            "</ul><p>24 semanas · 48 aulas ao vivo de 60 minutos · turma separada. "
            "Aberto a público acadêmico, cultural ou religioso, com ou sem objetivo "
            "religioso.</p>"
        ),
        "price": 497,
        "modules_fn": _biblico_modules,
    },
    {
        "slug": "hebraico-particular",
        "title": "Hebraico Particular",
        "short_introduction": (
            "Aulas 1:1 sob demanda, com plano personalizado. Pacotes de 8, 12 ou 24 "
            "encontros para objetivos específicos. A partir de R$ 140/h (sob consulta)."
        ),
        "description": (
            "<p>O <strong>Hebraico Particular</strong> é a oferta individual (1:1) para "
            "objetivos específicos: alfabetização acelerada, viagem, família, leitura "
            "bíblica, estudo acadêmico, cerimônia, pesquisa ou continuidade fora da turma.</p>"
            "<p><strong>Como funciona:</strong></p><ul>"
            "<li>Diagnóstico inicial e plano individual com meta mensurável</li>"
            "<li>Pacotes de 8, 12 ou 24 encontros (mínimo recomendado: 8)</li>"
            "<li>Entregável final personalizado + relatório de progresso</li>"
            "</ul><p>Valor de referência: R$ 140 a R$ 220/hora, conforme objetivo e "
            "carga — <strong>o valor final é combinado com a equipe</strong> (fale no "
            "WhatsApp ou pela página de contato antes de fechar o pacote).</p>"
        ),
        "price": 140,
        "modules_fn": _particular_modules,
    },
]


# ---------------------------------------------------------------------------
# Criação no banco (mesmo padrão validado no PLE/Espanhol)
# ---------------------------------------------------------------------------

def run():
    _ensure_category()
    cat_name = frappe.db.get_value("LMS Category", {"category": CATEGORY}, "name")

    for course_data in COURSES:
        _create_course(course_data, cat_name)

    frappe.db.commit()
    print("\n✓ Cursos de Hebraico criados/atualizados.")
    print("  Rode em seguida: vedium_core.scripts.migrations.oneshot.seed_hebraico_quizzes.run")


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


def _module_paragraphs(objetivo, conteudo, tarefa):
    return [
        f"<b>Objetivo:</b> {objetivo}",
        f"<b>Conteúdo-chave:</b> {conteudo}",
        f"<b>Tarefa / prática ao vivo:</b> {tarefa}",
        CLOSING_NOTE,
    ]


def _create_course(data, category_name):
    slug = data["slug"]

    # Se já existe com outro título (ex.: o shell antigo do A1), renomeia o slug
    existing_name = frappe.db.get_value("LMS Course", {"title": data["title"]}, "name")
    if existing_name and existing_name != slug:
        print(f"  — Encontrado '{existing_name}' → renomeando para '{slug}'...")
        frappe.rename_doc("LMS Course", existing_name, slug, force=True)
        frappe.db.commit()

    instructor = _default_instructor()

    if not frappe.db.exists("LMS Course", slug):
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
    else:
        # Curso já existe (ex.: shell do A1) — reconcilia título/descrição/preço.
        frappe.db.set_value("LMS Course", slug, {
            "title": data["title"],
            "short_introduction": data["short_introduction"],
            "description": data["description"],
            "course_price": data["price"],
            "paid_course": 1,
            "currency": CURRENCY,
            "category": category_name,
            "published": 1,
        })
        frappe.db.commit()
        print(f"\n  ✓ Curso '{slug}' já existia — título/descrição/preço reconciliados.")

    existing_chapters = frappe.db.count("Course Chapter", {"course": slug})
    if existing_chapters > 0:
        print(f"  — '{slug}' já tem {existing_chapters} módulo(s), pulando capítulos.")
        return

    modules = data["modules_fn"]()
    for title, objetivo, conteudo, tarefa in modules:
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
            "content": _lesson_content(_module_paragraphs(objetivo, conteudo, tarefa)),
        }).insert(ignore_permissions=True)

        print(f"    {title}")

    print(f"  ✓ '{slug}': {len(modules)} módulos criados.")

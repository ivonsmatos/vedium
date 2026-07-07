# -*- coding: utf-8 -*-
"""
Vedium — Atividades, exercícios de fixação e prova final do PLE Básico

Conteúdo 100% original (não copiado de nenhum material de terceiros),
escrito seguindo o escopo típico de um curso A1/A2 de Português para
Estrangeiros: saudações, apresentação pessoal, rotina diária, comida,
compras, clima e direções -- os mesmos temas já usados nos títulos de
lição de create_ple_courses.py.

Cria, de forma idempotente:
    - 3 quizzes de fixação (1 por módulo), ~10 questões cada, sem gate
      (max_attempts=0 = ilimitado, é treino, não avaliação).
    - 1 prova final (LMS Quiz do curso), banco de 80 questões,
      limit_questions_to=40, shuffle_questions=1, max_attempts=3,
      passing_percentage=70.

Rodar (idempotente -- pode rodar de novo sem duplicar):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.seed_ple_basico_activities.run
"""
import frappe

COURSE = "portugues-para-estrangeiros-basico"

# ---------------------------------------------------------------------------
# Banco de questões da PROVA FINAL (80 questões, sorteia 40 por tentativa)
# ---------------------------------------------------------------------------

EXAM_QUESTIONS = [
    # Módulo 1 — Primeiros contatos, ser/estar, artigos, presente do indicativo
    ("Complete: \"Bom dia! Como ___ o senhor?\"", ["vai", "vou", "vamos", "vão"], 0),
    ("Complete: \"Eu ___ de São Paulo.\"", ["sou", "estou", "é", "são"], 0),
    ("Qual verbo indica localização temporária? \"Ela ___ em Belo Horizonte agora.\"", ["está", "é", "são", "somos"], 0),
    ("\"Muito prazer\" é uma resposta a:", ["uma apresentação", "uma despedida", "um pedido de desculpas", "um convite"], 0),
    ("Complete: \"___ é seu nome?\"", ["Qual", "Quem", "Onde", "Quando"], 0),
    ("Escolha o artigo correto: \"___ casa é grande.\"", ["A", "O", "Os", "As"], 0),
    ("Complete: \"Nós ___ estudantes de português.\"", ["somos", "é", "está", "sou"], 0),
    ("\"Tchau\" e \"Até logo\" são exemplos de:", ["despedidas", "saudações", "profissões", "nacionalidades"], 0),
    ("Complete com a preposição correta: \"Ele mora ___ Brasil.\"", ["no", "na", "em", "de"], 0),
    ("Qual é o plural de \"professor\"?", ["professores", "professors", "professora", "professeres"], 0),
    ("Complete: \"Você ___ brasileiro?\"", ["é", "és", "sou", "somos"], 0),
    ("\"Eu trabalho em uma empresa de informática\" -- o verbo \"trabalhar\" está no:", ["presente do indicativo", "pretérito perfeito", "futuro", "imperativo"], 0),
    ("Complete: \"O senhor mora ___ ou trabalha aqui?\"", ["aqui", "aquilo", "isso", "aquele"], 0),
    ("Escolha a nacionalidade correta para alguém do Chile:", ["chileno", "chilena", "chilenas", "todas as anteriores, dependendo do gênero"], 3),
    ("Complete: \"Estes ___ Rui e Carlos.\"", ["são", "é", "está", "somos"], 0),
    ("\"Sobrenome\" significa:", ["o último nome de uma pessoa", "o primeiro nome", "a idade", "a profissão"], 0),
    ("Complete: \"Ela ___ engenheira.\"", ["é", "está", "são", "somos"], 0),
    ("Qual pergunta pede a profissão de alguém?", ["O que você faz?", "Onde você mora?", "Quantos anos você tem?", "Como você se chama?"], 0),
    ("Complete: \"Eles ___ de Portugal.\"", ["são", "é", "está", "sou"], 0),
    ("\"Igualmente\" é uma resposta educada a:", ["\"Muito prazer\"", "\"Bom dia\"", "\"Como vai?\"", "\"Tchau\""], 0),
    # Módulo 1 — localizar pessoas/objetos, verbos ser/estar, preposições, transporte
    ("Complete: \"O livro ___ em cima da mesa.\"", ["está", "é", "são", "estão"], 0),
    ("Qual preposição indica posição \"dentro de\"?", ["dentro de", "em cima de", "atrás de", "ao lado de"], 0),
    ("Complete: \"Nós vamos ___ ônibus.\"", ["de", "em", "no", "com"], 0),
    ("\"Que lugar maravilhoso!\" expressa:", ["admiração", "tristeza", "dúvida", "raiva"], 0),
    ("Complete: \"A farmácia fica ___ da padaria.\"", ["ao lado", "dentro", "sobre", "sob"], 0),
    ("Qual é o meio de transporte mais rápido para uma viagem longa?", ["avião", "bicicleta", "a pé", "carroça"], 0),
    ("Complete: \"Eu vou trabalhar ___ trem.\"", ["de", "em", "no", "por"], 0),
    ("\"Onde fica o hotel?\" é uma pergunta sobre:", ["localização", "tempo", "quantidade", "cor"], 0),
    ("Complete: \"Os alunos ___ na sala de aula.\"", ["estão", "são", "está", "é"], 0),
    ("Qual verbo completa: \"O museu ___ perto da praça.\"?", ["fica", "vai", "sai", "faz"], 0),
    # Módulo 2 — família, adjetivos, possessivos, rotina, advérbios de frequência
    ("Complete: \"Este é meu ___, ele se chama Pedro.\"", ["irmão", "irmã", "irmãos", "irmãs"], 0),
    ("Qual adjetivo descreve uma pessoa alta?", ["alto/alta", "baixo/baixa", "gordo/gorda", "magro/magra"], 0),
    ("Complete: \"___ carro é novo.\" (referindo-se a você)", ["Meu", "Minha", "Meus", "Minhas"], 0),
    ("\"Todo santo dia\" significa:", ["todos os dias", "nunca", "às vezes", "só hoje"], 0),
    ("Complete: \"Eu ___ às sete horas.\" (acordar)", ["acordo", "acorda", "acordamos", "acordam"], 0),
    ("Qual advérbio indica frequência baixa?", ["raramente", "sempre", "todo dia", "constantemente"], 0),
    ("Complete: \"Ela se ___ e depois toma café.\" (verbo reflexivo)", ["levanta", "levanto", "levantam", "levantamos"], 0),
    ("\"Sua prima é um gato!\" é uma expressão que significa:", ["ela é muito bonita", "ela tem um gato", "ela gosta de animais", "ela é engraçada"], 0),
    ("Complete: \"Nossos ___ moram no Rio.\" (avós)", ["avós", "avô", "avó", "avozinho"], 0),
    ("Qual é o feminino de \"simpático\"?", ["simpática", "simpatica", "simpático", "simpatico"], 0),
    # Módulo 2 — comida, imperativo, restaurante
    ("Complete no imperativo: \"___ a porta, por favor.\" (fechar)", ["Feche", "Fechar", "Fechando", "Fechou"], 0),
    ("Qual expressão se usa para pedir a conta no restaurante?", ["A conta, por favor.", "Bom apetite!", "Que pena!", "De nada."], 0),
    ("Complete: \"Eu queria ___ um suco de laranja.\"", ["pedir", "pede", "pedi", "pedindo"], 0),
    ("\"Que comidinha boa!\" expressa:", ["satisfação com a comida", "insatisfação", "surpresa negativa", "indiferença"], 0),
    ("Complete no imperativo: \"___ a mesa, por favor.\" (limpar, formal)", ["Limpe", "Limpar", "Limpando", "Limpou"], 0),
    ("Qual é o prato típico brasileiro feito com feijão preto e carne?", ["feijoada", "moqueca", "brigadeiro", "coxinha"], 0),
    ("Complete: \"Vamos ___ compras no mercado.\"", ["fazer", "faz", "fazendo", "fizemos"], 0),
    ("\"Quanto custa?\" é uma pergunta sobre:", ["preço", "sabor", "quantidade de calorias", "cor"], 0),
    ("Complete: \"Este restaurante serve comida ___.\" (vegetariana)", ["vegetariana", "vegetariano", "vegetarianos", "vegetarianas"], 0),
    ("Qual verbo completa: \"O garçom ___ o cardápio.\"?", ["traz", "trago", "trazem", "trouxemos"], 0),
    # Módulo 3 — clima, gerúndio, presente irregular
    ("Complete: \"O verão ___ chegando.\" (estar + gerúndio)", ["está", "é", "são", "somos"], 0),
    ("Qual estação vem depois do inverno?", ["primavera", "verão", "outono", "não existe ordem fixa"], 0),
    ("Complete: \"Eu ___ um convite para a festa.\" (fazer, presente irregular)", ["faço", "faz", "fazem", "fazemos"], 0),
    ("\"Está chovendo\" descreve:", ["o clima no momento", "uma lembrança do passado", "um plano futuro", "uma opinião"], 0),
    ("Complete: \"Nós ___ para a praia amanhã.\" (ir)", ["vamos", "vai", "vou", "vão"], 0),
    ("Qual verbo é irregular no presente: \"eu ___ (poder) te ajudar\"?", ["posso", "podo", "pode", "podemos"], 0),
    ("Complete: \"Está fazendo muito ___ hoje.\" (calor)", ["calor", "frio", "vento", "sol"], 0),
    ("\"Convidar alguém para sair\" é um exemplo de:", ["convite", "despedida", "reclamação", "pedido de desculpas"], 0),
    ("Complete: \"Eles ___ chegando atrasados.\" (estar + gerúndio)", ["estão", "está", "é", "são"], 0),
    ("Qual expressão se usa para aceitar um convite?", ["Vou adorar ir!", "Não, obrigado, nunca.", "Talvez, quem sabe daqui a 10 anos.", "Isso não é possível."], 0),
    # Módulo 3 — compras, comparativos, demonstrativos, roupas
    ("Complete: \"Esta camisa é mais cara ___ aquela.\"", ["do que", "que", "como", "igual"], 0),
    ("Qual demonstrativo se refere a algo perto de quem fala?", ["este/esta", "esse/essa", "aquele/aquela", "nenhum dos anteriores"], 0),
    ("Complete: \"Estas calças são tão boas ___ as outras.\"", ["quanto", "que", "como", "do que"], 0),
    ("\"Pechinchar\" significa:", ["negociar o preço", "pagar mais caro de propósito", "comprar sem olhar o preço", "devolver um produto"], 0),
    ("Complete: \"Aquela loja tem os melhores preços.\" -- \"aquela\" indica algo:", ["distante de quem fala e ouve", "perto de quem fala", "perto de quem ouve", "não indica distância"], 0),
    ("Qual peça de roupa se usa nos pés?", ["sapato", "chapéu", "cinto", "luva"], 0),
    ("Complete: \"Este vestido é ___ bonito quanto o outro.\"", ["tão", "mais", "menos", "do que"], 0),
    ("\"Vire à esquerda\" é um exemplo de:", ["instrução de direção", "cumprimento", "despedida", "pedido de comida"], 0),
    ("Complete: \"Siga em frente e ___ à direita na praça.\"", ["vire", "virar", "virando", "virou"], 0),
    ("Qual pergunta se faz para pedir direções?", ["Como chego até a estação?", "Quanto custa isso?", "Qual é o seu nome?", "Que horas são?"], 0),
    # Reforço geral: vocabulário e gramática A1/A2 misto
    ("Complete: \"Muito obrigado(a)\" é uma expressão de:", ["agradecimento", "pedido", "despedida", "dúvida"], 0),
    ("Qual é o oposto de \"grande\"?", ["pequeno", "alto", "largo", "comprido"], 0),
    ("Complete: \"Eu não ___ português muito bem ainda.\" (falar)", ["falo", "fala", "falam", "falamos"], 0),
    ("\"De nada\" é resposta a:", ["\"Obrigado(a)\"", "\"Com licença\"", "\"Desculpa\"", "\"Tchau\""], 0),
    ("Complete: \"Ela tem 25 ___.\" (idade)", ["anos", "meses", "dias", "horas"], 0),
    ("Qual pronome possessivo corresponde a \"dele\"?", ["seu/sua", "meu/minha", "nosso/nossa", "teu/tua"], 0),
    ("Complete: \"Nós moramos ___ Rua das Flores.\"", ["na", "no", "em", "de"], 0),
    ("\"Com licença\" se usa para:", ["pedir passagem ou interromper", "cumprimentar de manhã", "agradecer", "se despedir"], 0),
    ("Complete: \"Vocês ___ de onde?\" (ser)", ["são", "é", "está", "somos"], 0),
    ("Qual é o feminino de \"professor\"?", ["professora", "professor", "professoro", "professara"], 0),
]

# ---------------------------------------------------------------------------
# Exercícios de FIXAÇÃO por módulo (~10 questões cada, sem gate, prática livre)
# ---------------------------------------------------------------------------

MODULE_FIXATION = {
    "Módulo 1 — Primeiros Contatos e Informações Pessoais": [
        ("Complete: \"Bom dia! Tudo ___?\"", ["bem", "bom", "boa", "bons"], 0),
        ("Complete: \"Eu ___ estudante.\" (ser)", ["sou", "é", "somos", "são"], 0),
        ("Qual pergunta pede o nome de alguém?", ["Qual é o seu nome?", "Onde você mora?", "Quantos anos você tem?", "O que você faz?"], 0),
        ("Complete: \"Ele ___ de férias esta semana.\" (estar)", ["está", "é", "são", "somos"], 0),
        ("\"Prazer em conhecê-lo(a)\" é usado quando:", ["conhecemos alguém pela primeira vez", "nos despedimos", "agradecemos", "pedimos desculpas"], 0),
        ("Complete: \"Nós ___ de Portugal.\" (ser)", ["somos", "é", "está", "sou"], 0),
        ("Qual é o artigo definido feminino plural?", ["as", "os", "a", "o"], 0),
        ("Complete: \"Ela mora ___ Lisboa.\"", ["em", "no", "na", "de"], 0),
        ("\"Como vai o senhor?\" é uma forma:", ["formal de perguntar como alguém está", "informal de se despedir", "de pedir informação pessoal", "de agradecer"], 0),
        ("Complete: \"Eu trabalho ___ uma escola.\" (em)", ["em", "no", "na", "de"], 0),
    ],
    "Módulo 2 — O Dia a Dia e o Ambiente": [
        ("Complete: \"Meu ___ mora no Brasil.\" (irmão)", ["irmão", "irmã", "irmãos", "irmãs"], 0),
        ("Qual advérbio de frequência significa \"quase nunca\"?", ["raramente", "sempre", "frequentemente", "diariamente"], 0),
        ("Complete: \"Eu me ___ às 6h.\" (levantar)", ["levanto", "levanta", "levantam", "levantamos"], 0),
        ("Qual é o oposto de \"alto\"?", ["baixo", "gordo", "magro", "forte"], 0),
        ("Complete: \"Vamos ___ compras hoje.\" (fazer)", ["fazer", "faz", "fazendo", "fez"], 0),
        ("\"Que comidinha boa!\" expressa:", ["satisfação", "tristeza", "raiva", "medo"], 0),
        ("Complete no imperativo: \"___ aqui, por favor.\" (sentar, formal)", ["Sente-se", "Sentar", "Sentando", "Sentou"], 0),
        ("Qual pergunta se faz para saber o preço?", ["Quanto custa?", "Onde fica?", "Que horas são?", "Como se chama?"], 0),
        ("Complete: \"Ela ___ toda manhã.\" (correr)", ["corre", "correm", "corro", "corremos"], 0),
        ("\"Pedir a conta\" acontece em qual lugar?", ["restaurante", "escola", "hospital", "banco"], 0),
    ],
    "Módulo 3 — Interações e Cultura Brasileira": [
        ("Complete: \"O verão está ___.\" (chegar, gerúndio)", ["chegando", "chegado", "chega", "chegou"], 0),
        ("Qual verbo é irregular: \"eu ___ fazer isso amanhã\"?", ["posso", "podo", "pode", "podemos"], 0),
        ("Complete: \"Esta blusa é ___ cara que aquela.\"", ["mais", "tão", "menos que", "como"], 0),
        ("\"Pechinchar\" significa:", ["negociar preço", "pagar caro", "não comprar nada", "devolver a compra"], 0),
        ("Complete: \"Vire à ___ e siga em frente.\"", ["esquerda", "esquerdo", "esquerdas", "esquerdos"], 0),
        ("Qual demonstrativo indica algo perto de quem ouve?", ["esse/essa", "este/esta", "aquele/aquela", "nenhum"], 0),
        ("Complete: \"Está fazendo muito ___ hoje.\" (frio/calor)", ["frio", "chuva", "nublado", "vento forte demais para sair"], 0),
        ("\"Aceitar um convite\" é dizer:", ["\"Vou adorar ir!\"", "\"Não gosto de festas.\"", "\"Isso é impossível.\"", "\"Não sei o que é isso.\""], 0),
        ("Complete: \"A farmácia fica ___ do banco.\"", ["ao lado", "dentro", "sobre", "sob"], 0),
        ("Qual pergunta pede uma direção?", ["Como chego até a praça?", "Qual é o seu nome?", "Quantos anos você tem?", "Do que você gosta?"], 0),
    ],
}

# ---------------------------------------------------------------------------
# Criação no banco
# ---------------------------------------------------------------------------


def _make_question(question_text, options, correct_idx):
    """Cria (ou reaproveita) uma LMS Question de múltipla escolha, 4
    alternativas, uma correta. Idempotente por texto da pergunta."""
    existing = frappe.db.get_value("LMS Question", {"question": question_text})
    if existing:
        return existing

    doc = frappe.get_doc({
        "doctype": "LMS Question",
        "question": question_text,
        "type": "Choices",
        "multiple": 0,
    })
    for i, option_text in enumerate(options, start=1):
        doc.set(f"option_{i}", option_text)
        doc.set(f"is_correct_{i}", 1 if i - 1 == correct_idx else 0)
    doc.insert(ignore_permissions=True)
    return doc.name


def _make_quiz(title, course, lesson, questions, *, max_attempts, passing_percentage,
               shuffle_questions, limit_questions_to, total_marks):
    if frappe.db.exists("LMS Quiz", {"title": title}):
        print(f"  — Quiz '{title}' já existe, pulando.")
        return

    quiz = frappe.get_doc({
        "doctype": "LMS Quiz",
        "title": title,
        "course": course,
        "lesson": lesson,
        "max_attempts": max_attempts,
        "passing_percentage": passing_percentage,
        "shuffle_questions": 1 if shuffle_questions else 0,
        "limit_questions_to": limit_questions_to,
        "total_marks": total_marks,
    })
    for question_text, options, correct_idx in questions:
        q_name = _make_question(question_text, options, correct_idx)
        quiz.append("questions", {"question": q_name, "marks": 1})
    quiz.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  ✓ Quiz '{title}' criado ({len(questions)} questões no banco).")


def run():
    if not frappe.db.exists("LMS Course", COURSE):
        print(f"Curso '{COURSE}' não existe -- rode create_ple_courses.run primeiro.")
        return

    # Prova final -- banco de 80, sorteia 40, 70% pra passar, 3 tentativas,
    # ordem embaralhada a cada tentativa.
    _make_quiz(
        title="Prova Final — Português Básico (PLE)",
        course=COURSE,
        lesson=None,
        questions=EXAM_QUESTIONS,
        max_attempts=3,
        passing_percentage=70,
        shuffle_questions=True,
        limit_questions_to=40,
        total_marks=40,
    )

    # Exercícios de fixação por módulo -- prática livre, sem limite de
    # tentativas (max_attempts=0), vinculados à última lição do módulo.
    for chapter_title, questions in MODULE_FIXATION.items():
        chapter_name = frappe.db.get_value(
            "Course Chapter", {"course": COURSE, "title": chapter_title}
        )
        if not chapter_name:
            print(f"  AVISO: capítulo '{chapter_title}' não encontrado, pulando fixação.")
            continue
        last_lesson = frappe.db.get_value(
            "Course Lesson", {"chapter": chapter_name}, "name", order_by="idx desc"
        )
        _make_quiz(
            title=f"Exercícios de Fixação — {chapter_title}",
            course=COURSE,
            lesson=last_lesson,
            questions=questions,
            max_attempts=0,
            passing_percentage=70,
            shuffle_questions=True,
            limit_questions_to=0,
            total_marks=len(questions),
        )

    frappe.db.commit()
    print("\n✓ Atividades do PLE Básico concluídas.")

# -*- coding: utf-8 -*-
"""Quizzes de avaliação dos 5 cursos de Hebraico (docs "Vedium_Hebraico_*_
Grade_Conteudo_Avaliacao", 2026 — questões autorais da Vedium).

Cria, por curso, uma "Prova Final" (LMS Quiz) numa lição dedicada dentro de
um capítulo "Avaliação Final", exatamente como já foi feito para PLE/Espanhol,
e sincroniza as tabelas nativas de navegação do LMS.

Banco de cada prova = "Quiz de progresso" (10) + "Atividade final" (10) = 20
questões por curso.

Duas correções de qualidade sobre o material de origem:

1. Posição da resposta: nos docs de A1/A2-B1/Bíblico/Particular a alternativa
   correta é SEMPRE a letra "A". Se semeada assim, o aluno decora "marca A".
   `_make_question` aplica uma rotação determinística por questão (offset
   derivado do hash do enunciado), distribuindo a resposta certa entre A/B/C/D
   sem alterar o conjunto de alternativas. Idempotente.

2. A "prova integradora de 40 questões" do A2/B1 foi DESCARTADA: são ~10
   questões repetidas 4x e o gabarito é mecânico (1-A, 2-B, 3-C, 4-D...) que
   NÃO corresponde às alternativas mostradas (ex.: "ontem/semana passada" tem
   gabarito "Pronomes", mas a resposta certa é "Marcadores de tempo"). Usamos
   só o quiz + atividade final, cujos gabaritos conferem.

Rodar (idempotente):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.seed_hebraico_quizzes.run
"""

import hashlib

import frappe

FINAL_CHAPTER_TITLE = "Avaliação Final"
FINAL_LESSON_TITLE = "Prova Final — faça a avaliação do nível"


# ---------------------------------------------------------------------------
# Bancos por curso — (pergunta, [4 alternativas], índice correto 0-based)
# ---------------------------------------------------------------------------

A0_QUESTIONS = [
    ("Em que direção o hebraico é lido?", ["Da esquerda para a direita", "Da direita para a esquerda", "De cima para baixo", "Sem direção fixa"], 1),
    ("Quantas consoantes compõem tradicionalmente o alfabeto hebraico?", ["20", "22", "24", "26"], 1),
    ("O que são letras finais?", ["Letras usadas só no começo da palavra", "Letras usadas apenas em textos bíblicos", "Formas especiais de algumas letras no fim da palavra", "Sinais vocálicos"], 2),
    ("Qual expressão é usada para \"olá/paz\"?", ["Toda", "Shalom", "Slicha", "Bevakasha"], 1),
    ("Qual expressão significa \"obrigado/a\"?", ["Toda", "Erev tov", "Ma nishma", "Ani"], 0),
    ("O que o sinal vocálico indica em hebraico vocalizado?", ["Valor numérico", "Som de vogal", "Nome próprio", "Pontuação final"], 1),
    ("Qual é uma boa meta do A0?", ["Debater política em hebraico", "Ler letras, sons e palavras simples", "Traduzir poesia bíblica sem apoio", "Falar fluentemente"], 1),
    ("Qual prática ajuda mais na alfabetização?", ["Somente assistir vídeos", "Repetição oral, cópia e leitura curta", "Decorar listas sem ler", "Evitar escrever"], 1),
    ("\"Bevakasha\" costuma ser usado como:", ["Por favor/de nada", "Boa noite", "Eu moro", "Ontem"], 0),
    ("Na Vedium, a alfabetização deve ser:", ["Rápida, sem prática", "Ao vivo, guiada e com correção", "Só por apostila", "Sem leitura em voz alta"], 1),
    # Atividade final
    ("Ao ver uma palavra hebraica, o primeiro passo de leitura é:", ["Procurar a última letra à direita", "Começar pela direita", "Começar pelo centro", "Ignorar as vogais"], 1),
    ("Alef-Bet é:", ["O conjunto de letras hebraicas", "Um verbo", "Um número", "Uma saudação"], 0),
    ("A forma final de uma letra aparece:", ["No começo da palavra", "No fim da palavra", "Somente em nomes", "Somente com vogais"], 1),
    ("Qual par é saudação + agradecimento?", ["Shalom + toda", "Slicha + shlosha", "Ani + ata", "Echad + shtayim"], 0),
    ("A pronúncia deve ser trabalhada:", ["Só no final do curso", "Desde a primeira aula", "Somente no nível avançado", "Sem professor"], 1),
    ("O aluno conclui o A0 quando consegue:", ["Ler palavras simples com apoio", "Traduzir textos longos", "Conjugar todos os verbos", "Ler sem errar sempre"], 0),
    ("O número \"echad\" corresponde a:", ["Um", "Dois", "Três", "Quatro"], 0),
    ("\"Slicha\" é usado para:", ["Pedir desculpa/licença", "Dizer até logo", "Dizer sim", "Contar dinheiro"], 0),
    ("Um bom exercício final de A0 é:", ["Ler e soletrar o próprio nome", "Escrever tese acadêmica", "Debater notícia", "Traduzir capítulo inteiro"], 0),
    ("O foco da Vedium no A0 é:", ["Prometer fluência rápida", "Construir base segura e confiança", "Vender gramática sem prática", "Evitar cultura"], 1),
]

A1_QUESTIONS = [
    ("\"Ani\" corresponde a:", ["Eu", "Você", "Ele", "Nós"], 0),
    ("\"Ata\" é usado para:", ["Você (masculino)", "Você (feminino)", "Eles", "Ela"], 0),
    ("\"At\" é usado para:", ["Você (feminino)", "Ele", "Nós", "Eles"], 0),
    ("Qual frase indica \"bom dia\"?", ["Boker tov", "Erev tov", "Laila tov", "Toda raba"], 0),
    ("\"Ma nishma?\" é usado para:", ["Perguntar como vai / novidades", "Pedir preço", "Dizer idade", "Dizer onde mora"], 0),
    ("O foco do A1 Moderno é:", ["Comunicação cotidiana inicial", "Exegese avançada", "Tradução literária", "Gramática sem fala"], 0),
    ("Para dizer preferência, o aluno precisa praticar:", ["Vocabulário de gosto e escolha", "Somente alfabeto", "Somente números", "Somente letras finais"], 0),
    ("Uma turma A1 ideal deve priorizar:", ["Interação ao vivo", "Silêncio e cópia", "Só leitura individual", "Sem correção"], 0),
    ("Qual tema pertence ao A1?", ["Cumprimentos e apresentação", "Verbos geminados avançados", "Crítica literária", "Aramaico bíblico"], 0),
    ("Ao errar a pronúncia, o aluno deve receber:", ["Correção acolhedora e repetição guiada", "Punição", "Silêncio", "Mudança de turma imediata"], 0),
    # Atividade final
    ("Em uma apresentação inicial, o aluno deve conseguir dizer:", ["Nome, origem e objetivo", "Análise de sintaxe poética", "Tradução de capítulo inteiro", "Discussão filosófica"], 0),
    ("\"Hu\" significa:", ["Ele", "Ela", "Você", "Nós"], 0),
    ("\"Hi\" significa:", ["Ela", "Ele", "Vocês", "Eu"], 0),
    ("Números são úteis no A1 para:", ["Horários, preços e idade", "Somente textos bíblicos", "Evitar conversação", "Decorar sem uso"], 0),
    ("Uma frase nominal simples é importante porque:", ["Permite dizer quem/como algo é sem verbo complexo", "Substitui todo o curso", "Só existe em português", "Não aparece em hebraico"], 0),
    ("Em situação de restaurante, o aluno pratica:", ["Pedido, agradecimento e preferência", "Particípio bíblico", "Crítica textual", "Vogais massoréticas somente"], 0),
    ("No A1, cultura deve ser abordada:", ["Com respeito e contexto", "Como curiosidade rasa", "Sem relação com o idioma", "Apenas no fim"], 0),
    ("A tarefa final do A1 deve integrar:", ["Fala, leitura e perguntas simples", "Somente múltipla escolha", "Silêncio", "Cópia sem entender"], 0),
    ("O professor deve registrar:", ["Presença, vocabulário ativo e pontos de pronúncia", "Apenas a nota final", "Nada", "Somente o pagamento"], 0),
    ("A progressão natural após o A1 é:", ["A2/B1 Moderno ou trilha bíblica, conforme objetivo", "Encerrar sem feedback", "Pular para avançado sem base", "Fazer só aulas gravadas"], 0),
]

A2B1_QUESTIONS = [
    ("O principal salto do A1 para o A2/B1 é:", ["Manter conversas mais longas e narrar experiências", "Voltar ao alfabeto apenas", "Eliminar a fala", "Estudar só teoria"], 0),
    ("Para narrar o passado, o aluno precisa de:", ["Marcadores temporais e verbos frequentes", "Somente cumprimentos", "Apenas números", "Somente letras finais"], 0),
    ("Em conversação, uma pergunta de acompanhamento serve para:", ["Manter o diálogo vivo", "Encerrar a fala do colega", "Evitar a escuta", "Substituir vocabulário"], 0),
    ("Um conector básico de opinião é:", ["Porque", "Alef", "Qamats", "Dagesh"], 0),
    ("A leitura de avisos e mensagens exige:", ["Estratégias de contexto e palavras-chave", "Tradução palavra por palavra sempre", "Não ler", "Somente decorar"], 0),
    ("O A2/B1 deve preparar o aluno para:", ["Serviços, trabalho, estudo e conversa social", "Somente saudações", "Somente textos bíblicos", "Apenas caligrafia"], 0),
    ("Um projeto final adequado é:", ["Apresentação com perguntas da turma", "Cópia do alfabeto apenas", "Prova oral sem feedback", "Leitura silenciosa sem interação"], 0),
    ("Ao escrever um e-mail curto, o aluno precisa de:", ["Saudação, objetivo claro e fechamento", "Somente números", "Apenas letras", "Nenhuma estrutura"], 0),
    ("O feedback mais útil deve apontar:", ["Repertório ativo e próximos passos", "Só os erros", "Só elogios vagos", "Nada"], 0),
    ("O critério de conclusão do A2/B1 é:", ["Comunicar-se com autonomia básica e repertório ampliado", "Nunca errar", "Ser tradutor profissional", "Dominar todos os verbos bíblicos"], 0),
    # Atividade final
    ("Em uma narrativa curta, o aluno deve ordenar:", ["Quando, onde, quem e o que aconteceu", "Somente nomes de letras", "Somente números", "Sem sequência"], 0),
    ("Para reclamar com educação, o aluno precisa:", ["Explicar o problema e pedir solução", "Usar só \"shalom\"", "Evitar contexto", "Falar em português"], 0),
    ("Uma boa estratégia quando falta uma palavra é:", ["Reformular com palavras conhecidas", "Parar a conversa", "Desistir", "Trocar para português sempre"], 0),
    ("O aluno A2/B1 deve conseguir:", ["Expressar opinião simples com justificativa", "Fazer exegese avançada", "Ler sem vogais sempre", "Ensinar todos os níveis"], 0),
    ("Em textos curtos, as palavras-chave ajudam a:", ["Captar o sentido geral", "Impedir a leitura", "Ignorar o contexto", "Eliminar vocabulário"], 0),
    ("A autoavaliação deve responder:", ["O que já faço e qual é meu próximo passo", "Quanto sei decorar", "Quem errou mais", "Nada"], 0),
    ("Conversas de 3 minutos treinam:", ["Ritmo, escuta e reação", "Silêncio", "Caligrafia apenas", "Tradução simultânea"], 0),
    ("A cultura no A2/B1 aparece como:", ["Contexto para entender o uso real da língua", "Enfeite", "Exotismo", "Assunto proibido"], 0),
    ("A prova integrada mede:", ["Compreensão, vocabulário, estrutura e comunicação", "Memória isolada apenas", "Caligrafia somente", "Velocidade de digitação"], 0),
    ("O próximo passo após o A2/B1 é:", ["Manutenção, conversação, bíblico ou particular por objetivo", "Recomeçar sempre do zero", "Parar sem plano", "Trocar de professor sem diagnóstico"], 0),
]

BIBLICO_QUESTIONS = [
    ("O Hebraico Bíblico, neste curso, tem foco em:", ["Leitura guiada e base linguística", "Conversação de viagem", "Promessa religiosa", "Apenas caligrafia"], 0),
    ("A raiz verbal hebraica é frequentemente:", ["Triconsonantal", "Sempre de uma letra", "Sempre portuguesa", "Sem consoantes"], 0),
    ("O artigo definido em hebraico é estudado para:", ["Reconhecer substantivos definidos", "Substituir verbos", "Marcar o futuro", "Indicar números apenas"], 0),
    ("A relação de construto indica geralmente:", ["Ligação/posse entre nomes", "Cumprimento moderno", "Despedida", "Som de vogal apenas"], 0),
    ("Qal é:", ["Uma construção verbal básica", "Uma saudação", "Um dicionário", "Uma letra final"], 0),
    ("Sheva e dagesh ajudam a entender:", ["Leitura, sílaba e pronúncia", "Preço do curso", "História moderna somente", "Cores da marca"], 0),
    ("Um léxico serve para:", ["Consultar o sentido e a forma das palavras", "Substituir a aula", "Evitar a gramática", "Prometer tradução automática"], 0),
    ("A leitura responsável evita:", ["Forçar interpretações sem base linguística", "Analisar a forma", "Consultar o contexto", "Usar o dicionário"], 0),
    ("Na Vedium, o professor deve:", ["Separar língua, contexto e limites interpretativos", "Vender certeza absoluta", "Ignorar dúvidas", "Usar cultura como enfeite"], 0),
    ("A atividade final bíblica deve pedir:", ["Análise curta com forma, vocabulário e tradução comentada", "Sermão obrigatório", "Memorização sem leitura", "Debate político"], 0),
    # Atividade final
    ("Ao encontrar uma palavra, primeiro identifique:", ["A raiz ou a forma provável", "O preço", "A rede social", "A cor"], 0),
    ("Uma cadeia de construto pode ser traduzida como:", ["\"X de Y\"", "Olá", "Obrigado", "Amanhã"], 0),
    ("Sufixos pronominais podem indicar:", ["Meu/teu/seu etc.", "Somente tempo verbal", "Somente vogal", "Nenhuma função"], 0),
    ("O Qal completo costuma ser apresentado como:", ["Ação completa / perfeito", "Cumprimento", "Número", "Adjetivo moderno"], 0),
    ("O Qal incompleto costuma ser apresentado como:", ["Ação incompleta / futura conforme o contexto", "Letra final", "Nome de pessoa", "Artigo"], 0),
    ("A leitura de poesia exige atenção a:", ["Paralelismo e repetição", "Somente pontuação moderna", "Preço", "Alfabeto latino"], 0),
    ("Uma tradução comentada deve mostrar:", ["Decisões de vocabulário e limites", "Apenas a resposta final", "Sem justificativa", "Opinião sem texto"], 0),
    ("O aluno conclui a trilha quando consegue:", ["Ler passagem curta com apoio e explicar escolhas", "Ser especialista em semítica", "Traduzir tudo sem dicionário", "Falar moderno fluentemente"], 0),
    ("A Bíblia interlinear deve ser usada como:", ["Apoio, não muleta única", "Substituto da aprendizagem", "Prova de fluência", "Atalho sem gramática"], 0),
    ("O tom do curso deve ser:", ["Respeitoso, técnico e claro", "Dogmático e agressivo", "Promocional", "Confuso"], 0),
]

PARTICULAR_QUESTIONS = [
    ("A primeira etapa do Hebraico Particular deve ser:", ["Diagnóstico e meta individual", "Prova final imediata", "Troca de professor", "Aula sem objetivo"], 0),
    ("Um bom plano particular precisa de:", ["Objetivo, carga, evidência de progresso e rotina", "Apenas horário", "Só lista de palavras", "Sem avaliação"], 0),
    ("Qual objetivo exige a trilha moderna?", ["Viagem e comunicação cotidiana", "Leitura de Gênesis com morfologia", "Análise de Qal", "Crítica textual"], 0),
    ("Qual objetivo exige a trilha bíblica?", ["Leitura orientada de textos bíblicos", "Pedido em restaurante", "Conversa no hotel", "Compras"], 0),
    ("A cada 4 aulas, recomenda-se:", ["Revisar o progresso e ajustar a rota", "Começar tudo de novo sem razão", "Não registrar nada", "Cancelar a tarefa"], 0),
    ("O professor particular deve evitar:", ["Prometer fluência rápida", "Personalizar", "Dar feedback", "Registrar a evolução"], 0),
    ("O aluno de particular pode receber:", ["Plano de 8, 12 ou 24 encontros", "Somente turma coletiva", "Sem tarefa", "Sem diagnóstico"], 0),
    ("A avaliação no particular deve ser:", ["Adaptada ao objetivo contratado", "Igual para todos sempre", "Sem critérios", "Só opinião"], 0),
    ("Um bom entregável final é:", ["Leitura, apresentação, roteiro de viagem ou análise, conforme a meta", "Nada", "Só presença", "Só pagamento"], 0),
    ("O tom Vedium no particular é:", ["Próximo, sério e direto", "Milagroso", "Frio", "Automatizado"], 0),
    # Atividade final
    ("O aluno conclui um pacote particular quando:", ["Entrega uma evidência real ligada à meta", "Assiste passivamente", "Não faz tarefa", "Decora sem aplicar"], 0),
    ("Para viagem, uma atividade final adequada é:", ["Resolver 5 situações reais de deslocamento/serviço", "Analisar raízes fracas", "Ler poesia bíblica", "Fazer um sermão"], 0),
    ("Para leitura bíblica, uma atividade final adequada é:", ["Analisar uma passagem curta com apoio", "Pedir café", "Dizer a idade", "Contar dinheiro"], 0),
    ("Para família/herança, uma atividade final adequada é:", ["Apresentar nomes, história e vocabulário pessoal com cuidado", "Exigir debate avançado", "Sem contexto", "Somente prova escrita"], 0),
    ("O relatório do professor deve trazer:", ["Pontos fortes, lacunas e próximo plano", "Só a nota", "Só as faltas", "Nada"], 0),
    ("O particular não deve virar:", ["Aula solta sem trilha", "Plano mensurável", "Feedback constante", "Apoio personalizado"], 0),
    ("A melhor prática entre aulas é:", ["Tarefa curta e alinhada à meta", "Excesso sem foco", "Nenhuma tarefa", "Conteúdo aleatório"], 0),
    ("Para pronúncia, o professor deve usar:", ["Repetição, escuta e correção gentil", "Só texto", "Crítica dura", "Nenhum áudio"], 0),
    ("Para vocabulário, o ideal é:", ["Campo temático ligado ao objetivo", "Lista aleatória", "Palavras sem uso", "Somente dicionário"], 0),
    ("Ao renovar o pacote, a decisão deve considerar:", ["Meta atingida, nova meta e disponibilidade", "Somente impulso", "Sem feedback", "Sem preço claro"], 0),
]

COURSES = [
    {"course": "hebraico-a0-alfabetizacao", "quiz_title": "Prova Final — Hebraico A0 (Alfabetização)", "questions": A0_QUESTIONS},
    {"course": "hebraico-moderno-a1", "quiz_title": "Prova Final — Hebraico Moderno A1", "questions": A1_QUESTIONS},
    {"course": "hebraico-moderno-a2-b1", "quiz_title": "Prova Final — Hebraico Moderno A2/B1", "questions": A2B1_QUESTIONS},
    {"course": "hebraico-biblico-leitura-guiada", "quiz_title": "Prova Final — Hebraico Bíblico (Leitura Guiada)", "questions": BIBLICO_QUESTIONS},
    {"course": "hebraico-particular", "quiz_title": "Prova Final — Hebraico Particular", "questions": PARTICULAR_QUESTIONS},
]


# ---------------------------------------------------------------------------
# Rotação determinística da posição da resposta correta
# ---------------------------------------------------------------------------

def _rotate(options, correct_idx, seed_text):
    """Rotaciona as 4 alternativas por um offset derivado do enunciado, para
    que a resposta correta não fique sempre na mesma letra. Determinístico e
    idempotente (mesmo enunciado -> mesma rotação); preserva o conjunto de
    alternativas."""
    offset = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest(), 16) % 4
    rotated = options[offset:] + options[:offset]
    new_correct = (correct_idx - offset) % 4
    return rotated, new_correct


# ---------------------------------------------------------------------------
# Criação no banco (mesmo padrão do seed_espanhol_quizzes)
# ---------------------------------------------------------------------------

def _make_question(question_text, options, correct_idx):
    if len(options) != 4:
        frappe.throw(f"Pergunta precisa ter exatamente 4 opções: {question_text}")
    if correct_idx not in range(4):
        frappe.throw(f"Índice da resposta correta inválido: {question_text}")

    options, correct_idx = _rotate(options, correct_idx, question_text)

    existing = frappe.db.get_value("LMS Question", {"question": question_text})
    if existing:
        doc = frappe.get_doc("LMS Question", existing)
    else:
        doc = frappe.get_doc({"doctype": "LMS Question", "question": question_text})

    doc.type = "Choices"
    doc.multiple = 0
    for i, option_text in enumerate(options, start=1):
        doc.set(f"option_{i}", option_text)
        doc.set(f"is_correct_{i}", 1 if i - 1 == correct_idx else 0)

    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)
    return doc.name


def _make_quiz(title, course, questions):
    if not questions:
        frappe.throw(f"Quiz '{title}' precisa ter perguntas.")

    existing = frappe.db.get_value("LMS Quiz", {"title": title})
    if existing:
        quiz = frappe.get_doc("LMS Quiz", existing)
        action = "atualizado"
    else:
        quiz = frappe.get_doc({"doctype": "LMS Quiz", "title": title})
        action = "criado"

    quiz.course = course
    quiz.max_attempts = 3
    quiz.passing_percentage = 70
    quiz.shuffle_questions = 1
    quiz.limit_questions_to = 0
    quiz.total_marks = len(questions)
    quiz.set("questions", [])
    for question_text, options, correct_idx in questions:
        q_name = _make_question(question_text, options, correct_idx)
        quiz.append("questions", {"question": q_name, "marks": 1})

    if quiz.is_new():
        quiz.insert(ignore_permissions=True)
    else:
        quiz.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  ✓ Quiz '{title}' {action} ({len(questions)} questões).")
    return quiz.name


def _ensure_final_exam_lesson(course, quiz_name, total_questions):
    chapter_name = frappe.db.get_value("Course Chapter", {"course": course, "title": FINAL_CHAPTER_TITLE})
    if not chapter_name:
        chapter = frappe.get_doc({
            "doctype": "Course Chapter",
            "title": FINAL_CHAPTER_TITLE,
            "course": course,
        })
        chapter.insert(ignore_permissions=True)
        chapter_name = chapter.name
        print(f"  ✓ criado capítulo '{FINAL_CHAPTER_TITLE}'")

    body = (
        f"Prova final do nível: {total_questions} questões de múltipla escolha, "
        "nota mínima de 70% e até 3 tentativas. A ordem muda a cada tentativa."
    )

    lesson_name = frappe.db.get_value("Course Lesson", {"chapter": chapter_name, "title": FINAL_LESSON_TITLE}, "name")
    if not lesson_name:
        lesson = frappe.get_doc({
            "doctype": "Course Lesson",
            "title": FINAL_LESSON_TITLE,
            "chapter": chapter_name,
            "course": course,
            "content": "",
            "body": body,
            "quiz_id": quiz_name,
        })
        lesson.insert(ignore_permissions=True)
        lesson_name = lesson.name
        print(f"  ✓ criada lição '{FINAL_LESSON_TITLE}'")
    else:
        lesson = frappe.get_doc("Course Lesson", lesson_name)
        lesson.content = ""
        lesson.body = body
        lesson.quiz_id = quiz_name
        lesson.save(ignore_permissions=True)
        print(f"  ✓ atualizada lição '{FINAL_LESSON_TITLE}'")

    frappe.db.set_value("LMS Quiz", quiz_name, {"course": course, "lesson": lesson_name})


def _get_lms_schema():
    course_meta = frappe.get_meta("LMS Course")
    chapters_field = course_meta.get_field("chapters")
    if not chapters_field or chapters_field.fieldtype != "Table":
        frappe.throw("LMS Course.chapters table field was not found.")

    chapter_meta = frappe.get_meta("Course Chapter")
    lessons_field = chapter_meta.get_field("lessons")
    if not lessons_field or lessons_field.fieldtype != "Table":
        frappe.throw("Course Chapter.lessons table field was not found.")

    return {
        "chapter_reference_doctype": chapters_field.options,
        "lesson_reference_doctype": lessons_field.options,
    }


def _sync_child_links(child_doctype, parent_doctype, parent, parentfield, link_field, targets):
    current_rows = frappe.get_all(
        child_doctype, filters={"parent": parent}, fields=["name", link_field],
        order_by="idx asc, creation asc, name asc",
    )
    current = [row.get(link_field) for row in current_rows]
    if current == targets:
        return False

    for row in current_rows:
        frappe.delete_doc(child_doctype, row.name, ignore_permissions=True, force=True)

    for idx, target in enumerate(targets, start=1):
        frappe.get_doc({
            "doctype": child_doctype,
            "parent": parent,
            "parenttype": parent_doctype,
            "parentfield": parentfield,
            "idx": idx,
            link_field: target,
        }).insert(ignore_permissions=True)
    return True


def _sync_navigation(course, schema):
    chapters = frappe.get_all(
        "Course Chapter", filters={"course": course}, fields=["name"],
        order_by="idx asc, creation asc, name asc",
    )
    _sync_child_links(
        schema["chapter_reference_doctype"], "LMS Course", course, "chapters", "chapter",
        [c.name for c in chapters],
    )

    total_lessons = 0
    for chapter in chapters:
        lessons = frappe.get_all(
            "Course Lesson", filters={"chapter": chapter.name}, fields=["name"],
            order_by="idx asc, creation asc, name asc",
        )
        _sync_child_links(
            schema["lesson_reference_doctype"], "Course Chapter", chapter.name, "lessons", "lesson",
            [l.name for l in lessons],
        )
        total_lessons += len(lessons)

    frappe.db.set_value("LMS Course", course, "lessons", total_lessons)
    print(f"  ✓ navegação sincronizada ({total_lessons} lições)")


def run():
    schema = _get_lms_schema()

    for data in COURSES:
        course = data["course"]
        print(f"\n=== {course} ===")
        if not frappe.db.exists("LMS Course", course):
            print("  curso não existe -- rode create_hebraico_courses.run primeiro.")
            continue

        questions = data["questions"]
        quiz_name = _make_quiz(data["quiz_title"], course, questions)
        _ensure_final_exam_lesson(course, quiz_name, len(questions))
        _sync_navigation(course, schema)

    frappe.db.commit()
    print("\n✓ Quizzes de Hebraico configurados e navegação sincronizada.")

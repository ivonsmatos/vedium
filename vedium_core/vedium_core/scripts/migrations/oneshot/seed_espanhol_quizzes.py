# -*- coding: utf-8 -*-
"""Quizzes de avaliação dos cursos de Espanhol (a partir dos docs
"Vedium_Avaliacao_Espanhol_*", 2026 — questões autorais da Vedium).

Cria, por nível, uma "Prova Final" (LMS Quiz) e uma lição dedicada dentro de
um capítulo "Avaliação Final", exatamente como já foi feito pro PLE:
    - Básico: 10 questões (banco = todas as 10 do "Quiz do nível").
    - Intermediário: 10 questões (idem).
    - Avançado: banco de 50 (10 do "Quiz do nível" + 40 da "Prova final de
      40 questões"), sorteando 40 por tentativa.

Depois sincroniza as tabelas nativas de navegação do LMS (Chapter
Reference / Lesson Reference) — sem isso o "Continue Learning" do LMS não
enxerga os módulos (mesmo bug já visto e corrigido no PLE).

Rodar (idempotente):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.seed_espanhol_quizzes.run
"""

import frappe

FINAL_CHAPTER_TITLE = "Avaliação Final"
FINAL_LESSON_TITLE = "Prova Final — faça a avaliação do nível"

COURSES = [
    {
        "course": "espanhol-basico",
        "quiz_title": "Prova Final — Espanhol Básico (A1-A2)",
        "max_attempts": 3,
        "passing_percentage": 70,
        "limit_questions_to": 0,
    },
    {
        "course": "espanhol-intermediario",
        "quiz_title": "Prova Final — Espanhol Intermediário (B1-B2.1)",
        "max_attempts": 3,
        "passing_percentage": 70,
        "limit_questions_to": 0,
    },
    {
        "course": "espanhol-avancado",
        "quiz_title": "Prova Final — Espanhol Avançado (B2.2-C1)",
        "max_attempts": 3,
        "passing_percentage": 70,
        "limit_questions_to": 40,
    },
]

# ---------------------------------------------------------------------------
# Bancos de questões — (pergunta, [4 opções], índice da correta 0-based)
# ---------------------------------------------------------------------------

BASICO_QUESTIONS = [
    ("Escolha a resposta mais adequada para iniciar uma conversa formal.",
     ["¿Qué pasa, tío?", "Hola, buenos días. ¿Cómo está usted?", "Hasta luego, gracias.", "Me llamo Brasil."], 1),
    ("Complete: Yo _____ brasileño y vivo en São Paulo.",
     ["soy", "estoy", "tengo", "hay"], 0),
    ("Qual pergunta combina com a resposta: \"Soy de Brasil\"?",
     ["¿Dónde vives?", "¿De dónde eres?", "¿Qué haces?", "¿Cómo se escribe?"], 1),
    ("Complete: Estudio español _____ quiero viajar por América Latina.",
     ["pero", "porque", "también", "nunca"], 1),
    ("A opção correta para falar de gostos é:",
     ["Yo gusto café.", "A mí me gusta el café.", "Me gusto el café.", "A mí gusta el café."], 1),
    ("Escolha a frase correta sobre rotina.",
     ["Me levanto a las siete.", "Yo levantar a las siete.", "Me levanta a las siete.", "Levanto me a las siete."], 0),
    ("Em uma loja, para pedir preço, você diz:",
     ["¿Cuánto cuesta?", "¿Dónde comes?", "¿Qué hora tienes?", "¿Cómo se llama?"], 0),
    ("Complete: En mi ciudad _____ muchos parques y restaurantes.",
     ["está", "son", "hay", "tiene"], 2),
    ("No restaurante, a frase mais adequada é:",
     ["Quiero pagar la cuenta, por favor.", "Soy pagar la cuenta.", "Tengo la cuenta comer.", "Hay pagar favor."], 0),
    ("Para falar de futuro próximo, usamos:",
     ["ir + a + infinitivo", "ser + gerundio", "tener + participio", "estar + sustantivo"], 0),
]

INTERMEDIARIO_QUESTIONS = [
    ("Escolha a forma verbal mais adequada: Ayer _____ al centro y compré un libro.",
     ["he ido", "iba", "fui", "voy"], 2),
    ("Complete: Cuando era niño, _____ mucho con mis primos.",
     ["jugué", "jugaba", "he jugado", "jugaré"], 1),
    ("Qual frase faz um pedido mais educado?",
     ["Dame otra habitación.", "Quiero que cambies todo.", "¿Sería posible cambiar la habitación?", "Cambia mi habitación ahora."], 2),
    ("Em um e-mail profissional, o fechamento mais adequado é:",
     ["Besos, nos vemos.", "Atentamente, quedo a disposición.", "Chau, gracias por nada.", "¿Qué onda?"], 1),
    ("Complete: Estoy de acuerdo, _____ creo que falta considerar el presupuesto.",
     ["aunque", "sin embargo", "porque", "también"], 1),
    ("A opção que expressa hipótese realista no futuro é:",
     ["Si tengo tiempo, practicaré más.", "Si tendría tiempo, practicaré más.", "Si tengo tiempo, practicaría más.", "Si tuve tiempo, practico más."], 0),
    ("Para dar conselho, a forma mais natural é:",
     ["Deberías descansar un poco.", "Descansas tú ahora siempre.", "Tú descansar obligatorio.", "Hay que tú descansas."], 0),
    ("Qual frase evita generalização cultural?",
     ["Todos los españoles son iguales.", "En algunos contextos, se suele saludar de forma más cercana.", "Los latinos siempre hablan alto.", "Ese país es así y punto."], 1),
    ("Complete: Busco un curso _____ me ayude a hablar con más seguridad.",
     ["que", "quien", "donde", "cuyo"], 0),
    ("A frase que melhor resume uma opinião com nuance é:",
     ["Es malo y ya.", "No sirve para nada.", "Tiene ventajas, aunque también presenta límites.", "Todos deberían pensar igual."], 2),
]

_AVANCADO_QUIZ_10 = [
    ("Qual alternativa expressa opinião com nuance?",
     ["Eso es totalmente falso y absurdo.", "No hay nada que discutir.", "Si bien el argumento es pertinente, conviene matizarlo.", "La gente siempre se equivoca."], 2),
    ("Complete: Aunque _____ difícil, intentaremos llegar a un acuerdo.",
     ["es", "sea", "será", "fue"], 1),
    ("Escolha o conector que expressa consequência formal.",
     ["por consiguiente", "o sea", "bueno", "encima"], 0),
    ("Qual frase é mais diplomática em reunião?",
     ["No puedo hacerlo.", "Eso no sirve.", "Quizá podríamos revisar el plazo antes de comprometernos.", "Te equivocas."], 2),
    ("Em análise de mídia, \"el autor sostiene que...\" significa:",
     ["o autor duvida que", "o autor afirma/defende que", "o autor nega sempre que", "o autor traduz que"], 1),
    ("Qual opção usa voz impessoal corretamente?",
     ["Se dicen que el proyecto avanza.", "Se dice que el proyecto avanza.", "Se dice que avanzan el proyecto.", "Dice se que el proyecto avanza."], 1),
    ("Complete: Buscamos una solución que _____ sostenible a largo plazo.",
     ["es", "será", "sea", "fue"], 2),
    ("Qual frase mostra registro adequado e respeito cultural?",
     ["Esa cultura es exótica.", "Todos ellos son así.", "Conviene entender el contexto histórico antes de generalizar.", "Eso es raro y primitivo."], 2),
    ("Qual reformulação reduz viés em um título?",
     ["Fracaso total de la medida.", "Polémica sin sentido.", "La medida genera debate entre distintos sectores.", "La peor decisión de todas."], 2),
    ("Escolha a frase mais precisa para relatório.",
     ["Hicimos cosas y salió bien.", "Se implementaron tres acciones y los resultados mejoraron un 12%.", "Todo estuvo increíble.", "Fue más o menos bueno."], 1),
]

_AVANCADO_EXAM_40 = [
    ("Complete: Hola, me llamo Ana y _____ de Colombia.", ["soy", "estoy", "tengo", "hay"], 0),
    # Texto único ("Em espanhol, ...") de propósito: existia uma pergunta com
    # texto IDÊNTICO no seed do PLE Básico e o _make_question busca LMS Question
    # por texto — o seed que rodasse por último sobrescrevia as alternativas do
    # outro idioma nos DOIS quizzes (achado do QA 2026-07-10).
    ("Em espanhol, qual pergunta pede a profissão de alguém?", ["¿A qué te dedicas?", "¿De dónde eres?", "¿Cuánto cuesta?", "¿Qué hora es?"], 0),
    ("Complete: A mí _____ gusta estudiar por la mañana.", ["yo", "me", "mi", "soy"], 1),
    ("Escolha a frase correta.", ["Hay tres restaurantes en la calle.", "Tiene tres restaurantes en la calle.", "Son tres restaurantes en la calle.", "Está tres restaurantes en la calle."], 0),
    ("Em uma loja, \"talla\" significa:", ["preço", "tamanho", "rua", "horário"], 1),
    ("Complete: Normalmente _____ a las siete y media.", ["me levanto", "me levanté", "levantarme", "levantado"], 0),
    ("Para pedir a conta, diga:", ["La cuenta, por favor.", "La calle, por favor.", "El tiempo, por favor.", "El nombre, por favor."], 0),
    ("Complete: Mañana voy _____ estudiar español.", ["a", "de", "por", "con"], 0),
    ("Qual frase está no passado simples?", ["Ayer visité un museo.", "Mañana visito un museo.", "Todos los días visito un museo.", "Estoy visitando un museo."], 0),
    ("A melhor resposta para \"¿Cómo se escribe tu apellido?\" é:", ["Se escribe M-A-T-O-S.", "Soy de Brasil.", "Tengo 30 años.", "A las ocho."], 0),
    ("Escolha a instrução de direção.", ["Sigue todo recto y gira a la derecha.", "Me gusta mucho el café.", "Soy profesor.", "Tengo una hermana."], 0),
    ("Complete: No me gusta el té. - A mí _____.", ["tampoco", "también", "mucho", "nunca soy"], 0),
    ("Complete: El año pasado _____ a México por trabajo.", ["viajé", "viajaba", "viajo", "he viajando"], 0),
    ("Complete: Antes, cuando vivía cerca, _____ al trabajo caminando.", ["fui", "iba", "iré", "he ido"], 1),
    ("Escolha a frase mais cortês.", ["Necesito que lo arregles ya.", "¿Podría ayudarme con este problema?", "Hazlo ahora.", "No entiendo nada, cámbialo."], 1),
    ("Qual conector marca contraste?", ["sin embargo", "por eso", "además", "por ejemplo"], 0),
    ("Complete: Si practicas todos los días, _____ más seguridad.", ["ganarás", "ganarías", "ganabas", "ganaste"], 0),
    ("Escolha a forma correta de conselho.", ["Deberías revisar el vocabulario.", "Debes de revisaré vocabulario.", "Tendrías revisar vocabulario.", "Hay que tú revisas vocabulario."], 0),
    ("Em um e-mail, \"quedo a disposición\" indica:", ["fechamento profissional", "saudação informal", "reclamação agressiva", "erro gramatical"], 0),
    ("Complete: Necesito una persona que _____ español y portugués.", ["habla", "hable", "habló", "hablará siempre"], 1),
    ("Qual frase evita estereótipo?", ["Todos son iguales.", "En algunos países se usa más usted que tú.", "Ese povo é assim.", "A cultura deles é estranha."], 1),
    ("Escolha a melhor reformulação de \"no me gusta\" em debate.", ["No sirve.", "No me convence porque falta evidencia.", "Es horrible.", "Nunca funciona."], 1),
    ("Qual palavra combina com contexto profissional?", ["plazo", "helado", "zapato", "ventana"], 0),
    ("Complete: Aunque no tengo mucho tiempo, _____ practicar 20 minutos al día.", ["intentaré", "intentaba ayer", "soy intentar", "intentado"], 0),
    ("Para narrar uma sequência, o melhor conjunto é:", ["primero, después, al final", "alto, bajo, bonito", "ayer, rojo, nunca", "sí, no, tal vez"], 0),
    ("A frase \"Entiendo tu punto, pero...\" serve para:", ["discordar com respeito", "terminar uma compra", "pedir comida", "cumprimentar alguém"], 0),
    ("Complete: El curso _____ elegí tiene clases en vivo.", ["que", "quien", "cuyo", "donde persona"], 0),
    ("Qual opção indica causa?", ["ya que", "sin embargo", "aunque", "aun así"], 0),
    ("Qual frase é mais adequada em registro formal?", ["Creo que esto está fatal.", "Considero que la propuesta requiere algunos ajustes.", "Eso no va ni de broma.", "Está mal y punto."], 1),
    ("Complete: Es importante que todos _____ el contexto antes de opinar.", ["entienden", "entiendan", "entendieron", "entenderán"], 1),
    ("\"Por consiguiente\" indica:", ["consequência", "exemplo", "dúvida", "saudação"], 0),
    ("Qual frase usa linguagem diplomática?", ["No tienes razón.", "Eso es imposible.", "Podríamos considerar otra alternativa.", "Tu idea no sirve."], 2),
    ("Em análise textual, \"matizar\" significa:", ["dar nuance ou precisão", "traduzir literalmente", "apagar o texto", "falar mais alto"], 0),
    ("Escolha a construção impessoal correta.", ["Se recomienda revisar los datos.", "Se recomiendan revisar los datos.", "Recomienda se revisar datos.", "Se recomendable los datos."], 0),
    ("Complete: Buscamos un enfoque que _____ el diálogo intercultural.", ["fortalece", "fortalezca", "fortaleció", "fortalecerá seguro"], 1),
    ("Qual frase reduz generalização cultural?", ["Sempre foi assim nesse povo.", "Conviene observar diferencias regionales e históricas.", "É tudo igual.", "Não há contexto relevante."], 1),
    ("Qual título é mais neutro?", ["La peor reforma de todos los tiempos", "Reforma genera debate entre expertos y ciudadanos", "Desastre absoluto no país", "Gobierno fracasa outra vez"], 1),
    ("No relatório profissional, escolha a frase mais precisa.", ["Me parece que tudo foi legal.", "Se identificaron tres riesgos y se propusieron dos acciones correctivas.", "A coisa melhorou bastante.", "Foi ótimo e pronto."], 1),
    ("Complete: Si bien el resultado es positivo, _____ revisar los próximos pasos.", ["conviene", "aunque", "porque de", "a lo mejor de"], 0),
    ("Qual opção mostra maturidade argumentativa?", ["Minha opinião é a única certa.", "O tema é complexo e exige considerar diferentes perspectivas.", "Quem discorda não entende.", "Não há nada para debater."], 1),
]

AVANCADO_QUESTIONS = _AVANCADO_QUIZ_10 + _AVANCADO_EXAM_40

QUESTION_BANKS = {
    "espanhol-basico": BASICO_QUESTIONS,
    "espanhol-intermediario": INTERMEDIARIO_QUESTIONS,
    "espanhol-avancado": AVANCADO_QUESTIONS,
}


# ---------------------------------------------------------------------------
# Criação no banco (mesmo padrão já validado no PLE)
# ---------------------------------------------------------------------------

def _make_question(question_text, options, correct_idx):
    if len(options) != 4:
        frappe.throw(f"Pergunta precisa ter exatamente 4 opções: {question_text}")
    if correct_idx not in range(4):
        frappe.throw(f"Índice da resposta correta inválido: {question_text}")

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


def _make_quiz(title, course, questions, *, max_attempts, passing_percentage, limit_questions_to):
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
    quiz.max_attempts = max_attempts
    quiz.passing_percentage = passing_percentage
    quiz.shuffle_questions = 1
    quiz.limit_questions_to = limit_questions_to
    quiz.total_marks = limit_questions_to or len(questions)
    quiz.set("questions", [])
    for question_text, options, correct_idx in questions:
        q_name = _make_question(question_text, options, correct_idx)
        quiz.append("questions", {"question": q_name, "marks": 1})

    if quiz.is_new():
        quiz.insert(ignore_permissions=True)
    else:
        quiz.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  ✓ Quiz '{title}' {action} ({len(questions)} questões no banco).")
    return quiz.name


def _ensure_final_exam_lesson(course, quiz_name, total_questions, sampled):
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
        f"Prova final do nível: {sampled or total_questions} questões por tentativa "
        f"(banco de {total_questions}), nota mínima de 70% e até 3 tentativas. A ordem "
        "muda a cada tentativa."
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
            print("  curso não existe -- rode create_espanhol_courses.run primeiro.")
            continue

        questions = QUESTION_BANKS[course]
        quiz_name = _make_quiz(
            data["quiz_title"], course, questions,
            max_attempts=data["max_attempts"],
            passing_percentage=data["passing_percentage"],
            limit_questions_to=data["limit_questions_to"],
        )
        _ensure_final_exam_lesson(course, quiz_name, len(questions), data["limit_questions_to"])
        _sync_navigation(course, schema)

    frappe.db.commit()
    print("\n✓ Quizzes de Espanhol configurados e navegação sincronizada.")
